# TAVILY_API_KEY="Your Tavily API Key"
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

search = TavilySearchResults()
python = PythonREPLTool()
```

Explanation:

* `TavilySearchResults()` provides web/factual search capability.
* `PythonREPLTool()` exposes a REPL that can run Python snippets returned by the LLM.
* Store sensitive keys like `TAVILY_API_KEY` as environment variables (e.g., using `os.getenv`).

Step 2 — Build the chat prompt template and assemble LLM + tools
Create a chat prompt template to structure system instructions, conversation history, and the human prompt. Then instantiate the LLM and list the tools the agent can call.

```python theme={null}
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Think step by step before responding."),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ]
)

llm = ChatOpenAI()
tools = [search, python]
```

Notes:

* The prompt keeps `chat_history` and `agent_scratchpad` placeholders so the agent can use prior messages and intermediate reasoning.
* Add or customize system instructions where appropriate for your use case (e.g., domain-specific constraints).

Step 3 — Create the agent, executor, and runnable with history
Wrap the agent in an executor and a runnable that preserves chat history across calls. The example below enables verbose output so you can inspect tool invocations.

```python theme={null}
message_history = ChatMessageHistory()

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent1 = RunnableWithMessageHistory(
    agent_executor,
    # A function that returns the message history object for a given session id.
    lambda session_id: message_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)
```

Behavior:

* `RunnableWithMessageHistory` maps a `session_id` to a `ChatMessageHistory` instance so multiple requests in the same session share context.
* `verbose=True` outputs the agent's intermediate steps (tool calls and tool outputs) which is useful for debugging.

Step 4 — Example: factual query (uses Tavily)
Invoke the agent with a simple factual question; the agent should use Tavily for the lookup.

```python theme={null}
response = agent1.invoke(
    {"input": "Which countries are hosting?"},
    config={"configurable": {"session_id": "session1"}}
)
print(response["output"])
```

Example output:

```plaintext theme={null}
The ICC Men's T20 World Cup 2024 will be co-hosted by the United States and the West Indies. The venues for the tournament in the USA are Dallas, Florida, and New York.
```

Step 5 — Example: multi-step query mixing search + Python REPL
Ask a question that requires both a factual lookup and exact computation. Example:

"Today's date is May 1st, 2024. How many days before the first match starts?"

Flow:

1. The agent may call Tavily to find the start date (e.g., June 1, 2024).
2. The agent then generates Python code to compute the date difference.
3. The Python REPL executes the code and returns the exact result.
4. The agent synthesizes a natural-language response that includes the computed value.

Invoke the agent:

```python theme={null}
response = agent1.invoke(
    {"input": "Today's date is May 1st, 2024. How many days before the first match starts?"},
    config={"configurable": {"session_id": "session1"}}
)
print(response["output"])
```

Example of the Python snippet the agent might generate and execute:

```python theme={null}
from datetime import datetime

start_date = datetime(2024, 6, 1)
today_date = datetime(2024, 5, 1)
days_until_start = (start_date - today_date).days
print(days_until_start)
```

Execution output:

```plaintext theme={null}
31
There are 31 days left before the first match of the ICC Men's T20 World Cup 2024 starts on June 1, 2024.
```

Because the agent used Python for the arithmetic, the numeric result is exact and reliable; the agent can then present that result in natural language.

<Callout icon="lightbulb">
  Using a Python REPL tool allows the agent to run exact computations (like date arithmetic, numeric calculations, or custom logic) instead of relying on the LLM to calculate, which improves accuracy.
</Callout>

<Callout icon="warning">
  Python REPL can execute arbitrary code. Only enable it in trusted environments and ensure you have safeguards for untrusted inputs.
</Callout>

Concise recap — final setup

```python theme={null}
# Imports (consolidated)
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_experimental.tools import PythonREPLTool

from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor

import os

# Initialize tools and prompt
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
search = TavilySearchResults()
python = PythonREPLTool()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Think step by step before responding."),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

llm = ChatOpenAI()
tools = [search, python]

# Build agent + executor + runnable with history
message_history = ChatMessageHistory()
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
agent1 = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: message_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)
```

Final notes and references

* Use environment variables for API keys and avoid committing secrets.
* Limit Python REPL exposure to trusted sessions, or implement sandboxing and input validation.
* For more on LangChain tool calling and agents, see the official docs:
  * [LangChain Agents Documentation](https://langchain.readthedocs.io/)
  * [LangChain Tooling and Tools](https://langchain.readthedocs.io/en/latest/modules/agents.html)
  * (If using Tavily, consult its API docs for authentication and usage.)

With this configuration the agent combines web/factual search (Tavily) and exact computation (Python REPL) to answer complex, multi-step questions reliably.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/530ad7de-8948-4806-8824-19eb10923d1d/lesson/36589ae2-a513-4802-a9c4-7890498a4018" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/langchain/module/530ad7de-8948-4806-8824-19eb10923d1d/lesson/81d50dee-7ffb-4092-95c2-3f8b8b07686b" />
</CardGroup>


# Building a Real time Flight Agent

Source: https://notes.kodekloud.com/docs/LangChain/Building-Agents/Building-a-Real-time-Flight-Agent/page

Guide to building a LangChain ReAct agent that fetches real time flight status via FlightAware AeroAPI and performs datetime calculations

In this lesson you'll build an agent that answers real-time flight queries by calling FlightAware's AeroAPI. The agent uses a custom LangChain tool `get_flight_status` to fetch flight status and the Python REPL tool for simple calculations (for example, adding hours to an arrival time to compute when to book a cab).

Prerequisites

* Sign up at FlightAware and create an AeroAPI key: [FlightAware AeroAPI](https://flightaware.com/commercial/aeroapi/).
* Set the `AEROAPI_KEY` environment variable before running the examples (see callout below).
* Basic familiarity with Python and LangChain (see references at the end).

<Frame>
  <img alt="The image shows the home page of FlightAware, a website for flight tracking and aviation data, featuring search options for flights and routes." />
</Frame>

FlightAware provides REST endpoints for flight schedules and real-time traffic that are ideal for building a status-checking tool.

<Frame>
  <img alt="The image shows a real-time worldwide flight traffic map from FlightAware, displaying numerous aircraft icons over a region. It also includes promotional text for a global flight tracking data feed." />
</Frame>

Once you create an API key, you can monitor usage and quotas from the AeroAPI dashboard.

<Frame>
  <img alt="The image shows a FlightAware AeroAPI usage dashboard, displaying a line graph of flight call API usage over time, with a summary of total calls and cost below." />
</Frame>

<Callout icon="lightbulb">
  Set your FlightAware API key in the environment before running the code. For example, on macOS/Linux:

  ```bash theme={null}
  export AEROAPI_KEY="your_api_key_here"
  ```
</Callout>

Overview of the solution

* Implement a `get_flight_status` LangChain tool that:
  * Calls the AeroAPI for flights on the current day.
  * Picks the best available timestamps using the priority estimated > actual > scheduled.
  * Converts UTC timestamps to the local timezone of origin/destination.
  * Returns a human-readable status string.
* Register the tool along with the Python REPL tool.
* Create a ReAct-style agent prompt so the agent plans (Thought), calls tools (Action), observes results, and provides a final answer.
* Use the Python REPL tool for follow-up computations (e.g., add hours to arrival time).

Tool implementation

* Save the following implementation as `flight_agent.py`. This function uses requests to call the AeroAPI, chooses the best time fields, converts times from UTC to local timezones via `pytz`, and returns a readable status string.

```python theme={null}
