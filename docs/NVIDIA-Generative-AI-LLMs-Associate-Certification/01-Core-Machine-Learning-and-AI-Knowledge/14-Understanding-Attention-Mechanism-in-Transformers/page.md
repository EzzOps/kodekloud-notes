# Understanding Attention Mechanism in Transformers

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-Certification/Core-Machine-Learning-and-AI-Knowledge/Understanding-Attention-Mechanism-in-Transformers/page

Explains attention in transformers, showing how queries keys and values compute learned weights so models focus on relevant tokens for each prediction.

Question 9.

Which of the following best describes the concept of attention as used in transformer-based LLMs?

* A mechanism that randomly selects important words in a sequence?
* A mechanism that weighs the importance of different parts of the input sequence?
* A filter that removes stop words from the input sequence?
* Attention, a technique that extends the context window of the model.

Correct answer: A mechanism that weighs the importance of different parts of the input sequence.

In transformer-based LLMs, attention assigns learned weights to different tokens in the input so the model can focus on the most relevant pieces of context when producing each output token. This is a dynamic, per-token weighting process — not a random selection, stop-word filter, or a context-window extender.

<Frame>
  <img alt="The image displays a question about the concept of &#x22;attention&#x22; in transformer-based LLMs, alongside an explanation describing it as a mechanism that weights the importance of different parts of the input sequence." />
</Frame>

Why attention matters (concise)

* Attention enables each output token to “look at” the entire input sequence and assign higher influence to relevant tokens for that particular prediction.
* This allows transformers to capture long-range dependencies and contextual relationships without relying on recurrence.

Illustrative example
Imagine the sentence:
"The cat was chased by the dog that ran up the tree."

When predicting the next token after "chased", the model gives more weight to tokens such as "cat", "dog", "chased", and "ran" than to function words like "the" or "by". Those higher weights indicate stronger relevance for the specific prediction.

How attention is computed (high-level)

1. Each token position has Query (Q), Key (K), and Value (V) vectors (produced by learned linear projections).
2. For a given query, compute similarity scores with all keys (dot products).
3. Scale the scores (typically by sqrt(d\_k)), then apply softmax to obtain attention weights.
4. Use the weights to compute a weighted sum of the values — that becomes the attention output for the query position.

Simplified pseudocode for scaled dot-product attention:

```python theme={null}
