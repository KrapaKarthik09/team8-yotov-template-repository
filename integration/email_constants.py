"""Constants for email processing module."""

# Regex patterns for email extraction
EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
URL_PATTERN = r'https?://[^\s]+'

# Common date patterns
DATE_PATTERNS = [
    # MM/DD/YYYY
    r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',
    # Month DD, YYYY
    r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b',
    # DD Month YYYY
    r'\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b',
    # YYYY-MM-DD
    r'\b\d{4}-\d{1,2}-\d{1,2}\b'
]

# Sentiment analysis word lists
POSITIVE_WORDS = [
    'thank', 'thanks', 'appreciate', 'good', 'great', 'excellent',
    'happy', 'pleased', 'congratulations', 'love', 'like', 'enjoy'
]

NEGATIVE_WORDS = [
    'issue', 'problem', 'complaint', 'error', 'fail', 'sorry',
    'broken', 'unhappy', 'disappointed', 'bad', 'terrible', 'hate'
]

# Action item indicators
ACTION_INDICATORS = [
    'please', 'kindly', 'could you', 'can you', 'would you',
    'need to', 'should', 'must', 'required', 'deadline',
    'by tomorrow', 'asap', 'as soon as possible', 'urgent',
    'action required', 'to-do', 'todo', 'action item'
]