"""Tests for CLI module."""

import os
from unittest.mock import patch, MagicMock

import pytest

from pr_coverage_analyzer.cli import main, parse_args

def test_parse_args():
    """Test parse_args function."""
    with patch('sys.argv', ['pr-coverage', '--pr-url', 'https://github.com/user/repo/pull/123']):
        args = parse_args()
        assert args.pr_url == 'https://github.com/user/repo/pull/123'

def test_main_success():
    """Test main function with successful execution."""
    mock_analyzer = MagicMock()
    mock_analyzer.analyze.return_value = {"overall": {}}
    
    with patch('pr_coverage_analyzer.cli.PRCoverageAnalyzer', return_value=mock_analyzer), \
         patch('sys.argv', ['pr-coverage']):
        exit_code = main()
        
        assert exit_code == 0
        mock_analyzer.analyze.assert_called_once()
        mock_analyzer.generate_report.assert_called_once()

def test_main_error():
    """Test main function with error."""
    mock_analyzer = MagicMock()
    mock_analyzer.analyze.side_effect = Exception("Test error")
    
    with patch('pr_coverage_analyzer.cli.PRCoverageAnalyzer', return_value=mock_analyzer), \
         patch('sys.argv', ['pr-coverage']):
        exit_code = main()
        
        assert exit_code == 1
        mock_analyzer.analyze.assert_called_once()
