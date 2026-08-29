# X: numpy array of shape (n_samples, n_features) containing embeddings
# 1) PCA preprocessing to speed up and denoise (optional but recommended)
pca = PCA(n_components=50, random_state=42)
X_pca = pca.fit_transform(X)

# 2) UMAP projection to 2D
reducer = umap.UMAP(n_components=2, n_neighbors=15, min_dist=0.1, random_state=42)
X_umap = reducer.fit_transform(X_pca)

# 3) Plot
plt.figure(figsize=(8, 6))
scatter = plt.scatter(X_umap[:, 0], X_umap[:, 1], c=labels, cmap="Spectral", s=5)
plt.title("UMAP projection of embeddings")
plt.xlabel("UMAP 1")
plt.ylabel("UMAP 2")
plt.colorbar(scatter, label="label")
plt.show()
```

Example: PCA + t-SNE

```python theme={null}
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# 1) PCA to 50 dims
pca = PCA(n_components=50, random_state=42)
X_pca = pca.fit_transform(X)

# 2) t-SNE projection to 2D
tsne = TSNE(n_components=2, perplexity=30, learning_rate=200, n_iter=1000, random_state=42)
X_tsne = tsne.fit_transform(X_pca)

# 3) Plot
plt.figure(figsize=(8, 6))
scatter = plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=labels, cmap="Spectral", s=5)
plt.title("t-SNE projection of embeddings")
plt.xlabel("t-SNE 1")
plt.ylabel("t-SNE 2")
plt.colorbar(scatter, label="label")
plt.show()
```

Hyperparameter tips

* t-SNE:
  * `perplexity`: typically 5–50. Smaller values emphasize very local structure; larger values reveal broader groupings.
  * `learning_rate`: often between 100 and 1000.
  * `n_iter`: at least 500–1000; more iterations can improve stability.
* UMAP:
  * `n_neighbors`: controls local vs. global structure (small → very local, large → more global). Typical values: 5–50.
  * `min_dist`: controls how tightly points are packed (lower → tighter clusters).

Interpretation guidance

* Look for coherent clusters where semantically similar tokens/sentences are near each other.
* Use colors/markers for known labels (e.g., POS tags, concept labels, or predicted classes) to validate semantic separation.
* Beware of over-interpreting absolute distances—UMAP/t-SNE emphasize relative neighborhood relationships, not exact metric preservation.
* Validate clusters quantitatively (e.g., silhouette score, cluster purity) rather than relying solely on visual appearance.

> **warning** t-SNE and UMAP are stochastic. To ensure reproducibility and comparability, set `random_state`/seed, log hyperparameters (e.g., `perplexity`, `n_neighbors`, `min_dist`), and, when appropriate, run multiple seeds to check stability.

Summary

* For visualizing relationships between concepts in LLM learned representations, prefer UMAP or t-SNE, with UMAP as a practical default for exploratory work and larger datasets.
* Combine dimensionality reduction with preprocessing (PCA), color/annotate points by labels or scores, and validate findings with quantitative metrics.

Links and references

* [UMAP documentation](https://umap-learn.readthedocs.io/en/latest/)
* [t-SNE (scikit-learn)](https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html)
* [PCA (scikit-learn)](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/b8ad33c7-78ce-4828-a30c-4a8fc01d1781/lesson/21e82dab-3f67-4258-8dfc-d42f13a42249)


# Visualizing Transformer Attention Weights

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-Certification/Data-Analysis/Visualizing-Transformer-Attention-Weights/page

Guide to visualizing transformer attention weights using heat maps with explanations, plotting tips, and example code

Question 2.

When visualizing attention weights from a transformer-based LLM, which of the following visualization techniques would be most effective?

A bar chart, a line graph, heat map, or scatter plot?

Answer: heat maps.

Heat maps are the most effective visualization technique for attention weights in Transformer models because they present a 2D matrix where color intensity encodes attention strength between tokens. This layout directly maps the relationship between query (target/output) tokens and key (source/input) tokens, making it easy to see which input tokens the model attends to when producing each output token.

Why heat maps work well

* Axes correspond naturally to token positions: one axis for queries (output tokens) and one for keys/values (input tokens).
* Color intensity conveys magnitude (attention weight) at a glance.
* They scale well to full sequence matrices and can visualize per-head or aggregated attention.
* You can add token labels and annotations to link attention patterns to actual text.

Advantages summary

| Benefit                      | Why it helps                                                                |
| ---------------------------- | --------------------------------------------------------------------------- |
| Natural 2D mapping           | Rows = queries, columns = keys, matching the attention matrix layout        |
| Immediate magnitude cues     | Color intensity encodes attention weight without extra encoding             |
| Per-head and per-layer views | Enables fine-grained analysis of how different heads/layers focus attention |
| Annotatable                  | Token labels, groupings, and interactive zoom make patterns interpretable   |

Practical notes when plotting attention heat maps

* Transformer attentions are softmax-normalized per query: values usually sum to 1 across keys for each query.
* Visualize a single head, average across heads, or show multiple heads in a grid of heat maps to capture different granularities.
* Distinguish self-attention (within a sequence) from cross-attention (encoder-decoder models) when labeling axes.
* For long sequences, aggregate tokens (e.g., by sentence or span), use hierarchical clustering, or provide interactive zoom to maintain readability.
* Consider normalizing, clipping, or using a perceptually-uniform colormap (e.g., `viridis`) for consistent interpretation.

Example: plotting an average attention heat map (Hugging Face Transformers + seaborn)

```python theme={null}
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import seaborn as sns
import matplotlib.pyplot as plt
