"""
Demo für den Protokoll-Parser mit Volltext-Plenarprotokollen.
"""

import os

from pydipapi import DipAnfrage, ProtocolParser


def demo_protocol_parser():
    """Demonstriert die Verwendung des Protokoll-Parsers für Volltext."""

    # Initialize the API client
    api_key = os.getenv("DIP_API_KEY")
    if not api_key:
        print("Bitte setzen Sie die DIP_API_KEY Umgebungsvariable")
        return

    client = DipAnfrage(api_key=api_key)
    parser = ProtocolParser()

    print("=== Protokoll-Parser Demo für Volltext-Plenarprotokolle ===\n")

    # Beispiel 1: Volltext-Protokoll abrufen und parsen
    print("1. Abrufen und Parsen eines Volltext-Protokolls")
    print("-" * 50)

    try:
        # Hole ein Volltext-Protokoll (text=True für Volltext)
        protocols = client.get_plenarprotokoll(anzahl=1, text=True)

        if protocols:
            protocol = protocols[0]
            print(f"Protokoll gefunden: {protocol.get('titel', 'Unbekannt')}")
            print(f"Session: {protocol.get('sitzungsnummer', 'Unbekannt')}")
            print(f"Datum: {protocol.get('sitzungsdatum', 'Unbekannt')}")

            # Parse das Protokoll
            parsed_protocol = parser.parse(protocol)

            if isinstance(parsed_protocol, dict) and "parsed" in parsed_protocol:
                parsed = parsed_protocol["parsed"]

                # Session-Informationen
                session = parsed.get("session_info", {})
                print("\nSession-Info:")
                print(f"  Session-Nummer: {session.get('session_number', 'Unbekannt')}")
                print(
                    f"  Wahlperiode: {session.get('legislative_period', 'Unbekannt')}"
                )
                print(f"  Datum: {session.get('session_date', 'Unbekannt')}")

                # Sprecher-Informationen
                speakers = parsed.get("speakers", {})
                print("\nSprecher-Info:")
                print(f"  Gesamte Sprecher: {speakers.get('total_speakers', 0)}")
                print(f"  Parteien anwesend: {speakers.get('parties_present', [])}")

                # Interventionen
                interventions = parsed.get("interventions", {})
                print("\nInterventionen:")
                print(
                    f"  Gesamte Interventionen: {interventions.get('total_interventions', 0)}"
                )

                # Themen
                topics = parsed.get("topics", {})
                print("\nThemen:")
                print(f"  Hauptthemen: {len(topics.get('main_topics', []))}")
                print(f"  Diskutierte Gesetze: {len(topics.get('laws_discussed', []))}")

                # Abstimmungen
                votes = parsed.get("votes", {})
                print("\nAbstimmungen:")
                print(f"  Ja-Stimmen: {votes.get('yes_votes', 0)}")
                print(f"  Nein-Stimmen: {votes.get('no_votes', 0)}")
                print(f"  Enthaltungen: {votes.get('abstentions', 0)}")
                print(f"  Gesamte Stimmen: {votes.get('total_votes', 0)}")

                # Prozedurale Elemente
                procedural = parsed.get("procedural_elements", {})
                print("\nProzedurale Elemente:")
                print(
                    f"  Hat Unterbrechungen: {procedural.get('has_interruptions', False)}"
                )
                print(
                    f"  Hat Geschäftsordnungsanträge: {procedural.get('has_procedural_motions', False)}"
                )

                # Referenzen
                references = parsed.get("references", {})
                print("\nReferenzen:")
                print(f"  Links: {len(references.get('links', []))}")
                print(f"  Gesetze: {len(references.get('laws', []))}")
                print(f"  E-Mails: {len(references.get('emails', []))}")

            else:
                print("Keine geparsten Daten gefunden")
        else:
            print("Keine Protokolle gefunden")

    except Exception as e:
        print(f"Fehler beim Abrufen der Protokolle: {e}")

    # Beispiel 2: Beispiel-Protokoll mit Volltext simulieren
    print("\n\n2. Beispiel-Protokoll mit Volltext simulieren")
    print("-" * 50)

    sample_protocol = {
        "titel": "Plenarprotokoll 20/123",
        "sitzungsnummer": "123",
        "wahlperiode": "20",
        "sitzungsdatum": "2025-01-15",
        "text": """
        Deutscher Bundestag
        20. Wahlperiode
        123. Sitzung
        Berlin, Montag, den 15. Januar 2025

        Präsident Dr. Wolfgang Schäuble:
        Ich eröffne die 123. Sitzung des Deutschen Bundestages.

        Punkt 1: Beratung über den Gesetzentwurf zur Förderung erneuerbarer Energien

        Herr Dr. Schmidt (CDU/CSU): Sehr geehrte Damen und Herren, der vorliegende Gesetzentwurf ist ein wichtiger Schritt zur Energiewende. Wir unterstützen die Ziele, haben aber Bedenken bei der Umsetzung.

        Frau Mueller (SPD): Vielen Dank, Herr Präsident. Die SPD begrüßt diesen Gesetzentwurf. Er ist ein notwendiger Schritt zur Erreichung unserer Klimaziele.

        Abstimmung: Ja: 350, Nein: 150, Enthaltungen: 50

        Punkt 2: Kleine Anfrage der Abgeordneten Dr. Weber (FDP)

        Herr Dr. Weber (FDP): Sehr geehrte Damen und Herren, ich richte eine kleine Anfrage an die Bundesregierung bezüglich der Digitalisierung der Verwaltung.

        Kontakt: weber@bundestag.de, Tel: +49 30 227-54321
        """,
    }

    print("Parsing Beispiel-Protokoll...")
    parsed_sample = parser.parse(sample_protocol)

    if isinstance(parsed_sample, dict) and "parsed" in parsed_sample:
        parsed = parsed_sample["parsed"]

        print("\nSession-Info:")
        session = parsed.get("session_info", {})
        print(f"  Session: {session.get('session_number', 'Unbekannt')}")
        print(f"  Wahlperiode: {session.get('legislative_period', 'Unbekannt')}")

        print("\nSprecher-Info:")
        speakers = parsed.get("speakers", {})
        print(f"  Gesamte Sprecher: {speakers.get('total_speakers', 0)}")
        print(f"  Parteien: {speakers.get('parties_present', [])}")

        print("\nInterventionen:")
        interventions = parsed.get("interventions", {})
        print(
            f"  Gesamte Interventionen: {interventions.get('total_interventions', 0)}"
        )

        print("\nThemen:")
        topics = parsed.get("topics", {})
        print(f"  Hauptthemen: {topics.get('main_topics', [])}")
        print(f"  Gesetze: {topics.get('laws_discussed', [])}")

        print("\nAbstimmungen:")
        votes = parsed.get("votes", {})
        print(f"  Ja: {votes.get('yes_votes', 0)}")
        print(f"  Nein: {votes.get('no_votes', 0)}")
        print(f"  Enthaltungen: {votes.get('abstentions', 0)}")

        print("\nReferenzen:")
        references = parsed.get("references", {})
        print(f"  E-Mails: {references.get('emails', [])}")
        print(f"  Telefonnummern: {references.get('phone_numbers', [])}")

    print("\n=== Protokoll-Parser Demo abgeschlossen ===")


if __name__ == "__main__":
    demo_protocol_parser()
