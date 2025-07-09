"""
Example demonstrating the use of content parsers.

This example shows how to use the various parsers to extract
structured information from API responses.
"""

import os
from pydipapi import DipAnfrage, DocumentParser, PersonParser, ActivityParser, ProtocolParser


def main():
    """Demonstrate content parser usage."""
    
    # Initialize the API client
    api_key = os.getenv('DIP_API_KEY')
    if not api_key:
        print("Please set the DIP_API_KEY environment variable")
        return
        
    client = DipAnfrage(api_key=api_key)
    
    # Initialize parsers
    document_parser = DocumentParser()
    person_parser = PersonParser()
    activity_parser = ActivityParser()
    protocol_parser = ProtocolParser()
    
    print("=== Content Parsers Example ===\n")
    
    # Example 1: Parse documents
    print("1. Parsing Documents")
    print("-" * 30)
    
    try:
        documents = client.get_drucksache(anzahl=3)
        if documents:
            parsed_docs = document_parser.parse(documents)
            for i, doc in enumerate(parsed_docs[:2] if isinstance(parsed_docs, list) else [parsed_docs], 1):
                print(f"Document {i}:")
                if 'parsed' in doc:
                    parsed = doc['parsed']
                    print(f"  Type: {parsed.get('document_type', 'Unknown')}")
                    print(f"  Authors: {len(parsed.get('authors', []))}")
                    print(f"  Content Summary: {parsed.get('content_summary', {}).get('word_count', 0)} words")
                    print(f"  Parties mentioned: {parsed.get('parties', [])}")
                    print(f"  Laws referenced: {parsed.get('laws', [])}")
                print()
        else:
            print("No documents found")
    except Exception as e:
        print(f"Error parsing documents: {e}")
    
    # Example 2: Parse persons
    print("2. Parsing Persons")
    print("-" * 30)
    
    try:
        persons = client.get_person(anzahl=3)
        if persons:
            parsed_persons = person_parser.parse(persons)
            for i, person in enumerate(parsed_persons[:2] if isinstance(parsed_persons, list) else [parsed_persons], 1):
                print(f"Person {i}:")
                if 'parsed' in person:
                    parsed = person['parsed']
                    basic = parsed.get('basic_info', {})
                    print(f"  Name: {basic.get('name', 'Unknown')}")
                    print(f"  Party: {parsed.get('party_info', {}).get('current_party', 'Unknown')}")
                    print(f"  Committees: {len(parsed.get('committee_info', {}).get('current_committees', []))}")
                    print(f"  Contact: {parsed.get('contact_info', {}).get('email', 'No email')}")
                print()
        else:
            print("No persons found")
    except Exception as e:
        print(f"Error parsing persons: {e}")
    
    # Example 3: Parse activities
    print("3. Parsing Activities")
    print("-" * 30)
    
    try:
        activities = client.get_aktivitaet(anzahl=3)
        if activities:
            parsed_activities = activity_parser.parse(activities)
            for i, activity in enumerate(parsed_activities[:2] if isinstance(parsed_activities, list) else [parsed_activities], 1):
                print(f"Activity {i}:")
                if 'parsed' in activity:
                    parsed = activity['parsed']
                    print(f"  Type: {parsed.get('activity_type', 'Unknown')}")
                    session = parsed.get('session_info', {})
                    print(f"  Session: {session.get('session_number', 'Unknown')}")
                    print(f"  Date: {session.get('session_date', 'Unknown')}")
                    print(f"  Participants: {len(parsed.get('participants', {}).get('speakers', []))}")
                print()
        else:
            print("No activities found")
    except Exception as e:
        print(f"Error parsing activities: {e}")
    
    # Example 4: Parse protocols
    print("4. Parsing Protocols")
    print("-" * 30)
    
    try:
        protocols = client.get_plenarprotokoll(anzahl=3)
        if protocols:
            parsed_protocols = protocol_parser.parse(protocols)
            for i, protocol in enumerate(parsed_protocols[:2] if isinstance(parsed_protocols, list) else [parsed_protocols], 1):
                print(f"Protocol {i}:")
                if 'parsed' in protocol:
                    parsed = protocol['parsed']
                    session = parsed.get('session_info', {})
                    print(f"  Session: {session.get('session_number', 'Unknown')}")
                    print(f"  Date: {session.get('session_date', 'Unknown')}")
                    speakers = parsed.get('speakers', {})
                    print(f"  Total Speakers: {speakers.get('total_speakers', 0)}")
                    interventions = parsed.get('interventions', {})
                    print(f"  Total Interventions: {interventions.get('total_interventions', 0)}")
                print()
        else:
            print("No protocols found")
    except Exception as e:
        print(f"Error parsing protocols: {e}")
    
    # Example 5: Advanced parsing with custom data
    print("5. Advanced Parsing Example")
    print("-" * 30)
    
    # Create sample data for demonstration
    sample_document = {
        'titel': 'Kleine Anfrage der Abgeordneten Dr. Alice Schmidt (CDU/CSU)',
        'text': 'Die Bundesregierung wird gebeten, folgende Fragen zu beantworten: 1. Wie viele Windkraftanlagen wurden im Jahr 2023 errichtet? 2. Welche Maßnahmen plant die Regierung zur Förderung erneuerbarer Energien? Kontakt: alice.schmidt@bundestag.de, Tel: +49 30 227-12345',
        'datum': '2024-01-15',
        'dokumentart': 'Kleine Anfrage'
    }
    
    print("Parsing sample document:")
    parsed_sample = document_parser.parse(sample_document)
    if isinstance(parsed_sample, dict) and 'parsed' in parsed_sample:
        parsed = parsed_sample['parsed']
        print(f"  Document Type: {parsed.get('document_type')}")
        print(f"  Authors: {parsed.get('authors')}")
        print(f"  Emails: {parsed.get('references', {}).get('emails', [])}")
        print(f"  Phone Numbers: {parsed.get('references', {}).get('phone_numbers', [])}")
        print(f"  Parties: {parsed.get('parties', [])}")
    
    print("\n=== Content Parsers Example Complete ===")


if __name__ == "__main__":
    main() 