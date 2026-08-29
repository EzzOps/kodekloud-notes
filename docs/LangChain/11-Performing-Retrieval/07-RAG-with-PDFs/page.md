# Example: retrieve top 2 documents most related to "Rohit Sharma"
results_rohit = vectorstore.similarity_search("Rohit Sharma", k=2)
print(results_rohit)
# Example output (list of Document objects):
# [Document(page_content='Record Crowds and Unforgettable Moments: Highlights from the Cricket World Cup'),
# Example: retrieve top 2 documents most related to "Lionel Messi"
results_messi = vectorstore.similarity_search("Lionel Messi", k=2)
print(results_messi)
# Example output:
# [Document(page_content='From Underdogs to Contenders: Football World Cup Surprises and Breakout Stars'),
#  Document(page_content='Global Giants Clash: Football World Cup Semi-Finals Set the Stage for Epic Showdowns')]
```

## Why This Works (Concise)

* Both documents and the query are converted into embeddings by the same model (`text-embedding-3-large`).
* The vector database compares these vectors (e.g., using cosine similarity) and returns the nearest vectors/documents.
* This is semantic search: the system can associate concepts (e.g., player names) with relevant documents even when the exact token does not appear in the text.

<Callout icon="lightbulb">
  Tip: The `k` (top-k) parameter controls how many nearest neighbors you retrieve. Choose `k` based on how many documents you want to use downstream (for example, as context for a language model). You can also store metadata with each text to help identify sources.
</Callout>

## Common Parameters and Options

| Parameter  | Purpose                                                      | Example                         |
| ---------- | ------------------------------------------------------------ | ------------------------------- |
| `model`    | Embedding model used to create vector representations        | `text-embedding-3-large`        |
| `texts`    | List of strings to embed and store                           | `["text1", "text2"]`            |
| `k`        | Number of nearest neighbors to retrieve in similarity search | `k=2`                           |
| `metadata` | Optional: identify source, doc id, URL for each text         | `{"source": "news", "id": 123}` |

## End-to-End Pattern

A concise end-to-end workflow:

1. Initialize embeddings with your chosen model.
2. Convert texts (or chunks) into embeddings and store in Chroma.
3. For each user query, embed the query and run `similarity_search(query, k=...)`.
4. Use the retrieved documents as context for downstream tasks (summarization, QA, RAG).

This simple pattern powers many production retrieval pipelines: obtain relevant chunks quickly and then pass them to a language model for generation, question answering, or summarization.

## Links and References

* [Kubernetes Documentation](https://kubernetes.io/docs/) (example resource link)
* [LangChain Documentation](https://python.langchain.com/)
* [Chroma (vector DB)](https://www.trychroma.com/)
* [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-65c3-46f8-8bed-b075a18ab12b/lesson/412c6d90-f6c8-4468-9287-9efce864fe74" />
</CardGroup>


# RAG with PDFs

Source: https://notes.kodekloud.com/docs/LangChain/Performing-Retrieval/RAG-with-PDFs/page

Step-by-step guide to building a PDF-based RAG pipeline with LangChain, covering PDF loading, chunking, embeddings, Chroma indexing, retrieval, prompt composition, and LCEL chain for document-grounded QA.

This guide demonstrates an end-to-end Retrieval-Augmented Generation (RAG) pipeline using a single notebook. You will load a PDF, split it into chunks, embed those chunks, index them in a vector database, create a retriever, stitch retrieved passages into context, and run a LangChain Expression Language (LCEL) chain that answers user questions strictly from the document content.

This lesson connects document loaders, chunking strategy, embedding models, and vector stores to build a document-grounded Q\&A assistant.

## Key libraries and imports

Use the following imports in your notebook:

```python theme={null}
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
```

## High-level workflow

1. Load the PDF and split it into pages.
2. Chunk pages into smaller passages to control context length.
3. Embed chunks with an embeddings model.
4. Index embeddings into a vector store (Chroma).
5. Create a retriever from the vector store to fetch relevant passages at query time.
6. Format retrieved passages into a single context string.
7. Compose an LCEL chain: retriever -> formatter -> prompt -> LLM -> output parser.
8. Ask questions; the chain returns answers grounded in the document.

## Step-by-step implementation

### 1) Load the PDF and split into page documents

```python theme={null}
loader = PyPDFLoader("data/handbook.pdf")
pages = loader.load_and_split()
```

This produces a list of page-level Document objects that preserve page content and metadata.

### 2) Create chunks from the pages

```python theme={null}
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
chunks = text_splitter.split_documents(pages)
```

Use chunking to ensure passages are short enough for the embeddings model and downstream LLM context. Adjust `chunk_size` and `chunk_overlap` based on your LLM's context window and the granularity you need.

### 3) Initialize embeddings and index chunks into Chroma

```python theme={null}
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings)
```

Chroma stores vector representations for each chunk so you can retrieve the most relevant passages at query time.

### 4) Create a retriever from the vector store

```python theme={null}
retriever = vectorstore.as_retriever()
```

The retriever provides a simple API to fetch top-k relevant documents for a user query.

### 5) Helper to format retrieved docs into a single context string

```python theme={null}
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
```

This helper concatenates retrieved passages into a single context block that will be passed to the prompt. You can extend this to include source citations or metadata.

### 6) Set up the LLM and prompt template

```python theme={null}
llm = ChatOpenAI()

template = """SYSTEM: You are a question answer bot.
Be factual in your response.
Respond to the following question: {question} only from the below context: {context}.
If you don't know the answer, just say that you don't know.
"""

prompt = PromptTemplate.from_template(template)
```

This prompt explicitly instructs the model to answer only from the provided `context`, reducing hallucinations.

<Callout icon="lightbulb">
  Tip: You can expand the prompt to include explicit formatting requirements, a maximum answer length, or citation formatting (e.g., "Answer with the source page number in brackets after each sentence").
</Callout>

### 7) Build the LCEL chain that connects retriever -> formatter -> prompt -> LLM -> output parser

The LCEL pipeline retrieves relevant chunks at runtime, formats them, fills the prompt template, calls the LLM, and parses the output into a string.

```python theme={null}
chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

This runnable pipeline takes a question as input, runs retrieval, and returns a parsed string answer.

<Callout icon="warning">
  Warning: Retrieval quality depends on chunking strategy, embedding model, and vector store configuration. Also monitor API usage and costs when calling embedding and LLM endpoints.
</Callout>

### 8) Invoke the chain with user questions

Example 1 — ask about sick leaves:

```python theme={null}
response = chain.invoke("How many sick leaves are allowed in a year?")
