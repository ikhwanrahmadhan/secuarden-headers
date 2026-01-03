# Secuarden Headers - Quick Start Guide

## Installation

```bash
pip install secuarden-headers
```

## Basic Usage

### Scan a Single URL

```bash
secuarden-headers https://example.com
```

### Scan Multiple URLs

```bash
secuarden-headers https://example.com https://github.com
```

### Scan from File

```bash
secuarden-headers -f urls.txt
```

### Export Results

```bash
# Export to JSON
secuarden-headers https://example.com -o results.json

# Export to CSV
secuarden-headers -f urls.txt -o results.csv
```

## Python API

### Basic Example

```python
from secuarden_headers import SecurityHeaderScanner

scanner = SecurityHeaderScanner()
result = scanner.scan_url("https://example.com")

print(f"Score: {result.security_score}/100")
print(f"Missing: {result.missing_headers}")
```

### Async Example

```python
import asyncio
from secuarden_headers import SecurityHeaderScanner

async def scan():
    scanner = SecurityHeaderScanner()
    result = await scanner.scan_url_async("https://example.com")
    print(f"Score: {result.security_score}/100")

asyncio.run(scan())
```

### Batch Scanning

```python
from secuarden_headers import SecurityHeaderScanner

urls = [
    "https://example.com",
    "https://github.com",
    "https://google.com"
]

scanner = SecurityHeaderScanner()
results = scanner.scan_urls(urls, max_concurrent=5)

for result in results:
    print(f"{result.url}: {result.security_score}/100")
```

## Docker Usage

### Build Image

```bash
docker build -t secuarden-headers .
```

### Run Scanner

```bash
docker run secuarden-headers https://example.com
```

### Scan with File

```bash
docker run -v $(pwd)/urls.txt:/tmp/urls.txt secuarden-headers -f /tmp/urls.txt
```

## Common Options

- `-f, --file PATH` - Input file with URLs
- `-o, --output PATH` - Output file (JSON/CSV)
- `-t, --timeout INTEGER` - Request timeout (default: 10s)
- `-c, --concurrent INTEGER` - Max concurrent requests (default: 10)
- `--no-verify-ssl` - Disable SSL verification
- `-v, --verbose` - Verbose output

## Tips

1. **SSL Issues**: Use `--no-verify-ssl` for self-signed certificates
2. **Timeouts**: Increase timeout with `-t 30` for slow sites
3. **Performance**: Adjust concurrency with `-c 20` for faster scans
4. **Quiet Mode**: Use `--no-banner` to hide the banner

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [examples/](examples/) for more usage examples
- Visit [Secuarden.com](https://secuarden.com) for more security tools

---

**Made with ❤️ by Secuarden**
