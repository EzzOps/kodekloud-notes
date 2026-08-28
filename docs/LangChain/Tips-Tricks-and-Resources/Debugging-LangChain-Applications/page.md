# Create the handler and the chain
handler = StdOutCallbackHandler()

llm = ChatOpenAI()
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a {subject} teacher"),
        ("human", "Tell me about {concept}")
    ]
)
chain = LLMChain(llm=llm, prompt=prompt, callbacks=[handler])

# Invoke the chain
chain.invoke({"subject": "physics", "concept": "galaxy"})
```

When you run this, the stdout handler prints debug-like lifecycle messages to standard output. Example console output (truncated for brevity):

```text theme={null}
> Entering new LLMChain chain...
Prompt after formatting:
System: You are a physics teacher
Human: Tell me about galaxy

> Finished chain.
{
  "subject": "physics",
  "concept": "galaxy",
  "text": "A galaxy is a massive, gravitationally bound system that consists of stars, gas, dust, and dark matter. Galaxies come in various shapes and sizes, ranging from small dwarf galaxies to large spiral and elliptical galaxies. Our own Milky Way is a spiral galaxy that contains billions of stars."
}
```

## Key differences and control points

Use the right mechanism depending on environment and goals. The table below summarizes the options and when to use them.

| Option                          | When to use                                                                  | Example / Notes                                                                                                                                                        |
| ------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Global debug                    | Quick development-time debugging                                             | Enables global verbose output; simple but harder to route (`debug=True`)                                                                                               |
| Component-level `verbose`       | Inspect a specific component without changing global behavior                | Use `verbose=True` on the component: `LLMChain(..., verbose=True)`                                                                                                     |
| Callback handlers (recommended) | Production telemetry, structured logs, and routing to observability backends | Pass handlers via `callbacks=[handler]`. Use built-in handlers (e.g., `StdOutCallbackHandler`) or custom handlers to emit JSON, metrics, or push to external services. |

Example combining verbose and callbacks:

```python theme={null}
chain = LLMChain(llm=llm, prompt=prompt, callbacks=[handler], verbose=True)
chain.invoke({"subject": "physics", "concept": "galaxy"})
```

## Creating custom handlers when you need more control

For production use cases you’ll often want to implement a custom callback handler to format events, emit structured JSON, or push telemetry to a remote service. The handler receives lifecycle events and can perform any custom action required by your app.

Skeleton example (implement the methods you need):

```python theme={null}
from langchain.callbacks.base import BaseCallbackHandler

class MyLoggingHandler(BaseCallbackHandler):
    def on_chain_start(self, serialized, inputs, **kwargs):
        # Called when a chain starts
        print("chain started", inputs)

    def on_chain_end(self, outputs, **kwargs):
        # Called when a chain finishes
        # You can format outputs, write to files, or push to a logging backend
        print("chain finished", outputs)

    def on_llm_start(self, serialized, prompts, **kwargs):
        # Called when an LLM call starts
        pass

    def on_llm_end(self, response, **kwargs):
        # Called when the LLM call ends
        pass
```

Integrate your handler by passing it to the chain:

```python theme={null}
handler = MyLoggingHandler()
chain = LLMChain(llm=llm, prompt=prompt, callbacks=[handler])
```

## Best practices

* Use callback handlers for production logging, metrics, and observability.
* Keep stdout handlers for local development or CI debugging.
* Implement only the callback methods you need to minimize overhead.
* Ensure sensitive data (API keys, PII) is redacted before sending logs to third-party systems.
* Combine `verbose` on specific components with callbacks to get granular insight without overwhelming global logging.

<Callout icon="lightbulb">
  Callbacks are a flexible and powerful mechanism for observability and production-grade telemetry. Prefer callback handlers over global debug for routing structured logs, metrics, or formatted outputs to external systems.
</Callout>

## Summary

* Callbacks are invoked at key lifecycle events during chain execution.
* `StdOutCallbackHandler` is useful for quick, readable runtime output to the console.
* For production use, implement or reuse custom handlers to send structured logs, metrics, or trace data to files or cloud services.
* Combine component `verbose` flags with callbacks for targeted, flexible observability.

## Links and references

* [LangChain Documentation](https://langchain.readthedocs.io/)
* [OpenAI API Documentation](https://platform.openai.com/docs)
* Observability and logging references:
  * [Prometheus](https://prometheus.io/)
  * [OpenTelemetry](https://opentelemetry.io/)
  * [Datadog Logs](https://docs.datadoghq.com/logs/)

Later, we’ll walk through additional resources and practical examples to build production-grade LangChain applications.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-fdbc-45b1-a786-6c84bb7ffc76/lesson/4e795ffc-63cb-4935-b04e-fb4911326be5" />
</CardGroup>


# Debugging LangChain Applications

Source: https://notes.kodekloud.com/docs/LangChain/Tips-Tricks-and-Resources/Debugging-LangChain-Applications/page

Guide to enabling and interpreting LangChain global debug logging, with minimal chain example, sample logs, and tips for diagnosing, measuring latency, and inspecting prompts.

When inspecting a simple Jupyter notebook that uses LangChain, the typical flow is:

1. Define a prompt.
2. Create an LLM instance.
3. Wrap both in a chain.
4. Invoke the chain with inputs.

This guide provides a concise, corrected example showing the pattern, how to enable global debug logging in LangChain, and how to interpret the runtime logs to diagnose issues, measure latency, and inspect intermediate prompts.

## Quick example: a minimal Chat LLM chain

The example below demonstrates a minimal ChatOpenAI + ChatPromptTemplate + LLMChain setup. Note the updated import paths that match common LangChain usage.

```python theme={null}
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a {subject} teacher"),
        ("human", "Tell me about {concept}")
    ]
)

llm = ChatOpenAI()  # configure with api_key or environment variables as needed
chain = LLMChain(llm=llm, prompt=prompt)

result = chain.invoke({"subject": "physics", "concept": "galaxy"})
print(result)
```

## Typical chain output

A typical returned result (dictionary) contains the inputs and the generated text. Example:

```json theme={null}
{
  "subject": "physics",
  "concept": "galaxy",
  "text": "A galaxy is a gravitationally bound system of stars, stellar remnants, interstellar gas, dust, dark matter, and other astronomical objects. Galaxies can vary greatly in size and shape, from small dwarf galaxies with only a few billion stars to massive galaxies with trillions of stars. Our own galaxy, the Milky Way, is a barred spiral galaxy that contains roughly 100–400 billion stars. Galaxies are classified into spiral, elliptical, and irregular types. They are organized into larger structures such as galaxy clusters and superclusters. Studying galaxies helps us understand the evolution and dynamics of the cosmos."
}
```

## Why enable LangChain debug logging?

As chains grow in complexity—multiple components, custom transforms, callbacks, or several LLM calls—it's easy to lose visibility into what happened during execution. LangChain provides a global debug flag that instruments runs and prints structured, per-component logs showing inputs, prompts, outputs, and timing. This visibility helps you:

* Diagnose unexpected outputs or logic errors.
* Inspect intermediate prompts and transformed inputs.
* Measure token usage and per-component latency.
* Identify which component produced an error or unexpected text.

## Enabling global debug logging

Turn on global debug tracing with:

```python theme={null}
from langchain.globals import set_debug
set_debug(True)
```

Below is a full example that enables debug and runs the same chain:

```python theme={null}
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.globals import set_debug

set_debug(True)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a {subject} teacher"),
        ("human", "Tell me about {concept}")
    ]
)

llm = ChatOpenAI()
chain = LLMChain(llm=llm, prompt=prompt)

chain.invoke({"subject": "physics", "concept": "galaxy"})
```

## Sample debug output (abridged)

When debug is enabled, LangChain prints a structured trace. The example below is normalized for clarity:

```plaintext theme={null}
[chain/start] [1:chain:LLMChain] Entering Chain run with input:
{
  "subject": "physics",
  "concept": "galaxy"
}
[llm/start] [1:chain:LLMChain > 2:llm:ChatOpenAI] Entering LLM run with input:
{
  "prompts": [
    "System: You are a physics teacher\nHuman: Tell me about galaxy"
  ]
}
[llm/end]   [1:chain:LLMChain > 2:llm:ChatOpenAI] [3.27s] Exiting LLM run with output:
{
  "generations": [
    {
      "text": "Galaxies are vast systems of stars, dust, gas, and dark matter held together by gravity. They come in various shapes and sizes..."
    }
  ]
}
[chain/end] [1:chain:LLMChain] [3.27s] Exiting Chain run with output:
{
  "text": "Galaxies are vast systems of stars, dust, gas, and dark matter held together by gravity. They come in various shapes and sizes, ranging from small dwarf galaxies with just a few billion stars to massive galaxies like the Milky Way, which contains hundreds of billions of stars.\n\nGalaxies are the building blocks of the universe and are spread throughout the cosmos. They can be classified into different types based on their shape, such as spiral galaxies, elliptical galaxies, and irregular galaxies.\n\nStudying galaxies helps us understand the evolution of the universe, the formation of stars and planetary systems, and the distribution of dark matter."
}
```

## Interpreting the debug tags

Use the following as a quick reference to the most common log tags:

| Log tag                  | What it indicates            | Example information                              |
| ------------------------ | ---------------------------- | ------------------------------------------------ |
| `chain/start`            | Chain run began              | Inputs to the chain (e.g., `subject`, `concept`) |
| `llm/start`              | An LLM component was invoked | Exact prompt(s) sent to the model                |
| `llm/end`                | LLM returned                 | Generated text, `generations` arrays             |
| `chain/end`              | Chain finished               | Final chain output and any aggregated metadata   |
| Timing (e.g., `[3.27s]`) | Duration for the component   | Per-component latency, useful for bottlenecks    |

## Example LLM output metadata

The LLM output and the chain run often include metadata such as token usage and model identification. Example:

```json theme={null}
{
  "llm_output": {
    "token_usage": {
      "completion_tokens": 202,
      "prompt_tokens": 20,
      "total_tokens": 222
    },
    "model_name": "gpt-3.5-turbo",
    "system_fingerprint": "fp_4f0b692a78"
  },
  "run": null
}
```

## When to enable debug logs

* During development and troubleshooting.
* When iterating on prompt engineering and wanting to inspect the exact prompt(s) sent.
* To measure token usage and latency for cost/optimization decisions.
* While building or validating multi-component chains to see intermediate inputs/outputs.

<Callout icon="lightbulb">
  Enable `set_debug(True)` while developing or troubleshooting chains to obtain a detailed execution trace of each component. Debug logs may contain sensitive data—do not enable them in production or when handling private data.
</Callout>

## Links and references

* [LangChain Python documentation](https://python.langchain.com/en/latest/)
* [Jupyter](https://jupyter.org)
* [OpenAI API (for model configuration and keys)](https://platform.openai.com/)

If you need help interpreting a specific debug trace or want assistance instrumenting more complex multi-component chains (callbacks, transforms, or retrievers), share the trace and chain configuration and we can walk through it step by step.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-fdbc-45b1-a786-6c84bb7ffc76/lesson/2306b896-2eb1-409b-84f6-f2c392dbd3c4" />
</CardGroup>
