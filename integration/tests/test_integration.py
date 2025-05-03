"""Integration tests for the AI Email Assistant."""

import os
import sys
import pytest  
import tempfile
import json


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_email_assistant import AIEmailAssistant
from email_processor import (extract_entities, extract_dates,
                          format_email_for_ai, generate_email_response_template)


@pytest.fixture
def assistant():
    """Set up test environment."""
    # Create AI Email Assistant with mock clients
    assistant = AIEmailAssistant(use_mock=True, ai_client_name="mock")
    yield assistant
    # Clean up after tests (equivalent to tearDown)
    assistant.close()

@pytest.fixture
def email_ids(assistant):
    """Return a list of email IDs for testing"""
    # Ensure we have emails to work with
    return assistant.fetch_emails(count=5)
    
def test_fetch_emails(assistant):
    """Test fetching emails."""
    # Fetch some emails
    email_ids = assistant.fetch_emails(count=3)
    
    # Verify we got 3 email IDs
    assert len(email_ids) == 3
    
    # Verify each ID is a string
    for email_id in email_ids:
        assert isinstance(email_id, str)

# Example of using mocker for patching
def test_with_mocked_ai(assistant, mocker):
    """Test with mocked AI client."""
    # Mock the AI client's generate_response method
    mock_generate = mocker.patch.object(
        assistant.ai_client, 
        'generate_response', 
        return_value="Mocked AI response"
    )
    
    # Use the assistant with the mocked method
    result = assistant.process_test_input("Hello")
    
    # Assert the mock was called
    mock_generate.assert_called_once()
    assert "Mocked AI response" in result
