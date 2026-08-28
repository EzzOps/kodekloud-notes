# LCEL Demo 1

Source: https://notes.kodekloud.com/docs/LangChain/Introduction-to-LCEL/LCEL-Demo-1/page

Tutorial demonstrating a minimal LangChain LCEL chain composing a prompt, ChatOpenAI LLM, and StrOutputParser via pipe operator and inspecting input and output schemas.

This tutorial walks through a minimal LCEL (LangChain Core Execution Language) chain: a prompt -> ChatOpenAI LLM -> `StrOutputParser`. It demonstrates composing components with the `|` operator, invoking the chain, and inspecting input/output schemas. This is the canonical "hello world" of LCEL: simple, composable, and directly readable.

Quick links:

* LangChain Core docs: [https://python.langchain.com/en/latest/](https://python.langchain.com/en/latest/)
* LangChain OpenAI integration: [https://python.langchain.com/en/latest/modules/llms/integrations/openai.html](https://python.langchain.com/en/latest/modules/llms/integrations/openai.html)

## 1 — Import components and define prompt, LLM, and output parser

First, import the required pieces and create the prompt template, the ChatOpenAI LLM instance, and the `StrOutputParser` that converts model output to a plain Python string.

```python theme={null}
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant.
Answer the following question: {question}
""")

llm = ChatOpenAI()
output_parser = StrOutputParser()
```

## 2 — Compose the LCEL chain

Use the `|` (pipe) operator to connect components. Outputs are automatically mapped to the next component's inputs at runtime:

```python theme={null}
chain = prompt | llm | output_parser
```

This composition means:

* The prompt component produces data keyed by the prompt's output schema.
* The LLM component consumes that data (messages/metadata) and produces a chat-style output.
* The output parser consumes the LLM output and returns a final Python value (here, a `str`).

## 3 — Invoke the chain

Call the chain's `invoke` method with the prompt input fields. In this prompt, the placeholder key is `question`:

```python theme={null}
result = chain.invoke({"question": "Tell me about The Godfather movie"})
print(result)
```

Example console output (model wording will vary):

```text theme={null}
"The Godfather" is a classic crime film directed by Francis Ford Coppola and released in 1972. It is based on the novel of the same name by Mario Puzo and follows the story of the powerful Italian-American crime family, the Corleones. The film stars Marlon Brando as the patriarch Vito Corleone and Al Pacino as his youngest son, Michael Corleone, who becomes increasingly involved in the family's criminal activities.

The Godfather is widely regarded as one of the greatest films in cinematic history, known for its iconic performances, memorable quotes, and intricate storytelling. It won multiple Academy Awards, including Best Picture, and has had a significant impact on popular culture.
```

<Callout icon="lightbulb">
  `StrOutputParser` simply returns the LLM response as a plain Python string.
</Callout>

## 4 — Inspecting input and output schemas

Every LCEL component exposes an `input_schema` and `output_schema`. This makes composition safe and transparent: LangChain Core maps outputs to the next component’s inputs automatically, so you can focus on composing components instead of manually transforming data.

To view the chain-level schemas:

```python theme={null}
print(chain.input_schema.schema())
print(chain.output_schema.schema())
```

Example JSON for the chain input schema:

```json theme={null}
{
  "title": "PromptInput",
  "type": "object",
  "properties": {
    "question": {
      "title": "Question",
      "type": "string"
    }
  }
}
```

Example JSON for the chain output schema:

```json theme={null}
{
  "title": "StrOutputParserOutput",
  "type": "string"
}
```

To inspect the LLM's richer schemas (inputs accept messages, metadata, and kwargs; outputs follow a chat-style structure):

```python theme={null}
print(llm.input_schema.schema())
print(llm.output_schema.schema())
```

Truncated example JSON for the LLM input schema:

```json theme={null}
{
  "description": "Message from an AI.",
  "type": "object",
  "properties": {
    "content": {
      "title": "Content",
      "anyOf": [
        { "type": "string" },
        { "type": "object" }
      ]
    },
    "additional_kwargs": {
      "title": "Additional Kwargs",
      "type": "object"
    },
    "type": {
      "title": "Type",
      "default": "ai",
      "enum": ["ai"],
      "type": "string"
    },
    "name": { "title": "Name", "type": "string" },
    "id": { "title": "Id", "type": "string" },
    "example": { "title": "Example", "default": false, "type": "boolean" }
  },
  "required": ["content"]
}
```

Truncated example JSON for the LLM output schema:

```json theme={null}
{
  "title": "ChatOpenAIOutput",
  "anyOf": [
    { "$ref": "#/definitions/AIMessage" },
    { "$ref": "#/definitions/HumanMessage" },
    { "$ref": "#/definitions/ChatMessage" },
    { "$ref": "#/definitions/SystemMessage" },
    { "$ref": "#/definitions/FunctionMessage" },
    { "$ref": "#/definitions/ToolMessage" }
  ],
  "definitions": {
    "AIMessage": {
      "title": "AIMessage",
      "description": "Message from an AI.",
      "type": "object",
      "properties": {
        "content": {
          "title": "Content",
          "anyOf": [
            { "type": "string" },
            {
              "type": "array",
              "items": {
                "anyOf": [{ "type": "string" }, { "type": "object" }]
              }
            }
          ]
        },
        "additional_kwargs": { "title": "Additional Kwargs", "type": "object" },
        "type": { "title": "Type", "default": "ai", "enum": ["ai"], "type": "string" },
        "name": { "title": "Name", "type": "string" },
        "id": { "title": "Id", "type": "string" }
      },
      "required": ["content"]
    },
    "HumanMessage": {
      "title": "HumanMessage",
      "description": "Message from a human.",
      "type": "object"
    }
  }
}
```

## 5 — Component summary

| Component                       | Purpose                                                   | Example                                                  |
| ------------------------------- | --------------------------------------------------------- | -------------------------------------------------------- |
| Prompt (ChatPromptTemplate)     | Produces structured prompt output for the LLM             | `ChatPromptTemplate.from_template("Answer: {question}")` |
| LLM (ChatOpenAI)                | Consumes prompt messages and returns chat-style responses | `ChatOpenAI()`                                           |
| Output parser (StrOutputParser) | Converts LLM output to a final Python value (here: `str`) | `StrOutputParser()`                                      |

## 6 — Key takeaway and next steps

* Each LCEL component defines explicit `input_schema` and `output_schema`. The `|` operator composes components and LangChain Core maps data between them automatically.
* This pattern removes boilerplate transformation code and encourages building small, reusable components.

Next steps:

* Try implementing a custom LCEL component that follows the LCEL interface so it can be piped into chains just like built-ins.
* Explore `RunnablePassthrough` as a foundational example of a simple, composable component.

Further reading:

* LangChain Core docs: [https://python.langchain.com/en/latest/](https://python.langchain.com/en/latest/)
* LLM integration (OpenAI) docs: [https://python.langchain.com/en/latest/modules/llms/integrations/openai.html](https://python.langchain.com/en/latest/modules/llms/integrations/openai.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/754457c5-1386-422b-98ad-3342dfc6aab3/lesson/add69dd3-2805-44d2-b67f-5198effe7e2b" />
</CardGroup>
