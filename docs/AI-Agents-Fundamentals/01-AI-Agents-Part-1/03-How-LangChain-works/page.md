# How LangChain works

Source: https://notes.kodekloud.com/docs/AI-Agents-Fundamentals/AI-Agents-Part-1/How-LangChain-works/page

Explains how LangChain composes LLMs, embeddings, vector stores, memory, and tools to build retrieval augmented conversational agents and workflows for production chatbots

Now that we understand how LLMs and embeddings function, we need a system that ties those primitives together into a reliable, maintainable product.

TechCorp needs a chatbot that lets customers ask questions about company policy, product details, and support issues. The system must:

* Remember conversation history
* Access the company knowledge base (documents, FAQs, manuals)
* Handle complex multi-step interactions and take actions when needed

A naive implementation might call an LLM provider's SDK (for example, [OpenAI](https://learn.kodekloud.com/user/courses/introduction-to-openai)) for every user message. But that leaves several engineering gaps: storing chat messages, maintaining conversational context, performing semantic search over internal documents, routing calls to internal tools, and keeping the solution portable across providers (OpenAI → Anthropic → Google). What looks small quickly grows into a large integration project.

LangChain provides an abstraction layer that addresses these gaps with composable, standardized components and interfaces.

<Frame>
  <img alt="A hand-drawn architecture diagram of &#x22;Tech Corp's Chatbot&#x22; showing inputs like company policy, product info, and support issues routed through OpenAI's SDK and Langchain (abstraction layer) into conversation history, company knowledgebase, and multi-step interactions. A note at the bottom says &#x22;seems like a lot of work...&#x22;" />
</Frame>

Understanding LLM vs Agent

When you call a large language model (GPT, Claude, Gemini) directly, it acts as a static "brain" that generates answers from its training and prompt context. An agent, by contrast, augments that brain with autonomy, memory, and access to external tools — enabling it to decide which steps to take to satisfy a user request.

For TechCorp’s support scenario, consider the question: "What's your policy on refunds for a product that arrived damaged?" An agent might:

* Retrieve the relevant policy from the company knowledge base,
* Check prior conversation context to confirm whether the customer already provided an order number,
* Call an internal customer-database tool to validate purchase details,
* Open a support ticket if required — without you hard-coding an if/else flow for each step.

<Frame>
  <img alt="A hand-drawn diagram compares a static LLM (labeled GPT, Claude, Gemini) on the left with an agent-based system on the right that includes tools, memory, and autonomy. A sample user question about refunding a damaged product and an arrow to &#x22;software&#x22; are also shown." />
</Frame>

Why use LangChain?

LangChain exposes composable building blocks that map directly to the integration concerns above:

* Chat models: unified interfaces to LLM providers (OpenAI, Anthropic, Google). Switching providers often becomes a single-line change.
* Memory: session-aware memory components to store and retrieve conversation state without implementing a custom schema.
* Vector DB integration: standard adapters for vector databases (Chroma, Pinecone, etc.) so semantic search is consistent across providers.
* Embeddings: standardized embedding components to convert documents into vectors.
* Tools: easy definitions for external tool access (customer DB queries, web search, ticket creation), which agents can call when appropriate.

Without LangChain, you must implement API clients, connection management, storage layers, embedding pipelines, semantic search, memory systems, and tool routing yourself — complexity multiplies fast.

LangChain’s component library typically includes connectors and classes such as chat model wrappers, vectorstore adapters, embedding wrappers, memory classes for chat history, and a mechanism to define tools that agents can call. The agent orchestrates these components based on conversation context and system prompts.

LangChain components at a glance

| Component Type           | Purpose                                                  | Example                                         |
| ------------------------ | -------------------------------------------------------- | ----------------------------------------------- |
| Chat model               | Conversational LLM wrapper supporting multiple providers | `ChatOpenAI(model_name="gpt-3.5-turbo")`        |
| Memory                   | Stores session conversation history and state            | `ConversationBufferMemory`                      |
| Embeddings               | Converts text/documents to numeric vectors               | `OpenAIEmbeddings()`                            |
| Vector store / Retriever | Indexes vectors and supports semantic search             | `Chroma`, `Pinecone`                            |
| Chains / Agents          | Compose LLM, retriever, memory, and tools into workflows | `ConversationalRetrievalChain`                  |
| Tools                    | Integrations for external APIs and actions               | Customer DB query, web search, ticketing system |

Putting it together (example)

This concise example shows one way to wire a chat model, embeddings, vectorstore, memory, and a conversational retrieval chain — the core pattern for a retrieval-augmented chat agent. Import paths and class names can change between LangChain releases; check the documentation for your version.

```python theme={null}
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
