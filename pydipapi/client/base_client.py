"""
Base client for API operations.
"""
import logging
import time
from typing import Any, Dict, Optional

import requests

from ..util.cache import SimpleCache
from ..util.error_handler import handle_api_error, is_rate_limited, should_retry

logger = logging.getLogger(__name__)

class BaseApiClient:
    """
    Base client for API requests with rate limiting, retry logic, and caching.
    """

    def __init__(self, api_key: str, base_url: str, rate_limit_delay: float = 0.1,
                 max_retries: int = 3, enable_cache: bool = True, cache_ttl: int = 3600):
        """
        Initialize the base API client.

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

        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })

    def _make_request(self, url: str, params: Optional[Dict[str, Any]] = None,
                     use_cache: bool = True) -> Optional[requests.Response]:
        """
        Make an API request with rate limiting, retry logic, and optional caching.

        Args:
            url (str): The URL to request.
            params (Optional[Dict[str, Any]]): Query parameters.
            use_cache (bool): Whether to use caching for this request.

        Returns:
            requests.Response: The response object.

        Raises:
            requests.HTTPError: If the request fails after all retries.
        """
        logger.debug(f"Making request to URL: {url}")
        logger.debug(f"Parameters: {params}")
        logger.debug(f"Use cache: {use_cache}")

        # Check cache first if enabled
        if self.enable_cache and use_cache and self.cache:
            cached_data = self.cache.get(url, params)
            if cached_data:
                logger.debug("Returning cached response")
                # Create a mock response object with cached data
                response = requests.Response()
                response.status_code = 200
                response._content = cached_data.get('content', b'{}')
                response.headers = cached_data.get('headers', {})
                return response

        attempt = 0
        response = None

        while attempt <= self.max_retries:
            try:
                # Rate limiting delay
                if attempt > 0:
                    delay = self.rate_limit_delay * attempt
                    logger.debug(f"Rate limiting delay: {delay}s (attempt {attempt})")
                    time.sleep(delay)  # Exponential backoff

                logger.debug(f"Making HTTP request (attempt {attempt + 1}/{self.max_retries + 1})")
                response = self.session.get(url, params=params, timeout=30)
                logger.debug(f"Response status: {response.status_code}")
                logger.debug(f"Response headers: {dict(response.headers)}")

                # Check for rate limiting
                if is_rate_limited(response):
                    logger.warning(f"Rate limited - status: {response.status_code}")
                    if attempt < self.max_retries:
                        retry_after = int(response.headers.get('Retry-After', 60))
                        logger.info(f"Waiting {retry_after}s before retry")
                        time.sleep(retry_after)
                        attempt += 1
                        continue

                # Handle other errors
                try:
                    handle_api_error(response)
                except Exception as e:
                    logger.error(f"handle_api_error failed: {e}")
                    logger.error(f"Response status: {response.status_code}")
                    logger.error(f"Response text: {response.text[:500]}...")

                    # Provide specific guidance for common errors
                    if response.status_code == 401:
                        logger.error("Authentication failed. Please check your API key.")
                        logger.error("You can get an API key from: https://dip.bundestag.de/über-dip/hilfe/api")
                    elif response.status_code == 403:
                        logger.error("Access forbidden. Your API key may not have the required permissions.")
                    elif response.status_code == 429:
                        logger.error("Rate limit exceeded. Please wait before making more requests.")

                    raise e

                # Cache successful responses
                if self.enable_cache and use_cache and self.cache and response.status_code == 200:
                    logger.debug("Caching successful response")
                    cache_data = {
                        'content': response.content,
                        'headers': dict(response.headers)
                    }
                    self.cache.set(url, cache_data, params)

                logger.debug(f"Request successful - status: {response.status_code}")
                return response

            except requests.RequestException as e:
                logger.error(f"RequestException on attempt {attempt + 1}: {e}")
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

    def _fetch_single_item(self, endpoint: str, item_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetch a single item by ID.

        Args:
            endpoint (str): The API endpoint.
            item_id (int): The ID of the item to fetch.

        Returns:
            Optional[Dict[str, Any]]: The item data or None if not found.
        """
        url = f"{self.base_url}/{endpoint}/{item_id}/"
        response = self._make_request(url)
        if response is None:
            return None
        data = response.json()
        if data and 'documents' in data:
            documents = data['documents']
            return documents[0] if documents else None
        return None
