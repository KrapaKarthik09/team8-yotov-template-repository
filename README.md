# Team 8 : Mailing Interface 

## Description

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
| `cc`               | `list[str]`        | The CC recipients of the message.            |
| `bcc`              | `list[str]`        | The BCC recipients of the message.           |
| `date`             | `str`              | The date of the message.                     |
| `subject`          | `str`              | The subject of the message.                  |
| `body`             | `str`              | The body of the message.                     |
| `attachments`      | `list[Attachment]` | A list of attachments.                       |
| `is_read`          | `bool`             | Whether the message has been read.           |
| `mark_as_read()`   | `None`             | Marks the message as read.                   |
| `mark_as_unread()` | `None`             | Marks the message as unread.                 |

**`Client` Protocol:**

| Method                             | Parameters                               | Return Type         | Description                                       |
| :--------------------------------- | :--------------------------------------- | :------------------ | :------------------------------------------------ |
| `get_messages(limit, folder)`      | `limit: Optional[int]`, `folder: str`  | `Iterator[Message]` | Fetches messages from a specified folder.         |
| `search_messages(query, folder)`   | `query: str`, `folder: str`              | `Iterator[Message]` | Searches for messages matching the query.         |
| `get_folders()`                    | None                                     | `list[str]`         | Returns a list of available mail folders.         |

**Helper Function:**

| Function      | Return Type | Description                                    |
| :------------ | :---------- | :--------------------------------------------- |
| `get_client()`| `Client`    | Returns an instance of a mail client implementation. |

### Usage

Please refer to the implementation documentation for example usage.

## Getting Started

### Prerequisites

- Python 3.12 or higher
- UV package manager

### Installation

1. Install UV (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Clone this repository and install dependencies. For development, use:
   ```bash
   uv sync -e dev
   ```

See the implementation package for complete usage information.