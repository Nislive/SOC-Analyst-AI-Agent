from langchain.tools import tool
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain.messages import SystemMessage
import requests
from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator
from langchain.messages import SystemMessage
from langchain.messages import ToolMessage
from typing import Literal
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
from langchain.messages import HumanMessage
import time

load_dotenv()

model = init_chat_model(
    "llama-3.3-70b-versatile", 
    model_provider="groq",
    temperature=0)


@tool
def tavily_search_tool(query:str):
    """Searches for threat intelligence, IP reputation, or cybersecurity payloads."""

    search = TavilySearch(
        max_results=5
    )

    enriched_query = f"cybersecurity threat intelligence report: {query}"
    return search.invoke(enriched_query)


@tool
def send_security_alert(analysis_report:str):
    """Sends the final analysis report to the admin via Telegram."""
    token=os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id=os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        return "Error: Telegram credentials not found in environment."
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": f"🚨 *SOC ANALYST ALERT* 🚨\n\n{analysis_report}",
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return "Alert successfully sent to the administrator via Telegram."
        else:
            return f"Failed to send alert. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred while sending Telegram message: {str(e)}"

    

tools = [tavily_search_tool, send_security_alert]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)



class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int


def llm_call(state: dict):
    """The Core Decision-Making Hub for the SOC Analyst"""
    sys_msg = SystemMessage(content="""You are a Senior SOC Analyst. 
    1. Analyze logs for SQLi, XSS, Brute Force, or Directory Traversal.
    2. Use 'tavily_search_tool' to investigate suspicious IPs or payloads.
    3. Once the analysis is complete and a threat is confirmed, use 'send_security_alert' to notify the admin.
    4. If it's a false alarm, explain why and stop.""")
    response = model_with_tools.invoke([sys_msg] + state["messages"])
    return {"messages": [response]}



def tool_node(state: dict):
    """Performs the tool call"""

    result = []
    last_msg = state["messages"][-1]
    for tool_call in last_msg.tool_calls:

        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=str(observation), tool_call_id=tool_call["id"]))
    return {"messages": result}





def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tool_node"
    return END


agent_builder = StateGraph(MessagesState)


agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)


agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    ["tool_node", END]
)
agent_builder.add_edge("tool_node", "llm_call")


agent = agent_builder.compile()



def start_soc_monitoring(log_file_path):
    print(f"SOC Agent is active and monitoring: {log_file_path}")

    if not os.path.exists(log_file_path):
        open(log_file_path, 'w').close()

    with open(log_file_path, "r") as f:
        f.seek(0, 2)
        
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            
            log_entry = line.strip()
            if log_entry:
                for chunk in agent.stream({"messages": [HumanMessage(content=log_entry)]}, config={"recursion_limit": 15}):
                    for node, output in chunk.items():
                        print(f"--- Node: {node} ---")
                

if __name__ == "__main__":
    LOG_FILE = "server_logs.txt"
    start_soc_monitoring(LOG_FILE)