import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from tavily import TavilyClient

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_KEY = os.getenv("TAVILY_API_KEY")

tavily_client = TavilyClient(api_key=TAVILY_KEY)

@tool
def tavily_search(query: str) -> str:
    """Search the internet for real-time information."""
    
    print(f"Searching for: {query}")
    response = tavily_client.search(query=query, max_results=5)
    results = response.get("results", [])
    output = ""
    for item in results:
        output += f"Title: {item.get('title')}\nURL: {item.get('url')}\nContent: {item.get('content')}\n\n"
    return output

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    api_key=API_KEY
)

system_prompt = """You are an AI Research Assistant.
Always use the tavily_search tool to gather real-time data from the internet.

Structure your final response exactly with these headings:
# Research Title
## Introduction
## Key Findings
## Detailed Explanation
## Advantages and Disadvantages
## Real-World Applications
## Challenges and Limitations
## Conclusion
## References
"""

agent = create_agent(
    model=llm,
    tools=[tavily_search],
    system_prompt=system_prompt
)

user_topic = input("Enter research topic: ")

result = agent.invoke({
    "messages": [HumanMessage(content=f"Research this topic and provide a structured report: {user_topic}")]
})

report_content = result["messages"][-1].text
print(report_content)
