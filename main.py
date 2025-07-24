h
from src.graph import build_graph
from src.state import AgentState
from langchain_core.messages import HumanMessage, AIMessage

if __name__ == "__main__":
    app = build_graph()
    
    # Example usage
    chat_history = []
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break

        inputs = {"input": user_input, "chat_history": chat_history}
        
        # Process the stream from the graph
        final_state = None
        for s in app.stream(inputs):
            # The stream outputs are dictionaries with agent names as keys
            # The value under the agent name is the state update from that agent
            # We are interested in the 'agent_response' for printing
            for key, value in s.items():
                if key != "__end__":
                    if "agent_response" in value:
                        print(f"\n{key}: {value['agent_response']}")
                    elif key == "router":
                        print(f"\nRouter chose: {value['next']}")
                else:
                    # Capture the final state after the graph completes a turn
                    final_state = value
        
        # Update chat_history from the final state of the graph
        if final_state and "chat_history" in final_state:
            chat_history = final_state["chat_history"] 