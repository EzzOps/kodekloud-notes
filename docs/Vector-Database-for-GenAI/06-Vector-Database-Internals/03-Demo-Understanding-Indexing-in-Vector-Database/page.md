# Demo Understanding Indexing in Vector Database

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Database-Internals/Demo-Understanding-Indexing-in-Vector-Database/page

Hands-on demo showing how a simple three-bucket index in a vector database reduces distance computations versus brute-force linear search.

Welcome back. In this hands-on demo you'll see how indexing changes the behavior and efficiency of search in a vector database. We'll compare a brute-force linear scan with a very small toy index and count how many distance checks each approach performs.

<Frame>
  <img alt="The image features the text &#x22;Understanding indexing in vector DB&#x22; on a white background, with the word &#x22;Demo&#x22; highlighted in white against a blue shape on the right." />
</Frame>

What you'll run (environment)

* This demo is intended for a [Jupyter notebook](https://jupyter.org) but works in any Python REPL.
* Key goals:
  * Build a tiny deterministic embedding function (no ML).
  * Store embeddings (optionally) in ChromaDB.
  * Compare a linear (brute-force) search vs. a pruned (indexed) search.
  * Measure and compare the number of distance computations.

Quick plan (steps)

| Step | Description                                 | Example file                              |
| ---- | ------------------------------------------- | ----------------------------------------- |
| 1    | Minimal environment imports                 | `demo_setup.py`                           |
| 2    | Create dataset and deterministic embedder   | `data_and_embed.py`                       |
| 3    | (Optional) Upsert vectors into ChromaDB     | `store_in_chroma.py`                      |
| 4    | Linear (brute-force) search and measurement | `linear_search.py`                        |
| 5    | Build a toy index (3 buckets)               | `build_index.py`                          |
| 6    | Indexed (pruned) search and comparison      | `indexed_search.py`, `compare_results.py` |

Code and explanations follow. Each code block is labeled to help reproducibility.

```python theme={null}
