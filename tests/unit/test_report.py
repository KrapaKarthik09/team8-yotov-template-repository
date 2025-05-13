"""Tests for Report Generator module."""

import json
import os
from unittest.mock import patch, MagicMock, mock_open

import pytest

from pr_coverage_analyzer.report import ReportGenerator

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

def test_generate_markdown_report(sample_results):
    """Test generate_markdown_report method."""
    generator = ReportGenerator()
    
    report = generator.generate_markdown_report(sample_results)
    
    # Check some key phrases in the report
    assert "# Code Coverage PR Analysis" in report
    assert "## Summary" in report
    assert "Overall coverage: **75.00%** -> **87.50%**" in report
    assert "✅ **Overall coverage has improved**" in report
    assert "Lines covered: **6/8** -> **7/8**" in report
    assert "### sample_project/calculator.py" in report
    assert "| Line | Before | After | Status |" in report

def test_export_markdown_report(sample_results, tmp_path):
    """Test export_markdown_report method."""
    generator = ReportGenerator()
    output_file = tmp_path / "report.md"
    
    generator.export_markdown_report(sample_results, str(output_file))
    
    # Verify file was created
    assert os.path.exists(output_file)
    
    # Read content and verify
    with open(output_file, "r") as f:
        content = f.read()
    
    assert "# Code Coverage PR Analysis" in content
    assert "## Summary" in content

def test_generate_console_report(sample_results, capfd):
    """Test generate_console_report method."""
    generator = ReportGenerator()
    
    generator.generate_console_report(sample_results.copy())
    
    # Get captured stdout
    out, _ = capfd.readouterr()
    
    # Check output
    assert "=== Code Coverage PR Analysis ===" in out
    assert "Overall coverage: 75.00% -> 87.50% (+12.50%)" in out
    assert "✅ Overall coverage has improved" in out
    assert "Lines covered: 6/8 -> 7/8" in out
    assert "sample_project/calculator.py:" in out
