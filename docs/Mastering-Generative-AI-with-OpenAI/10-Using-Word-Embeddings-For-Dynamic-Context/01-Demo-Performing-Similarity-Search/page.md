# Use the tokenizer corresponding to the model you will call
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

msg = "If it is 9AM in London, what time is it in Hyderabad. Be concise."

# Encode the message into token IDs
tokens = encoding.encode(msg)
print(tokens)

# Number of tokens
print(len(tokens))

# Decode back to text
print(encoding.decode(tokens))
```

Interactive example (output may vary with encoding version):

```python theme={null}
In [1]: import tiktoken

In [2]: encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

In [3]: msg = "If it is 9AM in London, what time is it in Hyderabad. Be concise."

In [4]: tokens = encoding.encode(msg)
In [5]: tokens
Out[5]: [2746, 433, 374, 220, 24, 1428, 304, 7295, 11, 1148, 892, 374, 433, 304, 69547, 13, 2893, 64694, 13]

In [6]: len(tokens)
Out[6]: 19

In [7]: print(encoding.decode(tokens))
If it is 9AM in London, what time is it in Hyderabad. Be concise.
```

This shows the round trip: text → token IDs → text, and the token count.

## Context windows and token limits

Each model has a maximum context length (context window), measured in tokens. The context window includes both input tokens (your prompt) and output tokens (the model’s completion). When planning requests, add prompt tokens + expected output tokens and ensure they stay within the model’s context limit.

| Topic          | Guidance                                                                                               |
| -------------- | ------------------------------------------------------------------------------------------------------ |
| Context length | Varies by model (e.g., historically \~4,097 tokens for some models).                                   |
| Planning       | If your prompt consumes N tokens and the context limit is L, then available completion tokens ≈ L − N. |
| Strategy       | For large inputs, split text across multiple calls (chaining) or summarize to fit the window.          |

Example: if the model’s limit is 4,097 tokens and your prompt uses 3,900 tokens, you have \~197 tokens left for the model’s output. If your prompt uses the full limit, there is no room for completion.

<Frame>
  <img alt="A slide titled &#x22;Token Limits&#x22; that states OpenAI models have a maximum token size of 4,097. It notes that a 4,000-token prompt leaves up to 97 tokens for the completion and suggests breaking prompts into parts to work around the limit." />
</Frame>

<Callout icon="warning">
  Be mindful of the combined token usage (input + output). Exceeding a model’s context window will cause errors or truncated responses. If you need more context than the model allows, consider summarization, retrieval-augmented generation (RAG), or splitting inputs across multiple calls.
</Callout>

## Tokens and cost

OpenAI pricing is typically based on tokens processed (input + output). Keep a token budget for your application to:

* Ensure the model has sufficient context to produce accurate outputs.
* Control costs by reducing unnecessary tokens in prompts and responses.
* Choose an appropriate model for your use case (higher-capacity models often cost more per token).

Example (historical, subject to change): GPT‑3.5 Turbo was priced near \$0.002 per 1,000 tokens. Always check the official pricing page to estimate costs for your usage.

<Frame>
  <img alt="A presentation slide titled &#x22;Impact of Token Size on Cost&#x22; showing an example that GPT‑3.5 Turbo costs $0.002 per 1,000 tokens. It also notes you can optimize cost by selecting the right model, reducing token size, and setting usage limits." />
</Frame>

## Quick practical example: Try the tokenizer

Try the OpenAI Tokenizer: [https://platform.openai.com/tokenizer](https://platform.openai.com/tokenizer)

Paste this prompt into the tokenizer:

If it is 9AM in London, what time is it in Hyderabad. Be concise.

* Character count: 65 characters
* Token count (tool example): 19 tokens
* Word count: 14 words

This illustrates that tokens and words do not map 1:1.

## Summary

* Tokens are the basic units LLMs use to represent text.
* Tokenization splits text into tokens; encodings differ by model, so use the correct tokenizer.
* Context windows are measured in tokens and include both input and output—plan accordingly.
* Tokens determine cost—monitor and budget token usage.
* Use the OpenAI Tokenizer (web) or tiktoken (programmatic) to inspect tokens for your prompts.

References and further reading:

* OpenAI Tokenizer: [https://platform.openai.com/tokenizer](https://platform.openai.com/tokenizer)
* tiktoken GitHub: [https://github.com/openai/tiktoken](https://github.com/openai/tiktoken)
* [Kubernetes Documentation](https://kubernetes.io/docs/) (example external reference)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/e983525e-3a5a-4043-9319-4f259e41bc79/lesson/79a3c5fa-415e-4e90-a032-391ad1a0fd61" />
</CardGroup>


# Demo Performing Similarity Search

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Using-Word-Embeddings-For-Dynamic-Context/Demo-Performing-Similarity-Search/page

Learn to convert text into embeddings using OpenAI's model and perform similarity searches with NumPy for semantic applications.

In this guide, you’ll learn how to convert text into numerical vectors (embeddings) using OpenAI’s `text-embedding-ada-002` model and perform similarity searches with NumPy. This technique is essential for building semantic search, recommendation engines, and context-aware chatbots.

## 1. Setup

### 1.1 Install Dependencies

Make sure you have the OpenAI SDK and NumPy installed:

```bash theme={null}
pip install openai numpy
```

### 1.2 Import Libraries and Define Helper

```python theme={null}
import openai
import numpy as np

def text_embedding(text: str) -> list[float]:
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response["data"][0]["embedding"]
```

<Callout icon="lightbulb">
  Each embedding from `text-embedding-ada-002` has a fixed dimension of 1536, regardless of the input length.
</Callout>

## 2. Sample Phrases

We’ll use four phrases that share keywords but differ in meaning:

| Phrase                                                                                   | Context        |
| ---------------------------------------------------------------------------------------- | -------------- |
| "Most of the websites provide the users with the choice of accepting or denying cookies" | Web cookies    |
| "Olivia went to the bank to open a savings account"                                      | Financial bank |
| "Sam sat under a tree that was on the bank of a river"                                   | River bank     |
| "John's cookies were only half-baked but he still carries them for Mary"                 | Edible cookies |

## 3. Generating Embeddings

Convert each phrase to its embedding vector:

```python theme={null}
phrases = [
    "Most of the websites provide the users with the choice of accepting or denying cookies",
    "Olivia went to the bank to open a savings account",
    "Sam sat under a tree that was on the bank of a river",
    "John's cookies were only half-baked but he still carries them for Mary"
]

embeddings = [text_embedding(p) for p in phrases]
print(f"Embedding dimension: {len(embeddings[0])}")  # Expect 1536
```

## 4. Defining Cosine Similarity

Cosine similarity measures the angle between two vectors in the semantic space. Identical vectors yield a score of 1.0.

```python theme={null}
def vector_similarity(vec1: list[float], vec2: list[float]) -> float:
    a, b = np.array(vec1), np.array(vec2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
```

## 5. Running Similarity Searches

Define a function to find the most similar phrase from our list:

```python theme={null}
def find_most_similar(query: str) -> str:
    q_emb = text_embedding(query)
    scores = [vector_similarity(q_emb, emb) for emb in embeddings]
    ranked = sorted(zip(scores, phrases), reverse=True, key=lambda x: x[0])
    best_score, best_phrase = ranked[0]
    print(f"Query: {query!r}\nBest match ({best_score:.2f}): {best_phrase}\n")
    return best_phrase
```

### 5.1 Example Queries

```python theme={null}
find_most_similar("Sam sat under a tree that was on the bank of a river")
find_most_similar("Mary got the biscuits from John that were not fully baked")
find_most_similar("It's recommended to put your savings in a financial institution")
find_most_similar("You get refreshed when you spend time with nature")
find_most_similar("Cookies are covered by GDPR if they collect information about users that could be used to identify them")
```

Expected outputs:

* Exact riverbank match → similarity ≈ 1.00
* Biscuits (edible cookies) → ≈ 0.92
* Financial advice → ≈ 0.84
* Nature reference → ≈ 0.82
* GDPR cookies → ≈ 0.83

## 6. Discussion

* Embeddings capture **semantic context**, not just surface-level keywords.
* All vectors have the same dimensionality (1536) to sit in a common embedding space.
* Cosine similarity retrieves items by **meaning**, not by exact word overlap.

<Callout icon="lightbulb">
  This approach powers many AI-driven features such as semantic search, recommendation engines, and dynamic context for chatbots.
</Callout>

Experiment by adding new phrases, querying different sentences, and watching how similarity scores adapt to meaning.

## Links and References

* [OpenAI Embeddings Documentation](https://platform.openai.com/docs/guides/embeddings)
* [Cosine Similarity on Wikipedia](https://en.wikipedia.org/wiki/Cosine_similarity)
* [NumPy API Reference](https://numpy.org/doc/stable/reference/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/cf879fc5-dcc3-4470-830d-4393645105c9/lesson/d78345f7-7490-4860-b9fe-da2730b087d8" />
</CardGroup>
