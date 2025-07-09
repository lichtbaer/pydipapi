# API Reference

## DipAnfrage Class

::: pydipapi.api.DipAnfrage

## Filter Parameters Mapping

The following table shows how to map Python parameters to API query parameters:

| Python Parameter | API Query Parameter | Description | Example |
|------------------|-------------------|-------------|---------|
| `wahlperiode` | `f.wahlperiode` | Legislative period | `wahlperiode=20` |
| `datum_start` | `f.datum.start` | Start date | `datum_start="2022-01-01"` |
| `datum_end` | `f.datum.end` | End date | `datum_end="2022-12-31"` |
| `aktualisiert_start` | `f.aktualisiert.start` | Updated since | `aktualisiert_start="2022-01-01T00:00:00"` |
| `aktualisiert_end` | `f.aktualisiert.end` | Updated until | `aktualisiert_end="2022-12-31T23:59:59"` |
| `titel` | `f.titel` | Title filter | `titel="Bundeshaushalt"` |
| `id` | `f.id` | ID filter | `id=12345` |
| `dokumentnummer` | `f.dokumentnummer` | Document number | `dokumentnummer="19/1"` |
| `drucksachetyp` | `f.drucksachetyp` | Document type | `drucksachetyp="Antrag"` |
| `vorgangstyp` | `f.vorgangstyp` | Proceeding type | `vorgangstyp="Gesetzgebung"` |
| `person` | `f.person` | Person filter | `person="Merkel"` |
| `urheber` | `f.urheber` | Author filter | `urheber="CDU/CSU"` |
| `zuordnung` | `f.zuordnung` | Assignment | `zuordnung="BT"` |

## Usage Examples

### Basic Usage
```python
from pydipapi import DipAnfrage

dip = DipAnfrage(api_key='your_api_key')

# Get 10 persons
persons = dip.get_person(anzahl=10)

# Get a specific person by ID
person = dip.get_person_id(id=12345)
```

### Filtered Queries
```python
# Get persons from legislative period 20
persons = dip.get_person(anzahl=10, wahlperiode=20)

# Get documents with specific date range
docs = dip.get_drucksache(
    anzahl=5, 
    datum_start="2022-01-01", 
    datum_end="2022-12-31"
)

# Get activities by person
activities = dip.get_aktivitaet(
    anzahl=20, 
    person="Merkel"
)
```

### Single Item Retrieval
```python
# Get specific items by ID
activity = dip.get_aktivitaet_by_id(id=12345)
document = dip.get_drucksache_by_id(id=67890)
protocol = dip.get_plenarprotokoll_by_id(id=11111)
proceeding = dip.get_vorgang_by_id(id=22222)
```

### Batch Operations
```python
# Get multiple items by IDs
person_ids = [12345, 67890, 11111]
persons = dip.get_person_ids(person_ids)

# Get multiple documents
doc_ids = [12345, 67890]
documents = dip.get_drucksache_ids(doc_ids, text=True)

# Get multiple protocols
protocol_ids = [11111, 22222]
protocols = dip.get_plenarprotokoll_ids(protocol_ids, text=False)
```

### Convenience Methods
```python
# Search for documents
search_results = dip.search_documents("Bundeshaushalt", anzahl=10)

# Get recent activities
recent = dip.get_recent_activities(days=7, anzahl=20)

# Search for persons by name
persons = dip.get_person_by_name("Merkel", anzahl=5)

# Get documents by type
anträge = dip.get_documents_by_type("Antrag", anzahl=10)

# Get proceedings by type
gesetzgebung = dip.get_proceedings_by_type("Gesetzgebung", anzahl=15)
```

### Text vs Metadata
```python
# Get document metadata only
docs_meta = dip.get_drucksache(anzahl=5, text=False)

# Get documents with full text
docs_text = dip.get_drucksache(anzahl=5, text=True)

# Same for protocols
protocols_meta = dip.get_plenarprotokoll(anzahl=5, text=False)
protocols_text = dip.get_plenarprotokoll(anzahl=5, text=True)
```

### Caching and Performance
```python
# Initialize with custom cache settings
dip = DipAnfrage(
    api_key='your_api_key',
    enable_cache=True,
    cache_ttl=7200  # 2 hours
)

# Clear cache when needed
dip.clear_cache()

# Clear only expired cache entries
dip.clear_expired_cache()
```

### Rate Limiting and Retry Logic
```python
# Initialize with custom rate limiting
dip = DipAnfrage(
    api_key='your_api_key',
    rate_limit_delay=0.2,  # 200ms between requests
    max_retries=5
)
``` 