# Generate an impactful title for the input
title = (
    ChatPromptTemplate.from_template("Generate an impactful title for {input}")
    | ChatOpenAI()
    | StrOutputParser()
    | {"title": RunnablePassthrough()}
)

# Generate a detailed outline for the generated title
outline = (
    ChatPromptTemplate.from_template("Generate a detailed outline for {title}")
    | ChatOpenAI()
    | StrOutputParser()
    | {"outline": RunnablePassthrough()}
)

# Generate a blog post based on the outline
blog = (
    ChatPromptTemplate.from_template(
        "Generate a 200 word blog post based on the outline: {outline}"
    )
    | ChatOpenAI()
    | StrOutputParser()
    | {"blog": RunnablePassthrough()}
)

# Generate a short summary for the blog post (for social media)
summary = (
    ChatPromptTemplate.from_template("Generate a short summary for the post: {blog}")
    | ChatOpenAI()
    | StrOutputParser()
)

# Compose the full content chain (chain of chains)
content_chain = title | outline | blog | summary
```

## Pipeline overview (quick reference)

| Stage   | Prompt placeholder used | Output attached key | Purpose                                        |
| ------- | ----------------------- | ------------------- | ---------------------------------------------- |
| Title   | `"{input}"`             | `title`             | Create a short, impactful title                |
| Outline | `"{title}"`             | `outline`           | Produce a structured outline for the title     |
| Blog    | `"{outline}"`           | `blog`              | Expand the outline into \~200 words of content |
| Summary | `"{blog}"`              | (final output)      | Create a short social-media-ready summary      |

## Notes on placeholders and MDX safety

* When mentioning prompt placeholders in prose, always wrap them in backticks so MDX does not interpret curly braces as JavaScript: `"{input}"`, `"{title}"`, `"{outline}"`, `"{blog}"`.

## How RunnablePassthrough connects stages

Each mini-chain parses the LLM output into a string via `StrOutputParser()`. Using `| {"title": RunnablePassthrough()}` attaches that parsed string under the `title` key in the chain's execution context. Downstream chat prompts can then reference `"{title}"` to receive the exact string produced by the previous stage.

This produces a chain-of-chains effect: the output from one mini-chain becomes the input to the next via context keys.

## Invoking the pipeline

Call the top-level chained runnable with a single input dictionary. Intermediate values (like `title`, `outline`, `blog`) will be attached to the chain execution context while the final return value is the summary.

```python theme={null}
response = content_chain.invoke({"input": "The impact of AI on jobs"})
# `response` contains the final chain output (the summary).
# Intermediate outputs are available in the chain execution context as `title`, `outline`, and `blog`.
```

## Execution considerations

* This is a multi-stage pipeline: each mini-chain triggers a separate LLM call and parsing step. Expect longer runtimes than a single LLM request.
* For rapid iteration you can execute each mini-chain independently to validate or refine a stage without running the entire pipeline.

## Extending the pipeline: different LLMs per stage

A common pattern is to use specialized models per task:

* Use a fast, cheap model tuned for short creative outputs for the `title` stage.
* Use a model good at structured responses for the `outline` stage.
* Use a high-quality, longer-context model for the `blog` stage.

To swap models, replace `ChatOpenAI()` with another LLM runnable at the stage you want to change. The LCEL wiring (prompts → parser → passthrough) remains identical.

<Callout icon="lightbulb">
  Using different LLMs per mini-chain is a powerful approach: you can optimize cost and quality by selecting the best model for each subtask (e.g., catchy titles, structured outlines, long-form writing, and concise summarization).
</Callout>

## What we achieved

* Demonstrated how LCEL composes small runnable units (prompt → LLM → parser → attached key) into a larger, maintainable workflow.
* Built a reusable pattern for content generation, multi-stage processing, and orchestrating different LLMs for specialized subtasks.

## Links and references

* [LangChain Core documentation](https://python.langchain.com/)
* [OpenAI API documentation](https://platform.openai.com/docs)

In a future lesson we will explore memory, retrieval, and building more complex chains and integrations—stay tuned.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/754457c5-1386-422b-98ad-3342dfc6aab3/lesson/1f3becbf-1cff-4ffc-9082-6e462c0617b6" />
</CardGroup>


# LCEL Demo 6

Source: https://notes.kodekloud.com/docs/LangChain/Introduction-to-LCEL/LCEL-Demo-6/page

Demonstrates building LCEL pipelines combining prompts, models, parsers, and RunnableLambda functions to transform, inspect, and debug model outputs and visualize pipeline graphs.

This lesson demonstrates more advanced LCEL (LangChain Execution Layer) patterns: building a simple pipeline and extending it with custom runnable components to transform, inspect, and debug model outputs. You'll see how to compose prompts, models, parsers, and Python runnables using the pipe (`|`) operator to create expressive, debuggable pipelines.

## Initial chain

We start with a minimal chain that includes:

* A prompt asking for a one-line description of a topic
* A ChatOpenAI model
* A string output parser

```python theme={null}
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("Give me a one-line description of {topic}")
model = ChatOpenAI()
output_parser = StrOutputParser()

chain = prompt | model | output_parser

chain.invoke({"topic": "AI"})
```

Example output:

```plaintext theme={null}
'AI is the simulation of human intelligence processes by machines, especially computer systems.'
```

## Adding a custom runnable to transform the output

Goal: convert the model output to title case by wrapping a simple Python function in `RunnableLambda` and appending it to the chain so it receives the parser output at runtime.

```python theme={null}
from langchain_core.runnables import RunnableLambda

def to_titlecase(text: str) -> str:
    return text.title()
```

Attach the runnable to the chain:

```python theme={null}
chain = prompt | model | output_parser | RunnableLambda(to_titlecase)
result = chain.invoke({"topic": "AI"})
print(result)
```

Observed behavior:

```plaintext theme={null}
'Ai Is The Simulation Of Human Intelligence Processes By Machines, Especially Computer Systems.'
```

Note: Python's `str.title()` transforms `"AI"` into `"Ai"`. That behavior is expected for title-casing with `str.title()`.

<Callout icon="lightbulb">
  When appending a Python function to an LCEL chain, pass the function reference (e.g., `RunnableLambda(to_titlecase)`), not a function call. LangChain invokes it at runtime as part of the pipeline.
</Callout>

## Adding a second runnable to inspect output length

Next, add a second runnable that logs the transformed text (for debugging) and returns its character length. This shows how to chain multiple custom runnables to both inspect and transform data.

```python theme={null}
from langchain_core.runnables import RunnableLambda

def get_len(text: str) -> int:
    print(text)   # debug printing
    return len(text)
```

Append both runnables to the chain:

```python theme={null}
chain = prompt | model | output_parser | RunnableLambda(to_titlecase) | RunnableLambda(get_len)
