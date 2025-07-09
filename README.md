# pydipapi - Python Client für die deutsche Bundestag API

[![PyPI version](https://badge.fury.io/py/pydipapi.svg)](https://badge.fury.io/py/pydipapi)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://lichtbaer.github.io/pydipapi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

Ein moderner, vollständiger Python-Client für die deutsche Bundestag API (DIP) mit erweiterten Funktionen für Batch-Operationen, Caching und Performance-Optimierung.

## 🚀 Features

- **Vollständige API-Abdeckung** - Alle Endpunkte der Bundestag API
- **Batch-Operationen** - Mehrere IDs in einem Aufruf abrufen
- **Intelligentes Caching** - Automatisches Caching für bessere Performance
- **Rate Limiting** - Konfigurierbare Verzögerungen zwischen Requests
- **Retry-Logik** - Automatische Wiederholung bei Fehlern
- **Flexible Filterung** - Umfassende Such- und Filteroptionen
- **Convenience-Methoden** - Einfache Abfragen für häufige Anwendungsfälle
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

# Convenience-Methoden
recent_activities = dip.get_recent_activities(days=7)
```

## 📚 Dokumentation

Die vollständige Dokumentation ist verfügbar unter: **[https://lichtbaer.github.io/pydipapi/](https://lichtbaer.github.io/pydipapi/)**

### Dokumentationsseiten

- **[Grundlegende Verwendung](https://lichtbaer.github.io/pydipapi/usage/)** - Erste Schritte und grundlegende Funktionen
- **[API-Referenz](https://lichtbaer.github.io/pydipapi/api_reference/)** - Vollständige API-Dokumentation mit Filter-Mapping
- **[OpenAPI-Spezifikation](https://lichtbaer.github.io/pydipapi/openapi_spec/)** - Technische API-Details
- **[Entwickler-Guide](https://lichtbaer.github.io/pydipapi/developer_guide/)** - Erweiterte Nutzung und Entwicklung
- **[Changelog](https://lichtbaer.github.io/pydipapi/changelog/)** - Versionshistorie und Änderungen

### Jupyter Notebooks

Interaktive Beispiele und Tutorials:

- **[Grundlegende Verwendung](https://lichtbaer.github.io/pydipapi/notebooks/01_basic_usage/)** - Erste Schritte mit der API
- **[Filter und Suche](https://lichtbaer.github.io/pydipapi/notebooks/02_filtering_and_search/)** - Erweiterte Filteroptionen
- **[Batch-Operationen](https://lichtbaer.github.io/pydipapi/notebooks/03_batch_operations/)** - Performance-Optimierung

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

| Endpunkt | Beschreibung | Batch-Support |
|----------|--------------|---------------|
| `get_person()` | Personen abrufen | ✅ |
| `get_aktivitaet()` | Aktivitäten abrufen | ✅ |
| `get_drucksache()` | Dokumente abrufen | ✅ |
| `get_plenarprotokoll()` | Protokolle abrufen | ✅ |
| `get_vorgang()` | Vorgänge abrufen | ✅ |
| `get_vorgangsposition()` | Vorgangspositionen abrufen | ✅ |

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

- **Version**: 1.0.0
- **Python**: 3.9+
- **Status**: Produktionsbereit
- **Tests**: ✅ Bestehend
- **Dokumentation**: ✅ Vollständig
- **CI/CD**: ✅ Konfiguriert

---

**Hinweis**: Dieses Projekt ist nicht mit dem deutschen Bundestag affiliiert. Für offizielle Informationen besuchen Sie [https://dip.bundestag.de/](https://dip.bundestag.de/).