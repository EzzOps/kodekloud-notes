# Course Introduction

Source: https://notes.kodekloud.com/docs/AI-Agents-Fundamentals/Introduction/Course-Introduction/page

Hands-on course teaching semantic search, RAG, vector databases, and graph-based stateful AI agents with labs, code examples, and production deployment practices.

Welcome to the AI Agents Fundamentals course. AI-driven applications are transforming industries by enabling systems to reason, remember, and act — automating workflows and augmenting decision-making.

This lesson provides a hands-on path from your first API call to building production-quality, stateful AI agents. You’ll move from environment verification to implementing semantic search, Retrieval-Augmented Generation (RAG), and graph-based workflows that maintain memory and reasoning. Labs include runnable code examples so you can quickly move from theory to practical implementation.

What you’ll learn

* Make your first AI API call and understand modern model interactions.
* Build and deploy AI features using agent frameworks and prompt engineering best practices.
* Implement vector databases and a semantic search engine for technical documentation to retrieve by meaning rather than keywords.
* Combine retrieval and generation using Retrieval-Augmented Generation (RAG) for more accurate, context-aware outputs.
* Design stateful, graph-based workflows and agents that remember, reason, and react over time.
* Extend workflows with external tools, observability, and production-ready safety patterns.

Course modules summary

| Module                             | Focus                                              | Outcome                                           |
| ---------------------------------- | -------------------------------------------------- | ------------------------------------------------- |
| Environment & Setup                | Verify virtualenv and Python packages              | Run a verification script to confirm dependencies |
| Vector Search & Semantic Retrieval | sentence-transformers, Chroma/ChromaDB, embeddings | Build a semantic search index for docs            |
| RAG Pipelines                      | Retrieval + generation patterns                    | Create context-conditioned generation pipelines   |
| Graph-based Agents                 | StateGraph primitives, memory & reasoning          | Implement stateful agents that maintain context   |
| Advanced & Production              | Tool integrations, observability, safety           | Extend workflows for real-world deployment        |

First steps — verify your environment
Before you run labs, activate your virtual environment and ensure required packages are installed. Typical packages used in these labs include langchain, chromadb, sentence-transformers, numpy, and related dependencies.

Run this simple verification command after activating your venv:

```bash theme={null}
