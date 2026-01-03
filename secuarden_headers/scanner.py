"""
Main scanner module for HTTP security headers.
"""

import asyncio
import aiohttp
from typing import Dict, List, Optional, Set
from urllib.parse import urlparse
from dataclasses import dataclass, field
from datetime import datetime

from .headers import SECURITY_HEADERS, HeaderStatus, get_recommended_headers


@dataclass
class ScanResult:
    """Result of scanning a single URL."""

    url: str
    status_code: Optional[int] = None
    present_headers: Dict[str, str] = field(default_factory=dict)
    missing_headers: Set[str] = field(default_factory=set)
    deprecated_headers: Dict[str, str] = field(default_factory=dict)
    insecure_values: Dict[str, List[str]] = field(default_factory=dict)
    scan_time: Optional[datetime] = None
    error: Optional[str] = None

    @property
    def is_success(self) -> bool:
        """Check if scan was successful."""
        return self.error is None and self.status_code is not None

    @property
    def security_score(self) -> float:
        """Calculate security score (0-100)."""
        if not self.is_success:
            return 0.0

        recommended = get_recommended_headers()
        total_recommended = len(recommended)

        if total_recommended == 0:
            return 100.0

        present_count = sum(1 for h in recommended.keys() if h in self.present_headers)
        insecure_penalty = len(self.insecure_values) * 5
        deprecated_penalty = len(self.deprecated_headers) * 3

        score = (present_count / total_recommended) * 100
        score = max(0, score - insecure_penalty - deprecated_penalty)

        return round(score, 2)


class SecurityHeaderScanner:
    """Scanner for HTTP security headers."""

    def __init__(
        self,
        timeout: int = 10,
        follow_redirects: bool = True,
        verify_ssl: bool = True,
        user_agent: str = "Secuarden-Headers/2.0",
    ):
        """
        Initialize the scanner.

        Args:
            timeout: Request timeout in seconds
            follow_redirects: Follow HTTP redirects
            verify_ssl: Verify SSL certificates
            user_agent: User agent string
        """
        self.timeout = timeout
        self.follow_redirects = follow_redirects
        self.verify_ssl = verify_ssl
        self.user_agent = user_agent

    def _normalize_url(self, url: str) -> str:
        """Normalize URL by adding scheme if missing."""
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        return url

    def _analyze_headers(self, headers: Dict[str, str]) -> ScanResult:
        """Analyze response headers."""
        result = ScanResult(url="", scan_time=datetime.now())

        # Check for present headers
        for header_name, header_def in SECURITY_HEADERS.items():
            header_value = None

            # Case-insensitive header lookup
            for key, value in headers.items():
                if key.lower() == header_name.lower():
                    header_value = value
                    break

            if header_value:
                result.present_headers[header_name] = header_value

                # Check if deprecated
                if header_def.deprecated:
                    result.deprecated_headers[header_name] = header_value

                # Check for insecure values
                if header_def.bad_values:
                    insecure = []
                    for bad_value in header_def.bad_values:
                        if bad_value.lower() in header_value.lower():
                            insecure.append(bad_value)
                    if insecure:
                        result.insecure_values[header_name] = insecure
            else:
                # Check if missing recommended header
                if header_def.recommended and not header_def.deprecated:
                    result.missing_headers.add(header_name)

        return result

    async def scan_url_async(self, url: str) -> ScanResult:
        """
        Scan a single URL asynchronously.

        Args:
            url: URL to scan

        Returns:
            ScanResult object
        """
        url = self._normalize_url(url)
        result = ScanResult(url=url, scan_time=datetime.now())

        try:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            connector = aiohttp.TCPConnector(ssl=self.verify_ssl)

            async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
                headers = {"User-Agent": self.user_agent}

                async with session.get(
                    url, headers=headers, allow_redirects=self.follow_redirects
                ) as response:
                    result.status_code = response.status

                    # Analyze headers
                    analysis = self._analyze_headers(dict(response.headers))
                    result.present_headers = analysis.present_headers
                    result.missing_headers = analysis.missing_headers
                    result.deprecated_headers = analysis.deprecated_headers
                    result.insecure_values = analysis.insecure_values

        except asyncio.TimeoutError:
            result.error = f"Timeout after {self.timeout}s"
        except aiohttp.ClientSSLError as e:
            result.error = f"SSL error: {str(e)}"
        except aiohttp.ClientError as e:
            result.error = f"Connection error: {str(e)}"
        except Exception as e:
            result.error = f"Unexpected error: {str(e)}"

        return result

    def scan_url(self, url: str) -> ScanResult:
        """
        Scan a single URL synchronously.

        Args:
            url: URL to scan

        Returns:
            ScanResult object
        """
        return asyncio.run(self.scan_url_async(url))

    async def scan_urls_async(self, urls: List[str], max_concurrent: int = 10) -> List[ScanResult]:
        """
        Scan multiple URLs concurrently.

        Args:
            urls: List of URLs to scan
            max_concurrent: Maximum concurrent requests

        Returns:
            List of ScanResult objects
        """
        semaphore = asyncio.Semaphore(max_concurrent)

        async def scan_with_semaphore(url: str) -> ScanResult:
            async with semaphore:
                return await self.scan_url_async(url)

        tasks = [scan_with_semaphore(url) for url in urls]
        return await asyncio.gather(*tasks)

    def scan_urls(self, urls: List[str], max_concurrent: int = 10) -> List[ScanResult]:
        """
        Scan multiple URLs synchronously.

        Args:
            urls: List of URLs to scan
            max_concurrent: Maximum concurrent requests

        Returns:
            List of ScanResult objects
        """
        return asyncio.run(self.scan_urls_async(urls, max_concurrent))
