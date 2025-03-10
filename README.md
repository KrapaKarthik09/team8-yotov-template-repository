# Python Template Repository

A comprehensive Python template repository following best practices for software development. This template includes integrated testing, static analysis, code formatting, and CI/CD pipelines.

## Features

- **Complete Project Structure**: Well-organized directory structure for maintainability and scalability
- **Component-Based Architecture**: Modular components with clear interfaces
- **Testing Suite**: Unit, integration, and end-to-end tests with pytest
- **Static Analysis**: Type checking with mypy and linting with ruff
- **Dependency Management**: Modern package management with UV
- **CI/CD**: Continuous integration with CircleCI
- **Code Coverage**: Test coverage tracking and reporting

## Directory Structure
```
.
├── calculator/             # Calculator component
│   └── src/                # Source code directory
│       └── calculator/     # Implementation
│           ├── __init__.py # Component API
│           ├── calculator.py # Implementation
│           ├── tests/      # Unit tests for calculator
│           ├── pyproject.toml # Component dependencies
│           └── uv.lock     # Dependency lock file
├── logger/                 # Logger component
│   └── src/
│       └── logger/
│           ├── __init__.py
│           ├── logger.py
│           ├── tests/
│           ├── pyproject.toml
│           └── uv.lock
├── notifier/               # Notifier component
│   └── src/
│       └── notifier/
│           ├── __init__.py
│           ├── notifier.py
│           ├── tests/
│           ├── pyproject.toml
│           └── uv.lock
├── tests/                  # Top-level tests
│   ├── integration/        # Integration tests between components
│   └── e2e/                # End-to-end tests
├── .circleci/              # CircleCI configuration
├── .github/                # GitHub templates
│   ├── ISSUE_TEMPLATE/     # Issue templates
│   │   ├── bug_report.md   # Bug report template
│   │   └── feature_request.md  # Feature request template
│   └── pull_request_template.md
├── pyproject.toml          # Project configuration
├── component.md            # Component documentation
├── LICENSE                 # Open source license (MIT)
├── .gitignore              # Python-specific gitignore
└── README.md               # This file
```

## Getting Started

### Prerequisites

- Python 3.11 or higher
- UV package manager

### Installation

1. Install UV (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Clone this template:
   ```bash
   git clone https://github.com/yourusername/python-template-repository.git
   cd python-template-repository
   ```

3. Install dependencies:
   ```bash
   uv sync
   ```

## Components

This template includes three example components:

- **Calculator**: Performs basic arithmetic operations (addition, subtraction, multiplication, division)
- **Logger**: Records operations and their results with configurable output formats
- **Notifier**: Sends alerts when values exceed user-defined thresholds

### Using Components

```python
# Example usage of the components
from calculator.src.calculator import Calculator
from logger.src.logger import Logger
from notifier.src.notifier import Notifier

# Create a calculator
calc = Calculator()
result = calc.add(5, 3)  # Returns 8

# Log the operation
logger = Logger()
logger.log_operation("Addition", [5, 3], result)

# Set up notification
notifier = Notifier(threshold=10)
notifier.check_value(result)  # No notification (8 < 10)
result = calc.multiply(5, 3)  # Returns 15
notifier.check_value(result)  # Sends notification (15 > 10)
```

For detailed information about the component architecture, see `component.md`.

## Testing

### Running Tests

Run all tests:
```bash
uv run pytest
```

Run a specific component's unit tests:
```bash
uv run pytest calculator/src/calculator/tests/
```

Run integration tests:
```bash
uv run pytest tests/integration/
```

Run end-to-end tests:
```bash
uv run pytest tests/e2e/
```

Run tests with coverage:
```bash
uv run pytest --cov
```

### Test Structure

- **Unit Tests**: Located alongside each component to test individual functionality
  - Calculator tests verify addition, subtraction, and multiplication operations
  - Logger tests ensure operations are logged correctly
  - Notifier tests confirm notifications are sent when thresholds are exceeded

- **Integration Tests**: Located in `tests/integration/` to test component interactions
  - Calculator → Logger integration (with mocked Notifier)
  - Logger → Notifier integration (with mocked Calculator)

- **End-to-End Tests**: Located in `tests/e2e/` to test complete workflows
  - Full workflow test: calculation → logging → notification

## Code Quality

### Static Analysis

Run linting with Ruff:
```bash
uv run ruff check .
```

Run type checking with MyPy:
```bash
uv run mypy calculator logger notifier tests
```

### Configuration

This template uses strict settings for code quality:

- **MyPy**: Strict type checking enabled with all checks
- **Ruff**: Comprehensive linting rules enabled

Any disabled checks are documented with explanations in the `pyproject.toml` file.

## CI/CD Pipeline

This template is configured with CircleCI for continuous integration. The pipeline:

- Installs dependencies with UV
- Runs linting with ruff
- Runs type checking with mypy
- Runs all tests with pytest
- Generates code coverage reports
- Stores test results for viewing in the CircleCI dashboard

### CI/CD Links

- Example Passing Build
- Example Failing Build
- Code Coverage Report

## GitHub Templates

This repository includes templates to standardize:

- **Pull Requests**: Structured format for code changes
- **Bug Reports**: Detailed information for reporting issues
- **Feature Requests**: Format for suggesting enhancements

## Customizing This Template

To use this template for your own project:

1. Update package information in the root `pyproject.toml`
2. Modify component implementations for your specific needs
3. Update tests to match your new implementations
4. Update this README with your project details

## License

This project is licensed under the Apache License, Version 2.0 - see the LICENSE file for details.