import requests
from typing import List, Union
from pydantic import parse_obj_as
from .type import Vorgangsbezug, Vorgangspositionbezug, VorgangVerlinkung, Bundesland, Datum, Quadrant, Zuordnung

class DipAnfrage:
    def __init__(self, apikey: str = "I9FKdCn.hbfefNWCY336dL6x62vfwNKpoN2RZ1gp21"):
        # Initialize the API key, base URL, and other instance variables
        self.apikey = "&apikey=" + apikey
        self.url = "https://search.dip.bundestag.de/api/v1/"
        self.cursor = ""
        self.documents = []
        self.adresse = self.url
        self.composeurl = self.url
        self.datum_start = ""
        self.datum_end = "" # Format 2020-02-28 YYYY-MM-DD

    def __set_cursor(self):
        # Set the request URL based on the cursor value
        if self.cursor == "":
            self.adresse = self.composeurl
        else:
            self.adresse = self.composeurl + "cursor=" + self.cursor

    def __anfrage(self) -> dict:
        # Make a GET request to the API and handle potential errors
        try:
            r = requests.get(url=self.adresse + self.apikey)
            r.raise_for_status()
        except requests.exceptions.HTTPError as h:
            return h
        except requests.exceptions.ConnectionError as c:
            return c
        self.data = r.json()
        # Update cursor and documents if present in the response
        if "cursor" in self.data:
            self.cursor = self.data['cursor']
        if 'documents' in self.data:
            self.documents = self.documents + self.data['documents']

    def get_person(self, anzahl: int = 100) -> List[dict]:
        # Retrieve a list of persons from the API
        self.documents = []
        self.composeurl = self.url + 'person?'
        while len(self.documents) < anzahl:
            self.__set_cursor()
            self.__anfrage()
        return self.documents[:anzahl]

    def get_person_ids(self, ids: List[int]) -> List[dict]:
        # Retrieve persons by their IDs
        self.documents = []
        self.adresse = self.url + "person?"
        for i in ids:
            self.adresse = self.adresse + '&f.id=' + str(i)
        self.__anfrage()
        return self.documents

    def get_person_id(self, id: int) -> dict:
        # Retrieve a single person by their ID
        self.documents = []
        self.adresse = self.url + "person/" + str(id) + "/?"
        self.__anfrage()
        return self.data

    def get_aktivitaet(self, anzahl: int = 100) -> List[dict]:
        # Retrieve a list of activities from the API
        self.documents = []
        self.composeurl = self.url + 'aktivitaet?'
        while len(self.documents) < anzahl:
            self.__set_cursor()
            self.__anfrage()
        return self.documents[:anzahl]

    def get_drucksache(self, anzahl: int = 10, text: bool = True) -> List[dict]:
        # Retrieve a list of documents (Drucksache) from the API
        self.documents = []
        if text:
            self.composeurl = self.url + 'drucksache-text?'
        else:
            self.composeurl = self.url + 'drucksache?'
        while len(self.documents) < anzahl:
            self.__set_cursor()
            self.__anfrage()
        return self.documents[:anzahl]

    def get_plenarprotokoll(self, anzahl: int = 10, text: bool = True) -> List[dict]:
        # Retrieve a list of plenary protocols from the API
        self.documents = []
        if text:
            self.composeurl = self.url + 'plenarprotokoll-text?'
        else:
            self.composeurl = self.url + 'plenarprotokoll?'
        while len(self.documents) < anzahl:
            self.__set_cursor()
            self.__anfrage()
        return self.documents[:anzahl]

    def get_vorgang(self, anzahl: int = 10) -> List[Vorgangsbezug]:
        # Retrieve a list of proceedings (Vorgang) from the API
        self.documents = []
        self.composeurl = self.url + 'vorgang?'
        while len(self.documents) < anzahl:
            self.__set_cursor()
            self.__anfrage()
        return parse_obj_as(List[Vorgangsbezug], self.documents[:anzahl])

    def get_vorgangsposition(self, anzahl: int = 10) -> List[Vorgangspositionbezug]:
        # Retrieve a list of proceeding positions (Vorgangsposition) from the API
        self.documents = []
        self.composeurl = self.url + 'vorgangsposition?'
        while len(self.documents) < anzahl:
            self.__set_cursor()
            self.__anfrage()
        return parse_obj_as(List[Vorgangspositionbezug], self.documents[:anzahl])

