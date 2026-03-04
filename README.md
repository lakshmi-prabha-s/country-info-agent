# Country Q&A AI Agent

An AI agent built with LangGraph that answers questions about countries using the public REST Countries API.

## Architecture
The system follows a directed graph architecture using LangGraph:
1. **Extractor Node**: Analyzes the user's query to identify the target country and the specific data fields requested (intent).
2. **Fetcher Node**: A tool invocation step that queries the REST Countries API. It gracefully handles 404s and network errors.
3. **Synthesizer Node**: Combines the user query and the raw API data to generate a grounded, natural language response.

## Prerequisites
- Python 3.10+
- An API key for your chosen LLM provider: **OpenAI** or **Google Gemini**

## Setup

1. Clone the repository and navigate to the directory:

```bash
git clone https://github.com/lakshmi-prabha-s/country-info-agent.git
cd country-info-agent
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables:

Copy the `.env.example` to `.env` and fill in your API key:

```bash
cp .env.example .env
```

Edit `.env` to set your provider and key:

```text
# .env
LLM_PROVIDER=openai          # or: gemini
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_gemini_api_key_here
```

Only the key for your chosen `LLM_PROVIDER` is required.

---

## Usage

**Run the CLI:**

```bash
python cli.py
```

**Run the Web UI (Streamlit):**

```bash
streamlit run app.py
```
