# Create project and virtual environment
touch main.py
python3 -m venv venv
source venv/bin/activate

# Install the DOCX parser dependency
pip install python-docx
```

Note: Ensure you run these commands in the directory where you'll keep your DOCX files (for example, the same directory as `main.py`).

<Callout icon="lightbulb">
  Make sure a DOCX file named `Sample.docx` (or another filename you pass to the script) is present in the same directory when you run the example below.
</Callout>

Imports and core class

Below is a consolidated implementation of the DOCX ingestion pipeline. Save the code into `main.py`. This single file contains:

* `parse_docx` — read paragraphs and extract basic core properties into metadata.
* `chunk_text` — split text into overlapping chunks while preferring paragraph and sentence boundaries, and falling back to word boundaries.
* `process_document` — orchestrator that parses and chunks, injecting document metadata into each chunk.
* `_generate_doc_id` — convenience helper to create a deterministic document ID.

```python theme={null}
from docx import Document
from pathlib import Path
from typing import List, Dict, Optional
import hashlib
import datetime


class DocxParser:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Args:
            chunk_size: maximum number of characters per chunk
            chunk_overlap: number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def parse_docx(self, file_path: str) -> Dict:
        """
        Parse a DOCX file and extract content with metadata.

        Returns:
            dict: {
                'content': str,
                'paragraphs': List[str],
                'metadata': Dict[str, Optional[str]]
            }
        """
        path = Path(file_path)
        doc = Document(file_path)

        # Extract paragraphs (skip empty paragraphs)
        paragraphs: List[str] = []
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                paragraphs.append(text)

        # Join paragraphs with double newline to preserve paragraph boundaries
        content = "\n\n".join(paragraphs)

        # Core properties may be None
        core_props = doc.core_properties
        created = None
        modified = None
        try:
            if core_props.created:
                created = core_props.created.isoformat()
        except Exception:
            # Some versions or properties may not be datetime; convert to str as fallback
            created = str(core_props.created) if core_props.created else None

        try:
            if core_props.modified:
                modified = core_props.modified.isoformat()
        except Exception:
            modified = str(core_props.modified) if core_props.modified else None

        metadata = {
            "filename": path.name,
            "file_path": str(path.absolute()),
            "title": core_props.title or "Untitled",
            "author": core_props.author or "Unknown",
            "created": created,
            "modified": modified,
        }

        return {"content": content, "paragraphs": paragraphs, "metadata": metadata}

    def chunk_text(self, text: str) -> List[Dict]:
        """
        Split text into overlapping chunks.

        The method prioritizes:
          1. Paragraph boundaries ('\n\n')
          2. Sentence endings ('.', '!', '?')
          3. Word boundaries (whitespace)

        Returns:
            List of chunk dictionaries with metadata:
            {
                'chunk_id': int,
                'text': str,
                'start_char': int,
                'end_char': int,
                'chunk_length': int
            }
        """
        chunks: List[Dict] = []
        start = 0
        chunk_id = 0
        text_length = len(text)

        sentence_end_chars = {".", "!", "?"}

        while start < text_length:
            # Default end (cap at text_length)
            end = min(start + self.chunk_size, text_length)

            if end < text_length:
                # Search for paragraph break within the overlap zone
                search_start = max(start, end - self.chunk_overlap)
                found = False

                # Look for paragraph break '\n\n'
                for i in range(end, search_start - 1, -1):
                    if text[i : i + 2] == "\n\n":
                        end = i + 2  # include the paragraph break
                        found = True
                        break

                # Look for sentence ending if no paragraph break found
                if not found:
                    sentence_search_start = max(start, end - max(100, self.chunk_overlap // 2))
                    for i in range(end - 1, sentence_search_start - 1, -1):
                        if text[i] in sentence_end_chars:
                            end = i + 1  # include the sentence-ending punctuation
                            found = True
                            break

                # Finally, fallback to word boundary (whitespace)
                if not found:
                    for i in range(end - 1, search_start - 1, -1):
                        if text[i].isspace():
                            end = i
                            found = True
                            break

                # If still not found, keep the original end (hard cut)
            # Extract the chunk text
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(
                    {
                        "chunk_id": chunk_id,
                        "text": chunk_text,
                        "start_char": start,
                        "end_char": end,
                        "chunk_length": len(chunk_text),
                    }
                )
                chunk_id += 1

            # Advance start; if not at end, move back by overlap
            if end >= text_length:
                break
            start = end - self.chunk_overlap if end < text_length else end

        return chunks

    def process_document(self, file_path: str) -> List[Dict]:
        """
        Complete pipeline: parse DOCX and create chunks, attaching document metadata to each chunk.

        Returns:
            List[Dict]: chunks with attached 'document_metadata' and 'document_id'
        """
        # Parse the document
        doc_data = self.parse_docx(file_path)

        # Chunk the full content
        chunks = self.chunk_text(doc_data["content"])

        # Add document metadata to each chunk
        document_id = self._generate_doc_id(str(file_path))
        for chunk in chunks:
            chunk["document_metadata"] = doc_data["metadata"]
            chunk["document_id"] = document_id

        return chunks

    def _generate_doc_id(self, file_path: str) -> str:
        """Generate a deterministic document ID (MD5 of the file path)."""
        return hashlib.md5(file_path.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    # Ensure you have a file named 'Sample.docx' in the same directory!
    parser = DocxParser(chunk_size=1000, chunk_overlap=200)

    # Process the document and get our chunks
    chunks = parser.process_document("Sample.docx")

    # Print the results for inspection
    for chunk in chunks:
        print(f"---- Chunk {chunk['chunk_id']} (Length: {chunk['chunk_length']}) ----")
        print(chunk["text"])
        print(f"Source: {chunk['document_metadata']['title']} (ID: {chunk['document_id']})")
        print("________________________________________________________________\n")
```

How the parser works (summary)

* parse\_docx
  * Uses `python-docx` to read paragraph texts.
  * Removes empty paragraphs and joins paragraphs with a double-newline (`\n\n`) so that paragraph boundaries are preserved and available to the chunking logic.
  * Extracts core properties (title, author, created, modified) when available and returns them as metadata.

* chunk\_text
  * Slides a window of size `chunk_size` across the full text.
  * Within the overlap region it prefers:
    1. Paragraph boundary (`\n\n`)
    2. Sentence-ending punctuation (`.`, `!`, `?`)
    3. Word boundary (whitespace)
  * If none of the above are found in the overlap, it performs a hard cut.
  * Produces overlapping chunks by advancing start to `end - chunk_overlap`.

* process\_document
  * Orchestrates parsing and chunking, attaches `document_metadata` and a deterministic `document_id` to each chunk. Chunks are ready for embedding and storage in a vector database.

DocxParser configuration and outputs

| Parameter       |                                       Purpose | Example |
| --------------- | --------------------------------------------: | ------- |
| `chunk_size`    |                  Maximum characters per chunk | `1000`  |
| `chunk_overlap` | Overlap characters between consecutive chunks | `200`   |

Chunk dictionary schema (each chunk returned by `process_document`):

| Key                 | Description                         | Example                  |
| ------------------- | ----------------------------------- | ------------------------ |
| `chunk_id`          | Integer chunk index                 | `0`                      |
| `text`              | The chunked text string             | `"...paragraph text..."` |
| `start_char`        | Start offset in original text       | `0`                      |
| `end_char`          | End offset in original text         | `966`                    |
| `chunk_length`      | Length of the `text` field          | `966`                    |
| `document_metadata` | Document-level metadata (see below) | See below                |
| `document_id`       | Deterministic ID for provenance     | `md5 hash`               |

Document metadata keys produced by `parse_docx`:

| Key         | Description                     | Example                          |
| ----------- | ------------------------------- | -------------------------------- |
| `filename`  | File name                       | `Sample.docx`                    |
| `file_path` | Absolute path                   | `/home/user/project/Sample.docx` |
| `title`     | Document title (or `Untitled`)  | `My Report`                      |
| `author`    | Author (or `Unknown`)           | `Jane Doe`                       |
| `created`   | Created timestamp (ISO format)  | `2023-05-01T12:00:00`            |
| `modified`  | Modified timestamp (ISO format) | `2023-05-02T08:30:00`            |

Example output (sample)

When you run `python main.py` against a small DOCX (`Sample.docx`), you'll see printed chunks similar to:

```plaintext theme={null}
---- Chunk 0 (Length: 966) ----
The Fable of Fiona the Fussy Feline

Fiona, a tuxedo cat of considerable fluff and questionable temper, believed the world revolved entirely around the timely provision of tuna in springwater, not brine. She lived with a human named Bernard, a kind but perpetually confused soul who often purchased the wrong variety.

"Mrow?" Fiona would inquire, delicately batting a paw at the offensive can, a dramatic sigh escaping her tiny pink nose. The sound was less a plea and more a deeply felt existential critique of Bernard's life choices.

The Sardine Incident
...
Source: The Fable of Fiona the Fussy Feline (ID: 1a2b3c4d5e6f...)
________________________________________________________________

---- Chunk 1 (Length: 936) ----
Title: Untitled

Bernard's Excuse: "They were on a special, Fiona! And they have extra Omega-3s!"
...
Source: Untitled (ID: 1a2b3c4d5e6f...)
________________________________________________________________
```

Next steps and recommendations

* Embed each chunk's `text` with your embedding model and persist the vectors along with `document_metadata` and `document_id` in your vector database. Use the metadata to provide provenance during retrieval and answer generation.
* Extend `parse_docx` to extract headings, tables, footnotes, and other structured content to improve chunk semantics and retrieval precision.
* Tune `chunk_size`/`chunk_overlap` for your embedding model and retrieval latency: larger chunks reduce the number of vectors but may reduce relevance granularity.

Best practices

* Keep paragraph breaks (`\n\n`) intact when possible to make chunks more semantically meaningful.
* Store `document_id` and `filename` with vectors for traceability.
* For multi-document ingestion, compute a file hash or use a content hash for deduplication.

Links and references

* [python-docx documentation](https://python-docx.readthedocs.io/)
* [Introduction to LLMs and OpenAI courses](https://learn.kodekloud.com/user/courses/introduction-to-openai)
* [Fundamentals of RAG](https://learn.kodekloud.com/user/courses/fundamentals-of-rag)
* [Vector database essentials](https://learn.kodekloud.com/user/courses/vector-database-for-genai)

This parser is a simple, extensible baseline for DOCX ingestion in RAG pipelines and integrates well with embedding models and vector stores for scalable retrieval.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/6c0f08eb-0b91-48b6-af70-e95dbf30af15/lesson/03d7891a-3b40-440f-9db5-5f2b04a70a5f" />
</CardGroup>


# Demo Ingesting PDF

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Document-Processing-and-Chunking/Demo-Ingesting-PDF/page

A tutorial demonstrating a reusable PDFParser that extracts selectable text, splits it into RAG-friendly chunks, emits metadata, and provides usage examples and OCR guidance.

Earlier we built a Python script to parse and chunk DOCX files. In this lesson we'll add a reusable PDFParser to the toolkit so your retrieval-augmented generation (RAG) pipeline can handle PDFs as well.

Why this matters for RAG:

* A useful knowledge base must handle multiple document types.
* PDFs vary widely: some contain selectable text, others are scanned images that require OCR.
* This parser extracts selectable text (when present), splits it into context-aware chunks, and emits structured metadata to feed an embedding / vector store pipeline.

Install the required packages in your virtual environment:

```bash theme={null}
pip install PyPDF2 langchain
```

<Callout icon="lightbulb">
  [PyPDF2](https://pypi.org/project/PyPDF2/) extracts selectable text from PDF files. If your PDF is a scanned image (no selectable text), add an OCR preprocessing step such as [Tesseract](https://github.com/tesseract-ocr/tesseract) with [pytesseract](https://pypi.org/project/pytesseract/) before feeding the text into the chunker.
</Callout>

***

## pdf\_parser.py — reusable PDFParser class

This module provides a compact, reusable class that:

* extracts selectable text from PDFs,
* splits text into chunks optimized for RAG ingestion,
* returns structured metadata for each chunk,
* optionally writes a human-readable dump for inspection.

Save the file as `pdf_parser.py`.

```python theme={null}
