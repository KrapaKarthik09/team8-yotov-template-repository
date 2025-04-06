# Team 8 : Mailing Interface 

# Description

This repository contains the API definitions and a placeholder implementation for an email inbox client. It utilizes Python `Protocol` classes to define standardized interfaces for email messages, attachments, and the inbox client itself.

### Scope

This project defines an interface for an inbox client with the following capabilities:

#### In Scope:

* Basic email message retrieval.
* Email folder/label support.
* Message search functionality.
* Attachment handling.
* Message read/unread status management.

#### Out of Scope:

* Message composition and sending.
* Complex filtering rules.
* Server-side folder management.
* Account setup and configuration.
* Security features beyond basic authentication.

### API Protocols and Methods

The API defines the following protocols and their methods/properties:

**`Attachment` Protocol:**

| Property       | Return Type | Description                             |
| :------------- | :---------- | :-------------------------------------- |
| `filename`     | `str`       | The filename of the attachment.         |
| `content_type` | `str`       | The content type of the attachment.     |
| `size`         | `int`       | The size of the attachment in bytes.    |
| `get_content()`| `bytes`     | Returns the content of the attachment. |

**`Message` Protocol:**

| Property/Method    | Return Type        | Description                                  |
| :----------------- | :----------------- | :------------------------------------------- |
| `id`               | `str`              | The unique identifier of the message.        |
| `from_`            | `str`              | The sender of the message.                   |
| `to`               | `str`              | The recipient of the message.                |
| `cc`               | `Optional[str]`    | The CC recipients of the message, if any.    |
| `bcc`              | `Optional[str]`    | The BCC recipients of the message, if any.   |
| `date`             | `str`              | The date of the message.                     |
| `subject`          | `str`              | The subject of the message.                  |
| `body`             | `str`              | The body of the message.                     |
| `attachments`      | `List[Attachment]` | A list of attachments.                       |
| `is_read`          | `bool`             | Whether the message has been read.           |
| `mark_as_read()`   | `None`             | Marks the message as read.                   |
| `mark_as_unread()` | `None`             | Marks the message as unread.                 |

**`Client` Protocol:**

| Method                             | Parameters                               | Return Type         | Description                                       |
| :--------------------------------- | :--------------------------------------- | :------------------ | :------------------------------------------------ |
| `get_messages(limit, folder)`      | `limit: Optional[int]`, `folder: str`  | `Iterator[Message]` | Fetches messages from a specified folder.         |
| `search_messages(query, folder)`   | `query: str`, `folder: str`              | `Iterator[Message]` | Searches for messages matching the query.         |
| `get_folders()`                    | None                                     | `List[str]`         | Returns a list of available mail folders.         |

**Helper Function:**

| Function      | Return Type | Description                                    |
| :------------ | :---------- | :--------------------------------------------- |
| `get_client()`| `Client`    | Returns an instance of a mail client implementation. |

### Usage

*(Note: The implementation details in `my_inbox_impl` are currently placeholders. The following examples illustrate how the API is intended to be used once implemented, based on the API definition and test structure.)*

#### Getting a Client Instance

```python
import my_inbox_api

# This function will be provided by the implementation package
client = my_inbox_api.get_client()

# Listing Folders
folders = client.get_folders() 
print("Available folders:", folders) 

# Reading Messages
# Get top 10 messages from INBOX
messages = client.get_messages(folder="INBOX", limit=10)
for message in messages: 
    print(f"From: {message.from_}") 
    print(f"Subject: {message.subject}") 
    print(f"Read Status: {message.is_read}") 

# Searching Messages
search_results = client.search_messages(query="important project", folder="INBOX")
for message in search_results: 
    print(f"Found matching message: {message.subject}") 

```

## Directory Structure

```
.
├── src/                    # Source code directory
│   ├── calculator/         # Calculator component
│   │   ├── calculator.py   # Implementation
│   │   ├── __init__.py     # Component API
│   │   ├── pyproject.toml  # Component dependencies
│   │   └── tests/          # Component unit tests
│   ├── logger/             # Logger component
│   │   └── ...
│   ├── notifier/           # Notifier component
│   │   └── ...
│   └── __init__.py         # Package exports
|
├── .circleci/              # CircleCI configuration
├── .github/                # GitHub templates
│   ├── ISSUE_TEMPLATE/     # Issue templates
│   │   ├── bug_report.md   # Bug report template
│   │   └── feature_request.md  # Feature request template
│   └── pull_request_template.md
├── pyproject.toml          # Project configuration
├── component.md            # Component documentation
├── LICENSE                 # Open source license (MIT)
├── .gitignore              # Python-specific gitignore
└── README.md               # This file

## Getting Started

### Prerequisites

- Python 3.11 or higher
- UV package manager

### Installation

1. Install UV (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh

2. Clone this template:
   ```bash
   git clone https://github.com/yourusername/team8-yotov-template-repository.git
   cd team8-yotov-template-repository
   ```

3. Install dependencies:
   ```bash
   uv sync
   uv pip install -e .
   ```

### Running Tests

#### Run all tests:
```bash
uv run pytest
```

#### Run a specific component's unit tests:
```bash
uv run pytest my_inbox_api/tests/
```


#### Run tests with coverage:
```bash
uv run pytest --cov=src
```

### Code Quality

#### Run linting with Ruff:
```bash
uv run ruff check .
```

#### Run type checking with MyPy:
```bash
uv run mypy src tests
```

## CI/CD Pipeline

This template is configured with CircleCI for continuous integration. The pipeline:

1. Installs dependencies
2. Runs linting with ruff
3. Runs type checking with mypy
4. Runs all tests with pytest
5. Generates code coverage reports

## Components

This template includes two components:

1. **my_inbox_api** : Inbox API
2. **my_inbox_impl**: Inbox Implemenation

For detailed information about the component architecture, see [component.md](./component.md).

## Templates

GitHub templates are included to standardize:
- Pull requests
- Bug reports
- Feature requests

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.