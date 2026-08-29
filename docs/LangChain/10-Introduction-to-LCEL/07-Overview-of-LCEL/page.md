# Run the chain
length = chain.invoke({"topic": "AI"})
print(length)
```

Example console output (both printed text and returned length):

```plaintext theme={null}
Ai Is The Simulation Of Human Intelligence Processes By Machines, Especially Computer Systems.
94
```

## Putting it all together (concise example)

```python theme={null}
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

def to_titlecase(text: str) -> str:
    return text.title()

def get_len(text: str) -> int:
    print(text)
    return len(text)

prompt = ChatPromptTemplate.from_template("Give me a one-line description of {topic}")
model = ChatOpenAI()
output_parser = StrOutputParser()

chain = prompt | model | output_parser | RunnableLambda(to_titlecase) | RunnableLambda(get_len)

# Invoke and observe both the transformed text (printed) and the returned length
length = chain.invoke({"topic": "AI"})
print("Length returned by pipeline:", length)
```

## Use cases and rationale

Runnable lambdas let you inject arbitrary Python logic into LCEL pipelines to enrich, transform, validate, persist, or debug model outputs. Common use cases include:

| Use Case                         | Why                                                               | Example                                                              |
| -------------------------------- | ----------------------------------------------------------------- | -------------------------------------------------------------------- |
| Transform text                   | Normalize formatting or map outputs into a desired representation | Convert model text to title case with `RunnableLambda(to_titlecase)` |
| Validate or enforce schema       | Ensure model outputs conform to expected formats                  | Parse and validate JSON or enforce allowed tokens                    |
| Enrich context with runtime data | Add live data to prompts or model inputs                          | Call an API for flight status before invoking the model              |
| Persist outputs                  | Save results for auditing or downstream processing                | Write model outputs to a database or file                            |
| Debugging and inspection         | Print or log intermediate values for diagnosis                    | Use a runnable that prints intermediate text and returns its length  |

## Inspecting the LCEL graph

For complex pipelines, visualizing the internal graph is helpful. Install a graph utility (e.g., `grandalf`) to extract and visualize the chain graph.

```python theme={null}
# pip install grandalf
graph = chain.get_graph()
print(graph)              # textual representation
graph.print_ascii()       # ASCII visualization of the pipeline
```

Sample outputs (truncated / representative):

```plaintext theme={null}
Graph(nodes={ ... }, edges=[ ... ])
```

ASCII example (what `print_ascii()` might show):

```plaintext theme={null}
PromptInput -> ChatPromptTemplate -> ChatOpenAI -> StrOutputParser -> RunnableLambda(to_titlecase) -> RunnableLambda(get_len)
```

## Notes about runtime representations

* LCEL may convert some components (including wrapped functions) into internal Pydantic models or other runtime representations to enable type checking, validation, and serialization.
* These runtime conversions are primarily for inspection and validation; they don't change how you write Python functions for `RunnableLambda`.
* Use the graph and runtime representations to debug inputs/outputs and to validate that components are wired as expected.

## Quick reference

| Step | Action                                                              |    |
| ---- | ------------------------------------------------------------------- | -- |
| 1    | Create a prompt using `ChatPromptTemplate.from_template(...)`       |    |
| 2    | Attach a model such as `ChatOpenAI()`                               |    |
| 3    | Add an output parser like `StrOutputParser()`                       |    |
| 4    | Wrap Python functions with `RunnableLambda` and append them with \` | \` |
| 5    | Invoke the pipeline with `chain.invoke({"topic": "..."})`           |    |

## Summary

* LCEL pipelines are highly composable: prompts, models, parsers, and Python runnables can be combined using the pipe (`|`) operator.
* `RunnableLambda` wraps Python functions so they can participate in LCEL chains.
* Chain multiple runnables to transform, inspect, and persist outputs (e.g., title-casing, measuring length, calling external APIs).
* Use graph visualization (via `get_graph()` and `print_ascii()`) for debugging and understanding complex pipelines.

## Links and References

* [LangChain Documentation](https://langchain.readthedocs.io/)
* [ChatOpenAI integration (example)](https://github.com/langchain-ai/langchain)
* [grandalf (graph visualization)](https://pypi.org/project/grandalf/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-1386-422b-98ad-3342dfc6aab3/lesson/bd770c51-e411-479e-89f1-5c6fd2762abd" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.[SECRET_REDACTED]-1386-422b-98ad-3342dfc6aab3/lesson/d51c42c5-aefd-4edd-a892-ad0294da5d82" />
</CardGroup>


# Overview of LCEL

Source: https://notes.kodekloud.com/docs/LangChain/Introduction-to-LCEL/Overview-of-LCEL/page

Introduction to LangChain Expression Language, a concise declarative DSL using pipe-style chains to compose reusable LLM pipelines, Runnables, retrievers, transformers, and parsers.

Welcome back. This lesson introduces the LangChain Expression Language (LCEL) — a concise, declarative way to compose LangChain pipelines. LCEL makes it easy to build modular, production-ready applications by expressing chains with a familiar pipe-style syntax rather than constructing them imperatively.

What is LCEL?

* LCEL is a domain-specific language (DSL) designed for composing LLM-centric pipelines declaratively.
* It models LangChain components (prompts, LLMs, retrievers, output parsers, custom functions, etc.) as composable Runnables with well-defined inputs and outputs.
* Using a pipe operator, LCEL chains components so the output of one step becomes the input to the next, enabling readable, maintainable, and testable workflows.

<Frame>
  <img alt="The image illustrates the concept of &#x22;LangChain Expression Language,&#x22; showing a flow from &#x22;User&#x22; to &#x22;Language Model&#x22; through a &#x22;Chain&#x22; process." />
</Frame>

LCEL draws a clear analogy to Unix pipelines: if you’re used to chaining shell commands with `|`, LCEL uses the same mental model to connect LangChain components.

<Frame>
  <img alt="The image shows two terminal windows labeled &#x22;Terminal&#x22; with &#x22;Command&#x22; and &#x22;Output&#x22; text, and an arrow connecting them under the title &#x22;What is LangChain Expression Language?&#x22;." />
</Frame>

Example shell pipeline:

```bash theme={null}
cat file.txt | grep "error" | wc -l
```

This command finds lines containing "error" in `file.txt` and counts them. The pipe operator makes the composition concise and expressive.

LCEL applies the same pattern to LLM workflows: connect prompts, transformations, retrievers, LLMs, and parsers into a single pipeline that flows from input to final output.

<Frame>
  <img alt="The image is a diagram explaining the LangChain Expression Language, showing its components like prompts and output parsers in the context of a large language model (LLM) workflow." />
</Frame>

Core concept: Runnable

* The Runnable interface is the common abstraction that enables composability. Any component that implements Runnable can be piped into LCEL chains.
* Runnable specifies how a component accepts input, executes, and returns output — allowing components to fit into pipelines predictably.

LCEL’s design goals:

* Declarative composition: define what you want to run, not how to wire objects together imperatively.
* Readability: pipelines read left-to-right like data flow.
* Reusability: chains are values you can store, reuse, or nest.
* Extensibility: custom Runnables (functions, retrievers, formatters) plug directly into pipelines.

<Frame>
  <img alt="The image is a diagram explaining LangChain Expression Language, featuring a dark terminal window labeled &#x22;Runnable&#x22; and &#x22;Output&#x22; surrounded by colorful circles containing gear and box icons." />
</Frame>

Quick comparison — shell vs LCEL (Python pseudocode):

* Unix pipe example (shell)

```bash theme={null}
cat file.txt | grep "error" | wc -l
```

* Equivalent LCEL-style composition (Python pseudocode)

```python theme={null}
chain = prompt | llm | output_parser
result = chain.invoke({"question": "Tell me about the Godfather movie"})
```

How a typical LCEL pipeline flows:

1. A prompt or input-producing Runnable emits a string or structured payload.
2. Optional transformers or enrichment functions modify or augment the payload (e.g., add context).
3. A retriever fetches external knowledge (documents, embeddings, KBs) and enriches the prompt.
4. The enriched prompt is passed to the LLM Runnable, which returns raw model output.
5. An output parser or post-processor transforms the raw output into structured data or final results.

Because chains are first-class values, you can nest them:

* Compose smaller chains into larger workflows.
* Build hierarchical or meta-chains for complex systems.

Common LCEL components and use cases:

| Component Type | Typical Role                                  | Example                         |
| -------------- | --------------------------------------------- | ------------------------------- |
| Prompt         | Produce or format model input                 | `PromptTemplate`                |
| Transformer    | Enrich/modify payload before/after model call | custom function                 |
| Retriever      | Fetch external data to augment prompt         | `VectorStoreRetriever`          |
| LLM            | Generate text or structured output            | `OpenAI`, `Anthropic`           |
| Output Parser  | Parse model output into structured data       | `RegexParser`, `PydanticParser` |

<Callout icon="lightbulb">
  LCEL is increasingly the canonical way to express LangChain workflows. For a detailed comparison between imperative chain construction (e.g., `LLMChain`) and LCEL, see the [official LangChain documentation](https://langchain.readthedocs.io/en/latest/) for API examples, best practices, and custom Runnable implementations.
</Callout>

Where to use LCEL

* Building QA systems that combine retrievers, LLMs, and post-processors.
* Orchestrating complex pipelines with conditional logic and nested chains.
* Rapid prototyping of LLM-powered microservices and production systems.

What’s next in this lesson

* Practical demos and hands-on labs that demonstrate creating Runnables, building LCEL pipelines, and composing chains of chains.
* Examples will cover retriever-augmented generation, output parsing with structured types, and deploying LCEL workflows in production.

If you’re ready to build modular, composable LLM applications, LCEL is a foundational concept to master.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-1386-422b-98ad-3342dfc6aab3/lesson/59a17ad6-cdd8-42a5-868b-d7b47163d130" />
</CardGroup>
