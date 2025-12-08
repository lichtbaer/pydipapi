# Content-Parser

Die Content-Parser von pydipapi extrahieren strukturierte Informationen aus den API-Antworten der Bundestag API. Sie sind besonders nützlich für die Analyse von Protokollen, Dokumenten und Personen-Daten.

## Übersicht

pydipapi bietet vier spezialisierte Parser:

- **ProtocolParser** - Extrahiert Informationen aus Plenarprotokollen
- **DocumentParser** - Analysiert Drucksachen und andere Dokumente
- **PersonParser** - Verarbeitet Personen-Daten von Abgeordneten
- **ActivityParser** - Extrahiert Informationen aus Aktivitäten

## ProtocolParser

Der ProtocolParser ist speziell für Volltext-Plenarprotokolle entwickelt und extrahiert:

- **Session-Informationen** - Sitzungsnummer, Wahlperiode, Datum
- **Sprecher** - Redner, Parteien, Redezeiten
- **Interventionen** - Redebeiträge und Zwischenrufe
- **Themen** - Diskussionsthemen und Tagesordnungspunkte
- **Abstimmungen** - Abstimmungsergebnisse
- **Prozedurale Elemente** - Unterbrechungen, Geschäftsordnungsanträge
- **Referenzen** - Links, Gesetze, Kontaktdaten

### Verwendung

```python
from pydipapi import DipAnfrage, ProtocolParser

# Client und Parser initialisieren
dip = DipAnfrage(api_key='ihr_api_key')
parser = ProtocolParser()

# Volltext-Protokoll abrufen
protocols = dip.get_plenarprotokoll(anzahl=1, text=True)

if protocols:
    # Protokoll parsen
    parsed = parser.parse(protocols[0])
    
    # Session-Informationen
    session = parsed['parsed']['session_info']
    print(f"Session: {session['session_number']}")
    print(f"Wahlperiode: {session['legislative_period']}")
    
    # Sprecher-Informationen
    speakers = parsed['parsed']['speakers']
    print(f"Gesamte Sprecher: {speakers['total_speakers']}")
    print(f"Parteien: {speakers['parties_present']}")
    
    # Interventionen
    interventions = parsed['parsed']['interventions']
    print(f"Interventionen: {interventions['total_interventions']}")
    
    # Themen
    topics = parsed['parsed']['topics']
    print(f"Hauptthemen: {topics['main_topics']}")
    
    # Abstimmungen
    votes = parsed['parsed']['votes']
    print(f"Ja-Stimmen: {votes['yes_votes']}")
    print(f"Nein-Stimmen: {votes['no_votes']}")
```

### Beispiel-Output

```python
# Beispiel für geparste Daten
{
    'parsed': {
        'session_info': {
            'session_number': '123',
            'legislative_period': '20',
            'session_date': datetime(2025, 1, 15),
            'start_time': '09:00',
            'end_time': '18:00',
            'location': 'Berlin',
            'session_chair': 'Dr. Wolfgang Schäuble',
            'secretary': 'Max Mustermann'
        },
        'speakers': {
            'speakers_list': [
                {
                    'name': 'Dr. Alice Schmidt',
                    'party': 'CDU/CSU',
                    'role': 'Abgeordnete',
                    'speaking_time': '15:30',
                    'interventions': 3
                }
            ],
            'parties_present': ['CDU', 'CSU', 'SPD', 'FDP'],
            'total_speakers': 7,
            'speaking_times': {
                'Dr. Alice Schmidt': '15:30'
            }
        },
        'interventions': {
            'interventions_list': [
                {
                    'speaker': 'Dr. Alice Schmidt',
                    'content': 'Sehr geehrte Damen und Herren...',
                    'length': 150
                }
            ],
            'total_interventions': 7,
            'intervention_types': {},
            'speaker_interventions': {
                'Dr. Alice Schmidt': [...]
            }
        },
        'topics': {
            'agenda_items': [
                {
                    'title': 'Beratung über den Gesetzentwurf zur Förderung erneuerbarer Energien',
                    'description': 'Diskussion über Klimaschutzmaßnahmen',
                    'start_time': '09:15',
                    'end_time': '11:30',
                    'speakers': ['Dr. Alice Schmidt', 'Herr Mueller']
                }
            ],
            'main_topics': ['Umweltpolitik', 'Energiewende'],
            'laws_discussed': ['Gesetz zur Förderung erneuerbarer Energien'],
            'documents_referenced': []
        },
        'votes': {
            'vote_results': [
                {
                    'topic': 'Gesetzentwurf erneuerbare Energien',
                    'result': 'angenommen',
                    'yes': 350,
                    'no': 150,
                    'abstentions': 50,
                    'absent': 0
                }
            ],
            'total_votes': 550,
            'yes_votes': 350,
            'no_votes': 150,
            'abstentions': 50,
            'absent': 0
        },
        'procedural_elements': {
            'interruptions': [],
            'procedural_motions': [],
            'points_of_order': [],
            'adjournments': [],
            'has_interruptions': False,
            'has_procedural_motions': False
        },
        'dates': {
            'datum': datetime(2025, 1, 15),
            'sitzungsdatum': datetime(2025, 1, 15)
        },
        'references': {
            'links': ['https://bundestag.de'],
            'laws': ['§ 1 EEG'],
            'emails': ['alice.schmidt@bundestag.de'],
            'phone_numbers': ['+49 30 227-12345']
        }
    }
}
```

## DocumentParser

Der DocumentParser analysiert Drucksachen und andere Dokumente:

- **Dokumenttyp** - Antrag, Anfrage, Gesetzentwurf, etc.
- **Autoren** - Verfasser mit Namen und Partei
- **Inhaltszusammenfassung** - Wortanzahl, Zeichenanzahl, Vorschau
- **Parteien** - Erwähnte politische Parteien
- **Referenzen** - Links, E-Mails, Telefonnummern
- **Datumsextraktion** - Erkannte Datumsangaben

### Verwendung

```python
from pydipapi import DocumentParser

parser = DocumentParser()

# Dokument parsen
docs = dip.get_drucksache(anzahl=1)
if docs:
    parsed = parser.parse(docs[0])
    
    # Dokumenttyp
    doc_type = parsed['parsed']['document_type']
    print(f"Dokumenttyp: {doc_type}")
    
    # Autoren
    authors = parsed['parsed']['authors']
    for author in authors:
        print(f"Autor: {author['name']} ({author['party']})")
    
    # Inhaltszusammenfassung
    summary = parsed['parsed']['content_summary']
    print(f"Wörter: {summary['word_count']}")
    print(f"Zeichen: {summary['character_count']}")
    print(f"Vorschau: {summary['preview']}")
    
    # Parteien
    parties = parsed['parsed']['parties']
    print(f"Parteien: {parties}")
```

## PersonParser

Der PersonParser extrahiert Informationen aus Personen-Daten:

- **Grundinformationen** - Name, Vorname, Nachname
- **Partei-Informationen** - Aktuelle Partei, erwähnte Parteien
- **Kontaktinformationen** - E-Mail, Telefon, Adresse
- **Aktivitäten** - Beteiligte Aktivitäten und Rollen
- **Referenzen** - Links und Kontaktdaten

### Verwendung

```python
from pydipapi import PersonParser

parser = PersonParser()

# Person parsen
persons = dip.get_person(anzahl=1)
if persons:
    parsed = parser.parse(persons[0])
    
    # Grundinformationen
    basic = parsed['parsed']['basic_info']
    print(f"Name: {basic['name']}")
    print(f"Vorname: {basic['first_name']}")
    print(f"Nachname: {basic['last_name']}")
    
    # Partei-Informationen
    party = parsed['parsed']['party_info']
    print(f"Aktuelle Partei: {party['current_party']}")
    print(f"Erwähnte Parteien: {party['mentioned_parties']}")
    
    # Kontaktinformationen
    contact = parsed['parsed']['contact_info']
    print(f"E-Mail: {contact['email']}")
    print(f"Telefon: {contact['phone']}")
```

## ActivityParser

Der ActivityParser analysiert Aktivitäten und Sitzungen:

- **Aktivitätstyp** - Plenarsitzung, Ausschusssitzung, etc.
- **Session-Informationen** - Sitzungsnummer, Wahlperiode
- **Teilnehmer** - Anwesende Parteien und Personen
- **Abstimmungen** - Abstimmungsergebnisse
- **Themen** - Diskussionsthemen

### Verwendung

```python
from pydipapi import ActivityParser

parser = ActivityParser()

# Aktivität parsen
activities = dip.get_aktivitaet(anzahl=1)
if activities:
    parsed = parser.parse(activities[0])
    
    # Aktivitätstyp
    activity_type = parsed['parsed']['activity_type']
    print(f"Aktivitätstyp: {activity_type}")
    
    # Session-Informationen
    session = parsed['parsed']['session_info']
    print(f"Session: {session['session_number']}")
    print(f"Wahlperiode: {session['legislative_period']}")
    
    # Teilnehmer
    participants = parsed['parsed']['participants']
    print(f"Parteien: {participants['parties_present']}")
    print(f"Personen: {participants['persons_present']}")
    
    # Abstimmungen
    votes = parsed['parsed']['votes']
    print(f"Ja: {votes['yes_votes']}")
    print(f"Nein: {votes['no_votes']}")
```

## Erweiterte Verwendung

### Batch-Parsing

Alle Parser unterstützen das Parsen mehrerer Objekte:

```python
# Mehrere Protokolle parsen
protocols = dip.get_plenarprotokoll(anzahl=5, text=True)
parsed_protocols = parser.parse(protocols)  # Liste von geparsten Protokollen

# Mehrere Dokumente parsen
docs = dip.get_drucksache(anzahl=10)
parsed_docs = doc_parser.parse(docs)  # Liste von geparsten Dokumenten
```

### Benutzerdefinierte Parser

Sie können eigene Parser erstellen, die von BaseParser erben:

```python
from pydipapi.parsers import BaseParser

class CustomParser(BaseParser):
    def parse(self, data):
        # Ihre eigene Parsing-Logik
        return {'parsed': {'custom_field': 'value'}}
```

### Regex-Patterns

Alle Parser bieten nützliche Regex-Methoden:

```python
parser = ProtocolParser()

# Text extrahieren
email = parser.extract_text(text, r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')

# Alle Matches finden
parties = parser.extract_all_text(text, r'\b(CDU|SPD|FDP|Grüne)\b')

# Zahlen extrahieren
numbers = parser.extract_numbers(text)

# Datum parsen
date = parser.parse_date("2025-01-15")
```

## Beispiele

Vollständige Beispiele finden Sie in:

- `examples/protocol_parser_demo.py` - Protokoll-Parser Demo
- `examples/content_parsers_example.py` - Allgemeine Content-Parser Beispiele
- `tests/test_parsers.py` - Unit-Tests für alle Parser

## Performance-Tipps

1. **Caching aktivieren** - Verwenden Sie den integrierten Cache
2. **Batch-Operationen** - Parsen Sie mehrere Objekte auf einmal
3. **Async-Support** - Nutzen Sie AsyncDipAnfrage für bessere Performance
4. **Selektive Extraktion** - Extrahieren Sie nur benötigte Felder

```python
# Async mit Parsern
from pydipapi import AsyncDipAnfrage, ProtocolParser

async def parse_protocols():
    async_dip = AsyncDipAnfrage(api_key='key')
    parser = ProtocolParser()
    
    protocols = await async_dip.get_plenarprotokoll(anzahl=10, text=True)
    parsed = parser.parse(protocols)
    
    return parsed
``` 