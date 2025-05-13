"""Unit tests for the email processor module."""

import os
import sys
import pytest
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from email_processor import (extract_entities, extract_dates, format_email_for_ai,
                          generate_email_response_template, analyze_sentiment,
                          extract_action_items)

def test_extract_entities():
    """Test extracting entities from email text."""
    # Sample email body with entities
    email_body = """
    Hello team,
    Please contact john.doe@example.com or visit https://example.com for more information.
    We have a meeting scheduled on 05/15/2025 and another one on June 20, 2025.
    Regards,
    Jane Smith
    """
    
    # Extract entities
    entities = extract_entities(email_body)
    
    # Verify emails
    assert "john.doe@example.com" in entities["emails"]
    
    # Verify URLs
    assert "https://example.com" in entities["urls"]
    
    # Verify dates
    assert any("05/15/2025" in date for date in entities["dates"])
    assert any("June 20, 2025" in date for date in entities["dates"])

def test_extract_dates():
    """Test extracting dates from text."""
    # Text with various date formats
    text = """
    Meeting on 01/15/2025
    Conference call on March 20, 2025
    Deadline is 2025-04-30
    Review session on 5 April 2025
    """
    
    dates = extract_dates(text)
    
    # Verify we found all four dates
    assert len(dates) == 4
    assert any("01/15/2025" in date for date in dates)
    assert any("March 20, 2025" in date for date in dates)
    assert any("2025-04-30" in date for date in dates)
    assert any("5 April 2025" in date for date in dates)

def test_format_email_for_ai():
    """Test formatting email data for AI processing."""
    # Sample email data
    email_data = {
        "subject": "Project Update",
        "body": "Hello team,\nProject is on track. Please contact john@example.com.",
        "sender": "manager@company.com",
        "date": "2025-04-25"
    }
    
    # Format for AI
    formatted = format_email_for_ai(email_data)
    
    # Verify structure
    assert "EMAIL INFORMATION:" in formatted
    assert "From: manager@company.com" in formatted
    assert "Subject: Project Update" in formatted
    assert "Hello team," in formatted
    
    # Verify extracted entities
    assert "EXTRACTED ENTITIES:" in formatted
    assert "john@example.com" in formatted

def test_generate_email_response_template():
    """Test generating email response template."""
    # Original email
    original_email = {
        "subject": "Question about project",
        "body": "When will the project be completed?",
        "sender": "client@example.com",
        "date": "2025-04-24"
    }
    
    # AI response
    ai_response = "The project is scheduled to be completed by next Friday."
    
    # Generate template
    template = generate_email_response_template(original_email, ai_response)
    
    # Verify template structure
    assert template["to"] == "client@example.com"
    assert template["subject"] == "Re: Question about project"
    assert "The project is scheduled to be completed by next Friday" in template["body"]
    assert "On 2025-04-24" in template["body"]
    assert "> When will the project be completed?" in template["body"]

@pytest.mark.parametrize("text, expected", [
    ("Thank you for your excellent work. I really appreciate your help.", "positive"),
    ("There's a problem with the service. I'm disappointed with the results.", "negative"),
    ("Please find attached the requested documents.", "neutral")
])
def test_analyze_sentiment(text, expected):
    """Test sentiment analysis function."""
    assert analyze_sentiment(text) == expected

def test_extract_action_items():
    """Test extracting action items from email."""
    # Email with action items
    email_text = """
    Hello team,
    Please review the attached document by tomorrow.
    We need to finalize the report ASAP.
    Could you update the presentation with the latest figures?
    Let me know if you have any questions.
    """
    
    action_items = extract_action_items(email_text)
    
    # Verify we found at least 3 action items
    assert len(action_items) >= 3
    
    # Check for specific action items
    assert any("review the attached document" in item.lower() for item in action_items)
    assert any("finalize the report" in item.lower() for item in action_items)
    assert any("update the presentation" in item.lower() for item in action_items)
