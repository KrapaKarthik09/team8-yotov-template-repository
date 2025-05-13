"""Tests for GitHub integration module."""

import os
from unittest.mock import patch, MagicMock

import pytest
import requests

from pr_coverage_analyzer.github import GitHubPR

def test_parse_pr_url():
    """Test parse_pr_url method."""
    with patch.object(GitHubPR, '_fetch_pr_details'):
        # Valid PR URL
        github_pr = GitHubPR(pr_url="https://github.com/username/repo/pull/123")
        
        assert github_pr.repo_name == "username/repo"
        assert github_pr.pr_number == 123
        assert github_pr.repo_clone_url == "https://github.com/username/repo.git"
        
        # Invalid PR URL
        with pytest.raises(ValueError):
            GitHubPR(pr_url="https://github.com/invalid-url")

def test_fetch_pr_details():
    """Test _fetch_pr_details method."""
    # Mock GitHub API response
    mock_pr = MagicMock()
    mock_pr.base.ref = "main"
    mock_pr.head.ref = "feature"
    mock_pr.title = "Test PR"
    
    mock_repo = MagicMock()
    mock_repo.get_pull.return_value = mock_pr
    
    mock_github = MagicMock()
    mock_github.get_repo.return_value = mock_repo
    
    with patch('pr_coverage_analyzer.github.Github', return_value=mock_github):
        github_pr = GitHubPR()
        github_pr.repo_name = "username/repo"
        github_pr.pr_number = 123
        
        github_pr._fetch_pr_details()
        
        assert github_pr.base_branch == "main"
        assert github_pr.head_branch == "feature"
        
        mock_github.get_repo.assert_called_once_with("username/repo")
        mock_repo.get_pull.assert_called_once_with(123)

def test_post_comment():
    """Test post_comment method."""
    github_pr = GitHubPR()
    github_pr.repo_name = "username/repo"
    github_pr.pr_number = 123
    github_pr.token = "fake-token"
    
    # Test successful comment
    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response
        
        result = github_pr.post_comment("Test comment")
        
        assert result is True
        mock_post.assert_called_once()
    
    # Test failed comment
    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_post.return_value = mock_response
        
        result = github_pr.post_comment("Test comment")
        
        assert result is False
        mock_post.assert_called_once()
    
    # Test no token
    github_pr.token = None
    result = github_pr.post_comment("Test comment")
    assert result is False
    
    # Test no repo or PR number
    github_pr.repo_name = None
    result = github_pr.post_comment("Test comment")
    assert result is False
