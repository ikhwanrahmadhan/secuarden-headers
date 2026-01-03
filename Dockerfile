FROM python:3.11-slim

LABEL maintainer="Gaurab Bhattacharjee <contact@secuarden.com>"
LABEL description="Secuarden Headers - Modern HTTP Security Headers Scanner"
LABEL version="2.0.0"

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY secuarden_headers/ ./secuarden_headers/
COPY setup.py README.md LICENSE ./

# Install the package
RUN pip install --no-cache-dir .

# Create non-root user
RUN useradd -m -u 1000 scanner && \
    chown -R scanner:scanner /app

USER scanner

# Set entrypoint
ENTRYPOINT ["secuarden-headers"]
CMD ["--help"]
