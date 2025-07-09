# Usage Guide

## Installation

Install the package and dependencies in your virtual environment:

```sh
pip install -r requirements.txt
```

## Quickstart

```python
from pydipapi import DipAnfrage

dip = DipAnfrage(api_key='your_api_key_here')
persons = dip.get_person(anzahl=10)
print(persons)
```

## Endpoints
- Persons
- Activities
- Documents
- Plenary Protocols
- Legislative Processes

See the API Reference for details. 