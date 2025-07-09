# pydipapi - Python Client für die deutsche Bundestag API

Ein moderner, vollständiger Python-Client für die deutsche Bundestag API (DIP) mit erweiterten Funktionen für Batch-Operationen, Caching und Performance-Optimierung.

## 🚀 Features

- **Vollständige API-Abdeckung** - Alle Endpunkte der Bundestag API
- **Batch-Operationen** - Mehrere IDs in einem Aufruf abrufen
- **Intelligentes Caching** - Automatisches Caching für bessere Performance
- **Rate Limiting** - Konfigurierbare Verzögerungen zwischen Requests
- **Retry-Logik** - Automatische Wiederholung bei Fehlern
- **Flexible Filterung** - Umfassende Such- und Filteroptionen
- **Convenience-Methoden** - Einfache Abfragen für häufige Anwendungsfälle
- **Content-Parser** - Strukturierte Extraktion von Protokollen, Dokumenten und Personen
- **Async-Support** - Asynchrone API-Aufrufe für bessere Performance
- **Vollständige Dokumentation** - Detaillierte API-Referenz und Beispiele

## 📦 Installation

```bash
pip install pydipapi
```

## 🔑 API-Key erhalten

1. Besuchen Sie [https://dip.bundestag.de/über-dip/hilfe/api](https://dip.bundestag.de/über-dip/hilfe/api)
2. Registrieren Sie sich für einen API-Key
3. Setzen Sie die Umgebungsvariable: `export DIP_API_KEY='ihr_api_key'`

## 🎯 Schnellstart

### 📓 Interaktives Lernen (Empfohlen)
Nutzen Sie unsere **[Jupyter Notebooks](notebooks.md)** für eine Schritt-für-Schritt Einführung:

```bash
# Notebooks starten
jupyter lab
# Dann: notebooks/01_basic_usage.ipynb öffnen
```

### 💻 Code-Beispiele

```python
from pydipapi import DipAnfrage, ProtocolParser, DocumentParser, PersonParser

# Client initialisieren
dip = DipAnfrage(api_key='ihr_api_key')

# Personen abrufen
persons = dip.get_person(anzahl=10)

# Dokumente durchsuchen
docs = dip.search_documents("Bundeshaushalt", anzahl=5)

# Batch-Operationen
person_ids = [12345, 67890, 11111]
persons_batch = dip.get_person_ids(person_ids)

# Convenience-Methoden
recent_activities = dip.get_recent_activities(days=7)

# Content-Parser verwenden
parser = ProtocolParser()
protocols = dip.get_plenarprotokoll(anzahl=1, text=True)
if protocols:
    parsed = parser.parse(protocols[0])
    print(f"Sprecher: {parsed['parsed']['speakers']['total_speakers']}")
```

## 📚 Dokumentation

- **[Grundlegende Verwendung](usage.md)** - Erste Schritte und grundlegende Funktionen
- **[Interaktive Notebooks](notebooks.md)** - Jupyter Notebooks für praktisches Lernen
- **[API-Referenz](api_reference.md)** - Vollständige API-Dokumentation mit Filter-Mapping
- **[OpenAPI-Spezifikation](openapi_spec.md)** - Technische API-Details
- **[Entwickler-Guide](developer_guide.md)** - Erweiterte Nutzung und Entwicklung
- **[Changelog](changelog.md)** - Versionshistorie und Änderungen

## 🔧 Konfiguration

```python
# Erweiterte Konfiguration
dip = DipAnfrage(
    api_key='ihr_api_key',
    rate_limit_delay=0.1,    # 100ms zwischen Requests
    max_retries=3,           # Maximale Wiederholungsversuche
    enable_cache=True,        # Caching aktivieren
    cache_ttl=3600           # Cache-TTL in Sekunden
)
```

## 📊 Verfügbare Endpunkte

| Endpunkt | Beschreibung | Batch-Support | Parser |
|----------|--------------|---------------|--------|
| `get_person()` | Personen abrufen | ✅ | PersonParser |
| `get_aktivitaet()` | Aktivitäten abrufen | ✅ | ActivityParser |
| `get_drucksache()` | Dokumente abrufen | ✅ | DocumentParser |
| `get_plenarprotokoll()` | Protokolle abrufen | ✅ | ProtocolParser |
| `get_vorgang()` | Vorgänge abrufen | ✅ | - |
| `get_vorgangsposition()` | Vorgangspositionen abrufen | ✅ | - |

## 🔍 Filter-Optionen

| Parameter | Beschreibung | Beispiel |
|-----------|--------------|----------|
| `wahlperiode` | Legislaturperiode | `wahlperiode=20` |
| `datum_start` / `datum_end` | Datumsbereich | `datum_start="2024-01-01"` |
| `titel` | Titel-Suche | `titel="Bundeshaushalt"` |
| `drucksachetyp` | Dokumenttyp | `drucksachetyp="Antrag"` |
| `vorgangstyp` | Vorgangstyp | `vorgangstyp="Gesetzgebung"` |

## 🚀 Convenience-Methoden

```python
# Suche nach Dokumenten
docs = dip.search_documents("Klimaschutz", anzahl=10)

# Aktuelle Aktivitäten
recent = dip.get_recent_activities(days=7)

# Personen nach Namen suchen
persons = dip.get_person_by_name("Merkel", anzahl=5)

# Dokumente nach Typ
anträge = dip.get_documents_by_type("Antrag", anzahl=10)

# Vorgänge nach Typ
gesetzgebung = dip.get_proceedings_by_type("Gesetzgebung", anzahl=10)
```

## 📈 Performance-Optimierung

### Caching
```python
# Cache aktivieren
dip = DipAnfrage(api_key='key', enable_cache=True, cache_ttl=7200)

# Cache verwalten
dip.clear_cache()           # Gesamten Cache löschen
dip.clear_expired_cache()   # Abgelaufene Einträge löschen
```

### Batch-Operationen
```python
# Mehrere IDs auf einmal abrufen
person_ids = [12345, 67890, 11111]
persons = dip.get_person_ids(person_ids)

doc_ids = [12345, 67890]
docs = dip.get_drucksache_ids(doc_ids, text=True)
```

### Content-Parser
```python
from pydipapi import ProtocolParser, DocumentParser, PersonParser

# Protokoll-Parser für Volltext-Plenarprotokolle
protocol_parser = ProtocolParser()
protocols = dip.get_plenarprotokoll(anzahl=1, text=True)
if protocols:
    parsed = protocol_parser.parse(protocols[0])
    print(f"Sprecher: {parsed['parsed']['speakers']['total_speakers']}")
    print(f"Interventionen: {parsed['parsed']['interventions']['total_interventions']}")

# Dokument-Parser für strukturierte Dokumente
doc_parser = DocumentParser()
docs = dip.get_drucksache(anzahl=1)
if docs:
    parsed = doc_parser.parse(docs[0])
    print(f"Autoren: {len(parsed['parsed']['authors'])}")
    print(f"Parteien: {parsed['parsed']['parties']}")

# Personen-Parser für Abgeordnete
person_parser = PersonParser()
persons = dip.get_person(anzahl=1)
if persons:
    parsed = person_parser.parse(persons[0])
    print(f"Name: {parsed['parsed']['basic_info']['name']}")
    print(f"Partei: {parsed['parsed']['party_info']['current_party']}")
```

## 🛠️ Entwicklung

### Installation für Entwicklung
```bash
git clone https://github.com/lichtbaer/pydipapi.git
cd pydipapi
pip install -e .
pip install -r requirements-dev.txt
```

### Tests ausführen
```bash
pytest tests/
```

### Linting
```bash
ruff check .
bandit -r pydipapi/
```

## 📝 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.

## 🤝 Beitragen

Beiträge sind willkommen! Bitte lesen Sie den [Entwickler-Guide](developer_guide.md) für Details.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/lichtbaer/pydipapi/issues)
- **Dokumentation**: [Vollständige Dokumentation](https://lichtbaer.github.io/pydipapi/)
- **API-Dokumentation**: [Bundestag API](https://dip.bundestag.de/über-dip/hilfe/api)
