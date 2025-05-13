"""Git operations for PR Coverage Analyzer."""

import logging
import re
import subprocess
from typing import Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)

class GitOperations:
    """Handles Git operations for the PR Coverage Analyzer."""
    
    def __init__(self, base_branch: str = "main"):
        """Initialize GitOperations.
        
        Args:
            base_branch: The base branch to compare against (default: "main")
        """
        self.base_branch = base_branch
        self.original_branch = self.run_command("git rev-parse --abbrev-ref HEAD")
        self.merge_base = self.get_merge_base()
        self.current_revision = self.get_current_revision()
    
    def run_command(self, command: str) -> str:
        """Run a shell command and return its output.
        
        Args:
            command: Shell command to run
            
        Returns:
            Command output as a string
        """
        logger.debug(f"Running command: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Error executing command: {command}")
            logger.error(f"Error: {result.stderr}")
            return ""
        return result.stdout.strip()
    
    def get_merge_base(self) -> str:
        """Get the merge base between current branch and target branch.
        
        Returns:
            The merge base commit hash
        """
        current_branch = self.run_command("git rev-parse --abbrev-ref HEAD")
        merge_base = self.run_command(f"git merge-base {self.base_branch} {current_branch}")
        return merge_base
    
    def get_current_revision(self) -> str:
        """Get the current HEAD revision.
        
        Returns:
            The current HEAD commit hash
        """
        return self.run_command("git rev-parse HEAD")
    
    def get_modified_files(self, file_pattern: str = "*.py") -> List[str]:
        """Get list of modified files in the PR that match the file pattern.
        
        Args:
            file_pattern: File pattern to match (glob pattern)
            
        Returns:
            List of modified file paths
        """
        import fnmatch
        
        modified_files = self.run_command(f"git diff --name-only {self.merge_base}").split("\n")
        
        # Use glob pattern matching for file filtering
        matched_files = [f for f in modified_files if f and fnmatch.fnmatch(f, file_pattern)]
        
        logger.info(f"Found {len(matched_files)} modified files matching pattern {file_pattern}")
        return matched_files
    
    def get_modified_lines(self, file_path: str) -> Set[int]:
        """Get the line numbers that were modified in a file using git diff.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Set of modified line numbers
        """
        diff_output = self.run_command(f"git diff -U0 {self.merge_base} -- {file_path}")
        
        modified_lines = set()
        current_line = None
        
        for line in diff_output.split("\n"):
            if line.startswith("@@"):
                # Parse hunk header
                match = re.search(r"\+(\d+)(?:,(\d+))?", line)
                if match:
                    start_line = int(match.group(1))
                    line_count = int(match.group(2) or 1)
                    current_line = start_line
            elif line.startswith("+") and not line.startswith("+++"):
                # This is an added line
                if current_line is not None:
                    modified_lines.add(current_line)
                    current_line += 1
            elif line.startswith(" "):
                # This is an unchanged line
                if current_line is not None:
                    current_line += 1
        
        return modified_lines
    
    def checkout_revision(self, revision: str) -> None:
        """Checkout a specific git revision.
        
        Args:
            revision: Git revision to checkout
        """
        logger.info(f"Checking out revision: {revision[:7]}")
        self.run_command(f"git checkout {revision}")
    
    def restore_original_branch(self) -> None:
        """Restore the original branch."""
        self.checkout_revision(self.original_branch)
    
    def clone_repo(self, repo_url: str, target_dir: str) -> bool:
        """Clone a repository.
        
        Args:
            repo_url: Repository URL
            target_dir: Target directory
            
        Returns:
            True if clone was successful, False otherwise
        """
        result = subprocess.run(
            ["git", "clone", repo_url, target_dir],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
