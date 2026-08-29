# setup_and_preview.py
from pathlib import Path
import os
from PIL import Image
import matplotlib.pyplot as plt

# 1. Setup paths
BASE_DIR = Path.cwd()
IMAGE_DIR = BASE_DIR / "images"
DB_PATH = str(BASE_DIR / "lancedb_images")

# 2. Find and preview images
image_paths = list(IMAGE_DIR.glob("*.png")) + list(IMAGE_DIR.glob("*.jpg"))
print(f"Found {len(image_paths)} images at: {IMAGE_DIR}")

fig, axes = plt.subplots(1, len(image_paths), figsize=(15, 5))
for i, p in enumerate(image_paths):
    axes[i].imshow(Image.open(p))
    axes[i].axis("off")
plt.show()
```

How this works

* `image_paths` gathers all PNG and JPG files in the `images` folder.
* We preview each image with `matplotlib` to confirm the dataset before embedding.

Embedding images and storing vectors in LanceDB

* Load a CLIP-based model (`clip-ViT-B-32`) via `sentence-transformers`.
* Convert each image to an embedding vector.
* Store the vector along with the image path in LanceDB for future retrieval.

<Callout icon="lightbulb">
  Loading the CLIP model may take some time the first time because the pretrained weights are downloaded. Expect a minute or two depending on your connection and environment.
</Callout>

Before running the code below, note that it removes an existing database at `DB_PATH` (if present) and creates a fresh LanceDB instance.

<Callout icon="warning">
  The script below deletes any existing LanceDB at the configured `DB_PATH`. Back up data if you need to preserve a previous index.
</Callout>

```python theme={null}
# embed_and_store.py
import shutil
import lancedb
from sentence_transformers import SentenceTransformer
import numpy as np
from pathlib import Path
from PIL import Image

# Load the CLIP ViT-B-32 model (image+text)
model = SentenceTransformer("clip-ViT-B-32")
print("Model loaded successfully!")

# Load images and generate embeddings
print("Generating embeddings...")
images = [Image.open(p).convert("RGB") for p in image_paths]  # ensure consistent mode
vectors = model.encode(images)  # returns a numpy array with shape (n_images, dim)
print(f"Generated {len(vectors)} vectors with {vectors.shape[1]} dimensions each.")

# Prepare data for LanceDB
data = [
    {"path": str(p), "vector": v.tolist()}
    for p, v in zip(image_paths, vectors)
]

# Remove existing DB (if any) and create a fresh LanceDB
if os.path.exists(DB_PATH):
    shutil.rmtree(DB_PATH)

db = lancedb.connect(DB_PATH)
table = db.create_table("images", data=data)
print("Knowledge base ready for search!")
```

Notes on the code

* We call `model.encode(images)` with PIL images—sentence-transformers handles conversion for CLIP models.
* Each record stored in LanceDB contains the `path` (for later loading/display) and the `vector`.

Text-to-image search function

* Encode a text query using the same CLIP model so text and images live in the same embedding space.
* Query the LanceDB table for nearest neighbors and visualize the result(s).

```python theme={null}
# search_by_text.py
from pathlib import Path
import matplotlib.pyplot as plt
from PIL import Image

def search_by_text(query, limit=1):
    # Embed the text query
    query_vector = model.encode([query])[0]

    # Search the database for the closest match(es)
    results = table.search(query_vector).limit(limit).to_pandas()

    # Display each match
    for _, row in results.iterrows():
        img = Image.open(row["path"])
        plt.imshow(img)
        plt.title(
            f"Query: '{query}'\nMatch: {Path(row['path']).name} (Distance: {row['_distance']:.4f})"
        )
        plt.axis("off")
        plt.show()
```

Example queries

* Run these sample searches in the notebook to see text-to-image retrieval:

```python theme={null}
# Example queries
search_by_text("a photo of a cat")
search_by_text("a photo of a dog running")
search_by_text("a photo of a dog sitting")
```

Behavior and tips

* Query phrasing affects retrieval quality. Adding descriptive context (e.g., "running", "sitting") can help find the correct image when the attribute is present.
* Very short or ambiguous queries (e.g., "dog") may return a different image if its embedding is closer in vector space.

Visual example

<Frame>
  <img alt="The image shows a computer interface with a query for &#x22;a photo of a dog sitting,&#x22; but a photo of a cat sitting is displayed instead. A summary below explains the use of CLIP and LanceDB for image and text vector mapping and searching." />
</Frame>

Summary

* We used a CLIP-based model (via `sentence-transformers`) to compute embeddings for images and text so they share a joint embedding space.
* Image vectors and metadata (image paths) were stored in LanceDB and searched via nearest-neighbor queries.
* Query phrasing and level of descriptive detail influence retrieval results; refine queries to improve accuracy.

Further reading and references

* LanceDB: [https://www.lancedb.ai/](https://www.lancedb.ai/)
* sentence-transformers (CLIP models): [https://www.sbert.net/](https://www.sbert.net/)
* CLIP (OpenAI): [https://github.com/openai/CLIP](https://github.com/openai/CLIP)
* Jupyter: [https://jupyter.org/](https://jupyter.org/)

Troubleshooting

* If embeddings take a long time to generate, ensure GPU support is enabled and that the `sentence-transformers` model can access the internet to download weights.
* If the search returns unexpected images, try more descriptive queries or inspect pairwise distances in the returned DataFrame to understand which images are nearest in embedding space.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/47c71900-9efe-47e3-ac4c-502d14eafd06/lesson/07f3b28d-96de-440d-b8df-e31168048037" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/47c71900-9efe-47e3-ac4c-502d14eafd06/lesson/4cdce043-f06d-48a4-b9f4-3eb6c0f79bfc" />
</CardGroup>


# Demo Text Embedding with sentence transformer

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/From-Data-to-Vectors-The-Embedding-Layer/Demo-Text-Embedding-with-sentence-transformer/page

Hands-on tutorial converting a Markdown policy into SentenceTransformer embeddings, storing vectors in LanceDB, and performing semantic search with code examples and chunking strategies.

Welcome — in this hands-on demo we'll convert a Markdown policy document into vector embeddings using a SentenceTransformer, store them in LanceDB (an open-source vector database), and run semantic search over the document. All code runs in a Jupyter notebook; the examples below show the essential code, explanations, and sample outputs so you can reproduce the workflow.

Table of contents

* 1. Imports and prerequisites
* 2. Load the policy document
* 3. Chunk the document by headings
* 4. Load the embedding model
* 5. Encode chunks and store in LanceDB
* 6. Define search utilities
* 7. Example queries
* 8. Notes on behavior and limitations
* 9. Wrap-up and resources

## 1) Imports and prerequisites

Install dependencies (example):

```bash theme={null}
pip install sentence-transformers lancedb pandas numpy
```

Then import the Python modules required for file handling, text processing, embeddings, and the vector DB:

```python theme={null}
import os
import re
from pathlib import Path

import lancedb
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
```

Helpful links:

* SentenceTransformers: [https://www.sbert.net/](https://www.sbert.net/)
* LanceDB: [https://lancedb.ai/](https://lancedb.ai/)

Below is a short table of the key libraries used in this tutorial.

| Resource                | Purpose                          | Example / Link                            |
| ----------------------- | -------------------------------- | ----------------------------------------- |
| `sentence-transformers` | Convert text to dense embeddings | `SentenceTransformer("all-MiniLM-L6-v2")` |
| `lancedb`               | Store and query vectors locally  | `lancedb.connect(DB_PATH)`                |
| `pandas`, `numpy`       | Data manipulation & numeric ops  | -                                         |

## 2) Load the policy document

Load the Markdown file (here: `kodekloud_airlines_policy.md`) and print a short preview to confirm successful load.

```python theme={null}
BASE_DIR = Path.cwd()
POLICY_PATH = BASE_DIR / "kodekloud_airlines_policy.md"

policy_text = POLICY_PATH.read_text(encoding="utf-8")
print(f"Loaded policy: {POLICY_PATH.name}")
print(f"Characters: {len(policy_text):,}")

print("\n--- Preview (first 400 chars) ---\n")
print(policy_text[:400])
```

This policy includes sections for baggage, ticket changes and cancellations, pets, check-in, boarding, and more. We'll create semantic chunks from these sections and embed them.

<Frame>
  <img alt="The image shows a code or document editor with a file open displaying airline policies, including sections on baggage, ticket changes, and boarding information. The interface includes a file explorer on the left, showing other files and their modification times." />
</Frame>

## 3) Chunk the document

Embedding an entire long document at once reduces retrieval granularity. The recommended approach is to split into semantic chunks (for example, by headings) and embed each chunk independently.

The following `chunk_by_headings` function groups content by top-level headings (`#`, `##`, `###`) and discards very short buffers. It returns a list of dictionaries with `section` and `text` keys.

```python theme={null}
def chunk_by_headings(md: str) -> list[dict]:
    """
    Split markdown text into chunks grouped by the most recent heading.
    - Headings: lines starting with '#', '##', or '###'.
    - Ignore very short chunks.
    """
    lines = md.splitlines()
    chunks = []
    current_section = "(start)"
    buffer_lines = []

    def flush_buffer():
        text = "\n".join(buffer_lines).strip()
        if len(text) >= 60:
            chunks.append({"section": current_section, "text": text})

    for line in lines:
        heading_match = re.match(r'^(#{1,3})\s+(.*)', line)
        if heading_match:
            # Flush previous buffer
            flush_buffer()
            buffer_lines = []
            current_section = heading_match.group(2).strip()
        else:
            buffer_lines.append(line)

    # Flush the final buffer
    flush_buffer()
    return chunks
```

Run the chunker and inspect the first few chunks:

```python theme={null}
chunks = chunk_by_headings(policy_text)
print("Number of chunks:", len(chunks))
for i, c in enumerate(chunks[:5], 1):
    print(f"Chunk {i} section: {c['section']}; chars: {len(c['text'])}")
```

## 4) Load the embedding model

We use the `all-MiniLM-L6-v2` SentenceTransformer (compact, high-quality for semantic search). If you pull from the Hugging Face Hub frequently, consider setting `HF_TOKEN` as an environment variable to avoid unauthenticated rate limits.

<Callout icon="lightbulb">
  If you see warnings about unauthenticated Hugging Face Hub requests, set a `HF_TOKEN` environment variable to increase rate limits and speed up downloads.
</Callout>

Load the model and encode a test string:

```python theme={null}
MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

example = "What is the cabin baggage limit?"
v = model.encode(example)
print("Model:", MODEL_NAME)
print("Vector shape:", v.shape)
print("Vector preview:", np.array2string(v[:10], precision=3))
```

Example console output (actual numbers may differ):

```plaintext theme={null}
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
BertModel LOAD REPORT from: sentence-transformers/all-MiniLM-L6-v2
Model: all-MiniLM-L6-v2
Vector shape: (384,)
Vector preview: [ 0.063 -0.030 -0.080  0.035  0.013  0.002  0.059  0.028 -0.015  0.032]
```

## 5) Encode chunks and store in LanceDB

Create (or recreate) a local LanceDB store, encode each chunk into a normalized embedding vector, and store rows with `section`, `text`, and `vector` fields.

```python theme={null}
DB_PATH = str(BASE_DIR / "lancedb_kodekloud_airline")
TABLE_NAME = "policy_chunks"
