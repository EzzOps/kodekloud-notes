# Build the chain: prompt -> llm -> output_parser
chain = prompt | llm | output_parser

result = chain.invoke({"topic": "movies", "question": "Tell me about The Godfather movie"})
print(result)
```

Expected truncated example output:

```plaintext theme={null}
"The Godfather" is a classic American crime film released in 1972, directed by Francis Ford Coppola. The movie is based on the novel of the same name by Mario Puzo. It stars Marlon Brando as Vito Corleone and Al Pacino as Michael Corleone...
```

## RunnablePassthrough as a no-op passthrough

Inserting a plain `RunnablePassthrough()` anywhere in the pipeline with no `.assign(...)` simply forwards the data unchanged. This is useful as a placeholder or to preserve structure when conditionally inserting logic.

```python theme={null}
from langchain_core.runnables import RunnablePassthrough

# Passthrough at the start (no change to behavior)
chain = RunnablePassthrough() | prompt | llm | output_parser
result = chain.invoke({"topic": "movies", "question": "Tell me about The Godfather movie"})
print(result)

# Passthrough at the end (no change to behavior)
chain = prompt | llm | output_parser | RunnablePassthrough()
result = chain.invoke({"topic": "movies", "question": "Tell me about The Godfather movie"})
print(result)
```

Both examples produce the same output as the basic chain above because the passthrough forwards the input unchanged.

## RunnablePassthrough as an injector (`.assign(...)`)

`RunnablePassthrough` can add or override keys in the input dictionary at the point where it is placed in the chain. Use `.assign(...)` to compute or pin values. The assign mappers receive the runtime input (commonly named `x`), so you can compute values based on the current state or return constants.

Example: build a chain that accepts only `question` and injects `topic = "movies"` before the prompt is evaluated.

```python theme={null}
from langchain_core.runnables import RunnablePassthrough

# Chain accepts only "question". Inject "topic" = "movies" prior to prompt.
new_chain = (
    RunnablePassthrough()  # forward initial request
    | RunnablePassthrough().assign(topic=lambda x: "movies")  # inject topic
    | prompt
    | llm
    | output_parser
)

# Now callers provide only the question
result = new_chain.invoke({"question": "Tell me about Inception"})
print(result)
```

You can test the effect on the runtime dictionary:

```python theme={null}
test_chain = RunnablePassthrough() | RunnablePassthrough().assign(topic=lambda x: "movies")
print(test_chain.invoke({"question": "Tell me about Inception"}))
# Expected output: {'question': 'Tell me about Inception', 'topic': 'movies'}
```

## Use cases and quick reference

| Use Case                 | Behavior                                                         | Example                                                                          |
| ------------------------ | ---------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| No-op passthrough        | Forwards input unchanged                                         | `RunnablePassthrough()`                                                          |
| Inject constant key      | Adds a pinned value at runtime                                   | `RunnablePassthrough().assign(topic=lambda x: "movies")`                         |
| Compute value from input | Generate value using the current runtime payload                 | `RunnablePassthrough().assign(user_id=lambda x: x.get("session", {}).get("id"))` |
| Preserve external API    | Hide internal keys from callers by injecting defaults internally | Use `.assign(...)` inside the chain, callers only supply public keys             |

## Why this is useful

> **lightbulb** `RunnablePassthrough` is a small but powerful primitive. Use it to:

  * keep pipeline elements as hollow pipes when no transformation is required,
  * inject or compute additional inputs at runtime with `.assign(...)`,
  * pin or hide configuration/context values so external callers don't need to supply them.

## Notes and best practices

* `.assign(...)` mappers are evaluated at runtime and merged into the dictionary forwarded to downstream components.
* The lambda parameter name (often `x`) is arbitrary; it represents the current runtime input at that stage. If the injected value is constant, you can ignore it (e.g., `lambda x: "movies"`).
* Instantiate parsers and runnables explicitly (e.g., `StrOutputParser()`), and prefer clear variable names for readability.
* Use `RunnablePassthrough` to preserve external call signatures while adding internal context or configuration.
* When computing values based on prior steps, ensure the required keys exist to avoid runtime errors — validate or provide fallbacks inside your lambda.

## Example patterns

* Insert configuration or user context only when needed.
* Replace complex conditional logic in the chain with targeted, testable mappers using `.assign(...)`.
* Combine multiple `.assign(...)` calls to coalesce values from different sources (e.g., session, defaults, and request).

## Next steps

You can convert arbitrary Python functions into runnable components (for example, using a `RunnableLambda`) to encapsulate custom logic as first-class LCEL runnables. This lets custom logic participate directly in chains and simplifies testing and reuse.

## Links and references

* [LangChain Documentation](https://langchain.com/)
* [LangChain Core: Runnables Patterns](https://github.com/langchain-ai/langchain)
* [OpenAI Chat Models (ChatOpenAI)](https://platform.openai.com/docs/models)

- [Watch Video](https://learn.kodekloud.com/user/courses/langchain/module/754457c5-1386-422b-98ad-3342dfc6aab3/lesson/18f5c92b-a25c-4449-ae23-6c65658209d5)


# LCEL Demo 5

Source: https://notes.kodekloud.com/docs/LangChain/Introduction-to-LCEL/LCEL-Demo-5/page

Demonstrates an LCEL chain-of-chains pipeline that generates a title, outline, 200-word blog post, and social-media summary using prompts, LLMs, parsers, and passthroughs.

This lesson demonstrates a practical, end-to-end LCEL content-generation pipeline that composes multiple mini-chains into a single workflow. The pipeline produces an impactful title, a detailed outline, a 200-word blog post, and a short social-media style summary by chaining prompt → LLM → parser → passthrough for each stage.

## Key idea and imports

We use:

* `ChatPromptTemplate` to define prompts with placeholders
* `ChatOpenAI` as the LLM runnable (swapable per stage)
* `StrOutputParser` to extract clean string outputs
* `RunnablePassthrough` to attach parsed strings to keys in the execution context so downstream mini-chains can reference them

> **lightbulb** This pattern composes small, focused runnables into a chain-of-chains. Each stage returns a parsed string that is then attached to the execution context under a key like `title`, `outline`, or `blog`, allowing subsequent prompts to reference those values via placeholders (for example, `"{title}"`).

Example Python imports and the pipeline wiring:

```python theme={null}
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
```

## Example pipeline (title → outline → blog → summary)

Below is a compact, readable pipeline that demonstrates the pattern. Note how each mini-chain ends with a `StrOutputParser()` followed by attaching the parsed value to a new key with `RunnablePassthrough()`.

```python theme={null}
