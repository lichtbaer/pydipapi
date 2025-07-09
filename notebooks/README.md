# PyDipAPI Jupyter Notebooks

Diese Notebooks bieten eine interaktive Einführung in PyDipAPI, dem Python-Client für die Bundestag API.

## 📚 Notebooks

1. **01_basic_usage.ipynb** - Grundlagen und erste Schritte
   - API-Schlüssel einrichten
   - Client initialisieren
   - Erste einfache Abfragen
   - Basisfunktionen verstehen

2. **02_filtering_and_search.ipynb** - Erweiterte Filterung und Suche
   - Textsuche in Dokumenten
   - Datumsbasierte Filter
   - Wahlperioden-Filter
   - Kombinierte Filter

3. **03_batch_operations_and_caching.ipynb** - Batch-Operationen und Caching
   - Batch-Anfragen für mehrere IDs
   - Caching aktivieren und nutzen
   - Performance-Optimierung
   - Best Practices

## 🚀 Ersten Schritte

### Voraussetzungen

1. **Jupyter installieren:**
   ```bash
   pip install jupyter
   ```

2. **API-Schlüssel besorgen:**
   - Besuchen Sie: https://dip.bundestag.de/api/
   - Registrieren Sie sich für einen kostenlosen API-Schlüssel

3. **PyDipAPI installieren:**
   ```bash
   cd /home/johannes/PycharmProjects/pydipapi
   pip install -e .
   ```

### Notebooks starten

1. **Jupyter Lab starten:**
   ```bash
   cd /home/johannes/PycharmProjects/pydipapi
   jupyter lab
   ```

2. **Oder Jupyter Notebook:**
   ```bash
   cd /home/johannes/PycharmProjects/pydipapi
   jupyter notebook
   ```

3. **Navigieren Sie zum `notebooks/` Verzeichnis**

4. **Öffnen Sie das erste Notebook: `01_basic_usage.ipynb`**

## ⚠️ Wichtige Hinweise

- **API-Schlüssel:** Vergessen Sie nicht, in jedem Notebook `"HIER_IHREN_API_SCHLUESSEL_EINFUEGEN"` durch Ihren echten API-Schlüssel zu ersetzen!

- **Reihenfolge:** Arbeiten Sie die Notebooks in der angegebenen Reihenfolge durch (01 → 02 → 03)

- **Internet-Verbindung:** Für API-Aufrufe ist eine aktive Internet-Verbindung erforderlich

## 🔧 Fehlerbehebung

### "ModuleNotFoundError: No module named 'pydipapi'"
```bash
# Im Projektverzeichnis ausführen:
pip install -e .
```

### "API-Key fehlt oder ungültig"
- Überprüfen Sie Ihren API-Schlüssel
- Stellen Sie sicher, dass er korrekt in die Notebooks eingefügt wurde
- Besuchen Sie https://dip.bundestag.de/api/ für einen neuen Schlüssel

### "Jupyter nicht gefunden"
```bash
pip install jupyter jupyterlab
```

## 📖 Weitere Ressourcen

- **Projektdokumentation:** `../docs/`
- **API-Referenz:** `../docs/api_reference.md`
- **Entwickler-Guide:** `../docs/developer_guide.md`
- **Bundestag API-Dokumentation:** https://dip.bundestag.de/über-dip/hilfe/api

## 🎯 Nach den Notebooks

Nach dem Durcharbeiten der Notebooks können Sie:

- Eigene Projekte mit PyDipAPI entwickeln
- Die vollständige API-Dokumentation studieren
- Zur Weiterentwicklung von PyDipAPI beitragen
- Datenanalysen mit Bundestag-Daten durchführen

**Viel Erfolg beim Lernen! 🚀** 