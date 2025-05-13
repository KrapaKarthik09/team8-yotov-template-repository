"""Coverage data processing for PR Coverage Analyzer."""

import json
import logging
import os
from typing import Dict, List, Optional, Set, Tuple, Union

logger = logging.getLogger(__name__)

class CoverageProcessor:
    """Process coverage data for PR analysis."""
    
    def __init__(self, coverage_format: str = "coverage.py"):
        """Initialize CoverageProcessor.
        
        Args:
            coverage_format: Format of coverage data (default: "coverage.py")
        """
        self.coverage_format = coverage_format
    
    def run_coverage_command(self, command: str) -> bool:
        """Run a coverage command.
        
        Args:
            command: Command to run
            
        Returns:
            True if command was successful, False otherwise
        """
        import subprocess
        
        logger.info(f"Running coverage command: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.error(f"Error running coverage command: {command}")
            logger.error(f"Error: {result.stderr}")
            return False
        
        return True
    
    def load_coverage_data(self, file_path: str) -> Dict:
        """Load coverage data from a file.
        
        Args:
            file_path: Path to coverage data file
            
        Returns:
            Coverage data as a dictionary
        """
        logger.info(f"Loading coverage data from: {file_path}")
        
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading coverage data: {e}")
            return {}
    
    def get_file_coverage(self, coverage_data: Dict, file_path: str) -> Dict:
        """Extract coverage data for a specific file.
        
        Args:
            coverage_data: Coverage data dictionary
            file_path: Path to the file
            
        Returns:
            Dictionary with line coverage data and percentage
        """
        if self.coverage_format == "coverage.py":
            # Python coverage.py format
            try:
                file_data = coverage_data.get("files", {}).get(file_path, {})
                missing_lines = set(file_data.get("missing_lines", []))
                executed_lines = set(file_data.get("executed_lines", []))
                
                # Create a dictionary of line number to coverage status
                line_coverage = {}
                for line in executed_lines:
                    line_coverage[line] = True  # Covered
                for line in missing_lines:
                    line_coverage[line] = False  # Not covered
                
                total_lines = len(executed_lines) + len(missing_lines)
                if total_lines > 0:
                    coverage_percentage = (len(executed_lines) / total_lines) * 100
                else:
                    coverage_percentage = 0.0
                    
                return {
                    "line_coverage": line_coverage,
                    "percentage": coverage_percentage
                }
            except Exception as e:
                logger.error(f"Error processing coverage data for {file_path}: {e}")
                return {"line_coverage": {}, "percentage": 0.0}
        
        # Add support for other coverage formats as needed
        else:
            logger.error(f"Unsupported coverage format: {self.coverage_format}")
            return {"line_coverage": {}, "percentage": 0.0}
