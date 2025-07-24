
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

def route_query(state: dict) -> str:
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
    
    query = state["input"].lower()
    
    if "billing" in query or "invoice" in query:
        return "billing_agent"
    elif "tech support" in query or "technical issue" in query:
        return "tech_support_agent"
    elif "faq" in query or "frequently asked questions" in query:
        return "faq_agent"
    else:
        return "assistant_agent"

def router_node(state: dict) -> dict:
    """This node determines the next agent based on the input.
    It returns a dictionary with the 'next' key indicating the chosen agent.
    """
    next_agent = route_query(state)
    return {"next": next_agent} 