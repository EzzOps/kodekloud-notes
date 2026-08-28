# Set your OpenAI API key in the environment:
os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"
```

## 1) Define examples

Create a small list of example input/output pairs. In this demo, outputs are exact reversals of the inputs:

```python theme={null}
examples = [
    {"input": "India", "output": "aidnI"},
    {"input": "Canada", "output": "adanaC"},
    {"input": "Australia", "output": "ailartsuA"},
]
```

## 2) Create the example prompt

Construct a prompt template that defines how each example should be formatted for the chat. Each example is represented as a human message followed by an AI message:

```python theme={null}
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)
```

## 3) Build the few-shot message template

This collates all examples into a single few-shot block that can be inserted into a larger prompt sequence:

```python theme={null}
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)
```

## 4) Inspect the few-shot formatted content

You can inspect the generated few-shot block to verify formatting:

```python theme={null}
print(few_shot_prompt.format())
```

Expected formatted output:

```plaintext theme={null}
Human: India
AI: aidnI
Human: Canada
AI: adanaC
Human: Australia
AI: ailartsuA
```

## 5) Assemble the final chat prompt template

Combine a system instruction with the few-shot examples block and a human placeholder for the runtime input:

```python theme={null}
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a linguistic specialist."),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)
```

## 6) Format messages for a new input

Format the concrete message sequence for runtime inputs (for example, `"Brazil"`). This produces the actual messages that will be sent to the model:

```python theme={null}
messages = prompt_template.format_messages(input="Brazil")

# Example of the message sequence sent to the model:
# System: You are a linguistic specialist.
# Human: India
# AI: aidnI
# Human: Canada
# AI: adanaC
# Human: Australia
# AI: ailartsuA
# Human: Brazil
```

## 7) Invoke the chat model

Create a chat model instance and call it with the formatted messages. The model should generalize the reversal mapping from the few-shot examples and reverse the runtime input:

```python theme={null}
model = ChatOpenAI()
response = model(messages)
print(response.content)  # Expected: 'lizarB'
```

## Why this works

* The few-shot block provides concrete input/output pairs that demonstrate the intended transformation without an explicit instruction like "reverse the string".
* The system role ("You are a linguistic specialist.") nudges the model toward language-focused behaviors.
* At runtime you only supply the new `input`; the model infers the mapping from the examples.

<Callout icon="lightbulb">
  Few-shot prompting is especially effective when you want the model to generalize from a small set of representative examples (e.g., rows from a CSV or entries from a database). Choose examples that cover the variations you expect the model to handle.
</Callout>

## Notes and best practices

* Use at least a few examples (3+ is a reasonable starting point) so the model can identify consistent patterns.
* Ensure examples are representative of expected inputs and edge cases.
* You can reuse the same template structure to teach different mappings by swapping the `examples` list or adjusting the system role.
* For larger or more complex transformations, combine few-shot examples with a brief instruction in the system role to improve reliability.

## Quick reference

| Component                          | Purpose                                                 | Example                                                              |
| ---------------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------- |
| `ChatPromptTemplate`               | Build chat-style templates from message-role pairs      | `ChatPromptTemplate.from_messages([...])`                            |
| `FewShotChatMessagePromptTemplate` | Collate multiple example prompts into a few-shot block  | `FewShotChatMessagePromptTemplate(example_prompt=..., examples=...)` |
| `ChatOpenAI`                       | Chat model wrapper to send formatted messages to an LLM | `ChatOpenAI()`                                                       |
| `input` placeholder                | Runtime value injected into the human message           | use as `"{input}"` in templates                                      |

Links and references:

* [LangChain Documentation](https://python.langchain.com)
* [OpenAI API Documentation](https://platform.openai.com/docs)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/ae260750-791b-496c-991f-0d0333f61e40/lesson/e2f5f01a-0ea8-4905-8b0b-29d174baedb8" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/langchain/module/ae260750-791b-496c-991f-0d0333f61e40/lesson/c6cfbec7-d94d-4eaa-990e-4845b4b0ab5b" />
</CardGroup>


# Getting Started with LLMs

Source: https://notes.kodekloud.com/docs/LangChain/Interacting-with-LLMs/Getting-Started-with-LLMs/page

Intro guide to using LangChain LLM wrappers, showing minimal code, provider switching between OpenAI and Google Gemini, authentication via environment variables, and practical examples and best practices.

Welcome to the first demo of this course. In this lesson you'll learn how to interact with large language models (LLMs) using LangChain wrappers. The objectives are:

* Show the minimal code required to call an LLM.
* Demonstrate how to switch providers (OpenAI and Google Generative AI / Gemini) while keeping the same prompt and code flow.
* Highlight the environment variables and authentication patterns required for each provider.

<Callout icon="lightbulb">
  Before you begin, install the core LangChain package and any provider-specific integrations you plan to use. Make sure provider API keys or credentials are set as environment variables as shown below.
</Callout>

***

## 1) Authentication and environment variables

Store credentials in environment variables rather than hard-coding them. On a UNIX-like shell:

```bash theme={null}
