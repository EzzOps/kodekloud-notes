# --- Source loader ---
# To use a PDF instead, replace the loader below with PyPDFLoader:
URL = "https://www.theverge.com/2024/4/18/24133808/meta-ai-assistant-llama-3-chatgpt-openai-rival"
loader = WebBaseLoader(URL)

# --- Load and split into documents/pages ---
pages = loader.load_and_split()

# --- Split into smaller chunks to improve embedding quality ---
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
chunks = text_splitter.split_documents(pages)

# --- Create embeddings and build a vector store ---
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings)

# --- Use the vectorstore as a retriever ---
retriever = vectorstore.as_retriever()

# --- Helper: format retrieved documents into one context string ---
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# --- LLM and prompt configuration ---
llm = ChatOpenAI()  # choose model/temperature as needed
template = """SYSTEM: You are a question-answering bot.
Be factual in your response.
Answer the following question: {question}
Use ONLY the context provided below: {context}
If the answer is not in the context, say you don't know."""
prompt = PromptTemplate.from_template(template)

# --- Compose the chain: combine LLM and prompt ---
chain = LLMChain(llm=llm, prompt=prompt)

# --- Run a query against the retrieved context ---
question = "What's the size of the largest Llama 3 model?"
docs = retriever.get_relevant_documents(question)
context = format_docs(docs)
result = chain.run(context=context, question=question)
print(result)

# Expected output:
# 'The largest Llama 3 model will have over 400 billion parameters.'
```

<Callout icon="lightbulb">
  The key idea: switch the loader (for example, `PyPDFLoader` -> `WebBaseLoader`) to change your source from PDFs to webpages. The rest of the RAG pipeline—splitting, embeddings, vector store, retriever, prompt, and LLM—remains the same.
</Callout>

Workflow summary

| Step              | Purpose                                               | Example / Notes                                                    |
| ----------------- | ----------------------------------------------------- | ------------------------------------------------------------------ |
| Load documents    | Read source content (PDF or webpage)                  | `WebBaseLoader(URL)` or `PyPDFLoader("file.pdf")`                  |
| Split into chunks | Create smaller passages for embeddings                | `RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)` |
| Create embeddings | Convert text chunks to vectors                        | `OpenAIEmbeddings(model="text-embedding-3-large")`                 |
| Store embeddings  | Persist vectors for efficient retrieval               | `Chroma.from_documents(...)`                                       |
| Create retriever  | Provide similarity search API over embeddings         | `vectorstore.as_retriever()`                                       |
| Format context    | Aggregate retrieved docs into a single context string | `format_docs(docs)`                                                |
| Query LLM         | Send `context` + `question` to the prompt/LLM         | `LLMChain(llm=..., prompt=...)`                                    |

Best practices and tips

* Use chunk sizes that balance context fidelity and embedding cost. Typical ranges: 200–1000 tokens depending on use case.
* Persist your vector store (Chroma or other) between runs to avoid re-embedding the same documents.
* Add a retrieval filter or metadata to narrow results if you’re working with many documents.
* When querying the LLM, instruct it clearly to rely only on the provided context if factual accuracy is critical.

Links and references

* LangChain documentation: [https://langchain.readthedocs.io/](https://langchain.readthedocs.io/)
* Chroma vector database: [https://www.trychroma.com/](https://www.trychroma.com/)
* OpenAI embeddings: [https://platform.openai.com/docs/guides/embeddings](https://platform.openai.com/docs/guides/embeddings)
* The Verge article used in this example: [https://www.theverge.com/2024/4/18/24133808/meta-ai-assistant-llama-3-chatgpt-openai-rival](https://www.theverge.com/2024/4/18/24133808/meta-ai-assistant-llama-3-chatgpt-openai-rival)

Try replacing the `URL` with your own webpages or switching to `PyPDFLoader` to use PDFs. You can also plug this retrieval step into higher-level prebuilt chains for summarization, QA, or citation-aware responses.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/e47b44c9-65c3-46f8-8bed-b075a18ab12b/lesson/9b858443-cf1c-4573-b52f-7a1740cd473c" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/langchain/module/e47b44c9-65c3-46f8-8bed-b075a18ab12b/lesson/124c59d6-584f-4ab5-8190-8f83f35a14ab" />
</CardGroup>


# Callbacks

Source: https://notes.kodekloud.com/docs/LangChain/Tips-Tricks-and-Resources/Callbacks/page

Explains LangChain callbacks, using built-in and custom handlers to capture lifecycle events for logging, observability, telemetry, debugging, and production best practices.

All right — we are now at the third demo where

<Frame>
  <img alt="The image is a slide with the word &#x22;Demo&#x22; on the left and &#x22;Callbacks&#x22; on a blue gradient shape on the right." />
</Frame>

In this lesson we’ll explain what callbacks are in LangChain, why they matter for observability and production systems, and how to use built-in and custom handlers to capture lifecycle events from chains and LLM calls.

## Minimal LangChain example

This minimal program creates an LLM chain that formats a prompt and invokes an LLM:

```python theme={null}
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

llm = ChatOpenAI()
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a {subject} teacher"),
        ("human", "Tell me about {concept}")
    ]
)
chain = LLMChain(llm=llm, prompt=prompt)

chain.invoke({"subject": "physics", "concept": "galaxy"})
```

A typical result returned by the chain might look like this (JSON-style):

```json theme={null}
{
  "subject": "physics",
  "concept": "galaxy",
  "text": "A galaxy is a vast system of stars, gas, dust, and dark matter bound together by gravity. It is the basic building block of the universe, containing billions to trillions of stars, as well as planets, nebulae, and other celestial objects.\n\nGalaxies come in different shapes and sizes, including spiral, elliptical, and irregular types. Our Milky Way is a spiral galaxy that contains hundreds of billions of stars. Galaxies often group into clusters and provide important clues about the structure and evolution of the universe."
}
```

## What are callbacks and why use them?

A callback is a function or handler that the LangChain runtime invokes at specific lifecycle events — for example when a prompt is formatted, when an LLM call starts or ends, when a chain begins or finishes, or when tools are invoked. Callbacks allow you to:

* Record runtime events (console, files, or structured logs).
* Route events to observability systems (Datadog, Splunk, CloudWatch, etc.).
* Transform or post-process outputs (HTML, structured JSON).
* Aggregate metrics and implement custom telemetry.
* Debug and trace execution across chains and tools.

Example uses:

* Print LLM/chains events to stdout while developing.
* Save inputs/outputs into structured logs for later analysis.
* Emit metrics for latency, token usage, or error rates.

## Built-in stdout handler example

This example imports and uses the built-in StdOutCallbackHandler to print lifecycle messages to the console. Note how we pass the handler via the `callbacks` parameter to the chain.

```python theme={null}
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.callbacks.stdout import StdOutCallbackHandler
