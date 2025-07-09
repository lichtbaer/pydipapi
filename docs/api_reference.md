# API-Referenz

Diese Seite bietet eine vollständige Referenz für alle API-Methoden und Parameter von pydipapi.

## Übersicht

pydipapi ist ein Python-Client für die deutsche Bundestag API (DIP) mit erweiterten Funktionen für Batch-Operationen, Caching und Performance-Optimierung.

## Hauptklasse: DipAnfrage

### Konstruktor

```python
DipAnfrage(
    api_key: str,
    rate_limit_delay: float = 0.1,
    max_retries: int = 3,
    enable_cache: bool = True,
    cache_ttl: int = 3600
)
```

**Parameter:**
- `api_key` (str): Ihr API-Schlüssel für die Bundestag API
- `rate_limit_delay` (float): Verzögerung zwischen Requests in Sekunden (Standard: 0.1)
- `max_retries` (int): Maximale Anzahl Wiederholungsversuche bei Fehlern (Standard: 3)
- `enable_cache` (bool): Caching aktivieren/deaktivieren (Standard: True)
- `cache_ttl` (int): Cache-Gültigkeitsdauer in Sekunden (Standard: 3600)

## Personen-Endpunkte

### get_person()

```python
get_person(anzahl: int = 100, **filters) -> List[dict]
```

Ruft eine Liste von Personen aus der API ab.

**Parameter:**
- `anzahl` (int): Anzahl der abzurufenden Personen (Standard: 100)
- `**filters`: Zusätzliche Filter-Parameter

**Beispiel:**
```python
# Alle Personen abrufen
persons = dip.get_person()

# Personen mit Filter
persons = dip.get_person(anzahl=50, wahlperiode=20)

# Personen nach Datum
persons = dip.get_person(
    anzahl=20,
    datum_start="2024-01-01",
    datum_end="2024-12-31"
)
```

### get_person_id()

```python
get_person_id(id: int) -> Optional[dict]
```

Ruft eine spezifische Person anhand ihrer ID ab.

**Parameter:**
- `id` (int): Die ID der Person

**Beispiel:**
```python
person = dip.get_person_id(id=11000001)
if person:
    print(f"Name: {person['name']}")
```

### get_person_ids()

```python
get_person_ids(ids: List[int]) -> List[dict]
```

Ruft mehrere Personen anhand ihrer IDs ab (Batch-Operation).

**Parameter:**
- `ids` (List[int]): Liste der Personen-IDs

**Beispiel:**
```python
person_ids = [11000001, 11000002, 11000003]
persons = dip.get_person_ids(person_ids)
```

### get_person_by_name()

```python
get_person_by_name(name: str, anzahl: int = 20, **filters) -> List[dict]
```

Sucht Personen nach Namen.

**Parameter:**
- `name` (str): Name oder Teilname der Person
- `anzahl` (int): Anzahl der Ergebnisse (Standard: 20)
- `**filters`: Zusätzliche Filter-Parameter

**Beispiel:**
```python
# Personen mit Namen "Merkel" suchen
persons = dip.get_person_by_name("Merkel", anzahl=10)
```

## Dokumenten-Endpunkte

### get_drucksache()

```python
get_drucksache(anzahl: int = 10, text: bool = True, **filters) -> List[dict]
```

Ruft Drucksachen (Dokumente) aus der API ab.

**Parameter:**
- `anzahl` (int): Anzahl der abzurufenden Dokumente (Standard: 10)
- `text` (bool): Volltext-Dokumente abrufen (Standard: True)
- `**filters`: Zusätzliche Filter-Parameter

**Beispiel:**
```python
# Alle Drucksachen abrufen
documents = dip.get_drucksache()

# Nur Metadaten (ohne Volltext)
documents = dip.get_drucksache(text=False, anzahl=50)

# Dokumente nach Typ
documents = dip.get_drucksache(
    anzahl=20,
    drucksachetyp="Antrag",
    wahlperiode=20
)
```

### get_drucksache_by_id()

```python
get_drucksache_by_id(id: int) -> Optional[dict]
```

Ruft eine spezifische Drucksache anhand ihrer ID ab.

**Parameter:**
- `id` (int): Die ID der Drucksache

**Beispiel:**
```python
document = dip.get_drucksache_by_id(id=11000001)
if document:
    print(f"Titel: {document['titel']}")
```

### get_drucksache_ids()

```python
get_drucksache_ids(ids: List[int], text: bool = True) -> List[dict]
```

Ruft mehrere Drucksachen anhand ihrer IDs ab (Batch-Operation).

**Parameter:**
- `ids` (List[int]): Liste der Dokument-IDs
- `text` (bool): Volltext-Dokumente abrufen (Standard: True)

**Beispiel:**
```python
doc_ids = [11000001, 11000002]
documents = dip.get_drucksache_ids(doc_ids, text=True)
```

### get_documents_by_type()

```python
get_documents_by_type(doc_type: str, anzahl: int = 20, **filters) -> List[dict]
```

Ruft Dokumente nach Typ ab.

**Parameter:**
- `doc_type` (str): Dokumenttyp (z.B. "Antrag", "Beschlussempfehlung")
- `anzahl` (int): Anzahl der Ergebnisse (Standard: 20)
- `**filters`: Zusätzliche Filter-Parameter

**Beispiel:**
```python
# Alle Anträge abrufen
anträge = dip.get_documents_by_type("Antrag", anzahl=50)

# Anträge der aktuellen Wahlperiode
anträge = dip.get_documents_by_type(
    "Antrag",
    anzahl=30,
    wahlperiode=20
)
```

## Aktivitäten-Endpunkte

### get_aktivitaet()

```python
get_aktivitaet(anzahl: int = 100, **filters) -> List[dict]
```

Ruft Aktivitäten aus der API ab.

**Parameter:**
- `anzahl` (int): Anzahl der abzurufenden Aktivitäten (Standard: 100)
- `**filters`: Zusätzliche Filter-Parameter

**Beispiel:**
```python
# Alle Aktivitäten abrufen
activities = dip.get_aktivitaet()

# Aktivitäten nach Datum
activities = dip.get_aktivitaet(
    anzahl=50,
    datum_start="2024-01-01",
    datum_end="2024-12-31"
)
```

### get_aktivitaet_by_id()

```python
get_aktivitaet_by_id(id: int) -> Optional[dict]
```

Ruft eine spezifische Aktivität anhand ihrer ID ab.

**Parameter:**
- `id` (int): Die ID der Aktivität

**Beispiel:**
```python
activity = dip.get_aktivitaet_by_id(id=11000001)
if activity:
    print(f"Aktivität: {activity['titel']}")
```

### get_aktivitaet_ids()

```python
get_aktivitaet_ids(ids: List[int]) -> List[dict]
```

Ruft mehrere Aktivitäten anhand ihrer IDs ab (Batch-Operation).

**Parameter:**
- `ids` (List[int]): Liste der Aktivitäts-IDs

**Beispiel:**
```python
activity_ids = [11000001, 11000002, 11000003]
activities = dip.get_aktivitaet_ids(activity_ids)
```

## Vorgänge-Endpunkte

### get_vorgang()

```python
get_vorgang(anzahl: int = 10, **filters) -> List[dict]
```

Ruft Vorgänge (Procedures) aus der API ab.

**Parameter:**
- `anzahl` (int): Anzahl der abzurufenden Vorgänge (Standard: 10)
- `**filters`: Zusätzliche Filter-Parameter

**Beispiel:**
```python
# Alle Vorgänge abrufen
proceedings = dip.get_vorgang()

# Vorgänge nach Typ
proceedings = dip.get_vorgang(
    anzahl=30,
    vorgangstyp="Gesetzgebung"
)
```

### get_vorgang_by_id()

```python
get_vorgang_by_id(id: int) -> Optional[dict]
```

Ruft einen spezifischen Vorgang anhand seiner ID ab.

**Parameter:**
- `id` (int): Die ID des Vorgangs

**Beispiel:**
```python
proceeding = dip.get_vorgang_by_id(id=11000001)
if proceeding:
    print(f"Vorgang: {proceeding['titel']}")
```

### get_proceedings_by_type()

```python
get_proceedings_by_type(proc_type: str, anzahl: int = 20, **filters) -> List[dict]
```

Ruft Vorgänge nach Typ ab.

**Parameter:**
- `proc_type` (str): Vorgangstyp (z.B. "Gesetzgebung", "Antrag")
- `anzahl` (int): Anzahl der Ergebnisse (Standard: 20)
- `**filters`: Zusätzliche Filter-Parameter

**Beispiel:**
```python
# Gesetzgebungsverfahren abrufen
gesetzgebung = dip.get_proceedings_by_type("Gesetzgebung", anzahl=50)

# Anträge abrufen
anträge = dip.get_proceedings_by_type("Antrag", anzahl=30)
```

## Plenarprotokolle-Endpunkte

### get_plenarprotokoll()

```python
get_plenarprotokoll(anzahl: int = 10, text: bool = True, **filters) -> List[dict]
```

Ruft Plenarprotokolle aus der API ab.

**Parameter:**
- `anzahl` (int): Anzahl der abzurufenden Protokolle (Standard: 10)
- `text` (bool): Volltext-Protokolle abrufen (Standard: True)
- `**filters`: Zusätzliche Filter-Parameter

**Beispiel:**
```python
# Alle Plenarprotokolle abrufen
protocols = dip.get_plenarprotokoll()

# Nur Metadaten (ohne Volltext)
protocols = dip.get_plenarprotokoll(text=False, anzahl=50)

# Protokolle nach Datum
protocols = dip.get_plenarprotokoll(
    anzahl=20,
    datum_start="2024-01-01",
    datum_end="2024-12-31"
)
```

### get_plenarprotokoll_by_id()

```python
get_plenarprotokoll_by_id(id: int) -> Optional[dict]
```

Ruft ein spezifisches Plenarprotokoll anhand seiner ID ab.

**Parameter:**
- `id` (int): Die ID des Plenarprotokolls

**Beispiel:**
```python
protocol = dip.get_plenarprotokoll_by_id(id=11000001)
if protocol:
    print(f"Protokoll: {protocol['titel']}")
```

## Vorgangspositionen-Endpunkte

### get_vorgangsposition()

```python
get_vorgangsposition(anzahl: int = 10, **filters) -> List[Vorgangspositionbezug]
```

Ruft Vorgangspositionen aus der API ab.

**Parameter:**
- `anzahl` (int): Anzahl der abzurufenden Positionen (Standard: 10)
- `**filters`: Zusätzliche Filter-Parameter

**Beispiel:**
```python
# Alle Vorgangspositionen abrufen
positions = dip.get_vorgangsposition()

# Positionen nach Datum
positions = dip.get_vorgangsposition(
    anzahl=30,
    datum_start="2024-01-01",
    datum_end="2024-12-31"
)
```

### get_vorgangsposition_by_id()

```python
get_vorgangsposition_by_id(id: int) -> Optional[dict]
```

Ruft eine spezifische Vorgangsposition anhand ihrer ID ab.

**Parameter:**
- `id` (int): Die ID der Vorgangsposition

**Beispiel:**
```python
position = dip.get_vorgangsposition_by_id(id=11000001)
if position:
    print(f"Position: {position['titel']}")
```

## Convenience-Methoden

### search_documents()

```python
search_documents(query: str, anzahl: int = 20, **filters) -> List[dict]
```

Durchsucht Dokumente nach einem Suchbegriff.

**Parameter:**
- `query` (str): Suchbegriff
- `anzahl` (int): Anzahl der Ergebnisse (Standard: 20)
- `**filters`: Zusätzliche Filter-Parameter

**Beispiel:**
```python
# Nach "Bundeshaushalt" suchen
results = dip.search_documents("Bundeshaushalt", anzahl=10)

# Suche mit zusätzlichen Filtern
results = dip.search_documents(
    "Klimaschutz",
    anzahl=30,
    wahlperiode=20,
    drucksachetyp="Antrag"
)
```

### get_recent_activities()

```python
get_recent_activities(days: int = 7, anzahl: int = 50) -> List[dict]
```

Ruft aktuelle Aktivitäten der letzten Tage ab.

**Parameter:**
- `days` (int): Anzahl der Tage zurück (Standard: 7)
- `anzahl` (int): Anzahl der Ergebnisse (Standard: 50)

**Beispiel:**
```python
# Aktivitäten der letzten 7 Tage
recent = dip.get_recent_activities(days=7, anzahl=100)

# Aktivitäten der letzten 30 Tage
recent = dip.get_recent_activities(days=30, anzahl=200)
```

## Cache-Management

### clear_cache()

```python
clear_cache() -> None
```

Löscht den gesamten Cache.

**Beispiel:**
```python
# Cache leeren
dip.clear_cache()
```

### clear_expired_cache()

```python
clear_expired_cache() -> None
```

Löscht abgelaufene Cache-Einträge.

**Beispiel:**
```python
# Abgelaufene Cache-Einträge löschen
dip.clear_expired_cache()
```

## Filter-Parameter

Alle API-Methoden unterstützen zusätzliche Filter-Parameter:

### Datums-Filter
- `datum_start` (str): Startdatum im Format "YYYY-MM-DD"
- `datum_end` (str): Enddatum im Format "YYYY-MM-DD"
- `aktualisiert_start` (str): Startdatum für Aktualisierungen
- `aktualisiert_end` (str): Enddatum für Aktualisierungen

### Dokument-Filter
- `drucksachetyp` (str): Dokumenttyp (z.B. "Antrag", "Beschlussempfehlung")
- `dokumentnummer` (str): Dokumentnummer
- `titel` (str): Titel-Suche
- `urheber` (str): Urheber des Dokuments

### Vorgangs-Filter
- `vorgangstyp` (str): Vorgangstyp (z.B. "Gesetzgebung", "Antrag")
- `vorgangstyp_notation` (str): Vorgangstyp-Notation

### Personen-Filter
- `person` (str): Personen-Suche
- `wahlperiode` (int): Legislaturperiode

### Allgemeine Filter
- `id` (int): Spezifische ID
- `f_id` (List[int]): Liste von IDs für Batch-Operationen

## Error-Codes

Die API kann folgende HTTP-Status-Codes zurückgeben:

### 200 - OK
Erfolgreiche Anfrage. Die Antwort enthält die angeforderten Daten.

### 400 - Bad Request
Die Anfrage war fehlerhaft. Überprüfen Sie die Parameter.

### 401 - Unauthorized
API-Schlüssel fehlt oder ist ungültig. Registrieren Sie sich für einen API-Schlüssel.

### 403 - Forbidden
Zugriff verweigert. Ihr API-Schlüssel hat möglicherweise nicht die erforderlichen Berechtigungen.

### 404 - Not Found
Die angeforderte Ressource wurde nicht gefunden.

### 429 - Too Many Requests
Rate Limit überschritten. Warten Sie, bevor Sie weitere Anfragen stellen.

### 500 - Internal Server Error
Server-Fehler. Versuchen Sie es später erneut.

## Rate Limiting

Die Bundestag API hat Rate Limits. pydipapi handhabt diese automatisch:

- **Standard-Delay**: 0.1 Sekunden zwischen Requests
- **Retry-Logic**: Automatische Wiederholung bei Fehlern
- **Exponential Backoff**: Verzögerung erhöht sich bei wiederholten Fehlern

## Caching

pydipapi unterstützt automatisches Caching:

- **TTL**: Standard 3600 Sekunden (1 Stunde)
- **Cache-Schlüssel**: Basierend auf URL und Parametern
- **Cache-Speicher**: Lokale JSON-Dateien im `.cache/` Verzeichnis

## Beispiele

### Grundlegende Verwendung
```python
from pydipapi import DipAnfrage

# Client initialisieren
dip = DipAnfrage(api_key='ihr_api_key')

# Personen abrufen
persons = dip.get_person(anzahl=10)

# Dokumente durchsuchen
docs = dip.search_documents("Bundeshaushalt", anzahl=5)

# Batch-Operationen
person_ids = [12345, 67890, 11111]
persons_batch = dip.get_person_ids(person_ids)
```

### Erweiterte Konfiguration
```python
# Client mit erweiterten Optionen
dip = DipAnfrage(
    api_key='ihr_api_key',
    rate_limit_delay=0.2,    # 200ms zwischen Requests
    max_retries=5,           # 5 Wiederholungsversuche
    enable_cache=True,        # Caching aktivieren
    cache_ttl=7200           # 2 Stunden Cache-TTL
)
```

### Filter-Beispiele
```python
# Personen der 20. Wahlperiode
persons = dip.get_person(wahlperiode=20, anzahl=50)

# Dokumente nach Datum
docs = dip.get_drucksache(
    datum_start="2024-01-01",
    datum_end="2024-12-31",
    anzahl=100
)

# Anträge der aktuellen Wahlperiode
anträge = dip.get_documents_by_type(
    "Antrag",
    wahlperiode=20,
    anzahl=30
)
```

### Error-Handling
```python
try:
    persons = dip.get_person(anzahl=10)
    if persons:
        print(f"Gefunden: {len(persons)} Personen")
    else:
        print("Keine Personen gefunden")
except Exception as e:
    print(f"Fehler: {e}")
```

## Migration von 0.x zu 1.0

### Breaking Changes
- Keine Breaking Changes in der aktuellen Version
- Alle bestehenden Methoden bleiben kompatibel

### Neue Features
- Erweiterte Filter-Optionen
- Verbesserte Error-Handling
- Optimierte Caching-Strategien
- Batch-Operationen für alle Endpunkte

### Empfohlene Upgrades
1. Update auf neueste Version: `pip install --upgrade pydipapi`
2. Testen Sie bestehenden Code
3. Nutzen Sie neue Features wie Batch-Operationen
4. Konfigurieren Sie Caching für bessere Performance 