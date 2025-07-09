"""
Error handling utilities for the pydipapi package.
"""
import logging
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)


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
        return response.json()
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
        raise ValueError("API key is required. Please provide an API key or set the DIP_API_KEY environment variable.")
    return api_key
