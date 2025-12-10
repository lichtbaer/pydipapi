# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Typed Methods for Protocols and Proceedings** - `get_plenarprotokoll_typed()` and `get_vorgang_typed()` methods added to both sync and async APIs
- **Vorgang Model** - New typed model for legislative processes

### Fixed
- **Version Synchronization** - Fixed version inconsistency between `__init__.py` and `pyproject.toml`
- **Missing Import** - Added missing `json` import in `async_api.py`

## [0.3.0] - 2025-12-10

### Added
- **Content Parsers** - Complete parser suite for structured data analysis
  - **ProtocolParser** - Extracts information from full-text plenary protocols
  - **DocumentParser** - Analyzes documents and other materials
  - **PersonParser** - Processes member of parliament data
  - **ActivityParser** - Extracts information from activities
- **Async Support** - Asynchronous API calls for better performance
- **Extended Regex Patterns** - Useful extraction methods for all parsers
- **Batch Parsing** - Parse multiple objects in a single call
- **Complete Parser Documentation** - Detailed guide for all parsers

### Changed
- **Project Structure** - New `pydipapi.parsers` module structure
- **Import Structure** - Parsers are now directly importable from `pydipapi`
- **Documentation** - New content parser section with examples

### Improved
- **Performance** - Optimized regex patterns for better extraction
- **Code Quality** - Comprehensive tests for all parsers
- **Developer Experience** - Easy parser integration

## [1.0.0] - 2024-12-19

### Added
- **Complete API Coverage** - All Bundestag API endpoints implemented
- **Batch Operations** - Retrieve multiple IDs in a single call
- **Intelligent Caching** - File-based caching with TTL
- **Rate Limiting** - Configurable delays between requests
- **Retry Logic** - Automatic retry on errors
- **Convenience Methods** - Simple queries for common use cases
- **Flexible Filtering** - Comprehensive search and filter options
- **Complete Documentation** - Detailed API reference and examples
- **Jupyter Notebooks** - Interactive examples and tutorials
- **Pre-Commit Hooks** - Automatic code quality checks
- **CI/CD Pipeline** - Automated tests and deployment
- **MkDocs Integration** - Professional documentation website

### Changed
- **Project Structure** - Modular architecture with separate client and utility modules
- **Error Handling** - Improved error handling with specific exception types
- **Caching Implementation** - SHA256-based cache keys instead of MD5
- **API Response Parsing** - More robust parsing of API responses
- **Documentation** - Completely revised and extended documentation

### Improved
- **Performance** - Optimized batch operations and caching
- **Code Quality** - Ruff and Bandit integration for linting and security
- **Developer Experience** - Comprehensive developer documentation
- **Examples** - Practical examples and tutorials

### Fixed
- **Security Vulnerabilities** - Replaced MD5 with SHA256 for cache keys
- **Linting Errors** - Fixed all Ruff and Bandit warnings
- **Import Errors** - Correct import structure implemented
- **Documentation Errors** - Updated and corrected documentation

## [0.2.0] - 2024-12-18

### Added
- **Batch Operations** - `get_person_ids()`, `get_drucksache_ids()`, etc.
- **Convenience Methods** - `search_documents()`, `get_recent_activities()`, etc.
- **Caching System** - File-based caching with TTL
- **Rate Limiting** - Configurable delays
- **Filter Mapping Table** - Comprehensive documentation of all filter parameters
- **Extended Documentation** - API reference and developer guide

### Changed
- **Project Structure** - Modular architecture
- **Error Handling** - Improved error handling
- **Documentation** - Extended and improved documentation

## [0.1.0] - 2024-12-17

### Added
- **Basic API Functionality** - Retrieve persons, activities, documents
- **Simple Client Class** - `DipAnfrage` for API access
- **Basic Documentation** - README and basic guide
- **Requirements File** - Dependencies defined
- **Setup.py** - Package configuration

### Features
- `get_person()` - Retrieve persons
- `get_aktivitaet()` - Retrieve activities
- `get_drucksache()` - Retrieve documents
- `get_plenarprotokoll()` - Retrieve protocols
- `get_vorgang()` - Retrieve proceedings
- `get_vorgangsposition()` - Retrieve proceeding positions 