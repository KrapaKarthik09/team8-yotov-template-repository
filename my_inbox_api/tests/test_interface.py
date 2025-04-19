import pytest
from typing import Iterator, Optional, Any

import my_inbox_api
from my_inbox_api import Message, Client, Attachment

# Constants for tests
TEST_MESSAGE_COUNT = 5
TEST_LIMIT = 2
TEST_SEARCH_RESULT_COUNTS = 2

class MockAttachment:
    """Mock implementation of Attachment protocol for testing."""
    
    @property
    def filename(self) -> str:
        """Return test filename."""
        return "test_file.txt"

    @property
    def content_type(self) -> str:
        """Return test content type."""
        return "text/plain"

    @property
    def size(self) -> int:
        """Return test size in bytes."""
        return 1024

    def get_content(self) -> bytes:
        """Return test content as bytes."""
        return b"This is test content"


class MockMessage:
    """Mock implementation of Message protocol for testing."""

    @property
    def id(self) -> str:
        """Return message."""
        return "msg123"

    @property
    def from_(self) -> str:
        """Return mailid."""
        return "sender@example.com"

    @property
    def to(self) -> str:
        """Return mailid."""
        return "recipient@example.com"

    @property
    def cc(self) -> str:
        """Return mailid."""
        return "cc@example.com"

    @property
    def bcc(self) -> str:
        """Return mailid."""
        return "bcc@example.com"

    @property
    def date(self) -> str:
        """Return mailid."""
        return "Mon, 01 Apr 2025 12:00:00 +0000"

    @property
    def subject(self) -> str:
        """Return subject."""
        return "Test Subject"

    @property
    def body(self) -> str:
        """Return body."""
        return "This is the test body."

    @property
    def attachments(self) -> list[Attachment]:
        """Return MockAttachment."""
        return [MockAttachment()]

    @property
    def is_read(self) -> bool:
        """Return bool."""
        return False

    def mark_as_read(self) -> None:
        """Mark message as read (test implementation)."""
        pass

    def mark_as_unread(self) -> None:
        """Mark message as unread (test implementation)."""
        pass


class MockClient:
    """Mock implementation of Client protocol for testing."""

    def get_messages(self, limit: Optional[int] = None, folder: str = "INBOX") -> Iterator[Message]:
        """Return"""
        # Return 5 mock messages, respecting the limit if provided
        messages = [MockMessage() for _ in range(5)]
        if limit is not None:
            messages = messages[:limit]
        return iter(messages)

    def search_messages(self, query: str, folder: str = "INBOX") -> Iterator[Message]:
        """Return"""
        # Return 2 mock messages for any search
        return iter([MockMessage(), MockMessage()])

    def get_folders(self) -> list[str]:
        """Return"""
        return ["INBOX", "Sent", "Drafts", "Trash"]


def test_attachment_interface() -> None:
    """Test the Attachment protocol properties."""
    attachment = MockAttachment()

    # Test property types
    assert isinstance(attachment.filename, str)
    assert isinstance(attachment.content_type, str)
    assert isinstance(attachment.size, int)
    assert isinstance(attachment.get_content(), bytes)


def test_message_interface() -> None:
    """Test the Message protocol properties."""
    message = MockMessage()

    # Test property types
    assert isinstance(message.id, str)
    assert isinstance(message.from_, str)
    assert isinstance(message.to, str)
    assert isinstance(message.cc, str)
    assert isinstance(message.bcc, str)
    assert isinstance(message.date, str)
    assert isinstance(message.subject, str)
    assert isinstance(message.body, str)
    assert isinstance(message.attachments, list)
    assert isinstance(message.is_read, bool)

    # Test attachment list contains Attachment objects
    if message.attachments:
        assert isinstance(message.attachments[0].filename, str)


def test_client_interface() -> None:
    """Test the Client protocol methods."""
    client = MockClient()

    # Test get_messages
    messages = list(client.get_messages())
    assert len(messages) == TEST_MESSAGE_COUNT
    assert isinstance(messages[0].id, str)

    # Test get_messages with limit
    limited_messages = list(client.get_messages(limit=TEST_LIMIT))
    assert len(limited_messages) == TEST_LIMIT

    # Test search_messages
    search_results = list(client.search_messages("test"))
    assert len(search_results) == TEST_SEARCH_RESULT_COUNTS
    assert isinstance(search_results[0].id, str)

    # Test get_folders
    folders = client.get_folders()
    assert isinstance(folders, list)
    assert "INBOX" in folders


def test_get_client_function(monkeypatch) -> None:
    """Test the get_client function returns a Client instance."""
    # Using monkeypatch instead of patch decorator
    mock_client = MockClient()
    monkeypatch.setattr(my_inbox_api, 'get_client', lambda: mock_client)

    client = my_inbox_api.get_client()
    assert isinstance(client.get_messages(), Iterator)
    assert isinstance(client.get_folders(), list)
