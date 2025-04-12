import unittest
import tempfile
import os
import shutil
from pathlib import Path

from my_inbox_impl import get_client, ClientImpl, MessageImpl, AttachmentImpl
from my_inbox_impl.mail_fetcher import MockFetcher

class TestInboxImplementation(unittest.TestCase):
    """Test cases for the inbox implementation."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        self.client = ClientImpl(data_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        # Remove temporary directory
        shutil.rmtree(self.test_dir)
    
    def test_get_client(self):
        """Test that get_client returns a valid Client instance."""
        client = get_client()
        self.assertIsNotNone(client)
        
        # Check that it has the required methods
        self.assertTrue(hasattr(client, 'get_messages'))
        self.assertTrue(hasattr(client, 'search_messages'))
        self.assertTrue(hasattr(client, 'get_folders'))
    
    def test_attachment_implementation(self):
        """Test the AttachmentImpl class."""
        test_content = b"Test content for the attachment"
        attachment = AttachmentImpl(
            filename="test.txt",
            content_type="text/plain",
            content=test_content
        )
        
        # Check properties
        self.assertEqual(attachment.filename, "test.txt")
        self.assertEqual(attachment.content_type, "text/plain")
        self.assertEqual(attachment.size, len(test_content))
        self.assertEqual(attachment.get_content(), test_content)
    
    def test_message_implementation(self):
        """Test the MessageImpl class."""
        # Create a test message
        message = MessageImpl(
            message_id="test123",
            from_="sender@example.com",
            to="recipient@example.com",
            subject="Test Subject",
            body="Test body content",
            cc="cc@example.com",
            bcc="bcc@example.com",
            date="Mon, 01 Apr 2025 12:00:00 +0000",
            is_read=False
        )
        
        # Check properties
        self.assertEqual(message.id, "test123")
        self.assertEqual(message.from_, "sender@example.com")
        self.assertEqual(message.to, "recipient@example.com")
        self.assertEqual(message.cc, "cc@example.com")
        self.assertEqual(message.bcc, "bcc@example.com")
        self.assertEqual(message.date, "Mon, 01 Apr 2025 12:00:00 +0000")
        self.assertEqual(message.subject, "Test Subject")
        self.assertEqual(message.body, "Test body content")
        self.assertEqual(message.is_read, False)
        self.assertEqual(len(message.attachments), 0)
        
        # Test mark_as_read and mark_as_unread
        message.mark_as_read()
        self.assertEqual(message.is_read, True)
        
        message.mark_as_unread()
        self.assertEqual(message.is_read, False)
        
        # Test message with attachments
        test_attachment = AttachmentImpl(
            filename="test.txt",
            content_type="text/plain",
            content=b"Test content"
        )
        
        message_with_attachment = MessageImpl(
            message_id="test456",
            from_="sender@example.com",
            to="recipient@example.com",
            subject="Test with Attachment",
            body="Message with attachment",
            attachments=[test_attachment]
        )
        
        self.assertEqual(len(message_with_attachment.attachments), 1)
        self.assertEqual(message_with_attachment.attachments[0].filename, "test.txt")
    
    def test_client_implementation(self):
        """Test the ClientImpl class."""
        # Check default folders
        folders = self.client.get_folders()
        self.assertIn("INBOX", folders)
        self.assertIn("Sent", folders)
        
        # Verify folder directories were created
        for folder in folders:
            folder_path = os.path.join(self.test_dir, folder)
            self.assertTrue(os.path.exists(folder_path))
        
        # Test adding a message
        message = MessageImpl(
            message_id="test123",
            from_="sender@example.com",
            to="recipient@example.com",
            subject="Test Subject",
            body="Test body content"
        )
        
        self.client.add_message(message, "INBOX")
        
# Verify message was added
        messages = list(self.client.get_messages(folder="INBOX"))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].subject, "Test Subject")
        
        # Check message was saved to disk
        message_path = os.path.join(self.test_dir, "INBOX", f"{message.id}.json")
        self.assertTrue(os.path.exists(message_path))
        
        # Test search functionality
        search_results = list(self.client.search_messages("Test", "INBOX"))
        self.assertEqual(len(search_results), 1)
        
        # Test with no matching messages
        search_results = list(self.client.search_messages("NotFound", "INBOX"))
        self.assertEqual(len(search_results), 0)
        
        # Test creating a new folder
        self.client.create_folder("TestFolder")
        folders = self.client.get_folders()
        self.assertIn("TestFolder", folders)
        
        # Test moving a message between folders
        self.client.move_message(message.id, "INBOX", "TestFolder")
        
        # Verify message was moved
        inbox_messages = list(self.client.get_messages(folder="INBOX"))
        self.assertEqual(len(inbox_messages), 0)
        
        test_folder_messages = list(self.client.get_messages(folder="TestFolder"))
        self.assertEqual(len(test_folder_messages), 1)
        
        # Test deleting a message
        self.client.delete_message(message.id, "TestFolder")
        test_folder_messages = list(self.client.get_messages(folder="TestFolder"))
        self.assertEqual(len(test_folder_messages), 0)
    
    def test_mock_fetcher(self):
        """Test the MockFetcher class."""
        from my_inbox_impl.mail_fetcher import MockFetcher
        
        # Create a mock fetcher
        fetcher = MockFetcher()
        fetcher.set_client(self.client)
        
        # Generate mock messages
        mock_messages = fetcher.fetch_messages(count=10)
        self.assertEqual(len(mock_messages), 10)
        
        # Verify messages were added to the client
        client_messages = list(self.client.get_messages(folder="INBOX"))
        self.assertEqual(len(client_messages), 10)
        
        # Test search with mock messages
        search_results = list(self.client.search_messages("Important", "INBOX"))
        self.assertGreaterEqual(len(search_results), 1)
        
        # Check that some messages have attachments
        messages_with_attachments = [m for m in client_messages if m.attachments]
        self.assertGreaterEqual(len(messages_with_attachments), 1)


if __name__ == '__main__':
    unittest.main()