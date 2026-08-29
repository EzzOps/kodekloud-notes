# Inspect tool metadata provided by the decorator
print(GetFlightStatus.name)
print(GetFlightStatus.description)
print(GetFlightStatus.args)

# Build a prompt template that expects a context and a query
prompt = PromptTemplate.from_template(
    "Based on the context: {context},\nanswer the query: {query} about flight {flight} in one word."
)

# LLM and output parser
llm = OpenAI()
output_parser = StrOutputParser()

# Compose the chain: prompt -> llm -> output parser
chain = prompt | llm | output_parser

# Example flight and invoking the tool to fetch context
flight = "EK524"
context = GetFlightStatus.run(flight)

# Use the chain to answer specific queries based on the tool-provided context
status_answer = chain.invoke({"context": context, "query": "status", "flight": flight})
departure_answer = chain.invoke({"context": context, "query": "departure time", "flight": flight})
arrival_answer = chain.invoke({"context": context, "query": "arrival time", "flight": flight})
gate_answer = chain.invoke({"context": context, "query": "gate", "flight": flight})

print("Status:", status_answer)
print("Departure:", departure_answer)
print("Arrival:", arrival_answer)
print("Gate:", gate_answer)
```

Expected metadata printed when inspecting the tool:

```text theme={null}
GetFlightStatus
GetFlightStatus(flight_no: str) -> str - Gets flight status and schedule
{'flight_no': {'title': 'Flight No', 'type': 'string'}}
```

Example of the chain invocation outputs (based on the static tool response above):

```text theme={null}
Status: On-time
Departure: 5:20 PM
Arrival: Expected
Gate: B
```

Tool metadata reference

| Field       | Description                         | Example                                                                    |
| ----------- | ----------------------------------- | -------------------------------------------------------------------------- |
| Name        | Tool name exposed to LangChain      | `GetFlightStatus`                                                          |
| Description | Short summary of the tool's purpose | `GetFlightStatus(flight_no: str) -> str - Gets flight status and schedule` |
| Args        | Argument schema for the tool        | `{'flight_no': {'title': 'Flight No', 'type': 'string'}}`                  |

Notes on what's happening

* Decorating the function with `@tool` converts it into a StructuredTool-like object that LangChain can inspect and call. The decorator exposes metadata such as `name`, `description`, and `args` (the argument schema).
* `GetFlightStatus.run(flight)` executes the function and returns the static context string shown above. In production you would call a live flight-status API inside this function and return the real response.
* The `PromptTemplate` uses the tool output as `context`. The chain (`prompt | llm | output_parser`) takes the populated prompt, sends it to the LLM, and then parses the output into a simple string using `StrOutputParser`.
* This follows a retrieve-and-read pattern where the retrieval step is replaced by a tool call that supplies up-to-date context to the LLM.

> **lightbulb** This example uses a static response to keep the demonstration simple. For production, replace the static return with a real API call (include robust error handling, retries, and rate limiting). Also ensure the tool returns well-structured, documented data that your prompt and output parser expect.

Next steps

* Replace the static `GetFlightStatus` implementation with a real flight-status API to return live information.
* Build additional tools (e.g., airport info, weather) and explore creating an agent that selects between them to fulfill more complex user requests.
* Read more about LangChain tools and agents:
  * [LangChain Tools and Agents Guide](https://langchain.readthedocs.io/)
  * [OpenAI API Documentation](https://platform.openai.com/docs)

By following this pattern you can develop robust tool-backed chains that keep the LLM focused on reasoning while delegating data retrieval and structured logic to external functions.

- [Watch Video](https://learn.kodekloud.com/user/courses/langchain/module/06905b96-585d-4c9e-835a-d8fcaca76e2a/lesson/f564445e-f3df-4cae-9d49-986dc4a02a02)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/langchain/module/06905b96-585d-4c9e-835a-d8fcaca76e2a/lesson/a39008e8-97e9-4813-a404-3c1006e6e97c)


# Understanding and Using tools

Source: https://notes.kodekloud.com/docs/LangChain/Using-Tools/Understanding-and-Using-tools/page

Describes LangChain tools, their difference from RAG, and how to use external APIs and runtimes for live data, computation, and agent workflows.

Having implemented retrieval-augmented generation (RAG) and built chains for summarization and retrieval, it's time to focus on tools — what they are, why they matter, and how they differ from RAG.

[LangChain](https://python.langchain.com/en/latest/) provides a set of tools to integrate large language models (LLMs) with external systems. In production, LLMs rarely operate alone; they often need access to up-to-date information, computation, or services outside of pre-indexed content.

<Frame>
  <img alt="The image features an &#x22;Introduction&#x22; title, an icon of a toolbox with tools and a question mark, and three labeled elements: &#x22;LLM,&#x22; &#x22;Data Source,&#x22; and a question mark." />
</Frame>

We always need an LLM, and we frequently use a data source (for example, documents stored in a vector database). But many real-world tasks need integration points to external systems — tooling that either supplies live data or performs on-demand computation.

Example: an airline chatbot

* Customer asks, “What is the baggage policy?” — this typically triggers RAG: retrieve relevant policy text from an indexed document (vector DB), inject it into the prompt, and generate an answer.
* Customer asks, “When is my flight expected to arrive?” — that requires current status from a flight-tracking API; the answer depends on live data, not the stored PDF.

<Frame>
  <img alt="The image depicts an airline use case with a user asking, &#x22;What is the baggage policy?&#x22; accompanied by icons representing a vector database and a user." />
</Frame>

For live queries like the flight status, you must call an external API. This is the job of tools: they let your LangChain application interact with real-time services, streaming data sources, or specialized compute environments.

<Frame>
  <img alt="The image illustrates an airline use case involving a user asking about flight arrival using a flight tracking API, with a crossed-out PDF icon suggesting non-use of PDFs." />
</Frame>

What is a tool?

* In LangChain, a tool is a configurable module that exposes some external capability to your chain.
* Tools can fetch live data, call APIs, run custom logic, or execute code in a runtime (for example, Python).
* Agents — autonomous components that plan and pick actions — depend on tools to perform operations that the LLM cannot do by generation alone.

<Frame>
  <img alt="The image displays a simple illustration of a toolbox with tools inside, labeled &#x22;Tools&#x22; and &#x22;Configurable Module,&#x22; under the question &#x22;What is a Tool?&#x22;" />
</Frame>

Common tool examples

* Wikipedia — fetch and summarize articles ([Wikipedia](https://en.wikipedia.org/))
* Web search — perform live internet queries
* YouTube — retrieve transcripts or summarizations ([YouTube](https://www.youtube.com/))
* Python runtime — run code for numerical computation or data processing ([Python](https://www.python.org/))
* Custom tools — wrappers for internal APIs or business logic

<Frame>
  <img alt="The image shows icons representing &#x22;Wikipedia&#x22; and &#x22;Tools&#x22; under the heading &#x22;Tools – Examples.&#x22;" />
</Frame>

YouTube is a common case: fetch a transcript, summarize salient points, or answer questions about the video in real time.

<Frame>
  <img alt="The image shows the YouTube logo with a search bar beneath it. The words &#x22;Tools – Examples&#x22; are at the top left corner." />
</Frame>

A Python runtime as a tool is especially powerful:

* Run complex simulations, perform statistical analyses, or generate structured outputs.
* Return results to the LLM for further reasoning or response composition.
* Wrap domain-specific functions as callable tools to preserve business logic and ensure repeatability.

When to use RAG vs Tools

* RAG: augment prompts with context retrieved from preprocessed, indexed data (vector databases, document stores). Best for static or slowly changing content (policies, manuals, archived logs).
* Tools: interact with live systems or perform computation that must occur at query time (APIs, streaming data, heavy algorithms).

<Frame>
  <img alt="The image illustrates a comparison between RAG (Retrieval-Augmented Generation) and tools, showing interconnected external systems and applications. It includes icons representing tools and technology within a dotted framework." />
</Frame>

Key distinctions

* RAG is usually asynchronous and batch-driven: documents get vectorized over time, and retrieval happens during queries.
* Tools provide synchronous access to external capabilities and real-time data.
* For heavy computation or real-time decision-making, delegate to tools (e.g., a Python tool). For retrieving policy text or archived content, use RAG.

Example recap

* Baggage policy → RAG (static documentation)
* Flight tracking → Tool (flight-tracking API / real-time data)

<Frame>
  <img alt="The image illustrates use cases for an airlines chatbot, highlighting features like RAG, baggage policy, tools, and flight tracking." />
</Frame>

Quick reference: RAG vs Tools

|                           Capability | Best For                                      | Typical Example                                               |
| -----------------------------------: | --------------------------------------------- | ------------------------------------------------------------- |
| Retrieval-Augmented Generation (RAG) | Static or pre-indexed content                 | `Search a company's archived policy PDFs`                     |
|                                Tools | Real-time data, external APIs, or computation | `Call a flight-tracking API` or `Execute a Python simulation` |

> **lightbulb** RAG is ideal for retrieving pre-indexed, relatively static content. Use tools when you need real-time data, live API calls, or external computation.

Next steps

* We will demonstrate concrete tool implementations and how to wire them into LangChain chains.
* After the demos, we’ll dive into agents: how they plan, decide which tools to call, and orchestrate multi-step workflows.

Links and references

* [LangChain Documentation](https://python.langchain.com/en/latest/)
* [Wikipedia](https://en.wikipedia.org/)
* [YouTube](https://www.youtube.com/)
* [Python](https://www.python.org/)

- [Watch Video](https://learn.kodekloud.com/user/courses/langchain/module/06905b96-585d-4c9e-835a-d8fcaca76e2a/lesson/aa3a1783-f92e-417b-9352-d18c1784a501)
