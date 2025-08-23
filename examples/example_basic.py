#!/usr/bin/env python3
"""
Basic usage example for the pydipapi library.

This script demonstrates:
- Basic API client initialization
- Simple data retrieval
- Error handling
"""

import os
import sys

from pydipapi import DipAnfrage


def main():
    """Demonstrate basic usage of the pydipapi library."""

    # Get API key from environment
    api_key = os.getenv("DIP_API_KEY")
    if not api_key:
        print("Error: DIP_API_KEY environment variable not set")
        print("Please set your API key:")
        print("export DIP_API_KEY='your-api-key-here'")
        print(
            "You can get an API key from: https://dip.bundestag.de/über-dip/hilfe/api"
        )
        sys.exit(1)

    # Check if API key looks valid (not a placeholder)
    if api_key in ["your-api-key-here", "test-key", "demo-key"]:
        print("Error: Please use a valid API key, not a placeholder")
        print(
            "You can get an API key from: https://dip.bundestag.de/über-dip/hilfe/api"
        )
        sys.exit(1)

    print("=== Basic pydipapi Usage Example ===\n")

    try:
        # Initialize the client
        print("Initializing API client...")
        dip = DipAnfrage(api_key=api_key)
        print("✓ Client initialized successfully")

        # Test basic functionality
        print("\nTesting basic API functionality...")

        # Get some persons
        print("Fetching persons...")
        persons = dip.get_person(anzahl=5)
        print(f"✓ Retrieved {len(persons)} persons")

        if persons:
            print(f"First person: {persons[0].get('name', 'Unknown')}")

        # Search for documents
        print("\nSearching for documents...")
        documents = dip.search_documents("Bundestag", anzahl=3)
        print(f"✓ Retrieved {len(documents)} documents")

        if documents:
            print(f"First document: {documents[0].get('titel', 'Unknown')}")

        # Get activities
        print("\nFetching activities...")
        activities = dip.get_aktivitaet(anzahl=3)
        print(f"✓ Retrieved {len(activities)} activities")

        if activities:
            print(f"First activity: {activities[0].get('titel', 'Unknown')}")

        print("\n✓ All tests completed successfully!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting tips:")
        print("- Check if your API key is valid")
        print("- Ensure you have internet connectivity")
        print("- Check if the API service is available")
        sys.exit(1)


if __name__ == "__main__":
    main()
