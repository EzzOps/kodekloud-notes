# Loading PDFs

Source: https://notes.kodekloud.com/docs/LangChain/Performing-Retrieval/Loading-PDFs/page

Demonstrates loading a PDF with PyPDFLoader, splitting into page documents, inspecting content and metadata, and preparing pages for embeddings and RAG pipelines.

In this lesson you'll learn how to load a PDF and split it into pages as the first step of a Retrieval-Augmented Generation (RAG) pipeline. We'll use a small, fictitious employee handbook for "Lakeside Bicycles" — a simple three-page PDF containing policies such as leave and discipline procedures. The goal is to extract the handbook text, split it into page-level documents, inspect the results, and prepare the output for downstream steps like embedding, indexing, and building a Q\&A/chat interface.

> **lightbulb** Before running the examples, install the required packages. A typical install command is:

  ```bash theme={null}
  pip install langchain-community pypdf
  ```

  See [langchain-community on PyPI](https://pypi.org/project/langchain-community) and [pypdf on PyPI](https://pypi.org/project/pypdf) for details. For LangChain docs, visit [LangChain Documentation](https://langchain.readthedocs.io/en/latest/).

## Example dataset

From a notebook or shell, list the dataset directory:

```bash theme={null}
!ls data
```

```text theme={null}
handbook.pdf
```

## Load and split the PDF into page documents

We use the PyPDFLoader from the langchain-community package. The loader's `load_and_split()` method extracts text and returns a list of LangChain `Document` objects (one per page by default).

```python theme={null}
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("data/handbook.pdf")
pages = loader.load_and_split()
```

Check how many page documents were produced:

```python theme={null}
len(pages)
```

```text theme={null}
3
```

## What each page Document contains

Each item in `pages` is a LangChain `Document` with two primary attributes:

|      Attribute | Description                                         | Example                                      |
| -------------: | --------------------------------------------------- | -------------------------------------------- |
| `page_content` | Extracted text for that page                        | Short string containing page text            |
|     `metadata` | Metadata about the page (source, page number, etc.) | `{"source": "data/handbook.pdf", "page": 1}` |

## Inspect a page's content and metadata

View the first page's extracted text:

```python theme={null}
