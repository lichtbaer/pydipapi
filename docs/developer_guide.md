# Entwickler-Guide

Dieser Guide richtet sich an Entwickler, die pydipapi erweitern oder in ihre Projekte integrieren möchten.

## Installation für Entwicklung

```bash
# Repository klonen
git clone https://github.com/lichtbaer/pydipapi.git
cd pydipapi

# Virtuelle Umgebung erstellen
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows

# Entwicklungsumgebung installieren
pip install -e .
pip install -r requirements-dev.txt
```

## Projektstruktur

```
pydipapi/
├── pydipapi/
│   ├── __init__.py
│   ├── api.py              # Haupt-API-Klasse
│   ├── client/
│   │   └── base_client.py  # Basis-Client mit Caching/Rate-Limiting
│   ├── util/
│   │   ├── cache.py        # Caching-Implementierung
│   │   └── error_handler.py # Fehlerbehandlung
│   └── type.py             # Pydantic-Modelle
├── tests/
│   └── test_api.py         # Unit-Tests
├── docs/                   # Dokumentation
├── notebooks/              # Jupyter-Notebooks
├── examples/               # Beispiel-Skripte
└── requirements-dev.txt    # Entwicklungsabhängigkeiten
```

## Architektur

### Basis-Client (`BaseApiClient`)

Der `BaseApiClient` bietet grundlegende Funktionalitäten:

- **Rate Limiting** - Konfigurierbare Verzögerungen zwischen Requests
- **Retry-Logik** - Automatische Wiederholung bei Fehlern
- **Caching** - File-basiertes Caching mit TTL
- **Error Handling** - Einheitliche Fehlerbehandlung

### Haupt-API (`DipAnfrage`)

Die `DipAnfrage`-Klasse erbt von `BaseApiClient` und bietet:

- **Vollständige API-Abdeckung** - Alle Bundestag-API-Endpunkte
- **Batch-Operationen** - Mehrere IDs in einem Aufruf
- **Convenience-Methoden** - Einfache Abfragen für häufige Anwendungsfälle
- **Flexible Filterung** - Umfassende Such- und Filteroptionen

## Erweiterte Konfiguration

### Caching konfigurieren

```python
from pydipapi import DipAnfrage

# Caching aktivieren
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
# Konservatives Rate Limiting
dip_conservative = DipAnfrage(
    api_key='ihr_api_key',
    rate_limit_delay=0.5,  # 500ms zwischen Requests
    max_retries=5
)

# Aggressives Rate Limiting
dip_aggressive = DipAnfrage(
    api_key='ihr_api_key',
    rate_limit_delay=0.05,  # 50ms zwischen Requests
    max_retries=2
)
```

### Custom Cache-Verzeichnis

```python
import os
from pydipapi.util.cache import SimpleCache

# Custom Cache konfigurieren
custom_cache = SimpleCache(
    cache_dir="/tmp/pydipapi_cache",
    ttl=1800  # 30 Minuten
)

# Cache in Client verwenden
dip = DipAnfrage(
    api_key='ihr_api_key',
    enable_cache=True,
    cache_ttl=1800
)
```

## Batch-Operationen

### Mehrere IDs auf einmal abrufen

```python
# Personen-Batch
person_ids = [12345, 67890, 11111, 22222, 33333]
persons = dip.get_person_ids(person_ids)

# Dokumente-Batch (mit Text)
doc_ids = [12345, 67890, 11111]
docs_with_text = dip.get_drucksache_ids(doc_ids, text=True)

# Protokolle-Batch (nur Metadaten)
protocol_ids = [11111, 22222, 33333]
protocols_meta = dip.get_plenarprotokoll_ids(protocol_ids, text=False)
```

### Performance-Vergleich

```python
import time

# Einzelne Operationen
start_time = time.time()
for person_id in person_ids[:5]:
    person = dip.get_person_id(person_id)
single_time = time.time() - start_time

# Batch-Operation
start_time = time.time()
persons_batch = dip.get_person_ids(person_ids[:5])
batch_time = time.time() - start_time

print(f"Einzelne Operationen: {single_time:.2f}s")
print(f"Batch-Operation: {batch_time:.2f}s")
print(f"Performance-Verbesserung: {single_time/batch_time:.1f}x")
```

## Convenience-Methoden

### Dokumentensuche

```python
# Volltext-Suche
climate_docs = dip.search_documents("Klimaschutz", anzahl=10)
budget_docs = dip.search_documents("Bundeshaushalt", anzahl=10)

# Mit zusätzlichen Filtern
recent_climate_docs = dip.search_documents(
    "Klimaschutz", 
    anzahl=10,
    datum_start="2024-01-01",
    wahlperiode=20
)
```

### Aktuelle Aktivitäten

```python
# Aktivitäten der letzten 7 Tage
recent_7_days = dip.get_recent_activities(days=7, anzahl=20)

# Aktivitäten der letzten 30 Tage
recent_30_days = dip.get_recent_activities(days=30, anzahl=50)
```

### Personen-Suche

```python
# Nach Namen suchen
merkel = dip.get_person_by_name("Merkel", anzahl=5)
scholz = dip.get_person_by_name("Scholz", anzahl=5)
baerbock = dip.get_person_by_name("Baerbock", anzahl=5)
```

### Typ-basierte Filterung

```python
# Dokumente nach Typ
anträge = dip.get_documents_by_type("Antrag", anzahl=10)
gesetzentwürfe = dip.get_documents_by_type("Gesetzentwurf", anzahl=10)

# Vorgänge nach Typ
gesetzgebung = dip.get_proceedings_by_type("Gesetzgebung", anzahl=10)
berichte = dip.get_proceedings_by_type("Bericht", anzahl=10)
```

## Debugging und Fehlerbehebung

### Debug-Logging aktivieren

Für detaillierte Informationen über API-Requests und Responses:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from pydipapi import DipAnfrage
dip = DipAnfrage(api_key)
```

### Response-Handling verstehen

Die Bibliothek verwendet ein zweistufiges Response-Handling:

1. **BaseApiClient** gibt `requests.Response` Objekte zurück
2. **DipAnfrage** parsiert diese zu `dict` Objekten

```python
# In DipAnfrage._make_request()
def _make_request(self, url: str) -> Optional[dict]:
    response = super()._make_request(url)  # requests.Response
    
    if response is None:
        return None
        
    try:
        data = response.json()  # dict
        return data
    except Exception as e:
        logger.error(f"Failed to parse JSON response: {e}")
        return None
```

### Pagination-Logic

Die Pagination behandelt verschiedene Response-Formate:

```python
# In _fetch_paginated_data()
response = self._make_request(url)

# Handle both Response objects and dict data
if hasattr(response, 'json'):
    data = response.json()  # requests.Response
else:
    data = response  # dict

new_documents = data.get('documents', []) if isinstance(data, dict) else []
```

### Error-Handling verbessern

Die Bibliothek bietet spezifische Fehlermeldungen für häufige Probleme:

```python
# In base_client.py
if response.status_code == 401:
    logger.error("Authentication failed. Please check your API key.")
    logger.error("You can get an API key from: https://dip.bundestag.de/über-dip/hilfe/api")
elif response.status_code == 403:
    logger.error("Access forbidden. Your API key may not have the required permissions.")
elif response.status_code == 429:
    logger.error("Rate limit exceeded. Please wait before making more requests.")
```

### API-Key-Validierung

Implementieren Sie Validierung für ungültige API-Keys:

```python
def validate_api_key(api_key: str) -> bool:
    """Validate API key format and detect placeholder values."""
    if not api_key:
        return False
    
    # Check for placeholder values
    placeholder_keys = ['your-api-key-here', 'test-key', 'demo-key']
    if api_key in placeholder_keys:
        return False
    
    # Basic format validation
    if len(api_key) < 10:
        return False
    
    return True
```

### Cache-Probleme beheben

Bei Cache-Serialisierungsproblemen:

```python
# Cache deaktivieren für Debugging
dip = DipAnfrage(
    api_key='ihr_api_key',
    enable_cache=False
)

# Oder Cache-Verzeichnis ändern
import tempfile
temp_cache_dir = tempfile.mkdtemp()
```

## Unit-Tests schreiben

### Beispiel-Test für API-Methoden

```python
import pytest
from unittest.mock import Mock, patch
from pydipapi import DipAnfrage

class TestDipAnfrage:
    def setup_method(self):
        self.dip = DipAnfrage("test-api-key")
    
    def test_get_person_success(self):
        # Mock response data
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "documents": [{"id": 1, "name": "Test Person"}],
            "numFound": 1
        }
        
        with patch.object(self.dip, '_make_request', return_value=mock_response):
            persons = self.dip.get_person(anzahl=1)
            assert len(persons) == 1
            assert persons[0]["name"] == "Test Person"
    
    def test_get_person_api_error(self):
        # Mock API error
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = '{"error": "Unauthorized"}'
        
        with patch.object(self.dip, '_make_request', return_value=mock_response):
            persons = self.dip.get_person(anzahl=1)
            assert persons == []  # Should return empty list on error
```

### Integration-Tests

```python
def test_real_api_integration():
    """Test with real API (requires valid API key)."""
    import os
    
    api_key = os.getenv('DIP_API_KEY')
    if not api_key:
        pytest.skip("No API key available")
    
    dip = DipAnfrage(api_key)
    
    # Test basic functionality
    persons = dip.get_person(anzahl=1)
    assert len(persons) >= 0  # Should not raise exception
    
    # Test search functionality
    docs = dip.search_documents("Bundestag", anzahl=1)
    assert len(docs) >= 0  # Should not raise exception
```

## Performance-Optimierung

### Caching-Strategien

```python
# Langzeit-Caching für selten ändernde Daten
persons_cache = DipAnfrage(
    api_key='ihr_api_key',
    enable_cache=True,
    cache_ttl=86400  # 24 Stunden
)

# Kurzzeit-Caching für aktuelle Daten
activities_cache = DipAnfrage(
    api_key='ihr_api_key',
    enable_cache=True,
    cache_ttl=300  # 5 Minuten
)
```

### Rate Limiting optimieren

```python
# Für Bulk-Operationen
bulk_client = DipAnfrage(
    api_key='ihr_api_key',
    rate_limit_delay=0.1,  # 100ms
    max_retries=3
)

# Für Echtzeit-Anwendungen
realtime_client = DipAnfrage(
    api_key='ihr_api_key',
    rate_limit_delay=0.01,  # 10ms
    max_retries=1
)
```

### Batch-Operationen optimieren

```python
# Effiziente Batch-Größen
optimal_batch_size = 50  # API-spezifisch

def fetch_large_dataset(total_count: int, batch_size: int = 50):
    """Fetch large datasets efficiently."""
    all_data = []
    
    for offset in range(0, total_count, batch_size):
        batch = dip.get_person(anzahl=min(batch_size, total_count - offset))
        all_data.extend(batch)
        
        if len(batch) < batch_size:
            break
    
    return all_data
```

## Erweiterte Funktionen

### Custom Error Handler

```python
from pydipapi.util.error_handler import handle_api_error

def custom_error_handler(response):
    """Custom error handling for specific use cases."""
    if response.status_code == 429:
        # Implement custom rate limiting logic
        time.sleep(60)  # Wait 1 minute
        return True  # Retry
    
    # Use default error handling
    handle_api_error(response)
    return False
```

### Custom Cache Implementation

```python
from pydipapi.util.cache import SimpleCache

class RedisCache(SimpleCache):
    """Redis-based cache implementation."""
    
    def __init__(self, redis_client, ttl: int = 3600):
        self.redis = redis_client
        self.ttl = ttl
    
    def get(self, url: str, params=None):
        key = self._get_cache_key(url, params)
        data = self.redis.get(key)
        return json.loads(data) if data else None
    
    def set(self, url: str, data: dict, params=None):
        key = self._get_cache_key(url, params)
        self.redis.setex(key, self.ttl, json.dumps(data))
```

Diese Erweiterungen ermöglichen es Entwicklern, pydipapi an ihre spezifischen Anforderungen anzupassen und die Bibliothek in komplexere Anwendungen zu integrieren. 