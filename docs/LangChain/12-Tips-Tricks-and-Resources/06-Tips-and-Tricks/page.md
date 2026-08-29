# Run the chain
result = chain.run({"adjective": "funny"})
print(result)
```

The docs also provide conceptual guides and examples showing how LangChain supports context-aware, multi-step reasoning applications.

<Frame>
  <img alt="The image shows a webpage from the LangChain documentation, introducing the framework for developing applications powered by language models. It highlights features such as context-awareness and reasoning, and lists components like LangChain Libraries and LangServe." />
</Frame>

Below is a compact table of recommended links and resources to bookmark while working with LangChain:

| Resource                |                                      Purpose | Link                                                                                                     |
| ----------------------- | -------------------------------------------: | -------------------------------------------------------------------------------------------------------- |
| LangChain Documentation | Official API reference, guides, and examples | [https://python.langchain.com/en/latest/](https://python.langchain.com/en/latest/)                       |
| LangChain Blog          |     Releases, how-tos, and community updates | [https://blog.langchain.dev](https://blog.langchain.dev)                                                 |
| LangChain Releases      |              Changelogs and breaking changes | [https://github.com/langchain-ai/langchain/releases](https://github.com/langchain-ai/langchain/releases) |
| LLM Providers           |          Vendor SDKs and docs (e.g., OpenAI) | [https://openai.com](https://openai.com)                                                                 |
| Vector DBs & Embeddings |  Compare supported integrations and features | See Integrations -> Components in LangChain docs                                                         |

<Callout icon="lightbulb">
  Subscribe to the LangChain blog and monitor release notes. Changelogs help you track new features, provider integrations, and potential breaking changes that affect your code.
</Callout>

The goal of this section is to point you to authoritative resources and give practical tips for keeping your environment compatible with the course examples. When you encounter new terms or behaviors later in the material, return to these docs for the definitive explanation.

That concludes this section on tips, tricks, and resources. The next section introduces LCEL, the LangChain Expression Language.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/b5f7771a-fdbc-45b1-a786-6c84bb7ffc76/lesson/376f67ca-6dca-40d9-9d3a-830470975c42" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/langchain/module/b5f7771a-fdbc-45b1-a786-6c84bb7ffc76/lesson/eaabef57-b4d7-4497-aa1d-3bc1724723f4" />
</CardGroup>


# Tips and Tricks

Source: https://notes.kodekloud.com/docs/LangChain/Tips-Tricks-and-Resources/Tips-and-Tricks/page

Practical tips to add observability and debug LangChain apps using verbose logging, custom callbacks, and intermediate capture patterns to trace prompts, outputs, agents, and parsers.

Assuming familiarity with the core LangChain libraries, this article presents practical tips and techniques to debug LangChain applications and gain visibility into their runtime behavior.

LangChain can feel overwhelming at first—many parts of a chain (prompts, LLMs, output parsers, and agents) execute behind the scenes. When formatting is incorrect or responses are unexpected, you need tools that reveal the execution lifecycle so you can diagnose and fix issues quickly.

In this article you'll learn:

* How to enable built-in debug and verbose flags to surface internal information during execution.
* How to use callbacks to intercept and inspect events across prompts, LLM calls, chains, and agents.
* Practical patterns to capture intermediate inputs and outputs so you can trace where formatting or logic errors originate.

<Callout icon="lightbulb">
  This article focuses on techniques for observability and debugging. A demo in this article shows how to enable debug/verbose output and how to implement callbacks to capture detailed runtime information.
</Callout>

## Why observability matters for LangChain

When a chain produces unexpected results, the root cause can be in any layer:

* prompt formatting or template errors,
* LLM call parameters (temperature, max tokens),
* output parser logic (parsing failures),
* agent/tool execution and tool return values.

Observability helps you answer targeted questions such as:

* What prompt was actually sent to the LLM?
* What intermediate outputs did a chain produce before the final result?
* Which tools did an agent call and with what arguments?
* Did an output parser throw an error or silently return None?

Below are concrete techniques and examples you can adopt to make these answers visible.

## Summary of techniques

| Technique                     | Use case                                                            | Quick example                                                       |
| ----------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Verbose flags / logging       | Surface internal operations of LLMs and chains                      | `llm = ChatOpenAI(temperature=0, verbose=True)`                     |
| Callback handlers             | Intercept events across LLM calls, chains, agents, and tools        | Implement `BaseCallbackHandler` methods to capture lifecycle events |
| Intermediate capture patterns | Save intermediate inputs/outputs to debug parsing/formatting issues | Store inputs/outputs in memory, files, or a DB for review           |
| Structured tracing            | Combine verbose + callbacks for full traceable execution logs       | Use both `verbose=True` and a custom callback handler               |

## Enable verbose/debug output

Many LangChain classes expose a `verbose` flag that prints helpful information to stdout during execution. You can enable verbose on the LLM, chains, and some high-level components.

Python (Chat models and chains)

```python theme={null}
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain, PromptTemplate

template = "Summarize the following:\n\n{content}"
prompt = PromptTemplate(input_variables=["content"], template=template)

llm = ChatOpenAI(temperature=0.0, verbose=True)  # enable verbose on the LLM
chain = LLMChain(llm=llm, prompt=prompt, verbose=True)  # enable verbose on the chain

result = chain.run({"content": "LangChain is used for prompt orchestration..."})
print(result)
```

JavaScript / TypeScript (chat models and chains)

```javascript theme={null}
import { ChatOpenAI } from "langchain/chat_models";
import { LLMChain } from "langchain/chains";
import { PromptTemplate } from "langchain/prompts";

const prompt = new PromptTemplate({ inputVariables: ["content"], template: "Summarize:\n{content}" });
const llm = new ChatOpenAI({ temperature: 0, verbose: true });
const chain = new LLMChain({ llm, prompt, verbose: true });

const result = await chain.run({ content: "LangChain helps you build LLM-powered apps." });
console.log(result);
```

Tip: enabling verbose will print prompts and responses to stdout. If you have sensitive input (API keys, personal data), avoid printing them or sanitize logs.

<Callout icon="warning">
  Be careful when enabling verbose debug logging in production. Verbose logs may include user data, prompts, or model outputs that are sensitive. Always sanitize or disable verbose output for production environments.
</Callout>

## Callbacks — capture lifecycle events

Callbacks are the most flexible way to intercept runtime events. With a custom callback handler you can capture:

* prompt text before sending to the LLM
* LLM outputs and timings
* chain inputs/outputs at each step
* agent decisions and tool calls
* parser errors and exceptions

Below are minimal, robust examples that store events in memory (easy to extend to file, DB, or observability platforms).

Python — custom callback handler

```python theme={null}
from langchain.callbacks.base import BaseCallbackHandler
from typing import Any, Dict, List

class RecordingCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self.events: List[Dict[str, Any]] = []

    # called when a chain starts
    def on_chain_start(self, serialized, inputs, **kwargs):
        self.events.append({"type": "chain_start", "serialized": serialized, "inputs": inputs})

    # called when a chain ends
    def on_chain_end(self, outputs, **kwargs):
        self.events.append({"type": "chain_end", "outputs": outputs})

    # called when the LLM starts; receives prompts
    def on_llm_start(self, serialized, prompts, **kwargs):
        self.events.append({"type": "llm_start", "serialized": serialized, "prompts": prompts})

    # called when the LLM finishes
    def on_llm_end(self, response, **kwargs):
        self.events.append({"type": "llm_end", "response": response})

    # called on errors
    def on_tool_error(self, error, **kwargs):
        self.events.append({"type": "tool_error", "error": str(error)})
```

Register the handler with a chain or LLM:

```python theme={null}
from langchain.callbacks.manager import CallbackManager
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain, PromptTemplate

handler = RecordingCallbackHandler()
manager = CallbackManager([handler])

llm = ChatOpenAI(temperature=0.0, verbose=False, callback_manager=manager)
prompt = PromptTemplate(input_variables=["content"], template="Summarize:\n{content}")
chain = LLMChain(llm=llm, prompt=prompt, callback_manager=manager)

chain.run({"content": "Debugging LangChain step-by-step"})
