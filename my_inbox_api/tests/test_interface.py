import unittest
from unittest.mock import MagicMock, patch
from typing import Iterator, List

# Import your interface definitions
import my_inbox_api
from my_inbox_api import Message, Client, Attachment


class MockAttachment(MagicMock):
    """Mock implementation of Attachment protocol for testing."""
    
    @property
    def filename(self) -> str:
        return "test_file.txt"
    
    @property
    def content_type(self) -> str:
        return "text/plain"
    
    @property
    def size(self) -> int:
        return 1024
    
    def get_content(self) -> bytes:
        return b"This is test content"


class MockMessage(MagicMock):
    """Mock implementation of Message protocol for testing."""
    
    @property
    def id(self) -> str:
        return "msg123"
    
    @property
    def from_(self) -> str:
        return "sender@example.com"
    
    @property
    def to(self) -> str:
        return "recipient@example.com"
    
    @property
    def cc(self) -> str:
        return "cc@example.com"
    
    @property
    def bcc(self) -> str:
        return "bcc@example.com"
    
    @property
    def date(self) -> str:
        return "Mon, 01 Apr 2025 12:00:00 +0000"
    
    @property
    def subject(self) -> str:
        return "Test Subject"
    
    @property
    def body(self) -> str:
        return "This is the test body."
    
    @property
    def attachments(self) -> List[Attachment]:
        return [MockAttachment()]
    
    @property
    def is_read(self) -> bool:
        return False
    
    def mark_as_read(self) -> None:
        pass
    
    def mark_as_unread(self) -> None:
        pass


class MockClient(MagicMock):
    """Mock implementation of Client protocol for testing."""
    
    def get_messages(self, limit=None, folder="INBOX") -> Iterator[Message]:
        # Return 5 mock messages, respecting the limit if provided
        messages = [MockMessage() for _ in range(5)]
        if limit is not None:
            messages = messages[:limit]
        return iter(messages)
    
    def search_messages(self, query, folder="INBOX") -> Iterator[Message]:
        # Return 2 mock messages for any search
        return iter([MockMessage(), MockMessage()])
    
    def get_folders(self) -> List[str]:
        return ["INBOX", "Sent", "Drafts", "Trash"]


class TestInboxInterface(unittest.TestCase):
    """Test cases for the inbox client interface."""
    
    def test_attachment_interface(self):
        """Test the Attachment protocol properties."""
        attachment = MockAttachment()
        
        # Test property types
        self.assertIsInstance(attachment.filename, str)
        self.assertIsInstance(attachment.content_type, str)
        self.assertIsInstance(attachment.size, int)
        self.assertIsInstance(attachment.get_content(), bytes)
    
    def test_message_interface(self):
        """Test the Message protocol properties."""
        message = MockMessage()
        
        # Test property types
        self.assertIsInstance(message.id, str)
        self.assertIsInstance(message.from_, str)
        self.assertIsInstance(message.to, str)
        self.assertIsInstance(message.cc, str)
        self.assertIsInstance(message.bcc, str)
        self.assertIsInstance(message.date, str)
        self.assertIsInstance(message.subject, str)
        self.assertIsInstance(message.body, str)
        self.assertIsInstance(message.attachments, list)
        self.assertIsInstance(message.is_read, bool)
        
        # Test attachment list contains Attachment objects
        if message.attachments:
            self.assertIsInstance(message.attachments[0].filename, str)
    
    def test_client_interface(self):
        """Test the Client protocol methods."""
        client = MockClient()
        
        # Test get_messages
        messages = list(client.get_messages())
        self.assertEqual(len(messages), 5)
        self.assertIsInstance(messages[0].id, str)
        
        # Test get_messages with limit
        limited_messages = list(client.get_messages(limit=2))
        self.assertEqual(len(limited_messages), 2)
        
        # Test search_messages
        search_results = list(client.search_messages("test"))
        self.assertEqual(len(search_results), 2)
        self.assertIsInstance(search_results[0].id, str)
        
        # Test get_folders
        folders = client.get_folders()
        self.assertIsInstance(folders, list)
        self.assertIn("INBOX", folders)
    
    @patch('my_inbox_api.get_client')
    def test_get_client_function(self, mock_get_client):
        """Test the get_client function returns a Client instance."""
        mock_get_client.return_value = MockClient()
        
        client = my_inbox_api.get_client()
        self.assertIsInstance(client.get_messages(), Iterator)
        self.assertIsInstance(client.get_folders(), list)


if __name__ == '__main__':
    unittest.main()