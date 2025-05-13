"""Test fixtures for PR Coverage Analyzer."""

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

# Define sample coverage data for tests
@pytest.fixture
def sample_coverage_data():
    """Sample coverage data fixture."""
    return {
        "meta": {
            "version": "5.5",
            "timestamp": "2025-05-12T13:37:42.123456",
            "branch_coverage": True,
            "show_contexts": True
        },
        "files": {
            "sample_project/calculator.py": {
                "executed_lines": [1, 2, 3, 5, 6, 7],
                "missing_lines": [9, 10],
                "excluded_lines": []
            }
        },
        "totals": {
            "covered_lines": 6,
            "num_statements": 8,
            "percent_covered": 75.0,
            "missing_lines": 2,
            "excluded_lines": 0
        }
    }

@pytest.fixture
def sample_coverage_data_updated():
    """Updated sample coverage data fixture."""
    return {
        "meta": {
            "version": "5.5",
            "timestamp": "2025-05-12T14:45:42.123456",
            "branch_coverage": True,
            "show_contexts": True
        },
        "files": {
            "sample_project/calculator.py": {
                "executed_lines": [1, 2, 3, 5, 6, 7, 9],
                "missing_lines": [10],
                "excluded_lines": []
            }
        },
        "totals": {
            "covered_lines": 7,
            "num_statements": 8,
            "percent_covered": 87.5,
            "missing_lines": 1,
            "excluded_lines": 0
        }
    }

@pytest.fixture
def temp_git_repo():
    """Create a temporary Git repository for testing."""
    # Create temporary directory
    repo_dir = tempfile.mkdtemp()
    
    # Initialize Git repository
    subprocess.run(["git", "init"], cwd=repo_dir, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_dir, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_dir, check=True)
    
    # Create initial file
    with open(os.path.join(repo_dir, "README.md"), "w") as f:
        f.write("# Test Repository\n\nThis is a test repository.")
    
    # Commit initial file
    subprocess.run(["git", "add", "README.md"], cwd=repo_dir, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_dir, check=True)
    
    # Create main branch
    subprocess.run(["git", "branch", "-M", "main"], cwd=repo_dir, check=True)
    
    # Create feature branch
    subprocess.run(["git", "checkout", "-b", "feature"], cwd=repo_dir, check=True)
    
    yield repo_dir
    
    # Clean up
    shutil.rmtree(repo_dir)

@pytest.fixture
def sample_project_files(temp_git_repo):
    """Create sample project files in the Git repository."""
    project_dir = os.path.join(temp_git_repo, "sample_project")
    os.makedirs(project_dir, exist_ok=True)
    
    # Create calculator.py
    with open(os.path.join(project_dir, "calculator.py"), "w") as f:
        f.write('''"""Simple calculator module."""

def add(a, b):
    """Add two numbers."""
    return a + b

def subtract(a, b):
    """Subtract b from a."""
    return a - b

def multiply(a, b):
    """Multiply two numbers."""
    return a * b

def divide(a, b):
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
''')
    
    # Create __init__.py
    with open(os.path.join(project_dir, "__init__.py"), "w") as f:
        f.write('"""Sample project."""\n')
    
    # Create test_calculator.py
    with open(os.path.join(project_dir, "test_calculator.py"), "w") as f:
        f.write('''"""Tests for calculator module."""

import pytest
from sample_project.calculator import add, subtract, multiply, divide

def test_add():
    """Test add function."""
    assert add(1, 2) == 3
    assert add(-1, 1) == 0

def test_subtract():
    """Test subtract function."""
    assert subtract(3, 2) == 1
    assert subtract(5, 5) == 0

def test_multiply():
    """Test multiply function."""
    assert multiply(2, 3) == 6
    assert multiply(5, 0) == 0

def test_divide():
    """Test divide function."""
    assert divide(6, 3) == 2
    assert divide(5, 2) == 2.5
    
    with pytest.raises(ValueError):
        divide(1, 0)
''')
    
    # Create pyproject.toml
    with open(os.path.join(temp_git_repo, "pyproject.toml"), "w") as f:
        f.write('''[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "sample_project"
version = "0.1.0"
description = "Sample project for testing"

[tool.pytest.ini_options]
pythonpath = ["."]
''')
    
    # Add files to Git
    subprocess.run(["git", "add", "."], cwd=temp_git_repo, check=True)
    subprocess.run(["git", "commit", "-m", "Add sample project"], cwd=temp_git_repo, check=True)
    
    # Switch to main branch and then back to feature
    subprocess.run(["git", "checkout", "main"], cwd=temp_git_repo, check=True)
    subprocess.run(["git", "merge", "feature"], cwd=temp_git_repo, check=True)
    subprocess.run(["git", "checkout", "feature"], cwd=temp_git_repo, check=True)
    
    # Modify calculator.py in feature branch to improve coverage
    with open(os.path.join(project_dir, "calculator.py"), "w") as f:
        f.write('''"""Simple calculator module."""

def add(a, b):
    """Add two numbers."""
    return a + b

def subtract(a, b):
    """Subtract b from a."""
    return a - b

def multiply(a, b):
    """Multiply two numbers."""
    return a * b

def divide(a, b):
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def square(a):
    """Square a number."""
    return a * a
''')
    
    # Update test_calculator.py to include test for new function
    with open(os.path.join(project_dir, "test_calculator.py"), "w") as f:
        f.write('''"""Tests for calculator module."""

import pytest
from sample_project.calculator import add, subtract, multiply, divide, square

def test_add():
    """Test add function."""
    assert add(1, 2) == 3
    assert add(-1, 1) == 0

def test_subtract():
    """Test subtract function."""
    assert subtract(3, 2) == 1
    assert subtract(5, 5) == 0

def test_multiply():
    """Test multiply function."""
    assert multiply(2, 3) == 6
    assert multiply(5, 0) == 0

def test_divide():
    """Test divide function."""
    assert divide(6, 3) == 2
    assert divide(5, 2) == 2.5
    
    with pytest.raises(ValueError):
        divide(1, 0)

def test_square():
    """Test square function."""
    assert square(2) == 4
    assert square(-3) == 9
''')
    
    # Commit changes
    subprocess.run(["git", "add", "."], cwd=temp_git_repo, check=True)
    subprocess.run(["git", "commit", "-m", "Add square function with tests"], cwd=temp_git_repo, check=True)
    
    return temp_git_repo

@pytest.fixture
def mock_coverage_files(sample_project_files, sample_coverage_data, sample_coverage_data_updated):
    """Create mock coverage files."""
    repo_dir = sample_project_files
    
    # Create coverage files
    with open(os.path.join(repo_dir, "coverage-base.json"), "w") as f:
        json.dump(sample_coverage_data, f)
    
    with open(os.path.join(repo_dir, "coverage-head.json"), "w") as f:
        json.dump(sample_coverage_data_updated, f)
    
    return repo_dir
    
@pytest.fixture
def sample_results():
    """Sample results for testing."""
    return {
        "overall": {
            "base_percentage": 75.0,
            "current_percentage": 87.5,
            "base_covered": 6,
            "base_total": 8,
            "current_covered": 7,
            "current_total": 8
        },
        "sample_project/calculator.py": {
            "base_percentage": 75.0,
            "current_percentage": 87.5,
            "line_changes": {
                16: {"before": None, "after": True},
                17: {"before": None, "after": True},
                18: {"before": None, "after": True}
            }
        }
    }
