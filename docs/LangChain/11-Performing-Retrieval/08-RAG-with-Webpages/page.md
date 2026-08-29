# Expected output: 'You are eligible for 10 days of paid sick leave per year.'
```

Example 2 — ask about unpaid personal leave:

```python theme={null}
response = chain.invoke("How many unpaid leaves are allowed in a year?")
# response -> (answer extracted from the document, e.g., 'You are eligible for up to 10 days of unpaid personal leave per year.')
```

Example 3 — ask for the sick leave policy:

```python theme={null}
response = chain.invoke("What's the sick leave policy?")
# response -> 'You are eligible for 10 days of paid sick leave per year, which can be used for any illness or injury that prevents you from working.'
```

<Frame>
  <img alt="The image displays a section of a document outlining policies for paid vacation leave, paid sick leave, and unpaid personal leave, each with eligibility details and requirements for request and approval." />
</Frame>

When run against the employee handbook, the chain retrieves relevant passages and returns factual answers extracted from the document text:

```python theme={null}
# Example run
response = chain.invoke("How many sick leaves are allowed in a year?")
# response -> 'You are eligible for 10 days of paid sick leave per year.'
```

## Quick reference: Steps & commands

| Step       | Purpose                              | Example command/snippet                                            |
| ---------- | ------------------------------------ | ------------------------------------------------------------------ |
| Load PDF   | Create page-level documents          | `PyPDFLoader("data/handbook.pdf").load_and_split()`                |
| Chunking   | Split pages into manageable passages | `RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)` |
| Embeddings | Vectorize chunks                     | `OpenAIEmbeddings(model="text-embedding-3-large")`                 |
| Indexing   | Store vectors for retrieval          | `Chroma.from_documents(documents=chunks, embedding=embeddings)`    |
| Retriever  | Fetch relevant passages              | `vectorstore.as_retriever()`                                       |
| Formatting | Build context string for prompt      | `format_docs(docs)`                                                |
| LCEL chain | Connect retriever -> prompt -> LLM   | `chain = ({...} \| prompt \| llm \| StrOutputParser())`            |

## Summary

* Load PDFs with a document loader (PyPDFLoader) and split them into pages.
* Chunk pages with a TextSplitter (RecursiveCharacterTextSplitter) for reliable retrieval.
* Embed chunks using OpenAIEmbeddings and index them in Chroma.
* Use the vector store’s retriever to fetch relevant passages at query time.
* Format retrieved passages into a context string and pass it to the LLM via an LCEL chain so the LLM answers strictly from the document.
* This RAG pattern reduces hallucinations and enables document-grounded chatbots. Extend it by adding a UI, supporting arbitrary PDF uploads, or integrating advanced retrieval (reranking, hybrid search) and QA techniques.

## Links and References

* [LangChain — Learn LangChain](https://learn.kodekloud.com/user/courses/langchain)
* Chroma documentation: [https://www.trychroma.com/](https://www.trychroma.com/)
* OpenAI embeddings & models: [https://platform.openai.com/docs/models](https://platform.openai.com/docs/models)

- [Watch Video](https://learn.kodekloud.com/user/courses/langchain/module/e47b44c9-65c3-46f8-8bed-b075a18ab12b/lesson/01cbeda2-251d-4e7b-bf85-cac00fdf40d6)


# RAG with Webpages

Source: https://notes.kodekloud.com/docs/LangChain/Performing-Retrieval/RAG-with-Webpages/page

Explains RAG pipeline using webpages instead of PDFs, swapping only the document loader while keeping embeddings and retrieval unchanged.

This lesson demonstrates that the Retrieval-Augmented Generation (RAG) workflow is identical whether your source is a PDF or a webpage. The only change required is swapping the document loader; everything else in the pipeline—splitting, embedding, vector store, retriever, prompt, and LLM—remains the same.

Below is a clean, corrected example that uses a webpage as the source (a Verge article in this case). The code is organized to highlight each step of the RAG pipeline.

```python theme={null}
from langchain.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
