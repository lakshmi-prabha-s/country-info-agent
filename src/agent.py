from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import ChatPromptTemplate
from src.models import AgentState, ExtractionResult
from src.tools import fetch_country_data
from src.config import Config

# ---------------------------------------------------------
# Dynamic LLM Initialization
# ---------------------------------------------------------
Config.validate()

if Config.LLM_PROVIDER == "gemini":
    from langchain_google_genai import ChatGoogleGenerativeAI
    model_name = Config.MODEL_NAME or "gemini-2.5-flash"
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0)
else:
    from langchain_openai import ChatOpenAI
    model_name = Config.MODEL_NAME or "gpt-4o-mini"
    llm = ChatOpenAI(model=model_name, temperature=0)

def extract_intent(state: AgentState) -> AgentState:
    """Node 1: Identify the country and requested fields using Structured Output."""
    query = state["query"]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an intent extractor. Analyze the user query. "
                   "Extract the country name and the specific data fields they are asking about (e.g., population, capital, languages). "
                   "If the query is not about a country, set is_valid_query to False."),
        ("user", "{query}")
    ])
    
    chain = prompt | llm.with_structured_output(ExtractionResult)
    result: ExtractionResult = chain.invoke({"query": query})
    
    if not result.is_valid_query or not result.country:
        return {
            "country": None,
            "requested_fields": [],
            "error": "I can only answer questions about specific countries. Please ask about a country's population, capital, currency, etc."
        }
        
    return {
        "country": result.country,
        "requested_fields": result.requested_fields,
        "error": None
    }

def fetch_data(state: AgentState) -> AgentState:
    """Node 2: Tool invocation step. Fetches data from REST API."""
    # Skip if there was an error in extraction
    if state.get("error"):
        return state
        
    country = state["country"]
    api_response = fetch_country_data(country)
    
    return {"api_response": api_response}

def synthesize_answer(state: AgentState) -> AgentState:
    """Node 3: Generate the final natural language answer."""
    query = state["query"]
    error = state.get("error")
    
    # Handle early errors (invalid queries)
    if error:
        return {"final_answer": error}
        
    api_response = state.get("api_response", {})
    
    # Handle API-level errors (e.g., 404s)
    if "error" in api_response:
        return {"final_answer": f"I couldn't fulfill your request: {api_response['error']}"}
        
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use the provided JSON data to answer the user's question accurately. "
                   "Keep your answer concise and direct. If the requested information is not present in the data, state that clearly. "
                   "Do not invent or hallucinate information outside of the provided context.\n\n"
                   "Context Data:\n{data}"),
        ("user", "{query}")
    ])
    
    chain = prompt | llm
    result = chain.invoke({
        "data": str(api_response), # Pass raw dictionary; LLM can parse JSON structure well
        "query": query
    })
    
    return {"final_answer": result.content}

# ---------------------------------------------------------
# Graph Construction
# ---------------------------------------------------------
def build_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("extract", extract_intent)
    workflow.add_node("fetch", fetch_data)
    workflow.add_node("synthesize", synthesize_answer)
    
    # Routing logic
    def route_after_extraction(state: AgentState):
        if state.get("error"):
            return "synthesize" # Skip fetch if invalid query
        return "fetch"
        
    workflow.add_edge(START, "extract")
    workflow.add_conditional_edges("extract", route_after_extraction)
    workflow.add_edge("fetch", "synthesize")
    workflow.add_edge("synthesize", END)
    
    return workflow.compile()

# Singleton instance
agent_app = build_graph()
