from datetime import datetime, timezone

def calculate_health_score(repo_data: dict, additional_data: dict) -> dict:
    """
    Calculates a health score (0-100) based on repository metrics.
    
    Args:
        repo_data (dict): Core repository data from GitHub API.
        additional_data (dict): Extra data like PR counts, closed issues, etc.
        
    Returns:
        dict: A dictionary containing the score and a status string.
    """
    score = 0
    max_score = 100
    
    # 1. Recent Activity (30 points)
    # Check when it was last pushed
    pushed_at_str = repo_data.get('pushed_at')
    if pushed_at_str:
        pushed_at = datetime.strptime(pushed_at_str.replace('Z', '+0000'), "%Y-%m-%dT%H:%M:%S%z")
        now = datetime.now(timezone.utc)
        days_since_push = (now - pushed_at).days
        
        if days_since_push <= 30:
            score += 30
        elif days_since_push <= 90:
            score += 20
        elif days_since_push <= 180:
            score += 10
        elif days_since_push <= 365:
            score += 5
    
    # 2. Popularity & Engagement (20 points)
    stars = repo_data.get('stargazers_count', 0)
    forks = repo_data.get('forks_count', 0)
    if stars > 100 or forks > 20:
        score += 20
    elif stars > 10 or forks > 5:
        score += 10
    elif stars > 0:
        score += 5
        
    # 3. Documentation (20 points)
    if additional_data.get('has_readme', False):
        score += 10
        
    if repo_data.get('license'):
        score += 10
        
    # 4. Issue Management (15 points)
    open_issues = repo_data.get('open_issues_count', 0)
    closed_issues = additional_data.get('closed_issues', 0)
    total_issues = open_issues + closed_issues
    
    if total_issues > 0:
        # High closure rate is good
        closure_rate = closed_issues / total_issues
        if closure_rate >= 0.8:
            score += 15
        elif closure_rate >= 0.5:
            score += 10
        elif closure_rate >= 0.2:
            score += 5
    else:
        # No issues? Maybe it's a small or new project. Give partial points.
        score += 10
        
    # 5. Community (15 points)
    # Pull requests and contributors
    prs = additional_data.get('prs', {})
    total_prs = prs.get('open', 0) + prs.get('closed', 0)
    contributors = additional_data.get('contributors', 0)
    
    if total_prs > 5 or contributors > 2:
        score += 15
    elif total_prs > 0 or contributors > 1:
        score += 10
    else:
        score += 5
        
    # Determine Status
    if score >= 80:
        status = "Healthy"
    elif score >= 50:
        status = "Moderate"
    else:
        status = "Inactive / At Risk"
        
    return {
        "score": score,
        "status": status
    }
