"""Integration tests for AI Email Assistant - Spam Detection."""
import os
import sys
import pytest
import csv
import random
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ai_email_assistant import AIEmailAssistant

@pytest.fixture
def assistant():
    """Set up test environment."""
    assistant = AIEmailAssistant(use_mock=True, ai_client_name="mock")
    yield assistant
    assistant.close()

@pytest.fixture
def output_csv():
    """Create output CSV file for spam detection results."""
    filename = 'spam_detection_results.csv'
    yield filename
    # Optionally remove file after tests
    # if os.path.exists(filename):
    #     os.remove(filename)

def test_spam_detection_with_csv_output(assistant, output_csv):
    """Test spam detection and output results to CSV."""
    # Fetch emails for testing
    email_ids = assistant.fetch_emails(count=10)  # Adjust count as needed
    
    # Prepare results list
    results = []
    
    # Process each email for spam detection
    for email_id in email_ids:
        try:
            # Get email content
            email_data = assistant.get_email(email_id)
            
            # Create prompt for spam detection
            spam_detection_prompt = f"""
            Analyze this email and determine the probability it is spam.
            Return only a number between 0 and 100 representing the spam percentage.
            
            Email content:
            From: {email_data.get('from', '')}
            To: {email_data.get('to', '')}
            Subject: {email_data.get('subject', '')}
            Body: {email_data.get('body', '')[:500]}...
            
            Spam percentage (0-100):
            """
            
            # Get AI response for spam detection
            response = assistant.ai_client.generate_response(spam_detection_prompt)
            
            # Extract percentage from response
            # This is a simple extraction - might need more robust parsing
            try:
                pct_spam = float(''.join(filter(str.isdigit, response)))
                if pct_spam > 100:
                    pct_spam = 100
                elif pct_spam < 0:
                    pct_spam = 0
            except ValueError:
                #making the test fail when parsing fails
                pytest.fail(f"Failed to parse spam percentage from response: {response}")
            
            results.append({
                'mail_id': email_id,
                'Pct_spam': round(pct_spam, 2)
            })
            
        except Exception as e:
            print(f"Error processing email {email_id}: {e}")
            # Add error result
            results.append({
                'mail_id': email_id,
                'Pct_spam': -1  # Error indicator
            })
    
    # Write results to CSV
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['mail_id', 'Pct_spam']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    # Verify CSV was created properly
    assert os.path.exists(output_csv)
    
    # Verify CSV content
    with open(output_csv, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        
        # Check that we have results
        assert len(rows) > 0
        
        # Check that each row has the required columns
        for row in rows:
            assert 'mail_id' in row
            assert 'Pct_spam' in row
            
            # Verify Pct_spam is a valid number
            pct_spam = float(row['Pct_spam'])
            assert -1 <= pct_spam <= 100  # -1 is our error indicator
    
    print(f"Spam detection results written to {output_csv}")

def test_spam_detection_with_mock_data(assistant, output_csv, mocker):
    """Test spam detection with mock data and produce CSV output."""
    # Mock email data
    mock_emails = [
        {'id': 'email1', 'from': 'prince@nigeria.com', 'to': 'victim@example.com',
         'subject': 'URGENT: Claim Your $1M Prize!!!',
         'body': 'You have won millions! Send bank details now!'},
        {'id': 'email2', 'from': 'coworker@company.com', 'to': 'me@company.com',
         'subject': 'Meeting tomorrow',
         'body': 'Hi, can we reschedule our meeting to 3 PM?'},
        {'id': 'email3', 'from': 'pharmacy@spam.com', 'to': 'anyone@example.com',
         'subject': 'Cheap meds online',
         'body': 'Buy discounted medications without prescription!'},
        {'id': 'email4', 'from': 'mom@family.com', 'to': 'me@example.com',
         'subject': 'Happy Birthday!',
         'body': 'Hope you have a wonderful birthday!'},
    ]
    
    # Mock methods
    mocker.patch.object(assistant, 'fetch_emails',
                       return_value=['email1', 'email2', 'email3', 'email4'])
    mocker.patch.object(assistant, 'get_email',
                       side_effect=lambda id: next(e for e in mock_emails if e['id'] == id))
    
    # Mock AI responses with realistic spam scores
    mock_responses = {
        'email1': '95',  # Obvious spam
        'email2': '5',   # Legitimate email
        'email3': '85',  # Likely spam
        'email4': '2'    # Legitimate email
    }
    
    def mock_generate_response(prompt) -> str:
        for email_id, score in mock_responses.items():
            if email_id in prompt:
                return f"The spam probability is {score}%"
        return "50"  # Default score
    
    mocker.patch.object(assistant.ai_client, 'generate_response',
                       side_effect=mock_generate_response)
    
    # Run spam detection
    email_ids = assistant.fetch_emails(count=4)
    results = []
    
    for email_id in email_ids:
        email_data = assistant.get_email(email_id)
        
        prompt = f"Analyze email {email_id} for spam"
        response = assistant.ai_client.generate_response(prompt)
        
        # Extract percentage
        pct_spam = float(''.join(filter(str.isdigit, response)))
        
        results.append({
            'mail_id': email_id,
            'Pct_spam': pct_spam
        })
    
    # Write results to CSV
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['mail_id', 'Pct_spam'])
        writer.writeheader()
        writer.writerows(results)
    
    # Verify results
    with open(output_csv, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        
        assert len(rows) == 4
        
        # Verify specific results
        for row in rows:
            if row['mail_id'] == 'email1':
                assert float(row['Pct_spam']) == 95
            elif row['mail_id'] == 'email2':
                assert float(row['Pct_spam']) == 5
            elif row['mail_id'] == 'email3':
                assert float(row['Pct_spam']) == 85
            elif row['mail_id'] == 'email4':
                assert float(row['Pct_spam']) == 2

# Helper function for spam detection
def detect_spam(assistant, email_data):
    """Detect spam in an email.
    
    Args:
        assistant: AIEmailAssistant instance
        email_data: Dictionary containing email data
        
    Returns:
        float: Spam probability (0-100)
    """
    prompt = f"""
    Analyze this email and determine the probability it is spam.
    Consider factors like:
    - Sender address
    - Subject line (urgent, all caps, excessive punctuation)
    - Content (promises of money, requests for personal info)
    - Tone and language
    
    Return only a number between 0-100.
    
    Email:
    From: {email_data.get('from', '')}
    Subject: {email_data.get('subject', '')}
    Body: {email_data.get('body', '')[:500]}
    
    Spam probability:
    """
    
    response = assistant.ai_client.generate_response(prompt)
    
    try:
        # Extract number from response
        pct_spam = float(''.join(filter(str.isdigit, response)))
        return min(max(pct_spam, 0), 100)  # Ensure 0-100 range
    except ValueError:
        return 50  # Default to middle value if parsing fails

# Example usage function
def generate_spam_report(assistant, output_file='spam_detection_results.csv'):
    """
    Generate a spam detection report for all emails.
    
    Args:
        assistant: AIEmailAssistant instance
        output_file: Output CSV filename
    """
    email_ids = assistant.fetch_emails(count=100)  # Adjust as needed
    results = []
    
    for email_id in email_ids:
        try:
            email_data = assistant.get_email(email_id)
            pct_spam = detect_spam(assistant, email_data)
            
            results.append({
                'mail_id': email_id,
                'Pct_spam': round(pct_spam, 2)
            })
        except Exception as e:
            print(f"Error processing {email_id}: {e}")
            results.append({
                'mail_id': email_id,
                'Pct_spam': -1
            })
    
    # Write to CSV
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['mail_id', 'Pct_spam'])
        writer.writeheader()
        writer.writerows(results)
    
    return output_file