# Interaktive Jupyter Notebooks

PyDipAPI bietet eine Sammlung von interaktiven Jupyter Notebooks, die Ihnen eine praxisnahe Einführung in die Verwendung des Python-Clients für die Bundestag API ermöglichen.

## 📚 Verfügbare Notebooks

### 1. Grundlagen und erste Schritte
**Datei:** `notebooks/01_basic_usage.ipynb`

In diesem Notebook lernen Sie:
- API-Schlüssel einrichten und konfigurieren
- DipAnfrage Client initialisieren
- Erste einfache Abfragen durchführen
- Ergebnisse verstehen und verarbeiten
- Grundlegende Funktionen für Dokumente, Personen und Suche

### 2. Erweiterte Filterung und Suche
**Datei:** `notebooks/02_filtering_and_search.ipynb`

Erweiterte Suchfunktionen und Filteroptionen:
- Textsuche in Dokumenten mit verschiedenen Begriffen
- Datumsbasierte Filter für Zeiträume
- Wahlperioden-spezifische Suchen
- Kombinierte Filter für präzise Ergebnisse

### 3. Batch-Operationen und Caching
**Datei:** `notebooks/03_batch_operations_and_caching.ipynb`

Performance-Optimierung und fortgeschrittene Funktionen:
- Batch-Anfragen für mehrere IDs gleichzeitig
- Caching aktivieren und effektiv nutzen
- Performance-Optimierung und Timing-Vergleiche
- Best Practices für große Datenmengen

### 4. Content Parser (inkl. XML-Plenarprotokolle)
**Datei:** `notebooks/04_content_parsers.ipynb`

In diesem Notebook lernen Sie:
- Content-Parser (`DocumentParser`, `PersonParser`, `ActivityParser`, `ProtocolParser`)
- Unterschied zwischen Volltext-Protokollen und strukturierter XML
- **`ProtocolXmlParser`**: Agenda/Reden/Ereignisse aus `fundstelle.xml_url` parsen

### 5. Async API Tutorial
**Datei:** `notebooks/05_async_api_tutorial.ipynb`

In diesem Notebook lernen Sie:
- `AsyncDipAnfrage` im Context Manager
- parallele Requests mit `asyncio.gather`
- Error-Handling-Patterns im Async-Kontext

### 6. Datenvisualisierung
**Datei:** `notebooks/06_data_visualization.ipynb`

In diesem Notebook lernen Sie:
- Aus API-Daten einfache Auswertungen erstellen
- Visualisierungen (je nach Setup) ausgeben

## 🚀 Erste Schritte

### Voraussetzungen

1. **Jupyter installieren:**
   ```bash
   pip install jupyter
   ```

2. **PyDipAPI installieren:**
   ```bash
   pip install pydipapi
   # Oder für Entwicklung:
   git clone https://github.com/lichtbaer/pydipapi.git
   cd pydipapi
   pip install -e .
   ```

3. **API-Schlüssel besorgen:**
   - Besuchen Sie: [https://dip.bundestag.de/api/](https://dip.bundestag.de/api/)
   - Registrieren Sie sich für einen kostenlosen API-Schlüssel

### Notebooks starten

#### Option 1: Jupyter Lab (Empfohlen)
```bash
cd pydipapi
jupyter lab
```

#### Option 2: Jupyter Notebook
```bash
cd pydipapi
jupyter notebook
```

Nach dem Start:
1. Navigieren Sie zum `notebooks/` Verzeichnis
2. Öffnen Sie das erste Notebook: `01_basic_usage.ipynb`
3. Ersetzen Sie `"HIER_IHREN_API_SCHLUESSEL_EINFUEGEN"` mit Ihrem echten API-Schlüssel
4. Führen Sie die Zellen nacheinander aus

## ⚠️ Wichtige Hinweise

### API-Schlüssel konfigurieren
**Vergessen Sie nicht**, in jedem Notebook den Platzhalter durch Ihren echten API-Schlüssel zu ersetzen:

```python
# Ändern Sie diese Zeile:
API_KEY = "HIER_IHREN_API_SCHLUESSEL_EINFUEGEN"

# Zu Ihrem echten Schlüssel:
API_KEY = "IhrEchterAPISchluessel"
```

### Empfohlene Reihenfolge
Arbeiten Sie die Notebooks in der angegebenen Reihenfolge durch:
1. `01_basic_usage.ipynb` - Grundlagen verstehen
2. `02_filtering_and_search.ipynb` - Erweiterte Funktionen
3. `03_batch_operations_and_caching.ipynb` - Performance-Optimierung
4. `04_content_parsers.ipynb` - Strukturierte Datenextraktion (inkl. XML)
5. `05_async_api_tutorial.ipynb` - Async für maximale Performance
6. `06_data_visualization.ipynb` - Daten visualisieren

### Systemanforderungen
- **Internet-Verbindung:** Für API-Aufrufe erforderlich
- **Python 3.8+:** Unterstützte Python-Versionen
- **Jupyter:** Für die Ausführung der Notebooks

## 🔧 Fehlerbehebung

### "ModuleNotFoundError: No module named 'pydipapi'"
```bash
# Stellen Sie sicher, dass PyDipAPI installiert ist:
pip install pydipapi

# Oder für lokale Entwicklung:
pip install -e .
```

### "API-Key fehlt oder ungültig"
- Überprüfen Sie Ihren API-Schlüssel auf der [Bundestag API-Seite](https://dip.bundestag.de/api/)
- Stellen Sie sicher, dass der Schlüssel korrekt in die Notebooks eingefügt wurde
- Achten Sie auf führende/nachfolgende Leerzeichen

### "Jupyter nicht gefunden"
```bash
# Jupyter installieren:
pip install jupyter jupyterlab

# Oder mit conda:
conda install -c conda-forge jupyterlab
```

### Langsame API-Antworten
- Das ist normal - die Bundestag API kann bei großen Anfragen Zeit benötigen
- Verwenden Sie kleinere `anzahl`-Parameter für Tests
- Aktivieren Sie Caching für wiederholte Anfragen

## 📖 Weiterführende Ressourcen

Nach dem Durcharbeiten der Notebooks können Sie:

### Dokumentation studieren
- **[Grundlegende Verwendung](usage.md)** - Detaillierte API-Nutzung
- **[API-Referenz](api_reference.md)** - Vollständige Methoden-Dokumentation
- **[Entwickler-Guide](developer_guide.md)** - Erweiterte Funktionen

### Eigene Projekte entwickeln
- Integrieren Sie PyDipAPI in Ihre eigenen Anwendungen
- Erstellen Sie Datenanalysen mit Bundestag-Daten
- Entwickeln Sie automatisierte Berichte und Dashboards

### Zur Community beitragen
- Melden Sie Bugs oder Feature-Requests auf [GitHub](https://github.com/lichtbaer/pydipapi/issues)
- Tragen Sie zur Weiterentwicklung bei
- Teilen Sie Ihre Erfahrungen und Anwendungsfälle

## 💡 Beispiel-Anwendungsfälle

Die Notebooks zeigen praxisnahe Beispiele für:

- **Politische Recherche:** Suche nach Dokumenten zu bestimmten Themen
- **Datenanalyse:** Analyse von Aktivitätsmustern über Zeiträume
- **Monitoring:** Automatische Überwachung neuer Dokumente oder Aktivitäten
- **Berichterstattung:** Erstellung von Berichten über parlamentarische Vorgänge
- **Akademische Forschung:** Systematische Analyse parlamentarischer Daten

**Viel Erfolg beim Lernen und Entwickeln! 🚀** 