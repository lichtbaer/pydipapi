# Grundlegende Verwendung

Dieser Guide zeigt Ihnen, wie Sie pydipapi für den Zugriff auf die deutsche Bundestag API verwenden.

!!! tip "Async Support"
    pydipapi bietet sowohl synchrone als auch asynchrone APIs. Für bessere Performance bei mehreren gleichzeitigen Anfragen verwenden Sie die Async-Version!

!!! tip "Interaktive Lernumgebung"
    Für eine praxisnahe Einführung nutzen Sie unsere **[Jupyter Notebooks](notebooks.md)**! 
    Diese bieten Schritt-für-Schritt Anleitungen mit ausführbarem Code in drei Schwierigkeitsstufen.

## Installation

```bash
pip install pydipapi
```

## API-Key einrichten

1. Besuchen Sie [https://dip.bundestag.de/über-dip/hilfe/api](https://dip.bundestag.de/über-dip/hilfe/api)
2. Registrieren Sie sich für einen API-Key
3. Setzen Sie die Umgebungsvariable:

```bash
export DIP_API_KEY='ihr_api_key'
```

## Grundlegende Verwendung

### Client initialisieren

### Synchrone API

```python
from pydipapi import DipAnfrage

# Einfache Initialisierung
dip = DipAnfrage(api_key='ihr_api_key')

# Erweiterte Konfiguration
dip = DipAnfrage(
    api_key='ihr_api_key',
    rate_limit_delay=0.1,    # 100ms zwischen Requests
    max_retries=3,           # Maximale Wiederholungsversuche
    enable_cache=True,        # Caching aktivieren
    cache_ttl=3600           # Cache-TTL in Sekunden
)
```

### Asynchrone API

```python
import asyncio
from pydipapi import AsyncDipAnfrage

# Async Client mit Context Manager
async def main():
    async with AsyncDipAnfrage(api_key='ihr_api_key') as dip:
        # Alle async Methoden haben die gleichen Namen wie die sync Versionen
        persons = await dip.get_person(anzahl=10)
        activities = await dip.get_aktivitaet(anzahl=10)
        
        # Gleichzeitige Anfragen für bessere Performance
        tasks = [
            dip.get_person(anzahl=5),
            dip.get_aktivitaet(anzahl=5),
            dip.get_drucksache(anzahl=5)
        ]
        results = await asyncio.gather(*tasks)
        persons, activities, documents = results

# Ausführen
asyncio.run(main())
```

### Personen abrufen

```python
# Erste 10 Personen abrufen
persons = dip.get_person(anzahl=10)

# Personen aus einer bestimmten Wahlperiode
persons_20 = dip.get_person(anzahl=10, wahlperiode=20)

# Personen nach Namen suchen
merkel = dip.get_person_by_name("Merkel", anzahl=5)

# Mehrere Personen nach IDs abrufen
person_ids = [12345, 67890, 11111]
persons_batch = dip.get_person_ids(person_ids)
```

### Aktivitäten abrufen

```python
# Letzte Aktivitäten abrufen
activities = dip.get_aktivitaet(anzahl=20)

# Aktivitäten aus einem Zeitraum
activities_filtered = dip.get_aktivitaet(
    anzahl=10,
    datum_start="2025-01-01",
    datum_end="2025-12-31"
)

# Aktuelle Aktivitäten (letzte 7 Tage)
recent = dip.get_recent_activities(days=7, anzahl=10)

# Mehrere Aktivitäten nach IDs abrufen
activity_ids = [12345, 67890, 11111]
activities_batch = dip.get_aktivitaet_ids(activity_ids)
```

### Dokumente abrufen

```python
# Dokumente abrufen (nur Metadaten)
docs_meta = dip.get_drucksache(anzahl=10, text=False)

# Dokumente mit Text abrufen
docs_text = dip.get_drucksache(anzahl=10, text=True)

# Dokumente nach Typ filtern
anträge = dip.get_documents_by_type("Antrag", anzahl=10)

# Dokumente durchsuchen
budget_docs = dip.search_documents("Bundeshaushalt", anzahl=10)

# Mehrere Dokumente nach IDs abrufen
doc_ids = [12345, 67890]
docs_batch = dip.get_drucksache_ids(doc_ids, text=True)
```

### Plenarprotokolle abrufen

```python
# Protokolle abrufen (nur Metadaten)
protocols_meta = dip.get_plenarprotokoll(anzahl=10, text=False)

# Protokolle mit Text abrufen
protocols_text = dip.get_plenarprotokoll(anzahl=10, text=True)

# Mehrere Protokolle nach IDs abrufen
protocol_ids = [12345, 67890]
protocols_batch = dip.get_plenarprotokoll_ids(protocol_ids, text=False)
```

### Strukturierte XML-Plenarprotokolle (falls verfügbar)

Für viele Bundestag-Plenarprotokolle (typischerweise Wahlperiode ≥ 18) enthält das DIP-Objekt in `fundstelle.xml_url` einen Link auf die strukturierte XML-Version (gehostet auf dserver).

```python
from pydipapi import ProtocolXmlParser

# XML für ein einzelnes Protokoll-Objekt laden (falls verfügbar)
protocols = dip.get_plenarprotokoll(anzahl=1, text=True)
if protocols:
    xml_text = dip.get_plenarprotokoll_xml(protocols[0])
    if xml_text:
        parser = ProtocolXmlParser()
        parsed = parser.parse(xml_text)
        print(parsed["parsed"]["session_info"])

# Oder direkt per DIP-ID (Convenience)
xml_text = dip.get_plenarprotokoll_xml_by_id(id=123456, text=True)
```

### Vorgänge abrufen

```python
# Vorgänge abrufen
proceedings = dip.get_vorgang(anzahl=10)

# Vorgänge nach Typ filtern
gesetzgebung = dip.get_proceedings_by_type("Gesetzgebung", anzahl=10)

# Mehrere Vorgänge nach IDs abrufen
proceeding_ids = [12345, 67890]
proceedings_batch = dip.get_vorgang_ids(proceeding_ids)
```

## Filter-Optionen

### Datumsfilter

```python
# Aktivitäten aus einem Zeitraum
activities = dip.get_aktivitaet(
    anzahl=20,
    datum_start="2025-01-01",
    datum_end="2025-12-31"
)

# Dokumente aus einem Zeitraum
docs = dip.get_drucksache(
    anzahl=10,
    datum_start="2025-01-01",
    datum_end="2025-06-30",
    text=False
)
```

### Wahlperioden-Filter

```python
# Personen aus der 20. Wahlperiode
persons = dip.get_person(anzahl=20, wahlperiode=20)

# Aktivitäten aus der 19. Wahlperiode
activities = dip.get_aktivitaet(anzahl=20, wahlperiode=19)
```

### Textbasierte Filter

```python
# Dokumente mit bestimmten Begriffen
docs = dip.search_documents("Klimaschutz", anzahl=10)

# Personen nach Namen
persons = dip.get_person_by_name("Scholz", anzahl=5)
```

### Typ-Filter

```python
# Dokumente nach Typ
anträge = dip.get_documents_by_type("Antrag", anzahl=10)
gesetzentwürfe = dip.get_documents_by_type("Gesetzentwurf", anzahl=10)

# Vorgänge nach Typ
gesetzgebung = dip.get_proceedings_by_type("Gesetzgebung", anzahl=10)
berichte = dip.get_proceedings_by_type("Bericht", anzahl=10)
```

## Einzelne Elemente abrufen

```python
# Einzelne Person nach ID
person = dip.get_person_id(id=12345)

# Einzelne Aktivität nach ID
activity = dip.get_aktivitaet_by_id(id=67890)

# Einzelnes Dokument nach ID
document = dip.get_drucksache_by_id(id=11111)

# Einzelnes Protokoll nach ID
protocol = dip.get_plenarprotokoll_by_id(id=22222)

# Einzelnen Vorgang nach ID
proceeding = dip.get_vorgang_by_id(id=33333)
```

## Performance-Optimierung

### Caching aktivieren

```python
# Caching mit langer TTL für selten ändernde Daten
dip = DipAnfrage(
    api_key='ihr_api_key',
    enable_cache=True,
    cache_ttl=7200  # 2 Stunden
)

# Cache verwalten
dip.clear_cache()           # Gesamten Cache löschen
dip.clear_expired_cache()   # Abgelaufene Einträge löschen
```

### Rate Limiting anpassen

```python
# Konservatives Rate Limiting für stabile Verbindungen
dip_conservative = DipAnfrage(
    api_key='ihr_api_key',
    rate_limit_delay=0.5,  # 500ms zwischen Requests
    max_retries=5
)

# Aggressives Rate Limiting für schnelle Abfragen
dip_aggressive = DipAnfrage(
    api_key='ihr_api_key',
    rate_limit_delay=0.05,  # 50ms zwischen Requests
    max_retries=2
)
```

### Batch-Operationen verwenden

```python
# Statt mehrere einzelne Requests
for person_id in [12345, 67890, 11111]:
    person = dip.get_person_id(person_id)

# Batch-Request verwenden
persons = dip.get_person_ids([12345, 67890, 11111])
```

## Fehlerbehebung

### Häufige Probleme

#### 1. Authentifizierung fehlgeschlagen (401-Fehler)

**Symptome:**
```
API request failed: An API key is required to access this service.
```

**Lösung:**
1. Holen Sie sich einen gültigen API-Key von: https://dip.bundestag.de/über-dip/hilfe/api
2. Setzen Sie die Umgebungsvariable:
   ```bash
   export DIP_API_KEY='ihr-echter-api-key'
   ```
3. Stellen Sie sicher, dass Sie keine Platzhalter-Werte wie "your-api-key-here" verwenden

#### 2. Keine Daten zurückgegeben

**Symptome:**
- API-Aufrufe erfolgreich, aber leere Listen zurückgegeben
- Keine Fehlermeldungen, aber keine Daten

**Mögliche Ursachen:**
1. **Ungültiger API-Key**: Auch mit ungültigem Key können einige Endpunkte leere Ergebnisse zurückgeben
2. **Keine passenden Daten**: Ihre Suchkriterien könnten zu restriktiv sein
3. **API Rate Limiting**: Sie könnten Rate Limits erreichen

**Lösungen:**
1. Überprüfen Sie Ihren API-Key mit einem einfachen Request
2. Versuchen Sie breitere Suchbegriffe
3. Fügen Sie Verzögerungen zwischen Requests hinzu
4. Überprüfen Sie die API-Dokumentation für gültige Parameter

#### 3. Rate Limiting (429-Fehler)

**Symptome:**
```
Rate limit exceeded. Please wait before making more requests.
```

**Lösung:**
1. Erhöhen Sie die Verzögerung zwischen Requests:
   ```python
   dip = DipAnfrage(api_key, rate_limit_delay=0.5)  # 500ms Verzögerung
   ```
2. Reduzieren Sie die Anzahl gleichzeitiger Requests
3. Implementieren Sie exponentielles Backoff in Ihrer Anwendung

#### 4. Netzwerkprobleme

**Symptome:**
- Verbindungs-Timeouts
- DNS-Auflösungsfehler
- SSL-Zertifikatsfehler

**Lösungen:**
1. Überprüfen Sie Ihre Internetverbindung
2. Stellen Sie sicher, dass der API-Endpunkt erreichbar ist: https://search.dip.bundestag.de/api/v1
3. Überprüfen Sie, ob Ihre Firewall die Requests blockiert
4. Versuchen Sie es mit einem anderen Netzwerk

### Debugging

#### Debug-Logging aktivieren

Um detaillierte Informationen über das Geschehen zu erhalten:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from pydipapi import DipAnfrage
dip = DipAnfrage(api_key)
```

#### API-Key-Gültigkeit testen

```python
import requests

api_key = "ihr-api-key"
url = "https://search.dip.bundestag.de/api/v1/person"
params = {"apikey": api_key, "anzahl": 1}

response = requests.get(url, params=params)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
```

#### API-Status überprüfen

```python
# Grundlegende Konnektivität testen
import requests
response = requests.get("https://search.dip.bundestag.de/api/v1")
print(f"API Status: {response.status_code}")
```

### Hilfe bekommen

1. **Logs überprüfen**: Aktivieren Sie Debug-Logging für detaillierte Informationen
2. **Mit curl testen**: Testen Sie die API direkt mit curl, um Probleme zu isolieren
3. **API-Dokumentation prüfen**: https://dip.bundestag.de/über-dip/hilfe/api
4. **Issues melden**: Erstellen Sie ein Issue im GitHub-Repository mit:
   - Ihrer Fehlermeldung
   - Dem Code, der den Fehler verursacht hat
   - Debug-Logs (ohne sensible Informationen)

### Beispiel-Debug-Skript

```python
#!/usr/bin/env python3
import logging
import requests
from pydipapi import DipAnfrage

# Debug-Logging aktivieren
logging.basicConfig(level=logging.DEBUG)

def debug_api():
    api_key = "ihr-api-key"
    
    # Direkten API-Aufruf testen
    url = "https://search.dip.bundestag.de/api/v1/person"
    params = {"apikey": api_key, "anzahl": 1}
    
    print("Direkten API-Aufruf testen...")
    response = requests.get(url, params=params)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    # pydipapi testen
    print("\npydipapi testen...")
    dip = DipAnfrage(api_key)
    persons = dip.get_person(anzahl=1)
    print(f"{len(persons)} Personen abgerufen")

if __name__ == "__main__":
    debug_api()
```

## Nächste Schritte

- **[API-Referenz](api_reference.md)** - Vollständige API-Dokumentation
- **[Entwickler-Guide](developer_guide.md)** - Erweiterte Nutzung
- **[Jupyter Notebooks](notebooks.md)** - Interaktive Beispiele 