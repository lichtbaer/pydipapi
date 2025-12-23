"""
Legacy-style error handling helpers.

Tests (and some downstream code) expect a module named `pydipapi.util.error_handling`
that provides:
- validate_api_key()
- handle_api_response()
- DipApiError / DipApiHttpError / DipApiConnectionError

The newer clients also use `pydipapi.util.error_handler` for retry / rate-limit
logic. This module intentionally focuses on the simple, request/response-oriented
helpers used by unit tests.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional, cast

import requests

logger = logging.getLogger(__name__)


class DipApiError(Exception):
    """Base exception for pydipapi errors."""


class DipApiConnectionError(DipApiError):
    """Raised when connection to the API fails."""


class DipApiHttpError(DipApiError):
    """Raised when the API returns an HTTP error."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"HTTP {status_code}: {message}")


def validate_api_key(api_key: Optional[str]) -> str:
    """
    Validate that the API key is present and non-empty.
    """
    if api_key is None:
        raise ValueError("API key must not be None")
    if api_key == "":
        raise ValueError("API key must not be empty")
    return api_key


def handle_api_response(response: requests.Response) -> Optional[Dict[str, Any]]:
    """
    Handle API response and return JSON data or raise appropriate exceptions.
    """
    try:
        response.raise_for_status()
        data = response.json()
        return cast(Optional[Dict[str, Any]], data if isinstance(data, dict) else None)
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        raise DipApiHttpError(getattr(response, "status_code", 0) or 0, str(http_err))
    except requests.exceptions.ConnectionError as conn_err:
        logger.error(f"Connection error occurred: {conn_err}")
        raise DipApiConnectionError(f"Connection failed: {conn_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise DipApiConnectionError(f"Request failed: {req_err}")
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        raise DipApiError(f"Unexpected error: {e}")

