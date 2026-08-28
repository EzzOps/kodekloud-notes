# Initialize a chat model (e.g., LangChain's wrapper for OpenAI)
chat = ChatOpenAI(temperature=0.2)

# Build the conversation: system message first, then a human message
messages = [
    SystemMessage(content="You are a professional dietician who gives concise, evidence-based advice."),
    HumanMessage(content="What is a healthy breakfast for someone trying to lose weight?")
]

# Call the chat model with the messages list
response = chat(messages)

# The reply is available as an AI message; print its text content
print(response.content)
```

## Best practices and common usage patterns

* Always place the system message at the start of the message list so it influences later replies.
* Send human messages repeatedly as the user interacts; the model will reply with AI messages for each turn.
* If you need to change the assistant’s persona mid-session, prefer replacing the system message rather than appending multiple system messages (multiple system messages can be confusing).
* To preserve a persona across separate sessions, include the system message at the start of each new session—models do not retain state between sessions.

<Callout icon="lightbulb">
  Use the system message to reliably set tone and role (for example, professional, friendly, or terse). Treat the sequence of messages as the full conversation context sent to the model.
</Callout>

## Next steps

In the following sections we will demonstrate how to construct, manage, and reuse message lists in LangChain for multi-turn conversations, explore strategies for system message design, and show patterns for storing and replaying conversation history.

## Links and references

* [LangChain](https://learn.kodekloud.com/user/courses/langchain)
* [Introduction to OpenAI course](https://learn.kodekloud.com/user/courses/introduction-to-openai)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/ae260750-791b-496c-991f-0d0333f61e40/lesson/677506d8-0d22-4c90-bee6-b358e5f08e30" />
</CardGroup>


# Parsing Model Output Demo 1

Source: https://notes.kodekloud.com/docs/LangChain/Interacting-with-LLMs/Parsing-Model-Output-Demo-1/page

Demonstrates using output parsers to enforce LLM response formats and convert comma separated model outputs into native Python lists for reliable downstream processing.

In this lesson we explore output parsers and how they convert free-text responses from large language models into structured Python data. Output parsers make it simple to enforce predictable formats (CSV, JSON, lists) so downstream code can consume model outputs reliably.

<Frame>
  <img alt="The image shows the interface of a Jupyter Notebook, displaying an empty code cell ready for input. The toolbar and menu options are visible at the top." />
</Frame>

<Callout icon="lightbulb">
  This lesson assumes your OpenAI API key is already configured in your environment.
</Callout>

## Quick overview

* Goal: Instruct an LLM to return a comma-separated list and parse it into a native Python `list`.
* Approach: Append parser-provided `format_instructions` to the prompt so the model emits a predictable format, then use the parser to convert the text to Python objects.

## 1. Imports and basic prompt setup

Import the required classes, create an LLM client, and define a simple prompt template.

```python theme={null}
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.output_parsers import CommaSeparatedListOutputParser

llm = OpenAI()
prompt = PromptTemplate(
    template="List 3 {things}",
    input_variables=["things"]
)
```

## 2. Invoke the model with a simple prompt (raw output)

Call the LLM without any parser instructions to see the default textual output.

```python theme={null}
raw = llm.invoke(input=prompt.format(things="countries that play cricket in world cup"))
print(raw)
```

Example raw output (string)

```text theme={null}
1. India
2. Australia
3. England
```

This raw response is a plain string with numbered lines. To use it programmatically you'd typically write manual parsing logic (strip numbering, split lines). Output parsers automate this process.

## 3. Add a CommaSeparatedListOutputParser and get format instructions

The `CommaSeparatedListOutputParser` provides human-readable instructions that you append to your prompt. These instructions encourage the LLM to produce CSV-style output that can be parsed reliably.

```python theme={null}
output_parser = CommaSeparatedListOutputParser()
format_instructions = output_parser.get_format_instructions()
print(format_instructions)
```

Format instructions printed:

```text theme={null}
Your response should be a list of comma separated values, eg: `foo, bar, baz`
```

## 4. Inject the format instructions into the prompt

Use `partial_variables` in `PromptTemplate` to include the parser's `format_instructions` in the prompt. This keeps your prompt template flexible and reusable.

```python theme={null}
prompt = PromptTemplate(
    template="List 3 {things}.\n{format_instructions}",
    input_variables=["things"],
    partial_variables={"format_instructions": format_instructions}
)

final_prompt = prompt.format(things="countries that play cricket in world cup")
print(final_prompt)
```

The constructed `final_prompt` will look like:

```text theme={null}
List 3 countries that play cricket in world cup.
Your response should be a list of comma separated values, eg: `foo, bar, baz`
```

<Callout icon="lightbulb">
  Tip: Using `partial_variables` lets you add dynamic instructions (like format hints) without changing the main prompt template every time.
</Callout>

## 5. Invoke the model with the parser-aware prompt and parse the output

Now the model is instructed to return CSV-style text. After receiving the text, feed it to `output_parser.parse()` to get a Python list.

```python theme={null}
output = llm.invoke(input=final_prompt)
print(output.strip())       # e.g., "India, Australia, England"
print(type(output))         # <class 'str'>

things = output_parser.parse(output)
print(things)               # ['India', 'Australia', 'England']
print(type(things))         # <class 'list'>
print(things[0])            # 'India'
```

Example console outputs:

```text theme={null}
India, Australia, England
<class 'str'>
['India', 'Australia', 'England']
<class 'list'>
India
```

## Summary

* Append parser `format_instructions` to your prompt to guide the model toward a predictable output format (CSV in this example).
* Use `CommaSeparatedListOutputParser` to transform the returned string into a native Python `list`.
* This pattern reduces brittle string processing and improves data reliability when integrating LLM responses into applications.

## Quick reference table

| Component                        | Purpose                                           | Example                                                                   |
| -------------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------- |
| `PromptTemplate`                 | Reusable prompt structure with variables          | `PromptTemplate(template="List 3 {things}.\n{format_instructions}", ...)` |
| `OpenAI()`                       | LLM client / runtime                              | `llm = OpenAI()`                                                          |
| `CommaSeparatedListOutputParser` | Instructs and parses CSV-like outputs into `list` | `things = output_parser.parse(output)`                                    |

## Next steps

* Try other output parsers (for example, JSON-specific parsers) if you need objects/dictionaries directly from the model.
* Combine parser format instructions with few-shot examples when you need stronger conditioning.
* Validate parsed outputs before using them in production systems to handle cases where the model doesn't follow instructions exactly.

## Links and references

* [LangChain: PromptTemplate](https://langchain.readthedocs.io/)
* [OpenAI API documentation](https://platform.openai.com/docs)

<Callout icon="warning">
  LLMs may sometimes ignore formatting instructions. Always validate parser output and add fallback handling for unexpected formats.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/ae260750-791b-496c-991f-0d0333f61e40/lesson/1d5a8e19-7bfd-497d-8e3e-8ffd23c70eb3" />
</CardGroup>
