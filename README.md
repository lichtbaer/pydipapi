# pydipapi

pydipapi is a Python package that provides a simple and convenient wrapper around the API of the German Bundestag. This package allows developers to easily access various endpoints of the Bundestag's API to retrieve information about legislative processes, documents, and more.



> **Note:** The author is not affiliated with the German Bundestag or any of its institutions.

## Features

- Retrieve information about persons, activities, documents, and plenary protocols.
- Access detailed data on legislative processes and their positions.
- Designed to be easy to use and integrate into your projects.

## Requirements

- An API key is required to use the Bundestag API. You can obtain this key from the German Bundestag.
- Get your API key [here](https://dip.bundestag.de/%C3%BCber-dip/hilfe/api#content).
- Python 3.7 or later.

## Documentation

For more information on the API and how to obtain an API key, please refer to the official documentation.

## License

This project is licensed under the GPLv3 License.

## Installation

It is recommended to use a virtual environment. You can install the package using pip:

```sh
pip install pydipapi
```
## Usage

Here's a quick example of how to use the package:
### Initialize the API

```python
from pydipapi import DipAnfrage

# Initialize with your API key
dip = DipAnfrage(apikey='your_api_key_here')
```
### Example: Retrieve Persons
    
```python
# Retrieve a list of persons
persons = dip.get_person(anzahl=10)
print(persons)
```

### Example:  Retrieve a Single Person by ID

```python
# Retrieve a single person by ID
person = dip.get_person_id(id=7355)
print(person)

{'id': '7355', 'nachname': 'Larem', 'vorname': 'Andreas', 'typ': 'Person', 'wahlperiode': 20, 'aktualisiert': '2022-07-26T19:57:10+02:00', 'titel': 'Andreas Larem, MdB, SPD', 'datum': '2024-09-26', 'basisdatum': '2022-01-27'}
```

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue if you have suggestions for improvements or find any bugs.  

## Contact
For any inquiries, please contact the package author via GitHub.