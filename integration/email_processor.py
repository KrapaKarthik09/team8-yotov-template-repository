"""
Email Processing Module.

Provides utility functions for processing emails with AI assistance.
"""

import re
from typing import Dict, List, Any

# Import constants
from .email_constants import (
    EMAIL_PATTERN,
    URL_PATTERN,
    DATE_PATTERNS,
    POSITIVE_WORDS,
    NEGATIVE_WORDS,
    ACTION_INDICATORS
)


def extract_entities(email_body: str) -> Dict[str, List[str]]:
    """
    Extract important entities from an email body.
    
    Args:
        email_body: The email body content
        
    Returns:
        Dictionary with extracted entities:
            - emails: List of email addresses
            - urls: List of URLs
            - dates: List of date strings
    """
    entities = {
        "emails": re.findall(EMAIL_PATTERN, email_body),
        "urls": re.findall(URL_PATTERN, email_body),
        "dates": extract_dates(email_body)
    }
    
    return entities


def extract_dates(text: str) -> List[str]:
    """
    Extract date-like strings from text.
    
    Args:
        text: Text to process
        
    Returns:
        List of date strings found in the text
    """
    dates = []
    for pattern in DATE_PATTERNS:
        dates.extend(re.findall(pattern, text, re.IGNORECASE))
    
    return dates


def format_email_for_ai(email_data: Dict[str, Any]) -> str:
    """
    Format email data into a structured prompt for AI processing.
    
    Args:
        email_data: Dictionary containing email fields:
            - subject: Email subject
            - body: Email body
            - sender: Email sender
            - date: Email date
            
    Returns:
        Formatted string for AI processing
    """
    prompt = (
        f"EMAIL INFORMATION:\n"
        f"From: {email_data.get('sender', 'Unknown')}\n"
        f"Date: {email_data.get('date', 'Unknown')}\n"
        f"Subject: {email_data.get('subject', 'No Subject')}\n\n"
        f"Body:\n{email_data.get('body', '')}\n\n"
    )
    
    # Add entity extraction
    if 'body' in email_data:
        entities = extract_entities(email_data['body'])
        
        if any(entities.values()):
            prompt += "EXTRACTED ENTITIES:\n"
            
            if entities['emails']:
                prompt += f"Email addresses: {', '.join(entities['emails'])}\n"
                
            if entities['urls']:
                prompt += f"URLs: {', '.join(entities['urls'])}\n"
                
            if entities['dates']:
                prompt += f"Dates: {', '.join(entities['dates'])}\n"
    
    return prompt


def generate_email_response_template(
    original_email: Dict[str, Any],
    ai_response: str
) -> Dict[str, str]:
    """
    Generate a structured email response template.
    
    Args:
        original_email: Dictionary containing original email fields
        ai_response: AI-generated response text
        
    Returns:
        Dictionary with response template:
            - to: Recipient address
            - subject: Response subject line
            - body: Formatted response body
    """
    # Create subject line (prepend "Re: " if not already present)
    original_subject = original_email.get('subject', 'No Subject')
    subject = original_subject if original_subject.startswith('Re:') else f"Re: {original_subject}"
    
    # Format response body
    body = f"{ai_response}\n\n"
    
    # Add original email as quoted text
    body += (
        f"On {original_email.get('date', 'Unknown')}, "
        f"{original_email.get('sender', 'Unknown')} wrote:\n\n"
    )
    
    # Quote original email body
    original_body = original_email.get('body', '')
    quoted_body = '\n'.join([f"> {line}" for line in original_body.split('\n')])
    body += quoted_body
    
    return {
        "to": original_email.get('sender', ''),
        "subject": subject,
        "body": body
    }


def analyze_sentiment(email_body: str) -> str:
    """
    Perform sentiment analysis on the email body text.
    
    In a real integration, this would be done by the AI model.
    This is a simplified version for demonstration purposes.
    
    Args:
        email_body: Email body text
        
    Returns:
        Sentiment category: "positive", "negative", or "neutral"
    """
    # Convert to lowercase for case-insensitive matching
    text = email_body.lower()
    
    # Count word occurrences
    positive_count = sum(1 for word in POSITIVE_WORDS if word in text)
    negative_count = sum(1 for word in NEGATIVE_WORDS if word in text)
    
    # Determine sentiment
    if positive_count > negative_count:
        return "positive"
    elif negative_count > positive_count:
        return "negative"
    else:
        return "neutral"


def extract_action_items(email_body: str) -> List[str]:
    """
    Extract potential action items from an email.
    
    In a real integration, this would be done by the AI model.
    This is a simplified version for demonstration purposes.
    
    Args:
        email_body: Email body text
        
    Returns:
        List of extracted action items
    """
    # Convert to lowercase and split into sentences
    text = email_body.lower()
    sentences = re.split(r'[.!?]+', text)
    
    # Extract sentences that likely contain action items
    action_items = []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and any(indicator in sentence for indicator in ACTION_INDICATORS):
            # Capitalize first letter and add period
            formatted_sentence = sentence[0].upper() + sentence[1:] + '.'
            action_items.append(formatted_sentence)
    
    return action_items