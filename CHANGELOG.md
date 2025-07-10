# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub Actions workflows for CI/CD and automated publishing
- Dependabot configuration for automated dependency updates
- Comprehensive test coverage and quality checks

## [0.1.1] - 2025-07-10

### Fixed
- **AsyncDipAnfrage**: Fixed critical bugs in async client
  - Fixed `_make_request()` returning `None` for cached data
  - Fixed context manager issues with aiohttp responses
  - Fixed rate limiting compatibility with aiohttp responses
  - Improved error handling and response management
- **Notebooks**: Enhanced and fixed all tutorial notebooks
  - Fixed async problems in `05_async_api_tutorial.ipynb`
  - Added comprehensive error handling and fallback mechanisms
  - Improved performance testing and documentation
  - Updated API key handling across all notebooks

### Enhanced
- **Tutorial Notebooks**: Major improvements to all 6 tutorial notebooks
  - `02_filtering_and_search.ipynb`: Extended with comprehensive search examples
  - `03_batch_operations_and_caching.ipynb`: Enhanced with practical batch examples
  - `04_content_parsers.ipynb`: Added missing `parse_batch` methods and examples
  - `05_async_api_tutorial.ipynb`: Fixed async issues and improved error handling
  - `06_data_visualization.ipynb`: Significantly expanded with extensive visualization examples
- **Code Quality**: Improved type annotations and error handling throughout codebase
- **Documentation**: Updated all examples and documentation to reflect bug fixes

### Technical
- Fixed MockResponse implementation for proper async response handling
- Improved connection management with proper `await response.release()` calls
- Simplified rate limiting logic for better aiohttp compatibility
- Enhanced type safety with `Optional[Any]` return types

## [0.1.0] - 2025-01-XX

### Added
- Initial release of pydipapi
- Basic API client for German Bundestag DIP API
- Async API support with AsyncDipAnfrage
- Content parsers for protocols, documents, persons, and activities
- Batch operations and caching functionality
- Comprehensive documentation and examples
- Jupyter notebooks for tutorials
- Support for Python 3.8+

### Features
- **API Client**: Synchronous and asynchronous clients
- **Content Parsers**: Structured parsing of different content types
- **Caching**: Intelligent caching system for API responses
- **Batch Operations**: Efficient handling of multiple requests
- **Error Handling**: Robust error handling and retry mechanisms
- **Documentation**: Complete API reference and user guides

### Dependencies
- requests >= 2.25.0
- pydantic >= 1.8.0
- aiohttp (for async support)

## [0.0.1] - 2025-01-XX

### Added
- Project initialization
- Basic project structure
- Initial development setup 