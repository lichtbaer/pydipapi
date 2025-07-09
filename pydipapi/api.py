"""
Main API client for the German Bundestag API.
"""
from typing import List, Optional

from pydantic import parse_obj_as

from .client.base_client import BaseApiClient
from .type import Vorgangspositionbezug


class DipAnfrage(BaseApiClient):
    """
    A client for the German Bundestag API (DIP).

    This class provides methods to retrieve various types of data from the
    German Bundestag API, including persons, activities, documents,
    plenary protocols, proceedings, and proceeding positions.
    """

    def __init__(self, api_key: str, base_url: str = "https://search.dip.bundestag.de/api/v1",
                 rate_limit_delay: float = 0.1, max_retries: int = 3,
                 enable_cache: bool = True, cache_ttl: int = 3600):
        """
        Initialize the DIP API client.

        Args:
            api_key (str): The API key for authentication.
            base_url (str): The base URL for the API.
            rate_limit_delay (float): Delay between requests in seconds.
            max_retries (int): Maximum number of retries for failed requests.
            enable_cache (bool): Whether to enable caching.
            cache_ttl (int): Cache time to live in seconds.
        """
        super().__init__(api_key, base_url, rate_limit_delay, max_retries, enable_cache, cache_ttl)
        self.documents = []

    def _make_request(self, url: str) -> None:
        """
        Make a request and update the documents list.

        Args:
            url (str): The URL to request.
        """
        response = super()._make_request(url)
        data = response.json()

        if data:
            self.documents.extend(data.get('documents', []))

    def _build_url(self, endpoint: str, **kwargs) -> str:
        """
        Build a URL for the given endpoint with parameters.

        Args:
            endpoint (str): The API endpoint.
            **kwargs: Query parameters.

        Returns:
            str: The complete URL.
        """
        # Add API key to parameters
        kwargs['apikey'] = self.api_key
        return super()._build_url(endpoint, **kwargs)

    def get_person(self, anzahl: int = 100, **filters) -> List[dict]:
        """
        Retrieve a list of persons from the API.

        Args:
            anzahl (int): Number of persons to retrieve.
            **filters: Arbitrary filter parameters as keyword arguments (e.g. wahlperiode=20, aktualisiert_start="2022-01-01T00:00:00").

        Returns:
            List[dict]: A list of person dictionaries.
        """
        try:
            result = self._fetch_paginated_data('person', anzahl, **filters)
            return result or []
        except Exception:
            return []

    def get_person_ids(self, ids: List[int]) -> List[dict]:
        """
        Retrieve persons by their IDs.

        Args:
            ids (List[int]): A list of person IDs.

        Returns:
            List[dict]: A list of person dictionaries.
        """
        self.documents = []
        url = self._build_url("person", f_id=ids)
        self._make_request(url)
        return self.documents

    def get_aktivitaet_ids(self, ids: List[int]) -> List[dict]:
        """
        Retrieve activities by their IDs.

        Args:
            ids (List[int]): A list of activity IDs.

        Returns:
            List[dict]: A list of activity dictionaries.
        """
        self.documents = []
        url = self._build_url("aktivitaet", f_id=ids)
        self._make_request(url)
        return self.documents

    def get_drucksache_ids(self, ids: List[int], text: bool = True) -> List[dict]:
        """
        Retrieve documents by their IDs.

        Args:
            ids (List[int]): A list of document IDs.
            text (bool): Whether to retrieve text documents.

        Returns:
            List[dict]: A list of document dictionaries.
        """
        self.documents = []
        endpoint = 'drucksache-text' if text else 'drucksache'
        url = self._build_url(endpoint, f_id=ids)
        self._make_request(url)
        return self.documents

    def get_plenarprotokoll_ids(self, ids: List[int], text: bool = True) -> List[dict]:
        """
        Retrieve plenary protocols by their IDs.

        Args:
            ids (List[int]): A list of protocol IDs.
            text (bool): Whether to retrieve text protocols.

        Returns:
            List[dict]: A list of protocol dictionaries.
        """
        self.documents = []
        endpoint = 'plenarprotokoll-text' if text else 'plenarprotokoll'
        url = self._build_url(endpoint, f_id=ids)
        self._make_request(url)
        return self.documents

    def get_vorgang_ids(self, ids: List[int]) -> List[dict]:
        """
        Retrieve proceedings by their IDs.

        Args:
            ids (List[int]): A list of proceeding IDs.

        Returns:
            List[dict]: A list of proceeding dictionaries.
        """
        self.documents = []
        url = self._build_url("vorgang", f_id=ids)
        self._make_request(url)
        return self.documents

    def get_vorgangsposition_ids(self, ids: List[int]) -> List[dict]:
        """
        Retrieve proceeding positions by their IDs.

        Args:
            ids (List[int]): A list of proceeding position IDs.

        Returns:
            List[dict]: A list of proceeding position dictionaries.
        """
        self.documents = []
        url = self._build_url("vorgangsposition", f_id=ids)
        self._make_request(url)
        return self.documents

    def search_documents(self, query: str, anzahl: int = 10, **filters) -> List[dict]:
        """
        Search for documents with a text query.

        Args:
            query (str): The search query.
            anzahl (int): Number of results to return.
            **filters: Additional filter parameters.

        Returns:
            List[dict]: List of matching documents.
        """
        self.documents = []
        filters['q'] = query
        url = self._build_url("drucksache", anzahl=anzahl, **filters)
        self._make_request(url)
        return self.documents

    def get_recent_activities(self, days: int = 7, anzahl: int = 20) -> List[dict]:
        """
        Get recent activities from the last N days.

        Args:
            days (int): Number of days to look back.
            anzahl (int): Number of results to return.

        Returns:
            List[dict]: List of recent activities.
        """
        from datetime import datetime, timedelta

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        result = self.get_aktivitaet(
            anzahl=anzahl,
            datum_start=start_date.strftime("%Y-%m-%d"),
            datum_end=end_date.strftime("%Y-%m-%d")
        )
        return result or []

    def get_person_by_name(self, name: str, anzahl: int = 10) -> List[dict]:
        """
        Search for persons by name.

        Args:
            name (str): The name to search for.
            anzahl (int): Number of results to return.

        Returns:
            List[dict]: List of matching persons.
        """
        result = self.get_person(anzahl=anzahl, titel=name)
        return result or []

    def get_documents_by_type(self, doc_type: str, anzahl: int = 20, **filters) -> List[dict]:
        """
        Get documents by type.

        Args:
            doc_type (str): The document type (e.g., 'Antrag', 'Gesetzentwurf').
            anzahl (int): Number of results to return.
            **filters: Additional filter parameters.

        Returns:
            List[dict]: List of documents of the specified type.
        """
        filters['drucksachetyp'] = doc_type
        result = self.get_drucksache(anzahl=anzahl, **filters)
        return result or []

    def get_proceedings_by_type(self, proc_type: str, anzahl: int = 20, **filters) -> List[dict]:
        """
        Get proceedings by type.

        Args:
            proc_type (str): The proceeding type (e.g., 'Gesetzgebung', 'Antrag').
            anzahl (int): Number of results to return.
            **filters: Additional filter parameters.

        Returns:
            List[dict]: List of proceedings of the specified type.
        """
        filters['vorgangstyp'] = proc_type
        result = self.get_vorgang(anzahl=anzahl, **filters)
        return result or []

    def get_person_id(self, id: int) -> Optional[dict]:
        """
        Retrieve a single person by their ID.

        Args:
            id (int): The ID of the person.

        Returns:
            Optional[dict]: The person dictionary or None if not found.
        """
        return self._fetch_single_item('person', id)

    def get_aktivitaet(self, anzahl: int = 100, **filters) -> List[dict]:
        """
        Retrieve a list of activities from the API.

        Args:
            anzahl (int): Number of activities to retrieve.
            **filters: Arbitrary filter parameters as keyword arguments.

        Returns:
            List[dict]: A list of activity dictionaries.
        """
        try:
            result = self._fetch_paginated_data('aktivitaet', anzahl, **filters)
            return result or []
        except Exception:
            return []

    def get_drucksache(self, anzahl: int = 10, text: bool = True, **filters) -> List[dict]:
        """
        Retrieve a list of documents (Drucksache) from the API.

        Args:
            anzahl (int): Number of documents to retrieve.
            text (bool): Whether to retrieve text documents.
            **filters: Arbitrary filter parameters as keyword arguments.

        Returns:
            List[dict]: A list of document dictionaries.
        """
        try:
            endpoint = 'drucksache-text' if text else 'drucksache'
            result = self._fetch_paginated_data(endpoint, anzahl, **filters)
            return result or []
        except Exception:
            return []

    def get_plenarprotokoll(self, anzahl: int = 10, text: bool = True, **filters) -> List[dict]:
        """
        Retrieve a list of plenary protocols from the API.

        Args:
            anzahl (int): Number of protocols to retrieve.
            text (bool): Whether to retrieve text protocols.
            **filters: Arbitrary filter parameters as keyword arguments.

        Returns:
            List[dict]: A list of protocol dictionaries.
        """
        endpoint = 'plenarprotokoll-text' if text else 'plenarprotokoll'
        return self._fetch_paginated_data(endpoint, anzahl, **filters)

    def get_vorgang(self, anzahl: int = 10, **filters) -> List[dict]:
        """
        Retrieve a list of proceedings (Vorgang) from the API.

        Args:
            anzahl (int): Number of proceedings to retrieve.
            **filters: Arbitrary filter parameters as keyword arguments.

        Returns:
            List[dict]: A list of proceedings.
        """
        return self._fetch_paginated_data('vorgang', anzahl, **filters)

    def get_vorgangsposition(self, anzahl: int = 10, **filters) -> List[Vorgangspositionbezug]:
        """
        Retrieve a list of proceeding positions (Vorgangsposition) from the API.

        Args:
            anzahl (int): Number of proceeding positions to retrieve.
            **filters: Arbitrary filter parameters as keyword arguments.

        Returns:
            List[Vorgangspositionbezug]: A list of proceeding positions.
        """
        documents = self._fetch_paginated_data('vorgangsposition', anzahl, **filters)
        return parse_obj_as(List[Vorgangspositionbezug], documents)

    def get_aktivitaet_by_id(self, id: int) -> Optional[dict]:
        """
        Retrieve a single activity by its ID.

        Args:
            id (int): The ID of the activity.

        Returns:
            Optional[dict]: The activity dictionary or None if not found.
        """
        return self._fetch_single_item('aktivitaet', id)

    def get_drucksache_by_id(self, id: int) -> Optional[dict]:
        """
        Retrieve a single document (Drucksache) by its ID.

        Args:
            id (int): The ID of the document.

        Returns:
            Optional[dict]: The document dictionary or None if not found.
        """
        return self._fetch_single_item('drucksache', id)

    def get_drucksache_text_by_id(self, id: int) -> Optional[dict]:
        """
        Retrieve a single document (Drucksache) with text by its ID.

        Args:
            id (int): The ID of the document.

        Returns:
            Optional[dict]: The document dictionary or None if not found.
        """
        return self._fetch_single_item('drucksache-text', id)

    def get_plenarprotokoll_by_id(self, id: int) -> Optional[dict]:
        """
        Retrieve a single plenary protocol by its ID.

        Args:
            id (int): The ID of the protocol.

        Returns:
            Optional[dict]: The protocol dictionary or None if not found.
        """
        return self._fetch_single_item('plenarprotokoll', id)

    def get_plenarprotokoll_text_by_id(self, id: int) -> Optional[dict]:
        """
        Retrieve a single plenary protocol (with text) by its ID.

        Args:
            id (int): The ID of the protocol.

        Returns:
            Optional[dict]: The protocol dictionary or None if not found.
        """
        return self._fetch_single_item('plenarprotokoll-text', id)

    def get_vorgang_by_id(self, id: int) -> Optional[dict]:
        """
        Retrieve a single proceeding (Vorgang) by its ID.

        Args:
            id (int): The ID of the proceeding.

        Returns:
            Optional[dict]: The proceeding dictionary or None if not found.
        """
        return self._fetch_single_item('vorgang', id)

    def get_vorgangsposition_by_id(self, id: int) -> Optional[dict]:
        """
        Retrieve a single proceeding position (Vorgangsposition) by its ID.

        Args:
            id (int): The ID of the proceeding position.

        Returns:
            Optional[dict]: The proceeding position dictionary or None if not found.
        """
        return self._fetch_single_item('vorgangsposition', id)

    def clear_cache(self) -> None:
        """
        Clear the response cache.
        """
        if self.cache:
            self.cache.clear()

    def clear_expired_cache(self) -> None:
        """
        Clear expired cache entries.
        """
        if self.cache:
            self.cache.clear_expired()
