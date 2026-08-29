# First page content
pages[0].page_content
```

```text theme={null}
"complaint or concern about your work situation. You can contact the HR department for more information on the discipline and grievance procedures. We hope that this handbook has given you a clear and comprehensive overview of what it means to work at LakeSide Bicycles. If you have any questions or suggestions, please feel free to contact the HR department. We look forward to working with you and making LakeSide Bicycles a great place to work!"
```

View the first page's metadata:

```python theme={null}
# First page metadata
pages[0].metadata
```

```json theme={null}
{"source": "data/handbook.pdf", "page": 1}
```

## Iterate pages for inspection or processing

You can loop over `pages` to print metadata and a snippet of each page. This is useful for quick validation before moving to embeddings or indexing.

```python theme={null}
for i, p in enumerate(pages, start=1):
    print(f"Page {i} metadata: {p.metadata}")
    print(p.page_content[:200])  # print first 200 chars for a quick preview
    print("---")
```

## Next steps in a RAG pipeline

After successfully loading and splitting the PDF, common next steps are:

* Clean or normalize the text if necessary (remove headers/footers).
* Create embeddings for each page using an embeddings model.
* Store embeddings in a vector store (e.g., FAISS, Pinecone, Weaviate).
* Build a retriever and attach a language model for Q\&A/chat over the handbook.

References:

* LangChain docs: [https://langchain.readthedocs.io/en/latest/](https://langchain.readthedocs.io/en/latest/)
* Vector stores: FAISS, Pinecone, Weaviate

<Callout icon="warning">
  Scanned or image-based PDFs will not yield good text using PyPDFLoader alone — they need OCR (e.g., Tesseract, Amazon Textract, or other OCR services) before or during loading. Also, encrypted PDFs may require a decryption key or preprocessing.
</Callout>

## Tips and common issues

* If pages contain repeated header/footer text, consider removing those segments during preprocessing to improve retrieval relevance.
* Verify encoding and whitespace issues on extraction; sometimes lines may be broken incorrectly and require normalization.
* For large PDFs, consider splitting on semantic boundaries (sections or paragraphs) instead of fixed pages to get better retrieval granularity.

Now that the handbook is loaded and split into page-level Documents, you can proceed to embedding, indexing, and building your RAG-powered Q\&A or chat application. Similar loader patterns apply to web pages and other document formats (use appropriate loaders and OCR tools where necessary).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-65c3-46f8-8bed-b075a18ab12b/lesson/18155e0f-cc83-4438-ac30-051e60337344" />
</CardGroup>


# Loading Webpages

Source: https://notes.kodekloud.com/docs/LangChain/Performing-Retrieval/Loading-Webpages/page

Guide to loading webpages into LangChain, inspecting Documents, chunking text for embeddings and indexing, using WebBaseLoader and RecursiveCharacterTextSplitter with a Verge article example

This guide shows how to load a web page into LangChain so you can use its content as context for chatbots, retrieval-augmented generation (RAG), or other retrieval tasks. We'll demonstrate using an article from The Verge about Meta’s AI assistant and Llama 3. The process covers:

1. Loading the page with a web loader
2. Inspecting the returned Document(s)
3. Splitting (chunking) the text for embedding or indexing

<Frame>
  <img alt="The image is an article about Meta's competition with ChatGPT, discussing the introduction of Meta's AI assistant across platforms like Instagram, WhatsApp, and Facebook, along with the release of their AI model, Llama 3. It includes an event photo showing a presentation with large mobile UI mockups in the background." />
</Frame>

## 1) Load the page using WebBaseLoader

WebBaseLoader fetches and parses a page, returning a list of LangChain `Document` objects. It often captures metadata such as the source URL and title.

Example:

```python theme={null}
from langchain_community.document_loaders import WebBaseLoader

URL = "https://www.theverge.com/2024/4/18/24133808/meta-ai-assistant-llama-3-chatgpt-openai-rival"
loader = WebBaseLoader(URL)
data = loader.load()
```

Common immediate check:

```python theme={null}
len(data)
