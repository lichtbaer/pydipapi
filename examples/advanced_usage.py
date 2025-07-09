#!/usr/bin/env python3
"""
Advanced usage examples for the pydipapi library.

This script demonstrates:
- Batch operations for multiple IDs
- Convenience methods for common queries
- Caching and performance optimization
- Rate limiting and retry logic
"""

import os

from pydipapi import DipAnfrage


def main():
    """Demonstrate advanced features of the pydipapi library."""

    # Get API key from environment
    api_key = os.getenv('DIP_API_KEY')
    if not api_key:
        print("Please set the DIP_API_KEY environment variable")
        return

    # Initialize client with advanced settings
    dip = DipAnfrage(
        api_key=api_key,
        rate_limit_delay=0.1,  # 100ms between requests
        max_retries=3,
        enable_cache=True,
        cache_ttl=3600  # 1 hour cache
    )

    print("=== Advanced pydipapi Usage Examples ===\n")

    # 1. Batch Operations
    print("1. Batch Operations")
    print("-" * 30)

    # Example IDs (these would be real IDs in practice)
    person_ids = [12345, 67890, 11111]
    doc_ids = [12345, 67890]
    protocol_ids = [11111, 22222]

    try:
        # Get multiple persons
        persons = dip.get_person_ids(person_ids)
        print(f"Retrieved {len(persons)} persons in batch")

        # Get multiple documents with text
        documents = dip.get_drucksache_ids(doc_ids, text=True)
        print(f"Retrieved {len(documents)} documents with text in batch")

        # Get multiple protocols without text
        protocols = dip.get_plenarprotokoll_ids(protocol_ids, text=False)
        print(f"Retrieved {len(protocols)} protocols (metadata only) in batch")

    except Exception as e:
        print(f"Batch operations failed: {e}")

    print()

    # 2. Convenience Methods
    print("2. Convenience Methods")
    print("-" * 30)

    try:
        # Search for documents
        search_results = dip.search_documents("Bundeshaushalt", anzahl=5)
        print(f"Found {len(search_results)} documents matching 'Bundeshaushalt'")

        # Get recent activities
        recent_activities = dip.get_recent_activities(days=7, anzahl=10)
        print(f"Found {len(recent_activities)} recent activities")

        # Search for persons by name
        persons = dip.get_person_by_name("Merkel", anzahl=3)
        print(f"Found {len(persons)} persons matching 'Merkel'")

        # Get documents by type
        anträge = dip.get_documents_by_type("Antrag", anzahl=5)
        print(f"Found {len(anträge)} documents of type 'Antrag'")

        # Get proceedings by type
        gesetzgebung = dip.get_proceedings_by_type("Gesetzgebung", anzahl=5)
        print(f"Found {len(gesetzgebung)} proceedings of type 'Gesetzgebung'")

    except Exception as e:
        print(f"Convenience methods failed: {e}")

    print()

    # 3. Caching and Performance
    print("3. Caching and Performance")
    print("-" * 30)

    try:
        # First request (will be cached)
        print("Making first request (will be cached)...")
        persons1 = dip.get_person(anzahl=5)
        print(f"Retrieved {len(persons1)} persons")

        # Second request (should use cache)
        print("Making second request (should use cache)...")
        persons2 = dip.get_person(anzahl=5)
        print(f"Retrieved {len(persons2)} persons")

        # Clear cache
        print("Clearing cache...")
        dip.clear_cache()
        print("Cache cleared")

        # Clear expired cache entries
        print("Clearing expired cache entries...")
        dip.clear_expired_cache()
        print("Expired cache entries cleared")

    except Exception as e:
        print(f"Caching operations failed: {e}")

    print()

    # 4. Error Handling and Retry Logic
    print("4. Error Handling and Retry Logic")
    print("-" * 30)

    try:
        # This should demonstrate retry logic if there are temporary failures
        print("Testing retry logic with multiple requests...")

        for i in range(3):
            try:
                activities = dip.get_aktivitaet(anzahl=2)
                print(f"Request {i+1}: Retrieved {len(activities)} activities")
            except Exception as e:
                print(f"Request {i+1} failed: {e}")

    except Exception as e:
        print(f"Error handling test failed: {e}")

    print()
    print("=== Advanced Usage Examples Complete ===")


if __name__ == "__main__":
    main()
