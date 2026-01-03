"""
Secuarden Headers - Modern HTTP Security Headers Scanner
A security tool for analyzing HTTP response headers.
"""

__version__ = "2.0.0"
__author__ = "Gaurab Bhattacharjee"
__license__ = "MIT"

from .scanner import SecurityHeaderScanner
from .headers import SecurityHeader, HeaderStatus

__all__ = ["SecurityHeaderScanner", "SecurityHeader", "HeaderStatus"]
