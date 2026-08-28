# LCEL Demo 2

Source: https://notes.kodekloud.com/docs/LangChain/Introduction-to-LCEL/LCEL-Demo-2/page

Demonstrates synchronous, streaming, and batch execution modes for LangChain-style chains with examples, usage guidelines, and best practices for invoke, stream, and batch workflows.

This lesson demonstrates three common ways to execute LangChain-style chains so you can choose the right execution mode for your application: synchronous invocation (`invoke`), token-level streaming (`stream`), and parallel/batch execution (`batch`). Each example composes a prompt template, a chat LLM, and a simple string output parser into a single chain.

## Synchronous execution (invoke)

Synchronous invocation runs the entire chain and returns the final output only after the LLM call completes. Use this for straightforward requests where you need the full response before proceeding. It's a blocking call that waits for the model to finish generating.

```python theme={null}
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template(
    """
You are a helpful assistant.
Answer the following question: {question}
"""
)

llm = ChatOpenAI()  # default non-streaming
output_parser = StrOutputParser()

chain = prompt | llm | output_parser
