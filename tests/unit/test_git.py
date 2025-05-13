"""Tests for Git operations module."""

import os
import subprocess
from unittest.mock import patch, MagicMock

import pytest

from pr_coverage_analyzer.git import GitOperations

def test_run_command():
    """Test run_command method."""
    git_ops = GitOperations()
    
    # Test successful command
    with patch('subprocess.run') as mock_run:
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "Command output"
        mock_run.return_value = mock_process
        
        result = git_ops.run_command("git status")
        
        mock_run.assert_called_once_with(
            "git status", shell=True, capture_output=True, text=True
        )
        assert result == "Command output"
    
    # Test failed command
    with patch('subprocess.run') as mock_run:
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stderr = "Command error"
        mock_run.return_value = mock_process
        
        result = git_ops.run_command("git invalid")
        
        mock_run.assert_called_once_with(
            "git invalid", shell=True, capture_output=True, text=True
        )
        assert result == ""

def test_get_merge_base(sample_project_files):
    """Test get_merge_base method with actual Git repository."""
    os.chdir(sample_project_files)
    
    # Ensure we're on the feature branch
    subprocess.run(["git", "checkout", "feature"], check=True)
    
    git_ops = GitOperations(base_branch="main")
    merge_base = git_ops.get_merge_base()
    
    # Verify merge base exists
    assert merge_base, "Merge base should not be empty"
    
    # Get main branch commit
    main_commit = subprocess.run(
        ["git", "rev-parse", "main"],
        capture_output=True, text=True, check=True
    ).stdout.strip()
    
    # Verify merge base is the main branch commit
    assert merge_base == main_commit, "Merge base should be the main branch commit"

def test_get_modified_files(sample_project_files):
    """Test get_modified_files method with actual Git repository."""
    os.chdir(sample_project_files)
    
    # Ensure we're on the feature branch
    subprocess.run(["git", "checkout", "feature"], check=True)
    
    git_ops = GitOperations(base_branch="main")
    
    # Get modified Python files
    modified_files = git_ops.get_modified_files("*.py")
    
    # Verify the calculator.py file is in the list
    assert "sample_project/calculator.py" in modified_files
    assert "sample_project/test_calculator.py" in modified_files
    
    # Test different file pattern
    md_files = git_ops.get_modified_files("*.md")
    assert len(md_files) == 0, "No markdown files should be modified"

def test_get_modified_lines(sample_project_files):
    """Test get_modified_lines method with actual Git repository."""
    os.chdir(sample_project_files)
    
    # Ensure we're on the feature branch
    subprocess.run(["git", "checkout", "feature"], check=True)
    
    git_ops = GitOperations(base_branch="main")
    
    # Get modified lines in calculator.py
    modified_lines = git_ops.get_modified_lines("sample_project/calculator.py")
    
    # The newly added square function should be in the modified lines
    # Line numbers might vary, but typically would be around line 16-19
    assert len(modified_lines) > 0, "Should have some modified lines"
    
    # At least one line number should be greater than 15
    assert any(line > 15 for line in modified_lines), "Should include new square function lines"

def test_checkout_revision(sample_project_files):
    """Test checkout_revision method with actual Git repository."""
    os.chdir(sample_project_files)
    
    git_ops = GitOperations()
    
    # Get current branch
    current_branch = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True, text=True, check=True
    ).stdout.strip()
    
    # Get main branch commit
    main_commit = subprocess.run(
        ["git", "rev-parse", "main"],
        capture_output=True, text=True, check=True
    ).stdout.strip()
    
    # Checkout main branch commit
    git_ops.checkout_revision(main_commit)
    
    # Get current commit
    current_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True
    ).stdout.strip()
    
    # Verify we're on the main branch commit
    assert current_commit == main_commit, "Should be on main branch commit"
    
    # Restore original branch
    subprocess.run(["git", "checkout", current_branch], check=True)
