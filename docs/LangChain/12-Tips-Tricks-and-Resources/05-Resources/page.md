# Resources

Source: https://notes.kodekloud.com/docs/LangChain/Tips-Tricks-and-Resources/Resources/page

Overview of LangChain resources, documentation, setup tips, integrations, and examples for building chains, agents, embeddings, and retrieval-based applications

Before continuing, a brief disclaimer and a pointer to useful resources.

LangChain evolves quickly — think of it as a framework, a platform, or a library — and releases appear frequently. This lesson/article is based on LangChain 0.1.11 (and is compatible with 0.1.10). To avoid surprises, run the same LangChain version as used in this material so the notebooks and examples behave as shown.

> **lightbulb** Keep your LangChain installation aligned with the course version (0.1.10–0.1.11) to avoid API mismatches. If you run into issues, check the LangChain docs ([https://python.langchain.com/en/latest/](https://python.langchain.com/en/latest/)) or release notes ([https://github.com/langchain-ai/langchain/releases](https://github.com/langchain-ai/langchain/releases)) for the changes.

<Frame>
  <img alt="The image shows a LangChain logo with icons labeled &#x22;Framework,&#x22; &#x22;Platform,&#x22; and &#x22;Library.&#x22; It also includes the word &#x22;Disclaimer&#x22; in the top left corner." />
</Frame>

Quick setup tip: set your LLM provider API key in the environment before running examples. For interactive Python sessions, this pattern avoids persisting secrets in files or notebooks:

```python theme={null}
from getpass import getpass
import os

OPENAI_API_KEY = getpass("Enter your OpenAI API key: ")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
```

You can also use vendor-specific Python SDKs and follow the LangChain blog ([https://blog.langchain.dev](https://blog.langchain.dev)) to learn about new launches and integrations.

<Frame>
  <img alt="The image shows two webpage screenshots: one is Oracle Cloud Infrastructure documentation for the Python SDK, and the other is a LangChain blog about an open source extraction service." />
</Frame>

Primary documentation and the project website are the most authoritative references. Spend time navigating the docs to understand the library structure — it will save you effort when building chains, agents, or retrieval-based apps.

<Frame>
  <img alt="The image shows a webpage from LangChain, displaying sections for &#x22;LangChain-Community&#x22; and &#x22;LangChain-Core&#x22; with different components like Model I/O, Retrieval, and Agent Tooling. It's part of a documentation interface with navigation menus on the left and right." />
</Frame>

The docs map directly to LangChain’s main concepts: model I/O, prompt engineering, chat models, output parsers, retrieval, agents, chains, memory, and more. Each section includes examples and API references to help you move from concept to working code.

<Frame>
  <img alt="The image shows a webpage from LangChain about &#x22;Model I/O,&#x22; featuring a flowchart that explains the model input/output process, and a menu with various modules and guides." />
</Frame>

Several newer components—such as LangServe, LangSmith, and LangGraph—are evolving rapidly and may be out of scope for core examples here. You can still explore them or request early access if they match your project needs.

LangChain provides many third-party integrations. The docs include a matrix showing which providers support features like invoke, async invoke, streaming, and batch operations—handy when choosing a provider for production workloads.

<Frame>
  <img alt="The image shows a webpage from LangChain featuring a comparison table of various LLM integrations and their supported features, such as invoke, async invoke, stream, and batch. Each row lists a different model with check marks and crosses indicating the availability of each feature." />
</Frame>

Embeddings convert text to vectors for retrieval and similarity search. LangChain supports many embedding providers; consult the embeddings section of the docs to compare quality, performance, and cost trade-offs.

<Frame>
  <img alt="This image shows a webpage from LangChain's documentation site, highlighting various embedding model integrations with options like &#x22;Google Generative AI Embeddings&#x22; and &#x22;GPT4All&#x22; among others. The navigation menu is visible on the left." />
</Frame>

Vector stores (vector databases) are widely supported via integrations. Check Integrations -> Components in the docs to find your preferred vendor.

The API reference shows available classes and usage patterns. For example, the agents section documents how an agent chooses actions and details the class structure and available agent types.

<Frame>
  <img alt="The image displays a webpage from LangChain documentation, specifically the section about langchain.agents. It describes the role of agents in choosing a sequence of actions using a language model, and includes class hierarchy information." />
</Frame>

Many implementations live under `langchain` core and `langchain_community`. For example, OpenAI chat support is provided through the community package and builds on the core LLM abstractions:

```python theme={null}
from langchain_community.llms.openai import OpenAIChat

openai_chat = OpenAIChat(model_name="gpt-3.5-turbo")
```

Chains are a central abstraction. An `LLMChain` ties an LLM to a prompt template so you can encapsulate reusable steps cleanly.

<Frame>
  <img alt="The image shows a webpage displaying the LangChain documentation, focusing on chains and classes within the library. It lists various classes related to API and document handling, along with brief descriptions for each." />
</Frame>

Minimal LLMChain example (prompt template + OpenAI chat):

```python theme={null}
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms.openai import OpenAIChat

prompt = PromptTemplate(
    input_variables=["adjective"],
    template="Tell me a {adjective} joke"
)

llm = OpenAIChat(model_name="gpt-3.5-turbo")
chain = LLMChain(llm=llm, prompt=prompt)
