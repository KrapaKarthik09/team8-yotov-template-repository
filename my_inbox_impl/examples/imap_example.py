#!/usr/bin/env python3
"""Example showing how to use the IMAP fetcher with Gmail."""

import os
import sys
import time
from pathlib import Path

# Add parent directory to sys.path if running as a script
if __name__ == "__main__":
    parent_dir = str(Path(__file__).resolve().parent.parent)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

from my_inbox_impl import get_client
from my_inbox_impl.mail_fetcher import IMAPFetcher


def main():
    """Main function to demonstrate Gmail IMAP functionality."""
    # Gmail IMAP settings
    imap_host = "imap.gmail.com"
    imap_port = 993  # SSL port for IMAP
    
    # Gmail credentials
    username = os.environ.get("GMAIL_ADDRESS") or "prathamsaraf007@gmail.com"
    password = os.environ.get("GMAIL_APP_PASSWORD") or "twcf dzwz aqot dfnr"
    
    print(f"Using Gmail account: {username}")
    
    # Create client
    client = get_client()
    
    # Print initial client folders
    print("\nLocal client folders:")
    for folder in client.get_folders():
        print(f"  - {folder}")
    
    try:
        # Create IMAP fetcher with debug mode enabled
        print(f"\nConnecting to Gmail IMAP server ({imap_host}:{imap_port})...")
        fetcher = IMAPFetcher(
            host=imap_host,
            port=imap_port,
            username=username,
            password=password
        )
        
        # Set client
        fetcher.set_client(client)
        
        # List available folders on the Gmail server
        print("\nFolders available on Gmail:")
        try:
            server_folders = fetcher.list_folders()
            if not server_folders:
                print("  No folders retrieved. This might be a connection issue.")
            else:
                for folder in server_folders:
                    print(f"  - {folder}")
        except Exception as e:
            print(f"  Error retrieving folders: {e}")
            # Default to standard INBOX
            server_folders = ["INBOX"]
        
        # Find a valid inbox folder
        target_folder = "INBOX"
        valid_inbox_names = ["INBOX", "[Gmail]/INBOX", "Inbox", "inbox"]
        
        for folder_name in valid_inbox_names:
            if folder_name in server_folders:
                target_folder = folder_name
                break
                
        print(f"\nUsing folder: {target_folder}")
        
        # Ask how many messages to fetch
        limit = int(input("Number of messages to fetch (default: 5): ") or "5")
        
        # Fetch messages
        print(f"\nFetching {limit} messages from {target_folder}...")
        try:
            start_time = time.time()
            fetched = fetcher.fetch_messages(folder=target_folder, limit=limit)
            end_time = time.time()
            
            print(f"Fetched {len(fetched)} messages in {end_time - start_time:.2f} seconds")
            
            # Give system time to process
            print("Processing messages...")
            time.sleep(1)
            
            # Display fetched messages
            print("\nFetched messages:")
            fetched_messages = list(client.get_messages(folder="INBOX", limit=limit))
            
            if not fetched_messages:
                print("  No messages were successfully retrieved.")
            else:
                for idx, message in enumerate(fetched_messages, 1):
                    print(f"{idx}. From: {message.from_}")
                    print(f"   Subject: {message.subject}")
                    print(f"   Date: {message.date}")
                    print("-" * 50)
                    
                # If we have messages, offer to view one
                if fetched_messages:
                    msg_idx = input("\nEnter message number to view details (or press Enter to skip): ")
                    if msg_idx and msg_idx.isdigit() and 1 <= int(msg_idx) <= len(fetched_messages):
                        msg = fetched_messages[int(msg_idx) - 1]
                        print("\n" + "=" * 60)
                        print(f"ID: {msg.id}")
                        print(f"From: {msg.from_}")
                        print(f"To: {msg.to}")
                        if msg.cc:
                            print(f"CC: {msg.cc}")
                        print(f"Date: {msg.date}")
                        print(f"Subject: {msg.subject}")
                        print("=" * 60)
                        print(f"\nBody preview (first 200 chars):")
                        print(f"{msg.body[:200]}...")
                        
                        if msg.attachments:
                            print("\nAttachments:")
                            for idx, attachment in enumerate(msg.attachments, 1):
                                print(f"  {idx}. {attachment.filename} ({attachment.content_type}, {attachment.size} bytes)")
                        
                        print("\n" + "=" * 60)
            
        except Exception as e:
            print(f"Error fetching messages: {e}")
            import traceback
            traceback.print_exc()
        
        # Close the connection
        print("\nClosing connection...")
        fetcher.close()
        print("Done!")
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()