"""
Coverage tests for pydipapi.

These tests focus on edge cases and improving code coverage.
"""

import unittest
from unittest.mock import MagicMock, patch

import requests

from pydipapi import DipAnfrage


class TestCoverage(unittest.TestCase):
    """Tests for improving code coverage."""

    def setUp(self):
        """Set up test environment."""
        self.dip = DipAnfrage(api_key='test_key')

    def test_cache_serialization_error(self):
        """Test cache serialization error handling."""
        # Mock cache to raise serialization error
        with patch('pydipapi.util.cache.json.dump') as mock_dump:
            mock_dump.side_effect = Exception("Serialization error")

            # Create client with cache enabled
            dip = DipAnfrage(api_key='test', enable_cache=True)

            # Should not raise exception
            with patch('pydipapi.client.base_client.requests.Session.get') as mock_get:
                mock_response = MagicMock()
                mock_response.json.return_value = {'documents': []}
                mock_response.status_code = 200
                mock_get.return_value = mock_response

                result = dip.get_person(anzahl=1)
                self.assertEqual(result, [])

    def test_cache_invalid_json(self):
        """Test cache with invalid JSON."""
        # Mock cache to return invalid JSON
        with patch('pydipapi.util.cache.json.load') as mock_load:
            mock_load.side_effect = Exception("Invalid JSON")

            # Create client with cache enabled
            dip = DipAnfrage(api_key='test', enable_cache=True)

            # Should handle invalid cache gracefully
            with patch('pydipapi.client.base_client.requests.Session.get') as mock_get:
                mock_response = MagicMock()
                mock_response.json.return_value = {'documents': []}
                mock_response.status_code = 200
                mock_get.return_value = mock_response

                result = dip.get_person(anzahl=1)
                self.assertEqual(result, [])

    def test_connection_error_handling(self):
        """Test connection error handling."""
        with patch('pydipapi.client.base_client.requests.Session.get') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

            # Should return empty list on connection error
            result = self.dip.get_person(anzahl=1)
            self.assertEqual(result, [])

    def test_timeout_error_handling(self):
        """Test timeout error handling."""
        with patch('pydipapi.client.base_client.requests.Session.get') as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout("Request timeout")

            # Should return empty list on timeout error
            result = self.dip.get_person(anzahl=1)
            self.assertEqual(result, [])

    def test_ssl_error_handling(self):
        """Test SSL error handling."""
        with patch('pydipapi.client.base_client.requests.Session.get') as mock_get:
            mock_get.side_effect = requests.exceptions.SSLError("SSL error")

            # Should return empty list on SSL error
            result = self.dip.get_person(anzahl=1)
            self.assertEqual(result, [])

    def test_rate_limit_handling(self):
        """Test rate limit handling."""
        with patch('pydipapi.client.base_client.requests.Session.get') as mock_get:
            # Mock rate limit response
            mock_response = MagicMock()
            mock_response.status_code = 429
            mock_response.headers = {'Retry-After': '60'}
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Rate limited")
            mock_get.return_value = mock_response

            # Should return empty list on rate limit
            result = self.dip.get_person(anzahl=1)
            self.assertEqual(result, [])

    def test_unauthorized_error_handling(self):
        """Test unauthorized error handling."""
        with patch('pydipapi.client.base_client.requests.Session.get') as mock_get:
            # Mock unauthorized response
            mock_response = MagicMock()
            mock_response.status_code = 401
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Unauthorized")
            mock_get.return_value = mock_response

            # Should return empty list on unauthorized
            result = self.dip.get_person(anzahl=1)
            self.assertEqual(result, [])

    def test_forbidden_error_handling(self):
        """Test forbidden error handling."""
        with patch('pydipapi.client.base_client.requests.Session.get') as mock_get:
            # Mock forbidden response
            mock_response = MagicMock()
            mock_response.status_code = 403
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Forbidden")
            mock_get.return_value = mock_response

            # Should return empty list on forbidden
            result = self.dip.get_person(anzahl=1)
            self.assertEqual(result, [])

    def test_not_found_error_handling(self):
        """Test not found error handling."""
        with patch('pydipapi.client.base_client.requests.Session.get') as mock_get:
            # Mock not found response
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Not found")
            mock_get.return_value = mock_response

            # Should return empty list on not found
            result = self.dip.get_person(anzahl=1)
            self.assertEqual(result, [])

    def test_server_error_handling(self):
        """Test server error handling."""
        with patch('pydipapi.client.base_client.requests.Session.get') as mock_get:
            # Mock server error response
            mock_response = MagicMock()
            mock_response.status_code = 500
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Server error")
            mock_get.return_value = mock_response

            # Should return empty list on server error
            result = self.dip.get_person(anzahl=1)
            self.assertEqual(result, [])

    def test_retry_logic_with_failures(self):
        """Test retry logic with multiple failures."""
        with patch('pydipapi.client.base_client.requests.Session.get') as mock_get:
            # Mock multiple failures then success
            mock_response_fail = MagicMock()
            mock_response_fail.status_code = 500
            mock_response_fail.raise_for_status.side_effect = requests.exceptions.HTTPError("Server error")

            mock_response_success = MagicMock()
            mock_response_success.json.return_value = {'documents': [{'id': '1', 'name': 'Test'}]}
            mock_response_success.status_code = 200

            mock_get.side_effect = [mock_response_fail, mock_response_fail, mock_response_success]

            # Create client with retries
            dip = DipAnfrage(api_key='test', max_retries=3)

            # Should succeed after retries
            result = dip.get_person(anzahl=1)
            self.assertEqual(len(result), 1)

    def test_retry_logic_with_all_failures(self):
        """Test retry logic when all attempts fail."""
        with patch('pydipapi.client.base_client.requests.Session.get') as mock_get:
            # Mock all failures
            mock_response = MagicMock()
            mock_response.status_code = 500
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Server error")
            mock_get.return_value = mock_response

            # Create client with retries
            dip = DipAnfrage(api_key='test', max_retries=2)

            # Should return empty list after all retries fail
            result = dip.get_person(anzahl=1)
            self.assertEqual(result, [])

    def test_cache_key_generation(self):
        """Test cache key generation with various parameters."""
        dip = DipAnfrage(api_key='test', enable_cache=True)

        # Test with different parameters
        url1 = dip._build_url('person', anzahl=10)
        url2 = dip._build_url('person', anzahl=20)

        # URLs should be different
        self.assertNotEqual(url1, url2)

    def test_url_building_edge_cases(self):
        """Test URL building with edge cases."""
        dip = DipAnfrage(api_key='test')

        # Test with None values
        url = dip._build_url('person', anzahl=None, wahlperiode=20)
        self.assertIn('wahlperiode=20', url)
        self.assertNotIn('anzahl=None', url)

        # Test with empty string (should be included as empty parameter)
        url = dip._build_url('person', anzahl='', wahlperiode=20)
        self.assertIn('wahlperiode=20', url)
        self.assertIn('anzahl=', url)  # Empty string should be included

        # Test with zero values
        url = dip._build_url('person', anzahl=0, wahlperiode=20)
        self.assertIn('anzahl=0', url)

    def test_pagination_edge_cases(self):
        """Test pagination with edge cases."""
        with patch('pydipapi.client.base_client.requests.Session.get') as mock_get:
            # Mock response with no cursor
            mock_response = MagicMock()
            mock_response.json.return_value = {
                'documents': [{'id': '1', 'name': 'Test'}],
                'cursor': ''
            }
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            # Should handle empty cursor
            result = self.dip.get_person(anzahl=10)
            self.assertEqual(len(result), 1)

    def test_empty_documents_response(self):
        """Test handling of empty documents in response."""
        with patch('pydipapi.client.base_client.requests.Session.get') as mock_get:
            # Mock response with empty documents
            mock_response = MagicMock()
            mock_response.json.return_value = {
                'documents': [],
                'cursor': ''
            }
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            # Should return empty list
            result = self.dip.get_person(anzahl=10)
            self.assertEqual(result, [])

    def test_missing_documents_key(self):
        """Test handling of response without documents key."""
        with patch('pydipapi.client.base_client.requests.Session.get') as mock_get:
            # Mock response without documents key
            mock_response = MagicMock()
            mock_response.json.return_value = {
                'other_key': 'value',
                'cursor': ''
            }
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            # Should return empty list
            result = self.dip.get_person(anzahl=10)
            self.assertEqual(result, [])

    def test_non_dict_response(self):
        """Test handling of non-dict response."""
        with patch('pydipapi.client.base_client.requests.Session.get') as mock_get:
            # Mock non-dict response
            mock_response = MagicMock()
            mock_response.json.return_value = "not a dict"
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            # Should return empty list
            result = self.dip.get_person(anzahl=10)
            self.assertEqual(result, [])

    def test_cache_disabled(self):
        """Test behavior when cache is disabled."""
        dip = DipAnfrage(api_key='test', enable_cache=False)

        with patch('pydipapi.client.base_client.requests.Session.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {'documents': [{'id': '1', 'name': 'Test'}]}
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            # Should work without cache
            result = dip.get_person(anzahl=1)
            self.assertEqual(len(result), 1)

    def test_cache_clear_methods(self):
        """Test cache clearing methods."""
        dip = DipAnfrage(api_key='test', enable_cache=True)

        # Should not raise exceptions
        dip.clear_cache()
        dip.clear_expired_cache()

    def test_batch_operations_empty_list(self):
        """Test batch operations with empty list."""
        with patch('pydipapi.client.base_client.requests.Session.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {'documents': []}
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            result = self.dip.get_person_ids([])
            self.assertEqual(result, [])

    def test_batch_operations_single_item(self):
        """Test batch operations with single item."""
        with patch('pydipapi.client.base_client.requests.Session.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {'documents': [{'id': '1', 'name': 'Test'}]}
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            result = self.dip.get_person_ids([1])
            self.assertEqual(len(result), 1)

    def test_convenience_methods_edge_cases(self):
        """Test convenience methods with edge cases."""
        with patch('pydipapi.client.base_client.requests.Session.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {'documents': []}
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            # Test with empty search term
            result = self.dip.search_documents("", anzahl=1)
            self.assertEqual(result, [])

            # Test with empty string search term (None is not allowed by type hints)
            result = self.dip.search_documents("", anzahl=1)
            self.assertEqual(result, [])

    def test_error_logging(self):
        """Test that errors are properly logged."""
        with patch('pydipapi.client.base_client.logger') as mock_logger:
            with patch('pydipapi.client.base_client.requests.Session.get') as mock_get:
                mock_get.side_effect = Exception("Test error")

                # Should log error and return empty list
                result = self.dip.get_person(anzahl=1)
                self.assertEqual(result, [])

                # Should have logged error
                mock_logger.error.assert_called()

    def test_debug_logging(self):
        """Test that debug information is logged."""
        with patch('pydipapi.client.base_client.logger') as mock_logger:
            with patch('pydipapi.client.base_client.requests.Session.get') as mock_get:
                mock_response = MagicMock()
                mock_response.json.return_value = {'documents': []}
                mock_response.status_code = 200
                mock_get.return_value = mock_response

                # Should log debug information
                self.dip.get_person(anzahl=1)

                # Should have logged debug info
                mock_logger.debug.assert_called()


if __name__ == '__main__':
    unittest.main()
