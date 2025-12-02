"""
Error handling utilities for the DIP API client.
"""

import logging
from typing import Any, Dict, Optional, cast

import requests

logger = logging.getLogger(__name__)


def handle_api_error(response: requests.Response) -> None:
    """
    Handle API errors and raise appropriate exceptions.

    Args:
        response (requests.Response): The response object.

    Raises:
        DipApiHttpError: If the response indicates an HTTP error.
        DipApiConnectionError: If there's a connection error.
    """
    if response.status_code >= 400:
        try:
            error_data = response.json()
            error_message = error_data.get("message", "Unknown API error")
        except ValueError:
            error_message = f"HTTP {response.status_code}: {response.reason}"

        # Use custom exception instead of requests.HTTPError
        raise DipApiHttpError(response.status_code, error_message)


def is_rate_limited(response: Any) -> bool:
    """
    Check if the response indicates rate limiting.

    Args:
        response: The response object (requests or aiohttp).

    Returns:
        bool: True if rate limited, False otherwise.
    """
    # Prefer requests.Response.status_code; fallback to aiohttp's .status
    code = getattr(response, "status_code", None)
    if code is None:
        code = getattr(response, "status", None)

    try:
        code_int = int(code) if code is not None else 0
    except Exception:
        # Be defensive for mocks or unexpected types
        code_int = 0

    return code_int == 429


def should_retry(response: Any, attempt: int, max_retries: int) -> bool:
    """
    Determine if a request should be retried.

    Args:
        response: The response object (requests or aiohttp) or exception.
        attempt (int): Current attempt number.
        max_retries (int): Maximum number of retries.

    Returns:
        bool: True if should retry, False otherwise.
    """
    if attempt >= max_retries:
        return False

    # Retry on server errors (5xx) and rate limiting (429)
    # Prefer requests.Response.status_code; fallback to aiohttp's .status
    # Also support aiohttp.ClientResponseError which has .status
    code = getattr(response, "status_code", None)
    if code is None:
        code = getattr(response, "status", None)

    try:
        code_int = int(code) if code is not None else 0
    except Exception:
        # Be defensive for mocks or unexpected types
        code_int = 0

    return code_int >= 500 or code_int == 429


# Custom exception classes for pydipapi
class DipApiError(Exception):
    """Base exception for pydipapi errors."""

    pass


class DipApiConnectionError(DipApiError):
    """Raised when connection to the API fails."""

    pass


class DipApiHttpError(DipApiError):
    """Raised when the API returns an HTTP error."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"HTTP {status_code}: {message}")


def handle_api_response(response: requests.Response) -> Optional[Dict[str, Any]]:
    """
    Handle API response and return data or raise appropriate exceptions.

    Args:
        response: The requests.Response object from the API call.

    Returns:
        The JSON data from the response if successful.

    Raises:
        DipApiHttpError: If the response indicates an HTTP error.
        DipApiConnectionError: If there's a connection error.
    """
    try:
        response.raise_for_status()
        data = response.json()
        # Ensure we return a mapping as documented
        return cast(Optional[Dict[str, Any]], data if isinstance(data, dict) else None)
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        raise DipApiHttpError(response.status_code, str(http_err))
    except requests.exceptions.ConnectionError as conn_err:
        logger.error(f"Connection error occurred: {conn_err}")
        raise DipApiConnectionError(f"Connection failed: {conn_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise DipApiConnectionError(f"Request failed: {req_err}")
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        raise DipApiError(f"Unexpected error: {e}")


def handle_async_api_error(
    status_code: int, reason: str, response_text: Optional[str] = None
) -> None:
    """
    Handle async API errors and raise appropriate exceptions.

    Args:
        status_code: HTTP status code.
        reason: HTTP reason phrase.
        response_text: Optional response text for error message extraction.

    Raises:
        DipApiHttpError: If the response indicates an HTTP error.
    """
    if status_code >= 400:
        error_message = f"HTTP {status_code}: {reason}"
        
        # Try to extract error message from response text if available
        if response_text:
            try:
                import json
                error_data = json.loads(response_text)
                if isinstance(error_data, dict) and "message" in error_data:
                    error_message = error_data.get("message", error_message)
            except (ValueError, json.JSONDecodeError):
                pass
        
        raise DipApiHttpError(status_code, error_message)


def validate_api_key(api_key: Optional[str]) -> str:
    """
    Validate that an API key is provided.

    Args:
        api_key: The API key to validate.

    Returns:
        The validated API key.

    Raises:
        ValueError: If no API key is provided.
    """
    if not api_key:
        raise ValueError(
            "API key is required. Please provide an API key or set the DIP_API_KEY environment variable."
        )
    return api_key
