# Bug Report und Technische Schulden - PyDipAPI

## Kritische Bugs

### 1. **KRITISCH: Async Response Context Manager Bug** 
**Dateien:** 
- `pydipapi/client/async_client.py:130-200` (Bug)
- `pydipapi/async_api.py:76` (Verwendung der geschlossenen Response)

**Problem:** Die `response` wird innerhalb eines `async with` Context Managers zurückgegeben. Sobald der Context Manager verlassen wird, wird die Response geschlossen, bevor sie verwendet werden kann.

```python
# async_client.py:130-200
async with session.get(url, params=params) as response:
    # ... processing ...
    return response  # ❌ Response wird geschlossen, bevor sie verwendet werden kann

# async_api.py:76 - wird NACH dem Context Manager aufgerufen
data = await response.json()  # ❌ Response ist bereits geschlossen!
```

**Auswirkung:** Alle async API-Aufrufe schlagen fehl mit einem Fehler wie "Cannot read from closed response" oder ähnlich, da die Response bereits geschlossen ist, wenn `response.json()` aufgerufen wird.

**Bestätigung:** Der Bug ist reproduzierbar:
1. `_make_request()` gibt `response` zurück (Zeile 200)
2. Context Manager schließt die Response
3. `_request_json()` ruft `response.json()` auf (Zeile 76)
4. Response ist bereits geschlossen → Fehler

**Lösung:** Response-Daten müssen vor dem Verlassen des Context Managers gelesen und in einem Wrapper-Objekt gespeichert werden, oder die gesamte Logik muss umstrukturiert werden.

---

### 2. **State Management Bug: Geteilter Instanz-State**
**Datei:** `pydipapi/api.py:53`

**Problem:** `self.documents` wird als Instanz-Variable verwendet und von mehreren Methoden überschrieben. Dies kann zu Race Conditions und unerwartetem Verhalten führen, wenn Methoden nacheinander aufgerufen werden.

**Betroffene Methoden:**
- `get_person_ids()` (Zeile 180)
- `get_aktivitaet_ids()` (Zeile 199)
- `get_drucksache_ids()` (Zeile 219)
- `get_plenarprotokoll_ids()` (Zeile 240)
- `get_vorgang_ids()` (Zeile 260)
- `get_vorgangsposition_ids()` (Zeile 279)
- `search_documents()` (Zeile 302)

**Auswirkung:** Wenn mehrere Methoden nacheinander aufgerufen werden, überschreiben sie sich gegenseitig die `self.documents` Variable.

**Lösung:** Lokale Variablen statt Instanz-Variablen verwenden.

---

## Inkonsistenzen zwischen Sync und Async API

### 3. **Inkonsistente Filter-Parameter in get_recent_activities()**
**Dateien:** 
- `pydipapi/api.py:331-332` (sync)
- `pydipapi/async_api.py:318-319` (async)

**Problem:** 
- Sync-Version verwendet: `aktualisiert_start` und `aktualisiert_end`
- Async-Version verwendet: `datum_von` und `datum_bis`

**Auswirkung:** Unterschiedliches Verhalten zwischen sync und async Versionen.

---

### 4. **Inkonsistenter Endpoint in search_documents()**
**Dateien:**
- `pydipapi/api.py:304` (sync) - verwendet `"drucksache"`
- `pydipapi/async_api.py:291` (async) - verwendet `"search"`

**Problem:** Unterschiedliche Endpoints führen zu unterschiedlichen Ergebnissen.

**Auswirkung:** Sync und async Versionen liefern möglicherweise unterschiedliche Ergebnisse.

---

### 5. **Inkonsistente Filter-Parameter in get_documents_by_type()**
**Dateien:**
- `pydipapi/api.py:367` (sync) - verwendet `drucksachetyp`
- `pydipapi/async_api.py:361` (async) - verwendet `dokumentart`

**Problem:** Unterschiedliche Parameter-Namen für denselben Filter.

---

## Konfigurationsprobleme

### 6. **Python Version Inkonsistenz**
**Dateien:**
- `README.md:3, 357` - sagt "Python 3.8+"
- `pyproject.toml:11` - erfordert `requires-python = ">=3.10"`
- `.github/workflows/ci.yml:56` - testet nur 3.10, 3.11, 3.12

**Problem:** Dokumentation verspricht Python 3.8+, aber Code erfordert 3.10+.

**Auswirkung:** Benutzer mit Python 3.8/3.9 können das Paket nicht installieren.

---

### 7. **Placeholder-Autoren-Information**
**Datei:** `pydipapi/__init__.py:37-38`

**Problem:**
```python
__author__ = "Your Name"
__email__ = "your.email@example.com"
```

**Auswirkung:** Falsche Metadaten im Paket.

**Lösung:** Sollte mit `pyproject.toml` übereinstimmen (Johannes Gegenheimer).

---

## Code-Duplikation und Technische Schulden

### 8. **Zwei Error-Handling-Dateien**
**Dateien:**
- `pydipapi/util/error_handler.py` - wird aktiv verwendet
- `pydipapi/util/error_handling.py` - wird auch verwendet, aber weniger

**Problem:** Überlappende Funktionalität:
- `error_handler.py`: `handle_api_error`, `is_rate_limited`, `should_retry`
- `error_handling.py`: `DipApiError`, `DipApiHttpError`, `DipApiConnectionError`, `handle_api_response`, `validate_api_key`

**Auswirkung:** Verwirrung, welche Funktionen verwendet werden sollen. Potenzielle Wartungsprobleme.

**Lösung:** Konsolidierung in eine Datei oder klare Trennung der Verantwortlichkeiten.

---

### 9. **MyPy Type Checking deaktiviert für Parsers**
**Datei:** `pyproject.toml:184-186`

**Problem:**
```toml
[[tool.mypy.overrides]]
module = ["pydipapi.parsers.*"]
ignore_errors = true
```

**Auswirkung:** Type-Checking-Fehler in den Parsers werden ignoriert. Technische Schuld.

---

### 10. **MyPy Type Checking teilweise deaktiviert für API-Module**
**Datei:** `pyproject.toml:188-190`

**Problem:**
```toml
[[tool.mypy.overrides]]
module = ["pydipapi.api", "pydipapi.async_api"]
disable_error_code = ["type-arg", "no-untyped-def", "return-value"]
```

**Auswirkung:** Wichtige Type-Checking-Fehler werden ignoriert.

---

## Potenzielle Probleme

### 11. **Cache-Implementierung: Fehlende Fehlerbehandlung**
**Datei:** `pydipapi/util/cache.py`

**Problem:** 
- Cache-Verzeichnis wird mit `.cache` als Standard erstellt (Zeile 18)
- Keine Validierung, ob Schreibrechte vorhanden sind
- Keine Behandlung von Race Conditions beim gleichzeitigen Zugriff

**Auswirkung:** Potenzielle Fehler in Umgebungen ohne Schreibrechte oder bei parallelen Zugriffen.

---

### 12. **Fehlende Validierung in _build_url()**
**Dateien:**
- `pydipapi/client/base_client.py:182-210`
- `pydipapi/client/async_client.py:227-255`

**Problem:** URL-Parameter werden nicht URL-encoded. Spezielle Zeichen in Parametern könnten zu ungültigen URLs führen.

**Beispiel:**
```python
url = f"{key}={value}"  # ❌ Kein URL-Encoding
```

**Lösung:** `urllib.parse.urlencode()` verwenden.

---

### 13. **Exception Handling zu breit**
**Dateien:** Mehrere Stellen, z.B.:
- `pydipapi/api.py:151-153` - `except Exception` fängt alle Exceptions
- `pydipapi/async_api.py:120-122` - `except Exception` fängt alle Exceptions

**Problem:** Zu breite Exception-Handler verbergen echte Fehler.

**Auswirkung:** Schwierige Fehlerdiagnose.

---

### 14. **Fehlende Timeout-Konfiguration**
**Datei:** `pydipapi/client/base_client.py:99`

**Problem:** Timeout ist hardcoded auf 30 Sekunden, nicht konfigurierbar.

**Auswirkung:** Keine Flexibilität für langsame Netzwerke oder große Requests.

---

## Zusammenfassung

### Kritische Bugs (sofort beheben)
1. ✅ Async Response Context Manager Bug
2. ✅ State Management mit `self.documents`

### Wichtige Inkonsistenzen (beheben)
3. ✅ Filter-Parameter in `get_recent_activities()`
4. ✅ Endpoint in `search_documents()`
5. ✅ Filter-Parameter in `get_documents_by_type()`

### Konfigurationsprobleme (beheben)
6. ✅ Python Version Inkonsistenz
7. ✅ Placeholder-Autoren-Info

### Technische Schulden (refactoring)
8. ✅ Zwei Error-Handling-Dateien
9. ✅ MyPy Type Checking deaktiviert
10. ✅ URL-Encoding fehlt
11. ✅ Zu breite Exception Handler
12. ✅ Fehlende Timeout-Konfiguration

---

**Gesamt:** 14 identifizierte Probleme
- 2 kritische Bugs
- 3 wichtige Inkonsistenzen
- 2 Konfigurationsprobleme
- 7 technische Schulden/Potenzielle Probleme
