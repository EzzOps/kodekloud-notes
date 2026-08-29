# Choose your LLM provider
llm = ChatOpenAI(model_name="gpt-3.5-turbo")
# Alternative provider example:
# Memory for storing conversational history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Embeddings convert documents into vectors
embedding = OpenAIEmbeddings()

# Vector store that holds TechCorp documents (indexed using the embeddings)
db = Chroma(collection_name="techcorp_docs", embedding_function=embedding)

# Create a conversational retrieval chain that uses the LLM + vector DB + memory
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=db.as_retriever(),
    memory=memory
)

# Run a query through the chain
response = qa_chain.run("What is TechCorp's customer data policy?")
print(response)
```

> **lightbulb** Note: LangChain import locations and class names can change across releases. If an import fails, consult the LangChain docs for your installed version. Also ensure environment variables for provider API keys (e.g., OPENAI\_API\_KEY, ANTHROPIC\_API\_KEY) are set before running the code.

How the agent uses components

* LLM: natural-language reasoning and response generation.
* Embeddings: convert company documents into dense vectors for semantic indexing.
* Vector store / Retriever: performs semantic search over indexed documents and returns relevant context to the agent.
* Memory: holds recent chat history so replies are context-aware and coherent across turns.
* Tools: allow the agent to call external APIs or perform actions (customer DB lookups, ticket creation, web searches).

This modularity makes extending the agent straightforward: add new tools, swap the LLM provider, or change the vectorstore with minimal code changes.

> **warning** Warning: Avoid sending sensitive PII or confidential documents to third-party LLMs unless you have contracts and controls in place. Review your data privacy, retention, and compliance requirements before indexing private documents or integrating internal systems.

Conclusion and next steps

Using LangChain speeds up building production-ready conversational agents by providing tested building blocks for common integration tasks: RAG (retrieval-augmented generation), memory management, tool invocation, and multi-provider support. Start by:

1. Defining your data sources (documents, databases, support tickets).
2. Choosing an embedding provider and vector store (Chroma, Pinecone).
3. Wiring a conversational chain with memory and a retriever.
4. Adding tools for any external actions your agent must perform.

Links and references

* [LangChain — learn.kodekloud course](https://learn.kodekloud.com/user/courses/langchain)
* [OpenAI Docs](https://platform.openai.com/docs)
* Chroma: [https://www.trychroma.com/](https://www.trychroma.com/)
* Pinecone: [https://www.pinecone.io/](https://www.pinecone.io/)
* Retrieval-augmented generation (RAG) overview: [https://en.wikipedia.org/wiki/Retrieval-augmented\_generation](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)

Now that you’ve seen the conceptual elements and a practical snippet, you should have a clear idea of how LangChain brings together LLMs, embeddings, vector stores, memory, and tool integration to build reliable conversational agents.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-agents-fundamentals/module/dd5e8998-51f1-4352-82a5-3414cdc3299c/lesson/7fedd787-d1f6-4448-8498-933540462873)


# Introduction to AI Agents

Source: https://notes.kodekloud.com/docs/AI-Agents-Fundamentals/AI-Agents-Part-1/Introduction-to-AI-Agents/page

Hands-on overview of AI agents and related technologies including tokens, embeddings, RAG, vector databases, orchestration libraries, MCPs, and practical end-to-end project for building robust AI applications.

AI has advanced rapidly over the past few years. Today’s practical toolkit for building intelligent applications includes concepts and technologies such as prompt engineering, context windows, tokens, embeddings, Retrieval-Augmented Generation (RAG), vector databases, Model Context Protocols (MCPs), orchestration libraries like LangChain and LangGraph, and AI agents. This lesson gives a concise, hands-on overview so you can understand how these pieces fit together and start building right away.

> **lightbulb** This lesson assumes no prior knowledge. It’s structured around a single, practical project that integrates fundamental AI concepts (tokens, embeddings, context windows, prompt design) with retrieval and orchestration (RAG, vector databases, LangChain/LangGraph, MCPs, and agents).

We’ll cover these topics and why they matter:

| Topic                                  | What it is                                                                              | Why it matters                                                                         |
| -------------------------------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Tokens, context windows, prompt design | The basic units and limits for language model input and strategies for guiding behavior | Impacts cost, capability, and response quality                                         |
| Embeddings                             | Numerical vectors that represent text semantics                                         | Enables semantic search and similarity-based retrieval                                 |
| Retrieval-Augmented Generation (RAG)   | Combining retrieval from a knowledge store with generation by a model                   | Improves factual accuracy and relevance for LLM outputs                                |
| Vector databases                       | Storage and indexing systems for embeddings                                             | Fast, scalable similarity search for RAG pipelines                                     |
| LangChain / LangGraph                  | Orchestration libraries for composing models, prompts, and tools                        | Simplifies building complex, multi-step AI workflows (agents)                          |
| MCPs (Model Context Protocols)         | Conventions for how models share context and tools                                      | Helps agents coordinate model calls and external tools                                 |
| AI Agents                              | Systems that use models + tools to perform tasks autonomously                           | Enables multi-step, tool-enabled workflows like data lookups, API calls, and reasoning |

We’ll progress in a practical order:

1. Core AI fundamentals (tokens, embeddings, context windows, prompt design)
2. Retrieval-Augmented Generation and vector databases — how embeddings are stored and searched
3. Orchestration with LangChain and LangGraph, and how they help build agents
4. MCPs and agent coordination across models and tools
5. A single end-to-end project that ties these components together

Along the way you’ll see how each layer interacts with the others so you can design robust, production-ready AI applications that are both accurate and cost-effective. Useful references and deeper-dive resources are linked inline for each topic.

<Frame>
  <img alt="A chalkboard-style sketch showing a neural-network labeled &#x22;A.I.&#x22; with arrows to terms like embeddings, tokens, RAG, prompt engineering and a globe below, plus a small doodle of a person on the left." />
</Frame>

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-agents-fundamentals/module/dd5e8998-51f1-4352-82a5-3414cdc3299c/lesson/4db44634-7876-4871-b4a9-4bb6308728e0)
