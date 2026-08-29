# Agents

Source: https://notes.kodekloud.com/docs/LangChain/Key-Components-of-LangChain/Agents/page

Explains LangChain agents that combine LLM reasoning with external tools and data to perform multi-step, context-rich tasks, including workflows, examples, and best practices.

Agents are the most advanced components in LangChain. They combine the reasoning and planning capabilities of large language models (LLMs) with external tools and data sources to solve multi-step, context-rich tasks. Unlike a fixed program, an agent orchestrates interactions between an LLM and tools (APIs, functions, databases, calendars, etc.), dynamically deciding what information to request, which tools to call, and how to execute plans.

## How agents work — a concise workflow

1. The user issues a request that may require additional context or actions.
2. The agent asks the LLM what clarifying details or steps are needed.
3. The agent uses tools (e.g., calendar lookup, flight API, user profile lookup) to gather that information.
4. The agent returns the collected data to the LLM.
5. The LLM formulates a plan and specifies which tool calls or actions are required.
6. The agent executes those actions by invoking tools, then reports results back to the user.

Example travel scenario

* User: "Book me a cab for my return flight."
* LLM: Identifies missing details (return date/time, flight number, arrival city).
* Agent: Checks available tools (calendar, flight API, user profile) to fetch those details.
* Agent: Provides the gathered answers to the LLM.
* LLM: Produces a booking plan (which service to call, pickup time relative to arrival, confirmation).
* Agent: Executes the plan by calling the cab-booking API and reports back.

> **lightbulb** Agents enable iterative reasoning: the LLM asks follow-ups, the agent gathers facts via tools, the LLM plans, and the agent executes. This loop allows complex workflows that go beyond single-prompt answers.

## When to use agents

Agents are a good fit when your task requires:

* Multiple coordinated API calls or transactions.
* Clarifying questions to complete a request.
* Retrieval from external knowledge stores (documents, vector DBs).
* Combining short-term and long-term memory with live data.
* Multi-step automations where the steps depend on intermediate results.

Use simpler chains or direct model calls when the task is single-step, deterministic, or does not require external tool access.

## LangChain building blocks and where agents fit

Below is a high-level wrap-up of the LangChain building blocks and how agents integrate them:

<Frame>
  <img alt="The image illustrates the building blocks of LangChain, featuring components such as Model I/O, Memory, Retrieval, and others, with connections to Language Models, Vector Databases, and External Data." />
</Frame>

Building blocks recap

* Model I/O: The prompt and the model response. This is the core interaction with the LLM.
* Memory: Short-term and long-term memory that preserves conversational or contextual state.
* Retrieval: Pulling relevant content from external sources (documents, vector DBs) to augment prompts.
* Chains: Sequences/compositions of steps (prompts, transformations, calls) that perform multi-step processes.
* Tools: External functions or services the agent can call (APIs, databases, system utilities).
* Agents: Orchestrators that combine LLM reasoning with tools and memory to perform sophisticated tasks.

Table: Building blocks and example usage

| Building Block | Purpose                        | Example                                                  |
| -------------: | ------------------------------ | -------------------------------------------------------- |
|      Model I/O | Interact with the LLM          | `ChatOpenAI` for responses                               |
|         Memory | Maintain context across turns  | `ConversationBufferMemory` to store chat history         |
|      Retrieval | Augment prompts with documents | Use a vector store (e.g., FAISS) to fetch related docs   |
|         Chains | Compose multiple steps         | A chain that validates input, queries DB, formats output |
|          Tools | External capabilities          | Payment API, calendar lookup, web search                 |
|         Agents | Combine reasoning + tools      | `initialize_agent` with tools and LLM for orchestration  |

## Example: Simple Python agent (conceptual)

The following example demonstrates the typical structure: define tools, create an LLM, and initialize an agent to coordinate tools and model reasoning.

```python theme={null}
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
