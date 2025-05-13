"""Report generation for PR Coverage Analyzer."""

import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generate reports for PR code coverage analysis."""
    
    def generate_console_report(self, results: Dict) -> None:
        """Generate a console report of the coverage changes.
        
        Args:
            results: Analysis results
        """
        overall = results.pop("overall", {})
        
        print("\n=== Code Coverage PR Analysis ===\n")
        
        # Overall stats
        base_percentage = overall.get("base_percentage", 0)
        current_percentage = overall.get("current_percentage", 0)
        diff = current_percentage - base_percentage
        
        print(f"Overall coverage: {base_percentage:.2f}% -> {current_percentage:.2f}% ({diff:+.2f}%)")
        
        if diff > 0:
            print("✅ Overall coverage has improved")
        elif diff < 0:
            print("❌ Overall coverage has worsened")
        else:
            print("ℹ️ Overall coverage remains the same")
        
        # Add more detailed stats
        base_covered = overall.get("base_covered", 0)
        base_total = overall.get("base_total", 0)
        current_covered = overall.get("current_covered", 0)
        current_total = overall.get("current_total", 0)
        
        print(f"Lines covered: {base_covered}/{base_total} -> {current_covered}/{current_total}")
        
        # File details
        print("\nDetailed file coverage changes:")
        
        if not results:
            print("  No coverage changes detected in modified files.")
            return
        
        for file_path, data in sorted(results.items()):
            base_pct = data.get("base_percentage", 0)
            current_pct = data.get("current_percentage", 0)
            file_diff = current_pct - base_pct
            
            print(f"\n{file_path}:")
            print(f"  Coverage: {base_pct:.2f}% -> {current_pct:.2f}% ({file_diff:+.2f}%)")
            
            line_changes = data.get("line_changes", {})
            if line_changes:
                print("  Modified lines with coverage changes:")
                for line, change in sorted(line_changes.items()):
                    before = change.get("before")
                    after = change.get("after")
                    
                    before_str = "covered" if before else "not covered" if before is not None else "not executable"
                    after_str = "covered" if after else "not covered" if after is not None else "not executable"
                    
                    # Highlight improvements and regressions
                    status = "✅" if before is False and after is True else "❌" if before is True and after is False else "ℹ️"
                    
                    print(f"    {status} Line {line}: {before_str} -> {after_str}")
            else:
                print("  No coverage changes in modified lines")
    
    def generate_markdown_report(self, results: Dict) -> str:
        """Generate a Markdown report of the coverage changes.
        
        Args:
            results: Analysis results
            
        Returns:
            Markdown report as a string
        """
        overall = results.get("overall", {})
        markdown_lines = []
        
        markdown_lines.append("# Code Coverage PR Analysis\n")
        
        # Overall stats
        base_percentage = overall.get("base_percentage", 0)
        current_percentage = overall.get("current_percentage", 0)
        diff = current_percentage - base_percentage
        
        markdown_lines.append("## Summary\n")
        markdown_lines.append(f"* Overall coverage: **{base_percentage:.2f}%** -> **{current_percentage:.2f}%** ({diff:+.2f}%)\n")
        
        if diff > 0:
            markdown_lines.append("* ✅ **Overall coverage has improved**\n")
        elif diff < 0:
            markdown_lines.append("* ❌ **Overall coverage has worsened**\n")
        else:
            markdown_lines.append("* ℹ️ **Overall coverage remains the same**\n")
        
        # Add more detailed stats
        base_covered = overall.get("base_covered", 0)
        base_total = overall.get("base_total", 0)
        current_covered = overall.get("current_covered", 0)
        current_total = overall.get("current_total", 0)
        
        markdown_lines.append(f"* Lines covered: **{base_covered}/{base_total}** -> **{current_covered}/{current_total}**\n")
        
        # File details
        markdown_lines.append("## Detailed Changes\n")
        
        file_results = {k: v for k, v in results.items() if k != "overall"}
        
        if not file_results:
            markdown_lines.append("No coverage changes detected in modified files.\n")
            return "\n".join(markdown_lines)
        
        for file_path, data in sorted(file_results.items()):
            base_pct = data.get("base_percentage", 0)
            current_pct = data.get("current_percentage", 0)
            file_diff = current_pct - base_pct
            
            markdown_lines.append(f"### {file_path}\n")
            markdown_lines.append(f"* Coverage: **{base_pct:.2f}%** -> **{current_pct:.2f}%** ({file_diff:+.2f}%)\n")
            
            line_changes = data.get("line_changes", {})
            if line_changes:
                markdown_lines.append("\n**Modified lines with coverage changes:**\n")
                
                markdown_lines.append("| Line | Before | After | Status |\n")
                markdown_lines.append("|------|--------|-------|--------|\n")
                
                for line, change in sorted(line_changes.items()):
                    before = change.get("before")
                    after = change.get("after")
                    
                    before_str = "Covered" if before else "Not covered" if before is not None else "Not executable"
                    after_str = "Covered" if after else "Not covered" if after is not None else "Not executable"
                    
                    # Determine status emoji
                    status = "✅" if before is False and after is True else "❌" if before is True and after is False else "ℹ️"
                    
                    markdown_lines.append(f"| {line} | {before_str} | {after_str} | {status} |\n")
            else:
                markdown_lines.append("\nNo coverage changes in modified lines.\n")
            
            markdown_lines.append("\n")
        
        return "".join(markdown_lines)
    
    def export_markdown_report(self, results: Dict, output_file: str) -> None:
        """Export results to Markdown file.
        
        Args:
            results: Analysis results
            output_file: Output file path
        """
        markdown_content = self.generate_markdown_report(results)
        
        with open(output_file, 'w') as f:
            f.write(markdown_content)
        
        logger.info(f"Markdown report exported to {output_file}")
