# integration/tests/test_e2e_email_assistant.py
import pytest
import os
import tempfile
from datetime import datetime, timedelta
from ai_email_assistant import AIEmailAssistant
from email_processor import analyze_sentiment, extract_action_items

@pytest.fixture
def temp_config():
    """Create a temporary configuration directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = os.path.join(temp_dir, "config.json")
        
        # Create a minimal mock configuration
        config_data = {
            "email": {
                "imap_host": "mock.imap.server",
                "imap_port": 993,
                "username": "test@example.com",
                "password": "mock_password"
            },
            "ai_client": {
                "api_key": "mock_api_key"
            }
        }
        
        with open(config_path, 'w') as f:
            import json
            json.dump(config_data, f)
            
        yield config_path

@pytest.fixture
def mock_email_assistant(temp_config):
    """Create an email assistant instance with mock mode enabled."""
    assistant = AIEmailAssistant(use_mock=True, ai_client_name="mock", config_path=temp_config)
    return assistant

def test_full_email_processing_workflow(mock_email_assistant):
    """Test the complete email processing workflow from start to finish."""
    assistant = mock_email_assistant
    
    # 1. Test fetching emails
    email_ids = assistant.fetch_emails(count=5)
    assert isinstance(email_ids, list)
    assert len(email_ids) == 5  # We requested 5 emails
    assert all(isinstance(email_id, str) for email_id in email_ids)
    
    # 2. Test getting email details
    if email_ids:
        sample_email_id = email_ids[0]
        email_details = assistant.get_email_details(sample_email_id)
        
        assert isinstance(email_details, dict)
        assert "id" in email_details
        assert "from" in email_details
        assert "subject" in email_details
        assert "body" in email_details
        
        # 3. Test sentiment analysis
        sentiment = analyze_sentiment(email_details["body"])
        assert sentiment in ["positive", "negative", "neutral"]
        
        # 4. Test action item extraction
        action_items = extract_action_items(email_details["body"])
        assert isinstance(action_items, list)
        
        # 5. Test response generation
        response = assistant.generate_response(sample_email_id)
        assert isinstance(response, str)
        assert len(response) > 0

def test_session_management(mock_email_assistant):
    """Test proper session management and cleanup."""
    assistant = mock_email_assistant
    
    # Start a new session
    user_id = "test_user_1"
    session_id = assistant.ai_client.start_new_session(user_id)
    assert session_id is not None
    
    # Verify session exists
    sessions = assistant.ai_client._sessions
    assert session_id in sessions
    assert sessions[session_id]["active"] is True
    
    # End the session
    result = assistant.ai_client.end_session(session_id)
    assert result is True
    
    # Verify session was cleaned up
    assert session_id not in sessions

def test_email_cleanup(mock_email_assistant):
    """Test proper cleanup of resources."""
    assistant = mock_email_assistant
    
    # Store references before cleanup
    fetcher = assistant.email_fetcher
    
    # Perform cleanup
    assistant.close()
    
    # Verify cleanup happened
    if hasattr(fetcher, "close"):
        assert getattr(fetcher, "closed", False) is True

def test_conversation_history(mock_email_assistant):
    """Test conversation history handling across multiple interactions."""
    assistant = mock_email_assistant
    
    # Start a new session
    user_id = "test_user_2"
    session_id = assistant.ai_client.start_new_session(user_id)
    
    try:
        # Send first message
        first_message = "Can you summarize my inbox?"
        first_response = assistant.ai_client.send_message(session_id, first_message)
        
        assert isinstance(first_response, dict)
        assert "response" in first_response
        
        # Send second message
        second_message = "What are the most important emails?"
        second_response = assistant.ai_client.send_message(session_id, second_message)
        
        assert isinstance(second_response, dict)
        assert "response" in second_response
        
        # Get conversation history
        history = assistant.ai_client.get_chat_history(session_id)
        assert isinstance(history, list)
        assert len(history) >= 3  # System message + 2 user messages + 2 AI responses
        
        # Check timestamps are in order
        timestamps = [msg.get("timestamp") for msg in history if msg.get("timestamp")]
        for i in range(1, len(timestamps)):
            assert timestamps[i] >= timestamps[i-1]
            
    finally:
        # Always end the session
        assistant.ai_client.end_session(session_id)

def test_error_handling(mock_email_assistant):
    """Test error handling for invalid operations."""
    assistant = mock_email_assistant
    
    # Test fetching emails with invalid count
    with pytest.raises(ValueError):
        assistant.fetch_emails(count=-1)
    
    # Test processing non-existent email
    with pytest.raises(ValueError):
        assistant.get_email_details("nonexistent_email_id")
    
    # Test sending message to closed session
    session_id = assistant.ai_client.start_new_session("test_user_3")
    assistant.ai_client.end_session(session_id)
    
    with pytest.raises(ValueError):
        assistant.ai_client.send_message(session_id, "This should fail")

def test_configuration_loading(temp_config):
    """Test configuration loading from file."""
    from config import load_config
    
    config = load_config(temp_config)
    assert isinstance(config, dict)
    
    # Check email configuration
    assert "email" in config
    assert "imap_host" in config["email"]
    assert "username" in config["email"]
    
    # Check AI client configuration
    assert "ai_client" in config
    assert "api_key" in config["ai_client"]

def test_multiple_users(mock_email_assistant):
    """Test concurrent usage by multiple users."""
    assistant = mock_email_assistant
    
    # User 1
    user1_id = "user_1"
    session1_id = assistant.ai_client.start_new_session(user1_id)
    
    # User 2
    user2_id = "user_2"
    session2_id = assistant.ai_client.start_new_session(user2_id)
    
    try:
        # Both users send messages simultaneously
        message1 = assistant.ai_client.send_message(session1_id, "User 1 message")
        message2 = assistant.ai_client.send_message(session2_id, "User 2 message")
        
        assert "response" in message1
        assert "response" in message2
        assert message1["response"] != message2["response"]
        
        # Check each user's history is separate
        history1 = assistant.ai_client.get_chat_history(session1_id)
        history2 = assistant.ai_client.get_chat_history(session2_id)
        
        assert len(history1) >= 2
        assert len(history2) >= 2
        
    finally:
        # Clean up sessions
        assistant.ai_client.end_session(session1_id)
        assistant.ai_client.end_session(session2_id)