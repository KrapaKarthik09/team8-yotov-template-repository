"""Tests for Coverage Processor module."""

import json
import os
from unittest.mock import patch, MagicMock

import pytest

from pr_coverage_analyzer.coverage import CoverageProcessor

def test_load_coverage_data(tmp_path, sample_coverage_data):
    """Test load_coverage_data method."""
    # Create a temp coverage file
    coverage_file = tmp_path / "coverage.json"
    with open(coverage_file, "w") as f:
        json.dump(sample_coverage_data, f)
    
    processor = CoverageProcessor()
    loaded_data = processor.load_coverage_data(str(coverage_file))
    
    assert loaded_data == sample_coverage_data

def test_load_coverage_data_error(tmp_path):
    """Test load_coverage_data method with non-existent file."""
    processor = CoverageProcessor()
    loaded_data = processor.load_coverage_data(str(tmp_path / "non_existent.json"))
    
    assert loaded_data == {}

def test_run_coverage_command():
    """Test run_coverage_command method."""
    processor = CoverageProcessor()
    
    # Test successful command
    with patch('subprocess.run') as mock_run:
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_run.return_value = mock_process
        
        result = processor.run_coverage_command("coverage run -m pytest")
        
        mock_run.assert_called_once()
        assert result is True
    
    # Test failed command
    with patch('subprocess.run') as mock_run:
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stderr = "Command error"
        mock_run.return_value = mock_process
        
        result = processor.run_coverage_command("invalid command")
        
        mock_run.assert_called_once()
        assert result is False

def test_get_file_coverage(sample_coverage_data):
    """Test get_file_coverage method."""
    processor = CoverageProcessor()
    
    file_coverage = processor.get_file_coverage(
        sample_coverage_data, "sample_project/calculator.py"
    )
    
    # Verify coverage data
    assert "line_coverage" in file_coverage
    assert "percentage" in file_coverage
    
    # Calculate expected percentage
    executed_lines = sample_coverage_data["files"]["sample_project/calculator.py"]["executed_lines"]
    missing_lines = sample_coverage_data["files"]["sample_project/calculator.py"]["missing_lines"]
    expected_pct = len(executed_lines) / (len(executed_lines) + len(missing_lines)) * 100
    
    assert file_coverage["percentage"] == expected_pct
    
    # Verify line coverage
    for line in executed_lines:
        assert file_coverage["line_coverage"][line] is True
    
    for line in missing_lines:
        assert file_coverage["line_coverage"][line] is False

def test_get_file_coverage_missing_file(sample_coverage_data):
    """Test get_file_coverage method with missing file."""
    processor = CoverageProcessor()
    
    file_coverage = processor.get_file_coverage(
        sample_coverage_data, "non_existent.py"
    )
    
    assert file_coverage["line_coverage"] == {}
    assert file_coverage["percentage"] == 0.0

def test_get_file_coverage_unsupported_format():
    """Test get_file_coverage method with unsupported format."""
    processor = CoverageProcessor(coverage_format="unsupported")
    
    file_coverage = processor.get_file_coverage(
        {}, "file.py"
    )
    
    assert file_coverage["line_coverage"] == {}
    assert file_coverage["percentage"] == 0.0
