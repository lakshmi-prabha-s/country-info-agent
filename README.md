# Country Q&A AI Agent

An AI-powered agent built with [LangGraph](https://python.langchain.com/docs/langgraph) that answers factual questions about countries using real-time data from the public [REST Countries API](https://restcountries.com/).

This project is designed as a modular, production-grade service featuring strict typing, graceful error handling, and separation of concerns. It includes both a Command Line Interface (CLI) and a Web UI built with Streamlit.

---

## Architecture (LangGraph)

The agent operates on a directed state graph, processing user queries through three distinct nodes. This multi-step approach ensures accurate, grounded answers without relying on hallucination-prone zero-shot prompts.

1. **Intent / Field Identification (`extract_intent`)**
   * **Mechanism:** Uses LLM structured output (via Pydantic) to parse the user's natural language query.
   * **Output:** Extracts the target `country` name and the `requested_fields` (e.g., population, capital, currency). Validates if the query is actually about a country.
2. **Tool Invocation (`fetch_data`)**
   * **Mechanism:** A deterministic Python function that queries the `https://restcountries.com/v3.1/name/{country}` endpoint.
   * **Error Handling:** Gracefully catches network timeouts, 404s (country not found), and unexpected payloads without crashing the agent.
3. **Answer Synthesis (`synthesize_answer`)**
   * **Mechanism:** Passes the original query and the raw JSON API response back to the LLM.
   * **Grounding:** The LLM is strictly prompted to synthesize an answer *only* using the provided API context, ensuring 100% factual accuracy based on the data source.

---

## Production Design Decisions

* **No RAG / No Embeddings / No Database:** Per project constraints, all data is fetched live via REST API. The system relies on real-time tool calling rather than vector search.
* **LLM Agnostic:** Supports both **OpenAI** (default) and **Google Gemini** via LangChain's unified interface.
* **Separation of Concerns:** Core logic (nodes/edges), configuration, API tools, and Pydantic models are decoupled into separate modules within the `src/` directory.
* **Graceful Degradation:** If a user asks a non-country question (e.g., "What is the weather?"), the system catches this at the intent stage and bypasses the API call entirely, saving latency and compute.

---

## Getting Started

### Prerequisites
* Python 3.10+
* An API key for OpenAI (`OPENAI_API_KEY`) or Google Gemini (`GOOGLE_API_KEY`)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd country-agent
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup:**
Copy the example environment file and add your API keys.
   ```bash
   cp .env.example .env
   ```

*Edit `.env` to set your `LLM_PROVIDER` (`openai` or `gemini`) and corresponding API keys.*

---

## Usage

### Example Queries

* *"What is the population of Germany?"*
* *"What currency does Japan use?"*
* *"What is the capital and population of Brazil?"*
* *"Tell me about the languages spoken in Canada."*

### 1. Command Line Interface (CLI)

Run the interactive terminal agent:

```bash
python cli.py
```

### 2. Web UI (Streamlit)

Launch the graphical chat interface:

```bash
streamlit run app.py
```

---

## Project Structure

```text
country-info-agent/
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── cli.py                  # Command-line interface entry point
├── app.py                  # Streamlit web UI entry point
└── src/
    ├── __init__.py
    ├── config.py           # Environment and provider configuration
    ├── models.py           # Pydantic models and LangGraph state definitions
    ├── tools.py            # REST Countries API integration and error handling
    └── agent.py            # LangGraph nodes, edges, and compilation

```
