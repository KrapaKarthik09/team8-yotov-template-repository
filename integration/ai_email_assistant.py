"""
AI Email Assistant Integration.

This module integrates the Cerebras AI Conversation Client with MyInbox
email implementation to create an AI-powered email assistant.
"""

import os
import json
from typing import Dict, List, Optional, Union
from datetime import datetime

# Import from my_inbox_impl
# from my_inbox_impl import get_client as get_email_client
# from my_inbox_impl.get_client import get_email_client
from my_inbox_impl._impl import get_client as get_email_client
from my_inbox_impl.mail_fetcher import MockFetcher, IMAPFetcher

# Import from AI conversation client
from components.ai_conversation_client import get_client as get_ai_client
from components.ai_conversation_client import AIConversationClient, CerebrasClient

class AIEmailAssistant:
    """
    Integrates AI conversation capabilities with email operations.
    
    This class connects the Cerebras AI client with the MyInbox email
    implementation to provide AI-powered email processing and responses.
    """
    
    def __init__(
        self,
        use_mock: bool = True,
        ai_client_name: str = "mock",
        imap_config: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Initialize the AI Email Assistant.
        
        Args:
            use_mock: Whether to use mock data for emails (True) or connect to
                     real email server (False)
            ai_client_name: The AI client to use ("cerebras" or "mock")
            imap_config: Configuration for IMAP connection, required if use_mock is False
                         Format: {
                             "host": "imap.example.com",
                             "port": "993",
                             "username": "user@example.com",
                             "password": "password"
                         }
        
        Raises:
            ValueError: If use_mock is False and imap_config is not provided
        """
        # Initialize AI client
        self.ai_client = get_ai_client(ai_client_name)
        
        # Initialize email client
        self.email_client = get_email_client()
        
        # Set up email fetcher
        if use_mock:
            self.email_fetcher = MockFetcher()
        else:
            if not imap_config:
                raise ValueError("IMAP configuration is required when use_mock is False")
            
            self.email_fetcher = IMAPFetcher(
                host=imap_config["host"],
                port=int(imap_config["port"]),
                username=imap_config["username"],
                password=imap_config["password"]
            )
        
        # Connect email fetcher to email client
        self.email_fetcher.set_client(self.email_client)
        
        # Track AI sessions for each email context
        self.active_sessions: Dict[str, str] = {}  # email_id -> ai_session_id
    
    def fetch_emails(self, count: int = 10, folder: str = "INBOX") -> List[str]:
        """
        Fetch emails from the specified folder.
        
        Args:
            count: Number of emails to fetch
            folder: Folder to fetch emails from
            
        Returns:
            List of email IDs that were fetched
        """
        emails = self.email_fetcher.fetch_messages(count=count, folder=folder)
        return [email.id for email in emails]
    
    def process_email(self, email_id: str) -> Dict[str, str]:
        """
        Process an email using the AI client and generate a response.
        
        Args:
            email_id: ID of the email to process
            
        Returns:
            Dictionary containing:
                - original_subject: Original email subject
                - original_body: Original email body
                - sender: Email sender
                - ai_response: Generated AI response
                
        Raises:
            ValueError: If email with given ID is not found
        """
        # Get email messages
        messages = list(self.email_client.get_messages())
        
        # Find the specific email
        target_email = None
        for msg in messages:
            if msg.id == email_id:
                target_email = msg
                break
                
        if not target_email:
            raise ValueError(f"Email with ID {email_id} not found")
        
        # Create or retrieve an AI session for this email
        if email_id not in self.active_sessions:
            # Create new AI session
            user_id = f"email_user_{email_id[:8]}"
            session_id = self.ai_client.start_new_session(user_id)
            self.active_sessions[email_id] = session_id
        else:
            session_id = self.active_sessions[email_id]
        
        # Create a prompt based on the email content
        prompt = self._create_email_prompt(target_email.subject, target_email.body)
        
        # Get AI response
        response = self.ai_client.send_message(session_id, prompt)
        
        return {
            "original_subject": target_email.subject,
            "original_body": target_email.body,
            "sender": target_email.from_,
            "ai_response": response["response"]
        }
    
    def _create_email_prompt(self, subject: str, body: str) -> str:
        """
        Create a prompt for the AI based on email content.
        
        Args:
            subject: Email subject
            body: Email body
            
        Returns:
            Formatted prompt for the AI
        """
        prompt = (
            f"Please analyze this email and suggest a response:\n\n"
            f"Subject: {subject}\n\n"
            f"Body:\n{body}\n\n"
            f"Analyze the tone, content, and context of this email. "
            f"Then draft a professional and appropriate response."
        )
        return prompt
    
    def get_email_summary(self, email_id: str) -> str:
        """
        Generate a summary of an email using the AI.
        
        Args:
            email_id: ID of the email to summarize
            
        Returns:
            Summary of the email
            
        Raises:
            ValueError: If email with given ID is not found
        """
        # Get email messages
        messages = list(self.email_client.get_messages())
        
        # Find the specific email
        target_email = None
        for msg in messages:
            if msg.id == email_id:
                target_email = msg
                break
                
        if not target_email:
            raise ValueError(f"Email with ID {email_id} not found")
        
        # Create or retrieve an AI session for this email
        if email_id not in self.active_sessions:
            # Create new AI session
            user_id = f"email_user_{email_id[:8]}"
            session_id = self.ai_client.start_new_session(user_id)
            self.active_sessions[email_id] = session_id
        else:
            session_id = self.active_sessions[email_id]
        
        # Create a summary prompt
        prompt = (
            f"Please provide a concise 2-3 sentence summary of this email:\n\n"
            f"Subject: {target_email.subject}\n\n"
            f"Body:\n{target_email.body}\n\n"
        )
        
        # Get AI response
        response = self.ai_client.send_message(session_id, prompt)
        
        return response["response"]
    
    def search_emails(self, query: str) -> List[Dict[str, str]]:
        """
        Search emails with AI-enhanced context understanding.
        
        Args:
            query: Search query
            
        Returns:
            List of dictionaries containing matching email information:
                - id: Email ID
                - subject: Email subject
                - sender: Email sender
                - relevance: AI-determined relevance score (0-100)
        """
        # Get search results from email client
        search_results = list(self.email_client.search_messages(query))
        
        if not search_results:
            return []
        
        # Create a new AI session for search enhancement
        user_id = f"search_user_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        session_id = self.ai_client.start_new_session(user_id)
        
        # Enhanced results with AI relevance scoring
        enhanced_results = []
        
        for msg in search_results:
            # Create a relevance prompt
            prompt = (
                f"On a scale of 0-100, rate the relevance of this email to the search query: '{query}'\n\n"
                f"Subject: {msg.subject}\n\n"
                f"Body:\n{msg.body}\n\n"
                f"Return only a number between 0 and 100 representing the relevance score."
            )
            
            # Get AI response
            response = self.ai_client.send_message(session_id, prompt)
            
            # Try to extract a numeric score from the response
            try:
                score_text = ''.join([c for c in response["response"] if c.isdigit()])
                score = int(score_text) if score_text else 50  # Default to 50 if parsing fails
                score = max(0, min(100, score))  # Ensure score is within range
            except (ValueError, TypeError):
                score = 50  # Default score if parsing fails

            
            enhanced_results.append({
                "id": msg.id,
                "subject": msg.subject,
                "sender": msg.from_,
                "relevance": score
            })
        
        # Sort by relevance (highest first)
        enhanced_results.sort(key=lambda x: x["relevance"], reverse=True)
        
        # End the search session
        self.ai_client.end_session(session_id)
        
        return enhanced_results
    
    def categorize_email(self, email_id: str) -> str:
        """
        Categorize an email using AI to determine its type/folder.
        
        Args:
            email_id: ID of the email to categorize
            
        Returns:
            Suggested folder/category for the email
            
        Raises:
            ValueError: If email with given ID is not found
        """
        # Get email messages
        messages = list(self.email_client.get_messages())
        
        # Find the specific email
        target_email = None
        for msg in messages:
            if msg.id == email_id:
                target_email = msg
                break
                
        if not target_email:
            raise ValueError(f"Email with ID {email_id} not found")
        
        # Create a new AI session for categorization
        user_id = f"category_user_{email_id[:8]}"
        session_id = self.ai_client.start_new_session(user_id)
        
        # Create a categorization prompt
        prompt = (
            f"Please categorize this email into one of the following folders: "
            f"Inbox, Work, Personal, Finance, Social, Promotions, Updates, Forums, Spam.\n\n"
            f"Subject: {target_email.subject}\n\n"
            f"Body:\n{target_email.body}\n\n"
            f"Return only the folder name with no additional text or explanation."
        )
        
        # Get AI response
        response = self.ai_client.send_message(session_id, prompt)
        
        # Clean up response to get just the folder name
        folder = response["response"].strip()
        
        # End the categorization session
        self.ai_client.end_session(session_id)
        
        return folder
    
    def close(self) -> None:
        """Close all active sessions and connections."""
        # End all AI sessions
        for email_id, session_id in self.active_sessions.items():
            try:
                self.ai_client.end_session(session_id)
            except Exception as e:  # Catch general exceptions, but log them or handle accordingly
                print(f"Failed to end session for {session_id}: {e}")

        
        # Clear active sessions
        self.active_sessions.clear()
        
        # Close email fetcher if using IMAP
        if isinstance(self.email_fetcher, IMAPFetcher):
            self.email_fetcher.close()