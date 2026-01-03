"""
Security header definitions and configurations.
"""

from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass


class HeaderStatus(Enum):
    """Status of a security header."""

    PRESENT = "present"
    MISSING = "missing"
    DEPRECATED = "deprecated"
    INSECURE = "insecure"


@dataclass
class SecurityHeader:
    """Definition of a security header."""

    name: str
    description: str
    recommended: bool
    deprecated: bool = False
    reference_url: Optional[str] = None
    good_values: Optional[List[str]] = None
    bad_values: Optional[List[str]] = None


# Modern security headers to check
SECURITY_HEADERS = {
    "Content-Security-Policy": SecurityHeader(
        name="Content-Security-Policy",
        description="Controls resources the browser is allowed to load",
        recommended=True,
        reference_url="https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP",
        bad_values=["unsafe-inline", "unsafe-eval"],
    ),
    "Strict-Transport-Security": SecurityHeader(
        name="Strict-Transport-Security",
        description="Enforces HTTPS connections",
        recommended=True,
        reference_url="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security",
    ),
    "X-Frame-Options": SecurityHeader(
        name="X-Frame-Options",
        description="Prevents clickjacking attacks",
        recommended=True,
        reference_url="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options",
        good_values=["DENY", "SAMEORIGIN"],
    ),
    "X-Content-Type-Options": SecurityHeader(
        name="X-Content-Type-Options",
        description="Prevents MIME type sniffing",
        recommended=True,
        reference_url="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options",
        good_values=["nosniff"],
    ),
    "Referrer-Policy": SecurityHeader(
        name="Referrer-Policy",
        description="Controls referrer information sent with requests",
        recommended=True,
        reference_url="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy",
    ),
    "Permissions-Policy": SecurityHeader(
        name="Permissions-Policy",
        description="Controls browser features and APIs",
        recommended=True,
        reference_url="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy",
    ),
    "Cross-Origin-Embedder-Policy": SecurityHeader(
        name="Cross-Origin-Embedder-Policy",
        description="Controls cross-origin resource embedding",
        recommended=True,
        reference_url="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Embedder-Policy",
    ),
    "Cross-Origin-Opener-Policy": SecurityHeader(
        name="Cross-Origin-Opener-Policy",
        description="Controls cross-origin window interactions",
        recommended=True,
        reference_url="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy",
    ),
    "Cross-Origin-Resource-Policy": SecurityHeader(
        name="Cross-Origin-Resource-Policy",
        description="Controls cross-origin resource loading",
        recommended=True,
        reference_url="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Resource-Policy",
    ),
    "X-Download-Options": SecurityHeader(
        name="X-Download-Options",
        description="Prevents file downloads from opening in the browser context",
        recommended=False,
        reference_url="https://docs.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/compatibility/jj542450(v=vs.85)",
    ),
    "X-Permitted-Cross-Domain-Policies": SecurityHeader(
        name="X-Permitted-Cross-Domain-Policies",
        description="Controls cross-domain policy files",
        recommended=False,
        reference_url="https://www.adobe.com/devnet/adobe-media-server/articles/cross-domain-xml-for-streaming.html",
    ),
    "X-XSS-Protection": SecurityHeader(
        name="X-XSS-Protection",
        description="Legacy XSS filter (deprecated, use CSP instead)",
        recommended=False,
        deprecated=True,
        reference_url="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection",
    ),
}


def get_header_info(header_name: str) -> Optional[SecurityHeader]:
    """Get information about a security header."""
    return SECURITY_HEADERS.get(header_name)


def get_recommended_headers() -> Dict[str, SecurityHeader]:
    """Get all recommended security headers."""
    return {k: v for k, v in SECURITY_HEADERS.items() if v.recommended}
