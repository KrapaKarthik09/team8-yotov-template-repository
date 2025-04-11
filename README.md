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
├── src/                    # Source code directory
│   ├── calculator/         # Calculator component
│   │   ├── calculator.py   # Implementation
│   │   ├── __init__.py     # Component API
│   │   ├── pyproject.toml  # Component dependencies
│   │   └── tests/          # Component unit tests
│   ├── logger/             # Logger component
│   │   └── ...
│   ├── notifier/           # Notifier component
│   │   └── ...
│   └── __init__.py         # Package exports
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

## Getting Started

### Prerequisites

- Python 3.11 or higher
- UV package manager

### Installation

1. Install UV (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh

2. Clone this template:
   ```bash
   git clone https://github.com/yourusername/team8-yotov-template-repository.git
   cd team8-yotov-template-repository
   ```

3. Install dependencies:
   ```bash
   uv sync
   uv pip install -e .
   ```

### Running Tests

#### Run all tests:
```bash
uv run pytest
```

#### Run a specific component's unit tests:
```bash
uv run pytest src/calculator/tests/
```

#### Run integration tests:
```bash
uv run pytest tests/integration/
```

#### Run end-to-end tests:
```bash
uv run pytest tests/e2e/
```

#### Run tests with coverage:
```bash
uv run pytest --cov=src
```

### Code Quality

#### Run linting with Ruff:
```bash
uv run ruff check .
```

#### Run type checking with MyPy:
```bash
uv run mypy src tests
```

## CI/CD Pipeline

This template is configured with CircleCI for continuous integration. The pipeline:

1. Installs dependencies
2. Runs linting with ruff
3. Runs type checking with mypy
4. Runs all tests with pytest
5. Generates code coverage reports

## Components

This template includes three example components:

1. **Calculator**: Performs basic arithmetic operations
2. **Logger**: Records operations and their results
3. **Notifier**: Sends alerts when values exceed thresholds

For detailed information about the component architecture, see [component.md](./component.md).

## Templates

GitHub templates are included to standardize:
- Pull requests
- Bug reports
- Feature requests

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.