# Verbesserungsvorschläge für PyDipAPI

## Priorisierung
- 🔴 **Hoch**: Wichtige Verbesserungen für Stabilität und Performance
- 🟡 **Mittel**: Nützliche Features und Code-Qualität
- 🟢 **Niedrig**: Nice-to-have Features

---

## 1. Code-Qualität und Architektur

### 🔴 1.1 Exception-Handling konsolidieren

**Problem:**
- Custom Exceptions (`DipApiError`, `DipApiHttpError`, `DipApiConnectionError`) werden definiert, aber nicht konsequent verwendet
- `handle_api_error()` wirft `requests.HTTPError` statt Custom-Exceptions
- Inkonsistente Fehlerbehandlung zwischen sync und async

**Lösung:**
```python
# In error_handler.py - handle_api_error() anpassen
def handle_api_error(response: requests.Response) -> None:
    if response.status_code >= 400:
        try:
            error_data = response.json()
            error_message = error_data.get("message", "Unknown API error")
        except ValueError:
            error_message = f"HTTP {response.status_code}: {response.reason}"
        
        # Custom Exception verwenden statt requests.HTTPError
        raise DipApiHttpError(response.status_code, error_message)
```

**Vorteil:** Konsistente Fehlerbehandlung, bessere Fehlerbehandlung in User-Code

---

### 🟡 1.2 Type-Annotations verbessern

**Problem:**
- Viele Methoden verwenden `Dict[str, Any]` statt spezifischer Typen
- Pydantic-Modelle existieren, werden aber nicht überall verwendet
- `parse_obj_as()` wird nur in `*_typed()` Methoden verwendet

**Lösung:**
```python
# Statt:
def get_person(self, anzahl: int = 100, **filters) -> List[dict]:

# Besser:
def get_person(
    self, 
    anzahl: int = 100, 
    **filters: Any
) -> List[Dict[str, Any]]:
    # ... oder direkt:
    def get_person(self, anzahl: int = 100, **filters: Any) -> List[Person]:
        raw = self._fetch_paginated_data("person", anzahl, **filters)
        return parse_obj_as(List[Person], raw)
```

**Vorteil:** Bessere IDE-Unterstützung, weniger Runtime-Fehler

---

### 🟡 1.3 Parser-Interface standardisieren

**Problem:**
- Parser haben unterschiedliche `parse()` Signaturen
- Keine einheitliche Rückgabe-Struktur
- `parse_batch()` fehlt in einigen Parsern

**Lösung:**
```python
# In base_parser.py
class BaseParser(ABC):
    @abstractmethod
    def parse(self, data: Union[Dict, List[Dict]]) -> Union[Dict, List[Dict]]:
        """Parse data and return structured information."""
        pass
    
    def parse_batch(self, data: List[Dict]) -> List[Dict]:
        """Parse a batch of items."""
        return [self._parse_single(item) for item in data]
    
    @abstractmethod
    def _parse_single(self, data: Dict) -> Dict:
        """Parse a single item."""
        pass
```

**Vorteil:** Konsistente API, einfachere Erweiterung

---

## 2. Performance-Optimierungen

### 🔴 2.1 Connection Pooling für Async-Client

**Problem:**
- `AsyncBaseApiClient` erstellt Session bei jedem Request neu wenn geschlossen
- Keine Connection-Reuse-Optimierung

**Lösung:**
```python
# In async_client.py
class AsyncBaseApiClient:
    def __init__(self, ...):
        # ...
        self._connector: Optional[aiohttp.TCPConnector] = None
        self._connector_limit = 100  # Max connections
    
    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            # Connection Pooling mit Limits
            self._connector = aiohttp.TCPConnector(
                limit=self._connector_limit,
                limit_per_host=30,
                ttl_dns_cache=300,
                force_close=False
            )
            self._session = aiohttp.ClientSession(
                connector=self._connector,
                headers={"Content-Type": "application/json"},
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            )
        return self._session
```

**Vorteil:** Deutlich bessere Performance bei vielen Requests

---

### 🟡 2.2 Batch-Request-Optimierung

**Problem:**
- `get_*_ids()` Methoden machen einen Request pro Batch
- Könnte bei sehr großen Batches (>100 IDs) Probleme verursachen
- Keine Chunking-Strategie

**Lösung:**
```python
def get_person_ids(self, ids: List[int], chunk_size: int = 50) -> List[dict]:
    """
    Retrieve persons by their IDs with automatic chunking.
    
    Args:
        ids: List of person IDs
        chunk_size: Maximum IDs per request (default: 50)
    
    Returns:
        List of person dictionaries
    """
    if not ids:
        return []
    
    all_persons = []
    for chunk in [ids[i:i + chunk_size] for i in range(0, len(ids), chunk_size)]:
        url = self._build_url("person", f_id=chunk)
        data = self._request_json(url)
        if data:
            all_persons.extend(data.get("documents", []))
    
    return all_persons
```

**Vorteil:** Bessere Performance bei großen Batches, weniger Memory-Overhead

---

### 🟡 2.3 Cache-Strategie verbessern

**Problem:**
- Cache speichert komplette Responses (kann groß sein)
- Keine Kompression
- Keine Cache-Invalidierung bei API-Updates

**Lösung:**
```python
# In cache.py
import gzip
import json

class SimpleCache:
    def set(self, url: str, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> None:
        cache_key = self._get_cache_key(url, params)
        cache_file = self.cache_dir / f"{cache_key}.json.gz"  # Komprimiert
        
        cache_data = {"timestamp": time.time(), "data": data}
        
        try:
            temp_file = cache_file.with_suffix(".tmp")
            # Komprimiert speichern
            with gzip.open(temp_file, "wt", encoding="utf-8") as f:
                json.dump(cache_data, f)
            temp_file.replace(cache_file)
        except Exception as e:
            logger.warning(f"Failed to write cache: {e}")
    
    def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        cache_key = self._get_cache_key(url, params)
        cache_file = self.cache_dir / f"{cache_key}.json.gz"
        
        if not cache_file.exists():
            return None
        
        try:
            with gzip.open(cache_file, "rt", encoding="utf-8") as f:
                cached_data = json.load(f)
            # ... TTL-Prüfung ...
            return cached_data.get("data")
        except Exception:
            return None
```

**Vorteil:** Weniger Disk-Space, schnellere I/O bei großen Responses

---

## 3. Features und Funktionalität

### 🟡 3.1 Environment-Variable für API-Key

**Problem:**
- API-Key muss immer explizit übergeben werden
- Keine Unterstützung für Environment-Variablen

**Lösung:**
```python
# In base_client.py
import os

class BaseApiClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://search.dip.bundestag.de/api/v1",
        # ...
    ):
        # API-Key aus Environment oder Parameter
        self.api_key = api_key or os.getenv("DIP_API_KEY") or os.getenv("BUNDESTAG_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "API key is required. Provide it as parameter or set DIP_API_KEY environment variable."
            )
        # ...
```

**Vorteil:** Bessere Developer Experience, sicherer für CI/CD

---

### 🟡 3.2 Request-Timeout konfigurierbar pro Request

**Problem:**
- Timeout ist nur global konfigurierbar
- Manche Requests (z.B. große Dokumente) brauchen länger

**Lösung:**
```python
def get_drucksache(
    self, 
    anzahl: int = 10, 
    text: bool = True, 
    timeout: Optional[float] = None,
    **filters
) -> List[dict]:
    """
    Retrieve documents with optional per-request timeout.
    
    Args:
        timeout: Optional timeout override for this request
    """
    original_timeout = self.timeout
    if timeout is not None:
        self.timeout = timeout
    
    try:
        # ... request logic ...
    finally:
        self.timeout = original_timeout
```

**Vorteil:** Flexibler für verschiedene Request-Typen

---

### 🟢 3.3 Progress-Callbacks für lange Operationen

**Problem:**
- Keine Feedback-Möglichkeit bei langen Batch-Operationen
- User weiß nicht, wie lange Operation noch dauert

**Lösung:**
```python
from typing import Callable, Optional

def get_person(
    self, 
    anzahl: int = 100, 
    progress_callback: Optional[Callable[[int, int], None]] = None,
    **filters
) -> List[dict]:
    """
    Retrieve persons with optional progress callback.
    
    Args:
        progress_callback: Callable(current_count, total_count)
    """
    documents = []
    cursor = ""
    total_fetched = 0
    
    while len(documents) < anzahl:
        # ... fetch logic ...
        total_fetched += len(new_documents)
        
        if progress_callback:
            progress_callback(total_fetched, anzahl)
    
    return documents[:anzahl]
```

**Vorteil:** Bessere UX für lange Operationen

---

### 🟢 3.4 Retry-Strategie konfigurierbar machen

**Problem:**
- Retry-Logik ist hardcoded (exponential backoff)
- Keine Möglichkeit für andere Strategien (linear, custom)

**Lösung:**
```python
from typing import Callable
from enum import Enum

class RetryStrategy(Enum):
    EXPONENTIAL = "exponential"
    LINEAR = "linear"
    FIXED = "fixed"

class BaseApiClient:
    def __init__(
        self,
        # ...
        retry_strategy: RetryStrategy = RetryStrategy.EXPONENTIAL,
        custom_retry_delay: Optional[Callable[[int], float]] = None,
    ):
        self.retry_strategy = retry_strategy
        self.custom_retry_delay = custom_retry_delay
    
    def _calculate_retry_delay(self, attempt: int) -> float:
        if self.custom_retry_delay:
            return self.custom_retry_delay(attempt)
        
        if self.retry_strategy == RetryStrategy.EXPONENTIAL:
            return self.rate_limit_delay * (2 ** attempt)
        elif self.retry_strategy == RetryStrategy.LINEAR:
            return self.rate_limit_delay * attempt
        else:  # FIXED
            return self.rate_limit_delay
```

**Vorteil:** Flexiblere Retry-Strategien für verschiedene Use-Cases

---

## 4. Testing und Qualitätssicherung

### 🔴 4.1 Integration-Tests mit Mock-Server

**Problem:**
- Tests mocken nur einzelne Komponenten
- Keine End-to-End-Tests mit realistischem API-Verhalten

**Lösung:**
```python
# tests/conftest.py
import pytest
from aioresponses import aioresponses

@pytest.fixture
def mock_api_server():
    """Mock API server for integration tests."""
    with aioresponses() as m:
        # Mock verschiedene Endpunkte
        m.get(
            "https://search.dip.bundestag.de/api/v1/person?apikey=test",
            payload={"documents": [{"id": "1", "name": "Test"}]},
            status=200
        )
        yield m

# tests/test_integration.py
@pytest.mark.integration
async def test_full_workflow(mock_api_server):
    """Test complete workflow with mocked API."""
    async with AsyncDipAnfrage(api_key="test") as api:
        persons = await api.get_person(anzahl=10)
        assert len(persons) > 0
```

**Vorteil:** Realistischere Tests, bessere Fehlererkennung

---

### 🟡 4.2 Property-based Testing

**Problem:**
- Tests decken nur bekannte Fälle ab
- Edge-Cases werden möglicherweise übersehen

**Lösung:**
```python
# tests/test_property.py
from hypothesis import given, strategies as st

@given(
    anzahl=st.integers(min_value=1, max_value=1000),
    wahlperiode=st.integers(min_value=1, max_value=20)
)
def test_get_person_property_based(anzahl, wahlperiode):
    """Property-based test for get_person."""
    # Mock setup...
    result = api.get_person(anzahl=anzahl, wahlperiode=wahlperiode)
    
    # Properties die immer gelten sollten:
    assert isinstance(result, list)
    assert len(result) <= anzahl
    # ...
```

**Vorteil:** Findet unerwartete Edge-Cases

---

## 5. Dokumentation und Developer Experience

### 🟡 5.1 API-Response-Beispiele in Docstrings

**Problem:**
- Docstrings beschreiben Parameter, aber nicht Response-Struktur
- User muss API-Dokumentation konsultieren

**Lösung:**
```python
def get_person(self, anzahl: int = 100, **filters) -> List[dict]:
    """
    Retrieve a list of persons from the API.
    
    Args:
        anzahl: Number of persons to retrieve.
        **filters: Filter parameters (e.g., wahlperiode=20).
    
    Returns:
        List of person dictionaries with structure:
        [
            {
                "id": "12345",
                "vorname": "Max",
                "nachname": "Mustermann",
                "fraktion": "CDU/CSU",
                "wahlkreis": "Berlin-Mitte",
                ...
            },
            ...
        ]
    
    Example:
        >>> api = DipAnfrage(api_key="your_key")
        >>> persons = api.get_person(anzahl=10, wahlperiode=20)
        >>> print(persons[0]["vorname"])
        'Max'
    """
```

**Vorteil:** Bessere IDE-Unterstützung, weniger Konsultation der API-Docs

---

### 🟡 5.2 Type-Stubs für bessere IDE-Unterstützung

**Problem:**
- Pydantic-Modelle sind gut, aber IDE zeigt nicht immer alle Felder
- Keine `.pyi` Stub-Dateien

**Lösung:**
```python
# pydipapi/type.pyi (optional, für bessere IDE-Unterstützung)
from typing import TypedDict, Optional, List
from datetime import datetime

class Person(TypedDict):
    id: str
    vorname: str
    nachname: str
    fraktion: Optional[str]
    wahlkreis: Optional[str]
    # ...
```

**Vorteil:** Bessere Autocomplete, weniger Runtime-Fehler

---

### 🟢 5.3 Interactive Examples mit Rich

**Problem:**
- Beispiele sind textbasiert
- Keine visuellen Hilfen für komplexe Daten

**Lösung:**
```python
# examples/interactive_example.py
from rich.console import Console
from rich.table import Table
from rich import print as rprint

console = Console()

def display_persons_table(persons):
    """Display persons in a nice table."""
    table = Table(title="Bundestag Members")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Party", style="green")
    
    for person in persons[:10]:
        table.add_row(
            str(person.get("id", "")),
            f"{person.get('vorname', '')} {person.get('nachname', '')}",
            person.get("fraktion", "Unknown")
        )
    
    console.print(table)
```

**Vorteil:** Bessere Visualisierung für Tutorials und Demos

---

## 6. Sicherheit und Robustheit

### 🔴 6.1 API-Key-Sanitization in Logs

**Problem:**
- API-Key könnte in Logs erscheinen (z.B. in URLs)
- `redact_query_params()` existiert, aber wird nicht überall verwendet

**Lösung:**
```python
# In util/__init__.py - sicherstellen dass überall verwendet
from .util import redact_query_params

# In base_client.py - alle Log-Statements prüfen
logger.debug(f"Making request to: {redact_query_params(url)}")

# Zusätzlich: URL-Parsing für sicherere Redaction
def redact_query_params(url: str) -> str:
    """Redact sensitive parameters from URL."""
    from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
    
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    
    # Redact sensitive keys
    sensitive_keys = ["apikey", "api_key", "key", "token", "auth"]
    for key in sensitive_keys:
        if key.lower() in params:
            params[key] = ["***REDACTED***"]
    
    new_query = urlencode(params, doseq=True)
    new_url = urlunparse(parsed._replace(query=new_query))
    return new_url
```

**Vorteil:** Sicherheit, keine API-Keys in Logs

---

### 🟡 6.2 Input-Validierung

**Problem:**
- Keine Validierung von `anzahl`, `ids`, etc.
- Negative Werte oder zu große Werte könnten Probleme verursachen

**Lösung:**
```python
from pydantic import validator

def get_person(self, anzahl: int = 100, **filters) -> List[dict]:
    """
    Retrieve persons with input validation.
    """
    # Validierung
    if anzahl < 1:
        raise ValueError("anzahl must be >= 1")
    if anzahl > 10000:
        raise ValueError("anzahl must be <= 10000 (API limit)")
    
    # ... rest of method
```

**Vorteil:** Frühe Fehlererkennung, bessere Fehlermeldungen

---

### 🟡 6.3 Rate-Limiting-Erkennung verbessern

**Problem:**
- Rate-Limiting wird nur bei 429 erkannt
- Keine proaktive Rate-Limiting-Verhinderung

**Lösung:**
```python
class BaseApiClient:
    def __init__(self, ...):
        # ...
        self._request_times: List[float] = []  # Track request times
        self._rate_limit_window = 60.0  # 60 seconds window
    
    def _check_rate_limit(self) -> None:
        """Check if we're approaching rate limit."""
        now = time.time()
        # Remove old requests outside window
        self._request_times = [t for t in self._request_times if now - t < self._rate_limit_window]
        
        # If too many requests in window, wait
        if len(self._request_times) > 100:  # Example limit
            sleep_time = self._rate_limit_window - (now - self._request_times[0])
            if sleep_time > 0:
                logger.warning(f"Rate limit approaching, sleeping {sleep_time:.2f}s")
                time.sleep(sleep_time)
        
        self._request_times.append(now)
```

**Vorteil:** Proaktive Rate-Limiting-Vermeidung

---

## 7. Monitoring und Observability

### 🟡 7.1 Metrics-Sammlung

**Problem:**
- Keine Metriken über API-Usage
- Schwer zu debuggen Performance-Probleme

**Lösung:**
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class RequestMetrics:
    """Metrics for API requests."""
    endpoint: str
    duration: float
    status_code: int
    cache_hit: bool
    retry_count: int

class BaseApiClient:
    def __init__(self, ...):
        # ...
        self._metrics: List[RequestMetrics] = []
        self._enable_metrics = False
    
    def get_metrics(self) -> List[RequestMetrics]:
        """Get collected metrics."""
        return self._metrics.copy()
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary statistics."""
        if not self._metrics:
            return {}
        
        return {
            "total_requests": len(self._metrics),
            "cache_hit_rate": sum(1 for m in self._metrics if m.cache_hit) / len(self._metrics),
            "avg_duration": sum(m.duration for m in self._metrics) / len(self._metrics),
            "error_rate": sum(1 for m in self._metrics if m.status_code >= 400) / len(self._metrics),
        }
```

**Vorteil:** Besseres Monitoring, Performance-Analyse

---

### 🟢 7.2 OpenTelemetry-Integration

**Problem:**
- Keine Tracing-Möglichkeit für komplexe Workflows
- Schwer zu debuggen in Production

**Lösung:**
```python
# Optional dependency
try:
    from opentelemetry import trace
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False

class BaseApiClient:
    def __init__(self, enable_tracing: bool = False, ...):
        # ...
        if enable_tracing and OTEL_AVAILABLE:
            self.tracer = trace.get_tracer(__name__)
            RequestsInstrumentor().instrument()
        else:
            self.tracer = None
    
    def _make_request(self, url: str, ...):
        if self.tracer:
            with self.tracer.start_as_current_span("dip_api_request") as span:
                span.set_attribute("http.url", redact_query_params(url))
                # ... request logic ...
                span.set_attribute("http.status_code", response.status_code)
        else:
            # ... normal request logic ...
```

**Vorteil:** Production-Debugging, Performance-Analyse

---

## 8. Code-Organisation

### 🟡 8.1 Dependency-Injection für bessere Testbarkeit

**Problem:**
- Cache, Error-Handler sind direkt instanziiert
- Schwer zu mocken in Tests

**Lösung:**
```python
class BaseApiClient:
    def __init__(
        self,
        api_key: str,
        cache: Optional[SimpleCache] = None,
        error_handler: Optional[Callable] = None,
        # ...
    ):
        # ...
        self.cache = cache or (SimpleCache(ttl=cache_ttl) if enable_cache else None)
        self.error_handler = error_handler or handle_api_error
```

**Vorteil:** Bessere Testbarkeit, flexiblere Konfiguration

---

### 🟢 8.2 Plugin-System für Parser

**Problem:**
- Neue Parser müssen direkt in Code eingefügt werden
- Keine Möglichkeit für User-defined Parser

**Lösung:**
```python
# pydipapi/parsers/registry.py
class ParserRegistry:
    _parsers: Dict[str, Type[BaseParser]] = {}
    
    @classmethod
    def register(cls, name: str, parser_class: Type[BaseParser]):
        """Register a parser."""
        cls._parsers[name] = parser_class
    
    @classmethod
    def get(cls, name: str) -> Optional[BaseParser]:
        """Get a parser instance."""
        if name in cls._parsers:
            return cls._parsers[name]()
        return None

# User kann eigene Parser registrieren
from pydipapi.parsers import ParserRegistry, BaseParser

class MyCustomParser(BaseParser):
    # ...

ParserRegistry.register("custom", MyCustomParser)
```

**Vorteil:** Erweiterbarkeit, Community-Contributions

---

## Zusammenfassung der Prioritäten

### Sofort umsetzbar (🔴):
1. Exception-Handling konsolidieren
2. Connection Pooling für Async
3. API-Key-Sanitization verbessern
4. Integration-Tests mit Mock-Server

### Kurzfristig (🟡):
1. Type-Annotations verbessern
2. Environment-Variable für API-Key
3. Batch-Request-Optimierung
4. Cache-Kompression
5. Input-Validierung
6. Metrics-Sammlung

### Langfristig (🟢):
1. Progress-Callbacks
2. Retry-Strategien konfigurierbar
3. Rich-Integration für Examples
4. OpenTelemetry-Integration
5. Plugin-System

---

## Implementierungsreihenfolge

1. **Woche 1-2**: Exception-Handling, API-Key-Sanitization, Input-Validierung
2. **Woche 3-4**: Connection Pooling, Batch-Optimierung, Cache-Kompression
3. **Woche 5-6**: Type-Annotations, Environment-Variables, Metrics
4. **Woche 7+**: Nice-to-have Features (Progress-Callbacks, Rich, etc.)

Diese Verbesserungen würden PyDipAPI von einem guten zu einem exzellenten API-Client machen! 🚀
