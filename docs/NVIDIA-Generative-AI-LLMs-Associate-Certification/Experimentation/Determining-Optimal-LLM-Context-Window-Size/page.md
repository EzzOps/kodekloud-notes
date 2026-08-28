# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

text = "The quick brown fox jumps over the lazy dog"
inputs = tokenizer(text, return_tensors="pt")

# Forward pass with attentions enabled
outputs = model(**inputs, output_attentions=True)
# outputs.attentions is a tuple of length num_layers, each tensor of shape (batch, num_heads, seq_len, seq_len)
attentions = outputs.attentions

# Select the last layer and the first batch, then average across heads
last_layer = attentions[-1][0]             # shape: (num_heads, seq_len, seq_len)
avg_attn = last_layer.mean(dim=0).detach().cpu().numpy()  # shape: (seq_len, seq_len)

# Convert token ids to readable tokens
tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

# Plot heat map
plt.figure(figsize=(10, 8))
sns.heatmap(avg_attn, xticklabels=tokens, yticklabels=tokens, cmap="viridis", cbar_kws={"label": "Attention weight"})
plt.xlabel("Key / Source tokens")
plt.ylabel("Query / Target tokens")
plt.title("Average attention (last layer, averaged across heads)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
```

Interpretation tips

* Rows represent queries (the token receiving attention); columns represent keys (tokens being attended to).
* Brighter (or more intense) colors denote larger attention weights.
* A focused attention pattern (strong peaks) indicates the model is concentrating on particular tokens; diffuse patterns indicate distributed attention.
* Compare heads and layers to see how attention patterns evolve across the network; compute summary stats (e.g., entropy per query) to quantify concentration.
* Use attention visualizations alongside other interpretability tools (e.g., integrated gradients, ablation studies) to form more robust explanations.

<Callout icon="lightbulb">
  When comparing heads or layers, plot multiple heat maps side-by-side (one per head or per layer) or compute summary statistics (for example, entropy per query) to quantify how concentrated attention is. Interactive viewers (e.g., Plotly) help explore long sequences and multiple heads.
</Callout>

<Callout icon="warning">
  Attention weights are informative but are not a guaranteed causal explanation of model decisions. Interpret attention visualizations cautiously and corroborate findings with additional interpretability methods.
</Callout>

<Frame>
  <img alt="The image shows a heat map illustrating the attention weights in transformer models, specifically detailing the relationships between input and output tokens. It also includes a text explanation of how heat maps visualize attention distribution." />
</Frame>

Links and references

* [Hugging Face Transformers documentation](https://huggingface.co/docs/transformers)
* [seaborn: statistical data visualization](https://seaborn.pydata.org/)
* [matplotlib: plotting library for Python](https://matplotlib.org/)
* Attention interpretation resources: Vaswani et al., "Attention is All You Need" and follow-up interpretability work on transformer explanations

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/b8ad33c7-78ce-4828-a30c-4a8fc01d1781/lesson/e6c5cc72-8812-4eec-b74d-47135bc561fd" />
</CardGroup>


# Determining Optimal LLM Context Window Size

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-[SECRET_REDACTED]-Optimal-LLM-Context-Window-Size/page

Guidelines for experimentally determining the optimal LLM context window by systematically testing varied window sizes and measuring model and system metrics to balance performance, latency, memory, and cost.

Question 5.

A data scientist is conducting an experiment to determine the optimal context window size for a specific LLM application.

Which approach would provide the most reliable results?

* Testing a single, extremely large context window?
* Systematically testing incremental window sizes and measuring performance metrics?
* Using the default context window recommended by the model documentation.
* Asking users which context window they prefer?

Answer: Systematically testing incremental window sizes and measuring performance metrics.

<Callout icon="lightbulb">
  The most reliable method is a controlled, systematic experiment across multiple context window sizes, measuring both model performance and system/resource metrics. This reveals performance trends and practical trade-offs (accuracy, latency, memory, cost), rather than relying on a single data point or subjective preference.
</Callout>

Why this approach works

* Direct comparison: Changing only the context window isolates its effect on the task.
* Quantitative trade-offs: You can observe where performance gains plateau while resource costs keep rising.
* Reproducibility: Using consistent prompts, tokenization, and seeds reduces variance and supports statistically valid conclusions.
* Practicality: Allows you to combine model capability with operational constraints (latency, memory, and cost) to select the best real-world configuration.

Recommended experimental process

1. Define scope
   * Specify task(s): e.g., summarization, question answering, code generation.
   * Select datasets and clear evaluation splits (train/validation/test).
   * Choose metrics: accuracy, F1, exact match, perplexity, latency, peak GPU/CPU memory, and inference cost.

2. Select window sizes to test
   * Pick a range that covers typical and extreme cases (e.g., 512, 1,024, 2,048, 4,096 tokens), up to the model’s supported limit.

3. Ensure experimental consistency
   * Use identical prompt templates, preprocessing, tokenization, and random seeds across runs.
   * Repeat runs to quantify variance.

4. Measure and record both model and system metrics
   * Model metrics: accuracy, F1, BLEU, ROUGE, perplexity, recall for long-range dependencies.
   * System metrics: latency (p99/p95), throughput (tokens/sec), peak and average memory usage, and cost per inference.

5. Analyze results
   * Plot performance vs. window size and resource usage vs. window size to identify inflection points and diminishing returns.
   * Use statistical tests or confidence intervals to validate observed differences.

6. Consider hybrid or alternative approaches
   * Retrieval-augmented prompting (store and fetch relevant context).
   * Chunking + summarization (divide long context and compress).
   * Streaming/recurrence mechanisms or stateful architectures.
   * Compare any hybrid method against single-window baselines.

Table: Metrics and their purpose

| Metric category             | What it indicates                          | Example                     |
| --------------------------- | ------------------------------------------ | --------------------------- |
| Accuracy / F1 / Exact Match | Task performance & correctness             | `F1 = 0.82`                 |
| Perplexity                  | Model fluency & fit for generative tasks   | Lower is better             |
| Latency / Throughput        | User-facing responsiveness and scalability | `p95 latency = 120ms`       |
| Memory usage                | Feasibility for deployment hardware        | `peak GPU mem = 12GB`       |
| Cost                        | Economic impact at scale                   | `cost per 1k requests = $X` |

Practical tips and pitfalls

* Don’t assume “bigger is always better.” Large windows can improve recall but often increase latency, memory usage, and cost disproportionately.
* Use validation splits and repeated trials to mitigate noisy measurements.
* If long contexts are necessary but expensive, evaluate hybrid solutions (retrieval, summarization, chunking) as first-class options.

<Callout icon="warning">
  Avoid making decisions based on a single run, purely model-documented defaults, or user preference alone. Those approaches miss the trade-offs that matter in production (latency, memory, and cost). Always validate experimentally for your specific task and deployment constraints.
</Callout>

The diagram below summarizes the recommended, systematic testing workflow and why it yields more reliable, actionable results than single-point or purely opinion-based choices.

<Frame>
  <img alt="The image features a question about determining the optimal context window size for an LLM application, with the answer suggesting a systematic approach of testing incremental window sizes and measuring performance metrics." />
</Frame>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/44b444b3-19d6-4856-95a6-a46628fb2cf0/lesson/5b9d0f98-c154-480c-b223-e496f43e11bd" />
</CardGroup>
