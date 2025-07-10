# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Geplant
- Erweiterte Visualisierungsfunktionen
- Machine Learning Integration für Dokumentenanalyse
- GraphQL API Wrapper
- Real-time WebSocket Support

## [0.1.1] - 2025-07-10

### Behoben
- **AsyncDipAnfrage** - Kritische Bugs im Async-Client behoben
  - `_make_request()` gab `None` für gecachte Daten zurück - behoben
  - Context Manager Probleme mit aiohttp Responses - behoben  
  - Rate Limiting Kompatibilität mit aiohttp Responses - behoben
  - Verbesserte Fehlerbehandlung und Response-Management
- **Jupyter Notebooks** - Alle Tutorial-Notebooks verbessert und Fehler behoben
  - Async-Probleme in `05_async_api_tutorial.ipynb` behoben
  - Umfassende Fehlerbehandlung und Fallback-Mechanismen hinzugefügt
  - Verbesserte Performance-Tests und Dokumentation
  - API-Key-Behandlung in allen Notebooks aktualisiert

### Verbessert
- **Tutorial-Notebooks** - Wesentliche Verbesserungen in allen 6 Tutorial-Notebooks
  - `02_filtering_and_search.ipynb`: Erweitert mit umfassenden Suchbeispielen
  - `03_batch_operations_and_caching.ipynb`: Verbessert mit praktischen Batch-Beispielen
  - `04_content_parsers.ipynb`: Fehlende `parse_batch` Methoden und Beispiele hinzugefügt
  - `05_async_api_tutorial.ipynb`: Async-Probleme behoben und Fehlerbehandlung verbessert
  - `06_data_visualization.ipynb`: Erheblich erweitert mit umfangreichen Visualisierungsbeispielen
- **Code-Qualität** - Verbesserte Type-Annotations und Fehlerbehandlung im gesamten Codebase
- **Dokumentation** - Alle Beispiele und Dokumentation aktualisiert um Bug-Fixes zu reflektieren

### Technisch
- MockResponse-Implementierung für ordnungsgemäße Async-Response-Behandlung repariert
- Verbesserte Verbindungsverwaltung mit ordnungsgemäßen `await response.release()` Aufrufen
- Vereinfachte Rate-Limiting-Logik für bessere aiohttp-Kompatibilität
- Verbesserte Type-Safety mit `Optional[Any]` Return-Types

## [1.0.0] - 2025-07-10

### Hinzugefügt
- **Vollständige API-Abdeckung** - Alle Bundestag API Endpunkte implementiert
- **Batch-Operationen** - Mehrere IDs in einem Aufruf abrufen
- **Intelligentes Caching** - File-basiertes Caching mit TTL
- **Rate Limiting** - Konfigurierbare Verzögerungen zwischen Requests
- **Retry-Logik** - Automatische Wiederholung bei Fehlern
- **Convenience-Methoden** - Einfache Abfragen für häufige Anwendungsfälle
- **Flexible Filterung** - Umfassende Such- und Filteroptionen
- **Vollständige Dokumentation** - Detaillierte API-Referenz und Beispiele
- **Jupyter Notebooks** - Interaktive Beispiele und Tutorials
- **Pre-Commit Hooks** - Automatische Code-Qualitätsprüfung
- **CI/CD Pipeline** - Automatisierte Tests und Deployment
- **MkDocs Integration** - Professionelle Dokumentationswebsite

### Geändert
- **Projektstruktur** - Modularisierte Architektur mit separaten Client- und Utility-Modulen
- **Error Handling** - Verbesserte Fehlerbehandlung mit spezifischen Exception-Typen
- **Caching-Implementierung** - SHA256-basierte Cache-Keys statt MD5
- **API-Response-Parsing** - Robusteres Parsing der API-Responses
- **Dokumentation** - Vollständig überarbeitete und erweiterte Dokumentation

### Verbessert
- **Performance** - Optimierte Batch-Operationen und Caching
- **Code-Qualität** - Ruff und Bandit Integration für Linting und Sicherheit
- **Entwickler-Experience** - Umfassende Entwickler-Dokumentation
- **Beispiele** - Praktische Beispiele und Tutorials

### Behoben
- **Sicherheitslücken** - Ersetzung von MD5 durch SHA256 für Cache-Keys
- **Linting-Fehler** - Alle Ruff und Bandit Warnungen behoben
- **Import-Fehler** - Korrekte Import-Struktur implementiert
- **Dokumentationsfehler** - Aktualisierte und korrekte Dokumentation

## [0.2.0] - 2025-06-XX

### Hinzugefügt
- **Batch-Operationen** - `get_person_ids()`, `get_drucksache_ids()`, etc.
- **Convenience-Methoden** - `search_documents()`, `get_recent_activities()`, etc.
- **Caching-System** - File-basiertes Caching mit TTL
- **Rate Limiting** - Konfigurierbare Verzögerungen
- **Filter-Mapping-Tabelle** - Umfassende Dokumentation aller Filter-Parameter
- **Erweiterte Dokumentation** - API-Referenz und Entwickler-Guide

### Geändert
- **Projektstruktur** - Modularisierte Architektur
- **Error Handling** - Verbesserte Fehlerbehandlung
- **Dokumentation** - Erweiterte und verbesserte Dokumentation

## [0.1.0] - 2025-01-XX

### Hinzugefügt
- **Grundlegende API-Funktionalität** - Personen, Aktivitäten, Dokumente abrufen
- **Einfache Client-Klasse** - `DipAnfrage` für API-Zugriff
- **Basis-Dokumentation** - README und grundlegende Anleitung
- **Requirements-Datei** - Abhängigkeiten definiert
- **Setup.py** - Package-Konfiguration

### Features
- `get_person()` - Personen abrufen
- `get_aktivitaet()` - Aktivitäten abrufen
- `get_drucksache()` - Dokumente abrufen
- `get_plenarprotokoll()` - Protokolle abrufen
- `get_vorgang()` - Vorgänge abrufen
- `get_vorgangsposition()` - Vorgangspositionen abrufen

## Technische Details

### Versionsschema
- **MAJOR.MINOR.PATCH**
- **MAJOR**: Inkompatible API-Änderungen
- **MINOR**: Neue Features (rückwärtskompatibel)
- **PATCH**: Bug-Fixes (rückwärtskompatibel)

### Breaking Changes
- Version 1.0.0: Vollständige API-Umstrukturierung mit modularer Architektur
- Version 0.2.0: Hinzufügung von Batch-Operationen und Convenience-Methoden

### Migration Guide
- **Von 0.1.0 zu 0.2.0**: Keine Breaking Changes
- **Von 0.2.0 zu 1.0.0**: 
  - Neue Import-Struktur: `from pydipapi import DipAnfrage`
  - Erweiterte Konfigurationsoptionen
  - Neue Convenience-Methoden verfügbar

## Bekannte Probleme

### Version 1.0.0
- Keine bekannten kritischen Probleme
- Einige Edge Cases bei sehr großen Batch-Operationen (>100 IDs)
- Cache-Performance bei sehr großen Datensätzen

### Geplante Fixes
- Optimierung der Batch-Operationen für große Datensätze
- Verbesserte Cache-Performance
- Erweiterte Error-Handling für spezifische API-Fehler

## Contributors

- **lichtbaer** - Hauptentwickler und Projektleiter
- **GitHub Community** - Bug Reports und Feature Requests

## Danksagungen

- **Deutscher Bundestag** - Bereitstellung der API
- **Python Community** - Open Source Libraries und Tools
- **MkDocs Team** - Dokumentations-Framework
- **Ruff Team** - Python Linter
- **Bandit Team** - Sicherheits-Tool 