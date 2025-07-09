"""
Basic usage example for pydipapi.
"""
from pydipapi import DipAnfrage

dip = DipAnfrage(api_key='your_api_key_here')
persons = dip.get_person(anzahl=5)
print(persons)
