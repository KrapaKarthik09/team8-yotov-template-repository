"""
Demo script for the AI Email Assistant integration.

This script demonstrates the integration between the AI Conversation Client 
and MyInbox email implementation.
"""

import os
import sys
import argparse
from typing import Dict, List, Optional, Any

from integration.ai_email_assistant import AIEmailAssistant
from integration.config import load_config, create_default_config


def demo_mock_mode():
    """Run the demo in mock mode (no real email or AI connections)."""
    print("\n=== AI Email Assistant Demo (Mock Mode) ===\n")
    
    # Initialize AI Email Assistant with mock clients
    assistant = AIEmailAssistant(use_mock=True, ai_client_name="mock")
    
    try:
        # 1. Fetch mock emails
        print("Fetching mock emails...")
        email_ids = assistant.fetch_emails(count=10)
        print(f"Fetched {len(email_ids)} mock emails")
        
        if not email_ids:
            print("No emails to process. Exiting demo.")
            return
        
        # 2. Process one email
        print("\n--- Processing a sample email ---")
        email_id = email_ids[0]  # Use the first email
        result = assistant.process_email(email_id)
        
        print(f"Original Subject: {result['original_subject']}")
        print(f"From: {result['sender']}")
        print("\nOriginal Email Body:")
        print(f"{result['original_body'][:200]}..." if len(result['original_body']) > 200 else result['original_body'])
        print("\nAI-Generated Response:")
        print(result['ai_response'])
        
        # 3. Generate email summary
        print("\n--- Generating Email Summary ---")
        summary = assistant.get_email_summary(email_id)
        print(f"Summary: {summary}")
        
        # 4. Search emails
        print("\n--- Searching Emails ---")
        search_term = "important"
        print(f"Searching for: '{search_term}'")
        search_results = assistant.search_emails(search_term)
        
        print(f"Found {len(search_results)} emails (sorted by AI-determined relevance):")
        for idx, result in enumerate(search_results[:3], 1):  # Show top 3 results
            print(f"{idx}. '{result['subject']}' (Relevance: {result['relevance']}%)")
        
        # 5. Categorize emails
        print("\n--- Categorizing Emails ---")
        for i, email_id in enumerate(email_ids[:3], 1):  # Categorize first 3 emails
            try:
                category = assistant.categorize_email(email_id)
                
                # Get email info for display
                messages = list(assistant.email_client.get_messages())
                email = next((msg for msg in messages if msg.id == email_id), None)
                
                if email:
                    print(f"{i}. '{email.subject}' → Category: {category}")
            except ValueError as e:
                print(f"Error categorizing email {email_id}: {e}")
        
        print("\nDemo completed successfully!")
        
    finally:
        # Ensure resources are cleaned up
        assistant.close()


def demo_with_config(config_path: str):
    """
    Run the demo using a configuration file.
    
    Args:
        config_path: Path to the configuration file
    """
    print(f"\n=== AI Email Assistant Demo (Using config: {config_path}) ===\n")
    
    # Load configuration
    config = load_config(config_path)
    
    # Determine if we're using mock mode
    use_mock = config.get("use_mock", True)
    ai_client_name = config.get("ai_client", {}).get("name", "mock")
    
    # Set up IMAP config if not using mock
    imap_config = None
    if not config.get("email", {}).get("use_mock", True):
        imap_config = config.get("email", {}).get("imap", {})
    
    print(f"Mode: {'Mock' if use_mock else 'Real'}")
    print(f"AI Client: {ai_client_name}")
    
    # Initialize AI Email Assistant
    assistant = AIEmailAssistant(
        use_mock=use_mock,
        ai_client_name=ai_client_name,
        imap_config=imap_config
    )
    
    try:
        # Run demo logic similar to mock mode
        print("Fetching emails...")
        email_ids = assistant.fetch_emails(count=5)
        print(f"Fetched {len(email_ids)} emails")
        
        # Continue with similar demo logic as mock_mode
        # ...
        
    finally:
        assistant.close()


def main():
    """Main entry point for the demo."""
    parser = argparse.ArgumentParser(description="AI Email Assistant Demo")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--create-config", help="Create default configuration file at specified path")
    parser.add_argument("--mock", action="store_true", help="Run in mock mode (default if no config)")
    
    args = parser.parse_args()
    
    # Create default config if requested
    if args.create_config:
        create_default_config(args.create_config)
        return
    
    # Determine mode
    if args.config:
        demo_with_config(args.config)
    else:
        demo_mock_mode()


if __name__ == "__main__":
    main()