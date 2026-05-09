import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
BASE_URL = "https://api.github.com"

def get_headers():
    """Returns headers required for GitHub API authentication."""
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    return headers

def fetch_repository_data(owner: str, repo: str) -> dict:
    """
    Fetches core repository details from GitHub API.
    """
    url = f"{BASE_URL}/repos/{owner}/{repo}"
    response = requests.get(url, headers=get_headers())
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        raise ValueError("Repository not found. Please check the URL.")
    else:
        raise Exception(f"GitHub API Error: {response.status_code} - {response.text}")

def fetch_closed_issues_count(owner: str, repo: str) -> int:
    """
    Fetches the total number of closed issues using the Search API.
    Note: We separate issues from PRs by specifying 'is:issue'.
    """
    url = f"{BASE_URL}/search/issues?q=repo:{owner}/{repo}+is:issue+is:closed"
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        return response.json().get('total_count', 0)
    return 0

def fetch_pull_requests_count(owner: str, repo: str) -> dict:
    """
    Fetches total PR counts (open and closed).
    """
    open_url = f"{BASE_URL}/search/issues?q=repo:{owner}/{repo}+is:pr+is:open"
    closed_url = f"{BASE_URL}/search/issues?q=repo:{owner}/{repo}+is:pr+is:closed"
    
    open_count = 0
    closed_count = 0
    
    res_open = requests.get(open_url, headers=get_headers())
    if res_open.status_code == 200:
        open_count = res_open.json().get('total_count', 0)
        
    res_closed = requests.get(closed_url, headers=get_headers())
    if res_closed.status_code == 200:
        closed_count = res_closed.json().get('total_count', 0)
        
    return {"open": open_count, "closed": closed_count}

def fetch_contributors_count(owner: str, repo: str) -> int:
    """
    Fetches the number of contributors.
    GitHub paginates this, but we can often just look at the Link header 
    of the first request per page=1&per_page=1 to get the total.
    For simplicity in this beginner project, we'll fetch one page of max 100.
    """
    url = f"{BASE_URL}/repos/{owner}/{repo}/contributors?per_page=1&anon=1"
    response = requests.get(url, headers=get_headers())
    
    if response.status_code == 200:
        # Check 'Link' header for pagination to find the last page
        if 'Link' in response.headers:
            # Example: <...page=34>; rel="last"
            links = response.headers['Link']
            import re
            match = re.search(r'page=(\d+)>; rel="last"', links)
            if match:
                return int(match.group(1))
        # If no link header, the list might be empty or length 1
        return len(response.json())
    return 0

def check_readme_exists(owner: str, repo: str) -> bool:
    """
    Checks if a README file exists in the repository.
    """
    url = f"{BASE_URL}/repos/{owner}/{repo}/readme"
    response = requests.get(url, headers=get_headers())
    return response.status_code == 200
