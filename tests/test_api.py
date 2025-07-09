import unittest
from unittest.mock import MagicMock, patch

import requests

from pydipapi import DipAnfrage


class TestDipAnfrage(unittest.TestCase):
    def setUp(self, api_key: str = 'testkey'):
        self.api_key = api_key
        self.dip = DipAnfrage(api_key=self.api_key)

    @patch('pydipapi.client.base_client.requests.Session.get')
    def test_get_person(self, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'cursor': '',
            'documents': [{'id': '1', 'name': 'John Doe'}]
        }
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Call the method
        persons = self.dip.get_person(anzahl=1)

        # Assertions
        self.assertEqual(len(persons), 1)
        self.assertEqual(persons[0]['id'], '1')
        self.assertEqual(persons[0]['name'], 'John Doe')

    @patch('pydipapi.client.base_client.requests.Session.get')
    def test_get_person_id(self, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'documents': [{'id': '1', 'name': 'John Doe'}]
        }
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Call the method
        person = self.dip.get_person_id(id=1)

        # Assertions
        if person is not None:
            self.assertEqual(person['id'], '1')
            self.assertEqual(person['name'], 'John Doe')
        else:
            self.fail("Expected person to be returned")

    @patch('pydipapi.client.base_client.requests.Session.get')
    def test_api_error_handling(self, mock_get):
        # Mock an HTTP error
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("An error occurred")
        mock_get.return_value = mock_response

        # Call the method and assert that it handles the error
        result = self.dip.get_person(anzahl=1)
        self.assertEqual(result, [])  # Should return empty list on error

    def test_api_key_validation(self):
        """Test that API key validation works correctly."""
        # Test with valid API key
        dip = DipAnfrage(api_key='valid_key')
        self.assertEqual(dip.api_key, 'valid_key')

        # Test with empty API key (should not raise ValueError)
        dip = DipAnfrage(api_key='')
        self.assertEqual(dip.api_key, '')

    @patch('pydipapi.client.base_client.requests.Session.get')
    def test_batch_operations(self, mock_get):
        """Test batch operations for multiple IDs."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'documents': [
                {'id': '1', 'name': 'John Doe'},
                {'id': '2', 'name': 'Jane Smith'}
            ]
        }
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Test batch person retrieval
        persons = self.dip.get_person_ids([1, 2])
        self.assertEqual(len(persons), 2)
        self.assertEqual(persons[0]['id'], '1')
        self.assertEqual(persons[1]['id'], '2')

    @patch('pydipapi.client.base_client.requests.Session.get')
    def test_convenience_methods(self, mock_get):
        """Test convenience methods."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'documents': [{'id': '1', 'name': 'Test Person'}]
        }
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Test search documents
        results = self.dip.search_documents("test", anzahl=1)
        self.assertEqual(len(results), 1)

        # Test get person by name
        persons = self.dip.get_person_by_name("Test", anzahl=1)
        self.assertEqual(len(persons), 1)

        # Test get documents by type
        docs = self.dip.get_documents_by_type("Antrag", anzahl=1)
        self.assertEqual(len(docs), 1)

        # Test get proceedings by type
        procs = self.dip.get_proceedings_by_type("Gesetzgebung", anzahl=1)
        self.assertEqual(len(procs), 1)


if __name__ == '__main__':
    unittest.main()
