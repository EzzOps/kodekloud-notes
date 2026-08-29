# llm: an instantiated LLM
# prompt: your PromptTemplate or prompt string
stuff_chain = StuffDocumentsChain(llm=llm, prompt=prompt)

# documents: a list of langchain.schema.Document objects
result = stuff_chain.run(documents)
print(result)
```

Tips:

* Pre-filter documents if you cannot guarantee they will always fit.
* Use concise prompts and templates to reduce token usage.

## 2) Retrieval chain (RAG-style)

When your document collection is too large for a single prompt, use a retrieval-style chain. This pattern fetches relevant chunks from a retriever (vector DBs like FAISS, Chroma, Milvus, Pinecone, etc.), then combines the retrieved chunks into a prompt using a combiner (e.g., "stuff", "map\_reduce", "refine") before calling the LLM.

This is the common Retrieval-Augmented Generation (RAG) flow: retrieve → combine → generate.

When to use:

* Your corpus is large or contains long documents.
* You need better precision by narrowing context to the most relevant chunks.

Advantages:

* Scales to very large document collections.
* Focuses the LLM on relevant context, improving answer quality and reducing cost.
* Allows indexing, caching, and faster repeated queries.

Limitations:

* Requires an index and retriever infrastructure.
* Adds retrieval latency and tuning complexity (chunk size, embedding model, similarity metrics).

Typical pattern with LangChain’s RetrievalQA helper:

```python theme={null}
from langchain.chains import RetrievalQA

# llm: your LLM instance
# retriever: retriever from a vector store (e.g., faiss_retriever)
retrieval_qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",   # or "map_reduce", "refine" depending on your combine strategy
    retriever=retriever
)

answer = retrieval_qa.run("What is the summary of topic X?")
print(answer)
```

Additional notes:

* The `chain_type` selects the combiner strategy used after retrieval.
* For extremely long collections, `map_reduce` first summarizes chunks (map) then combines summaries (reduce).
* `refine` iteratively improves an initial answer using additional context.

## Compare chains: quick reference

| Chain Type              | Best for                                                | Key advantages                                     | Example usage                                               |
| ----------------------- | ------------------------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------- |
| `stuff`                 | Small collections or when all context fits in the model | Simple, single LLM call, deterministic             | `StuffDocumentsChain(llm=llm, prompt=prompt)`               |
| `retrieval` (RAG)       | Large collections, many documents, or long docs         | Scales, focuses on relevant chunks, more efficient | `RetrievalQA.from_chain_type(llm=llm, retriever=retriever)` |
| `map_reduce` (combiner) | Very large inputs where summarization per chunk helps   | Summarizes chunks first, reduces prompt size       | Use as `chain_type="map_reduce"` in RetrievalQA             |
| `refine` (combiner)     | When iterative improvement yields better quality        | Improves answers stepwise with more context        | Use as `chain_type="refine"` in RetrievalQA                 |

## Choosing the right combine strategy

Selecting a combiner depends on:

* Context window size of your LLM (e.g., 8k, 32k tokens).
* Document size and number of documents.
* Desired latency vs. quality trade-offs.

Guidelines:

* If total tokens \<\< context window: prefer `stuff` for simplicity.
* If documents are many or long: use a retrieval chain with `map_reduce` or `refine`.
* If you need higher accuracy and can afford extra calls, prefer `refine`.
* If you need the fastest throughput and context fits: `stuff` is usually best.

<Callout icon="lightbulb">
  Choosing the right combiner (e.g., `stuff`, `map_reduce`, `refine`) affects quality and cost: `stuff` is fast and simple, `map_reduce` reduces token usage by summarizing pieces first, and `refine` iteratively improves an answer and can yield higher-quality responses.
</Callout>

## Example end-to-end flow (retrieval + stuff)

1. Index documents into a vector store (FAISS, Chroma, etc.) with embeddings.
2. Create a retriever from the vector store.
3. Instantiate a RetrievalQA chain using `chain_type="stuff"` (or a different combiner).
4. Run queries to retrieve relevant chunks and generate answers.

Minimal skeleton:

```python theme={null}
# 1. Indexing (pseudo)
# embeddings = embed_model.embed_documents(doc_texts)
# 2. Create retriever
retriever = vector_store.as_retriever(search_k=10)

# 3. Create RetrievalQA chain
from langchain.chains import RetrievalQA
retrieval_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

# 4. Run a query
answer = retrieval_qa.run("Explain the main points about X.")
print(answer)
```

## Practical tips for production

* Monitor token usage and costs when using `stuff` on many documents.
* Tune chunk size and overlap at indexing time to balance retrieval relevance and context length.
* Cache frequent retrieval results or answers to reduce repeated costs.
* Test different combiner strategies on a validation set to pick the best trade-off of cost and quality.

## Summary

* Stuff chain: concatenates documents into a single prompt and works well when everything fits in the LLM context window.
* Retrieval chain: retrieves relevant chunks from a vector store and then combines them (often via `stuff`, `map_reduce`, or `refine`) before calling the LLM; it scales to large document collections.
* Choose between them based on corpus size, LLM context limits, latency, and quality needs.

## Links and references

* [LangChain documentation](https://langchain.readthedocs.io/)
* FAISS: [https://github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss)
* Chroma: [https://www.trychroma.com/](https://www.trychroma.com/)
* Overview on RAG patterns: [https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-bfc2-40d7-89fc-f537792272ff/lesson/83ce2c7c-a5ea-428f-8fec-a33a56c9d69e" />
</CardGroup>


# Using Document Chain

Source: https://notes.kodekloud.com/docs/LangChain/Implementing-Chains/Using-Document-Chain/page

Tutorial showing how to use LangChain to load two TechCrunch articles, concatenate their text into a single prompt, and synthesize information with a stuff documents chain.

In this lesson we build a simple "stuff documents" chain with LangChain to synthesize information from two TechCrunch articles. The objective is to:

* Load both web pages,
* Combine (or "stuff") their text into a single prompt context, and
* Send that combined context with a prompt to an LLM using LangChain’s `create_stuff_documents_chain`.

We’ll use two articles that both cover recent developments in generative AI, which makes them a good fit for synthesis across sources.

<Frame>
  <img alt="The image shows a webpage from TechCrunch discussing Microsoft's investment in Mistral AI, with some ads and a navigation bar on the left side." />
</Frame>

Overview

* Input: two TechCrunch URLs about Mistral AI and AI21 Labs.
* Process: fetch page text with `WebBaseLoader`, concatenate documents into `{context}`, and run a "stuff" chain that uses a chat LLM.
* Output: a synthesized answer that extracts model names or other requested facts from both articles.

Imports and setup

* Import the chat model, the chat prompt template helper, the web loader, and the helper that builds a "stuff documents" chain.

```python theme={null}
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.document_loaders import WebBaseLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
```

Load the two URLs and inspect the loaded documents

* Define the two TechCrunch URLs, construct a `WebBaseLoader` with both, and call `load()`. The loader returns a list of Document objects (one per page in this example), each containing `page_content` and `metadata`.

```python theme={null}
URL1 = "https://techcrunch.com/2024/02/27/microsoft-made-a-16-million-investment-in-mistral-ai/"
URL2 = "https://techcrunch.com/2024/03/28/ai21-labs-new-text-generating-ai-model-is-more-efficient-than-most/"

loader = WebBaseLoader([URL1, URL2])
data = loader.load()

print(len(data))  # Expect: 2
```

* Inspect `data[0].page_content` or `data[1].page_content` to preview the scraped text. Each Document has the text and any available metadata (e.g., `source`).

<Frame>
  <img alt="The image shows a JupyterLab interface with a document open, displaying a large block of text discussing Microsoft's investment in Mistral AI." />
</Frame>

Construct the prompt

* Create a system-style prompt template that expects a `context` variable. The stuffs chain will concatenate document texts and inject them into `{context}`.

```python theme={null}
prompt = ChatPromptTemplate.from_messages(
    [("system", "What models are launched by Mistral and AI21 Labs:\n\n{context}")]
)
```

* This simple template asks the model to extract model names (and can be adapted to request summaries, comparisons, or bullet lists).

Initialize the LLM and create the stuff documents chain

* Instantiate the chat LLM (here using GPT-3.5-turbo) and pass it with the prompt template into `create_stuff_documents_chain`.

```python theme={null}
llm = ChatOpenAI(model_name="gpt-3.5-turbo")
chain = create_stuff_documents_chain(llm, prompt)
```

Invoke the chain with the loaded documents

* Call the chain with the `input_documents` parameter set to the `data` list returned by the loader. The stuff chain concatenates the Documents and places that text into the prompt’s `{context}` variable before sending the combined prompt to the LLM.

```python theme={null}
result = chain.invoke({"input_documents": data})
print(result)
```

Example model response (illustrative)

* The LLM may return a concise synthesized answer combining information from both articles, for example:

```plaintext theme={null}
"The articles indicate which specific models each company announced; the chain would extract and list the model names and any short descriptions provided in the articles."
```

How the stuff documents chain works

* The "stuff" approach:
  * Concatenates all document contents into a single context string.
  * Inserts that string into the prompt template’s `{context}`.
  * Sends the full prompt to the LLM in one request.

When to use a stuff chain vs. retrieval

* Use a stuff documents chain when:
  * The combined text comfortably fits within your model’s context window.
  * You want a simple, deterministic pipeline for small document sets.

* Prefer a retrieval-based chain when:
  * You have many documents or very long texts.
  * You need relevance filtering or semantic search over chunks before prompting.

Summary

* Steps covered:
  1. Load multiple web pages with `WebBaseLoader`.
  2. Build a prompt template that accepts a `{context}` placeholder.
  3. Create a stuff documents chain using `create_stuff_documents_chain(llm, prompt)`.
  4. Invoke the chain with the loaded documents to get a synthesized response.

Quick reference

| Topic             | Example / Command                                     |
| ----------------- | ----------------------------------------------------- |
| Load web pages    | `loader = WebBaseLoader([URL1, URL2])`                |
| Inspect documents | `data[0].page_content`                                |
| Prompt template   | `ChatPromptTemplate.from_messages([... "{context}"])` |
| Create chain      | `create_stuff_documents_chain(llm, prompt)`           |
| Invoke chain      | `chain.invoke({"input_documents": data})`             |

Links and references

* [LangChain Documentation](https://langchain.readthedocs.io/)
* [OpenAI Chat Models](https://platform.openai.com/docs/models)
* [TechCrunch](https://techcrunch.com/)

<Callout icon="lightbulb">
  Use the stuff documents chain when your documents' combined size is comfortably within the model's context window. If you expect larger corpora or many documents, prefer a retrieval chain to select relevant chunks before prompting the LLM.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-bfc2-40d7-89fc-f537792272ff/lesson/19ac7110-a87f-434a-aa15-a4fcb9e410b1" />
</CardGroup>
