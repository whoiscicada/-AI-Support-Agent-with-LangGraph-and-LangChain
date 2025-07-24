
from typing import List, Annotated, TypedDict
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    input: str
    chat_history: List[BaseMessage]
    agent_response: str | None # Add this line
    # Add other state variables as needed, e.g., for specific agent data 