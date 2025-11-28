"""
Async client for the DIP API with rate limiting, retry logic, and caching.
"""

import asyncio
import json
import logging
from typing import Any, Dict, Optional, cast
from urllib.parse import urlencode

import aiohttp

from ..util.cache import SimpleCache
from ..util.error_handler import is_rate_limited, should_retry

logger = logging.getLogger(__name__)


class AsyncBaseApiClient:
    """
    Async base client for API requests with rate limiting, retry logic, and caching.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str,
        rate_limit_delay: float = 0.1,
        max_retries: int = 3,
        enable_cache: bool = True,
        cache_ttl: int = 3600,
        timeout: float = 30.0,
    ):
        """
        Initialize the async base API client.

        Args:
            api_key (str): The API key for authentication.
            base_url (str): The base URL for the API.
            rate_limit_delay (float): Delay between requests in seconds.
            max_retries (int): Maximum number of retries for failed requests.
            enable_cache (bool): Whether to enable caching.
            cache_ttl (int): Cache time to live in seconds.
            timeout (float): Request timeout in seconds. Default is 30.0.
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.rate_limit_delay = rate_limit_delay
        self.max_retries = max_retries
        self.enable_cache = enable_cache
        self.cache = SimpleCache(ttl=cache_ttl) if enable_cache else None
        self.timeout = timeout
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create the aiohttp session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers={"Content-Type": "application/json"},
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            )
        return self._session

    async def _make_request(
        self, url: str, params: Optional[Dict[str, Any]] = None, use_cache: bool = True
    ) -> Optional[aiohttp.ClientResponse]:
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
                    def __init__(
                        self,
                        data_json: Optional[Dict[str, Any]],
                        headers: Dict[str, Any],
                    ):
                        self._data_json = data_json or {}
                        self.headers = headers or {}
                        self.status = 200

                    async def json(self) -> Dict[str, Any]:
                        return self._data_json

                    async def text(self) -> str:
                        return json.dumps(self._data_json)

                # Support both legacy 'content' bytes and new 'json' cache formats
                data_json: Optional[Dict[str, Any]] = None
                if "json" in cached_data:
                    data_json = cached_data.get("json")
                elif "content" in cached_data:
                    try:
                        data_json = json.loads(cached_data["content"].decode("utf-8"))
                    except Exception:
                        data_json = None
                cached_resp = _CachedResponse(data_json, cached_data.get("headers", {}))
                return cast(Optional[aiohttp.ClientResponse], cached_resp)

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

                logger.debug(
                    f"Making async HTTP request (attempt {attempt + 1}/{self.max_retries + 1})"
                )
                async with session.get(url, params=params) as response:
                    logger.debug(f"Response status: {response.status}")
                    logger.debug(f"Response headers: {dict(response.headers)}")

                    # Check for rate limiting
                    if is_rate_limited(response):
                        logger.warning(f"Rate limited - status: {response.status}")
                        if attempt < self.max_retries:
                            retry_after = int(response.headers.get("Retry-After", 60))
                            logger.info(f"Waiting {retry_after}s before retry")
                            await asyncio.sleep(retry_after)
                            attempt += 1
                            continue

                    # Read response data while still in context manager
                    response_text = await response.text()
                    response_headers = dict(response.headers)
                    response_status = response.status

                    # Handle errors
                    if response_status >= 400:
                        logger.error(f"HTTP error: {response_status}")
                        logger.error(f"Response text: {response_text[:500]}...")

                        # Provide specific guidance for common errors
                        if response_status == 401:
                            logger.error(
                                "Authentication failed. Please check your API key."
                            )
                            logger.error(
                                "You can get an API key from: https://dip.bundestag.de/über-dip/hilfe/api"
                            )
                        elif response_status == 403:
                            logger.error(
                                "Access forbidden. Your API key may not have the required permissions."
                            )
                        elif response_status == 429:
                            logger.error(
                                "Rate limit exceeded. Please wait before making more requests."
                            )

                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response_status,
                            message=f"HTTP {response_status}: {response.reason}",
                        )

                    # Parse JSON while still in context manager
                    try:
                        response_json = json.loads(response_text) if response_text else {}
                    except json.JSONDecodeError:
                        logger.warning("Failed to parse response as JSON, returning empty dict")
                        response_json = {}

                    # Cache successful responses
                    if (
                        self.enable_cache
                        and use_cache
                        and self.cache
                        and response_status == 200
                    ):
                        logger.debug("Caching successful response")
                        try:
                            cache_data = {
                                "json": response_json,
                                "headers": response_headers,
                            }
                            self.cache.set(url, cache_data, params)
                        except Exception:
                            logger.exception("Failed to write response to cache")

                    # Create a wrapper object that mimics aiohttp.ClientResponse
                    # but contains the already-read data
                    class _ResponseWrapper:
                        def __init__(
                            self,
                            data_json: Dict[str, Any],
                            headers: Dict[str, Any],
                            status: int,
                        ):
                            self._data_json = data_json
                            self.headers = headers
                            self.status = status
                            self.request_info = getattr(response, "request_info", None)
                            self.history = getattr(response, "history", ())

                        async def json(self) -> Dict[str, Any]:
                            return self._data_json

                        async def text(self) -> str:
                            return json.dumps(self._data_json)

                    logger.debug(f"Request successful - status: {response_status}")
                    return cast(Optional[aiohttp.ClientResponse], _ResponseWrapper(
                        response_json, response_headers, response_status
                    ))

            except aiohttp.ClientError as e:
                logger.error(f"ClientError on attempt {attempt + 1}: {e}")
                # Check if we should retry based on the error type
                if attempt < self.max_retries:
                    # For ClientResponseError, check status code
                    if isinstance(e, aiohttp.ClientResponseError):
                        if should_retry(e, attempt, self.max_retries):
                            logger.info(f"Retrying request (attempt {attempt + 1})")
                            attempt += 1
                            continue
                    else:
                        # For other ClientErrors, retry
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

    def _build_url(self, endpoint: str, **kwargs: Any) -> str:
        """
        Build a URL for the given endpoint with optional parameters.

        Args:
            endpoint (str): The API endpoint.
            **kwargs: Query parameters.

        Returns:
            str: The complete URL with properly encoded parameters.
        """
        url = f"{self.base_url}/{endpoint}"

        if kwargs:
            # Convert kwargs to query parameters with proper URL encoding
            params_dict: Dict[str, Any] = {}
            for key, value in kwargs.items():
                if value is not None:
                    if isinstance(value, list):
                        # Handle list parameters (e.g., f_id for multiple IDs)
                        # For lists, we need to add multiple entries with the same key
                        params_dict[key] = value
                    else:
                        params_dict[key] = value

            if params_dict:
                # Use urlencode with doseq=True to handle lists properly
                query_string = urlencode(params_dict, doseq=True)
                url += "?" + query_string

        return url

    async def _fetch_single_item(
        self, endpoint: str, item_id: int
    ) -> Optional[Dict[str, Any]]:
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
        if data and "documents" in data:
            documents = data["documents"]
            return documents[0] if documents else None
        return None

    async def close(self) -> None:
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self) -> "AsyncBaseApiClient":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()
