"""
Error handling utilities for the DIP API client.
"""

from typing import Any

import requests


def handle_api_error(response: requests.Response) -> None:
    """
    Handle API errors and raise appropriate exceptions.

    Args:
        response (requests.Response): The response object.

    Raises:
        requests.HTTPError: If the response indicates an error.
    """
    if response.status_code >= 400:
        try:
            error_data = response.json()
            error_message = error_data.get("message", "Unknown API error")
        except ValueError:
            error_message = f"HTTP {response.status_code}: {response.reason}"

        raise requests.HTTPError(
            f"API request failed: {error_message}", response=response
        )


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
        response: The response object (requests or aiohttp).
        attempt (int): Current attempt number.
        max_retries (int): Maximum number of retries.

    Returns:
        bool: True if should retry, False otherwise.
    """
    if attempt >= max_retries:
        return False

    # Retry on server errors (5xx) and rate limiting (429)
    # Prefer requests.Response.status_code; fallback to aiohttp's .status
    code = getattr(response, "status_code", None)
    if code is None:
        code = getattr(response, "status", None)

    try:
        code_int = int(code) if code is not None else 0
    except Exception:
        # Be defensive for mocks or unexpected types
        code_int = 0

    return code_int >= 500 or code_int == 429
