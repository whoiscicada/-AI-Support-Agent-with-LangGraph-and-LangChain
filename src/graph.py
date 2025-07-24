
from langgraph.graph import StateGraph, END
from .state import AgentState
from .agents import get_assistant_agent, get_billing_agent, get_tech_support_agent, get_faq_agent
from .router import route_query, router_node

def build_graph():
    workflow = StateGraph(AgentState)

    # Define the nodes
    workflow.add_node("assistant_agent", get_assistant_agent())
    workflow.add_node("billing_agent", get_billing_agent())
    workflow.add_node("tech_support_agent", get_tech_support_agent())
    workflow.add_node("faq_agent", get_faq_agent())
    workflow.add_node("router", router_node) # Use the new router_node

    # Set the entry point of the graph to the router
    workflow.set_entry_point("router")

    # Define edges - router will conditionally route
    # This function will determine the next node based on the state's "next" value
    def select_next_agent(state: dict):
        return state.get("next")

    workflow.add_conditional_edges(
        "router",
        select_next_agent, # Use the new function to select the next agent
        {
            "assistant_agent": "assistant_agent",
            "billing_agent": "billing_agent",
            "tech_support_agent": "tech_support_agent",
            "faq_agent": "faq_agent",
        },
    )

    # Each agent can transition back to the router for follow-up or END
    # We need to make sure the agents actually return a state update
    # For simplicity, we'll have them return to the router for now.
    workflow.add_edge("assistant_agent", END)
    workflow.add_edge("billing_agent", END) # Changed to END
    workflow.add_edge("tech_support_agent", END) # Changed to END
    workflow.add_edge("faq_agent", END) # Changed to END
    
    # Compile the graph
    app = workflow.compile()
    return app 