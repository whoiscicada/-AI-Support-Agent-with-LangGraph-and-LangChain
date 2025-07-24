
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from .tools import knowledge_base_lookup # Import your tools here
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

def create_agent(llm, tools, system_prompt: str):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])
    # Use create_tool_calling_agent for Gemini
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # Define a new runnable that updates the state with the agent's response
    def run_agent(state: dict):
        result = agent_executor.invoke({"input": state["input"], "chat_history": state["chat_history"]})
        return {"agent_response": result["output"], "chat_history": state["chat_history"] + [HumanMessage(content=state["input"]), AIMessage(content=result["output"])]}

    return run_agent # Return the new runnable

def get_assistant_agent():
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, google_api_key=os.getenv("GOOGLE_API_KEY"))
    tools = [knowledge_base_lookup]
    system_prompt = (
        "You are a helpful assistant. Use the provided tools to answer questions."
        "If you cannot answer with the tools, say so."
    )
    return create_agent(llm, tools, system_prompt)

def get_billing_agent():
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, google_api_key=os.getenv("GOOGLE_API_KEY"))
    # In a real scenario, you'd have billing-specific tools here
    tools = [] 
    system_prompt = (
        "You are a billing support agent. Answer questions related to billing, invoices, and payments."
        "If you cannot answer, direct the user to the general assistant."
    )
    return create_agent(llm, tools, system_prompt)

def get_tech_support_agent():
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, google_api_key=os.getenv("GOOGLE_API_KEY"))
    # In a real scenario, you'd have tech support-specific tools here
    tools = []
    system_prompt = (
        "You are a technical support agent. Help users with technical issues and troubleshooting."
        "If you cannot resolve the issue, direct the user to the general assistant."
    )
    return create_agent(llm, tools, system_prompt)

def get_faq_agent():
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, google_api_key=os.getenv("GOOGLE_API_KEY"))
    # You might use the knowledge_base_lookup tool here, or a specialized FAQ tool
    tools = [knowledge_base_lookup]
    system_prompt = (
        "You are an FAQ agent. Provide answers to frequently asked questions based on the knowledge base."
        "If the question is not in the FAQ, direct the user to the general assistant."
    )
    return create_agent(llm, tools, system_prompt) 