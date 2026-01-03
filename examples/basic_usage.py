#!/usr/bin/env python3
"""
Example usage of Secuarden Headers scanner.
"""

from secuarden_headers import SecurityHeaderScanner


def example_single_url():
    """Example: Scan a single URL."""
    print("=" * 60)
    print("Example 1: Scanning a single URL")
    print("=" * 60)

    scanner = SecurityHeaderScanner()
    result = scanner.scan_url("https://example.com")

    print(f"\nURL: {result.url}")
    print(f"Status: {result.status_code}")
    print(f"Security Score: {result.security_score}/100")
    print(f"\nPresent Headers: {len(result.present_headers)}")
    for header, value in result.present_headers.items():
        print(f"  - {header}: {value[:50]}...")

    print(f"\nMissing Headers: {len(result.missing_headers)}")
    for header in result.missing_headers:
        print(f"  - {header}")


def example_multiple_urls():
    """Example: Scan multiple URLs concurrently."""
    print("\n" + "=" * 60)
    print("Example 2: Scanning multiple URLs")
    print("=" * 60)

    urls = ["https://example.com", "https://github.com", "https://google.com"]

    scanner = SecurityHeaderScanner(timeout=5)
    results = scanner.scan_urls(urls, max_concurrent=3)

    print(f"\nScanned {len(results)} URLs:")
    for result in results:
        if result.is_success:
            print(f"\n{result.url}")
            print(f"  Score: {result.security_score}/100")
            print(
                f"  Present: {len(result.present_headers)}, Missing: {len(result.missing_headers)}"
            )
        else:
            print(f"\n{result.url}")
            print(f"  Error: {result.error}")


def example_custom_config():
    """Example: Scanner with custom configuration."""
    print("\n" + "=" * 60)
    print("Example 3: Custom scanner configuration")
    print("=" * 60)

    scanner = SecurityHeaderScanner(
        timeout=15, follow_redirects=True, verify_ssl=True, user_agent="MyCustomScanner/1.0"
    )

    result = scanner.scan_url("https://github.com")

    print(f"\nScanned with custom configuration:")
    print(f"URL: {result.url}")
    print(f"Score: {result.security_score}/100")

    if result.deprecated_headers:
        print(f"\nDeprecated headers found:")
        for header in result.deprecated_headers:
            print(f"  - {header}")

    if result.insecure_values:
        print(f"\nInsecure values found:")
        for header, values in result.insecure_values.items():
            print(f"  - {header}: {', '.join(values)}")


if __name__ == "__main__":
    example_single_url()
    example_multiple_urls()
    example_custom_config()

    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
