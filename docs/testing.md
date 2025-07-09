# Testing Guide

Diese Seite dokumentiert die Test-Strategie und -Abdeckung von pydipapi.

## Test-Übersicht

pydipapi verwendet eine umfassende Test-Strategie mit verschiedenen Test-Typen:

### Test-Typen

1. **Unit Tests** (`tests/test_api.py`)
   - Testen einzelne Funktionen und Methoden
   - Verwenden Mock-Objekte für externe Abhängigkeiten
   - Schnelle Ausführung

2. **Coverage Tests** (`tests/test_coverage.py`)
   - Testen Edge Cases und Fehlerfälle
   - Verbessern Code-Coverage
   - Testen Error-Handling

3. **Integration Tests** (`tests/test_integration.py`)
   - Testen gegen echte Bundestag API
   - Erfordern gültigen API-Schlüssel
   - Testen reale API-Responses

## Test-Abdeckung

### Aktuelle Coverage (86%)

| Modul | Statements | Missed | Coverage |
|-------|------------|--------|----------|
| `pydipapi/__init__.py` | 10 | 0 | 100% |
| `pydipapi/api.py` | 205 | 75 | 63% |
| `pydipapi/client/base_client.py` | 111 | 19 | 83% |
| `pydipapi/type.py` | 45 | 0 | 100% |
| `pydipapi/util/cache.py` | 56 | 13 | 77% |
| `pydipapi/util/error_handler.py` | 15 | 3 | 80% |
| **Gesamt** | **796** | **113** | **86%** |

### Coverage-Ziele

- **Ziel**: >95% Code-Coverage
- **Aktuell**: 86% Code-Coverage
- **Nächste Schritte**: Erweiterte Tests für `api.py` und `cache.py`

## Test-Ausführung

### Alle Tests ausführen

```bash
# Alle Tests
python -m pytest tests/

# Nur Unit Tests
python -m pytest tests/test_api.py tests/test_coverage.py

# Nur Integration Tests (erfordert API-Key)
python -m pytest tests/test_integration.py
```

### Mit Coverage

```bash
# Coverage messen
coverage run -m pytest tests/test_api.py tests/test_coverage.py

# Coverage-Report anzeigen
coverage report

# HTML-Report generieren
coverage html
```

### Mit API-Key

```bash
# Integration Tests mit API-Key
export DIP_API_KEY='ihr_api_key'
python -m pytest tests/test_integration.py -v
```

## Test-Kategorien

### 1. Unit Tests (`test_api.py`)

#### API-Methoden Tests
```python
def test_get_person(self):
    """Test getting persons from API."""
    # Mock API response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'documents': [{'id': '1', 'name': 'John Doe'}]
    }
    mock_response.status_code = 200
    
    # Test method
    persons = self.dip.get_person(anzahl=1)
    self.assertEqual(len(persons), 1)
    self.assertEqual(persons[0]['name'], 'John Doe')
```

#### Error-Handling Tests
```python
def test_api_error_handling(self):
    """Test API error handling."""
    # Mock HTTP error
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
    
    # Should return empty list on error
    result = self.dip.get_person(anzahl=1)
    self.assertEqual(result, [])
```

#### Cache Tests
```python
def test_cache_functionality(self):
    """Test caching functionality."""
    # Enable cache
    dip = DipAnfrage(api_key='test', enable_cache=True)
    
    # First call should hit API
    persons1 = dip.get_person(anzahl=1)
    
    # Second call should use cache
    persons2 = dip.get_person(anzahl=1)
    self.assertEqual(persons1, persons2)
```

### 2. Coverage Tests (`test_coverage.py`)

#### Edge Cases
```python
def test_empty_response_handling(self):
    """Test handling of empty responses."""
    mock_response = MagicMock()
    mock_response.json.return_value = {'documents': []}
    
    result = self.dip.get_person(anzahl=10)
    self.assertEqual(result, [])
```

#### Error Scenarios
```python
def test_connection_error_handling(self):
    """Test connection error handling."""
    with patch('requests.Session.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()
        
        result = self.dip.get_person(anzahl=1)
        self.assertEqual(result, [])
```

#### Cache Edge Cases
```python
def test_cache_serialization_error(self):
    """Test cache serialization error handling."""
    with patch('json.dump') as mock_dump:
        mock_dump.side_effect = Exception("Serialization error")
        
        # Should not raise exception
        result = dip.get_person(anzahl=1)
        self.assertEqual(result, [])
```

### 3. Integration Tests (`test_integration.py`)

#### Real API Tests
```python
def test_get_person_integration(self):
    """Test getting persons from real API."""
    persons = self.dip.get_person(anzahl=5)
    
    # Should return a list
    self.assertIsInstance(persons, list)
    
    # Should have some results
    if persons:
        person = persons[0]
        self.assertIsInstance(person, dict)
        self.assertIn('id', person)
        self.assertIn('name', person)
```

#### Rate Limiting Tests
```python
def test_rate_limiting_integration(self):
    """Test rate limiting with real API."""
    start_time = time.time()
    
    # Make multiple requests quickly
    for _ in range(3):
        self.dip.get_person(anzahl=1)
    
    end_time = time.time()
    
    # Should take at least 0.2 seconds
    self.assertGreaterEqual(end_time - start_time, 0.2)
```

## Test-Strategie

### 1. Mock-Strategie

#### API-Responses Mocken
```python
# Erfolgreiche Response
mock_response = MagicMock()
mock_response.json.return_value = {
    'documents': [{'id': '1', 'name': 'Test'}],
    'cursor': ''
}
mock_response.status_code = 200

# Fehler-Response
mock_response = MagicMock()
mock_response.status_code = 500
mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
```

#### Session Mocken
```python
@patch('pydipapi.client.base_client.requests.Session.get')
def test_method(self, mock_get):
    mock_get.return_value = mock_response
    # Test method
```

### 2. Error-Handling Tests

#### HTTP-Status-Codes
- **200**: Erfolgreiche Response
- **400**: Bad Request
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Not Found
- **429**: Rate Limited
- **500**: Server Error

#### Exception-Typen
- `requests.exceptions.ConnectionError`
- `requests.exceptions.Timeout`
- `requests.exceptions.SSLError`
- `requests.exceptions.HTTPError`

### 3. Cache-Tests

#### Cache-Verhalten
- Cache-Hit vs Cache-Miss
- Cache-Invalidierung
- Cache-Serialization-Fehler
- Cache-TTL-Tests

## Test-Daten

### Mock-Daten

```python
# Personen-Daten
PERSON_DATA = {
    'id': '11000001',
    'name': 'Test Person',
    'wahlperiode': 20
}

# Dokument-Daten
DOCUMENT_DATA = {
    'id': '11000001',
    'titel': 'Test Document',
    'drucksachetyp': 'Antrag'
}

# Aktivitäts-Daten
ACTIVITY_DATA = {
    'id': '11000001',
    'titel': 'Test Activity',
    'datum': '2024-01-01'
}
```

### Test-IDs

```python
# Bekannte Test-IDs
TEST_PERSON_ID = 11000001
TEST_DOCUMENT_ID = 11000001
TEST_ACTIVITY_ID = 11000001
```

## Continuous Integration

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest coverage
      - name: Run tests
        run: |
          python -m pytest tests/test_api.py tests/test_coverage.py
      - name: Generate coverage report
        run: |
          coverage run -m pytest tests/test_api.py tests/test_coverage.py
          coverage report
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.4
    hooks:
      - id: ruff
        args: [--fix]
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.8
    hooks:
      - id: bandit
        args: [-r, pydipapi/]
```

## Test-Best-Practices

### 1. Test-Struktur

```python
class TestDipAnfrage(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.dip = DipAnfrage(api_key='test_key')
    
    def test_method_name(self):
        """Test description."""
        # Arrange
        # Act
        # Assert
```

### 2. Mocking-Best-Practices

```python
# Gute Praxis: Spezifische Mocks
@patch('pydipapi.client.base_client.requests.Session.get')
def test_method(self, mock_get):
    # Mock setup
    mock_get.return_value = mock_response
    
    # Test execution
    result = self.dip.get_person(anzahl=1)
    
    # Assertions
    self.assertEqual(len(result), 1)
```

### 3. Error-Testing

```python
# Testen von Fehlerfällen
def test_error_scenario(self):
    """Test error scenario."""
    with patch('requests.Session.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()
        
        # Should handle error gracefully
        result = self.dip.get_person(anzahl=1)
        self.assertEqual(result, [])
```

## Coverage-Verbesserung

### Aktuelle Lücken

1. **api.py (63% Coverage)**
   - Einige Convenience-Methoden nicht getestet
   - Edge Cases bei Pagination
   - Spezielle Filter-Kombinationen

2. **cache.py (77% Coverage)**
   - Cache-Invalidierung
   - Cache-Datei-Fehler
   - Cache-Schlüssel-Generierung

### Nächste Schritte

1. **Erweiterte Unit Tests**
   - Alle Convenience-Methoden testen
   - Pagination-Edge-Cases
   - Filter-Kombinationen

2. **Cache-Tests erweitern**
   - Cache-Invalidierung
   - Cache-Datei-Operationen
   - Cache-Performance

3. **Integration Tests**
   - Echte API-Tests mit API-Key
   - Rate-Limiting-Tests
   - Performance-Tests

## Test-Automatisierung

### Lokale Entwicklung

```bash
# Automatische Tests bei Änderungen
watchmedo auto-restart --patterns="*.py" --recursive -- python -m pytest tests/

# Coverage bei jedem Commit
pre-commit run --all-files
```

### CI/CD Pipeline

```yaml
# Automatische Tests bei Push/PR
- name: Run tests
  run: python -m pytest tests/ -v

- name: Generate coverage
  run: |
    coverage run -m pytest tests/test_api.py tests/test_coverage.py
    coverage report --fail-under=85
```

## Debugging Tests

### Test-Ausgabe

```bash
# Verbose Ausgabe
python -m pytest tests/ -v

# Mit Print-Statements
python -m pytest tests/ -s

# Spezifischen Test ausführen
python -m pytest tests/test_api.py::TestDipAnfrage::test_get_person -v
```

### Coverage-Analyse

```bash
# HTML-Report öffnen
coverage html
open htmlcov/index.html

# Spezifische Datei analysieren
coverage report --include="pydipapi/api.py"
```

## Fazit

Die Test-Strategie von pydipapi bietet:

- **86% Code-Coverage** (Ziel: >95%)
- **Umfassende Unit Tests** für alle Hauptfunktionen
- **Coverage Tests** für Edge Cases und Fehlerfälle
- **Integration Tests** für echte API-Interaktion
- **Automatisierte CI/CD** Pipeline
- **Pre-commit Hooks** für Code-Qualität

Die Tests sind modular aufgebaut und können einfach erweitert werden. Das Ziel ist eine 95%+ Code-Coverage vor dem 1.0.0 Release. 