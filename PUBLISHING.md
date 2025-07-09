# PyPI Publishing Guide für pydipapi

Diese Anleitung erklärt, wie das pydipapi-Paket auf PyPI veröffentlicht wird.

## 🚀 Schnellstart

### Automatisiert (Empfohlen)
```bash
python scripts/publish.py
```

### Manuell
```bash
# 1. Build erstellen
python -m build

# 2. Package prüfen
twine check dist/*

# 3. Zu Test PyPI hochladen (optional)
twine upload --repository testpypi dist/*

# 4. Zu PyPI hochladen
twine upload dist/*
```

## 📋 Voraussetzungen

### 1. Tools installieren
```bash
pip install build twine
```

### 2. PyPI-Accounts einrichten

#### Production PyPI
1. Account erstellen: https://pypi.org/account/register/
2. API Token erstellen: https://pypi.org/manage/account/token/
3. Token konfigurieren:
   ```bash
   # ~/.pypirc erstellen
   [pypi]
   username = __token__
   password = pypi-your-token-here
   ```

#### Test PyPI (Empfohlen zum Testen)
1. Account erstellen: https://test.pypi.org/account/register/
2. API Token erstellen: https://test.pypi.org/manage/account/token/
3. Token konfigurieren:
   ```bash
   # ~/.pypirc erweitern
   [testpypi]
   repository = https://test.pypi.org/legacy/
   username = __token__
   password = pypi-your-test-token-here
   ```

### 3. Projektstruktur prüfen
```
pydipapi/
├── pyproject.toml          # ✅ Moderne Konfiguration
├── pydipapi/
│   ├── __init__.py         # ✅ Mit __version__
│   ├── py.typed            # ✅ Typ-Unterstützung
│   └── ...
├── LICENSE                 # ✅ MIT License
├── README.md               # ✅ Beschreibung
└── MANIFEST.in             # ✅ Datei-Inklusion
```

## 🔧 Build-Prozess

### 1. Aufräumen
```bash
rm -rf dist/ build/ *.egg-info
```

### 2. Paket bauen
```bash
python -m build
```

**Output:**
- `dist/pydipapi-1.0.0-py3-none-any.whl` (Wheel)
- `dist/pydipapi-1.0.0.tar.gz` (Source Distribution)

### 3. Validierung
```bash
twine check dist/*
```

**Erwartete Ausgabe:**
```
Checking dist/pydipapi-1.0.0-py3-none-any.whl: PASSED
Checking dist/pydipapi-1.0.0.tar.gz: PASSED
```

## 📤 Veröffentlichung

### Test PyPI (Empfohlen zuerst)
```bash
twine upload --repository testpypi dist/*
```

**Testen der Installation:**
```bash
pip install --index-url https://test.pypi.org/simple/ pydipapi
```

### Production PyPI
```bash
twine upload dist/*
```

**Nach erfolgreicher Veröffentlichung:**
- PyPI-Seite: https://pypi.org/project/pydipapi/
- Installation: `pip install pydipapi`

## 🔄 Versionierung

### Version erhöhen
1. **pyproject.toml** aktualisieren:
   ```toml
   version = "1.0.1"  # Neue Version
   ```

2. **pydipapi/__init__.py** aktualisieren:
   ```python
   __version__ = "1.0.1"  # Gleiche Version
   ```

3. **Changelog** aktualisieren in `docs/changelog.md`

### Versioning-Schema (SemVer)
- **Major (1.x.x)**: Breaking Changes
- **Minor (x.1.x)**: Neue Features (backward compatible)
- **Patch (x.x.1)**: Bug Fixes

## 📊 Checkliste vor Veröffentlichung

### Code-Qualität
- [ ] Alle Tests bestehen: `pytest tests/`
- [ ] Linter-Checks: `ruff check .`
- [ ] Security-Checks: `bandit -r pydipapi/`
- [ ] Typ-Checks: `mypy pydipapi/` (optional)

### Dokumentation
- [ ] README.md aktualisiert
- [ ] CHANGELOG.md aktualisiert
- [ ] API-Dokumentation aktualisiert
- [ ] Beispiele funktionieren

### Paket-Konfiguration
- [ ] Version in pyproject.toml und __init__.py identisch
- [ ] Dependencies korrekt spezifiziert
- [ ] Klassifikatoren aktuell
- [ ] License korrekt

### Build & Test
- [ ] `twine check dist/*` besteht
- [ ] Test-Installation funktioniert
- [ ] Beispiele mit installiertem Paket testen

## 🚨 Häufige Probleme

### "Version already exists"
- Version in pyproject.toml und __init__.py erhöhen
- Bereits veröffentlichte Versionen können nicht überschrieben werden

### "Invalid package metadata"
- `twine check dist/*` für Details ausführen
- pyproject.toml-Format prüfen

### "Authentication failed"
- API-Token prüfen
- ~/.pypirc-Konfiguration überprüfen

### "Package too large"
- MANIFEST.in prüfen
- Unnötige Dateien ausschließen

## 🔍 Nach der Veröffentlichung

### Verifikation
1. **PyPI-Seite besuchen:** https://pypi.org/project/pydipapi/
2. **Installation testen:**
   ```bash
   pip install pydipapi==1.0.0  # Spezifische Version
   python -c "import pydipapi; print(pydipapi.__version__)"
   ```

3. **Funktionalität testen:**
   ```bash
   python -c "from pydipapi import DipAnfrage; print('OK')"
   ```

### Kommunikation
- [ ] GitHub Release erstellen
- [ ] Dokumentation aktualisieren
- [ ] Users über Updates informieren

## 🤖 Automatisierung (Future)

### GitHub Actions (Planned)
```yaml
# .github/workflows/publish.yml
name: Publish to PyPI
on:
  release:
    types: [published]
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: pip install build twine
      - name: Build package
        run: python -m build
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

## 📞 Support

Bei Problemen:
1. [GitHub Issues](https://github.com/lichtbaer/pydipapi/issues)
2. [PyPI Help](https://pypi.org/help/)
3. [Python Packaging Guide](https://packaging.python.org/) 