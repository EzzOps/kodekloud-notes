# Embeddings Demo

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Text-Generation/Embeddings-Demo/page

This article explains embeddings in NLP, how to create and inspect them using OpenAI's Python library, and their applications in various projects.

Welcome back! In this lesson, we’ll dive into **embeddings**—a fundamental building block for modern NLP applications. You’ll learn what embeddings are, how to create them with the OpenAI Python library, inspect the resulting vectors, and explore next steps for integrating embeddings into your projects.

## What Is an Embedding?

An **embedding** is a high-dimensional vector representation of text (or other data) that captures semantic meaning. Machine learning models use embeddings to measure relatedness between inputs for tasks like:

| Use Case              | Description                                          |
| --------------------- | ---------------------------------------------------- |
| Semantic Search       | Retrieve documents most relevant to a query          |
| Clustering            | Group similar texts together                         |
| Recommendations       | Suggest related items based on content similarity    |
| Anomaly Detection     | Identify outliers in text datasets                   |
| Diversity Measurement | Quantify variation within a corpus                   |
| Classification        | Improve text classifiers with richer feature vectors |

Embeddings map text strings into a continuous vector space, allowing algorithms to compute distances (e.g., cosine similarity) and uncover relationships.

## Creating an Embedding

First, install the OpenAI Python library and export your API key:

```bash theme={null}
pip install openai
export OPENAI_API_KEY="YOUR_API_KEY"
```

<Callout icon="triangle-alert">
  Never commit your `OPENAI_API_KEY` to public repositories. Use environment variables or secret managers to keep your key secure.
</Callout>

Next, generate an embedding:

```python theme={null}
from openai import OpenAI

client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-ada-002",
    input="The food was delicious and the waiter was very attentive."
)

print(response)
```

```json theme={null}
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "embedding": [
        0.00230642455,
        0.0032792702,
        ...
        // 1536 floats total for ada-002
      ]
    }
  ]
}
```

For details on models, parameters, and rate limits, see the [OpenAI embeddings documentation][1].

## Embedding Model Comparison

| Model                  | Dimensions | Context Window | Typical Use Case                |
| ---------------------- | ---------- | -------------- | ------------------------------- |
| text-embedding-ada-002 | 1536       | 8,192 tokens   | Cost-effective, general purpose |
| text-embedding-3-large | 12,288     | 8,192 tokens   | High-fidelity semantic tasks    |

<Callout icon="lightbulb">
  Larger models often yield richer representations but come with higher compute costs and latency.
</Callout>

## Inspecting Embeddings in Python

Once you have embeddings, you can examine the raw vectors:

```python theme={null}
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

response = client.embeddings.create(
    input="Michael Jordan is better than LeBron James",
    model="text-embedding-3-large"
)

vector = response.data[0].embedding
print(vector)
```

```plaintext theme={null}
[ 0.016919609921797, 0.008237271796965, 0.015445727936748, 
  0.011458127799397, 0.015966911630216, 0.01077441280857632, 
  0.001197237995964063, ... ]
```

These floating-point values position your text in a semantic space. Use similarity metrics (e.g., cosine similarity) to compare vectors.

## Next Steps

With embeddings at your disposal, you can:

1. **Store** them in a vector database like [Pinecone][2] or [Weaviate][3].
2. **Perform** similarity searches to retrieve related documents or answers.
3. **Cluster** content by semantic similarity for topic modeling.
4. **Build** recommendation systems based on text or user-profile embeddings.

Embeddings power a wide range of NLP pipelines—experiment with different models, inputs, and downstream algorithms to unlock new insights!

***

## Links and References

* [OpenAI Embeddings Documentation][1]
* [Pinecone Vector Database][2]
* [Weaviate Vector Database][3]
* [TensorFlow Similarity Search][4]

[1]: https://platform.openai.com/docs/guides/embeddings

[2]: https://www.pinecone.io/

[3]: https://weaviate.io/

[4]: https://www.tensorflow.org/recommenders/overview/similarity_search

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-openai/module/b6b7bec7-ed21-47d5-afbb-663df59f5e97/lesson/230ede25-404b-4bb9-bffe-13680dd8b8d0" />
</CardGroup>
