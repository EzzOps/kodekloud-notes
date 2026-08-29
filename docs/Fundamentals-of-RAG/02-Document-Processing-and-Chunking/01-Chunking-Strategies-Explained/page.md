# python
from pathlib import Path
from typing import List, Dict
from collections import defaultdict
import re

def read_text_files(root: Path) -> Dict[str, str]:
    """Return dict[file_name] = text"""
    files = {}
    for p in root.glob("*.txt"):
        files[p.name] = p.read_text(encoding="utf-8")
    return files

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> List[str]:
    """Split text into overlapping chunks of approx chunk_size characters."""
    chunks = []
    i = 0
    n = len(text)
    while i < n:
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def tokenize(s: str) -> List[str]:
    """Very small tokenizer for BM25 corpus building."""
    # lowercase, split on non-word characters
    return [t for t in re.split(r"\W+", s.lower()) if t]

def rrf_merge(list_a: List[str], list_b: List[str], k: int = 60, topn: int = 5) -> List[str]:
    """Reciprocal Rank Fusion for two ranked lists of IDs."""
    scores = defaultdict(float)
    for lst in (list_a, list_b):
        for rank, _id in enumerate(lst):
            scores[_id] += 1.0 / (k + rank + 1)
    return [x for x, _ in sorted(scores.items(), key=lambda kv: kv[1], reverse=True)][:topn]
```

CLI arguments (parser snippet)

* `k_each`: how many candidates to fetch from each retriever (BM25, vector).
* `final_k`: how many merged, deduplicated candidates to include in the LLM prompt.

```python theme={null}
# python
import argparse

sp = argparse.ArgumentParser()
sub = sp.add_subparsers(dest="cmd", required=True)

p_ing = sub.add_parser("ingest")
p_ing.add_argument("--dir", required=True, help="Folder or .txt file")
p_ing.add_argument("--embed-model", default="nomic-embed-text")

p_ask = sub.add_parser("ask")
p_ask.add_argument("--query", required=True)
p_ask.add_argument("--llm", default="llama3:latest")
p_ask.add_argument("--embed-model", default="nomic-embed-text")
p_ask.add_argument("--k-each", type=int, default=6)
p_ask.add_argument("--final-k", type=int, default=5)

args = sp.parse_args()
if args.cmd == "ingest":
    ingest(args.dir, embedding_model=args.embed_model)
else:
    ask(args.query, llm_model=args.llm, embedding_model=args.embed_model,
        k_each=args.k_each, final_k=args.final_k)
```

First queries and expected behavior

* Example corpus for these tests: two books — Adventures of Sherlock Holmes and Frankenstein.
* Test question: "Who is the narrator of this document?"

Run:

```bash theme={null}
# bash
python hybrid_rag.py ask --query "Who is the narrator of this document?"
```

Typical returned answer (example):

```plaintext theme={null}
=== Answer ===
The narrator of "The Adventures of Sherlock Holmes" appears to be someone who is friends with Sherlock Holmes, likely Dr. John Watson, as indicated by the text in chunk 324 where it says "I remember" and "you on one occasion, in the early days of our friendship". However, the name "Dr. John Watson" may not explicitly appear in every returned chunk.

In contrast, the narrator of "Frankenstein" is not clearly identified in the given chunk.

--- Sources ---
adventuresofsherlockholmes.txt (chunk 324)
frankenstein.txt (chunk 48)
...
```

Notes:

* If retrieval returns chunks from multiple books, that is expected for a mixed corpus. To isolate testing to a single book, reset the index and re-ingest only that book.

Resetting and re-ingesting
If you need to reset the vector index (for example ChromaDB), remove or reset the vector store directory and re-run ingestion to build a deterministic test set.

<Callout icon="warning">
  Be careful when removing your vector store directory (e.g., `rm -rf .chroma`) — this will delete the indexed embeddings and cannot be undone unless you have a backup.
</Callout>

Example commands:

```bash theme={null}
# bash: reset index (implementation-specific; this example removes the vector store directory)
rm -rf .chroma
python hybrid_rag.py ingest --dir data/  # re-ingest files in data/
```

After ingesting only Sherlock Holmes, re-run the same query and the system should be more consistent identifying Dr. Watson as the narrator.

Tuning knobs and examples
Use the following parameters to tune retrieval accuracy and LLM input quality.

| Parameter    | Purpose                                                                                             | Example / Suggested Change                        |
| ------------ | --------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| `chunk_size` | Approximate characters per chunk. Larger preserves more context.                                    | Increase from `800` → `1024` for broader context. |
| `overlap`    | Characters that overlap between adjacent chunks. Helps with boundary-context questions.             | Increase from `150` → `200`.                      |
| `k_each`     | Number of candidates fetched per retriever (BM25, vector). Higher → more recall.                    | `--k-each=10`                                     |
| `final_k`    | Number of merged candidates passed to the LLM after dedupe/rerank. Constrained by LLM token budget. | `--final-k=10`                                    |

1. Chunk size and overlap
   * Larger chunk size and more overlap preserve more contiguous context, improving answers for questions that require extended context (addresses, sequences, long descriptions).
   * Example change: set defaults to `chunk_size=1024` and `overlap=200`, then re-ingest.

```python theme={null}
# python
def chunk_text(text: str, chunk_size: int = 1024, overlap: int = 200) -> List[str]:
    ...
```

2. `k_each` and `final_k` (retrieval budget)
   * `k_each`: how many candidates to pull from each retriever (per-retriever).
   * `final_k`: number of merged candidates passed to the LLM after dedupe and rerank.
   * Example usage:

```bash theme={null}
# bash
python hybrid_rag.py ask --query "What is Holmes' address?" --k-each=10 --final-k=10
```

Observations and examples

* Query phrasing matters. Some phrasings produce concise, accurate answers; others need more context from retrieval.
  * Example: "Who lives on Baker Street?" often returns: "Sherlock Holmes lives on Baker Street, at 221B."
  * However, "What is Holmes' address?" may produce "I don't know." if the retrieved chunks lack the exact address context.
* Keyword searches can be very effective: searching for "221B" or "Irene Adler" often returns precise chunks.

Example:

```bash theme={null}
# bash
python hybrid_rag.py ask --query "Who does Irene Adler marry?" --k-each=12 --final-k=10

=== Answer ===
Irene Adler marries Godfrey Norton, an English lawyer.

=== Sources ===
adventuresofsherlockholmes.txt (chunk 28)
adventuresofsherlockholmes.txt (chunk 36)
...
```

Testing for hallucination

* Intentionally ask questions that are not covered by the corpus to verify the system returns "I don't know" (or a safe decline) instead of inventing facts.
* Example queries:
  * "What is Holmes' mother's maiden name?"
  * "Which smartphone did Holmes prefer?"

Best practices:

* Ensure your prompt explicitly instructs the LLM: "Do not make assumptions. If the answer is not supported by the provided sources, respond: 'I don't know.'"
* When the system hallucinates, revisit:
  * Retrieval quality (chunking and overlap)
  * Score thresholds and reranking logic
  * Prompt engineering (explicit refusal instructions)
  * Increasing `final_k` (balance against token budgets)

Example:

```bash theme={null}
# bash
python hybrid_rag.py ask --query "What is Holmes' mother's maiden name?"
# => I don't know.
```

Testing strategies and checklist

* Sanity checks: ask questions with known answers from the corpus.
* Hallucination checks: ask questions that are outside the corpus.
* Rephrase checks: ask the same question with different phrasing to test semantic search robustness.
* Isolate tests: re-ingest a single document for deterministic behavior.
* Systematic tuning: change one parameter at a time (chunk size, then `k_each`, then `final_k`) and record results.
* Track compute: increasing `k_each` and `final_k` raises recall but also uses more compute and tokens.

Practical tip

<Callout icon="lightbulb">
  When tuning, change one parameter at a time (e.g., chunk size, then `k_each`, then `final_k`) and re-run a fixed set of test queries so you can measure the effect of each change.
</Callout>

Summary

* Testing a RAG system is iterative: tune chunking, retrieval budgets, and reranking while validating results with curated test queries.
* Use deterministic checks (keyword-based queries) plus open-ended checks (possible hallucination prompts).
* Add clear refusal instructions in your prompt so the LLM avoids unsupported inferences.
* Maintain a fixed suite of positive and negative test queries to measure improvement over time.

Further reading and references

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Reciprocal Rank Fusion (RRF) — Original Paper](https://trec.nist.gov/pubs/trec13/papers/miura_rf.pdf)

Thanks for following this lesson. Use the accompanying code and sample data to experiment and share results with the KodeKloud community.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/d536d16b-ddcc-4d4a-bbdb-477dda1c4d34/lesson/f8a3a23c-f430-4064-855e-3ddea857cbd4" />
</CardGroup>


# Chunking Strategies Explained

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Document-Processing-and-Chunking/Chunking-Strategies-Explained/page

Guidance on text chunking strategies for efficient LLM ingestion and retrieval in RAG systems

This guide covers how to prepare text for LLM ingestion by comparing chunking techniques, explaining why chunking matters, and showing how to pick the best approach for retrieval-augmented generation (RAG) systems.

Why chunk at all?

LLMs have finite context windows (commonly \~4k to \~128k tokens depending on the model). Entire knowledge bases or very long documents rarely fit into one prompt. Even when they do, large documents slow retrieval and dilute relevant signals with noise, making it harder for the model to find the right context.

Practical benefits of chunking:

* Respect model context limits (tokens).
* Speed up retrieval and ranking (smaller units are faster to search).
* Reduce noise and improve recall by limiting irrelevant text inside any one context window.

Anatomy of a "good" chunk

A chunk is a tradeoff: small enough to be searchable and to fit in your target context window, but large enough to preserve semantic meaning. There’s no universal “perfect” chunk — only the right choice for your use case.

A strong chunk usually exhibits:

* Coherence: self-contained and semantically complete where possible (avoid cutting mid-sentence or mid-thought).
* Appropriate size: fits your target token limit while retaining required concepts.
* Overlap: intentional overlap with adjacent chunks (commonly \~10–20% or 1–2 sentences) so multi-sentence concepts don’t disappear across boundaries.
* Natural boundaries: prefer paragraph, heading, code block, or section boundaries when available.
* Provenance metadata: include source, document id, section/title, page number, timestamps, etc., so retrieved chunks can be traced to their origin.

<Frame>
  <img alt="The image depicts the &#x22;Anatomy of a Perfect Chunk,&#x22; highlighting four elements: Coherence, Size (Tokens), Overlap, and Natural Boundaries, with brief descriptions for each." />
</Frame>

Typical chunk sizes by use case

| Use case                                  | Typical chunk size (tokens) | Notes                                                    |
| ----------------------------------------- | --------------------------: | -------------------------------------------------------- |
| Q\&A / retrieval                          |                     256–512 | Good for short factual lookups and fast ranking.         |
| Summarization / single-document synthesis |                       1k–4k | Larger chunks preserve longer context for summarization. |
| Long documents / book-scale               |                      512–1k | Combine chunking with retrieval or multi-hop approaches. |

Always pick sizes informed by your model’s context window and retrieval needs. Use the same tokenizer as your model to measure token counts accurately.

Core chunking strategies

1. Fixed-size chunking

* What it is: Split text into fixed N-character or N-token chunks, optionally with a fixed overlap.
* When to use: Quick ingestion pipelines, or when document structure is unavailable and speed/predictability is critical.
* Pros: Simple, predictable, and fast to compute.
* Cons: Semantically blind — may break sentences and reduce coherence.

Example (fixed-size chunking with overlap):

```python theme={null}
chunk_size = 1000  # characters or tokens depending on your splitter
overlap = 100
chunks = split_fixed(text, chunk_size, overlap)
```

<Frame>
  <img alt="The image is a slide discussing the advantages and disadvantages of a core strategy called &#x22;Fixed-Size Chunking.&#x22; Advantages include simplicity and fast processing, while disadvantages include destroying coherence and high risk of breaking sentences mid-word." />
</Frame>

2. Context-aware splits (paragraph / sentence splitting)

* What it is: Use natural textual delimiters — paragraphs, sentences, and line breaks — to create chunks.
* Pros: Preserves linguistic boundaries and improves coherence compared to fixed-size splits. Easy to implement with standard NLP tools.
* Cons: Chunk sizes vary; long paragraphs may still exceed token limits and require further splitting.

Best practices:

* Combine paragraph/sentence splitting with a tokenizer check to ensure chunks fit your token budget.
* Apply small overlaps (1–2 sentences) to prevent loss of cross-boundary context.

<Frame>
  <img alt="The image illustrates a core strategy for context-aware text splitting using natural delimiters, highlighting different methods: raw text, paragraph split, and sentence split." />
</Frame>

<Frame>
  <img alt="The image contrasts the advantages and disadvantages of &#x22;Context-Aware Splits&#x22; in a core strategy, highlighting better coherence, respecting linguistic boundaries, and variable chunk sizes." />
</Frame>

3. Recursive split (recommended default)

* What it is: Multi-pass splitting that preserves the largest natural units first and only splits deeper when chunks exceed size constraints.
* Typical pass order: headings/sections → paragraphs → lines → sentences → words.
* Why use it: Balances coherence and size constraints by adapting to document structure and avoiding blind truncation.
* When to use: Default for most RAG pipelines — a strong choice for \~80% of use cases.

Conceptual recursive splitting flow:

* Try to split by paragraph/section boundaries.
* If a chunk still exceeds token limits, split by line breaks.
* If still too large, split into sentences.
* As a last resort, split by words or fixed token slices.

<Frame>
  <img alt="The image outlines a &#x22;Recursive Split&#x22; strategy with four methods: splitting by paragraphs, lines, sentences, and words. It describes steps to manage text chunk sizes using line and paragraph breaks, and sentence boundaries." />
</Frame>

4. Header / Markdown splitting

* What it is: Use document structure (Markdown H1/H2/H3, or other structured headings) to keep headings and their content together.
* Pros: Excellent for technical docs, API references, and knowledge bases — preserves hierarchy and section context.
* Cons: Fails on unstructured prose and depends on well-formatted source documents.

When working with Markdown knowledge bases, prefer header-based splitting first and then apply recursive or sentence-level splitting inside large sections.

5. Semantic / topic-shift splitting (advanced)

* What it is: Use embeddings to detect semantic similarity and place boundaries where similarity drops below a threshold.
* Process:
  1. Embed sentences or small units (e.g., with SentenceTransformers).
  2. Compute cosine similarities between adjacent embeddings.
  3. Insert a chunk boundary when similarity falls under a tuned threshold that indicates a topic shift.
* Pros: Produces highly coherent, concept-aligned chunks — ideal for long content with shifting themes.
* Cons: Computationally expensive and sensitive to embedding-model quality and threshold tuning.

Recommended resources:

* SentenceTransformers: [https://www.sbert.net/](https://www.sbert.net/)

<Frame>
  <img alt="The image is a slide titled &#x22;Core Strategy: Advanced Splitting Techniques,&#x22; showing a comparison of advantages and disadvantages of the technique, highlighting semantic coherence and natural topic boundaries as advantages, and computational expense and slower processing as disadvantages." />
</Frame>

Choosing the right strategy

A practical workflow:

1. Analyze your sources — are they structured (reports, Markdown) or unstructured (books, articles)?
2. Default to recursive splitting — it provides a strong balance of coherence, size control, and simplicity.
3. Build a ground-truth question set (queries with expected answers) and measure retrieval recall against top-k results.
4. If recursive splitting underperforms:
   * Use header/Markdown splitting for structured documents, or
   * Use semantic/topic-shift splitting for long content with frequent theme changes.
5. Consider hybrid approaches, e.g., header splitting to isolate sections, then recursive or semantic splitting inside each section.

Testing and metrics

Create representative queries with known answers and evaluate:

* Retrieval recall: do the top-k retrieved chunks contain the correct evidence?
* Answer quality: does the LLM produce useful answers when given retrieved context?

Design metrics tolerant of paraphrase and semantic variation rather than requiring exact string matches. RAG systems are not fully deterministic — measure recall first, then end-to-end answer quality under your prompt and LLM configuration.

<Callout icon="lightbulb">
  Measure retrieval and end-to-end answer quality using a ground-truth dataset. Start with recall-focused tests (does the correct chunk appear in top-k?) and then measure final answer quality with your prompt/LLM setup.
</Callout>

<Callout icon="warning">
  Always use the tokenizer that matches your embedding/model to measure token counts accurately. Token counting mismatches are a common source of overflow and unexpected behavior.
</Callout>

Key takeaways

* Chunking is fundamental to RAG pipelines — poor chunking propagates errors downstream.
* No single best strategy fits every document — choose based on document structure, query patterns, and compute constraints.
* Start with recursive splitting as a default. It’s simple, fast, and effective for most cases.
* For long or thematically shifting content, consider semantic splitting (with higher compute cost) or hybrid strategies.
* Always test: build ground-truth queries, measure retrieval performance and answer quality, and iterate.

<Frame>
  <img alt="The image outlines key takeaways about document processing strategies, emphasizing the importance of chunking, using tailored strategies, starting with recursive methods, and upgrading to semantic splitting when possible." />
</Frame>

Further reading and references

* RAG patterns and best practices: [https://platform.openai.com/docs/guides/retrieval](https://platform.openai.com/docs/guides/retrieval)
* SentenceTransformers (semantic splitting): [https://www.sbert.net/](https://www.sbert.net/)
* Tokenizers and byte-pair encoding: [https://huggingface.co/docs/tokenizers/usage](https://huggingface.co/docs/tokenizers/usage)
* Evaluation guidance for RAG: experiment with recall/top-k and end-to-end answer scoring; consider fuzzy matching and semantic similarity metrics.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/6c0f08eb-0b91-48b6-af70-e95dbf30af15/lesson/a8b6d648-cf3a-469d-af6a-015c5cdb9326" />
</CardGroup>
