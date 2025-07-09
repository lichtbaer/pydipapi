"""
Tests for the async API client.
"""

import asyncio
import unittest
from unittest.mock import AsyncMock, patch

from pydipapi import AsyncDipAnfrage


class TestAsyncDipAnfrage(unittest.TestCase):
    """Tests for the async DIP API client."""

    def setUp(self):
        """Set up test environment."""
        self.async_client = AsyncDipAnfrage(api_key='test_key')

    def tearDown(self):
        """Clean up after tests."""
        # Close the session if it exists
        if hasattr(self.async_client, '_session') and self.async_client._session:
            asyncio.run(self.async_client.close())

    def test_async_client_initialization(self):
        """Test async client initialization."""
        client = AsyncDipAnfrage(api_key='test', enable_cache=False)
        self.assertEqual(client.api_key, 'test')
        self.assertFalse(client.enable_cache)
        self.assertIsNone(client.cache)

    @patch('aiohttp.ClientSession')
    async def test_async_make_request(self):
        """Test async make request."""
        # Mock the session
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={'documents': [{'id': 1}]})
        mock_response.status = 200
        mock_session.get.return_value.__aenter__.return_value = mock_response

        with patch.object(self.async_client, '_get_session', return_value=mock_session):
            result = await self.async_client._make_request('https://test.com')
            self.assertEqual(result, {'documents': [{'id': 1}]})

    @patch('aiohttp.ClientSession')
    async def test_async_fetch_paginated_data(self):
        """Test async fetch paginated data."""
        # Mock the session
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={
            'documents': [{'id': 1}, {'id': 2}],
            'cursor': ''
        })
        mock_response.status = 200
        mock_session.get.return_value.__aenter__.return_value = mock_response

        with patch.object(self.async_client, '_get_session', return_value=mock_session):
            result = await self.async_client._fetch_paginated_data('person', 5)
            self.assertEqual(len(result), 2)

    async def test_async_get_person(self):
        """Test async get person."""
        with patch.object(self.async_client, '_fetch_paginated_data', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = [{'id': 1, 'name': 'Test Person'}]

            result = await self.async_client.get_person(anzahl=5)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['name'], 'Test Person')

    async def test_async_get_person_ids(self):
        """Test async get person IDs."""
        with patch.object(self.async_client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {'documents': [{'id': 1}, {'id': 2}]}

            result = await self.async_client.get_person_ids([1, 2])
            self.assertEqual(len(result), 2)

    async def test_async_search_documents(self):
        """Test async search documents."""
        with patch.object(self.async_client, '_fetch_paginated_data', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = [{'id': 1, 'title': 'Test Document'}]

            result = await self.async_client.search_documents("test", anzahl=5)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['title'], 'Test Document')

    async def test_async_get_recent_activities(self):
        """Test async get recent activities."""
        with patch.object(self.async_client, '_fetch_paginated_data', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = [{'id': 1, 'type': 'activity'}]

            result = await self.async_client.get_recent_activities(days=7, anzahl=5)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['type'], 'activity')

    async def test_async_get_person_by_name(self):
        """Test async get person by name."""
        with patch.object(self.async_client, '_fetch_paginated_data', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = [{'id': 1, 'name': 'Test Person'}]

            result = await self.async_client.get_person_by_name("Test", anzahl=5)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['name'], 'Test Person')

    async def test_async_get_documents_by_type(self):
        """Test async get documents by type."""
        with patch.object(self.async_client, '_fetch_paginated_data', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = [{'id': 1, 'type': 'kleine_anfrage'}]

            result = await self.async_client.get_documents_by_type("kleine_anfrage", anzahl=5)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['type'], 'kleine_anfrage')

    async def test_async_get_proceedings_by_type(self):
        """Test async get proceedings by type."""
        with patch.object(self.async_client, '_fetch_paginated_data', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = [{'id': 1, 'type': 'proceeding'}]

            result = await self.async_client.get_proceedings_by_type("test_type", anzahl=5)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['type'], 'proceeding')

    async def test_async_get_aktivitaet(self):
        """Test async get aktivitaet."""
        with patch.object(self.async_client, '_fetch_paginated_data', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = [{'id': 1, 'type': 'aktivitaet'}]

            result = await self.async_client.get_aktivitaet(anzahl=5)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['type'], 'aktivitaet')

    async def test_async_get_drucksache(self):
        """Test async get drucksache."""
        with patch.object(self.async_client, '_fetch_paginated_data', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = [{'id': 1, 'type': 'drucksache'}]

            result = await self.async_client.get_drucksache(anzahl=5)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['type'], 'drucksache')

    async def test_async_get_plenarprotokoll(self):
        """Test async get plenarprotokoll."""
        with patch.object(self.async_client, '_fetch_paginated_data', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = [{'id': 1, 'type': 'plenarprotokoll'}]

            result = await self.async_client.get_plenarprotokoll(anzahl=5)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['type'], 'plenarprotokoll')

    async def test_async_get_vorgang(self):
        """Test async get vorgang."""
        with patch.object(self.async_client, '_fetch_paginated_data', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = [{'id': 1, 'type': 'vorgang'}]

            result = await self.async_client.get_vorgang(anzahl=5)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['type'], 'vorgang')

    async def test_async_get_vorgangsposition(self):
        """Test async get vorgangsposition."""
        with patch.object(self.async_client, '_fetch_paginated_data', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = [{'id': 1, 'type': 'vorgangsposition'}]

            result = await self.async_client.get_vorgangsposition(anzahl=5)
            self.assertEqual(len(result), 1)
            # The result is a list of Vorgangspositionbezug objects, not dicts
            self.assertEqual(result[0].id, 1)

    async def test_async_context_manager(self):
        """Test async context manager."""
        async with AsyncDipAnfrage(api_key='test') as client:
            self.assertIsInstance(client, AsyncDipAnfrage)

    def test_build_url(self):
        """Test URL building in async client."""
        url = self.async_client._build_url('person', wahlperiode=20)
        self.assertIn('wahlperiode=20', url)

    def test_build_url_with_list_params(self):
        """Test URL building with list parameters."""
        url = self.async_client._build_url('person', f_id=[1, 2, 3])
        self.assertIn('f_id=1', url)
        self.assertIn('f_id=2', url)
        self.assertIn('f_id=3', url)


def run_async_test(test_method):
    """Helper to run async tests."""
    return asyncio.run(test_method())


if __name__ == '__main__':
    # Create a test suite that can handle async tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestAsyncDipAnfrage)

    # Run the tests
    runner = unittest.TextTestRunner()
    runner.run(suite)
