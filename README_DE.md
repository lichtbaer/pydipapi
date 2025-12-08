# pydipapi - Python Client für die deutsche Bundestag API

[![PyPI version](https://badge.fury.io/py/pydipapi.svg)](https://badge.fury.io/py/pydipapi)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://lichtbaer.github.io/pydipapi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

Ein moderner, vollständiger Python-Client für die deutsche Bundestag API (DIP) mit erweiterten Funktionen für Batch-Operationen, Caching und Performance-Optimierung.

## 🚀 Features

- **🔄 Async Support** - Hochperformanter asynchroner API-Client für gleichzeitige Anfragen
- **📊 Content Parsers** - Strukturierte Datenextraktion aus parlamentarischen Dokumenten
- **⚡ Intelligentes Caching** - Integriertes Caching mit konfigurierbarer TTL und Größenlimits
- **🔍 Erweiterte Filterung** - Leistungsstarke Such- und Filterfunktionen
- **📦 Batch-Operationen** - Effiziente Massendatenabfrage und -verarbeitung
- **🛡️ Fehlerbehandlung** - Robuste Fehlerbehandlung mit Wiederholungsmechanismen
- **📚 Typsicherheit** - Vollständige Typannotationen für bessere IDE-Unterstützung
- **🎯 Einfach zu verwenden** - Einfaches, intuitives API-Design

## 📦 Installation

```bash
pip install pydipapi
```

## 🔑 API-Key erhalten

1. Besuchen Sie [https://dip.bundestag.de/über-dip/hilfe/api](https://dip.bundestag.de/über-dip/hilfe/api)
2. Registrieren Sie sich für einen API-Key
3. Setzen Sie die Umgebungsvariable: `export DIP_API_KEY='ihr_api_key'`

## 🏃 Schnellstart

### Grundlegende Verwendung

```python
from pydipapi import DipAnfrage

# Client initialisieren
api = DipAnfrage(api_key="ihr_api_key_hier")

# Abgeordnete abrufen
members = api.get_person(anzahl=10)
for member in members:
    print(f"{member['vorname']} {member['nachname']} ({member.get('fraktion', 'Unbekannt')})")

# Aktuelle Dokumente abrufen
documents = api.get_drucksache(anzahl=5)
for doc in documents:
    print(f"Dokument: {doc['titel']}")
```

### Async-Verwendung

```python
import asyncio
from pydipapi.async_api import AsyncDipAnfrage

async def main():
    async with AsyncDipAnfrage(api_key="ihr_api_key_hier") as api:
        # Parallele Anfragen für bessere Performance
        members, documents, activities = await asyncio.gather(
            api.get_person(anzahl=10),
            api.get_drucksache(anzahl=10),
            api.get_aktivitaet(anzahl=10)
        )
        
        print(f"Abgerufen: {len(members)} Abgeordnete, {len(documents)} Dokumente, {len(activities)} Aktivitäten")

asyncio.run(main())
```

### Content Parsing

```python
from pydipapi import DipAnfrage
from pydipapi.parsers import DocumentParser, PersonParser

api = DipAnfrage(api_key="ihr_api_key_hier")

# Dokumentinhalt parsen
documents = api.get_drucksache(anzahl=5)
doc_parser = DocumentParser()
parsed_docs = doc_parser.parse_batch(documents)

for doc in parsed_docs:
    print(f"Titel: {doc.get('titel')}")
    print(f"Typ: {doc.get('dokumenttyp')}")
    print(f"Autoren: {', '.join(doc.get('autoren', []))}")

# Abgeordneteninformationen parsen
members = api.get_person(anzahl=10)
person_parser = PersonParser()
parsed_members = person_parser.parse_batch(members)

for member in parsed_members:
    print(f"Name: {member.get('name')}")
    print(f"Partei: {member.get('partei')}")
    print(f"Wahlkreis: {member.get('wahlkreis')}")
```

## 📚 Dokumentation

Die vollständige Dokumentation ist verfügbar unter: **[https://lichtbaer.github.io/pydipapi/](https://lichtbaer.github.io/pydipapi/)**

### Dokumentationsseiten

- **[Grundlegende Verwendung](https://lichtbaer.github.io/pydipapi/usage/)** - Erste Schritte und grundlegende Funktionen
- **[Interaktive Notebooks](https://lichtbaer.github.io/pydipapi/notebooks/)** - Jupyter Notebooks für praktisches Lernen
- **[API-Referenz](https://lichtbaer.github.io/pydipapi/api_reference/)** - Vollständige API-Dokumentation mit Filter-Mapping
- **[OpenAPI-Spezifikation](https://lichtbaer.github.io/pydipapi/openapi_spec/)** - Technische API-Details
- **[Entwickler-Guide](https://lichtbaer.github.io/pydipapi/developer_guide/)** - Erweiterte Nutzung und Entwicklung
- **[Changelog](https://lichtbaer.github.io/pydipapi/changelog/)** - Versionshistorie und Änderungen

### 📓 Jupyter Notebooks

Interaktive Tutorials für praktisches Lernen (im `notebooks/` Verzeichnis):

- **`01_basic_usage.ipynb`** - Grundlagen und erste Schritte mit der API
- **`02_filtering_and_search.ipynb`** - Erweiterte Filteroptionen und Suchfunktionen  
- **`03_batch_operations_and_caching.ipynb`** - Performance-Optimierung und Batch-Operationen

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

## 🏗️ Verfügbare Endpunkte

| Endpunkt | Methode | Beschreibung |
|----------|--------|-------------|
| **Abgeordnete** | `get_person()` | Abgeordnete abrufen |
| **Dokumente** | `get_drucksache()` | Parlamentarische Dokumente abrufen |
| **Protokolle** | `get_plenarprotokoll()` | Plenarsitzungsprotokolle abrufen |
| **Aktivitäten** | `get_aktivitaet()` | Parlamentarische Aktivitäten abrufen |
| **Verfahren** | `get_vorgang()` | Gesetzgebungsverfahren abrufen |

## 🔍 Filter-Optionen

| Parameter | Beschreibung | Beispiel |
|-----------|--------------|----------|
| `wahlperiode` | Legislaturperiode | `wahlperiode=20` |
| `datum_start` / `datum_end` | Datumsbereich | `datum_start="2024-01-01"` |
| `titel` | Titel-Suche | `titel="Bundeshaushalt"` |
| `drucksachetyp` | Dokumenttyp | `drucksachetyp="Antrag"` |
| `vorgangstyp` | Vorgangstyp | `vorgangstyp="Gesetzgebung"` |

## 📚 Dokumentation & Beispiele

### Jupyter Notebooks
Umfassende Tutorials sind im `notebooks/` Verzeichnis verfügbar:

1. **Grundlegende Verwendung** - Erste Schritte mit PyDipAPI
2. **Filterung & Suche** - Erweiterte Abfragetechniken
3. **Batch-Operationen** - Effiziente Massendatenverarbeitung
4. **Content Parsers** - Strukturierte Datenextraktion
5. **Async API** - Hochperformante Async-Operationen
6. **Datenvisualisierung** - Erstellen von Diagrammen und Dashboards

### Beispiel-Skripte
Prüfen Sie das `examples/` Verzeichnis für praktische Anwendungsfälle:
- Grundlegende API-Verwendung
- Async-Implementierung
- Content-Parsing-Beispiele
- Erweiterte Filterungstechniken

## 📈 Erweiterte Features

### Intelligentes Caching

```python
from pydipapi import DipAnfrage
from pydipapi.util.cache import SimpleCache

# Caching konfigurieren
cache = SimpleCache(
    ttl=3600  # Cache TTL: 1 Stunde
)

api = DipAnfrage(api_key="ihr_api_key_hier", enable_cache=True, cache_ttl=3600)

# Erster Aufruf greift auf die API zu
members = api.get_person(anzahl=10)

# Zweiter Aufruf nutzt Cache (viel schneller)
members_cached = api.get_person(anzahl=10)

# Cache-Statistiken prüfen
print(f"Cache Treffer: {cache.hits}")
print(f"Cache Fehlschläge: {cache.misses}")
print(f"Trefferquote: {cache.hit_rate:.2%}")
```

### Erweiterte Filterung

```python
from datetime import datetime, timedelta

# Nach Datumsbereich filtern
start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()

recent_documents = api.get_drucksache(
    datum_start=start_date.strftime("%Y-%m-%d"),
    datum_end=end_date.strftime("%Y-%m-%d"),
    anzahl=50
)

# Nach Wahlperiode filtern
current_period_docs = api.get_drucksache(
    wahlperiode=20,
    anzahl=100
)

# Komplexe Filterung mit mehreren Parametern
specific_activities = api.get_aktivitaet(
    wahlperiode=20,
    datum_start="2023-01-01",
    anzahl=50
)
```

### Batch-Operationen

```python
# Effiziente Batch-Verarbeitung
all_members = []
batch_size = 100

for offset in range(0, 1000, batch_size):
    batch = api.get_person(anzahl=batch_size, offset=offset)
    all_members.extend(batch)
    print(f"Bisher abgerufen: {len(all_members)} Abgeordnete...")

print(f"Gesamt abgerufene Abgeordnete: {len(all_members)}")
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

### Dokumentation lokal bauen
```bash
mkdocs serve
```

## 📝 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Siehe [LICENSE](LICENSE) für Details.

## 🤝 Beitragen

Beiträge sind willkommen! Bitte lesen Sie den [Entwickler-Guide](https://lichtbaer.github.io/pydipapi/developer_guide/) für Details.

### Entwicklungsumgebung einrichten

1. Repository klonen
2. Virtuelle Umgebung erstellen
3. Abhängigkeiten installieren: `pip install -r requirements-dev.txt`
4. Pre-Commit Hooks installieren: `pre-commit install`
5. Tests ausführen: `pytest tests/`

### Pull Request Guidelines

- Verwenden Sie aussagekräftige Commit-Messages
- Fügen Sie Tests für neue Features hinzu
- Aktualisieren Sie die Dokumentation bei Bedarf
- Stellen Sie sicher, dass alle Tests bestehen

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/lichtbaer/pydipapi/issues)
- **Dokumentation**: [https://lichtbaer.github.io/pydipapi/](https://lichtbaer.github.io/pydipapi/)
- **API-Dokumentation**: [Bundestag API](https://dip.bundestag.de/über-dip/hilfe/api)

## 🙏 Danksagungen

- **Deutscher Bundestag** - Bereitstellung der API
- **Python Community** - Open Source Libraries und Tools
- **MkDocs Team** - Dokumentations-Framework
- **Ruff Team** - Python Linter
- **Bandit Team** - Sicherheits-Tool

## 📊 Projekt-Status

- **Version**: 0.1.0 (Beta)
- **Python**: 3.9+
- **Status**: Beta - Vorbereitung für 1.0.0
- **Tests**: ✅ Bestehend
- **Dokumentation**: ✅ Vollständig
- **CI/CD**: ✅ Konfiguriert

---

**Hinweis**: Dieses Projekt ist nicht mit dem deutschen Bundestag affiliiert. Für offizielle Informationen besuchen Sie [https://dip.bundestag.de/](https://dip.bundestag.de/).