"""
Error handling utilities for the DIP API client.
"""


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
            error_message = error_data.get('message', 'Unknown API error')
        except ValueError:
            error_message = f"HTTP {response.status_code}: {response.reason}"

        raise requests.HTTPError(
            f"API request failed: {error_message}",
            response=response
        )


def is_rate_limited(response: requests.Response) -> bool:
    """
    Check if the response indicates rate limiting.

    Args:
        response (requests.Response): The response object.

    Returns:
        bool: True if rate limited, False otherwise.
    """
    return response.status_code == 429


def should_retry(response: requests.Response, attempt: int, max_retries: int) -> bool:
    """
    Determine if a request should be retried.

    Args:
        response (requests.Response): The response object.
        attempt (int): Current attempt number.
        max_retries (int): Maximum number of retries.

    Returns:
        bool: True if should retry, False otherwise.
    """
    if attempt >= max_retries:
        return False

    # Retry on server errors (5xx) and rate limiting (429)
    return response.status_code >= 500 or response.status_code == 429
