# Country Q&A AI Agent

An AI agent built with LangGraph that answers questions about countries using the public REST Countries API.

## Architecture
The system follows a directed graph architecture using LangGraph:
1. **Extractor Node**: Analyzes the user's query to identify the target country and the specific data fields requested (intent).
2. **Fetcher Node**: A tool invocation step that queries the REST Countries API. It gracefully handles 404s and network errors.
3. **Synthesizer Node**: Combines the user query and the raw API data to generate a grounded, natural language response.

## Prerequisites
- Python 3.10+
- OpenAI API Key (or easily swappable to Anthropic/Google via LangChain)

## Setup
1. Clone the repository and navigate to the directory.
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy the `.env.example` to `.env` and add your LLM API key:
```bash
cp .env.example .env
```



## Usage

**Run the CLI:**

```bash
python cli.py
```

**Run the Web UI (Streamlit):**

```bash
streamlit run app.py
```