import requests


class DipAnfrage:
    def __init__(self, apikey: str = "N64VhW8.yChkBUIJeosGojQ7CSR2xwLf3Qy7Apw464"):
        self.apikey = "&apikey=" + apikey
        self.url = "https://search.dip.bundestag.de/api/v1/"
        self.cursor = ""
        self.documents = []
        self.adresse = self.url
        self.composeurl = self.url
        self.datum_start = ""
        self.datum_end = "" # Format 2020-02-28 YYYY-MM-DD

    def __set_cursor(self):
        if self.cursor == "":
            self.adresse = self.composeurl
        else:
            self.adresse = self.composeurl + "cursor=" + self.cursor

    def __anfrage(self) -> dict:
        try:
            r = requests.get(url=self.adresse + self.apikey)
        except requests.exceptions.HTTPError as h:
            return h
        except requests.exceptions.ConnectionError as c:
            return c
        self.data = r.json()
        if "cursor" in self.data:
            self.cursor = self.data['cursor']
        if 'documents' in self.data:
            self.documents = self.documents +self.data['documents']
    '''
    def set_datum(self, start= "2020-02-01", end = "2020-02-28"):
        self.datum_start = start
        self.datum_end = end
        self.composeurl = self.composeurl + "&f.datum.start="+ start + "&f.datum.end=" + end
    '''

    def get_person(self, anzahl:int = 100) -> list:
        self.documents = []
        self.composeurl = self.url + 'person?'
        while len(self.documents) < anzahl:
            self.__set_cursor()
            self.__anfrage()
        return self.documents[:anzahl]

    def get_person_ids(self, ids:list) -> list:
        self.documents = []
        self.adresse = self.url + "person?"
        for i in ids:
            self.adresse = self.adresse + '&f.id=' + str(i)
        self.__anfrage()
        return self.documents

    def get_person_id(self, id:int)-> dict:
        self.documents = []
        self.adresse = self.url + "person/" + str(id) +"/?"
        self.__anfrage()
        return self.data

    def get_aktivitaet(self, anzahl:int = 100) -> list:
        self.documents = []
        self.composeurl = self.url + 'aktivitaet?'
        while len(self.documents) < anzahl:
            self.__set_cursor()
            self.__anfrage()
        return self.documents[:anzahl]

    def get_drucksache(self, anzahl:int = 10, text = True) -> list:
        self.documents = []
        if text:
            self.composeurl = self.url + 'drucksache-text?'
        else:
            self.composeurl = self.url + 'drucksache?'
        while len(self.documents) < anzahl:
            self.__set_cursor()
            self.__anfrage()
        return self.documents[:anzahl]

    def get_plenarprotokoll(self, anzahl:int = 10, text = True) -> list:
        self.documents = []
        if text:
            self.composeurl = self.url + 'plenarprotokoll-text?'
        else:
            self.composeurl = self.url + 'plenarprotokoll?'
        while len(self.documents) < anzahl:
            self.__set_cursor()
            self.__anfrage()
        return self.documents[:anzahl]

    def get_vorgang(self, anzahl:int = 10, text = True) -> list:
        self.documents = []
        self.composeurl = self.url + 'vorgang?'
        while len(self.documents) < anzahl:
            self.__set_cursor()
            self.__anfrage()
        return self.documents[:anzahl]

    def get_vorgangsposition(self, anzahl:int = 10, text = True) -> list:
        self.documents = []
        self.composeurl = self.url + 'vorgangsposition?'
        while len(self.documents) < anzahl:
            self.__set_cursor()
            self.__anfrage()
        return self.documents[:anzahl]
