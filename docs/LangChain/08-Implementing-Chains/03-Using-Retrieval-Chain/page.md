# Using Retrieval Chain

Source: https://notes.kodekloud.com/docs/LangChain/Implementing-Chains/Using-Retrieval-Chain/page

Guide to building a retrieval augmented generation pipeline using embeddings, FAISS vector store, and an LLM constrained to retrieved document context for accurate question answering

In this lesson we'll build a simple retrieval-augmented generation (RAG) pipeline that constrains a language model to answer using only retrieved documents. We'll use two TechCrunch articles as the source documents:

* "Anthropic claims its new models beat GPT-4" (March)
* "AI21 Labs' new text-generating AI model is more efficient than most" (March)

Workflow overview: load the articles from the web, split them into smaller chunks, create embeddings for those chunks, index them in an in-memory `FAISS` vector store, and then run a retrieval chain that supplies retrieved context to an LLM with instructions to answer only from that context.

Key benefits of this pattern:

* Keeps LLM input within the model context window.
* Reduces hallucination by restricting answers to retrieved text.
* Makes long-document QA, summarization, and fact-checking more reliable.

Below is a consolidated, corrected, and cleaned-up implementation that follows the same sequence as the original lesson.

```python theme={null}
