# First invocation
base_chain.invoke({"ability": "math", "input": "What's a right-angled triangle?"})
```

Example output:

```text theme={null}
AIMessage(content='A triangle with one angle measuring 90 degrees.', response_metadata={...}, id='run-614688a6-...')
```

Now a follow-up question, still without passing any history:

```python theme={null}
# Follow-up invocation without history
base_chain.invoke({"ability": "math", "input": "What are the other types?"})
```

Because the model was not provided the prior exchange as part of the prompt, it typically asks for clarification:

```text theme={null}
AIMessage(content='Could you please provide more context or specify what you are referring to?', response_metadata={...}, id='run-875b6d0b-...')
```

This demonstrates the core problem: LLMs do not retain conversation context across separate calls unless you explicitly include that context in the prompt.

## Adding a MessagesPlaceholder to carry short-term memory

To give the model access to prior turns, add a `MessagesPlaceholder` to the chat prompt template and pass a `history` list on invocation. At runtime the placeholder will be replaced with the provided messages.

```python theme={null}
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI

model = ChatOpenAI()
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You're an assistant who's good at {ability}. Respond in 20 words or fewer"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)
base_chain = prompt | model
```

Create a simple `history` list that represents the prior human/AI exchange, then invoke the chain while passing that history:

```python theme={null}
history = [
    ("human", "What's a right-angled triangle?"),
    ("ai", "A right-angled triangle has one angle of 90 degrees, with the other two angles summing to 90 degrees.")
]

# Now the model receives the previous exchange as part of the prompt
base_chain.invoke({"ability": "math", "input": "What are the other types?", "history": history})
```

With the history included, the model can respond in context:

```text theme={null}
AIMessage(content='Other types of triangles include equilateral (all sides equal), isosceles (two sides equal), and scalene (no sides equal).', response_metadata={...}, id='run-ed7687bf-...')
```

<Callout icon="lightbulb">
  The `variable_name` you assign to `MessagesPlaceholder` (for example, `"history"`) is the key you must use when passing the list to `invoke`. The name can be anything, but the invocation dictionary key must match the placeholder's `variable_name`.
</Callout>

## Quick reference

|              Concept | Purpose                                                             | Example                                               |
| -------------------: | ------------------------------------------------------------------- | ----------------------------------------------------- |
| Chat prompt template | Define the ordered set of messages the model sees                   | `ChatPromptTemplate.from_messages([...])`             |
|  MessagesPlaceholder | Placeholder for injected conversation turns at runtime              | `MessagesPlaceholder(variable_name="history")`        |
|  History list format | Sequence of prior turns passed to the placeholder                   | `history = [("human", "Hi"), ("ai", "Hello")]`        |
|      Invocation dict | Values passed when running the chain (must include placeholder key) | `{"ability":"math","input":"...","history": history}` |

## Summary and next steps

* Without explicit history included in the prompt, the model has no memory of prior invocations.
* Adding a `MessagesPlaceholder` to your chat prompt template and providing a `history` list at invocation time gives your application short-term conversational memory.
* Use this technique for multi-step workflows, follow-up questions, or any conversational app that needs access to preceding messages.

## Further reading

* [LangChain ChatPromptTemplate docs](https://python.langchain.com/en/latest/modules/prompts/how_to_guides/chat_prompt_template.html)
* [LangChain Concepts & Usage](https://python.langchain.com/en/latest/index.html)
* [OpenAI Chat API reference](https://platform.openai.com/docs/guides/chat)

Experiment: try changing the contents of `history`, the `ability` parameter, or the user `input` to observe how the model's responses change when conversation history is included.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/abd1e527-3f6e-4e04-b421-3b1f8de5c69d/lesson/2b05e60c-8398-432c-8215-1bb3a9e64cb5" />
</CardGroup>


# Exploring Configurable Parameters

Source: https://notes.kodekloud.com/docs/LangChain/Adding-Memory-to-LLM-Apps/Exploring-Configurable-Parameters/page

Explains configurable fields for runnables to override runtime parameters like LLM model per invocation, enabling cost control and flexible per-request model selection.

This lesson explains configurable fields — a mechanism for passing runtime parameters to runnables (for example, switching the LLM model used for a specific invocation). Configurable fields let you avoid hard-coding options when initializing a runnable and instead override them per invocation. This is useful for cost control (default to a cheaper model) and flexibility (upgrade to a stronger model when needed).

## Why use configurable fields?

* Avoid reinitializing runnables to change runtime behavior.
* Control costs by selecting cheaper defaults and overriding on demand.
* Compose overrides with dynamic prompts and memory for flexible workflows.

## Quick overview

1. Import required classes.
2. Register a configurable field on a runnable (e.g., `model_name`).
3. Compose the runnable with a prompt.
4. Invoke normally (uses default) or override with `with_config(configurable={...})`.

## Imports and setup

```python theme={null}
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import ConfigurableField
```

## Register a configurable field on a runnable

Initialize the ChatOpenAI runnable with a default model (for example `gpt-3.5-turbo`) and expose `model_name` as a configurable field that can be overridden at invocation time:

```python theme={null}
model = ChatOpenAI(model_name="gpt-3.5-turbo").configurable_fields(
    model_name=ConfigurableField(
        id="model_name",
        name="model name",
        description="The GPT model to use for chat",
    )
)
```

## Create a prompt template

Wrap the template text in backticks in prose to avoid MDX parsing issues:

```python theme={null}
prompt = PromptTemplate.from_template("Write a Haiku on {subject}")
```

## Compose the chain and invoke (default)

Compose the prompt and the runnable, then invoke normally. This uses the runnable's default model (`gpt-3.5-turbo`):

```python theme={null}
chain = prompt | model
