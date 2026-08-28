# examine handler.events to inspect the full lifecycle
```

JavaScript — callback-like handlers

* The JS SDK uses a `callbacks` array to pass handlers. Create a handler object with methods such as `onLLMStart`, `onLLMEnd`, `onChainStart`, `onChainEnd`, etc., and pass it to the model/chain.
* Example reference: [LangChain.js callbacks docs](https://js.langchain.com/docs/modules/callbacks/overview) (link for reference).

Patterns for callbacks

* Persist events to a JSON file or database for later analysis.
* Enrich events with timestamps, latencies, and environment metadata.
* Correlate events with unique run IDs to stitch together multi-step flows.

## Capture intermediate inputs and outputs

When parsing fails or outputs are malformed, locating the exact intermediate value that caused the failure is crucial.

Common capture patterns:

* In-memory capture: store intermediate values in a list or dict on a callback handler for quick debugging.
* File-based capture: dump prompts and responses to a file (rotating logs) for persistent review.
* Structured logging & tracing: send events to an observability backend (e.g., Datadog, Elastic, or OpenTelemetry).

Example: writing prompts + responses to a file

```python theme={null}
import json
from datetime import datetime

def persist_event(event, filename="langchain_trace.jsonl"):
    event["_ts"] = datetime.utcnow().isoformat()
    with open(filename, "a") as f:
        f.write(json.dumps(event) + "\n")

# inside your callback handler methods:
# persist_event({"type":"llm_start", "prompts": prompts})
# persist_event({"type":"llm_end", "response": response})
```

## Debugging common problems

* Unexpected output format from parser:
  * Capture raw LLM text before parsing to see if the model deviated from the template.
  * Use output parser tests with unit tests (feed sample LLM outputs to parser and assert parse results).

* Agent selects wrong tool:
  * Enable agent callbacks to capture `on_agent_action` and `on_agent_finish`.
  * Inspect tool inputs to verify the agent's reasoning step.

* Prompt formatting issues:
  * Enable `verbose=True` or capture the final prompt text in callbacks.
  * Validate templates with example inputs before running them in production.

## Best practices

* Always start with `verbose=True` in development to surface immediate issues.
* Use callback handlers to store traces, then switch verbose off in production.
* Sanitize logs before persisting or sending to external observability systems.
* Add unit tests for prompts and parsers to catch format regressions early.

## Quick reference table

| Topic                 | What to enable                                       | Where to capture                              |
| --------------------- | ---------------------------------------------------- | --------------------------------------------- |
| Prompt debugging      | `verbose=True` on chain or LLM                       | Callback `on_llm_start` or `on_chain_start`   |
| Output parsing        | Capture raw LLM output                               | Callback `on_llm_end` then run parser locally |
| Agent troubleshooting | Agent-specific callbacks (agent actions, tool calls) | `on_agent_action`, `on_agent_finish`          |
| Persistent traces     | Use callback handler to persist JSON lines           | File, DB, or observability backend            |

## Links and references

* LangChain documentation — [https://langchain.com/docs](https://langchain.com/docs)
* LangChain callbacks (Python) — [https://python.langchain.com/en/latest/modules/callbacks/index.html](https://python.langchain.com/en/latest/modules/callbacks/index.html)
* LangChain.js callbacks — [https://js.langchain.com/docs/modules/callbacks/overview](https://js.langchain.com/docs/modules/callbacks/overview)

***

By combining verbose runtime flags with custom callback handlers and a standardized persistence pattern for traces, you can quickly locate the source of errors, validate prompt formats, and build a robust observability workflow around LangChain applications.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-fdbc-45b1-a786-6c84bb7ffc76/lesson/873344b7-d6b4-4c2f-86ad-82ae24246258" />
</CardGroup>


# Using Verbose Flag

Source: https://notes.kodekloud.com/docs/LangChain/Tips-Tricks-and-Resources/Using-Verbose-Flag/page

Explains enabling verbose logging in LangChain to inspect formatted prompts, lifecycle events, and outputs, how to set verbose True, use it selectively, and route logs via callbacks

In this lesson we'll demonstrate how to enable verbose logging for a specific LangChain component so you can inspect what happens during execution. This technique is useful for debugging prompt formatting, understanding chain lifecycle events, and routing runtime information to custom handlers.

We use an LLMChain with a ChatPromptTemplate that contains placeholders. First, here is the same program with verbose logging disabled.

```python theme={null}
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {subject} teacher"),
    ("human", "Tell me about {concept}")
])

llm = ChatOpenAI()
chain = LLMChain(llm=llm, prompt=prompt)

result = chain.invoke({"subject": "physics", "concept": "galaxy"})
print(result)
```

Example output (non-verbose):

```python theme={null}
{
  'subject': 'physics',
  'concept': 'galaxy',
  'text': 'Galaxies are massive systems of stars, stellar remnants, interstellar gas, dust, dark matter, and other astronomical objects bound together by gravity. They come in a variety of shapes and sizes, ranging from dwarf galaxies with just a few billion stars to giant galaxies with hundreds of billions of stars.\n\nOur own Milky Way galaxy is a spiral galaxy, with a central bulge surrounded by a disk of stars, gas, and dust...'
}
```

## Enable verbose output for a chain

To print lifecycle messages and the fully formatted prompt (placeholders replaced), pass `verbose=True` when constructing the component:

```python theme={null}
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {subject} teacher"),
    ("human", "Tell me about {concept}")
])

llm = ChatOpenAI()
chain = LLMChain(llm=llm, prompt=prompt, verbose=True)

result = chain.invoke({"subject": "physics", "concept": "galaxy"})
print(result)
```

Verbose console output (example):

```text theme={null}
> Entering new LLMChain chain...
Prompt after formatting:
System: You are a physics teacher
Human: Tell me about galaxy

> Finished chain.
{'subject': 'physics',
 'concept': 'galaxy',
 'text': 'A galaxy is a vast system of stars, stellar remnants, interstellar gas, dust, dark matter, and other celestial objects bound together by gravity. These systems can contain billions or even trillions of stars, as well as various types of celestial bodies such as planets, moons, asteroids, and comets.\n\nOur own galaxy, the Milky Way, is a barred spiral galaxy that contains an estimated 100-400 billion stars. Galaxies come in various shapes and sizes, including spiral, elliptical, and irregular...'}
```

## What the verbose flag exposes

Verbose is a targeted debugging aid that reveals key runtime information for a component. It typically provides:

|                                           What it prints | Why it helps                                                                |
| -------------------------------------------------------: | --------------------------------------------------------------------------- |
| Lifecycle messages (entering/finishing a chain or agent) | Shows when a component starts and ends, useful for timing and flow analysis |
|      The prompt after formatting (placeholders replaced) | Lets you verify the exact text sent to the LLM and catch template mistakes  |
|                                Response or final outputs | Confirms what the component returned and how it was processed               |

## Use verbose selectively

Enable `verbose=True` only on the component(s) you need to inspect. This focused approach avoids overwhelming output from other parts of your system while giving clear visibility into the component under investigation.

|    Component type | How to enable verbose                                 | Example                          |
| ----------------: | ----------------------------------------------------- | -------------------------------- |
|             Chain | Pass `verbose=True` to the chain constructor          | `LLMChain(..., verbose=True)`    |
|             Agent | Pass `verbose=True` to the agent when creating it     | `Agent(..., verbose=True)`       |
| Custom components | Implement and expose a verbose flag in your component | `MyComponent(..., verbose=True)` |

<Callout icon="lightbulb">
  Use `verbose=True` on only the components you need to inspect. Global debug or tracing options can produce a large amount of output; verbose is a targeted way to get helpful runtime visibility.
</Callout>

## Example input data

Below is the input dictionary used in the examples (shown in a code block to avoid MDX parsing issues):

```python theme={null}
{"subject": "physics", "concept": "galaxy"}
```

## Routing verbose output with callbacks

If you prefer structured logging or tracing, LangChain callbacks let you capture verbose events and route them to custom handlers (for example, sending logs to a monitoring system, or collecting them in a structured store). Use callbacks to integrate verbose output with your observability stack.

For more details, see:

* LangChain documentation: [https://langchain.readthedocs.io/](https://langchain.readthedocs.io/)
* ChatOpenAI: [https://pypi.org/project/langchain-openai/](https://pypi.org/project/langchain-openai/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-fdbc-45b1-a786-6c84bb7ffc76/lesson/ea0b058a-7c2d-4b17-81e6-fb4026f5a6fe" />
</CardGroup>
