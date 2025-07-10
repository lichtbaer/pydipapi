"""
Async API client for the German Bundestag DIP API.
"""

import logging
from typing import Any, Dict, List, Optional

from pydantic import parse_obj_as

from .client.async_client import AsyncBaseApiClient
from .type import Vorgangspositionbezug

logger = logging.getLogger(__name__)


class AsyncDipAnfrage(AsyncBaseApiClient):
    """
    Async client for the German Bundestag DIP API.

    This client provides async versions of all API methods for better performance
    when making multiple concurrent requests.
    """

    def __init__(self, api_key: str, base_url: str = "https://search.dip.bundestag.de/api/v1",
                 rate_limit_delay: float = 0.1, max_retries: int = 3,
                 enable_cache: bool = True, cache_ttl: int = 3600):
        """
        Initialize the async DIP API client.

        Args:
            api_key (str): The API key for authentication.
            base_url (str): The base URL for the API.
            rate_limit_delay (float): Delay between requests in seconds.
            max_retries (int): Maximum number of retries for failed requests.
            enable_cache (bool): Whether to enable caching.
            cache_ttl (int): Cache time to live in seconds.
        """
        super().__init__(api_key, base_url, rate_limit_delay, max_retries, enable_cache, cache_ttl)

    async def _make_request(self, url: str) -> Optional[dict]:
        """
        Make an async API request and return JSON data.

        Args:
            url (str): The URL to request.

        Returns:
            Optional[dict]: The JSON response data or None if failed.
        """
        try:
            response = await super()._make_request(url)
            if response is None:
                return None
            return await response.json()
        except Exception as e:
            logger.error(f"Error making async request to {url}: {e}")
            return None

    async def _fetch_paginated_data(self, endpoint: str, count: int, **params) -> List[Dict[str, Any]]:
        """
        Fetch paginated data from the API asynchronously.

        Args:
            endpoint (str): The API endpoint.
            count (int): Number of items to fetch.
            **params: Additional parameters for the request.

        Returns:
            List[Dict[str, Any]]: List of documents.
        """
        logger.debug(f"Fetching async paginated data from endpoint: {endpoint}, count: {count}, params: {params}")
        documents = []
        cursor = ""

        while len(documents) < count:
            # Add cursor to parameters if we have one
            if cursor:
                params['cursor'] = cursor

            url = self._build_url(endpoint, **params)
            logger.debug(f"Making async request to URL: {url}")

            data = await self._make_request(url)
            if data is None:
                logger.error("No response received from async _make_request")
                break

            logger.debug(f"Response data type: {type(data)}")
            logger.debug(f"Response data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")

            if not data:
                logger.warning("Empty response data")
                break

            new_documents = data.get('documents', []) if isinstance(data, dict) else []
            logger.debug(f"Retrieved {len(new_documents)} new documents")
            documents.extend(new_documents)

            # Update cursor for next page
            cursor = data.get('cursor', '') if isinstance(data, dict) else ''
            logger.debug(f"Next cursor: {cursor}")

            # If no more documents or no cursor, break
            if not new_documents or not cursor:
                logger.debug("No more documents or no cursor, stopping pagination")
                break

        logger.info(f"Total documents retrieved: {len(documents)}")
        return documents[:count]

    async def get_person(self, anzahl: int = 100, **filters) -> List[dict]:
        """
        Retrieve a list of persons from the API asynchronously.

        Args:
            anzahl (int): Number of persons to retrieve.
            **filters: Arbitrary filter parameters as keyword arguments.

        Returns:
            List[dict]: A list of person dictionaries.
        """
        try:
            result = await self._fetch_paginated_data('person', anzahl, **filters)
            return result or []
        except Exception as e:
            logger.error(f"Error fetching persons: {e}")
            return []

    async def get_person_ids(self, ids: List[int]) -> List[dict]:
        """
        Retrieve multiple persons by their IDs asynchronously.

        Args:
            ids (List[int]): List of person IDs.

        Returns:
            List[dict]: A list of person dictionaries.
        """
        if not ids:
            return []

        try:
            # Use batch endpoint if available, otherwise fetch individually
            url = self._build_url('person', f_id=ids)
            data = await self._make_request(url)
            if data and 'documents' in data:
                return data['documents']
            return []
        except Exception as e:
            logger.error(f"Error fetching person IDs: {e}")
            return []

    async def get_aktivitaet_ids(self, ids: List[int]) -> List[dict]:
        """
        Retrieve multiple activities by their IDs asynchronously.

        Args:
            ids (List[int]): List of activity IDs.

        Returns:
            List[dict]: A list of activity dictionaries.
        """
        if not ids:
            return []

        try:
            url = self._build_url('aktivitaet', f_id=ids)
            data = await self._make_request(url)
            if data and 'documents' in data:
                return data['documents']
            return []
        except Exception as e:
            logger.error(f"Error fetching activity IDs: {e}")
            return []

    async def get_drucksache_ids(self, ids: List[int], text: bool = True) -> List[dict]:
        """
        Retrieve multiple documents by their IDs asynchronously.

        Args:
            ids (List[int]): List of document IDs.
            text (bool): Whether to retrieve text versions.

        Returns:
            List[dict]: A list of document dictionaries.
        """
        if not ids:
            return []

        try:
            endpoint = 'drucksache-text' if text else 'drucksache'
            url = self._build_url(endpoint, f_id=ids)
            data = await self._make_request(url)
            if data and 'documents' in data:
                return data['documents']
            return []
        except Exception as e:
            logger.error(f"Error fetching document IDs: {e}")
            return []

    async def get_plenarprotokoll_ids(self, ids: List[int], text: bool = True) -> List[dict]:
        """
        Retrieve multiple plenary protocols by their IDs asynchronously.

        Args:
            ids (List[int]): List of protocol IDs.
            text (bool): Whether to retrieve text versions.

        Returns:
            List[dict]: A list of protocol dictionaries.
        """
        if not ids:
            return []

        try:
            endpoint = 'plenarprotokoll-text' if text else 'plenarprotokoll'
            url = self._build_url(endpoint, f_id=ids)
            data = await self._make_request(url)
            if data and 'documents' in data:
                return data['documents']
            return []
        except Exception as e:
            logger.error(f"Error fetching protocol IDs: {e}")
            return []

    async def get_vorgang_ids(self, ids: List[int]) -> List[dict]:
        """
        Retrieve multiple proceedings by their IDs asynchronously.

        Args:
            ids (List[int]): List of proceeding IDs.

        Returns:
            List[dict]: A list of proceeding dictionaries.
        """
        if not ids:
            return []

        try:
            url = self._build_url('vorgang', f_id=ids)
            data = await self._make_request(url)
            if data and 'documents' in data:
                return data['documents']
            return []
        except Exception as e:
            logger.error(f"Error fetching proceeding IDs: {e}")
            return []

    async def get_vorgangsposition_ids(self, ids: List[int]) -> List[dict]:
        """
        Retrieve multiple proceeding positions by their IDs asynchronously.

        Args:
            ids (List[int]): List of proceeding position IDs.

        Returns:
            List[dict]: A list of proceeding position dictionaries.
        """
        if not ids:
            return []

        try:
            url = self._build_url('vorgangsposition', f_id=ids)
            data = await self._make_request(url)
            if data and 'documents' in data:
                return data['documents']
            return []
        except Exception as e:
            logger.error(f"Error fetching proceeding position IDs: {e}")
            return []

    async def search_documents(self, query: str, anzahl: int = 10, **filters) -> List[dict]:
        """
        Search for documents asynchronously.

        Args:
            query (str): The search query.
            anzahl (int): Number of results to retrieve.
            **filters: Additional filter parameters.

        Returns:
            List[dict]: A list of matching documents.
        """
        try:
            filters['q'] = query
            result = await self._fetch_paginated_data('search', anzahl, **filters)
            return result or []
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return []

    async def get_recent_activities(self, days: int = 7, anzahl: int = 20) -> List[dict]:
        """
        Get recent activities from the last N days asynchronously.

        Args:
            days (int): Number of days to look back.
            anzahl (int): Number of activities to retrieve.

        Returns:
            List[dict]: A list of recent activities.
        """
        try:
            # Calculate date range
            from datetime import datetime, timedelta
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            filters = {
                'datum_von': start_date.strftime('%Y-%m-%d'),
                'datum_bis': end_date.strftime('%Y-%m-%d')
            }

            result = await self._fetch_paginated_data('aktivitaet', anzahl, **filters)
            return result or []
        except Exception as e:
            logger.error(f"Error fetching recent activities: {e}")
            return []

    async def get_person_by_name(self, name: str, anzahl: int = 10) -> List[dict]:
        """
        Search for persons by name asynchronously.

        Args:
            name (str): The name to search for.
            anzahl (int): Number of results to retrieve.

        Returns:
            List[dict]: A list of matching persons.
        """
        try:
            # Use f.person parameter for name-based search according to API documentation
            result = await self._fetch_paginated_data('person', anzahl, **{'f.person': name})
            return result or []
        except Exception as e:
            logger.error(f"Error searching persons by name: {e}")
            return []

    async def get_documents_by_type(self, doc_type: str, anzahl: int = 20, **filters) -> List[dict]:
        """
        Get documents by type asynchronously.

        Args:
            doc_type (str): The document type (e.g., 'kleine_anfrage', 'grosse_anfrage').
            anzahl (int): Number of documents to retrieve.
            **filters: Additional filter parameters.

        Returns:
            List[dict]: A list of documents of the specified type.
        """
        try:
            filters['dokumentart'] = doc_type
            result = await self._fetch_paginated_data('drucksache', anzahl, **filters)
            return result or []
        except Exception as e:
            logger.error(f"Error fetching documents by type: {e}")
            return []

    async def get_proceedings_by_type(self, proc_type: str, anzahl: int = 20, **filters) -> List[dict]:
        """
        Get proceedings by type asynchronously.

        Args:
            proc_type (str): The proceeding type.
            anzahl (int): Number of proceedings to retrieve.
            **filters: Additional filter parameters.

        Returns:
            List[dict]: A list of proceedings of the specified type.
        """
        try:
            filters['vorgangstyp'] = proc_type
            result = await self._fetch_paginated_data('vorgang', anzahl, **filters)
            return result or []
        except Exception as e:
            logger.error(f"Error fetching proceedings by type: {e}")
            return []

    async def get_person_id(self, id: int) -> Optional[dict]:
        """
        Retrieve a single person by ID asynchronously.

        Args:
            id (int): The ID of the person.

        Returns:
            Optional[dict]: The person dictionary or None if not found.
        """
        return await self._fetch_single_item('person', id)

    async def get_aktivitaet(self, anzahl: int = 100, **filters) -> List[dict]:
        """
        Retrieve a list of activities from the API asynchronously.

        Args:
            anzahl (int): Number of activities to retrieve.
            **filters: Arbitrary filter parameters as keyword arguments.

        Returns:
            List[dict]: A list of activity dictionaries.
        """
        try:
            result = await self._fetch_paginated_data('aktivitaet', anzahl, **filters)
            return result or []
        except Exception as e:
            logger.error(f"Error fetching activities: {e}")
            return []

    async def get_drucksache(self, anzahl: int = 10, text: bool = True, **filters) -> List[dict]:
        """
        Retrieve a list of documents (Drucksache) from the API asynchronously.

        Args:
            anzahl (int): Number of documents to retrieve.
            text (bool): Whether to retrieve text versions.
            **filters: Arbitrary filter parameters as keyword arguments.

        Returns:
            List[dict]: A list of document dictionaries.
        """
        try:
            endpoint = 'drucksache-text' if text else 'drucksache'
            result = await self._fetch_paginated_data(endpoint, anzahl, **filters)
            return result or []
        except Exception as e:
            logger.error(f"Error fetching documents: {e}")
            return []

    async def get_plenarprotokoll(self, anzahl: int = 10, text: bool = True, **filters) -> List[dict]:
        """
        Retrieve a list of plenary protocols from the API asynchronously.

        Args:
            anzahl (int): Number of protocols to retrieve.
            text (bool): Whether to retrieve text protocols.
            **filters: Arbitrary filter parameters as keyword arguments.

        Returns:
            List[dict]: A list of protocol dictionaries.
        """
        try:
            endpoint = 'plenarprotokoll-text' if text else 'plenarprotokoll'
            result = await self._fetch_paginated_data(endpoint, anzahl, **filters)
            return result or []
        except Exception as e:
            logger.error(f"Error fetching protocols: {e}")
            return []

    async def get_vorgang(self, anzahl: int = 10, **filters) -> List[dict]:
        """
        Retrieve a list of proceedings (Vorgang) from the API asynchronously.

        Args:
            anzahl (int): Number of proceedings to retrieve.
            **filters: Arbitrary filter parameters as keyword arguments.

        Returns:
            List[dict]: A list of proceedings.
        """
        try:
            result = await self._fetch_paginated_data('vorgang', anzahl, **filters)
            return result or []
        except Exception as e:
            logger.error(f"Error fetching proceedings: {e}")
            return []

    async def get_vorgangsposition(self, anzahl: int = 10, **filters) -> List[Vorgangspositionbezug]:
        """
        Retrieve a list of proceeding positions (Vorgangsposition) from the API asynchronously.

        Args:
            anzahl (int): Number of proceeding positions to retrieve.
            **filters: Arbitrary filter parameters as keyword arguments.

        Returns:
            List[Vorgangspositionbezug]: A list of proceeding positions.
        """
        try:
            documents = await self._fetch_paginated_data('vorgangsposition', anzahl, **filters)
            return parse_obj_as(List[Vorgangspositionbezug], documents)
        except Exception as e:
            logger.error(f"Error fetching proceeding positions: {e}")
            return []

    # Single item retrieval methods
    async def get_aktivitaet_by_id(self, id: int) -> Optional[dict]:
        """Retrieve a single activity by its ID asynchronously."""
        return await self._fetch_single_item('aktivitaet', id)

    async def get_drucksache_by_id(self, id: int) -> Optional[dict]:
        """Retrieve a single document (Drucksache) by its ID asynchronously."""
        return await self._fetch_single_item('drucksache', id)

    async def get_drucksache_text_by_id(self, id: int) -> Optional[dict]:
        """Retrieve a single document (Drucksache) with text by its ID asynchronously."""
        return await self._fetch_single_item('drucksache-text', id)

    async def get_plenarprotokoll_by_id(self, id: int) -> Optional[dict]:
        """Retrieve a single plenary protocol by its ID asynchronously."""
        return await self._fetch_single_item('plenarprotokoll', id)

    async def get_plenarprotokoll_text_by_id(self, id: int) -> Optional[dict]:
        """Retrieve a single plenary protocol (with text) by its ID asynchronously."""
        return await self._fetch_single_item('plenarprotokoll-text', id)

    async def get_vorgang_by_id(self, id: int) -> Optional[dict]:
        """Retrieve a single proceeding (Vorgang) by its ID asynchronously."""
        return await self._fetch_single_item('vorgang', id)

    async def get_vorgangsposition_by_id(self, id: int) -> Optional[dict]:
        """Retrieve a single proceeding position (Vorgangsposition) by its ID asynchronously."""
        return await self._fetch_single_item('vorgangsposition', id)

    # Cache management methods
    def clear_cache(self) -> None:
        """Clear the response cache."""
        if self.cache:
            self.cache.clear()

    def clear_expired_cache(self) -> None:
        """Clear expired cache entries."""
        if self.cache:
            self.cache.clear_expired()
