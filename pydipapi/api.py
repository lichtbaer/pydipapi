import logging
import os
from typing import List, Union, Optional
import requests
from pydantic import parse_obj_as
from .type import Vorgangsbezug, Vorgangspositionbezug

# Configure logging for the library
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DipAnfrage:
    def __init__(self, apikey: Optional[str] = None):
        """
        Initialize the API key, base URL, and other instance variables.

        Args:
            apikey (Optional[str]): The API key for accessing the Bundestag API. If not provided, will attempt to use the 'DIP_API_KEY' environment variable.
        """
        self.apikey = apikey or os.getenv('DIP_API_KEY')
        if not self.apikey:
            logger.error(
                "API key must be provided either as an argument or through the 'DIP_API_KEY' environment variable.")
            raise ValueError("API key is required.")

        self.apikey = f"&apikey={self.apikey}"
        self.url = "https://search.dip.bundestag.de/api/v1/"
        self.cursor = ""
        self.documents = []
        self.adresse = self.url
        self.composeurl = self.url

    def __set_cursor(self):
        """
        Set the request URL based on the cursor value.
        """
        self.adresse = f"{self.composeurl}cursor={self.cursor}" if self.cursor else self.composeurl

    def __anfrage(self) -> Optional[dict]:
        """
        Make a GET request to the API and handle potential errors.

        Returns:
            Optional[dict]: The JSON response from the API if successful, otherwise None.
        """
        try:
            response = requests.get(url=self.adresse + self.apikey)
            response.raise_for_status()
            data = response.json()
            self.cursor = data.get('cursor', self.cursor)
            self.documents.extend(data.get('documents', []))
            return data
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            logger.error(f"Connection error occurred: {conn_err}")
        except requests.exceptions.RequestException as req_err:
            logger.error(f"Request exception occurred: {req_err}")
        return None

    def get_person(self, anzahl: int = 100) -> List[dict]:
        """
        Retrieve a list of persons from the API.

        Args:
            anzahl (int): Number of persons to retrieve.

        Returns:
            List[dict]: A list of person dictionaries.
        """
        self.documents = []
        self.composeurl = self.url + 'person?'
        while len(self.documents) < anzahl:
            self.__set_cursor()
            if not self.__anfrage():
                break
        return self.documents[:anzahl]

    def get_person_ids(self, ids: List[int]) -> List[dict]:
        """
        Retrieve persons by their IDs.

        Args:
            ids (List[int]): A list of person IDs.

        Returns:
            List[dict]: A list of person dictionaries.
        """
        self.documents = []
        self.adresse = self.url + "person?" + ''.join(f'&f.id={i}' for i in ids)
        self.__anfrage()
        return self.documents

    def get_person_id(self, id: int) -> Union[dict, None]:
        """
        Retrieve a single person by their ID.

        Args:
            id (int): The ID of the person.

        Returns:
            Union[dict, None]: The person dictionary or None if not found.
        """
        self.documents = []
        self.adresse = f"{self.url}person/{id}/?"
        return self.__anfrage()

    def get_aktivitaet(self, anzahl: int = 100) -> List[dict]:
        """
        Retrieve a list of activities from the API.

        Args:
            anzahl (int): Number of activities to retrieve.

        Returns:
            List[dict]: A list of activity dictionaries.
        """
        self.documents = []
        self.composeurl = self.url + 'aktivitaet?'
        while len(self.documents) < anzahl:
            self.__set_cursor()
            if not self.__anfrage():
                break
        return self.documents[:anzahl]

    def get_drucksache(self, anzahl: int = 10, text: bool = True) -> List[dict]:
        """
        Retrieve a list of documents (Drucksache) from the API.

        Args:
            anzahl (int): Number of documents to retrieve.
            text (bool): Whether to retrieve text documents.

        Returns:
            List[dict]: A list of document dictionaries.
        """
        self.documents = []
        self.composeurl = self.url + ('drucksache-text?' if text else 'drucksache?')
        while len(self.documents) < anzahl:
            self.__set_cursor()
            if not self.__anfrage():
                break
        return self.documents[:anzahl]

    def get_plenarprotokoll(self, anzahl: int = 10, text: bool = True) -> List[dict]:
        """
        Retrieve a list of plenary protocols from the API.

        Args:
            anzahl (int): Number of protocols to retrieve.
            text (bool): Whether to retrieve text protocols.

        Returns:
            List[dict]: A list of protocol dictionaries.
        """
        self.documents = []
        self.composeurl = self.url + ('plenarprotokoll-text?' if text else 'plenarprotokoll?')
        while len(self.documents) < anzahl:
            self.__set_cursor()
            if not self.__anfrage():
                break
        return self.documents[:anzahl]

    def get_vorgang(self, anzahl: int = 10) -> List[Vorgangsbezug]:
        """
        Retrieve a list of proceedings (Vorgang) from the API.

        Args:
            anzahl (int): Number of proceedings to retrieve.

        Returns:
            List[Vorgangsbezug]: A list of proceedings.
        """
        self.documents = []
        self.composeurl = self.url + 'vorgang?'
        while len(self.documents) < anzahl:
            self.__set_cursor()
            if not self.__anfrage():
                break
        return parse_obj_as(List[Vorgangsbezug], self.documents[:anzahl])

    def get_vorgangsposition(self, anzahl: int = 10) -> List[Vorgangspositionbezug]:
        """
        Retrieve a list of proceeding positions (Vorgangsposition) from the API.

        Args:
            anzahl (int): Number of proceeding positions to retrieve.

        Returns:
            List[Vorgangspositionbezug]: A list of proceeding positions.
        """
        self.documents = []
        self.composeurl = self.url + 'vorgangsposition?'
        while len(self.documents) < anzahl:
            self.__set_cursor()
            if not self.__anfrage():
                break
        return parse_obj_as(List[Vorgangspositionbezug], self.documents[:anzahl])