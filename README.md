# 📨 AI Email Assistant Integration README

This project integrates an AI conversation client with an email system to provide intelligent email processing capabilities. The integration allows the assistant to fetch emails, analyze their content using AI models, generate responses, extract entities and action items, and summarize conversations.

The system is built on two core components:
- **Email Client (`my_inbox_impl`)** – A flexible email interface that supports mock and real IMAP-based clients.
- **AI Conversation Client (`ai-client-component`)** – An AI model interaction module that uses the Cerebras API or other LLMs.

This README provides a high-level overview of the architecture, key modules, and how integration tests validate the system's behavior.

---

## 🧠 Overview of Integration

### Components Involved

1. **Email Client (`my_inbox_impl`)**
   - Handles connection to email servers via IMAP or mocks.
   - Provides methods to:
     - Fetch emails
     - Retrieve message details
     - Search messages
     - Manage folders
   - Supports both real and mock modes for development/testing.

2. **AI Conversation Client (`ai-client-component`)**
   - Wraps the Cerebras LLM API.
   - Provides methods to:
     - Start/end sessions
     - Send prompts
     - Retrieve chat history
     - Generate summaries/responses
   - Can operate in mock mode when no API key is available.

3. **Integration Layer (`integration.ai_email_assistant`)**
   - Combines the two components into a single `AIEmailAssistant`.
   - Key features:
     - Fetch and process emails using AI
     - Generate AI-powered email responses
     - Extract entities, dates, and action items from emails
     - Summarize email threads
     - Write spam detection results to CSV

---

## 🔗 How the Integration Works

The integration between the email and AI systems is orchestrated by the `AIEmailAssistant` class. Here's a breakdown of how they interact:

```
+------------------+ +-----------------------+ +----------------------------+
|                  | |                       | |                            |
| Email Client     |<----->| AI Email Assistant |<----->| AI Conversation Client |
| (IMAP/Mock)      | fetch | (Integration Layer) | prompt| (Cerebras/OpenAI/etc.) |
|                  | email | | ai |                |
+------------------+ +-----------------------+ +----------------------------+
                     ↑       ↑       ↑
                     |       |       |
                     Fetch emails, get   Process emails  Send prompts to AI model,
                     message details     with AI,        receive completions,
                     and manage folders  generate        summarize conversations,
                                         responses,      detect spam
                                         extract 
                                         action items
```

---

## 🔄 Component Interaction Flow

### 1. Initialization

When you create an instance of `AIEmailAssistant`, it initializes both the email and AI clients:

```python
assistant = AIEmailAssistant(use_mock=True, ai_client_name="mock")
```

- Uses configuration files or defaults.
- In mock mode, no real network calls are made.

### 2. Fetching Emails

The assistant uses the email client to fetch messages from the inbox:

```python
email_ids = assistant.fetch_emails(count=5)
```

- Internally: Calls `email_client.get_messages()` or its mock counterpart.
- Returns a list of message IDs or metadata depending on the use case.

### 3. Retrieving Email Details

Once emails are fetched, their content can be retrieved individually:

```python
details = assistant.get_email_details(email_id)
```

- Returns structured data including:
  - ID
  - From
  - To
  - Subject
  - Body
  - Date, etc.

### 4. Processing with AI

The email body is passed to the AI conversation client to generate a response:

```python
response = assistant.generate_response(email_id)
```

Internally:
- Retrieves the body from email details
- Sends it as a prompt to `ai_client.send_message(session_id, prompt)`

### 5. Text Processing Utilities

Additional tools help analyze unstructured email text:

```python
action_items = assistant.extract_action_items(email_body)
entities = assistant.extract_entities(email_body)
dates = assistant.extract_dates(email_body)
```

- These functions reside in `email_processor.py`
- Uses regex or NLP rules to parse the email body

### 6. Session Management

Each user interaction with the AI is tracked via a session:

```python
session_id = ai_client.start_new_session(user_id="user_1")
history = ai_client.get_chat_history(session_id)
ai_client.end_session(session_id)
```

- Ensures separation of conversations across users
- Maintains context within a single interaction thread

### 7. Cleanup & Resource Management

After processing is complete, resources should be released properly:

```python
assistant.close()
```

- Safely ends all active AI sessions
- Closes the IMAP connection if applicable

---

## 🧪 Testing the Integration

All tests live under the `integration/tests/` directory and are implemented using pytest.

### Test Types

1. `test_integration.py`
   - Tests full workflow including spam detection

2. `test_email_processor.py`
   - Unit tests for entity/date/action extraction

3. `test_e2e_email_assistant.py`
   - End-to-end test covering all operations

### Mock Mode Usage in Tests

- All tests use `use_mock=True` to avoid hitting external APIs
- Simulated email data ensures consistent and fast execution
- AI responses are pre-defined to verify correctness without relying on model output variability

### Example E2E Test: Spam Detection

```python
def test_spam_detection_with_mock_data(assistant, output_csv, mocker):
    # Mock spam-like emails
    mock_emails = [
        {'id': 'email1', 'from': 'scammer@example.com', 'subject': 'Win $1M Now!', ...},
        {'id': 'email2', 'from': 'team@company.com', 'subject': 'Weekly Sync', ...}
    ]

    # Patch email fetching
    mocker.patch.object(assistant.email_client, 'get_messages', return_value=mock_emails)

    # Run spam detection
    result_file = assistant.detect_spam_and_export(output_csv)

    # Assert CSV written successfully
    assert os.path.exists(result_file)
```

This demonstrates how integration tests validate business logic using controlled inputs.

---

## 🛠️ Running the Tests

### Prerequisites

- Python 3.12+
- pytest, coverage, uv, mypy, etc.

### Install Dependencies

```bash
cd integration
pip install -e .
```

### Run Tests

```bash
cd integration/tests
pytest test_e2e_email_assistant.py -v
```

### Collect Coverage

```bash
pytest --cov=integration tests/
```

---

## 📁 Directory Structure

```
integration/
├── ai_email_assistant.py       # Main integration class
├── email_processor.py          # Text analysis utilities
├── config.py                   # Configuration handling
├── __init__.py                 # Package exports
├── demo.py                     # Interactive usage example
└── tests/
    ├── test_integration.py     # Core integration tests
    ├── test_email_processor.py # Extraction unit tests
    └── test_e2e_email_assistant.py # Custom E2E tests
```

---

## 🧩 Dependencies

- `my_inbox_api`: Defines the email client interface
- `my_inbox_impl`: Implements real/mock email clients
- `ai-client-component`: Manages AI conversation with Cerebras
- `components.ai_conversation_client`: Used by AIEmailAssistant

These are managed through uv as part of the workspace defined in `pyproject.toml`.

---

## 🧪 Future Enhancements

- Add support for sending generated responses as actual replies
- Integrate with spam filtering models for more accurate classification
- Add web UI to visualize email summaries and action items
- Support multiple AI backends (e.g., OpenAI, Anthropic)

---

## 📝 License

MIT License – See LICENSE for details.
