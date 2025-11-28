# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub Actions workflows for CI/CD and automated publishing
- Dependabot configuration for automated dependency updates
- Comprehensive test coverage and quality checks

## [0.1.0] - 2024-01-XX

### Added
- Initial release of pydipapi
- Basic API client for German Bundestag DIP API
- Async API support with AsyncDipAnfrage
- Content parsers for protocols, documents, persons, and activities
- Batch operations and caching functionality
- Comprehensive documentation and examples
- Jupyter notebooks for tutorials
- Support for Python 3.10+

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

## [0.0.1] - 2024-01-XX

### Added
- Project initialization
- Basic project structure
- Initial development setup 