# Define the target schema
class Person(BaseModel):
    name: str
    age: int
    email: str

# Create a Pydantic output parser
parser = PydanticOutputParser(pydantic_object=Person)
format_instructions = parser.get_format_instructions()

# Build a prompt that includes the parser's format instructions
prompt = PromptTemplate(
    input_variables=["text", "format_instructions"],
    template="Extract the person's information from the following text. Respond only in JSON that follows the schema exactly.\n\n{format_instructions}\n\nText:\n{text}"
)

# Prepare the LLM chain and run it
llm = ChatOpenAI(temperature=0)
chain = LLMChain(llm=llm, prompt=prompt)

raw_output = chain.run({"text": "Alice, 30, alice@example.com", "format_instructions": format_instructions})
# Parse the model output into a Pydantic model instance
person = parser.parse(raw_output)

print(person)          # Person(name='Alice', age=30, email='alice@example.com')
print(person.dict())   # {'name': 'Alice', 'age': 30, 'email': 'alice@example.com'}
```

Best practices when using output parsers

* Include the parser’s format instructions in the prompt so the LLM knows the expected structure.
* Always validate and handle parsing errors—models can still produce malformed or extra text.
* Use temperature 0 (or low values) for more deterministic outputs when format strictness matters.
* Consider tolerant post-processing strategies (strip extra commentary, repair minor JSON issues) when the model frequently deviates.
* Log raw model outputs and parsing errors to help iterate on prompt wording and parser configuration.

<Callout icon="lightbulb">
  Always validate model outputs before using them in production. Even with strict format instructions, the model may produce additional text or malformed structures—handle parsing errors and sanitize input for downstream systems.
</Callout>

Further reading and references

* LangChain documentation and output parser utilities: [https://learn.kodekloud.com/user/courses/langchain](https://learn.kodekloud.com/user/courses/langchain)
* Pydantic: [https://pydantic-docs.helpmanual.io/](https://pydantic-docs.helpmanual.io/)
* Best practices for prompt engineering: [https://www.prompting.guide/](https://www.prompting.guide/)

These resources show alternative output parsers and transformation strategies you can use to safely and reliably consume model outputs across different languages and runtime environments.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/ae260750-791b-496c-991f-0d0333f61e40/lesson/ee38bab1-8189-4ab1-8b0e-8933a1ca8ab0" />
</CardGroup>


# Prompt Templates Demo

Source: https://notes.kodekloud.com/docs/LangChain/Interacting-with-LLMs/Prompt-Templates-Demo/page

Guide to building and using LangChain chat prompt templates, populating them at runtime, and invoking ChatOpenAI to generate assistant responses, with examples and best practices.

This lesson demonstrates how to convert message patterns into reusable prompt templates and then create concrete prompts to send to a chat model using LangChain. The example below walks through the essential steps in order: imports, defining message templates, building a chat prompt template, populating it at runtime, invoking a chat model, and reading the model response.

<Callout icon="lightbulb">
  Before running the examples, ensure your OpenAI API key is set in the environment, for example:
  `export OPENAI_API_KEY="sk-..."`. See [Introduction to OpenAI](https://learn.kodekloud.com/user/courses/introduction-to-openai) for details and safe handling of secrets.
</Callout>

## Overview

* Build modular message templates (system/human).
* Combine them into a `ChatPromptTemplate`.
* Populate templates at runtime using `format_messages`.
* Send the formatted messages to a chat model (e.g., `ChatOpenAI`) and extract the assistant response.
* Optionally extend with few-shot examples, output parsing, or post-processing steps.

## Quick reference: core classes

| Class / helper                | Purpose                                                   | Example                                               |
| ----------------------------- | --------------------------------------------------------- | ----------------------------------------------------- |
| `ChatOpenAI`                  | Chat model wrapper — handles calling the model            | `model = ChatOpenAI()`                                |
| `ChatPromptTemplate`          | Holds a sequence of message templates and input variables | `ChatPromptTemplate.from_messages([...])`             |
| `SystemMessagePromptTemplate` | Template for system-level instructions (e.g., role)       | `SystemMessagePromptTemplate.from_template(sys_msg)`  |
| `HumanMessagePromptTemplate`  | Template for user/human messages                          | `HumanMessagePromptTemplate.from_template(human_msg)` |

## 1. Imports

Import the LangChain chat model and prompt template helpers:

```python theme={null}
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import os
```

## 2. Define message templates

Define your system and human message templates with placeholders for runtime variables. These templates describe the pattern of messages but do not include concrete values yet.

```python theme={null}
sys_msg = "You are a {subject} teacher"
human_msg = "Tell me about {concept}"
```

These define two reusable patterns:

* System template: instructs the assistant's role and behavior.
* Human template: expresses the user query with a placeholder.

## 3. Create a ChatPromptTemplate from message templates

Combine the message templates into a structured prompt template using `ChatPromptTemplate.from_messages`. Create message template objects from the raw templates, then pass them to `from_messages`:

```python theme={null}
prompt_template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(sys_msg),
        HumanMessagePromptTemplate.from_template(human_msg),
    ]
)
```

If you inspect `prompt_template`, it describes its input variables and the underlying message templates. Example representation (console output):

```text theme={null}
