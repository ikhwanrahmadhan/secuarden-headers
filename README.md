# Secuarden Headers

> Modern HTTP Security Headers Scanner for Web Applications

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A powerful, modern Python tool for scanning and analyzing HTTP security headers across web applications. Built by [Secuarden](https://secuarden.com) to help development teams identify and fix security header misconfigurations.

## ✨ Features

- 🚀 **Fast Concurrent Scanning** - Scan multiple URLs simultaneously with async/await
- 🎯 **Modern Security Headers** - Checks for all current best-practice headers including:
  - Content-Security-Policy (CSP)
  - Strict-Transport-Security (HSTS)
  - Permissions-Policy
  - Cross-Origin policies (COOP, COEP, CORP)
  - And more...
- 📊 **Security Scoring** - Get an instant security score (0-100) for each domain
- 🎨 **Beautiful CLI Output** - Rich terminal interface with colors and tables
- 📄 **Multiple Export Formats** - Export results to JSON or CSV
- 🔍 **Detailed Analysis** - Identifies missing, deprecated, and insecure headers
- ⚡ **Easy to Use** - Simple CLI interface and Python API

## 📦 Installation

### Using pip

```bash
pip install secuarden-headers
```

### From source

```bash
git clone https://github.com/gaurabb/secuarden-headers.git
cd secuarden-headers
pip install -e .
```

### Development installation

```bash
git clone https://github.com/gaurabb/secuarden-headers.git
cd secuarden-headers
pip install -e ".[dev]"
pre-commit install
```

## 🚀 Quick Start

### Command Line

Scan a single URL:

```bash
secuarden-headers https://example.com
```

Scan multiple URLs:

```bash
secuarden-headers https://example.com https://google.com
```

Scan URLs from a file:

```bash
secuarden-headers -f urls.txt
```

Export results to JSON:

```bash
secuarden-headers https://example.com -o results.json
```

Export to CSV:

```bash
secuarden-headers -f urls.txt -o results.csv
```

### Python API

```python
from secuarden_headers import SecurityHeaderScanner

# Initialize scanner
scanner = SecurityHeaderScanner(timeout=10)

# Scan a single URL
result = scanner.scan_url("https://example.com")

print(f"Security Score: {result.security_score}/100")
print(f"Missing Headers: {result.missing_headers}")

# Scan multiple URLs concurrently
urls = ["https://example.com", "https://google.com"]
results = scanner.scan_urls(urls, max_concurrent=5)

for result in results:
    print(f"{result.url}: {result.security_score}/100")
```

### Async API

```python
import asyncio
from secuarden_headers import SecurityHeaderScanner

async def main():
    scanner = SecurityHeaderScanner()
    
    # Scan single URL
    result = await scanner.scan_url_async("https://example.com")
    
    # Scan multiple URLs
    urls = ["https://example.com", "https://google.com"]
    results = await scanner.scan_urls_async(urls)
    
    for result in results:
        print(f"{result.url}: {result.security_score}/100")

asyncio.run(main())
```

## 🔧 CLI Options

```
Usage: secuarden-headers [OPTIONS] [URLS]...

Options:
  -f, --file PATH              File containing URLs (one per line)
  -o, --output PATH            Output file (JSON or CSV)
  -t, --timeout INTEGER        Request timeout in seconds (default: 10)
  -c, --concurrent INTEGER     Maximum concurrent requests (default: 10)
  --no-verify-ssl              Disable SSL verification
  --no-follow-redirects        Do not follow redirects
  -v, --verbose                Verbose output
  --no-banner                  Hide banner
  --help                       Show this message and exit
```

## 📋 Checked Headers

### ✅ Recommended Headers

- **Content-Security-Policy** - Controls resource loading and XSS prevention
- **Strict-Transport-Security** - Enforces HTTPS connections
- **X-Frame-Options** - Prevents clickjacking attacks
- **X-Content-Type-Options** - Prevents MIME type sniffing
- **Referrer-Policy** - Controls referrer information
- **Permissions-Policy** - Controls browser features and APIs
- **Cross-Origin-Embedder-Policy** - Controls cross-origin embedding
- **Cross-Origin-Opener-Policy** - Controls cross-origin window interactions
- **Cross-Origin-Resource-Policy** - Controls cross-origin resource loading

### ⚠️ Legacy/Optional Headers

- **X-XSS-Protection** - Deprecated (use CSP instead)
- **X-Download-Options** - IE-specific protection
- **X-Permitted-Cross-Domain-Policies** - Adobe Flash protection

## 📊 Output Examples

### Terminal Output

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ███████╗███████╗ ██████╗██╗   ██╗ █████╗ ██████╗       ║
║   ██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██╔══██╗      ║
║   ███████╗█████╗  ██║     ██║   ██║███████║██████╔╝      ║
║   ╚════██║██╔══╝  ██║     ██║   ██║██╔══██║██╔══██╗      ║
║   ███████║███████╗╚██████╗╚██████╔╝██║  ██║██║  ██║      ║
║   ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝      ║
║                                                           ║
║            HTTP Security Headers Scanner v2.0             ║
║                  by Secuarden.com                         ║
╚═══════════════════════════════════════════════════════════╝

Target: https://example.com
Status: 200
Security Score: 72.5/100

┌─ ✓ Present Security Headers ─────────────────────────┐
│ Header                       Value                    │
├──────────────────────────────────────────────────────┤
│ Content-Security-Policy      default-src 'self'       │
│ X-Content-Type-Options       nosniff                  │
│ X-Frame-Options              DENY                     │
└──────────────────────────────────────────────────────┘

┌─ ✗ Missing Recommended Headers ──────────────────────┐
│ Header                              Description       │
├──────────────────────────────────────────────────────┤
│ Strict-Transport-Security           Enforces HTTPS    │
│ Permissions-Policy                  Controls features │
└──────────────────────────────────────────────────────┘
```

### JSON Output

```json
[
  {
    "url": "https://example.com",
    "status_code": 200,
    "security_score": 72.5,
    "present_headers": {
      "Content-Security-Policy": "default-src 'self'",
      "X-Frame-Options": "DENY"
    },
    "missing_headers": [
      "Strict-Transport-Security",
      "Permissions-Policy"
    ],
    "deprecated_headers": {},
    "insecure_values": {},
    "error": null,
    "scan_time": "2026-01-02T10:30:00"
  }
]
```

## 🧪 Testing

Run the test suite:

```bash
pytest
```

With coverage:

```bash
pytest --cov=secuarden_headers
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Secuarden](https://secuarden.com) - AI-powered application security platform
- [GitHub Repository](https://github.com/gaurabb/secuarden-headers)
- [Issue Tracker](https://github.com/gaurabb/secuarden-headers/issues)

## 🙏 Acknowledgments

- Built with [aiohttp](https://docs.aiohttp.org/) for async HTTP requests
- CLI powered by [Click](https://click.palletsprojects.com/) and [Rich](https://rich.readthedocs.io/)
- Inspired by [securityheaders.com](https://securityheaders.com/)

## 📧 Contact

For questions, feedback, or support:
- Visit [Secuarden.com](https://secuarden.com)
- Open an [issue](https://github.com/gaurabb/secuarden-headers/issues)

---

**Made with ❤️ by [Secuarden](https://secuarden.com)** - Securing applications, one header at a time.
