# pdf_parser.py
from typing import List, Dict, Any
from pathlib import Path
import json
import PyPDF2
from langchain.text_splitters import RecursiveCharacterTextSplitter


class PDFParser:
    """Parse PDF files and prepare them for RAG ingestion."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the PDF parser.

        Args:
            chunk_size: Maximum size of each text chunk in characters.
            chunk_overlap: Number of characters to overlap between chunks.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # separators chosen to prefer paragraph/sentence boundaries, then fallback to spaces
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract all selectable text from a PDF file.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            Extracted text as a single string.

        Raises:
            FileNotFoundError: If the PDF file doesn't exist.
            Exception: If there's an error reading the PDF.
        """
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        text_parts: List[str] = []
        try:
            with open(pdf_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                num_pages = len(reader.pages)
                for i in range(num_pages):
                    page = reader.pages[i]
                    # extract_text() may return None for some pages; guard it
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
        except Exception as e:
            raise Exception(f"Error reading PDF: {e}")

        # Join pages with double newline to preserve some structure
        return "\n\n".join(text_parts).strip()

    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into chunks suitable for RAG ingestion.

        Args:
            text: The text to chunk.

        Returns:
            List of text chunks.
        """
        if not text:
            return []
        return self.text_splitter.split_text(text)

    def parse_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Parse a PDF and return chunked text with metadata.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            List of dictionaries containing chunk text and metadata.
        """
        text = self.extract_text_from_pdf(pdf_path)
        chunks = self.chunk_text(text)

        results: List[Dict[str, Any]] = []
        total_chunks = len(chunks)
        for idx, chunk in enumerate(chunks):
            results.append({
                "chunk_id": idx,
                "text": chunk,
                "source": str(Path(pdf_path).resolve()),
                "chunk_size": len(chunk),
                "total_chunks": total_chunks,
            })
        return results

    def parse_pdf_to_file(self, pdf_path: str, output_path: str) -> None:
        """
        Parse a PDF and save the chunked results to a text file for inspection.

        Args:
            pdf_path: Path to the PDF file.
            output_path: Path to write the output text file.
        """
        results = self.parse_pdf(pdf_path)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("PDF Parser Results\n")
            f.write(f"Source: {pdf_path}\n")
            f.write(f"Total Chunks: {len(results)}\n")
            f.write("-" * 80 + "\n\n")

            for result in results:
                f.write(f"Chunk {result['chunk_id'] + 1}/{result['total_chunks']}\n")
                f.write(f"Size: {result['chunk_size']} characters\n")
                f.write("-" * 80 + "\n")
                f.write(result["text"].strip() + "\n\n")
                f.write("=" * 80 + "\n\n")
```

Key design notes:

* The parser raises a clear `FileNotFoundError` if the PDF path is invalid.
* `PyPDF2.PdfReader().pages[i].extract_text()` can return `None` for pages — these are skipped to avoid errors.
* The text splitter prioritizes paragraph and sentence boundaries before falling back to spaces, producing readable chunks for embeddings.
* For scanned/image-only PDFs, add OCR beforehand (see the warning below).

Table — PDFParser public methods

| Method                                     | Purpose                                                             | Returns                  |
| ------------------------------------------ | ------------------------------------------------------------------- | ------------------------ |
| `extract_text_from_pdf(pdf_path)`          | Extract selectable text from PDF pages                              | `str` (joined page text) |
| `chunk_text(text)`                         | Split a long text string into RAG-friendly chunks                   | `List[str]`              |
| `parse_pdf(pdf_path)`                      | Full pipeline: extract, chunk, and return metadata-enhanced results | `List[Dict[str, Any]]`   |
| `parse_pdf_to_file(pdf_path, output_path)` | Save a human-readable dump of chunks to a text file                 | `None` (writes file)     |

***

## main.py — examples and usage

Create `main.py` to demonstrate typical usage of the `PDFParser`. This script shows:

* parsing and printing a summary,
* saving chunked results to JSON for downstream ingestion,
* writing a human-readable text dump,
* comparing chunking parameter impacts on chunk count.

Save as `main.py`.

```python theme={null}
# main.py
from pdf_parser import PDFParser
import json
from pathlib import Path


def main():
    # Path to your sample PDF
    pdf_path = "sample.pdf"  # <-- replace with your PDF path

    parser = PDFParser(chunk_size=1000, chunk_overlap=200)

    print("Example 1: Parsing PDF to structured data")
    print("-" * 80)

    try:
        results = parser.parse_pdf(pdf_path)
        print(f"Successfully parsed: {pdf_path}")
        print(f"Total chunks created: {len(results)}")
        if results:
            print("\nFirst chunk preview:")
            print(results[0]["text"][:200] + "...")
        # Save structured chunks to JSON for RAG ingestion
        with open("chunks.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print("\nChunks saved to: chunks.json")
    except FileNotFoundError:
        print(f"Error: PDF file '{pdf_path}' not found. Please update the path variable.")
    except Exception as e:
        print(f"Error processing PDF: {e}")

    print("\n" + "=" * 80 + "\n")

    print("Example 2: Parsing PDF to text file")
    print("-" * 80)
    try:
        parser.parse_pdf_to_file(pdf_path, "output.txt")
        print("Chunks saved to: output.txt")
    except FileNotFoundError:
        print(f"Error: PDF file '{pdf_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")

    print("\n" + "=" * 80 + "\n")

    print("Example 3: Custom chunking parameters")
    print("-" * 80)
    # Smaller chunks (more pieces)
    small_parser = PDFParser(chunk_size=500, chunk_overlap=100)
    try:
        small_results = small_parser.parse_pdf(pdf_path)
        print(f"Chunks with size=500: {len(small_results)}")
    except Exception:
        print("Skipping small chunk example due to missing or unreadable PDF file")

    # Larger chunks (more context per chunk)
    large_parser = PDFParser(chunk_size=2000, chunk_overlap=400)
    try:
        large_results = large_parser.parse_pdf(pdf_path)
        print(f"Chunks with size=2000: {len(large_results)}")
    except Exception:
        print("Skipping large chunk example due to missing or unreadable PDF file")


if __name__ == "__main__":
    main()
```

***

## Sample terminal output (cleaned)

This is an example of the console output when running `python main.py` with a small sample PDF that produces 3 chunks.

```plaintext theme={null}
Example 1: Parsing PDF to structured data
--------------------------------------------------------------------------------
Successfully parsed: sample.pdf
Total chunks created: 3

First chunk preview:
The Fable of Fiona the Fussy Feline  Fiona, a tuxedo cat of considerable fluff and questionable temper, believed the world revolved entirely around the timely provision of tuna in springwater, not brin...

Chunks saved to: chunks.json
================================================================================

Example 2: Parsing PDF to text file
--------------------------------------------------------------------------------
Chunks saved to: output.txt
================================================================================

Example 3: Custom chunking parameters
--------------------------------------------------------------------------------
Chunks with size=500: 7
Chunks with size=2000: 2
```

***

## Final notes

* This parser processes selectable text only. For scanned PDFs you must run OCR before parsing.
* Tune `chunk_size` and `chunk_overlap` for your model/embedding limits — smaller chunks increase recall but reduce context; larger chunks increase context but consume more embedding tokens.
* The `chunks.json` file is ready to be embedded and stored in your vector DB for RAG use cases.

> **warning** If a PDF contains no selectable text (for example, scanned pages), PyPDF2 will not extract the content. In that case, perform OCR (Tesseract + pytesseract or a cloud OCR service) to produce text before using this parser. Consider adding an automatic OCR fallback for production pipelines.

If you want to extend this parser, consider:

* Adding page-level metadata (page numbers, section headings if extractable).
* Detecting image-only pages and automatically running OCR.
* Integrating directly with an embeddings pipeline (e.g., to automatically insert chunks into a vector store).

Links and References

* [PyPDF2 on PyPI](https://pypi.org/project/PyPDF2/)
* [LangChain text splitters](https://docs.langchain.com/docs/modules/data_connection/text_splitters)
* [Tesseract OCR project](https://github.com/tesseract-ocr/tesseract)
* [pytesseract on PyPI](https://pypi.org/project/pytesseract/)

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/6c0f08eb-0b91-48b6-af70-e95dbf30af15/lesson/d960d02f-a547-476c-abb6-aff916ffee6e)


# Demo Ingesting Text

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Document-Processing-and-Chunking/Demo-Ingesting-Text/page

Guide to building a Python UTF-8 text parser that chunks documents with sentence-aware overlap and attaches metadata for retrieval-augmented generation pipelines

This lesson walks through building a production-ready text file parser in Python designed for retrieval-augmented generation (RAG) pipelines. You'll learn how to:

* Parse UTF-8 text files and extract stable metadata.
* Split content into semantically coherent, overlapping chunks.
* Preserve context across chunk boundaries to improve embeddings and retrieval.

We implement a `TextDocumentParser` class that:

* reads UTF-8 text files,
* generates a stable document ID,
* chunks text preferring sentence breaks and falling back to word boundaries,
* attaches source metadata to every chunk for provenance.

> **lightbulb** We use UTF-8 for broad character support and Python's `pathlib` for robust path handling. Effective chunking yields better embeddings; preserving context across boundaries improves retrieval quality.

## Why good chunking matters

* Sentence-aware chunking produces semantically coherent chunks which yield higher-quality embeddings.
* Overlap between chunks keeps context across boundaries, increasing retrieval relevance.
* Document-level metadata attached to chunks enables provenance, filtering, and better display for retrieved results.

## Implementation overview

The implementation below provides a single, cohesive `TextDocumentParser` class with the following responsibilities:

* `parse_file(file_path)`: read a UTF-8 file and produce content + metadata.
* `_generate_doc_id(file_path)`: produce a stable document ID (MD5 of absolute path).
* `chunk_text(text)`: split text into overlapping chunks, preferring sentence boundaries and falling back to whitespace.
* `process_document(file_path)`: run the full pipeline and attach metadata to each chunk.

Key configurable parameters:

| Parameter       | Description                                                                                 | Example |
| --------------- | ------------------------------------------------------------------------------------------- | ------- |
| `chunk_size`    | Approximate max number of characters per chunk. Tune for your embedding model token limits. | `1000`  |
| `chunk_overlap` | Number of characters to overlap between consecutive chunks to preserve context.             | `200`   |

Reference links:

* [UTF-8 (Unicode) — Overview](https://en.wikipedia.org/wiki/UTF-8)
* [pathlib — Python Docs](https://docs.python.org/3/library/pathlib.html)
* [Retrieval-Augmented Generation (RAG) — Introduction](https://huggingface.co/blog/rag)

## Production-ready parser (full code)

```python theme={null}
