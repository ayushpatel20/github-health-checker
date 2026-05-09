import streamlit as st
import pandas as pd
from utils.helpers import parse_github_url, format_date
from utils.charts import create_issue_ratio_chart, create_metric_bar_chart
from services.github_service import (
    fetch_repository_data,
    fetch_closed_issues_count,
    fetch_pull_requests_count,
    fetch_contributors_count,
    check_readme_exists
)
from services.scoring_service import calculate_health_score
from services.llm_service import generate_repository_summary_stream

# Set page configuration
st.set_page_config(
    page_title="GitHub Repo Health Checker",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a cleaner look
st.markdown("""
    <style>
    .main { padding: 2rem; }
    .stProgress .st-bo { background-color: #4CAF50; }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .status-badge {
        display: inline-block;
        padding: 0.25em 0.6em;
        font-size: 75%;
        font-weight: 700;
        line-height: 1;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 0.25rem;
    }
    .status-Healthy { background-color: #d4edda; color: #155724; }
    .status-Moderate { background-color: #fff3cd; color: #856404; }
    .status-Inactive { background-color: #f8d7da; color: #721c24; }
    </style>
""", unsafe_allow_html=True)

st.title("🏥 GitHub Repository Health Checker")
st.markdown("Analyze any public GitHub repository to determine its health, activity level, and get AI-powered recommendations.")

# Sidebar for input
with st.sidebar:
    st.header("Configuration")
    repo_url = st.text_input("GitHub Repository URL", placeholder="https://github.com/octocat/Hello-World")
    analyze_button = st.button("Analyze Repository", type="primary")
    
    st.markdown("---")
    st.markdown("### How it works")
    st.markdown("""
    1. Fetches data using **GitHub REST API**.
    2. Calculates a **Health Score** based on activity.
    3. Generates insights using **NVIDIA's LLM**.
    """)

if analyze_button and repo_url:
    owner, repo = parse_github_url(repo_url)
    
    if not owner or not repo:
        st.error("Invalid GitHub URL. Please enter a valid URL like: https://github.com/owner/repo")
    else:
        with st.spinner("Fetching repository data from GitHub..."):
            try:
                # Fetching data using our modular services
                repo_data = fetch_repository_data(owner, repo)
                closed_issues = fetch_closed_issues_count(owner, repo)
                prs = fetch_pull_requests_count(owner, repo)
                contributors = fetch_contributors_count(owner, repo)
                has_readme = check_readme_exists(owner, repo)
                
                additional_data = {
                    "closed_issues": closed_issues,
                    "prs": prs,
                    "contributors": contributors,
                    "has_readme": has_readme
                }
                
                # Calculate Health Score
                health_data = calculate_health_score(repo_data, additional_data)
                
                # Collect metrics for display and LLM
                metrics = {
                    "stars": repo_data.get('stargazers_count', 0),
                    "forks": repo_data.get('forks_count', 0),
                    "open_issues": repo_data.get('open_issues_count', 0),
                    "closed_issues": closed_issues,
                    "contributors": contributors,
                    "last_push": format_date(repo_data.get('pushed_at')),
                    "has_readme": "Yes" if has_readme else "No",
                    "license": repo_data.get('license', {}).get('name', 'None') if repo_data.get('license') else 'None',
                    "language": repo_data.get('language', 'N/A')
                }
                
                st.success("Analysis complete!")
                
                # Display Results
                st.header(f"Repository: {owner}/{repo}")
                
                # Top Level Metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    status_class = f"status-{health_data['status'].split(' ')[0]}"
                    st.markdown(f"### Health Score")
                    st.progress(health_data['score'] / 100)
                    st.markdown(f"<h2>{health_data['score']}/100 <span class='status-badge {status_class}'>{health_data['status']}</span></h2>", unsafe_allow_html=True)
                    
                with col2:
                    st.markdown("### Core Info")
                    st.write(f"**Primary Language:** {metrics['language']}")
                    st.write(f"**License:** {metrics['license']}")
                    st.write(f"**Has README:** {metrics['has_readme']}")
                    st.write(f"**Last Push:** {metrics['last_push']}")
                    
                with col3:
                    st.markdown("### Community")
                    st.write(f"**⭐ Stars:** {metrics['stars']:,}")
                    st.write(f"**🍴 Forks:** {metrics['forks']:,}")
                    st.write(f"**👥 Contributors:** {metrics['contributors']}")
                
                st.markdown("---")
                

                
                # AI Summary Section
                st.subheader("🤖 AI-Powered Insights")
                
                reasoning_expander = st.expander("Thinking Process...", expanded=False)
                reasoning_container = reasoning_expander.empty()
                content_container = st.empty()
                
                reasoning_text = ""
                content_text = ""
                
                for chunk_type, text in generate_repository_summary_stream(f"{owner}/{repo}", metrics, health_data):
                    if chunk_type == "reasoning":
                        reasoning_text += text
                        reasoning_container.markdown(reasoning_text)
                    elif chunk_type == "content":
                        content_text += text
                        content_container.markdown(content_text)
                        
                llm_summary = content_text
                    
                # Downloadable Report
                st.markdown("---")
                report_content = f"""# Repository Health Report: {owner}/{repo}
                
## Score: {health_data['score']}/100 ({health_data['status']})

## Metrics
- Stars: {metrics['stars']}
- Forks: {metrics['forks']}
- Open Issues: {metrics['open_issues']}
- Closed Issues: {metrics['closed_issues']}
- Contributors: {metrics['contributors']}
- Language: {metrics['language']}

## AI Insights
{llm_summary}
"""
                st.download_button(
                    label="📥 Download Full Report (Markdown)",
                    data=report_content,
                    file_name=f"{owner}_{repo}_health_report.md",
                    mime="text/markdown"
                )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

elif not repo_url and analyze_button:
    st.warning("Please enter a repository URL.")
else:
    # Initial state screen
    st.info("👈 Enter a GitHub repository URL in the sidebar and click 'Analyze Repository' to get started.")
