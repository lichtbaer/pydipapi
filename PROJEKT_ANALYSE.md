# Projektanalyse: PyDipAPI

## 1. Projektziel

**PyDipAPI** ist ein moderner Python-Client für die **Deutsche Bundestag API (DIP API)**. Das Projekt ermöglicht einfachen Zugriff auf parlamentarische Daten des deutschen Bundestages, einschließlich:

- **Abgeordnete** (Personen/Mitglieder des Bundestages)
- **Dokumente** (Drucksachen, Gesetzesentwürfe, Anträge)
- **Plenarprotokolle** (Sitzungsprotokolle mit Text)
- **Aktivitäten** (Abstimmungen, Sitzungen, Verfahren)
- **Vorgänge** (Gesetzgebungsverfahren)
- **Vorgangspositionen** (spezifische Positionen innerhalb von Verfahren)

### Hauptziele:
1. **Einfacher Zugriff** auf Bundestag-Daten für Entwickler, Forscher und Journalisten
2. **Performance-Optimierung** durch asynchrone Operationen und intelligentes Caching
3. **Datenstrukturierung** durch spezialisierte Content-Parser
4. **Type-Safety** durch Pydantic-Modelle für bessere IDE-Unterstützung
5. **Robustheit** durch Fehlerbehandlung, Retry-Logik und Rate-Limiting

## 2. Umsetzung

### 2.1 Technologie-Stack

**Core Dependencies:**
- `requests >= 2.25.0` - Synchroner HTTP-Client
- `aiohttp >= 3.9.0` - Asynchroner HTTP-Client
- `pydantic >= 1.8.0` - Datenvalidierung und Type-Safety

**Development Tools:**
- `pytest` - Testing Framework
- `ruff` - Linting und Code-Formatierung
- `bandit` - Security-Analyse
- `mypy` - Type-Checking
- `mkdocs` - Dokumentations-Generator

**Python-Version:** 3.10+

### 2.2 Hauptfunktionalitäten

#### 2.2.1 Synchroner API-Client (`DipAnfrage`)
- Vollständige Abdeckung aller DIP-API-Endpunkte
- Batch-Operationen für mehrere IDs
- Flexible Filterung und Suche
- Convenience-Methoden für häufige Anwendungsfälle

#### 2.2.2 Asynchroner API-Client (`AsyncDipAnfrage`)
- Parallele API-Anfragen für bessere Performance
- Connection-Pooling
- Context-Manager-Support für automatisches Resource-Management

#### 2.2.3 Content-Parser
- **ProtocolParser**: Extrahiert Redner, Themen und Interventionen aus Plenarprotokollen
- **DocumentParser**: Parst Dokument-Metadaten, Autoren und Inhaltszusammenfassungen
- **PersonParser**: Extrahiert Abgeordneten-Informationen, Parteien und Wahlkreise
- **ActivityParser**: Parst Abstimmungsergebnisse, Teilnehmer und verknüpfte Dokumente

#### 2.2.4 Caching-System
- File-basiertes Caching mit konfigurierbarer TTL
- SHA256-basierte Cache-Keys für Sicherheit
- Atomare Schreiboperationen
- Automatische Bereinigung abgelaufener Einträge

#### 2.2.5 Fehlerbehandlung
- Automatische Retry-Logik mit exponentieller Backoff
- Rate-Limiting-Erkennung und -Behandlung
- Detailliertes Logging für Debugging
- Spezifische Fehlermeldungen für häufige Probleme (401, 403, 429)

## 3. Architektur

### 3.1 Schichtarchitektur

```
┌─────────────────────────────────────────┐
│   Public API Layer                      │
│   (DipAnfrage, AsyncDipAnfrage)        │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│   Base Client Layer                     │
│   (BaseApiClient, AsyncBaseApiClient)   │
│   - Rate Limiting                       │
│   - Retry Logic                         │
│   - Caching                             │
│   - Error Handling                      │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│   Utility Layer                         │
│   - SimpleCache                         │
│   - Error Handler                       │
│   - Pagination Helpers                  │
└─────────────────────────────────────────┘
```

### 3.2 Modulare Struktur

```
pydipapi/
├── __init__.py              # Public API Export
├── api.py                   # Synchroner Client (DipAnfrage)
├── async_api.py             # Asynchroner Client (AsyncDipAnfrage)
├── type.py                  # Pydantic-Modelle für Type-Safety
│
├── client/                  # Client-Infrastruktur
│   ├── base_client.py       # Basis-Client (synchron)
│   ├── async_client.py      # Basis-Client (asynchron)
│   └── pagination.py        # Pagination-Logik (sync & async)
│
├── parsers/                 # Content-Parser
│   ├── base_parser.py       # Basis-Parser mit gemeinsamen Methoden
│   ├── protocol_parser.py   # Plenarprotokoll-Parser
│   ├── document_parser.py   # Dokument-Parser
│   ├── person_parser.py     # Abgeordneten-Parser
│   └── activity_parser.py   # Aktivitäten-Parser
│
└── util/                    # Utilities
    ├── cache.py             # Caching-Implementierung
    └── error_handler.py      # Fehlerbehandlung
```

### 3.3 Design-Patterns

#### 3.3.1 Template Method Pattern
- `BaseApiClient` und `AsyncBaseApiClient` definieren das Template für API-Requests
- Konkrete Implementierungen (`DipAnfrage`, `AsyncDipAnfrage`) erweitern die Basis-Funktionalität

#### 3.3.2 Strategy Pattern
- Verschiedene Parser-Strategien für unterschiedliche Content-Typen
- Alle Parser erben von `BaseParser` und implementieren `_parse_single()`

#### 3.3.3 Factory Pattern (implizit)
- `SimpleCache` erstellt und verwaltet Cache-Dateien
- Parser werden durch Factory-Methoden erstellt

#### 3.3.4 Dependency Injection
- Cache, Error-Handler und Pagination-Helpers werden als Abhängigkeiten injiziert
- Ermöglicht einfaches Testen und Mocking

### 3.4 Datenfluss

#### Synchroner Request-Flow:
```
User Code
  ↓
DipAnfrage.get_person()
  ↓
_fetch_paginated_data()
  ↓
fetch_paginated_sync()
  ↓
_build_url() → _request_json()
  ↓
BaseApiClient._make_request()
  ↓
[Cache Check] → [HTTP Request] → [Error Handling] → [Retry Logic]
  ↓
Response → [Cache Write] → JSON Parsing → Return
```

#### Asynchroner Request-Flow:
```
User Code
  ↓
AsyncDipAnfrage.get_person()
  ↓
_fetch_paginated_data()
  ↓
fetch_paginated_async()
  ↓
_build_url() → _request_json()
  ↓
AsyncBaseApiClient._make_request()
  ↓
[Cache Check] → [aiohttp Request] → [Error Handling] → [Retry Logic]
  ↓
Response → [Cache Write] → JSON Parsing → Return
```

### 3.5 Caching-Architektur

**Cache-Key-Generierung:**
- URL + Query-Parameter werden zu JSON serialisiert
- SHA256-Hash wird als Cache-Key verwendet
- Dateiname: `{hash}.json`

**Cache-Struktur:**
```json
{
  "timestamp": 1234567890.123,
  "data": {
    "json": {...},  // Für async
    "content": b"...",  // Für sync (legacy)
    "headers": {...}
  }
}
```

**TTL-Mechanismus:**
- Jeder Cache-Eintrag hat einen Timestamp
- Bei Abfrage wird TTL geprüft
- Abgelaufene Einträge werden automatisch gelöscht

### 3.6 Pagination-Mechanismus

**Cursor-basierte Pagination:**
- API verwendet Cursor für Pagination
- `fetch_paginated_sync/async` iteriert über Seiten
- Sammelt Dokumente bis zur gewünschten Anzahl erreicht ist
- Unterstützt beide Client-Typen (sync/async)

### 3.7 Error-Handling-Strategie

**Retry-Logik:**
- Exponential Backoff: `delay = rate_limit_delay * attempt`
- Max. Retries konfigurierbar (Standard: 3)
- Spezielle Behandlung für Rate-Limiting (429)

**Fehlerkategorien:**
- **401 Unauthorized**: API-Key-Problem
- **403 Forbidden**: Berechtigungsproblem
- **429 Too Many Requests**: Rate-Limiting
- **5xx Server Errors**: Retry-würdig
- **4xx Client Errors**: Normalerweise nicht retry-würdig

## 4. Code-Qualität und Best Practices

### 4.1 Type-Safety
- Vollständige Type-Annotations mit `typing`
- Pydantic-Modelle für Datenvalidierung
- MyPy-Konfiguration für statische Type-Checks
- `py.typed` Marker für PEP 561 Compliance

### 4.2 Code-Formatierung
- Ruff für Linting und Formatierung
- Konsistente Code-Style (PEP 8)
- Line-Length: 88 Zeichen

### 4.3 Testing
- Unit-Tests mit pytest
- Integration-Tests
- Coverage-Tracking
- Separate Test-Marker für langsame/Integration-Tests

### 4.4 Dokumentation
- Umfassende Docstrings
- Jupyter-Notebooks für Tutorials
- MkDocs-basierte Dokumentation
- API-Reference automatisch generiert

### 4.5 Security
- Bandit für Security-Scanning
- SHA256 statt MD5 für Cache-Keys
- API-Key-Redaktion in Logs
- Input-Validierung durch Pydantic

## 5. CI/CD-Pipeline

### 5.1 GitHub Actions Workflows

**CI Pipeline (`ci.yml`):**
- Multi-Python-Version Testing (3.10, 3.11, 3.12)
- Cross-Platform Testing (Ubuntu, Windows, macOS)
- Code-Quality-Checks (Ruff, Bandit, MyPy)
- Security-Scanning
- Dokumentations-Build

**Release Pipeline (`release.yml`):**
- Package-Building und -Validierung
- Automatisches PyPI-Publishing bei Version-Tags
- GitHub-Releases mit Changelog
- Dokumentations-Deployment

**Dependabot (`dependabot.yml`):**
- Wöchentliche Dependency-Updates
- Auto-Merge für Patch/Minor-Updates
- Security-Vulnerability-Alerts

## 6. Stärken der Architektur

1. **Modularität**: Klare Trennung von Concerns (Client, Parser, Utilities)
2. **Erweiterbarkeit**: Einfach neue Parser oder Endpunkte hinzufügen
3. **Performance**: Async-Support und intelligentes Caching
4. **Robustheit**: Umfassende Fehlerbehandlung und Retry-Logik
5. **Type-Safety**: Pydantic-Modelle für bessere Entwicklererfahrung
6. **Testbarkeit**: Dependency Injection ermöglicht einfaches Mocking
7. **Dokumentation**: Umfassende Docs und Beispiele

## 7. Verbesserungspotenziale

1. **Persistenter Cache**: Aktuell nur File-basiert, könnte Redis/Memcached unterstützen
2. **Streaming**: Für große Datensätze könnte Streaming-API nützlich sein
3. **Webhooks**: Unterstützung für Event-basierte Updates
4. **GraphQL-Interface**: Alternative zu REST für komplexe Queries
5. **Offline-Mode**: Lokale Datenbank für Offline-Zugriff
6. **Rate-Limiting-Strategien**: Adaptive Rate-Limiting basierend auf API-Response

## 8. Zusammenfassung

PyDipAPI ist ein **gut strukturiertes, modernes Python-Projekt** mit:

- **Klarer Architektur** mit Schichtentrennung
- **Modularem Design** für einfache Erweiterbarkeit
- **Robuster Implementierung** mit umfassendem Error-Handling
- **Performance-Optimierungen** durch Async-Support und Caching
- **Hoher Code-Qualität** mit Type-Safety und umfassenden Tests
- **Professionellem CI/CD** mit automatisiertem Testing und Publishing

Das Projekt folgt Python-Best-Practices und ist für den produktiven Einsatz in Forschung, Journalismus und Software-Entwicklung geeignet.
