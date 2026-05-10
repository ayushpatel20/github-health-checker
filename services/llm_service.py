import os
# pyrefly: ignore [missing-import]
from openai import OpenAI
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY","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")

# Initialize the OpenAI client pointing to NVIDIA's API endpoint
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)

def generate_repository_summary_stream(repo_name: str, metrics: dict, health_data: dict):
    """
    Uses NVIDIA's LLM endpoint to generate a summary and recommendations for the repository, streaming the results.
    
    Args:
        repo_name (str): Name of the repository.
        metrics (dict): Various repository metrics.
        health_data (dict): Calculated health score and status.
        
    Yields:
        tuple: (chunk_type, text) where chunk_type is 'reasoning' or 'content'.
    """
    if not NVIDIA_API_KEY or NVIDIA_API_KEY == "your_nvidia_api_key_here":
        yield ("content", "⚠️ *NVIDIA API Key is missing. Please add it to your .env file to generate AI insights.*")
        return

    prompt = f"""
    You are an expert software engineering consultant. Please analyze the following GitHub repository and provide a brief summary, explain whether it is active, suggest improvements, and detect any potential risks.
    Keep the tone professional and helpful. Use Markdown formatting.
    
    Repository Name: {repo_name}
    
    Metrics:
    - Stars: {metrics.get('stars')}
    - Forks: {metrics.get('forks')}
    - Open Issues: {metrics.get('open_issues')}
    - Closed Issues: {metrics.get('closed_issues')}
    - Contributors: {metrics.get('contributors')}
    - Last Push: {metrics.get('last_push')}
    - Has README: {metrics.get('has_readme')}
    - License: {metrics.get('license')}
    
    Health Score: {health_data.get('score')}/100 ({health_data.get('status')})
    
    Please structure your response with the following headings:
    ### 📊 Repository Overview
    ### 🏃 Activity Status
    ### 💡 Suggestions for Improvement
    ### ⚠️ Potential Risks
    """

    try:
        completion = client.chat.completions.create(
            model="meta/llama-3.1-8b-instruct",
            messages=[
                {"role": "system", "content": "You are a concise expert software engineering consultant. Provide direct and professional insights. Avoid repeating yourself."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            top_p=0.9,
            max_tokens=1024,
            stream=True
        )
        
        for chunk in completion:
            if not chunk.choices:
                continue
                
            content = chunk.choices[0].delta.content
            if content is not None:
                yield ("content", content)
        
    except Exception as e:
        yield ("content", f"❌ Failed to generate AI summary: {str(e)}")
