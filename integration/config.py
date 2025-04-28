"""Configuration settings for the AI Email Assistant integration."""

import os
from typing import Dict, Any, Optional
import json


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from a JSON file or environment variables.
    
    Args:
        config_path: Path to JSON configuration file (optional)
        
    Returns:
        Dictionary containing configuration settings
    """
    config = {
        "use_mock": True,  # Default to using mock data
        "ai_client": {
            "name": "mock",  # Default to mock AI client
            "api_key": os.environ.get("CEREBRAS_API_KEY", "")
        },
        "email": {
            "use_mock": True,  # Default to using mock email fetcher
            "imap": {
                "host": os.environ.get("EMAIL_IMAP_HOST", ""),
                "port": os.environ.get("EMAIL_IMAP_PORT", "993"),
                "username": os.environ.get("EMAIL_USERNAME", ""),
                "password": os.environ.get("EMAIL_PASSWORD", "")
            }
        }
    }
    
    # Load from file if provided
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r') as f:
            file_config = json.load(f)
            # Merge configurations
            config = deep_merge(config, file_config)
    
    return config


def deep_merge(base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively merge two dictionaries.
    
    Args:
        base: Base dictionary
        update: Dictionary with values to update
        
    Returns:
        Merged dictionary
    """
    result = base.copy()
    
    for key, value in update.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    
    return result


def create_default_config(output_path: str) -> None:
    """
    Create a default configuration file.
    
    Args:
        output_path: Path where to save the configuration file
    """
    config = {
        "use_mock": True,
        "ai_client": {
            "name": "mock",
            "api_key": ""
        },
        "email": {
            "use_mock": True,
            "imap": {
                "host": "imap.example.com",
                "port": "993",
                "username": "user@example.com",
                "password": ""
            }
        }
    }
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # Write config file
    with open(output_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Default configuration created at {output_path}")