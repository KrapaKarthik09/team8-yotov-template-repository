"""End-to-end integration tests for PR Coverage Analyzer."""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

from pr_coverage_analyzer.analyzer import PRCoverageAnalyzer

@pytest.fixture
def integration_repo():
    """Create a Git repository with sample project for integration testing."""
    # Create temporary directory
    repo_dir = tempfile.mkdtemp()
    
    try:
        # Initialize Git repository
        subprocess.run(["git", "init"], cwd=repo_dir, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_dir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_dir, check=True)
        
        # Copy sample project
        sample_dir = os.path.join(os.path.dirname(__file__), "sample_project")
        project_dir = os.path.join(repo_dir, "project")
        os.makedirs(project_dir)
        
        for item in os.listdir(sample_dir):
            if item.endswith(".py"):
                src = os.path.join(sample_dir, item)
                dst = os.path.join(project_dir, item)
                shutil.copy2(src, dst)
        
        # Create __init__.py
        with open(os.path.join(project_dir, "__init__.py"), "w") as f:
            f.write("")
        
        # Create pyproject.toml
        with open(os.path.join(repo_dir, "pyproject.toml"), "w") as f:
            f.write('''[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "project"
version = "0.1.0"
description = "Test project"

[tool.pytest.ini_options]
pythonpath = ["."]
''')
        
        # Install coverage and pytest
        subprocess.run(["pip", "install", "coverage", "pytest"], check=True)
        
        # Add files to Git
        subprocess.run(["git", "add", "."], cwd=repo_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_dir, check=True)
        
        # Create main branch
        subprocess.run(["git", "branch", "-M", "main"], cwd=repo_dir, check=True)
        
        # Create feature branch
        subprocess.run(["git", "checkout", "-b", "feature"], cwd=repo_dir, check=True)
        
        # Modify calculator.py to add a new function
        with open(os.path.join(project_dir, "calculator.py"), "a") as f:
            f.write('''
def power(a, b):
    """Raise a to the power of b."""
    return a ** b
''')
        
        # Add test for the new function
        with open(os.path.join(project_dir, "test_calculator.py"), "a") as f:
            f.write('''
def test_power():
    """Test power function."""
    assert power(2, 3) == 8
    assert power(5, 0) == 1
''')
        
        # Fix imports in test_calculator.py
        with open(os.path.join(project_dir, "test_calculator.py"), "r") as f:
            content = f.read()
        
        content = content.replace(
            "from .calculator import add, subtract, multiply, divide, square",
            "from .calculator import add, subtract, multiply, divide, square, power"
        )
        
        with open(os.path.join(project_dir, "test_calculator.py"), "w") as f:
            f.write(content)
        
        # Commit changes
        subprocess.run(["git", "add", "."], cwd=repo_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Add power function with tests"], cwd=repo_dir, check=True)
        
        # Return to the repository directory
        yield repo_dir
    
    finally:
        # Clean up
        shutil.rmtree(repo_dir)

def test_end_to_end_analysis(integration_repo):
    """Test end-to-end analysis process."""
    os.chdir(integration_repo)
    
    # Configure analyzer
    analyzer = PRCoverageAnalyzer(
        base_branch="main",
        file_pattern="*.py",
        coverage_commands={
            "base": "cd {} && coverage run -m pytest project && coverage json -o coverage-base.json".format(integration_repo),
            "head": "cd {} && coverage run -m pytest project && coverage json -o coverage-head.json".format(integration_repo)
        }
    )
    
    # Run analysis
    results = analyzer.analyze()
    
    # Generate report
    report_file = os.path.join(integration_repo, "coverage-report.md")
    analyzer.generate_report(results, report_file)
    
    # Verify results
    assert "overall" in results
    assert results["overall"]["current_percentage"] > results["overall"]["base_percentage"]
    
    # Verify report file was created
    assert os.path.exists(report_file)
    
    # Read report content
    with open(report_file, "r") as f:
        report_content = f.read()
    
    # Verify report contains expected content
    assert "# Code Coverage PR Analysis" in report_content
    assert "Overall coverage has improved" in report_content
    assert "project/calculator.py" in report_content
