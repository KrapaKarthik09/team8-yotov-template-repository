"""Main analyzer module for PR Coverage Analyzer."""

import logging
import os
from collections import defaultdict
from typing import Dict, List, Optional, Set

from pr_coverage_analyzer.coverage import CoverageProcessor
from pr_coverage_analyzer.git import GitOperations
from pr_coverage_analyzer.github import GitHubPR
from pr_coverage_analyzer.report import ReportGenerator

logger = logging.getLogger(__name__)

class PRCoverageAnalyzer:
    """Analyze code coverage changes in a Pull Request."""
    
    def __init__(self, 
                base_branch: str = "main", 
                file_pattern: str = "*.py", 
                coverage_format: str = "coverage.py",
                coverage_commands: Optional[Dict[str, str]] = None,
                coverage_files: Optional[Dict[str, str]] = None,
                verbose: bool = False,
                pr_url: Optional[str] = None,
                github_token: Optional[str] = None):
        """Initialize PRCoverageAnalyzer.
        
        Args:
            base_branch: Base branch to compare against (default: "main")
            file_pattern: File pattern to match (default: "*.py")
            coverage_format: Coverage format (default: "coverage.py")
            coverage_commands: Dictionary with commands to run for coverage (optional)
            coverage_files: Dictionary with coverage data file paths (optional)
            verbose: Enable verbose logging (default: False)
            pr_url: GitHub PR URL (optional)
            github_token: GitHub API token (optional)
        """
        # Setup logging
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)
        
        # Default configuration
        self.config = {
            "base_branch": base_branch,
            "file_pattern": file_pattern,
            "coverage_format": coverage_format,
            "coverage_commands": coverage_commands or {
                "base": "coverage run -m pytest && coverage json -o coverage-base.json",
                "head": "coverage run -m pytest && coverage json -o coverage-head.json"
            },
            "coverage_files": coverage_files or {
                "base": "coverage-base.json",
                "head": "coverage-head.json"
            },
            "verbose": verbose
        }
        
        # Initialize components
        self.git_ops = GitOperations(base_branch=self.config["base_branch"])
        self.coverage_processor = CoverageProcessor(coverage_format=self.config["coverage_format"])
        self.report_generator = ReportGenerator()
        
        # GitHub PR integration
        self.github_pr = None
        if pr_url:
            self.github_pr = GitHubPR(pr_url=pr_url, token=github_token)
    
    def analyze(self):
        """Main function to analyze coverage changes in a PR.
        
        Returns:
            Dictionary with analysis results
        """
        try:
            # If we have a GitHub PR, clone the repository
            if self.github_pr:
                repo_dir = self.github_pr.clone_repo()
                # Update the Git operations with the correct base branch
                self.git_ops = GitOperations(base_branch=self.github_pr.base_branch)
            
            # Get modified files
            modified_files = self.git_ops.get_modified_files(self.config["file_pattern"])
            if not modified_files:
                logger.info("No matching files were modified in this PR.")
                return {}
            
            # Store modified lines for each file
            file_modified_lines = {}
            for file_path in modified_files:
                file_modified_lines[file_path] = self.git_ops.get_modified_lines(file_path)
            
            # Get coverage for merge base
            self.git_ops.checkout_revision(self.git_ops.merge_base)
            self.coverage_processor.run_coverage_command(self.config["coverage_commands"]["base"])
            base_coverage_data = self.coverage_processor.load_coverage_data(self.config["coverage_files"]["base"])
            
            # Get coverage for current revision
            self.git_ops.checkout_revision(self.git_ops.current_revision)
            self.coverage_processor.run_coverage_command(self.config["coverage_commands"]["head"])
            current_coverage_data = self.coverage_processor.load_coverage_data(self.config["coverage_files"]["head"])
            
            # Analyze changes
            results = self.compare_coverage(
                base_coverage_data, 
                current_coverage_data,
                modified_files,
                file_modified_lines
            )
            
            return results
        
        finally:
            # Restore original state
            self.git_ops.restore_original_branch()
            
            # Clean up GitHub PR resources if applicable
            if self.github_pr:
                self.github_pr.cleanup()
    
    def compare_coverage(self, base_coverage_data, current_coverage_data, modified_files, file_modified_lines):
        """Compare coverage data between two revisions.
        
        Args:
            base_coverage_data: Base coverage data
            current_coverage_data: Current coverage data
            modified_files: List of modified files
            file_modified_lines: Dictionary of modified lines per file
            
        Returns:
            Dictionary with comparison results
        """
        results = defaultdict(dict)
        overall_stats = {
            "base": {"covered": 0, "total": 0},
            "current": {"covered": 0, "total": 0}
        }
        
        for file_path in modified_files:
            base_file_coverage = self.coverage_processor.get_file_coverage(base_coverage_data, file_path)
            current_file_coverage = self.coverage_processor.get_file_coverage(current_coverage_data, file_path)
            
            results[file_path] = {
                "base_percentage": base_file_coverage["percentage"],
                "current_percentage": current_file_coverage["percentage"],
                "line_changes": {}
            }
            
            # Count overall stats
            base_covered = sum(1 for v in base_file_coverage["line_coverage"].values() if v)
            base_total = len(base_file_coverage["line_coverage"])
            current_covered = sum(1 for v in current_file_coverage["line_coverage"].values() if v)
            current_total = len(current_file_coverage["line_coverage"])
            
            overall_stats["base"]["covered"] += base_covered
            overall_stats["base"]["total"] += base_total
            overall_stats["current"]["covered"] += current_covered
            overall_stats["current"]["total"] += current_total
            
            # Analyze changes for modified lines
            modified_lines = file_modified_lines[file_path]
            for line in modified_lines:
                base_covered = base_file_coverage["line_coverage"].get(line, None)
                current_covered = current_file_coverage["line_coverage"].get(line, None)
                
                # Only record if there's a change or if the line is not covered
                if base_covered != current_covered or (current_covered is not None and not current_covered):
                    results[file_path]["line_changes"][line] = {
                        "before": base_covered,
                        "after": current_covered
                    }
        
        # Calculate overall percentage
        base_total = overall_stats["base"]["total"]
        current_total = overall_stats["current"]["total"]
        
        overall_base_percentage = (overall_stats["base"]["covered"] / base_total * 100) if base_total > 0 else 0
        overall_current_percentage = (overall_stats["current"]["covered"] / current_total * 100) if current_total > 0 else 0
        
        results["overall"] = {
            "base_percentage": overall_base_percentage,
            "current_percentage": overall_current_percentage,
            "base_covered": overall_stats["base"]["covered"],
            "base_total": overall_stats["base"]["total"],
            "current_covered": overall_stats["current"]["covered"],
            "current_total": overall_stats["current"]["total"]
        }
        
        return results
    
    def generate_report(self, results, output_file=None):
        """Generate a report of the coverage changes.
        
        Args:
            results: Analysis results
            output_file: Markdown output file path (optional)
            
        Returns:
            None
        """
        # Generate console report
        self.report_generator.generate_console_report(results.copy())
        
        # Generate and export Markdown report if requested
        if output_file:
            self.report_generator.export_markdown_report(results.copy(), output_file)
            
            # Post comment to GitHub PR if applicable
            if self.github_pr and os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    comment_body = f.read()
                
                self.github_pr.post_comment(comment_body)
