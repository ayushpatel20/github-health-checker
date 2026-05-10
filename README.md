# 🏥 GitHub Repository Health Checker

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.2-FF4B4B)
![NVIDIA NIM](https://img.shields.io/badge/AI-NVIDIA_NIM-76B900)

A clean, modular Python web application built with Streamlit that analyzes any public GitHub repository to determine its health, activity, and maintenance quality. It uses the GitHub REST API for data gathering and NVIDIA's free LLM endpoint (Llama 3) to generate intelligent insights and recommendations.

## 🌐 Live Demo

https://github-health-checker-1.onrender.com/

## 📸 Screenshots

*(Screenshot goes here - place your image in the `assets/` folder and update this section)*

## 🎥 Demo Video

*(Demo video goes here - place your video in the `assets/` folder and update this section)*

---

## ✨ Features

- **GitHub API Integration**: Fetches real-time repository metrics including stars, forks, issues, PRs, and commit history.
- **Repository Health Score**: Calculates a custom 0-100 score based on recent activity, documentation, issue resolution rates, and community size.
- **AI-Powered Insights**: Integrates with NVIDIA's NIM API to generate natural language summaries, risk detection, and actionable suggestions.
- **Visual Analytics**: Interactive Plotly charts comparing open vs. closed issues and displaying key repository stats.
- **Clean UI**: Built with Streamlit, featuring loading indicators, metric cards, and a clean and responsive design.
- **Downloadable Reports**: Export your analysis as a Markdown report with one click.

## 📊 Health Metrics Used

The repository health score is calculated using:

- Recent commit activity
- Open vs closed issues
- Pull request activity
- Number of contributors
- Star and fork count
- Repository update frequency
- Documentation availability
- Release activity

Each metric contributes to an overall repository health score between 0–100.

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Frontend/Framework**: Streamlit
- **Data Visualization**: Plotly
- **APIs**: GitHub REST API v3, NVIDIA NIM (OpenAI compatible client)
- **Data Manipulation**: Pandas
- **Environment Management**: python-dotenv

---

## 🚀 Setup Instructions

Follow these steps to run the application locally.

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/github-health-checker.git
cd github-health-checker
```

### 2. Set up a virtual environment (Recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup

Copy the example environment file:
```bash
cp .env.example .env
```

Open the `.env` file and add your API keys:
- **GITHUB_TOKEN**: (Optional but highly recommended) Generate a Personal Access Token from GitHub settings to increase rate limits.
- **NVIDIA_API_KEY**: Get your free API key from [NVIDIA Build](https://build.nvidia.com/).

```ini
GITHUB_TOKEN=your_github_token_here
NVIDIA_API_KEY=your_nvidia_api_key_here
```

### 5. Run the Application
```bash
streamlit run app.py
```
The app will open automatically in your browser at `http://localhost:8501`.

---

## 📂 Project Structure

```
github-health-checker/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── .env.example            # Environment variables template
├── services/               # Core business logic
│   ├── github_service.py   # GitHub API interactions
│   ├── llm_service.py      # NVIDIA LLM integration
│   └── scoring_service.py  # Health score calculation
├── utils/                  # Helper functions and UI components
│   ├── helpers.py          # Data parsing and formatting
│   └── charts.py           # Plotly chart generation
└── assets/                 # Images and demo files (create if needed)
```

## 🔮 Future Improvements

- Add caching (e.g., `st.cache_data`) to prevent redundant API calls on refresh.
- Compare multiple repositories side-by-side.
- Analyze recent commit messages using NLP for sentiment/quality analysis.
- Add support for private repositories via OAuth login.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute.

## 📝 License

This project is open-source and available under the MIT License.
