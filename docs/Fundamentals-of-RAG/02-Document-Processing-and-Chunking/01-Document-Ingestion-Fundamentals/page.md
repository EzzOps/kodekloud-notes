# main.py
import hashlib
from pathlib import Path
from typing import List, Dict


class TextDocumentParser:
    """Parse text files for RAG system ingestion."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Args:
            chunk_size: approximate maximum number of characters per chunk.
            chunk_overlap: number of characters to overlap between consecutive chunks.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def parse_file(self, file_path: str) -> Dict:
        """
        Read a UTF-8 text file and return its content and metadata.

        Returns:
            A dict with 'content' (the file text) and 'metadata' (filename, path, size, extension,
            document_id, char_count, and word_count).
        """
        path = Path(file_path)
        with path.open("r", encoding="utf-8") as f:
            content = f.read()

        metadata = {
            "filename": path.name,
            "file_path": str(path.resolve()),
            "file_size": path.stat().st_size,
            "file_extension": path.suffix,
            "document_id": self._generate_doc_id(str(path.resolve())),
            "char_count": len(content),
            "word_count": len(content.split()),
        }

        return {"content": content, "metadata": metadata}

    def _generate_doc_id(self, file_path: str) -> str:
        """Generate a stable unique document ID based on the absolute file path."""
        return hashlib.md5(file_path.encode("utf-8")).hexdigest()

    def chunk_text(self, text: str) -> List[Dict]:
        """
        Split text into overlapping chunks for RAG processing.

        Algorithm:
        - Start at position 0.
        - Set an initial end = start + chunk_size.
        - If the end is not at the end of text, search backwards from end for a sentence boundary
          (one of '.', '!', '?', or a newline). If found within a reasonable backtrack window,
          break there (include the punctuation/newline in the chunk where appropriate).
        - If no sentence boundary is found, search backwards for a whitespace (word boundary).
        - Extract the chunk, strip whitespace, append to list if non-empty.
        - Advance start to (end - chunk_overlap) to keep an overlap between chunks.
        - Guard against zero-length progress (when no suitable break is found) by forcing forward
          progress up to chunk_size to avoid infinite loops.
        """
        if not text:
            return []

        chunks: List[Dict] = []
        start = 0
        chunk_id = 0
        length = len(text)
        sentence_ends = {".", "!", "?", "\n"}

        while start < length:
            end = min(start + self.chunk_size, length)

            # When we're not at the end, prefer a sentence boundary inside a lookback window
            if end < length:
                best_break = end
                lookback_sentence = max(start, end - 100)  # search up to 100 chars back for sentence end
                for i in range(end - 1, lookback_sentence - 1, -1):
                    if text[i] in sentence_ends:
                        # include the sentence terminator in the chunk
                        best_break = i + 1
                        break

                # If no sentence break found, search for a whitespace/word boundary within a smaller window
                if best_break == end:
                    lookback_word = max(start, end - 50)  # search up to 50 chars back for whitespace
                    for i in range(end - 1, lookback_word - 1, -1):
                        if text[i].isspace():
                            best_break = i
                            break

                end = best_break

                # Ensure we make forward progress; if no break was found and end equals start, advance by chunk_size
                if end <= start:
                    end = min(start + self.chunk_size, length)
                    if end <= start:
                        # nothing more to extract
                        break

            # Extract and store the chunk
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

            # Advance start with overlap
            if end >= length:
                break
            start = max(0, end - self.chunk_overlap)

        return chunks

    def process_document(self, file_path: str) -> List[Dict]:
        """
        Complete pipeline: parse file, chunk content, and attach document metadata to each chunk.

        Returns:
            A list of chunk dicts, each augmented with 'document_metadata'.
        """
        doc_data = self.parse_file(file_path)
        chunks = self.chunk_text(doc_data["content"])

        for chunk in chunks:
            chunk["document_metadata"] = doc_data["metadata"]

        return chunks


if __name__ == "__main__":
    # Example usage
    parser = TextDocumentParser(chunk_size=500, chunk_overlap=100)

    sample_text = """Introduction to RAG Systems
Retrieval-Augmented Generation (RAG) is a powerful technique that augments a model's responses
with external documents by retrieving relevant content and conditioning generation on those results.

The Squirrel and the Wi-Fi Router
Once upon a time, in a quiet suburban neighborhood, there lived a squirrel named Nibbles who loved gadgets...
(Imagine a longer story here to demo chunking.)"""

    sample_path = "sample_doc.txt"
    with open(sample_path, "w", encoding="utf-8") as f:
        f.write(sample_text)

    chunks = parser.process_document(sample_path)

    print(f"Document: {chunks[0]['document_metadata']['filename']}")
    print(f"Total chunks: {len(chunks)}")

    for chunk in chunks[:5]:
        print(f"\nChunk {chunk['chunk_id']}:")
        print(f"Length: {chunk['chunk_length']} chars")
        print(f"Text (preview): {chunk['text'][:150]}...")
```

## How the chunking helps RAG (summary)

* Preferencing sentence boundaries makes chunk contents more meaningful for semantic embeddings.
* Falling back to word boundaries prevents cutting tokens mid-word and reduces noisy embeddings.
* Controlled overlap preserves local context across chunk boundaries, improving relevance during retrieval.
* Attaching `document_metadata` to each chunk enables tracing back results to original documents for provenance, filtering, or display.

> **lightbulb** Tip: Tune `chunk_size` and `chunk_overlap` to match your embedding model's tokenization and the level of context you need. Larger overlap increases context at the cost of more embeddings and storage.

## Example terminal output (abridged)

When you run the script you should see output similar to:

```plaintext theme={null}
Document: sample_doc.txt
Total chunks: 2

Chunk 0:
Length: 287 chars
Text (preview): Introduction to RAG Systems Retrieval-Augmented Generation (RAG) is a powerful technique that augments...

Chunk 1:
Length: 193 chars
Text (preview): The Squirrel and the Wi-Fi Router Once upon a time, in a quiet suburban neighborhood, there lived a squirrel...
```

This confirms the parser reads the file, splits it into coherent chunks, and attaches metadata for each chunk—ready for embedding and ingestion into a RAG pipeline.

## Further reading and references

* [Retrieval-Augmented Generation overview (Hugging Face)](https://huggingface.co/blog/rag)
* [Python pathlib — Working with filesystem paths](https://docs.python.org/3/library/pathlib.html)
* [Unicode/UTF-8 — Background and rationale](https://en.wikipedia.org/wiki/UTF-8)

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/6c0f08eb-0b91-48b6-af70-e95dbf30af15/lesson/98be1389-c32b-4d45-9968-d9a57dc2a65f)


# Document Ingestion Fundamentals

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Document-Processing-and-Chunking/Document-Ingestion-Fundamentals/page

Guides converting messy documents into structured, metadata-rich text for retrieval-augmented generation, covering parsing challenges, PDF layout handling, chunking, and recommended tools

This lesson explains how to convert messy source files into clean, machine-readable artifacts suitable for retrieval-augmented generation (RAG). You’ll learn why raw files often “poison” downstream retrieval, what successful ingestion looks like, and the key parsing challenges across common file types.

Why this matters: large language models and vector search expect clean, sequential, and semantically coherent text. When documents contain layout noise (headers repeated as body text, tables flattened, multi-column misordering), embeddings become noisy and retrieval quality and answer accuracy drop.

<Frame>
  <img alt="The image illustrates the problem of raw data being &#x22;poisonous&#x22; for models due to issues like formatting noise and misinterpretation of headers and tables. It features a robot icon, an input box showing different document types, and a list of problems caused by raw data." />
</Frame>

## What successful ingestion produces

The ingestion pipeline’s output should be consistent, searchable, and enriched with metadata so chunking and indexing produce semantically meaningful embeddings. Effective ingestion typically:

* Extracts readable text with preserved sections and paragraphs.
* Preserves logical structure: headings, sections, lists, and hierarchy.
* Captures relationships: table columns and figure-caption pairings.
* Records document metadata: source, page numbers, authors, timestamps, document type.

These outputs allow chunking to generate coherent, semantically dense units that retrieval systems can match reliably.

> **lightbulb** Design ingestion to produce clean textual units plus metadata. Chunking and indexing rely as much on structure and metadata as on raw text.

## Three pillars of RAG data and ingestion implications

Understanding the data category helps select the right parsing strategy and chunking approach.

* Unstructured: plain text, Markdown, simple logs. Minimal parsing required—text is ready for chunking.
* Semi-structured: PDFs, DOCX, HTML, and other layout-aware documents. Require layout-aware parsing to recover reading order, headings, and tables.
* Structured: databases, CSVs, spreadsheets (XLSX). Focus is on preserving relationships—columns, keys, and row semantics—so query-time reasoning remains accurate.

<Frame>
  <img alt="The image illustrates the three pillars of RAG data: unstructured (plain text, markdown), semi-structured (layout-aware documents like PDFs and DOCX), and structured (databases, spreadsheets like CSVs and XLSX)." />
</Frame>

### Quick reference: formats, common issues, and recommended tools

| Format category                   | Common ingestion problems                      | Recommended tools / approaches                                                       |
| --------------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------ |
| Unstructured (txt, md, logs)      | Little to no structure; noisy tokens           | Python I/O, simple token cleaning                                                    |
| Semi-structured (PDF, DOCX, HTML) | Reading-order loss, columns, detached captions | `python-docx`, `pdfplumber`, `PyMuPDF`, `pdfminer.six`, `layout-parser`, Apache Tika |
| Structured (CSV, XLSX, DB)        | Column relationships, type conversion          | `pandas`, `openpyxl`, DB connectors, schema-aware loaders                            |

Note: wrap any example objects or placeholders as code (e.g., `[{ "object": "person" }]`) to avoid MDX parsing issues.

## Why PDFs are often the hardest case

PDFs are presentation formats: content is placed by coordinates instead of logical sequence. Naive text extraction can produce:

* Column-order collisions (left column mixed with right column).
* Flattened or scrambled tables (cell order lost).
* Headers, footers, and page numbers mixed into body text.
* Captions or figure labels detached from visuals.

<Frame>
  <img alt="The image highlights the challenge with PDFs, emphasizing layout significance with a design meant for viewing rather than reading, and content stored in coordinates. A PDF cover titled &#x22;Powering the Future of Automation&#x22; is also shown." />
</Frame>

Recovering the intended reading order typically requires layout analysis and heuristics—or ML-based document understanding—to group lines into paragraphs, separate columns, and reconstruct tables and captions.

> **warning** Beware of naive PDF text extraction—without layout-aware parsing you'll get noisy text that degrades embeddings and retrieval quality.

## Typical ingestion pipeline pattern

A resilient ingestion pipeline usually mixes multiple specialized parsers and a normalization stage:

1. Raw extraction: choose a parser appropriate for the file type (e.g., `pdfplumber` for PDFs, `python-docx` for DOCX, `pandas` for CSVs).
2. Layout and structure recovery: use layout parsers or heuristics to reconstruct sections, columns, tables, and captions.
3. Chunking: split content into semantically coherent chunks (by paragraph, heading, or table row), keeping chunk size aligned to your embedding model’s context window.
4. Metadata enrichment: attach source, page range, section heading, and other helpful attributes to every chunk.
5. Indexing: calculate embeddings and store in a vector store with metadata for filtering and retrieval.

## Tools and libraries

* DOCX and rich text: `python-docx` — preserves paragraphs and headings.
* PDFs: `pdfplumber`, `PyMuPDF` (fitz), `pdfminer.six` — combine with `layout-parser` or Apache Tika for layout analysis.
* Tables & spreadsheets: `pandas`, `tabula-py`, `openpyxl` — preserve columns and data types.
* RAG and loader frameworks: LangChain, LlamaIndex, Haystack — provide document loaders, chunkers, and connectors for common storage backends.

Resources:

* [pdfplumber](https://github.com/jsvine/pdfplumber)
* [PyMuPDF / fitz](https://pymupdf.readthedocs.io)
* [pdfminer.six](https://github.com/pdfminer/pdfminer.six)
* [layout-parser](https://layout-parser.github.io)
* [python-docx](https://python-docx.readthedocs.io)
* [pandas](https://pandas.pydata.org)
* [openpyxl](https://openpyxl.readthedocs.io)
* RAG frameworks: LangChain, LlamaIndex, Haystack

## Practical tips for robust ingestion

* Always retain source metadata. It enables filtering and provenance in retrieval.
* Chunk semantically (by heading/section) rather than blindly by token count whenever possible.
* Normalize repeated headers/footers and remove page artifacts early in the pipeline.
* Treat tables as first-class objects: keep columns and types instead of flattening to plain text.
* Validate with small end-to-end tests: ingest a representative sample, compute embeddings, and run retrieval queries to check quality.

## Conclusion

Ingestion is the foundation of reliable RAG systems. Converting presentation-oriented or noisy documents into structured, metadata-rich text enables meaningful chunking and high-quality embeddings. Combine layout-aware parsing, format-specific tools, and metadata-first chunking to maintain retrieval accuracy and trustworthy responses downstream.

In this course we’ll combine the tools and techniques above to build ingestion pipelines that produce clean text chunks enriched with metadata—improving embeddings and retrieval performance for RAG workloads.

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/6c0f08eb-0b91-48b6-af70-e95dbf30af15/lesson/83b386d8-edec-4737-b679-ac5900c21148)
