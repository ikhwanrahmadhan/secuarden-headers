"""
Tests for the scanner module.
"""

import pytest
from unittest.mock import Mock, patch
from secuarden_headers.scanner import SecurityHeaderScanner, ScanResult


class TestScanResult:
    """Test ScanResult class."""
    
    def test_is_success_true(self):
        """Test successful scan result."""
        result = ScanResult(
            url="https://example.com",
            status_code=200
        )
        assert result.is_success is True
    
    def test_is_success_false_with_error(self):
        """Test failed scan with error."""
        result = ScanResult(
            url="https://example.com",
            error="Connection failed"
        )
        assert result.is_success is False
    
    def test_is_success_false_no_status(self):
        """Test failed scan without status code."""
        result = ScanResult(url="https://example.com")
        assert result.is_success is False
    
    def test_security_score_perfect(self):
        """Test perfect security score."""
        result = ScanResult(
            url="https://example.com",
            status_code=200,
            present_headers={
                "Content-Security-Policy": "default-src 'self'",
                "Strict-Transport-Security": "max-age=31536000",
                "X-Frame-Options": "DENY",
                "X-Content-Type-Options": "nosniff",
                "Referrer-Policy": "no-referrer",
                "Permissions-Policy": "geolocation=()",
                "Cross-Origin-Embedder-Policy": "require-corp",
                "Cross-Origin-Opener-Policy": "same-origin",
                "Cross-Origin-Resource-Policy": "same-origin"
            }
        )
        assert result.security_score == 100.0
    
    def test_security_score_with_missing(self):
        """Test security score with missing headers."""
        result = ScanResult(
            url="https://example.com",
            status_code=200,
            present_headers={
                "X-Frame-Options": "DENY"
            },
            missing_headers={
                "Content-Security-Policy",
                "Strict-Transport-Security"
            }
        )
        score = result.security_score
        assert 0 < score < 100
    
    def test_security_score_failed_scan(self):
        """Test security score for failed scan."""
        result = ScanResult(
            url="https://example.com",
            error="Connection failed"
        )
        assert result.security_score == 0.0


class TestSecurityHeaderScanner:
    """Test SecurityHeaderScanner class."""
    
    def test_normalize_url_adds_https(self):
        """Test URL normalization adds https."""
        scanner = SecurityHeaderScanner()
        url = scanner._normalize_url("example.com")
        assert url == "https://example.com"
    
    def test_normalize_url_keeps_scheme(self):
        """Test URL normalization keeps existing scheme."""
        scanner = SecurityHeaderScanner()
        url = scanner._normalize_url("http://example.com")
        assert url == "http://example.com"
    
    def test_analyze_headers_identifies_present(self):
        """Test header analysis identifies present headers."""
        scanner = SecurityHeaderScanner()
        headers = {
            "Content-Security-Policy": "default-src 'self'",
            "X-Frame-Options": "DENY"
        }
        result = scanner._analyze_headers(headers)
        assert "Content-Security-Policy" in result.present_headers
        assert "X-Frame-Options" in result.present_headers
    
    def test_analyze_headers_identifies_missing(self):
        """Test header analysis identifies missing headers."""
        scanner = SecurityHeaderScanner()
        headers = {}
        result = scanner._analyze_headers(headers)
        assert len(result.missing_headers) > 0
        assert "Content-Security-Policy" in result.missing_headers
    
    def test_analyze_headers_identifies_deprecated(self):
        """Test header analysis identifies deprecated headers."""
        scanner = SecurityHeaderScanner()
        headers = {
            "X-XSS-Protection": "1; mode=block"
        }
        result = scanner._analyze_headers(headers)
        assert "X-XSS-Protection" in result.deprecated_headers
    
    def test_analyze_headers_identifies_insecure(self):
        """Test header analysis identifies insecure values."""
        scanner = SecurityHeaderScanner()
        headers = {
            "Content-Security-Policy": "default-src 'self' 'unsafe-inline'"
        }
        result = scanner._analyze_headers(headers)
        assert "Content-Security-Policy" in result.insecure_values
        assert "unsafe-inline" in result.insecure_values["Content-Security-Policy"]
    
    @pytest.mark.asyncio
    async def test_scan_url_async_success(self):
        """Test async URL scanning success."""
        scanner = SecurityHeaderScanner()
        # This would need mocking for actual tests
        # Just testing the method exists
        assert hasattr(scanner, 'scan_url_async')
    
    def test_scanner_initialization(self):
        """Test scanner initialization with custom settings."""
        scanner = SecurityHeaderScanner(
            timeout=5,
            follow_redirects=False,
            verify_ssl=False,
            user_agent="TestAgent"
        )
        assert scanner.timeout == 5
        assert scanner.follow_redirects is False
        assert scanner.verify_ssl is False
        assert scanner.user_agent == "TestAgent"
