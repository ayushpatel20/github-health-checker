import re
from datetime import datetime

def parse_github_url(url: str):
    """
    Parses a GitHub URL and extracts the owner and repository name.
    
    Args:
        url (str): The GitHub repository URL.
        
    Returns:
        tuple: (owner, repo_name) or (None, None) if invalid.
    """
    # Quick and practical regex for most common GitHub URLs
    pattern = r"github\.com/([^/]+)/([^/]+?)(?:\.git|/)?$"
    match = re.search(pattern, url.strip())
    
    if match:
        return match.group(1), match.group(2)
    return None, None

def format_date(date_string: str) -> str:
    """
    Converts an ISO 8601 date string to a more readable format.
    
    Args:
        date_string (str): ISO formatted date string (e.g., "2023-10-25T14:30:00Z").
        
    Returns:
        str: Human-readable date string.
    """
    if not date_string:
        return "N/A"
        
    try:
        dt = datetime.strptime(date_string.replace('Z', '+0000'), "%Y-%m-%dT%H:%M:%S%z")
        return dt.strftime("%B %d, %Y")
    except ValueError:
        return date_string
