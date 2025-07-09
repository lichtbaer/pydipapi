"""
Main API client for the German Bundestag API.
"""
from typing import List, Optional

from pydantic import parse_obj_as

from .client.base_client import BaseApiClient
from .type import Vorgangsbezug, Vorgangspositionbezug


class DipAnfrage(BaseApiClient):
    """
    Main client for accessing the German Bundestag API.

    This class provides methods to retrieve information about persons, activities,
    documents, and legislative processes from the Bundestag API.
    """
    def get_person(self, anzahl: int = 100) -> Optional[List[dict]]:
        """
        Retrieve a list of persons from the API.

        Args:
            anzahl (int): Number of persons to retrieve.

        Returns:
            Optional[List[dict]]: A list of person dictionaries or None if an error occurred.
        """
        try:
            return self._fetch_paginated_data('person', anzahl)
        except Exception:
            return None

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

    def get_person_id(self, id: int) -> Optional[dict]:
        """
        Retrieve a single person by their ID.

        Args:
            id (int): The ID of the person.

        Returns:
            Optional[dict]: The person dictionary or None if not found.
        """
        return self._fetch_single_item('person', id)

    def get_aktivitaet(self, anzahl: int = 100) -> List[dict]:
        """
        Retrieve a list of activities from the API.

        Args:
            anzahl (int): Number of activities to retrieve.

        Returns:
            List[dict]: A list of activity dictionaries.
        """
        return self._fetch_paginated_data('aktivitaet', anzahl)

    def get_drucksache(self, anzahl: int = 10, text: bool = True) -> List[dict]:
        """
        Retrieve a list of documents (Drucksache) from the API.

        Args:
            anzahl (int): Number of documents to retrieve.
            text (bool): Whether to retrieve text documents.

        Returns:
            List[dict]: A list of document dictionaries.
        """
        endpoint = 'drucksache-text' if text else 'drucksache'
        return self._fetch_paginated_data(endpoint, anzahl)

    def get_plenarprotokoll(self, anzahl: int = 10, text: bool = True) -> List[dict]:
        """
        Retrieve a list of plenary protocols from the API.

        Args:
            anzahl (int): Number of protocols to retrieve.
            text (bool): Whether to retrieve text protocols.

        Returns:
            List[dict]: A list of protocol dictionaries.
        """
        endpoint = 'plenarprotokoll-text' if text else 'plenarprotokoll'
        return self._fetch_paginated_data(endpoint, anzahl)

    def get_vorgang(self, anzahl: int = 10) -> List[Vorgangsbezug]:
        """
        Retrieve a list of proceedings (Vorgang) from the API.

        Args:
            anzahl (int): Number of proceedings to retrieve.

        Returns:
            List[Vorgangsbezug]: A list of proceedings.
        """
        documents = self._fetch_paginated_data('vorgang', anzahl)
        return parse_obj_as(List[Vorgangsbezug], documents)

    def get_vorgangsposition(self, anzahl: int = 10) -> List[Vorgangspositionbezug]:
        """
        Retrieve a list of proceeding positions (Vorgangsposition) from the API.

        Args:
            anzahl (int): Number of proceeding positions to retrieve.

        Returns:
            List[Vorgangspositionbezug]: A list of proceeding positions.
        """
        documents = self._fetch_paginated_data('vorgangsposition', anzahl)
        return parse_obj_as(List[Vorgangspositionbezug], documents)
