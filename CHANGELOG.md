# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-01-02

### Added
- Complete rewrite with modern Python 3.10+ features
- Async/await support for concurrent URL scanning
- New security headers:
  - Permissions-Policy
  - Cross-Origin-Embedder-Policy (COEP)
  - Cross-Origin-Opener-Policy (COOP)
  - Cross-Origin-Resource-Policy (CORP)
  - Referrer-Policy
- Security scoring system (0-100 scale)
- Rich CLI interface with colors and tables
- JSON and CSV export options
- Docker support
- Comprehensive test suite with pytest
- GitHub Actions CI/CD pipeline
- Pre-commit hooks for code quality
- Type hints throughout codebase
- Detailed documentation and examples
- Secuarden branding and professional presentation

### Changed
- Migrated from Python 2 to Python 3.10+
- Replaced synchronous requests with aiohttp for better performance
- Modernized package structure and setup
- Updated all dependencies to latest versions
- Improved error handling and reporting
- Enhanced CLI with click and rich libraries

### Deprecated
- X-XSS-Protection header (marked as deprecated, CSP is recommended)

### Removed
- Python 2 support
- Legacy synchronous-only scanning

### Fixed
- Various bugs from original implementation
- SSL verification issues
- Timeout handling improvements

## [1.0.0] - 2016-XX-XX

### Added
- Initial release
- Basic security header scanning
- Support for:
  - Content-Security-Policy
  - X-Frame-Options
  - X-XSS-Protection
  - X-Content-Type-Options
  - Strict-Transport-Security
  - X-Download-Options
  - X-Permitted-Cross-Domain-Policies
- Simple CLI interface
- File-based URL input
- Python 2 support

---

**Note**: Version 1.0.0 was the original release. Version 2.0.0 represents a complete modernization and rebranding for Secuarden.
