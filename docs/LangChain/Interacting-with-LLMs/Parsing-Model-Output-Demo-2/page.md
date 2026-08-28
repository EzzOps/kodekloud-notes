# Parsing Model Output Demo 2

Source: https://notes.kodekloud.com/docs/LangChain/Interacting-with-LLMs/Parsing-Model-Output-Demo-2/page

Demonstrates using LangChain to prompt an LLM to emit valid JSON via JsonOutputParser and parse model responses into native Python structures for reliable downstream use.

In this lesson we generate LLM output and reliably transform it into JSON using an output parser. You'll learn how to:

* Call a language model to list countries and capitals.
* Instruct the model to return valid JSON using a `JsonOutputParser`'s format instructions.
* Parse the LLM response into native Python data structures for direct use in application logic.

Quick links and references:

* [LangChain Documentation](https://langchain.readthedocs.io/)
* [OpenAI API](https://platform.openai.com/docs)

## 1) Imports and a simple LLM call

Start by importing the necessary components and creating an LLM client:

```python theme={null}
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.output_parsers import JsonOutputParser
import json

llm = OpenAI()
```

Construct a straightforward prompt template and call the model to get an unconstrained textual answer (a plain list):

```python theme={null}
prompt = PromptTemplate(
    template="List 3 countries in {continent} and their capitals",
    input_variables=["continent"],
)
