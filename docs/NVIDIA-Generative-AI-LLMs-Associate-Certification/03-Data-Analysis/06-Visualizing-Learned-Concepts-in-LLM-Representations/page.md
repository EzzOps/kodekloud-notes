# Visualizing Learned Concepts in LLM Representations

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-Certification/Data-Analysis/Visualizing-Learned-Concepts-in-LLM-Representations/page

Guidance on using UMAP and t-SNE to visualize semantic clusters in LLM embedding spaces.

Question 5.

When analyzing the output of a transformer-based language model, which technique would be most effective for visualizing the relationship between different concepts in the model's learned representations?

Options: [t-SNE](https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html) or [UMAP](https://umap-learn.readthedocs.io/en/latest/) dimensionality reduction, bar charts of token frequencies, time series analysis, or cumulative distribution functions?

Answer: [t-SNE](https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html) or [UMAP](https://umap-learn.readthedocs.io/en/latest/) dimensionality reduction.

These nonlinear dimensionality-reduction techniques are the most effective ways to visualize relationships between concepts in high-dimensional embedding spaces. They project high-dimensional token or sentence embeddings into 2D or 3D while preserving neighborhood (local) relationships, enabling inspection of semantic similarity, clustering, and concept separation.

<Callout icon="lightbulb">
  Use [UMAP](https://umap-learn.readthedocs.io/en/latest/) or [t-SNE](https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html) to explore semantic clusters in embedding spaces. For exploratory visualization, UMAP is typically faster and preserves more global structure; t-SNE often produces clearer local clusters but can be slower and requires careful tuning of perplexity.
</Callout>

Why t-SNE / UMAP are preferred over the other listed options

* Bar charts of token frequencies: show token counts and distributional properties of the corpus, but do not capture geometric relationships in embedding space.
* Time series analysis: suited to temporal trends and sequence behavior, not spatial neighborhood structure in vector embeddings.
* Cumulative distribution functions (CDFs): summarize similarity-score distributions, but cannot reveal cluster topology or neighborhood relationships.

Comparison table

| Technique   |                                  What it reveals | Best use case                                                      |
| ----------- | -----------------------------------------------: | ------------------------------------------------------------------ |
| t-SNE       |  Local neighborhood structure and tight clusters | Small-to-moderate embedding sets where local clustering is primary |
| UMAP        |   Local + more global structure, faster at scale | Exploratory visualization of larger embedding sets; good default   |
| Bar charts  |                    Token frequency distributions | Corpus analysis and preprocessing checks                           |
| Time series |                       Temporal trends in metrics | Sequence/temporal model diagnostics                                |
| CDFs        | Distribution summaries (e.g., similarity scores) | Statistical summaries and threshold selection                      |

Practical recommendations

* Preprocess embeddings: standard scale and optionally apply PCA (e.g., to 50 dims) before UMAP/t-SNE to speed computation and reduce noise.
* Choose the right tool:
  * UMAP: usually the default—faster, scales well, preserves more global relationships.
  * t-SNE: useful when you need very clear local clusters; requires careful hyperparameter tuning.
* Reproducibility: set random seeds—both UMAP and t-SNE are stochastic.
* Visual cues: color points by label, token type, cluster assignment, or model-derived scores (e.g., attention weight or prediction confidence) to make semantic structure obvious.

Example workflow (high-level)

1. Compute or load embeddings (one vector per token/sentence).
2. Optionally apply PCA to reduce to \~50 dimensions.
3. Fit UMAP or t-SNE to 2D/3D.
4. Plot with colors/markers reflecting labels or cluster assignments.

Example: PCA + UMAP

```python theme={null}
import numpy as np
from sklearn.decomposition import PCA
import umap
import matplotlib.pyplot as plt
