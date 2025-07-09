"""
Async example for pydipapi.

This example demonstrates how to use the async API client for concurrent requests.
"""

import asyncio
import os

from pydipapi import AsyncDipAnfrage


async def main():
    """Main async function demonstrating the async API."""
    # Get API key from environment
    api_key = os.getenv('DIP_API_KEY')
    if not api_key:
        print("Please set DIP_API_KEY environment variable")
        return

    # Create async client
    async with AsyncDipAnfrage(api_key=api_key) as client:
        print("🚀 Starting async API requests...")

        # Example 1: Concurrent requests for different data types
        print("\n📊 Fetching different data types concurrently...")

        try:
            # Create tasks for concurrent execution
            tasks = [
                client.get_person(anzahl=5),
                client.get_aktivitaet(anzahl=5),
                client.get_drucksache(anzahl=5),
                client.get_vorgang(anzahl=5)
            ]

            # Execute all tasks concurrently
            results = await asyncio.gather(*tasks)

            persons, activities, documents, proceedings = results

            print(f"✅ Retrieved {len(persons)} persons")
            print(f"✅ Retrieved {len(activities)} activities")
            print(f"✅ Retrieved {len(documents)} documents")
            print(f"✅ Retrieved {len(proceedings)} proceedings")

        except Exception as e:
            print(f"❌ Error in concurrent requests: {e}")

        # Example 2: Search for documents
        print("\n🔍 Searching for documents...")
        try:
            search_results = await client.search_documents("Bundeshaushalt", anzahl=3)
            print(f"✅ Found {len(search_results)} documents matching 'Bundeshaushalt'")
        except Exception as e:
            print(f"❌ Error searching documents: {e}")

        # Example 3: Get recent activities
        print("\n📅 Getting recent activities...")
        try:
            recent_activities = await client.get_recent_activities(days=7, anzahl=5)
            print(f"✅ Retrieved {len(recent_activities)} recent activities")
        except Exception as e:
            print(f"❌ Error getting recent activities: {e}")

        # Example 4: Search for persons by name
        print("\n👥 Searching for persons by name...")
        try:
            persons_by_name = await client.get_person_by_name("Merkel", anzahl=3)
            print(f"✅ Found {len(persons_by_name)} persons matching 'Merkel'")
        except Exception as e:
            print(f"❌ Error searching persons: {e}")

        # Example 5: Get documents by type
        print("\n📄 Getting documents by type...")
        try:
            kleine_anfragen = await client.get_documents_by_type("kleine_anfrage", anzahl=3)
            print(f"✅ Retrieved {len(kleine_anfragen)} kleine Anfragen")
        except Exception as e:
            print(f"❌ Error getting documents by type: {e}")

        print("\n🎉 All async operations completed!")


async def performance_comparison():
    """Compare sync vs async performance."""
    api_key = os.getenv('DIP_API_KEY')
    if not api_key:
        print("Please set DIP_API_KEY environment variable")
        return

    print("\n⚡ Performance comparison...")

    # Async version
    async with AsyncDipAnfrage(api_key=api_key) as async_client:
        start_time = asyncio.get_event_loop().time()

        try:
            # Make multiple concurrent requests
            tasks = [
                async_client.get_person(anzahl=3),
                async_client.get_aktivitaet(anzahl=3),
                async_client.get_drucksache(anzahl=3),
                async_client.get_vorgang(anzahl=3),
                async_client.get_plenarprotokoll(anzahl=3)
            ]

            results = await asyncio.gather(*tasks)
            async_time = asyncio.get_event_loop().time() - start_time

            total_items = sum(len(result) for result in results)
            print(f"⏱️  Async execution time: {async_time:.2f} seconds")
            print(f"📊 Total items retrieved: {total_items}")
        except Exception as e:
            print(f"❌ Error in performance comparison: {e}")


if __name__ == "__main__":
    # Run the main example
    asyncio.run(main())

    # Run performance comparison
    asyncio.run(performance_comparison())
