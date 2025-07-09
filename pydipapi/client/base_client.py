"""
Base client for API operations.
"""
import logging
import os
from typing import Any, Dict, List, Optional

import requests

from ..util.error_handling import DipApiError, handle_api_response, validate_api_key

logger = logging.getLogger(__name__)

class BaseApiClient:
    """
    Base class for Bundestag API client operations.

    Handles authentication, request building, and response processing.
    """
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the API client.

        Args:
            api_key: The API key for accessing the Bundestag API. If not provided, will attempt to use the 'DIP_API_KEY' environment variable.
        """
        self.api_key = validate_api_key(api_key or os.getenv('DIP_API_KEY'))
        self.base_url: str = "https://search.dip.bundestag.de/api/v1/"
        self.cursor = ""
        self.documents: List[Dict[str, Any]] = []

    def _build_url(self, endpoint: str, **params) -> str:
        """
        Build the complete URL for an API request.

        Args:
            endpoint: The API endpoint (e.g., 'person', 'aktivitaet')
            **params: Additional query parameters

        Returns:
            The complete URL with parameters
        """
        url = f"{self.base_url}{endpoint}?"
        if self.cursor:
            url += f"cursor={self.cursor}&"
        for key, value in params.items():
            if isinstance(value, list):
                for item in value:
                    url += f"&{key}={item}"
            else:
                url += f"&{key}={value}"
        url += f"&apikey={self.api_key}"
        return url

    def _make_request(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Make a GET request to the API.

        Args:
            url: The complete URL to request

        Returns:
            The JSON response data or None if an error occurred
        """
        try:
            response = requests.get(url=url, timeout=10)
            data = handle_api_response(response)
            if data:
                self.cursor = data.get('cursor', self.cursor)
                self.documents.extend(data.get('documents', []))
            return data
        except DipApiError:
            return None

    def _fetch_paginated_data(self, endpoint: str, count: int, **params) -> List[Dict[str, Any]]:
        """
        Fetch paginated data from the API.

        Args:
            endpoint: The API endpoint
            count: Number of items to fetch
            **params: Additional parameters for the request

        Returns:
            List of documents
        """
        self.documents = []
        while len(self.documents) < count:
            url = self._build_url(endpoint, **params)
            if not self._make_request(url):
                break
        return self.documents[:count]

    def _fetch_single_item(self, endpoint: str, item_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetch a single item by ID.

        Args:
            endpoint: The API endpoint
            item_id: The ID of the item to fetch

        Returns:
            The item data or None if not found
        """
        url = f"{self.base_url}{endpoint}/{item_id}/?apikey={self.api_key}"
        return self._make_request(url)
