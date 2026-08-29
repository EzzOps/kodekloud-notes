# main.py
import csv
import json
from pathlib import Path
from typing import List, Dict, Optional

def parse_csv_for_rag(csv_file_path: str, output_file_path: Optional[str] = None) -> List[Dict]:
    """
    Parse a CSV file into a list of documents suitable for RAG ingestion.
    Each document contains:
      - id: a generated id (doc_{row_index})
      - text: a concatenated text representation of non-empty fields
      - metadata: includes source, row_number, and the original CSV fields
    """
    documents: List[Dict] = []

    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames or []
            print(f"Found columns: {fieldnames}")

            for idx, row in enumerate(reader):
                # Build a readable text representation from non-empty fields
                text_parts = []
                for key, value in row.items():
                    if value is not None:
                        value_str = value.strip()
                        if value_str:
                            text_parts.append(f"{key}: {value_str}")

                text = " | ".join(text_parts)

                # Copy row fields into metadata (preserve as strings)
                row_metadata = {k: (v if v is not None else "") for k, v in row.items()}

                document = {
                    "id": f"doc_{idx}",
                    "text": text,
                    "metadata": {
                        "source": str(csv_file_path),
                        "row_number": idx,
                        **row_metadata
                    }
                }

                documents.append(document)

    except FileNotFoundError:
        print(f"Error: {csv_file_path} not found!")
        return []
    except Exception as e:
        print(f"Error reading {csv_file_path}: {e}")
        return []

    print(f"Processed {len(documents)} documents")

    # Optionally save to JSON file
    if output_file_path:
        try:
            with open(output_file_path, 'w', encoding='utf-8') as outfile:
                json.dump(documents, outfile, indent=2, ensure_ascii=False)
            print(f"Saved documents to {output_file_path}")
        except Exception as e:
            print(f"Error writing {output_file_path}: {e}")

    return documents


def main():
    # Input and output file paths (adjust as needed)
    csv_file = "sample_data.csv"
    output_file = "rag_documents.json"

    if not Path(csv_file).exists():
        print(f"Error: {csv_file} not found!")
        return

    documents = parse_csv_for_rag(csv_file, output_file)

    if documents:
        # Print a sample document and the total number of chunks
        print("\nSample document:")
        print(json.dumps(documents[0], indent=2, ensure_ascii=False))
        total = len(documents)
        print(f"\nTotal Chunks: {total}")


if __name__ == "__main__":
    main()
```

## Document schema (what each parsed item contains)

| Field      | Type   | Description                                                                   | Example                                                                               |                     |       |
| ---------- | ------ | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------- | ----- |
| `id`       | string | Generated identifier for the document (`doc_{row_index}`)                     | `doc_0`                                                                               |                     |       |
| `text`     | string | Human-readable concatenation of non-empty `key: value` pairs                  | \`id: 1                                                                               | first\_name: Victor | ...\` |
| `metadata` | object | Contains `source`, `row_number`, and all original CSV fields as string values | `{ "source": "sample_data.csv", "row_number": 0, "id": "1", "first_name": "Victor" }` |                     |       |

## How the parser works (summary)

* Uses [`csv.DictReader`](https://docs.python.org/3/library/csv.html#csv.DictReader) to map header names to values per row.
* For each row:
  * Builds a `text` string by concatenating non-empty `key: value` pairs separated by `|` for easy searchability.
  * Copies all original CSV fields into `metadata` (preserving string values).
  * Adds `source` and `row_number` to `metadata`.
  * Generates a top-level document `id` using the `doc_{row_index}` pattern.
* Appends each document to a list and optionally writes the full list to a JSON file for ingestion.

## Run the script

Place your CSV (for example, `sample_data.csv`) in the same directory as `main.py`. Then run:

```bash theme={null}
python main.py
```

On success you should see the columns found, the processed document count, and a sample output. Example console output:

```plaintext theme={null}
Found columns: ['id', 'first_name', 'last_name', 'email', 'ip_address', 'favorite_animal']
Processed 1000 documents
Saved documents to rag_documents.json

Sample document:
{
  "id": "doc_0",
  "text": "id: 1 | first_name: Victor | last_name: Heliet | email: vheliet@pagesperso-orange.fr | ip_address: 225.97.9.194 | favorite_animal: Panthera leo persica",
  "metadata": {
    "source": "sample_data.csv",
    "row_number": 0,
    "id": "1",
    "first_name": "Victor",
    "last_name": "Heliet",
    "email": "vheliet@pagesperso-orange.fr",
    "ip_address": "225.97.9.194",
    "favorite_animal": "Panthera leo persica"
  }
}

Total Chunks: 1000
```

## Notes, tips, and next steps

* One CSV row maps to one RAG "chunk" (document). If you need different chunking strategies (e.g., split long text fields or combine rows), update `parse_csv_for_rag` accordingly.
* Header names are used as-is. Normalize column names (trim whitespace, lower-case, replace spaces) if you have inconsistent sources.
* The script generates a top-level `id` and will also include any `id` column from the CSV inside `metadata`. Avoid naming collisions if your downstream store expects a single unique id.
* For larger CSVs (tens of thousands of rows), consider streaming rows and writing documents incrementally (or sending them directly to your vector store) to avoid high memory use.
* After generating `rag_documents.json`, ingest it into your vector database/retriever using the connector or ingestion script supported by your vector store.

> **warning** If your CSV contains nested JSON, fields with embedded commas, or multi-line values, ensure fields are properly quoted. For complex inputs, use a robust CSV library or preprocessor that properly handles quoting, escaping, and multi-line fields to avoid corrupted records.

## Links and references

* [Python csv.DictReader documentation](https://docs.python.org/3/library/csv.html#csv.DictReader)
* [Vector database fundamentals (for ingestion)](https://learn.kodekloud.com/user/courses/vector-database-for-genai)
* [RAG fundamentals course](https://learn.kodekloud.com/user/courses/fundamentals-of-rag)

This parser offers a straightforward, reproducible method to convert tabular CSV data into RAG-ready documents with both human-readable text and full metadata preservation.

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/6c0f08eb-0b91-48b6-af70-e95dbf30af15/lesson/b43b295f-1cd0-4ed3-9a53-1f80a924a850)


# Demo Ingesting Docx

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Document-Processing-and-Chunking/Demo-Ingesting-Docx/page

A tutorial showing how to parse DOCX files in Python, chunk text preserving paragraph and sentence boundaries, and prepare chunks with metadata for RAG embedding workflows

This lesson continues the document ingestion series for retrieval-augmented generation (RAG) systems and focuses on parsing Microsoft Word DOCX files with Python. We’ll build a robust DOCX ingestion pipeline that:

* extracts text and core metadata from DOCX files,
* splits large documents into intelligent, overlapping chunks suitable for embedding,
* preserves paragraph and sentence boundaries when possible to improve retrieval quality for downstream LLM usage.

What you'll get

* A minimal, production-friendly `DocxParser` implementation (parsing, chunking, and orchestration).
* A chunking strategy that prefers paragraph and sentence boundaries, with word-boundary fallback.
* A small example script to run and inspect chunks before embedding into a vector store.

Contents

* Setup
* Quick note about files
* Imports and the core class (complete code you can save as `main.py`)
* How the parser works (summary)
* Output example and next steps
* Links and references

Setup

Run these commands to create a Python virtual environment and install the DOCX parsing dependency:

```bash theme={null}
