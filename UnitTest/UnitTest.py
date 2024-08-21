import unittest
import requests
from unittest.mock import patch, MagicMock
from pydipapi import DipAnfrage


class TestDipAnfrage(unittest.TestCase):
    def setUp(self, api_key: str = None):
        self.api_key = api_key or 'testkey'
        self.dip = DipAnfrage(apikey=self.api_key)

    @patch('pydipapi.requests.get')
    def test_get_person(self, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'cursor': '',
            'documents': [{'id': '1', 'name': 'John Doe'}]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Call the method
        persons = self.dip.get_person(anzahl=1)

        # Assertions
        self.assertEqual(len(persons), 1)
        self.assertEqual(persons[0]['id'], '1')
        self.assertEqual(persons[0]['name'], 'John Doe')

    @patch('pydipapi.requests.get')
    def test_get_person_id(self, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {'id': '1', 'name': 'John Doe'}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Call the method
        person = self.dip.get_person_id(id=1)

        # Assertions
        self.assertEqual(person['id'], '1')
        self.assertEqual(person['name'], 'John Doe')

    @patch('pydipapi.requests.get')
    def test_api_error_handling(self, mock_get):
        # Mock an HTTP error
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("An error occurred")
        mock_get.return_value = mock_response

        # Call the method and assert that it handles the error
        result = self.dip.get_person(anzahl=1)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
