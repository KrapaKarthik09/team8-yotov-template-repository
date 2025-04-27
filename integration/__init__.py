# __init__.py
"""
AI Email Assistant Integration Package.

This package integrates the Cerebras AI Conversation Client with 
MyInbox email implementation.
"""

from .ai_email_assistant import AIEmailAssistant
from .email_processor import (
    extract_entities, extract_dates, format_email_for_ai,
    generate_email_response_template, analyze_sentiment,
    extract_action_items
)
from .config import load_config, create_default_config

__all__ = [
    'AIEmailAssistant',
    'extract_entities',
    'extract_dates',
    'format_email_for_ai',
    'generate_email_response_template',
    'analyze_sentiment',
    'extract_action_items',
    'load_config',
    'create_default_config'
]