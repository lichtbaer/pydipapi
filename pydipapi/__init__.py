"""
PyDipAPI - Modern Python client for the German Bundestag API

This package provides a comprehensive, high-performance client for accessing
the German Bundestag API (DIP) with features like batch operations, intelligent
caching, rate limiting, and extensive filtering capabilities.

Features:
- Complete API coverage for all Bundestag endpoints
- Batch operations for efficient data retrieval
- Intelligent caching with configurable TTL
- Rate limiting with exponential backoff
- Comprehensive error handling and retry logic
- Extensive filtering and search capabilities
- Type hints and full documentation

Example:
    >>> from pydipapi import DipAnfrage
    >>> client = DipAnfrage(api_key='your_api_key')
    >>> documents = client.get_drucksache(anzahl=10)
    >>> persons = client.get_person(anzahl=5)
"""

from .api import DipAnfrage
from .type import Vorgangsbezug, Vorgangspositionbezug

__version__ = "0.1.0"
__author__ = "Johannes Gegenheimer"
__email__ = "jg@politikpraxis.de"
__license__ = "MIT"
__description__ = "Modern Python client for the German Bundestag API"
__url__ = "https://github.com/lichtbaer/pydipapi"
__documentation__ = "https://lichtbaer.github.io/pydipapi/"

# Public API
__all__ = [
    "DipAnfrage",
    "Vorgangsbezug",
    "Vorgangspositionbezug",
    "__version__",
]
