# Python Library for Semantic Similarity Calculation LLM Eval

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-Certification/Software-Development/Python-Library-for-Semantic-Similarity-Calculation-LLM-Eval/page

Recommending Sentence Transformers for computing semantic similarity between LLM outputs and references, with example code, interpretation, and comparisons to NumPy, pandas, and Matplotlib.

Question 9.

When implementing a Python script to evaluate LLM outputs, which library would be most useful for calculating semantic similarity between generated and referenced texts? NumPy, Sentence Transformers, Matplotlib, or pandas?

The answer: [Sentence Transformers](https://www.sbert.net/).

<Frame>
  <img alt="The image contains a multiple-choice question regarding the most useful Python library for calculating semantic similarity between generated and reference texts, with the answer highlighted as &#x22;sentence-transformers.&#x22; It includes an explanation of why that library is most suitable." />
</Frame>

Why Sentence Transformers for LLM evaluation?

* Sentence Transformers (the `sentence-transformers` library) is built to produce dense sentence and text embeddings that capture semantic meaning, not just lexical overlap.
* Embeddings let you compare generated and reference texts by meaning using similarity metrics (commonly cosine similarity), which is essential for evaluating LLM outputs where many valid phrasings exist.
* Pretrained models are available in sizes that trade off speed and accuracy, enabling both low-latency inference and higher-fidelity comparisons.

Minimal example: compute semantic similarity with Sentence Transformers

```python theme={null}
from sentence_transformers import SentenceTransformer, util
