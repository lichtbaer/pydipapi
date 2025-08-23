"""
Async client for the DIP API with rate limiting, retry logic, and caching.
"""

import asyncio
import logging
from typing import Any, Dict, Optional

import aiohttp
import json
from typing import Protocol, runtime_checkable, cast

from ..util.cache import SimpleCache
from ..util.error_handler import is_rate_limited, should_retry

logger = logging.getLogger(__name__)


class AsyncBaseApiClient:
    """
    Async base client for API requests with rate limiting, retry logic, and caching.
    """

    def __init__(self, api_key: str, base_url: str, rate_limit_delay: float = 0.1,
                 max_retries: int = 3, enable_cache: bool = True, cache_ttl: int = 3600):
        """
        Initialize the async base API client.

        Args:
            api_key (str): The API key for authentication.
            base_url (str): The base URL for the API.
            rate_limit_delay (float): Delay between requests in seconds.
            max_retries (int): Maximum number of retries for failed requests.
            enable_cache (bool): Whether to enable caching.
            cache_ttl (int): Cache time to live in seconds.
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.rate_limit_delay = rate_limit_delay
        self.max_retries = max_retries
        self.enable_cache = enable_cache
        self.cache = SimpleCache(ttl=cache_ttl) if enable_cache else None
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create the aiohttp session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers={'Content-Type': 'application/json'},
                timeout=aiohttp.ClientTimeout(total=30)
            )
        return self._session

@runtime_checkable
class _ResponseLike(Protocol):
    status: int
    async def json(self) -> Dict[str, Any]: ...
    async def text(self) -> str: ...
    headers: Dict[str, Any]

async def _make_request(self, url: str, params: Optional[Dict[str, Any]] = None,
                       use_cache: bool = True) -> Optional[aiohttp.ClientResponse]:
    """
    Make an async API request with rate limiting, retry logic, and optional caching.

    Args:
        url (str): The URL to request.
        params (Optional[Dict[str, Any]]): Query parameters.
        use_cache (bool): Whether to use caching for this request.

    Returns:
        aiohttp.ClientResponse: The response object.

    Raises:
        aiohttp.ClientError: If the request fails after all retries.
    """
    logger.debug(f"Making async request to URL: {url}")
    logger.debug(f"Parameters: {params}")
    logger.debug(f"Use cache: {use_cache}")

    # Check cache first if enabled
    if self.enable_cache and use_cache and self.cache:
        cached_data = self.cache.get(url, params)
        if cached_data:
            logger.debug("Returning cached response")
            class _CachedResponse:
                def __init__(self, data_json: Optional[Dict[str, Any]], headers: Dict[str, Any]):
                    self._data_json = data_json or {}
                    self.headers = headers or {}
                    self.status = 200

                async def json(self) -> Dict[str, Any]:
                    return self._data_json

                async def text(self) -> str:
                    return json.dumps(self._data_json)

            # Support both legacy 'content' bytes and new 'json' cache formats
            data_json: Optional[Dict[str, Any]] = None
            if 'json' in cached_data:
                data_json = cached_data.get('json')
            elif 'content' in cached_data:
                try:
                    data_json = json.loads(cached_data['content'].decode('utf-8'))
                except Exception:
                    data_json = None
            cached_resp: _ResponseLike = _CachedResponse(data_json, cached_data.get('headers', {}))
            # mypy: we're returning a compatible object; runtime users only use .json/.status
            return cast(Optional[aiohttp.ClientResponse], cached_resp)  # type: ignore[return-value]

    session = await self._get_session()
    attempt = 0
    response = None

    while attempt <= self.max_retries:
        try:
            # Rate limiting delay
            if attempt > 0:
                delay = self.rate_limit_delay * attempt
                logger.debug(f"Rate limiting delay: {delay}s (attempt {attempt})")
                await asyncio.sleep(delay)  # Async sleep

            logger.debug(f"Making async HTTP request (attempt {attempt + 1}/{self.max_retries + 1})")
            async with session.get(url, params=params) as response:
                logger.debug(f"Response status: {response.status}")
                logger.debug(f"Response headers: {dict(response.headers)}")

                # Check for rate limiting
                if is_rate_limited(response):
                    logger.warning(f"Rate limited - status: {response.status}")
                    if attempt < self.max_retries:
                        retry_after = int(response.headers.get('Retry-After', 60))
                        logger.info(f"Waiting {retry_after}s before retry")
                        await asyncio.sleep(retry_after)
                        attempt += 1
                        continue

                # Handle other errors
                try:
                    # Convert aiohttp response to requests-like response for error handling
                    response_text = await response.text()
                    # We'll handle errors differently for async
                    if response.status >= 400:
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                            message=f"HTTP {response.status}: {response.reason}"
                        )
                except Exception as e:
                    logger.error(f"handle_api_error failed: {e}")
                    logger.error(f"Response status: {response.status}")
                    response_text = await response.text()
                    logger.error(f"Response text: {response_text[:500]}...")

                    # Provide specific guidance for common errors
                    if response.status == 401:
                        logger.error("Authentication failed. Please check your API key.")
                        logger.error("You can get an API key from: https://dip.bundestag.de/über-dip/hilfe/api")
                    elif response.status == 403:
                        logger.error("Access forbidden. Your API key may not have the required permissions.")
                    elif response.status == 429:
                        logger.error("Rate limit exceeded. Please wait before making more requests.")

                    raise e

                # Cache successful responses (store JSON to be JSON-serializable)
                if self.enable_cache and use_cache and self.cache and response.status == 200:
                    logger.debug("Caching successful response")
                    try:
                        response_json = await response.json()
                        cache_data = {
                            'json': response_json,
                            'headers': dict(response.headers)
                        }
                        self.cache.set(url, cache_data, params)
                    except Exception:
                        # Fallback: ignore cache write errors silently (already logged by cache)
                        pass

                logger.debug(f"Request successful - status: {response.status}")
                return response

        except aiohttp.ClientError as e:
            logger.error(f"ClientError on attempt {attempt + 1}: {e}")
            if attempt < self.max_retries and response and should_retry(response, attempt, self.max_retries):
                logger.info(f"Retrying request (attempt {attempt + 1})")
                attempt += 1
                continue
            raise e
        except Exception as e:
            logger.error(f"Unexpected exception on attempt {attempt + 1}: {e}")
            if attempt < self.max_retries:
                logger.info(f"Retrying request (attempt {attempt + 1})")
                attempt += 1
                continue
            raise e

    # If we get here, all retries failed
    logger.error("Request failed after all retries")
    logger.error(f"URL: {url}")
    logger.error(f"Params: {params}")
    return None

    def _build_url(self, endpoint: str, **kwargs) -> str:
        """
        Build a URL for the given endpoint with optional parameters.

        Args:
            endpoint (str): The API endpoint.
            **kwargs: Query parameters.

        Returns:
            str: The complete URL.
        """
        url = f"{self.base_url}/{endpoint}"

        if kwargs:
            # Convert kwargs to query parameters
            params = []
            for key, value in kwargs.items():
                if value is not None:
                    if isinstance(value, list):
                        # Handle list parameters (e.g., f_id for multiple IDs)
                        for item in value:
                            params.append(f"{key}={item}")
                    else:
                        params.append(f"{key}={value}")

            if params:
                url += "?" + "&".join(params)

        return url

    async def _fetch_single_item(self, endpoint: str, item_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetch a single item by ID asynchronously.

        Args:
            endpoint (str): The API endpoint.
            item_id (int): The ID of the item to fetch.

        Returns:
            Optional[Dict[str, Any]]: The item data or None if not found.
        """
        url = f"{self.base_url}/{endpoint}/{item_id}/"
        response = await self._make_request(url)
        if response is None:
            return None
        data = await response.json()
        if data and 'documents' in data:
            documents = data['documents']
            return documents[0] if documents else None
        return None

    async def close(self):
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
