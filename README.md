# PyDipAPI

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PyPI version](https://badge.fury.io/py/pydipapi.svg)](https://badge.fury.io/py/pydipapi)

**PyDipAPI** is a modern, feature-rich Python client for the German Bundestag (Parliament) API. It provides easy access to parliamentary data including members, documents, protocols, and activities with advanced features like async support, content parsing, and intelligent caching.

## 🚀 Features

- **🔄 Async Support**: High-performance asynchronous API client for concurrent requests
- **📊 Content Parsers**: Extract structured data from parliamentary documents
- **⚡ Intelligent Caching**: Built-in caching with configurable TTL and size limits
- **🔍 Advanced Filtering**: Powerful search and filtering capabilities
- **📦 Batch Operations**: Efficient bulk data retrieval and processing
- **🛡️ Error Handling**: Robust error handling with retry mechanisms
- **📚 Type Safety**: Full type annotations for better IDE support
- **🎯 Easy to Use**: Simple, intuitive API design

## 📦 Installation

```bash
pip install pydipapi
```

## 🏃 Quick Start

### Basic Usage

```python
from pydipapi import DipAnfrage

# Initialize the client
api = DipAnfrage(api_key="your_api_key_here")

# Get members of parliament
members = api.get_person(anzahl=10)
for member in members:
    print(f"{member['vorname']} {member['nachname']} ({member.get('fraktion', 'Unknown')})")

# Get recent documents
documents = api.get_drucksache(anzahl=5)
for doc in documents:
    print(f"Document: {doc['titel']}")
```

### Async Usage

```python
import asyncio
from pydipapi.async_api import AsyncDipAnfrage

async def main():
    async with AsyncDipAnfrage(api_key="your_api_key_here") as api:
        # Parallel requests for better performance
        members, documents, activities = await asyncio.gather(
            api.get_person(anzahl=10),
            api.get_drucksache(anzahl=10),
            api.get_aktivitaet(anzahl=10)
        )
        
        print(f"Retrieved {len(members)} members, {len(documents)} documents, {len(activities)} activities")

asyncio.run(main())
```

### Content Parsing

```python
from pydipapi import DipAnfrage
from pydipapi.parsers import DocumentParser, PersonParser

api = DipAnfrage(api_key="your_api_key_here")

# Parse document content
documents = api.get_drucksache(anzahl=5)
doc_parser = DocumentParser()
parsed_docs = doc_parser.parse_batch(documents)

for doc in parsed_docs:
    print(f"Title: {doc.get('titel')}")
    print(f"Type: {doc.get('dokumenttyp')}")
    print(f"Authors: {', '.join(doc.get('autoren', []))}")

# Parse member information
members = api.get_person(anzahl=10)
person_parser = PersonParser()
parsed_members = person_parser.parse_batch(members)

for member in parsed_members:
    print(f"Name: {member.get('name')}")
    print(f"Party: {member.get('partei')}")
    print(f"Constituency: {member.get('wahlkreis')}")
```

## 📊 Advanced Features

### Intelligent Caching

```python
from pydipapi import DipAnfrage
from pydipapi.util.cache import DipCache

# Configure caching
cache = DipCache(
    max_size=1000,      # Maximum number of cached items
    ttl_seconds=3600    # Cache TTL: 1 hour
)

api = DipAnfrage(api_key="your_api_key_here", cache=cache)

# First call hits the API
members = api.get_person(anzahl=10)

# Second call uses cache (much faster)
members_cached = api.get_person(anzahl=10)

# Check cache statistics
print(f"Cache hits: {cache.hits}")
print(f"Cache misses: {cache.misses}")
print(f"Hit rate: {cache.hit_rate:.2%}")
```

### Advanced Filtering

```python
from datetime import datetime, timedelta

# Filter by date range
start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()

recent_documents = api.get_drucksache(
    datum_start=start_date.strftime("%Y-%m-%d"),
    datum_end=end_date.strftime("%Y-%m-%d"),
    anzahl=50
)

# Filter by electoral period
current_period_docs = api.get_drucksache(
    wahlperiode=20,
    anzahl=100
)

# Complex filtering with multiple parameters
specific_activities = api.get_aktivitaet(
    wahlperiode=20,
    datum_start="2023-01-01",
    anzahl=50
)
```

### Batch Operations

```python
# Efficient batch processing
all_members = []
batch_size = 100

for offset in range(0, 1000, batch_size):
    batch = api.get_person(anzahl=batch_size, offset=offset)
    all_members.extend(batch)
    print(f"Retrieved {len(all_members)} members so far...")

print(f"Total members retrieved: {len(all_members)}")
```

## 🏗️ Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| **Members** | `get_person()` | Retrieve parliament members |
| **Documents** | `get_drucksache()` | Access parliamentary documents |
| **Protocols** | `get_plenarprotokoll()` | Get plenary session protocols |
| **Activities** | `get_aktivitaet()` | Fetch parliamentary activities |
| **Procedures** | `get_vorgang()` | Access legislative procedures |

## 🔧 Content Parsers

PyDipAPI includes specialized parsers for extracting structured data:

- **`ProtocolParser`**: Extract speakers, topics, and interventions from plenary protocols
- **`DocumentParser`**: Parse document metadata, authors, and content summaries
- **`PersonParser`**: Extract member information, parties, and constituencies
- **`ActivityParser`**: Parse voting results, participants, and related documents

## ⚡ Performance Features

### Async Support
- **Concurrent Requests**: Make multiple API calls simultaneously
- **Connection Pooling**: Efficient HTTP connection management
- **Context Managers**: Automatic resource cleanup

### Caching
- **In-Memory Cache**: Fast access to recently requested data
- **Configurable TTL**: Control cache expiration times
- **Size Limits**: Prevent memory overflow with configurable limits

### Error Handling
- **Automatic Retries**: Configurable retry logic for failed requests
- **Rate Limiting**: Respect API rate limits with intelligent backoff
- **Detailed Logging**: Comprehensive logging for debugging

## 📚 Documentation & Examples

### Jupyter Notebooks
Comprehensive tutorials are available in the `notebooks/` directory:

1. **Basic Usage** - Getting started with PyDipAPI
2. **Filtering & Search** - Advanced query techniques
3. **Batch Operations** - Efficient bulk data processing
4. **Content Parsers** - Structured data extraction
5. **Async API** - High-performance async operations
6. **Data Visualization** - Creating charts and dashboards

### Example Scripts
Check the `examples/` directory for practical use cases:
- Basic API usage
- Async implementation
- Content parsing examples
- Advanced filtering techniques

## 🛠️ Development

### Setup Development Environment

```bash
git clone https://github.com/lichtbaer/pydipapi.git
cd pydipapi

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Install development dependencies
pip install pytest pytest-cov ruff bandit
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pydipapi

# Run specific test categories
pytest tests/test_api.py
pytest tests/test_async_api.py
pytest tests/test_parsers.py
```

### Code Quality

```bash
# Linting with Ruff
ruff check .

# Security analysis with Bandit
bandit -r pydipapi/

# Type checking
mypy pydipapi/
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Contribution Guidelines

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Standards

- Write tests for new features
- Follow PEP 8 style guidelines
- Add type annotations
- Update documentation
- Ensure all tests pass

## 📋 Requirements

- **Python**: 3.8 or higher
- **Dependencies**: 
  - `requests >= 2.25.0`
  - `pydantic >= 1.8.0`
  - `aiohttp >= 3.8.0` (for async features)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋 Support

- **Documentation**: [Read the Docs](https://pydipapi.readthedocs.io/)
- **Issues**: [GitHub Issues](https://github.com/lichtbaer/pydipapi/issues)
- **Discussions**: [GitHub Discussions](https://github.com/lichtbaer/pydipapi/discussions)

## 🌟 Acknowledgments

- German Bundestag for providing the public API
- The Python community for excellent libraries and tools
- Contributors who help improve this project

---

**Made with ❤️ for the Python and open government data communities**

[🇩🇪 Deutsche Version](README_DE.md) | [📚 Documentation](https://pydipapi.readthedocs.io/) | [🐛 Report Bug](https://github.com/lichtbaer/pydipapi/issues) | [💡 Request Feature](https://github.com/lichtbaer/pydipapi/issues) 