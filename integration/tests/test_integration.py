"""Integration tests for the AI Email Assistant."""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_email_assistant import AIEmailAssistant
from email_processor import (extract_entities, extract_dates,
                            format_email_for_ai, generate_email_response_template)


class TestAIEmailIntegration(unittest.TestCase):
    """Test suite for the AI Email Assistant integration."""
    
    def setUp(self):
        """Set up test environment."""
        # Create AI Email Assistant with mock clients
        self.assistant = AIEmailAssistant(use_mock=True, ai_client_name="mock")
        
        # Ensure we have emails to work with
        self.email_ids = self.assistant.fetch_emails(count=5)
        
    def test_fetch_emails(self):
        """Test fetching emails."""
        # Fetch some emails
        email_ids = self.assistant.fetch_emails(count=3)
        
        # Verify we got 3 email IDs
        self.assertEqual(len(email_ids), 3)
        
        # Verify each ID is a string
        for email_id in email_ids:
            self.assertIsInstance(email_id, str)
    
    def test_process_email(self):
        """Test processing an email with AI."""
        if not self.email_ids:
            self.skipTest("No emails available to test")
        
        # Process first email
        result = self.assistant.process_email(self.email_ids[0])
        
        # Verify result structure
        self.assertIn('original_subject', result)
        self.assertIn('original_body', result)
        self.assertIn('sender', result)
        self.assertIn('ai_response', result)
        
        # Verify content types
        self.assertIsInstance(result['original_subject'], str)
        self.assertIsInstance(result['original_body'], str)
        self.assertIsInstance(result['sender'], str)
        self.assertIsInstance(result['ai_response'], str)
    
    def test_get_email_summary(self):
        """Test generating an email summary."""
        if not self.email_ids:
            self.skipTest("No emails available to test")
        
        # Get summary for first email
        summary = self.assistant.get_email_summary(self.email_ids[0])
        
        # Verify summary is a non-empty string
        self.assertIsInstance(summary, str)
        self.assertTrue(len(summary) > 0)
    
    def test_search_emails(self):
        """Test searching emails with AI enhancement."""
        # Populate with test emails first
        if not self.email_ids:
            self.email_ids = self.assistant.fetch_emails(count=10)
            
        if not self.email_ids:
            self.skipTest("No emails available to test")
        
        # Search for emails
        results = self.assistant.search_emails("important")
        
        # Verify results structure
        for result in results:
            self.assertIn('id', result)
            self.assertIn('subject', result)
            self.assertIn('sender', result)
            self.assertIn('relevance', result)
            
            # Verify relevance score is within range
            self.assertGreaterEqual(result['relevance'], 0)
            self.assertLessEqual(result['relevance'], 100)
    
    def test_categorize_email(self):
        """Test categorizing an email."""
        if not self.email_ids:
            self.skipTest("No emails available to test")
        
        # Categorize first email
        category = self.assistant.categorize_email(self.email_ids[0])
        
        # Verify category is a non-empty string
        self.assertIsInstance(category, str)
        self.assertTrue(len(category) > 0)
        
    def test_with_invalid_email_id(self):
        """Test behavior with invalid email ID."""
        # Try to process a non-existent email
        with self.assertRaises(ValueError):
            self.assistant.process_email("nonexistent_id")
    
    def tearDown(self):
        """Clean up after tests."""
        self.assistant.close()


class TestWithConfig(unittest.TestCase):
    """Test the integration with configuration."""
    
    def test_load_from_config(self):
        """Test loading configuration from file."""
        # Create a temporary config file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            config = {
                "use_mock": True,
                "ai_client": {
                    "name": "mock",
                    "api_key": "test_key"
                },
                "email": {
                    "use_mock": True
                }
            }
            json.dump(config, f)
            config_path = f.name
        
        try:
            # Import here to avoid module import issues
            from config import load_config
            
            # Load config from file
            loaded_config = load_config(config_path)
            
            # Verify config values
            self.assertTrue(loaded_config["use_mock"])
            self.assertEqual(loaded_config["ai_client"]["name"], "mock")
            self.assertEqual(loaded_config["ai_client"]["api_key"], "test_key")
            self.assertTrue(loaded_config["email"]["use_mock"])
            
        finally:
            # Clean up temp file
            if os.path.exists(config_path):
                os.remove(config_path)


if __name__ == '__main__':
    unittest.main()