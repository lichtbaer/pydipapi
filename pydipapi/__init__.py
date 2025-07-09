"""
pydipapi - Python client for the German Bundestag API

A comprehensive Python wrapper for the German Bundestag API,
providing easy access to parliamentary data including documents,
members, activities, and protocols.
"""

from .api import DipAnfrage
from .async_api import AsyncDipAnfrage
from .client.base_client import BaseApiClient
from .client.async_client import AsyncBaseApiClient
from .parsers import (
    BaseParser,
    DocumentParser,
    PersonParser,
    ActivityParser,
    ProtocolParser,
)

__version__ = "0.3.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    "DipAnfrage",
    "AsyncDipAnfrage", 
    "BaseApiClient",
    "AsyncBaseApiClient",
    "BaseParser",
    "DocumentParser",
    "PersonParser",
    "ActivityParser",
    "ProtocolParser",
]
