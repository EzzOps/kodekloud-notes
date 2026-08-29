# Demo Setting up a Vector Database

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Introduction-to-Vector-Databases-and-Generative-AI/Demo-Setting-up-a-Vector-Database/page

Guide to running Qdrant locally with Docker and Jupyter, using Python client to create collections, insert embeddings, and perform basic vector similarity queries.

Welcome! This walkthrough demonstrates how simple it is to run a vector database locally using Qdrant and connect to it from a Jupyter Notebook with the official Python client. We'll cover a minimal local setup (Docker), a ready-to-run container image that bundles Qdrant + Jupyter, and example Python snippets to create collections, insert embeddings, and run basic queries.

This guide is ideal for developers experimenting with embeddings, similarity search, or building retrieval-augmented generation (RAG) prototypes.

## Quick overview

* Start a Qdrant instance locally (Docker).
* Connect from a Jupyter Notebook using `qdrant-client`.
* Create a collection, upsert sample points (vectors + payload), and run simple retrieval/inspection APIs.

## Prerequisites

| Requirement      | Purpose / Notes                                                            |
| ---------------- | -------------------------------------------------------------------------- |
| Docker           | Run the Qdrant container locally.                                          |
| Python + Jupyter | Run the notebook locally, or use the included image which bundles Jupyter. |
| `qdrant-client`  | Official Python client for Qdrant (install via `requirements.txt`).        |

## Connect from a Jupyter Notebook

The simplest import and connection looks like this:

```python theme={null}
from qdrant_client import QdrantClient
import os

qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
client = QdrantClient(url=qdrant_url)
print(f"Client created for: {qdrant_url}")
```

This creates a client for the default local Qdrant HTTP endpoint (`http://localhost:6333`) or uses a `QDRANT_URL` environment variable if provided.

## Requirements (notebook / container)

Add at minimum the following to your `requirements.txt`:

```text theme={null}
qdrant-client
notebook
jupyterlab
```

You can extend this list with your favorite embedding libraries (Transformers, sentence-transformers, OpenAI client, etc.) depending on how you generate embeddings.

## Container image (Dockerfile)

This demo uses a Docker image that pulls the official Qdrant image and prepares a workspace with Python and Jupyter. Use this concise Dockerfile:

```dockerfile theme={null}
FROM qdrant/qdrant:latest

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /workspace/requirements.txt
RUN python3 -m venv /workspace/venv && \
    /workspace/venv/bin/pip install --no-cache-dir -r /workspace/requirements.txt

COPY setup_and_connection.ipynb /workspace/setup_and_connection.ipynb
COPY start.sh /workspace/start.sh
RUN chmod +x /workspace/start.sh

EXPOSE 6333 6334 8888

CMD ["/workspace/start.sh"]
```

## Build and run (local)

Build and run the container locally:

```bash theme={null}
docker build -t qdrant-demo .
docker run -p 6333:6333 -p 6334:6334 -p 8888:8888 --name qdrant-demo qdrant-demo
```

Qdrant exposes its HTTP API on port `6333` by default; `6334` is for gRPC. Jupyter (if used) typically runs on port `8888`.

| Port   | Service                                      |
| ------ | -------------------------------------------- |
| `6333` | Qdrant HTTP API                              |
| `6334` | Qdrant gRPC                                  |
| `8888` | Jupyter Notebook / Lab (if present in image) |

> **lightbulb** You can manage Qdrant via its dashboard (HTTP) or entirely through the Python client — the UI is mostly for administrative convenience.

## Verify connection from the notebook

After starting Qdrant, run the connection cell in your notebook. Example (same as above to verify connectivity):

```python theme={null}
from qdrant_client import QdrantClient
import os

qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
client = QdrantClient(url=qdrant_url)
print(f"Client created for: {qdrant_url}")
```

## List collections (showing collections like tables in an RDBMS)

Programmatically list collections to confirm connectivity and inspect existing collections:

```python theme={null}
collections_response = client.get_collections()
print("Connection established.")
print("Collections:", collections_response.collections)
```

## Open the Qdrant dashboard from the notebook (optional)

Display a link to the dashboard inside a Jupyter environment:

```python theme={null}
from IPython.display import display, Markdown

dashboard_url = "http://localhost:6333"
display(Markdown(f"Open Qdrant Dashboard: [{dashboard_url}]({dashboard_url})"))
```

## Create or recreate a collection

Define a collection to store vectors and recreate it (note: this deletes an existing collection with the same name before creating a new one). Use `VectorParams` to set the vector dimensionality and distance metric:

```python theme={null}
from qdrant_client.models import Distance, VectorParams

client.recreate_collection(
    collection_name="demo_collection",
    vectors_config=VectorParams(size=4, distance=Distance.COSINE),
)
print("Recreated collection: demo_collection")
```

> **warning** `recreate_collection` will delete an existing collection with the same name. Use with caution in production environments to avoid accidental data loss.

## Insert points (vectors + payload)

Insert a few sample vectors (called points) along with payload metadata:

```python theme={null}
from qdrant_client.models import PointStruct

client.upsert(
    collection_name="demo_collection",
    points=[
        PointStruct(id=1, vector=[0.1, 0.2, 0.3, 0.4], payload={"topic": "setup"}),
        PointStruct(id=2, vector=[0.2, 0.1, 0.4, 0.3], payload={"topic": "connection"}),
        PointStruct(id=3, vector=[0.9, 0.8, 0.7, 0.6], payload={"topic": "demo"}),
    ],
)
print("Inserted 3 points into demo_collection.")
```

## Inspect stored points

For small datasets, the scroll API is a convenient way to retrieve stored points:

```python theme={null}
result = client.scroll(collection_name="demo_collection", limit=5, with_payload=True)
print(result)
```

## What is a vector?

A vector is a list of numeric values (floats) representing an embedding for a piece of data (text, image, etc.). The vector dimensionality must match the `size` specified in `VectorParams`. Vector similarity search (nearest-neighbor search) is based on distance metrics such as cosine or euclidean.

## Next steps / Common workflows

Once embeddings are stored in the vector database, typical next steps include:

* Running nearest-neighbor similarity searches with `client.search` or `client.search_with_payload`.
* Integrating into a RAG pipeline: store document embeddings and retrieve relevant passages at query time.
* Combining metadata filtering with vector search for more precise retrieval.
* Packaging the notebook or application as a Docker image and deploying to Kubernetes for production.

Examples of other vector databases you may consider:

* Qdrant (this lesson)
* ChromaDB
* LanceDB
* Pinecone
* Weaviate

## References and further reading

* Qdrant: [https://qdrant.tech/](https://qdrant.tech/)
* qdrant-client (Python): [https://github.com/qdrant/qdrant-client](https://github.com/qdrant/qdrant-client)
* Jupyter: [https://jupyter.org/](https://jupyter.org/)
* Docker: [https://www.docker.com/](https://www.docker.com/)
* Kubernetes basics: [https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

Thanks for following along — see you in the next lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/841f0a59-96ec-4dc1-b84f-b577ab5a5bb7/lesson/85b55938-7e31-4c8d-a8b5-1d174bdd93b4)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/841f0a59-96ec-4dc1-b84f-b577ab5a5bb7/lesson/bf207774-c2d0-4a88-863d-b36c9186398d)
