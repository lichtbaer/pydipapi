"""
Integration tests for pydipapi.

These tests require a valid API key and test against the real Bundestag API.
"""

import os
import time
import unittest

import pytest

from pydipapi import DipAnfrage


class TestIntegration(unittest.TestCase):
    """Integration tests using the real Bundestag API."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        # Get API key from environment
        api_key = os.getenv('DIP_API_KEY')
        if not api_key:
            pytest.skip("DIP_API_KEY environment variable not set")

        cls.api_key = api_key
        cls.dip = DipAnfrage(api_key=api_key, enable_cache=False)

        # Test data for known entities
        cls.test_person_id = 11000001  # Known person ID
        cls.test_document_id = 11000001  # Known document ID
        cls.test_activity_id = 11000001  # Known activity ID

    def setUp(self):
        """Set up before each test."""
        # Add delay between tests to respect rate limits
        time.sleep(0.5)

    def test_get_person_integration(self):
        """Test getting persons from the real API."""
        persons = self.dip.get_person(anzahl=5)

        # Should return a list
        self.assertIsInstance(persons, list)

        # Should have some results (API might be empty, but structure should be correct)
        if persons:
            # Check structure of first person
            person = persons[0]
            self.assertIsInstance(person, dict)
            # Check for expected fields
            self.assertIn('id', person)
            self.assertIn('name', person)

    def test_get_person_by_id_integration(self):
        """Test getting a specific person by ID."""
        person = self.dip.get_person_id(id=self.test_person_id)

        # Should return a person or None (if ID doesn't exist)
        if person is not None:
            self.assertIsInstance(person, dict)
            self.assertEqual(str(person.get('id')), str(self.test_person_id))
            self.assertIn('name', person)

    def test_get_documents_integration(self):
        """Test getting documents from the real API."""
        documents = self.dip.get_drucksache(anzahl=5)

        # Should return a list
        self.assertIsInstance(documents, list)

        # Should have some results
        if documents:
            # Check structure of first document
            document = documents[0]
            self.assertIsInstance(document, dict)
            # Check for expected fields
            self.assertIn('id', document)
            self.assertIn('titel', document)

    def test_get_document_by_id_integration(self):
        """Test getting a specific document by ID."""
        document = self.dip.get_drucksache_by_id(id=self.test_document_id)

        # Should return a document or None (if ID doesn't exist)
        if document is not None:
            self.assertIsInstance(document, dict)
            self.assertEqual(str(document.get('id')), str(self.test_document_id))
            self.assertIn('titel', document)

    def test_get_activities_integration(self):
        """Test getting activities from the real API."""
        activities = self.dip.get_aktivitaet(anzahl=5)

        # Should return a list
        self.assertIsInstance(activities, list)

        # Should have some results
        if activities:
            # Check structure of first activity
            activity = activities[0]
            self.assertIsInstance(activity, dict)
            # Check for expected fields
            self.assertIn('id', activity)

    def test_get_activity_by_id_integration(self):
        """Test getting a specific activity by ID."""
        activity = self.dip.get_aktivitaet_by_id(id=self.test_activity_id)

        # Should return an activity or None (if ID doesn't exist)
        if activity is not None:
            self.assertIsInstance(activity, dict)
            self.assertEqual(str(activity.get('id')), str(self.test_activity_id))

    def test_search_documents_integration(self):
        """Test searching documents with real API."""
        # Search for a common term
        results = self.dip.search_documents("Bundeshaushalt", anzahl=3)

        # Should return a list
        self.assertIsInstance(results, list)

        # Should have some results
        if results:
            # Check structure of first result
            result = results[0]
            self.assertIsInstance(result, dict)
            self.assertIn('id', result)
            self.assertIn('titel', result)

    def test_get_person_by_name_integration(self):
        """Test getting persons by name with real API."""
        # Search for a common name
        persons = self.dip.get_person_by_name("Merkel", anzahl=3)

        # Should return a list
        self.assertIsInstance(persons, list)

        # Should have some results
        if persons:
            # Check structure of first person
            person = persons[0]
            self.assertIsInstance(person, dict)
            self.assertIn('id', person)
            self.assertIn('name', person)

    def test_get_documents_by_type_integration(self):
        """Test getting documents by type with real API."""
        # Get documents of type "Antrag"
        documents = self.dip.get_documents_by_type("Antrag", anzahl=3)

        # Should return a list
        self.assertIsInstance(documents, list)

        # Should have some results
        if documents:
            # Check structure of first document
            document = documents[0]
            self.assertIsInstance(document, dict)
            self.assertIn('id', document)
            self.assertIn('titel', document)

    def test_get_proceedings_by_type_integration(self):
        """Test getting proceedings by type with real API."""
        # Get proceedings of type "Gesetzgebung"
        proceedings = self.dip.get_proceedings_by_type("Gesetzgebung", anzahl=3)

        # Should return a list
        self.assertIsInstance(proceedings, list)

        # Should have some results
        if proceedings:
            # Check structure of first proceeding
            proceeding = proceedings[0]
            self.assertIsInstance(proceeding, dict)
            self.assertIn('id', proceeding)

    def test_batch_operations_integration(self):
        """Test batch operations with real API."""
        # Test with a few known IDs
        test_ids = [self.test_person_id, self.test_person_id + 1]

        persons = self.dip.get_person_ids(test_ids)

        # Should return a list
        self.assertIsInstance(persons, list)

        # Should have some results
        if persons:
            # Check structure of first person
            person = persons[0]
            self.assertIsInstance(person, dict)
            self.assertIn('id', person)

    def test_filtering_integration(self):
        """Test filtering with real API."""
        # Test with wahlperiode filter
        persons = self.dip.get_person(wahlperiode=20, anzahl=3)

        # Should return a list
        self.assertIsInstance(persons, list)

        # Should have some results
        if persons:
            # Check structure of first person
            person = persons[0]
            self.assertIsInstance(person, dict)
            self.assertIn('id', person)

    def test_rate_limiting_integration(self):
        """Test that rate limiting works with real API."""
        start_time = time.time()

        # Make multiple requests quickly
        for _ in range(3):
            self.dip.get_person(anzahl=1)

        end_time = time.time()

        # Should take at least 0.2 seconds (2 delays of 0.1s each)
        self.assertGreaterEqual(end_time - start_time, 0.2)

    def test_error_handling_integration(self):
        """Test error handling with real API."""
        # Test with invalid API key
        invalid_dip = DipAnfrage(api_key="invalid_key")

        # Should return empty list on authentication error
        persons = invalid_dip.get_person(anzahl=1)
        self.assertEqual(persons, [])

    def test_cache_functionality_integration(self):
        """Test caching with real API."""
        # Create client with cache enabled
        cached_dip = DipAnfrage(api_key=self.api_key, enable_cache=True, cache_ttl=3600)

        # First call
        persons1 = cached_dip.get_person(anzahl=1)
        self.assertIsInstance(persons1, list)

        # Second call should use cache
        persons2 = cached_dip.get_person(anzahl=1)
        self.assertIsInstance(persons2, list)

        # Results should be the same
        self.assertEqual(persons1, persons2)

        # Test cache clearing
        cached_dip.clear_cache()
        persons3 = cached_dip.get_person(anzahl=1)
        self.assertIsInstance(persons3, list)

    def test_pagination_integration(self):
        """Test pagination with real API."""
        # Get more results than default
        persons = self.dip.get_person(anzahl=20)

        # Should return a list
        self.assertIsInstance(persons, list)

        # Should have some results
        if persons:
            # Check that we got multiple results
            self.assertGreater(len(persons), 0)

            # Check structure of first person
            person = persons[0]
            self.assertIsInstance(person, dict)
            self.assertIn('id', person)

    def test_url_building_integration(self):
        """Test URL building with real API."""
        # Test URL building with various parameters
        url = self.dip._build_url('person', anzahl=10, wahlperiode=20)

        # Should contain expected components
        self.assertIn('person', url)
        self.assertIn('apikey', url)
        self.assertIn('anzahl=10', url)
        self.assertIn('f.wahlperiode=20', url)

    def test_empty_response_handling_integration(self):
        """Test handling of empty responses from real API."""
        # Test with very specific filter that might return empty results
        persons = self.dip.get_person(anzahl=1, person="nonexistent_person_12345")

        # Should return empty list
        self.assertEqual(persons, [])

    def test_plenarprotokoll_integration(self):
        """Test getting plenary protocols from real API."""
        protocols = self.dip.get_plenarprotokoll(anzahl=3)

        # Should return a list
        self.assertIsInstance(protocols, list)

        # Should have some results
        if protocols:
            # Check structure of first protocol
            protocol = protocols[0]
            self.assertIsInstance(protocol, dict)
            self.assertIn('id', protocol)

    def test_vorgang_integration(self):
        """Test getting proceedings from real API."""
        proceedings = self.dip.get_vorgang(anzahl=3)

        # Should return a list
        self.assertIsInstance(proceedings, list)

        # Should have some results
        if proceedings:
            # Check structure of first proceeding
            proceeding = proceedings[0]
            self.assertIsInstance(proceeding, dict)
            self.assertIn('id', proceeding)

    def test_vorgangsposition_integration(self):
        """Test getting proceeding positions from real API."""
        positions = self.dip.get_vorgangsposition(anzahl=3)

        # Should return a list
        self.assertIsInstance(positions, list)

        # Should have some results
        if positions:
            # Check structure of first position
            position = positions[0]
            self.assertIsInstance(position, dict)
            self.assertIn('id', position)


if __name__ == '__main__':
    unittest.main()
