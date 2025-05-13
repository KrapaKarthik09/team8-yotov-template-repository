# PR Coverage Analyzer
## Team 8 [Extra Credit]

A tool to analyze code coverage changes in Pull Requests by comparing coverage before and after the changes.

## Features

- 📊 Compare code coverage between PR base and head
- 📈 Identify coverage changes for modified lines
- 📝 Generate detailed reports in console and Markdown formats
- 🔗 GitHub PR integration for automated analysis
- 🔄 CircleCI integration for CI/CD pipelines
- ⚙️ Customizable configuration

## Installation

### From PyPI

```bash
pip install pr-coverage-analyzer
```

### From Source

```bash
git clone https://github.com/username/pr-coverage-analyzer.git
cd pr-coverage-analyzer
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
```

## Quick Start

1. Navigate to your project:

```bash
cd your-project
```

2. Run the analyzer on your current branch:

```bash
pr-coverage
```

3. To export a Markdown report:

```bash
pr-coverage --markdown-output coverage-report.md
```

## Usage

### Basic Usage

Analyze coverage in your current branch against the main branch:

```bash
pr-coverage
```

### Custom Base Branch

```bash
pr-coverage --base-branch develop
```

### Custom File Pattern

Analyze only Python files:

```bash
pr-coverage --file-pattern "*.py"
```

Or Java files:

```bash
pr-coverage --file-pattern "*.java"
```

### GitHub PR Integration

Analyze a GitHub PR directly:

```bash
pr-coverage --pr-url https://github.com/username/repo/pull/123 --github-token YOUR_TOKEN
```

This will:
1. Clone the repository
2. Checkout the appropriate branches
3. Run the coverage analysis
4. Generate a report
5. Post the report as a comment on the PR (if a token is provided)

### Export Options

Generate a Markdown report:

```bash
pr-coverage --markdown-output coverage-report.md
```

### Verbose Mode

Enable detailed logging:

```bash
pr-coverage --verbose
```

## CircleCI Integration

Add the following to your CircleCI configuration:

```yaml
version: 2.1

orbs:
  python: circleci/python@2.1a

jobs:
  analyze-pr:
    docker:
      - image: cimg/python:3.10
    parameters:
      pr_url:
        type: string
        default: ""
    steps:
      - checkout
      - python/install-packages:
          pkg-manager: pip
          packages:
            - "pr-coverage-analyzer"
      - run:
          name: Analyze PR Coverage
          command: |
            if [[ -n "<< parameters.pr_url >>" ]]; then
              pr-coverage --pr-url << parameters.pr_url >> --markdown-output coverage-report.md
            else
              pr-coverage --markdown-output coverage-report.md
            fi
      - store_artifacts:
          path: coverage-report.md

workflows:
  version: 2
  pr-analysis:
    jobs:
      - analyze-pr:
          pr_url: << pipeline.parameters.pr_url >>

# Pipeline parameters for manual triggering with PR URL
parameters:
  pr_url:
    type: string
    default: ""
```

You can trigger this workflow manually with a PR URL:

```bash
circleci trigger \
  --project-slug <your-project-slug> \
  --branch <branch> \
  --parameter pr_url="https://github.com/username/repo/pull/123"
```

## Configuration

PR Coverage Analyzer can be configured with command-line arguments or by creating a configuration file.

### Command-Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--base-branch` | Base branch to compare against | `main` |
| `--file-pattern` | File pattern to analyze | `*.py` |
| `--coverage-format` | Coverage format | `coverage.py` |
| `--base-coverage-cmd` | Command to run for base coverage | `coverage run -m pytest && coverage json -o coverage-base.json` |
| `--head-coverage-cmd` | Command to run for head coverage | `coverage run -m pytest && coverage json -o coverage-head.json` |
| `--base-coverage-file` | Path to base coverage data file | `coverage-base.json` |
| `--head-coverage-file` | Path to head coverage data file | `coverage-head.json` |
| `--pr-url` | GitHub PR URL to analyze | None |
| `--github-token` | GitHub API token for PR integration | None |
| `--markdown-output` | Export results to Markdown file | None |
| `--verbose` | Enable verbose logging | False |

## How It Works

1. The tool identifies the merge base (common ancestor) between your current branch and the target branch
2. It gets all modified files in your PR that match the specified pattern
3. For each file, it identifies which lines were modified
4. It checks out the merge base, runs tests with coverage, and captures the coverage data
5. It checks out your current branch, runs tests with coverage again, and captures the coverage data
6. It compares the two sets of coverage data to determine:
   - Which modified lines had coverage changes
   - Whether overall coverage improved or worsened
7. It generates a report showing the coverage changes for each file and line

## Project Structure

```
pr_coverage_analyzer/
  ├── pyproject.toml
  ├── .circleci/
  │   └── config.yml
  ├── pr_coverage_analyzer/
  │   ├── __init__.py
  │   ├── analyzer.py          # Main analyzer logic
  │   ├── git.py               # Git-related operations
  │   ├── coverage.py          # Coverage data processing
  │   ├── report.py            # Report generation
  │   ├── github.py            # GitHub integration
  │   └── cli.py               # Command-line interface
  ├── tests/
  │   ├── __init__.py
  │   ├── conftest.py          # Test configuration
  │   ├── unit/                # Unit tests
  │   └── integration/         # Integration tests
```

## Example Output

### Console Output

```
=== Code Coverage PR Analysis ===

Overall coverage: 75.00% -> 87.50% (+12.50%)
✅ Overall coverage has improved
Lines covered: 6/8 -> 7/8

Detailed file coverage changes:

sample_project/calculator.py:
  Coverage: 75.00% -> 87.50% (+12.50%)
  Modified lines with coverage changes:
    ✅ Line 16: not covered -> covered
    ✅ Line 17: not covered -> covered
    ✅ Line 18: not covered -> covered
```

### Markdown Report

The tool generates detailed Markdown reports that can be posted as PR comments:

```markdown
# Code Coverage PR Analysis

## Summary

* Overall coverage: **75.00%** -> **87.50%** (+12.50%)
* ✅ **Overall coverage has improved**
* Lines covered: **6/8** -> **7/8**

## Detailed Changes

### sample_project/calculator.py

* Coverage: **75.00%** -> **87.50%** (+12.50%)

**Modified lines with coverage changes:**

| Line | Before | After | Status |
|------|--------|-------|--------|
| 16 | Not covered | Covered | ✅ |
| 17 | Not covered | Covered | ✅ |
| 18 | Not covered | Covered | ✅ |
```

## Running the Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run unit tests only
pytest tests/unit

# Run integration tests only
pytest tests/integration

# Run tests with coverage
coverage run -m pytest
coverage report
coverage html
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please make sure to update tests as appropriate and ensure all tests pass before submitting PRs.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
