"""
Integration tests with mocked API server.

These tests use a mock server to test the complete workflow without
requiring a real API connection.
"""

import json
import unittest
from unittest.mock import MagicMock, patch

import pytest
import requests

from pydipapi import DipAnfrage
from pydipapi.async_api import AsyncDipAnfrage
from pydipapi.util.error_handler import DipApiHttpError, DipApiConnectionError


class TestIntegrationMockSync(unittest.TestCase):
    """Integration tests with mocked API server (synchronous)."""

    def setUp(self):
        """Set up test environment."""
        self.api_key = "test_api_key_12345"
        self.dip = DipAnfrage(api_key=self.api_key, enable_cache=False)

    @patch("pydipapi.client.base_client.requests.Session.get")
    def test_full_workflow_person(self, mock_get):
        """Test complete workflow for person retrieval."""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "cursor": "",
            "documents": [
                {
                    "id": "12345",
                    "vorname": "Max",
                    "nachname": "Mustermann",
                    "fraktion": "CDU/CSU",
                    "wahlkreis": "Berlin-Mitte",
                },
                {
                    "id": "67890",
                    "vorname": "Anna",
                    "nachname": "Schmidt",
                    "fraktion": "SPD",
                    "wahlkreis": "Hamburg-Nord",
                },
            ],
        }
        mock_response.raise_for_status = MagicMock()
        mock_response.headers = {}
        mock_response.content = json.dumps(mock_response.json.return_value).encode()
        mock_get.return_value = mock_response

        # Test workflow
        persons = self.dip.get_person(anzahl=2)

        # Assertions
        self.assertIsInstance(persons, list)
        self.assertEqual(len(persons), 2)
        self.assertEqual(persons[0]["id"], "12345")
        self.assertEqual(persons[0]["vorname"], "Max")
        self.assertEqual(persons[1]["fraktion"], "SPD")

        # Verify API was called correctly
        mock_get.assert_called()
        call_args = mock_get.call_args
        self.assertIn("apikey=test_api_key_12345", call_args[0][0])

    @patch("pydipapi.client.base_client.requests.Session.get")
    def test_full_workflow_documents(self, mock_get):
        """Test complete workflow for document retrieval."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "cursor": "",
            "documents": [
                {
                    "id": "11111",
                    "titel": "Test Document 1",
                    "dokumenttyp": "Antrag",
                    "datum": "2024-01-15",
                },
                {
                    "id": "22222",
                    "titel": "Test Document 2",
                    "dokumenttyp": "Kleine Anfrage",
                    "datum": "2024-01-20",
                },
            ],
        }
        mock_response.raise_for_status = MagicMock()
        mock_response.headers = {}
        mock_response.content = json.dumps(mock_response.json.return_value).encode()
        mock_get.return_value = mock_response

        documents = self.dip.get_drucksache(anzahl=2, text=False)

        self.assertIsInstance(documents, list)
        self.assertEqual(len(documents), 2)
        self.assertEqual(documents[0]["titel"], "Test Document 1")
        self.assertEqual(documents[1]["dokumenttyp"], "Kleine Anfrage")

    @patch("pydipapi.client.base_client.requests.Session.get")
    def test_batch_operations(self, mock_get):
        """Test batch operations workflow."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "documents": [
                {"id": "1", "name": "Person 1"},
                {"id": "2", "name": "Person 2"},
                {"id": "3", "name": "Person 3"},
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_response.headers = {}
        mock_response.content = json.dumps(mock_response.json.return_value).encode()
        mock_get.return_value = mock_response

        persons = self.dip.get_person_ids([1, 2, 3])

        self.assertEqual(len(persons), 3)
        self.assertEqual(persons[0]["id"], "1")
        self.assertEqual(persons[2]["name"], "Person 3")

    @patch("pydipapi.client.base_client.requests.Session.get")
    def test_error_handling_401(self, mock_get):
        """Test error handling for 401 Unauthorized."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.reason = "Unauthorized"
        mock_response.json.return_value = {"message": "Invalid API key"}
        mock_response.raise_for_status = MagicMock()
        mock_response.headers = {}
        mock_response.text = json.dumps({"message": "Invalid API key"})
        mock_get.return_value = mock_response

        # Should raise custom exception
        with self.assertRaises(DipApiHttpError) as context:
            self.dip.get_person(anzahl=1)

        self.assertEqual(context.exception.status_code, 401)
        self.assertIn("Invalid API key", str(context.exception))

    @patch("pydipapi.client.base_client.requests.Session.get")
    def test_error_handling_429(self, mock_get):
        """Test error handling for 429 Rate Limited."""
        # First call: rate limited
        mock_response_rate_limited = MagicMock()
        mock_response_rate_limited.status_code = 429
        mock_response_rate_limited.reason = "Too Many Requests"
        mock_response_rate_limited.headers = {"Retry-After": "60"}
        mock_response_rate_limited.raise_for_status = MagicMock()
        mock_response_rate_limited.text = "Rate limit exceeded"

        # Second call: success after retry
        mock_response_success = MagicMock()
        mock_response_success.status_code = 200
        mock_response_success.json.return_value = {
            "cursor": "",
            "documents": [{"id": "1", "name": "Test"}],
        }
        mock_response_success.raise_for_status = MagicMock()
        mock_response_success.headers = {}
        mock_response_success.content = json.dumps(
            mock_response_success.json.return_value
        ).encode()

        mock_get.side_effect = [mock_response_rate_limited, mock_response_success]

        # Should retry and eventually succeed
        persons = self.dip.get_person(anzahl=1, max_retries=2)

        self.assertEqual(len(persons), 1)
        self.assertEqual(mock_get.call_count, 2)  # Should have retried

    @patch("pydipapi.client.base_client.requests.Session.get")
    def test_pagination_workflow(self, mock_get):
        """Test pagination workflow with multiple pages."""
        # First page
        mock_response_page1 = MagicMock()
        mock_response_page1.status_code = 200
        mock_response_page1.json.return_value = {
            "cursor": "cursor_page2",
            "documents": [
                {"id": "1", "name": "Person 1"},
                {"id": "2", "name": "Person 2"},
            ],
        }
        mock_response_page1.raise_for_status = MagicMock()
        mock_response_page1.headers = {}
        mock_response_page1.content = json.dumps(
            mock_response_page1.json.return_value
        ).encode()

        # Second page
        mock_response_page2 = MagicMock()
        mock_response_page2.status_code = 200
        mock_response_page2.json.return_value = {
            "cursor": "",
            "documents": [
                {"id": "3", "name": "Person 3"},
            ],
        }
        mock_response_page2.raise_for_status = MagicMock()
        mock_response_page2.headers = {}
        mock_response_page2.content = json.dumps(
            mock_response_page2.json.return_value
        ).encode()

        mock_get.side_effect = [mock_response_page1, mock_response_page2]

        persons = self.dip.get_person(anzahl=3)

        self.assertEqual(len(persons), 3)
        self.assertEqual(mock_get.call_count, 2)  # Should have paginated


@pytest.mark.asyncio
class TestIntegrationMockAsync(unittest.TestCase):
    """Integration tests with mocked API server (asynchronous)."""

    def setUp(self):
        """Set up test environment."""
        self.api_key = "test_api_key_12345"

    @pytest.mark.asyncio
    async def test_full_workflow_async(self):
        """Test complete async workflow."""
        from unittest.mock import AsyncMock, patch

        # Mock aiohttp session
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.headers = {}
        mock_response.json = AsyncMock(
            return_value={
                "cursor": "",
                "documents": [
                    {"id": "1", "vorname": "Max", "nachname": "Mustermann"},
                ],
            }
        )
        mock_response.text = AsyncMock(
            return_value=json.dumps(
                {"cursor": "", "documents": [{"id": "1", "vorname": "Max", "nachname": "Mustermann"}]}
            )
        )

        mock_session = AsyncMock()
        mock_session.get = AsyncMock()
        mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.get.return_value.__aexit__ = AsyncMock(return_value=None)
        mock_session.closed = False

        with patch(
            "pydipapi.client.async_client.AsyncBaseApiClient._get_session",
            return_value=mock_session,
        ):
            async with AsyncDipAnfrage(api_key=self.api_key, enable_cache=False) as api:
                persons = await api.get_person(anzahl=1)

                self.assertIsInstance(persons, list)
                self.assertEqual(len(persons), 1)
                self.assertEqual(persons[0]["id"], "1")

    @pytest.mark.asyncio
    async def test_error_handling_async(self):
        """Test error handling in async client."""
        from unittest.mock import AsyncMock, patch

        mock_response = AsyncMock()
        mock_response.status = 401
        mock_response.reason = "Unauthorized"
        mock_response.headers = {}
        mock_response.text = AsyncMock(return_value='{"message": "Invalid API key"}')
        mock_response.json = AsyncMock(return_value={"message": "Invalid API key"})
        mock_response.request_info = MagicMock()
        mock_response.history = ()

        mock_session = AsyncMock()
        mock_session.get = AsyncMock()
        mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.get.return_value.__aexit__ = AsyncMock(return_value=None)
        mock_session.closed = False

        with patch(
            "pydipapi.client.async_client.AsyncBaseApiClient._get_session",
            return_value=mock_session,
        ):
            async with AsyncDipAnfrage(api_key=self.api_key, enable_cache=False) as api:
                with self.assertRaises(DipApiHttpError) as context:
                    await api.get_person(anzahl=1)

                self.assertEqual(context.exception.status_code, 401)


class TestIntegrationMockErrorHandling(unittest.TestCase):
    """Test error handling workflows with mocked errors."""

    def setUp(self):
        """Set up test environment."""
        self.api_key = "test_api_key_12345"
        self.dip = DipAnfrage(api_key=self.api_key, enable_cache=False)

    @patch("pydipapi.client.base_client.requests.Session.get")
    def test_connection_error(self, mock_get):
        """Test handling of connection errors."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

        # Should return empty list on connection error
        result = self.dip.get_person(anzahl=1)
        self.assertEqual(result, [])

    @patch("pydipapi.client.base_client.requests.Session.get")
    def test_timeout_error(self, mock_get):
        """Test handling of timeout errors."""
        mock_get.side_effect = requests.exceptions.Timeout("Request timeout")

        # Should return empty list on timeout
        result = self.dip.get_person(anzahl=1)
        self.assertEqual(result, [])

    @patch("pydipapi.client.base_client.requests.Session.get")
    def test_server_error_500(self, mock_get):
        """Test handling of server errors (500)."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.reason = "Internal Server Error"
        mock_response.json.return_value = {"message": "Server error"}
        mock_response.raise_for_status = MagicMock()
        mock_response.headers = {}
        mock_response.text = json.dumps({"message": "Server error"})
        mock_get.return_value = mock_response

        # Should raise custom exception
        with self.assertRaises(DipApiHttpError) as context:
            self.dip.get_person(anzahl=1)

        self.assertEqual(context.exception.status_code, 500)


if __name__ == "__main__":
    unittest.main()
