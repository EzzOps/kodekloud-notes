# imports
from typing import List

from langchain_openai import OpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

# initialize model
model = OpenAI()

# define the Pydantic model for a ticket reservation
class Ticket(BaseModel):
    date: str = Field(description="show date")
    time: str = Field(description="show time")
    theater: str = Field(description="theater name")
    count: int = Field(description="number of tickets")
    movie: str = Field(description="preferred movie")

# create the Pydantic output parser
parser = PydanticOutputParser(pydantic_object=Ticket)

# prompt template with placeholders for the movie query and parser format instructions
ticket_template = '''
Book us a movie ticket for two this Friday at 6:00 PM.
Choose any theater, it doesn't matter. Send the confirmation by email.
Our preferred movie is: {query}
Format instructions:
{format_instructions}
'''

prompt = PromptTemplate(
    template=ticket_template,
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
```

> **lightbulb** This example shows how the parser provides `format_instructions` (a JSON Schema-like specification). Including these instructions in your prompt guides the LLM to emit well-formed JSON that the parser can validate and load into a Pydantic model.

## Notes on imports and model invocation

Import paths and how you call the model can differ between LangChain versions and wrappers. Common variations:

* `from langchain import OpenAI` vs `from langchain_openai import OpenAI`
* `BaseModel` and `Field` may come directly from `pydantic`
* Model invocation can use `model.invoke(...)`, `model.predict(...)`, or `model(...)` depending on the wrapper

Be sure to consult your installed LangChain / OpenAI wrapper docs if you hit import or invocation errors.

## Build the final prompt

Supply a movie name (for example, `Interstellar`) and render the prompt. The `format_instructions` partial will contain the JSON Schema-like instructions the model should follow.

```python theme={null}
input = prompt.format_prompt(query="Interstellar")
print(input.to_string())
```

The embedded format instructions will look similar to this excerpt (JSON Schema-like):

```json theme={null}
{
  "properties": {
    "date": { "title": "Date", "description": "show date", "type": "string" },
    "time": { "title": "Time", "description": "show time", "type": "string" },
    "theater": { "title": "Theater", "description": "theater name", "type": "string" },
    "count": { "title": "Count", "description": "number of tickets", "type": "integer" },
    "movie": { "title": "Movie", "description": "preferred movie", "type": "string" }
  },
  "required": ["date", "time", "theater", "count", "movie"]
}
```

## Invoke the model and parse the response

Call the model with the formatted prompt string and capture the output:

```python theme={null}
output = model.invoke(input.to_string())
```

A typical LLM response (the exact wrapper text depends on the model) containing JSON might be:

```json theme={null}
{
  "date": "Friday",
  "time": "6:00 PM",
  "theater": "AMC",
  "count": 2,
  "movie": "Interstellar"
}
```

Pass the model output through the `PydanticOutputParser` to convert it into a typed `Ticket` instance:

```python theme={null}
reservation = parser.parse(output)
print(reservation)
print(type(reservation))
```

Example parser output:

```text theme={null}
Ticket(date='Friday', time='6:00 PM', theater='AMC', count=2, movie='Interstellar')
<class '__main__.Ticket'>
```

## Field reference

| Field     | Type      | Description       | Example        |
| --------- | --------- | ----------------- | -------------- |
| `date`    | `string`  | Show date         | `Friday`       |
| `time`    | `string`  | Show time         | `6:00 PM`      |
| `theater` | `string`  | Theater name      | `AMC`          |
| `count`   | `integer` | Number of tickets | `2`            |
| `movie`   | `string`  | Preferred movie   | `Interstellar` |

## Why this pattern is useful

* You get strong guarantees about the shape and types of the data your application receives from an LLM.
* Parsing into a Pydantic model makes downstream processing, validation, and IDE/autocomplete support straightforward.
* Embedding `parser.get_format_instructions()` in the prompt aligns the LLM output to the schema, reducing parsing errors.

> **lightbulb** The parser validates and converts JSON to an instance of the `Ticket` model. If the model's output does not conform to the schema, the parser will raise a validation error—so including `format_instructions` in the prompt is important to guide the LLM toward valid output.

## Summary

Steps to follow:

1. Define a Pydantic model (subclass of `BaseModel`) describing the expected fields and types.
2. Create a `PydanticOutputParser` using that Pydantic model.
3. Include `parser.get_format_instructions()` as a partial variable in your prompt template.
4. Invoke the LLM with the formatted prompt.
5. Use `parser.parse(...)` to convert the model output into a typed Python object.

This approach makes it straightforward to work with LLM-generated data in a type-safe way and reduces runtime errors caused by unexpected response formats.

## Links and references

* LangChain Output Parsers: [https://langchain.readthedocs.io/](https://langchain.readthedocs.io/)
* Pydantic: [https://pydantic-docs.helpmanual.io/](https://pydantic-docs.helpmanual.io/)
* OpenAI API / SDK docs: [https://platform.openai.com/docs](https://platform.openai.com/docs)

A future article will cover adding short-term and long-term memory to LLMs.

- [Watch Video](https://learn.kodekloud.com/user/courses/langchain/module/ae260750-791b-496c-991f-0d0333f61e40/lesson/31aecd1b-7ea9-4bab-898d-b8bc6b35ab62)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/langchain/module/ae260750-791b-496c-991f-0d0333f61e40/lesson/932a32b6-0fa6-445f-b1f6-7db4e21dc369)


# Parsing Model Output

Source: https://notes.kodekloud.com/docs/LangChain/Interacting-with-LLMs/Parsing-Model-Output/page

Explains converting LLM text into structured, validated data using format instructions and output parsers to produce typed objects like JSON, XML, YAML or Pydantic models for reliable integration.

This module covers model output handling—how to get structured, validated data back from large language models (LLMs). While earlier lessons focused on inputs and prompts, here we emphasize turning the LLM’s naturally textual output into reliable, typed data your application can consume: JSON, XML, YAML, CSV, or language-specific objects.

Large language models generate text by default. To integrate that text into production systems you typically:

1. Instruct the model, in the prompt, to produce a specific format (for example `JSON`, `XML`, `CSV`, or `YAML`), and provide a schema or examples.
2. Parse, validate, and transform the returned text into the target schema or runtime data structure (e.g., a Pydantic model, dataclass, or XML object).

<Frame>
  <img alt="The image is a diagram illustrating a process flow from a user to a language model, showing components labeled as input, model I/O, output, and &#x22;always text.&#x22;" />
</Frame>

Prompt instructions should be explicit: specify the exact format, provide a schema or examples, and include the machine-readable format instructions the parser generates. Even with strict instructions, models can and do deviate—extra commentary, stray punctuation, or slightly malformed JSON are common—so make parsing and validation part of your pipeline.

LangChain’s output parser utilities address both sides of this problem:

* They generate format instructions to include in your prompt, so the model knows the precise structure you expect.
* They offer parsers that convert the model’s textual output into typed objects (for example, Pydantic models), or into other markup languages (XML/YAML), making the output immediately consumable.

<Frame>
  <img alt="The image shows a comparison between an &#x22;Internal Python Data Structure&#x22; represented by the Python logo and &#x22;More Structured Markup&#x22; represented by icons for XML and YAML." />
</Frame>

This workflow is especially useful when you let an LLM do domain-specific extraction or transformation but need to integrate the results with other systems reliably.

Key steps summary:

* Add the parser’s format instructions to the prompt so the model returns data that matches the expected schema.
* Parse the returned text into a typed structure (e.g., a Pydantic model) to enforce types and validation.
* Handle parsing errors and edge cases gracefully—never assume a perfect output.

Recommended formats and typical use cases:

| Output Format             | When to Use                                                       | Example                             |
| ------------------------- | ----------------------------------------------------------------- | ----------------------------------- |
| JSON                      | Structured data exchanged between services or stored in databases | API responses, analytics events     |
| YAML                      | Human-editable configuration or templates                         | Config files, deployment manifests  |
| XML                       | Interoperability with legacy systems or specific schemas          | SOAP integrations, document formats |
| CSV                       | Tabular exports or simple ETL pipelines                           | Reports, data ingestion             |
| Language-specific objects | Direct use inside application code                                | `Pydantic` models, dataclasses      |

Below is a concise, practical example using LangChain’s `PydanticOutputParser`. It shows how to instruct the model to produce JSON matching a Pydantic schema, then parse that JSON into a typed Python object.

```python theme={null}
from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
