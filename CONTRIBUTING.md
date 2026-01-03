# Contributing to Secuarden Headers

Thank you for your interest in contributing to Secuarden Headers! This document provides guidelines and instructions for contributing.

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow. Please be respectful and constructive in all interactions.

## Getting Started

### Development Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/secuarden-headers.git
   cd secuarden-headers
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

5. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Making Changes

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

3. Ensure your code passes all tests:
   ```bash
   pytest
   ```

4. Ensure your code follows the style guidelines:
   ```bash
   black secuarden_headers
   flake8 secuarden_headers
   mypy secuarden_headers
   ```

### Running Tests

Run the full test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=secuarden_headers
```

Run specific test file:
```bash
pytest tests/test_scanner.py
```

### Code Style

We use the following tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

Pre-commit hooks will automatically check these before each commit.

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update tests to cover your changes
3. Ensure all tests pass and code style checks pass
4. Update the version number following [Semantic Versioning](https://semver.org/)
5. Submit a pull request with a clear description of the changes

### Pull Request Guidelines

- Keep pull requests focused on a single feature or bugfix
- Write clear, descriptive commit messages
- Add tests for new functionality
- Update documentation as needed
- Ensure CI checks pass

## Reporting Bugs

When reporting bugs, please include:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Python version and OS
- Any relevant logs or error messages

## Feature Requests

We welcome feature requests! Please:

- Check if the feature has already been requested
- Provide a clear use case
- Explain why the feature would be valuable
- Be open to discussion and feedback

## Questions?

If you have questions about contributing, please open an issue with the `question` label.

## License

By contributing to Secuarden Headers, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Secuarden Headers! 🚀
