# Implementation file with proper docstrings

import my_inbox_api
from typing import Iterator, List, Optional

class Attachment(my_inbox_api.Attachment):
    """Implementation of the Attachment protocol.

    This class handles email attachments including their metadata and content.
    """

    pass

class Message(my_inbox_api.Message):
    """Implementation of the Message protocol.

    This class represents an email message with its headers, body, and attachments.
    """

    pass

class Client(my_inbox_api.Client):
    """Implementation of the Client protocol.

    This class provides methods for interacting with an email inbox,
    including retrieving messages and managing folders.
    """

    pass
