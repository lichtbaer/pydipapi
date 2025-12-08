# PyDipAPI Jupyter Notebooks

Diese Notebooks bieten eine umfassende, interaktive Einführung in PyDipAPI, dem modernen Python-Client für die Bundestag API.

## 📚 Vollständige Notebook-Serie

### Grundlagen
1. **01_basic_usage.ipynb** - Grundlagen und erste Schritte
   - API-Schlüssel einrichten
   - Client initialisieren
   - Erste einfache Abfragen
   - Convenience-Methoden kennenlernen

2. **02_filtering_and_search.ipynb** - Erweiterte Filterung und Suche
   - Textsuche in Dokumenten
   - Datumsbasierte Filter
   - Wahlperioden-Filter
   - Kombinierte Filter-Strategien

3. **03_batch_operations_and_caching.ipynb** - Performance-Optimierung
   - Batch-Anfragen für mehrere IDs
   - Intelligentes Caching nutzen
   - Cache-Management
   - Performance-Optimierung Best Practices

### Erweiterte Features
4. **04_content_parsers.ipynb** - Content-Parser für strukturierte Datenanalyse
   - ProtocolParser - Plenarprotokolle analysieren
   - DocumentParser - Drucksachen verarbeiten
   - PersonParser - Abgeordneten-Daten strukturieren
   - ActivityParser - Aktivitäten analysieren
   - Batch-Parsing und Regex-Extraktion

5. **05_async_api_tutorial.ipynb** - Asynchrone API für maximale Performance
   - AsyncDipAnfrage verwenden
   - Performance-Vergleich Sync vs. Async
   - Asynchrone Batch-Operationen
   - Async Context Manager
   - Error Handling in async-Kontext

6. **06_data_visualization.ipynb** - Datenvisualisierung und Analyse
   - Interaktive Charts mit Plotly
   - Statistische Analysen
   - Dashboard-Erstellung
   - Export-Funktionen (CSV, JSON, HTML)
   - Integration mit Matplotlib und Pandas

## 🚀 Ersten Schritte

### Voraussetzungen

1. **Python-Umgebung:**
   ```bash
   # Im Projektverzeichnis
   pip install -e .
   pip install jupyter jupyterlab matplotlib plotly pandas
   ```

2. **API-Schlüssel besorgen:**
   - Besuchen Sie: https://dip.bundestag.de/api/
   - Registrieren Sie sich für einen kostenlosen API-Schlüssel
   - **Wichtig**: Ersetzen Sie in jedem Notebook `"HIER_IHREN_API_SCHLUESSEL_EINFUEGEN"`

### Notebooks starten

1. **Jupyter Lab starten (empfohlen):**
   ```bash
   # Im Projektverzeichnis
   jupyter lab
   ```

2. **Oder klassisches Jupyter Notebook:**
   ```bash
   # Im Projektverzeichnis
   jupyter notebook
   ```

3. **Navigieren Sie zum `notebooks/` Verzeichnis**

4. **Starten Sie mit `01_basic_usage.ipynb`**

## 📋 Lernpfad-Empfehlungen

### 🥉 Einsteiger (Notebooks 1-3)
**Ziel**: Grundlagen der Bundestag API beherrschen
- Verstehen der API-Struktur
- Einfache Datenabfragen
- Performance-Optimierung

### 🥈 Fortgeschrittene (Notebooks 4-5)
**Ziel**: Strukturierte Datenanalyse und Performance
- Content-Parser für Datenextraktion
- Asynchrone Programmierung
- Komplexe Datenverarbeitung

### 🥇 Experten (Notebook 6)
**Ziel**: Professionelle Datenvisualisierung
- Interaktive Dashboards
- Statistische Analysen
- Export und Berichtswesen

## 🔧 Troubleshooting

### Häufige Probleme

**"ModuleNotFoundError: No module named 'pydipapi'"**
```bash
# Im Projektverzeichnis ausführen:
pip install -e .
```

**"API-Key fehlt oder ungültig"**
- Überprüfen Sie Ihren API-Schlüssel
- Ersetzen Sie `"HIER_IHREN_API_SCHLUESSEL_EINFUEGEN"` in jedem Notebook
- Besuchen Sie https://dip.bundestag.de/api/ für einen neuen Schlüssel

**"Jupyter nicht gefunden"**
```bash
pip install jupyter jupyterlab
```

**"Plotting-Bibliotheken fehlen"**
```bash
pip install matplotlib plotly pandas seaborn
```

**Cache-Probleme**
```bash
# Cache-Verzeichnis löschen falls nötig
rm -rf notebooks/.cache
```

## 📊 Datenquellen und APIs

### Bundestag API Endpunkte
- **Personen**: Abgeordnete und ihre Daten
- **Drucksachen**: Parlamentarische Dokumente
- **Aktivitäten**: Parlamentarische Aktivitäten
- **Plenarprotokolle**: Volltext-Sitzungsprotokolle
- **Vorgänge**: Gesetzgebungsverfahren
- **Vorgangspositionen**: Einzelne Verfahrensschritte

### Verfügbare Filter
- Wahlperioden (z.B. 19, 20)
- Datumsbereiche
- Dokumenttypen (Antrag, Gesetzentwurf, etc.)
- Textsuche
- Personen-IDs
- Und viele mehr...

## 🎯 Praktische Anwendungsfälle

### Journalismus & Recherche
- Verfolgung aktueller Gesetzgebung
- Analyse von Redebeiträgen
- Monitoring politischer Aktivitäten

### Wissenschaft & Forschung
- Politikwissenschaftliche Analysen
- Parlamentarische Datenauswertung
- Longitudinale Studien

### Bildung & Lehre
- Politische Bildung
- Demokratie-Vermittlung
- Datenanalyse-Übungen

### Zivilgesellschaft
- Bürgerbeteiligung
- Transparenz-Initiativen
- Advocacy-Arbeit

## 📖 Weitere Ressourcen

### Projekt-Dokumentation
- **API-Referenz**: `../docs/api_reference.md`
- **Entwickler-Guide**: `../docs/developer_guide.md`
- **Content-Parser Docs**: `../docs/content_parsers.md`

### Externe Ressourcen
- **Bundestag API-Dokumentation**: https://dip.bundestag.de/über-dip/hilfe/api
- **PyDipAPI GitHub**: https://github.com/lichtbaer/pydipapi
- **Python Dokumentation**: https://docs.python.org/3/

### Community & Support
- GitHub Issues für Fragen und Bugs
- Discussions für allgemeine Fragen
- Wiki für Community-Beiträge

## 💡 Tipps für effektives Lernen

1. **Arbeiten Sie die Notebooks in Reihenfolge durch**
2. **Experimentieren Sie mit eigenen Beispielen**
3. **Nutzen Sie echte Daten für Ihre Projekte**
4. **Kombinieren Sie verschiedene Techniken**
5. **Dokumentieren Sie Ihre Erkenntnisse**

## 🔄 Updates und Neuerungen

Die Notebooks werden regelmäßig aktualisiert:
- Neue API-Features werden integriert
- Zusätzliche Beispiele werden hinzugefügt
- Performance-Verbesserungen werden dokumentiert
- Community-Feedback wird eingearbeitet

**Viel Erfolg beim Lernen und Analysieren! 🚀**

---
**📅 Letztes Update**: 2025-01-09  
**📧 Fragen?** Erstellen Sie ein Issue auf GitHub! 