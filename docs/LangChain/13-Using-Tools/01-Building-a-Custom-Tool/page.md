# Building a Custom Tool

Source: https://notes.kodekloud.com/docs/LangChain/Using-Tools/Building-a-Custom-Tool/page

Explains building a LangChain custom tool that returns flight status, inspects tool metadata, and integrates the tool output into a prompt, LLM, and output parser chain

Now that we understand the concept of tools in LangChain, this lesson puts everything together by building a compact custom tool that returns flight status information. The example demonstrates:

* How to convert a Python function into a LangChain tool using the `@tool` decorator.
* How to inspect generated tool metadata (name, description, args).
* How to call the tool, use its output as context in a prompt, and run a prompt → LLM → output-parser chain.

The following concise, corrected example shows the end-to-end flow.

```python theme={null}
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_core.output_parsers import StrOutputParser

@tool
def GetFlightStatus(flight_no: str) -> str:
    """Gets flight status and schedule"""
    # In a real application you could invoke an external API here.
    return f"Flight {flight_no} departed at 5:20 PM. It is on-time and expected to arrive at 8:10 PM at Gate B."
