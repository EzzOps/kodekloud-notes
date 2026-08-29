# flight_agent.py
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain.experimental.tools import PythonREPLTool

from datetime import datetime, timedelta
import requests
import pytz
import os

AEROAPI_BASE_URL = "https://aeroapi.flightaware.com/aeroapi"
AEROAPI_KEY = os.getenv("AEROAPI_KEY")

@tool
def get_flight_status(flight_id: str) -> str:
    """Returns Flight Information"""
    if not AEROAPI_KEY:
        return "Error: AEROAPI_KEY is not set in the environment."

    def get_api_session():
        session = requests.Session()
        session.headers.update({"x-apikey": AEROAPI_KEY})
        return session

    def fetch_flight_data(flight_id: str, session: requests.Session):
        # Accept inputs like "flight_id=EK226" or plain "EK226"
        if "flight_id=" in flight_id:
            flight_id = flight_id.split("flight_id=")[1]

        start_date = datetime.now().date().strftime("%Y-%m-%d")
        end_date = (datetime.now().date() + timedelta(days=1)).strftime("%Y-%m-%d")
        api_resource = f"/flights/{flight_id}?start={start_date}&end={end_date}"
        response = session.get(f"{AEROAPI_BASE_URL}{api_resource}")
        response.raise_for_status()
        data = response.json()
        # Expecting at least one flight in the result
        if "flights" not in data or not data["flights"]:
            raise ValueError(f"No flights found for {flight_id}")
        return data["flights"][0]

    def utc_to_local(utc_date_str: str, local_timezone_str: str) -> str:
        utc_datetime = datetime.strptime(utc_date_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc)
        local_timezone = pytz.timezone(local_timezone_str)
        local_datetime = utc_datetime.astimezone(local_timezone)
        return local_datetime.strftime("%Y-%m-%d %H:%M:%S")

    session = get_api_session()
    flight_data = fetch_flight_data(flight_id, session)

    # Choose best available time keys (priority: estimated > actual > scheduled)
    dep_key = (
        "estimated_out" if flight_data.get("estimated_out")
        else "actual_out" if flight_data.get("actual_out")
        else "scheduled_out"
    )
    arr_key = (
        "estimated_in" if flight_data.get("estimated_in")
        else "actual_in" if flight_data.get("actual_in")
        else "scheduled_in"
    )

    flight_details = {
        "source": flight_data["origin"].get("city", flight_data["origin"].get("code")),
        "destination": flight_data["destination"].get("city", flight_data["destination"].get("code")),
        "depart_time": utc_to_local(flight_data[dep_key], flight_data["origin"]["timezone"]) if flight_data.get(dep_key) else "N/A",
        "arrival_time": utc_to_local(flight_data[arr_key], flight_data["destination"]["timezone"]) if flight_data.get(arr_key) else "N/A",
        "status": flight_data.get("status", "Unknown")
    }

    return (
        f"The current status of flight {flight_id} from {flight_details['source']} to "
        f"{flight_details['destination']} is {flight_details['status']} with departure at "
        f"{flight_details['depart_time']} and arrival at {flight_details['arrival_time']}"
    )
```

Quick testing of the tool (direct calls)

* With `AEROAPI_KEY` set and network available, you can call the tool directly:

```python theme={null}
print(get_flight_status("EK226"))
# Example output:
print(get_flight_status("EK524"))
# Example output:
# 'The current status of flight EK524 from Dubai to Hyderabad is Scheduled with departure at 2024-04-30 22:00:00 and arrival at 2024-05-01 03:05:00'
```

Register tools and create the ReAct agent

* Register the two tools (custom flight tool + Python REPL) and construct a ReAct prompt that directs the agent to think, act, observe, and repeat until it produces the final answer.

```python theme={null}
from langchain.experimental.tools import PythonREPLTool
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent

tools = [get_flight_status, PythonREPLTool()]

template = """Answer the following questions as best you can.
You have access to the following tools:
{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
(this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!
Question: {input}
Thought:{agent_scratchpad}
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["agent_scratchpad", "input", "tool_names", "tools"],
)

llm = ChatOpenAI()
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
```

Invoke the agent

* Send a flight query to the agent executor. The ReAct loop will call `get_flight_status`, observe the API result, optionally perform follow-up calculations via the Python REPL, and then produce a final answer.

```python theme={null}
response = agent_executor.invoke({"input": "What is the status of EK524? Always include the source and destination."})
print(response["output"])
```

Typical verbose execution (illustrative)

* When `agent_executor` runs in verbose mode it logs the Thought/Action/Observation steps. Example:

```plaintext theme={null}
> Entering new AgentExecutor chain...
I should use the get_flight_status tool to retrieve the status of flight EK524 and its details.
Action: get_flight_status
Action Input: EK524
Observation: The current status of flight EK524 from Dubai to Hyderabad is Scheduled with the departure time as 2024-04-30 22:00:00 and arrival time as 2024-05-01 03:05:00
I now know the final answer

Final Answer: The status of flight EK524 from Dubai to Hyderabad is Scheduled with departure time at 2024-04-30 22:00:00 and arrival time at 2024-05-01 03:05:00.

> Finished chain.
```

Using the Python REPL tool for datetime math

* The Python REPL tool is useful for follow-up computations, such as determining the time to book a cab after arrival.

Example: add 3 hours to the arrival time:

```python theme={null}
from datetime import datetime, timedelta

arrival_time = datetime.strptime("2024-05-01 03:05:00", "%Y-%m-%d %H:%M:%S")
cab_time = arrival_time + timedelta(hours=3)
cab_time.strftime("%Y-%m-%d %H:%M:%S")
# -> '2024-05-01 06:05:00'
```

For 4.5 hours:

```python theme={null}
arrival_time = datetime.strptime("2024-05-01 03:05:00", "%Y-%m-%d %H:%M:%S")
cab_time = arrival_time + timedelta(hours=4.5)
cab_time.strftime("%Y-%m-%d %H:%M:%S")
# -> '2024-05-01 07:35:00'
```

Tool summary

| Tool                | Purpose                                                                                      | Example usage                  |
| ------------------- | -------------------------------------------------------------------------------------------- | ------------------------------ |
| `get_flight_status` | Fetches flight metadata & times from FlightAware AeroAPI and returns a human-readable status | `get_flight_status("EK524")`   |
| `PythonREPLTool`    | Performs local computations such as datetime arithmetic                                      | `arrival + timedelta(hours=3)` |

Best practices and production considerations

* Always set your `AEROAPI_KEY` environment variable before running the agent.
* The timestamp selection prioritizes `estimated` over `actual` over `scheduled`.
* Handle HTTP/network errors and JSON parsing gracefully in production (the example raises errors for clarity).
* Be mindful of API quotas and rate limits—use caching or debounce frequent queries when appropriate.
* Extend the agent with additional tools (weather, maps, booking APIs) to support richer interactions.

<Callout icon="warning">
  FlightAware's free tier may have limitations on calls and data. Monitor usage in the AeroAPI dashboard and upgrade if you need higher quotas or commercial support.
</Callout>

References and further reading

* [FlightAware AeroAPI](https://flightaware.com/commercial/aeroapi/)
* [LangChain documentation](https://learn.kodekloud.com/user/courses/langchain)
* [pytz timezone handling](https://pypi.org/project/pytz/)

This concludes the lesson on building a real-time flight agent using a custom LangChain tool and the Python REPL tool. Experiment by adding more tools to extend capabilities and support richer, multi-step queries.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-8948-4806-8824-19eb10923d1d/lesson/3835c8f5-0c1a-4581-8e62-8b1111b2b42c" />
</CardGroup>


# Building an Agent with Search Tool

Source: https://notes.kodekloud.com/docs/LangChain/Building-Agents/Building-an-Agent-with-Search-Tool/page

Guide to building a session-aware agent that combines a ChatOpenAI LLM with a Tavily search tool, using message history and an agent scratchpad for multi-step queries.

This lesson walks through a compact agent demo that connects a search tool (Tavily) with an LLM (ChatOpenAI). The goal is to demonstrate how message history, a prompt with an agent scratchpad, tools, and a runnable agent fit together to handle multi-step and context-aware queries. Some module names or imports may change over time—if you run into import errors, consult the latest LangChain Python SDK docs: [https://python.langchain.com/en/latest/](https://python.langchain.com/en/latest/).

## Overview

* Build a chat prompt that includes a system instruction, a conversation history placeholder, the user input placeholder, and an `agent_scratchpad` placeholder.
* Create an LLM (ChatOpenAI) and attach the Tavily search tool for web results.
* Wrap an `AgentExecutor` with `RunnableWithMessageHistory` so each session can preserve history and the agent scratchpad.
* Invoke the runnable agent with per-session IDs to support follow-up questions.

## Key components

| Component        |                                               Purpose | Example / Notes                               |
| ---------------- | ----------------------------------------------------: | --------------------------------------------- |
| Prompt Template  |  Structures the system, user, and scratchpad messages | `ChatPromptTemplate.from_messages(...)`       |
| Agent Scratchpad | Temporary workspace for chain-of-thought / tool calls | `MessagesPlaceholder("agent_scratchpad")`     |
| Search Tool      |      External retrieval (Tavily) to fetch web results | `TavilySearchResults(api_key=TAVILY_API_KEY)` |
| LLM              |                          Generates language responses | `ChatOpenAI()`                                |
| Message History  |                        Session-aware chat persistence | `ChatMessageHistory()`                        |
| Runnable Wrapper |      Adds session-aware history to the agent executor | `RunnableWithMessageHistory(...)`             |

## Imports and basic setup

We need imports for prompt templates, message history, runnables, the LLM, the Tavily search tool, and agent utilities. The `agent_scratchpad` placeholder is used as the agent's temporary workspace.

```python theme={null}
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_openai import ChatOpenAI

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_tool_calling_agent, tool
from langchain.agents import AgentExecutor, AgentType, initialize_agent, load_tools

import os
