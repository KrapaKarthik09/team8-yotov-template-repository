"""GitHub integration for PR Coverage Analyzer."""

import logging
import os
import re
import tempfile
import subprocess
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

import requests
from github import Github, GithubException

from pr_coverage_analyzer.git import GitOperations

logger = logging.getLogger(__name__)

class GitHubPR:
    """GitHub Pull Request integration."""
    
    def __init__(self, pr_url: Optional[str] = None, token: Optional[str] = None):
        """Initialize GitHub PR integration.
        
        Args:
            pr_url: GitHub PR URL (optional)
            token: GitHub API token (optional)
        """
        self.pr_url = pr_url
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.repo_name = None
        self.pr_number = None
        self.base_branch = None
        self.head_branch = None
        self.repo_clone_url = None
        self.repo_dir = None
        
        if pr_url:
            self.parse_pr_url(pr_url)
    
    def parse_pr_url(self, pr_url: str) -> None:
        """Parse GitHub PR URL to extract repo and PR number.
        
        Args:
            pr_url: GitHub PR URL
        """
        # Extract owner, repo, and PR number from URL
        # Format: https://github.com/owner/repo/pull/123
        pattern = r"https?://github\.com/([^/]+)/([^/]+)/pull/(\d+)"
        match = re.match(pattern, pr_url)
        
        if not match:
            raise ValueError(f"Invalid GitHub PR URL: {pr_url}")
        
        owner, repo, pr_number = match.groups()
        self.repo_name = f"{owner}/{repo}"
        self.pr_number = int(pr_number)
        self.repo_clone_url = f"https://github.com/{self.repo_name}.git"
        
        # Get PR details using GitHub API
        self._fetch_pr_details()
    
    def _fetch_pr_details(self) -> None:
        """Fetch PR details using GitHub API."""
        if not self.repo_name or not self.pr_number:
            raise ValueError("Repository name and PR number must be set")
        
        github = Github(self.token) if self.token else Github()
        
        try:
            repo = github.get_repo(self.repo_name)
            pr = repo.get_pull(self.pr_number)
            
            self.base_branch = pr.base.ref
            self.head_branch = pr.head.ref
            
            logger.info(f"PR #{self.pr_number}: {pr.title}")
            logger.info(f"Base branch: {self.base_branch}")
            logger.info(f"Head branch: {self.head_branch}")
        
        except GithubException as e:
            logger.error(f"Failed to fetch PR details: {e}")
            raise
    
    def clone_repo(self) -> str:
        """Clone the repository to a temporary directory.
        
        Returns:
            Path to the cloned repository
        """
        if not self.repo_clone_url:
            raise ValueError("Repository clone URL is not set")
        
        # Create temporary directory for the repository
        self.repo_dir = tempfile.mkdtemp(prefix="pr_coverage_")
        
        # Clone the repository
        git_ops = GitOperations()
        success = git_ops.clone_repo(self.repo_clone_url, self.repo_dir)
        
        if not success:
            raise RuntimeError(f"Failed to clone repository: {self.repo_clone_url}")
        
        logger.info(f"Repository cloned to: {self.repo_dir}")
        
        # Change to the repository directory
        os.chdir(self.repo_dir)
        
        # Fetch the PR head branch
        subprocess.run(["git", "fetch", "origin", self.head_branch], check=True)
        
        return self.repo_dir
    
    def post_comment(self, comment_body: str) -> bool:
        """Post a comment to the PR.
        
        Args:
            comment_body: Comment body in Markdown format
            
        Returns:
            True if comment was posted successfully, False otherwise
        """
        if not self.token:
            logger.warning("GitHub token not provided. Cannot post comment.")
            return False
        
        if not self.repo_name or not self.pr_number:
            logger.error("Repository name and PR number must be set")
            return False
        
        # Use GitHub API to post comment
        url = f"https://api.github.com/repos/{self.repo_name}/issues/{self.pr_number}/comments"
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {"body": comment_body}
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 201:
            logger.info("Comment posted successfully")
            return True
        else:
            logger.error(f"Failed to post comment: {response.status_code} {response.text}")
            return False
    
    def cleanup(self) -> None:
        """Clean up temporary repository directory."""
        if self.repo_dir and os.path.exists(self.repo_dir):
            import shutil
            shutil.rmtree(self.repo_dir)
            logger.info(f"Removed temporary directory: {self.repo_dir}")
