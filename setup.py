"""
Setup configuration for Secuarden Headers.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="secuarden-headers",
    version="2.0.0",
    author="Gaurab Bhattacharjee",
    author_email="contact@secuarden.com",
    description="Modern HTTP security headers scanner for web applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gaurabb/secuarden-headers",
    project_urls={
        "Bug Reports": "https://github.com/gaurabb/secuarden-headers/issues",
        "Source": "https://github.com/gaurabb/secuarden-headers",
        "Documentation": "https://github.com/gaurabb/secuarden-headers#readme",
        "Secuarden": "https://secuarden.com",
    },
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "aiohttp>=3.9.0",
        "click>=8.1.0",
        "rich>=13.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.12.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
            "pre-commit>=3.6.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "secuarden-headers=secuarden_headers.cli:main",
        ],
    },
    keywords=[
        "security",
        "headers",
        "http",
        "web-security",
        "security-scanner",
        "csp",
        "hsts",
        "secuarden",
        "appsec",
        "devsecops",
    ],
    license="MIT",
    zip_safe=False,
)
