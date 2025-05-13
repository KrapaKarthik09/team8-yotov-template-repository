"""Tests for PR Coverage Analyzer module."""

import os
from unittest.mock import patch, MagicMock

import pytest

from pr_coverage_analyzer.analyzer import PRCoverageAnalyzer

def test_analyze_no_modified_files():
    """Test analyze method with no modified files."""
    analyzer = PRCoverageAnalyzer()
    
    with patch.object(analyzer.git_ops, 'get_modified_files', return_value=[]):
        results = analyzer.analyze()
        assert results == {}

def test_compare_coverage(sample_coverage_data, sample_coverage_data_updated):
    """Test compare_coverage method."""
    analyzer = PRCoverageAnalyzer()
    
    modified_files = ["sample_project/calculator.py"]
    file_modified_lines = {
        "sample_project/calculator.py": set([16, 17, 18])
    }
    
    results = analyzer.compare_coverage(
        sample_coverage_data,
        sample_coverage_data_updated,
        modified_files,
        file_modified_lines
    )
    
    # Verify results structure
    assert "overall" in results
    assert "sample_project/calculator.py" in results
    
    # Verify overall stats
    overall = results["overall"]
    assert overall["base_percentage"] == 75.0
    assert overall["current_percentage"] == 87.5
    assert overall["base_covered"] == 6
    assert overall["base_total"] == 8
    assert overall["current_covered"] == 7
    assert overall["current_total"] == 8
    
    # Verify file stats
    file_data = results["sample_project/calculator.py"]
    assert file_data["base_percentage"] == 75.0
    assert file_data["current_percentage"] == 87.5
    
    # Verify line changes
    line_changes = file_data["line_changes"]
    
    # Line 9 should be changed from not covered to covered
    if 9 in line_changes:
        assert line_changes[9]["before"] is False
        assert line_changes[9]["after"] is True

def test_analyze_with_github_pr():
    """Test analyze method with GitHub PR integration."""
    mock_github_pr = MagicMock()
    mock_github_pr.clone_repo.return_value = "/tmp/repo"
    mock_github_pr.base_branch = "main"
    
    analyzer = PRCoverageAnalyzer()
    analyzer.github_pr = mock_github_pr
    
    with patch.object(analyzer.git_ops, 'get_modified_files', return_value=[]), \
         patch('os.chdir'):
        results = analyzer.analyze()
        
        # Verify GitHub PR methods were called
        mock_github_pr.clone_repo.assert_called_once()
        mock_github_pr.cleanup.assert_called_once()

def test_generate_report(sample_results, capfd, tmp_path):
    """Test generate_report method."""
    analyzer = PRCoverageAnalyzer()
    
    # Test console report
    analyzer.generate_report(sample_results.copy())
    
    out, _ = capfd.readouterr()
    assert "=== Code Coverage PR Analysis ===" in out
    
    # Test Markdown report
    output_file = tmp_path / "report.md"
    analyzer.generate_report(sample_results.copy(), str(output_file))
    
    assert os.path.exists(output_file)
    
    # Test with GitHub PR
    mock_github_pr = MagicMock()
    analyzer.github_pr = mock_github_pr
    
    analyzer.generate_report(sample_results.copy(), str(output_file))
    
    mock_github_pr.post_comment.assert_called_once()
