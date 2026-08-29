# Effective Chunking Strategy for RAG Systems

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-Certification/Software-Development/Effective-Chunking-Strategy-for-RAG-Systems/page

Evaluating chunking strategies for RAG systems and recommending semantic unit splitting with overlap to preserve context and maximize retrieval relevance.

In this lesson we evaluate common chunking strategies used in Retrieval-Augmented Generation (RAG) systems and recommend the most effective approach for preserving context while maximizing retrieval relevance. We'll compare popular methods, explain their trade-offs, and provide practical, model-aware recommendations you can apply to real-world pipelines.

## Common chunking strategies

* Splitting text by fixed character count
* Splitting text by fixed token count
* Splitting text by semantic units with overlap (recommended)
* Random chunking to increase diversity

## Recommended approach: semantic units with overlap

Splitting by semantic units (sentences, paragraphs, or logical sections) and adding controlled overlap preserves natural context and meaning. Chunks aligned with semantic boundaries are more coherent for both embedding models and LLM retrieval. Overlap helps prevent information loss when a concept crosses a chunk boundary and improves recall during retrieval.

<Frame>
  <img alt="The image presents a question about the most effective chunking strategy for a RAG system, highlighting &#x22;splitting text by semantic units with overlap&#x22; as the answer. A brief explanation follows, stating that this method preserves natural context and prevents information loss." />
</Frame>

## Why other strategies fall short

| Strategy                  |                                    When it fails | Key issues                                                                                       |
| ------------------------- | -----------------------------------------------: | ------------------------------------------------------------------------------------------------ |
| Fixed-character splitting |                        Any natural language text | Cuts words/sentences arbitrarily; produces incoherent chunks that reduce embedding quality       |
| Fixed-token splitting     | Better than fixed-character, but still imperfect | Requires exact tokenizer match; can split sentences/logical units in unnatural places            |
| Random chunking           |                    For primary retrieval indices | Increases diversity but breaks coherence; lowers precision — can be useful only for augmentation |

### Additional notes on token-based splitting

* Token-aware splitting is preferable to raw character counts because embeddings and LLMs operate on tokens. However, tokenization must match the embedding/LLM tokenizer to avoid mismatches.
* Use the embedding model’s tokenizer (for example, `tiktoken`) to compute token lengths before embedding or truncation.

## Practical recommendations

* Chunk unit
  * Prefer semantic boundaries: sentences, paragraphs, or logical sections.
  * Preserve special content (code blocks, tables, lists) as single chunks when possible to keep structure intact.
* Chunk size
  * Tune to your embedding model and LLM context window. A common target is a few hundred tokens per chunk (e.g., 200–500 tokens), adjusted for your model and document types.
* Overlap
  * Use overlap to cover boundary-spanning concepts. Typical overlap options:
    * Sentence-based: 1–3 sentences
    * Proportional: 10–20% of the chunk
    * Token-based: 50–100 tokens as a pragmatic starting point
* Token accounting
  * Use the embedding model’s tokenizer to measure tokens. Example: [tiktoken on GitHub](https://github.com/openai/tiktoken).
* Metadata
  * Store source identifiers, position offsets, and structural metadata so retrieved chunks can be traced and reassembled.
* Deduplication and normalization
  * Remove near-duplicates to avoid redundant retrievals, but keep intended overlapping chunks since overlaps are deliberate for context continuity.

### Quick reference: chunking guidelines by document type

| Document type                 | Suggested chunk unit                 |                Chunk size (tokens) |                       Typical overlap |
| ----------------------------- | ------------------------------------ | ---------------------------------: | ------------------------------------: |
| Short articles / blog posts   | Paragraphs or sentence groups        |                            150–300 |               10–20% or 1–2 sentences |
| Long technical docs / manuals | Sections → paragraphs (hierarchical) |        300–600 per paragraph chunk |               10–20% or 50–100 tokens |
| Code-heavy documents          | Keep code blocks whole               | Varies; ensure block fits in chunk |  Minimal; avoid splitting code blocks |
| Streaming/real-time           | Sliding window with semantic fence   |                    Small (100–300) | Sliding overlap (e.g., 50–100 tokens) |

## Example: sentence-based chunking with overlap (Python)

Below is a simple, production-friendly function that splits a list of sentences into overlapping chunks. The function uses sentence counts for chunk size and overlap, which is easy to reason about and map back to semantic boundaries. Before embedding, convert chunk text to tokens using your model tokenizer to ensure chunk token budgets are respected.

```python theme={null}
from typing import List

def chunk_sentences(sentences: List[str], chunk_size: int, overlap: int) -> List[str]:
    """
    Split a list of sentences into overlapping chunks.
    - chunk_size and overlap are in number of sentences.
    - Returns a list of chunk strings where sentences are joined with a space.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")

    chunks: List[str] = []
    i = 0
    step = max(1, chunk_size - overlap)
    while i < len(sentences):
        chunk = sentences[i : i + chunk_size]
        chunks.append(" ".join(chunk))
        if i + chunk_size >= len(sentences):
            break
        i += step
    return chunks
