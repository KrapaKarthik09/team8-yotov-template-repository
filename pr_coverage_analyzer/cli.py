"""Command-line interface for PR Coverage Analyzer."""

import argparse
import logging
import os
import sys
from typing import Dict, List, Optional

from pr_coverage_analyzer.analyzer import PRCoverageAnalyzer

logger = logging.getLogger(__name__)

def parse_args():
    """Parse command-line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Analyze code coverage changes in a PR")
    
    # Git configuration
    parser.add_argument("--base-branch", help="Base branch to compare against (default: main)")
    parser.add_argument("--file-pattern", help="File pattern to analyze (default: *.py)")
    
    # Coverage configuration
    parser.add_argument("--coverage-format", help="Coverage format (default: coverage.py)")
    parser.add_argument("--base-coverage-cmd", help="Command to run for base coverage")
    parser.add_argument("--head-coverage-cmd", help="Command to run for head coverage")
    parser.add_argument("--base-coverage-file", help="Path to base coverage data file")
    parser.add_argument("--head-coverage-file", help="Path to head coverage data file")
    
    # GitHub integration
    parser.add_argument("--pr-url", help="GitHub PR URL to analyze")
    parser.add_argument("--github-token", help="GitHub API token for PR integration")
    
    # Output configuration
    parser.add_argument("--markdown-output", help="Export results to Markdown file for PR comments")
    
    # Other options
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    
    return parser.parse_args()

def main():
    """Main entry point for the command-line interface."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Parse arguments
    args = parse_args()
    
    # Configure coverage commands if provided
    coverage_commands = None
    if args.base_coverage_cmd or args.head_coverage_cmd:
        coverage_commands = {
            "base": args.base_coverage_cmd or "coverage run -m pytest && coverage json -o coverage-base.json",
            "head": args.head_coverage_cmd or "coverage run -m pytest && coverage json -o coverage-head.json"
        }
    
    # Configure coverage files if provided
    coverage_files = None
    if args.base_coverage_file or args.head_coverage_file:
        coverage_files = {
            "base": args.base_coverage_file or "coverage-base.json",
            "head": args.head_coverage_file or "coverage-head.json"
        }
    
    # Create analyzer
    analyzer = PRCoverageAnalyzer(
        base_branch=args.base_branch,
        file_pattern=args.file_pattern,
        coverage_format=args.coverage_format,
        coverage_commands=coverage_commands,
        coverage_files=coverage_files,
        verbose=args.verbose,
        pr_url=args.pr_url,
        github_token=args.github_token
    )
    
    try:
        # Analyze coverage
        results = analyzer.analyze()
        
        # Generate report
        analyzer.generate_report(results, args.markdown_output)
        
        return 0
    except Exception as e:
        logger.error(f"Error analyzing coverage: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
