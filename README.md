# pydipapi

pydipapi is a Python package that provides a simple and convenient wrapper around the API of the German Bundestag. This package allows developers to easily access various endpoints of the Bundestag's API to retrieve information about legislative processes, documents, and more.

> **Note:** The author is not affiliated with the German Bundestag or any of its institutions.

## Features
- Retrieve information about persons, activities, documents, and plenary protocols.
- Access detailed data on legislative processes and their positions.
- Designed to be easy to use and integrate into your projects.

## Documentation
The full documentation is available at [docs/](docs/index.md) and can be built locally with [MkDocs](https://www.mkdocs.org/):

```sh
mkdocs serve
```

- [Usage Guide](docs/usage.md)
- [API Reference](docs/api_reference.md)
- [OpenAPI Spec](docs/openapi.md)
- [Developer Guide](docs/development.md)
- [Changelog](docs/changelog.md)

## Requirements
- An API key is required to use the Bundestag API. You can obtain this key from the German Bundestag.
- Get your API key [here](https://dip.bundestag.de/%C3%BCber-dip/hilfe/api#content).
- Python 3.7 or later.

## Installation
It is recommended to use a virtual environment. You can install the package using pip:

```sh
pip install -r requirements.txt
```

## Usage
Here's a quick example of how to use the package:

```python
from pydipapi import DipAnfrage

dip = DipAnfrage(api_key='your_api_key_here')
persons = dip.get_person(anzahl=10)
print(persons)
```

## Contributing
Contributions are welcome! Please see [docs/development.md](docs/development.md) for guidelines.

## License
This project is licensed under the GPLv3 License.

## Contact
For any inquiries, please contact the package author via GitHub.