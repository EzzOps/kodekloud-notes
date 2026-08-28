# Call the LLM (returns a string)
raw_output = llm(prompt.format(continent="Asia"))
print(raw_output)
```

Example typical output:

```plaintext theme={null}
1. Japan - Tokyo
2. China - Beijing
3. India - New Delhi
```

This output is human-readable but not structured. To work with it programmatically, we need to guide the model to emit JSON.

## 2) Add a JsonOutputParser and obtain format instructions

Instantiate a `JsonOutputParser` to provide the LLM with exact format instructions. The parser exposes a helper string you can embed in your prompt to ask for valid JSON:

```python theme={null}
output_parser = JsonOutputParser()
format_instructions = output_parser.get_format_instructions()
print(format_instructions)
```

The printed `format_instructions` will be a short guideline such as "Return a JSON object." Use this text so the model knows to produce valid, parseable JSON.

## 3) Create a prompt that includes the format instructions

Embed the parser's instructions into your prompt using `partial_variables`. This ensures every invocation contains the necessary instructions for structured output:

```python theme={null}
prompt = PromptTemplate(
    template="List 3 countries in {continent} and their capitals\n{format_instructions}",
    input_variables=["continent"],
    partial_variables={"format_instructions": format_instructions},
)
```

Inspect the prompt to confirm the instructions are included:

```python theme={null}
print(prompt.format(continent="North America"))
```

Example rendered prompt:

```plaintext theme={null}
List 3 countries in North America and their capitals
Return a JSON object.
```

## 4) Invoke the LLM with the structured prompt and parse the result

Call the model with the new prompt and then parse the returned JSON string into native Python types:

```python theme={null}
response = llm(prompt.format(continent="North America"))
print(response)
```

Example model output (valid JSON):

```json theme={null}
{
  "USA": "Washington D.C.",
  "Canada": "Ottawa",
  "Mexico": "Mexico City"
}
```

Now parse the JSON string into Python:

```python theme={null}
countries = output_parser.parse(response)  # Parses string -> Python dict/list depending on JSON
print(type(countries))   # -> <class 'dict'>
print(json.dumps(countries))  # Serializes back to a JSON string if needed
```

Example console output:

```plaintext theme={null}
<class 'dict'>
{"USA": "Washington D.C.", "Canada": "Ottawa", "Mexico": "Mexico City"}
```

## 5) Why this approach helps

* The parser's format instructions encourage the LLM to produce valid JSON (or another predictable format), reducing parsing errors.
* Passing the LLM response through `JsonOutputParser` converts a string into native Python types (dict, list), which eliminates manual parsing and validation plumbing.
* Once parsed, the result can be fed directly into application logic, converted into dataclasses, or serialized for storage/transmission.

## Quick reference: workflow steps

| Step | Purpose                   | Example/Command                                                                                                |
| ---- | ------------------------- | -------------------------------------------------------------------------------------------------------------- |
| 1    | Define prompt template    | `PromptTemplate(template="List 3 countries in {continent} and their capitals", input_variables=["continent"])` |
| 2    | Create LLM client         | `llm = OpenAI()`                                                                                               |
| 3    | Instantiate parser        | `output_parser = JsonOutputParser()`                                                                           |
| 4    | Embed format instructions | Use `format_instructions = output_parser.get_format_instructions()` and `partial_variables`                    |
| 5    | Call LLM and parse        | `response = llm(prompt.format(...))` then `countries = output_parser.parse(response)`                          |

## Links and further reading

* [LangChain: Output Parsers](https://langchain.readthedocs.io/en/latest/modules/output_parsers.html)
* [OpenAI Python client](https://platform.openai.com/docs/api-reference)

<Callout icon="lightbulb">
  Always include the parser's format instructions in the prompt when you want structured output; otherwise the model may return freeform text that fails to parse.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-791b-496c-991f-0d0333f61e40/lesson/0a72e0ca-6e2c-41db-b741-2a1763894c11" />
</CardGroup>


# Parsing Model Output Demo 3

Source: https://notes.kodekloud.com/docs/LangChain/Interacting-with-LLMs/Parsing-Model-Output-Demo-3/page

Explains using a Pydantic output parser to convert LLM responses into typed Python objects

In this lesson you'll learn how to use a Pydantic-based output parser to convert LLM responses into a typed Python object. Using Pydantic (via LangChain utilities), you declare a schema with Python type annotations and then validate/parse JSON-like model output into instances of that schema—giving you robust guarantees about structure and types when working with LLM-generated data.

Key concepts covered:

* Defining a Pydantic model for the expected response.
* Creating a `PydanticOutputParser`.
* Embedding parser format instructions in the prompt so the LLM returns JSON matching the schema.
* Invoking the model and parsing the output into a typed Python object.

## Complete example

Below is a concise, runnable example showing the full workflow: define a model, create a parser, add format instructions to the prompt, call the model, and parse the response.

```python theme={null}
