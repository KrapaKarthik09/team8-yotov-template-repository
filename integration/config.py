"""Configuration settings for the AI Email Assistant integration."""

import os
from typing import Dict, Any, Optional
import json

# Import constants
from config_constants import (
    DEFAULT_USE_MOCK, DEFAULT_AI_CLIENT_NAME, DEFAULT_EMAIL_USE_MOCK,
    CONFIG_USE_MOCK, CONFIG_AI_CLIENT, CONFIG_AI_CLIENT_NAME, CONFIG_AI_CLIENT_API_KEY,
    CONFIG_EMAIL, CONFIG_EMAIL_USE_MOCK, CONFIG_EMAIL_IMAP,
    CONFIG_EMAIL_IMAP_HOST, CONFIG_EMAIL_IMAP_PORT, CONFIG_EMAIL_IMAP_USERNAME, CONFIG_EMAIL_IMAP_PASSWORD,
    ENV_CEREBRAS_API_KEY, ENV_EMAIL_IMAP_HOST, ENV_EMAIL_IMAP_PORT, ENV_EMAIL_USERNAME, ENV_EMAIL_PASSWORD,
    DEFAULT_IMAP_PORT, DEFAULT_IMAP_HOST, DEFAULT_EMAIL_USERNAME
)

def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from a JSON file or environment variables.

    Args:
        config_path: Path to JSON configuration file (optional)

    Returns:
        Dictionary containing configuration settings
    """
    config = {
        CONFIG_USE_MOCK: DEFAULT_USE_MOCK,
        CONFIG_AI_CLIENT: {
            CONFIG_AI_CLIENT_NAME: DEFAULT_AI_CLIENT_NAME,
            CONFIG_AI_CLIENT_API_KEY: os.environ.get(ENV_CEREBRAS_API_KEY, "")
        },
        CONFIG_EMAIL: {
            CONFIG_EMAIL_USE_MOCK: DEFAULT_EMAIL_USE_MOCK,
            CONFIG_EMAIL_IMAP: {
                CONFIG_EMAIL_IMAP_HOST: os.environ.get(ENV_EMAIL_IMAP_HOST, ""),
                CONFIG_EMAIL_IMAP_PORT: os.environ.get(ENV_EMAIL_IMAP_PORT, DEFAULT_IMAP_PORT),
                CONFIG_EMAIL_IMAP_USERNAME: os.environ.get(ENV_EMAIL_USERNAME, ""),
                CONFIG_EMAIL_IMAP_PASSWORD: os.environ.get(ENV_EMAIL_PASSWORD, "")
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
        CONFIG_USE_MOCK: DEFAULT_USE_MOCK,
        CONFIG_AI_CLIENT: {
            CONFIG_AI_CLIENT_NAME: DEFAULT_AI_CLIENT_NAME,
            CONFIG_AI_CLIENT_API_KEY: ""
        },
        CONFIG_EMAIL: {
            CONFIG_EMAIL_USE_MOCK: DEFAULT_EMAIL_USE_MOCK,
            CONFIG_EMAIL_IMAP: {
                CONFIG_EMAIL_IMAP_HOST: DEFAULT_IMAP_HOST,
                CONFIG_EMAIL_IMAP_PORT: DEFAULT_IMAP_PORT,
                CONFIG_EMAIL_IMAP_USERNAME: DEFAULT_EMAIL_USERNAME,
                CONFIG_EMAIL_IMAP_PASSWORD: ""
            }
        }
    }

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # Write config file
    with open(output_path, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"Default configuration created at {output_path}")
