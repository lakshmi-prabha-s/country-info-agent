from typing import TypedDict, Optional, List, Any
from pydantic import BaseModel, Field

# ---------------------------------------------------------
# State Definition for LangGraph
# ---------------------------------------------------------
class AgentState(TypedDict):
    query: str
    country: Optional[str]
    requested_fields: List[str]
    api_response: Optional[dict[str, Any]]
    final_answer: str
    error: Optional[str]

# ---------------------------------------------------------
# Structured Output Models for LLM Extraction
# ---------------------------------------------------------
class ExtractionResult(BaseModel):
    """Result of analyzing the user's country query."""
    country: Optional[str] = Field(
        description="The name of the country mentioned in the query. Null if no country is found."
    )
    requested_fields: List[str] = Field(
        description="The specific attributes requested (e.g., 'population', 'capital', 'currency')."
    )
    is_valid_query: bool = Field(
        description="True if the query is asking about country information, False otherwise."
    )