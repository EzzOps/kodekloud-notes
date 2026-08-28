# Embeddings

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Text-Generation/Embeddings/page

This article explains how embeddings convert various data types into vectors for applications like semantic search and clustering.

In this article, you’ll learn how embeddings transform text, images, and audio into high-dimensional numeric vectors. By representing data in a common vector space, embeddings power semantic search, clustering, recommendations, and more.

<Frame>
  ![The image illustrates an embedding model that converts images, documents, and audio into vectors, which are then visualized in a 3D space.](https://kodekloud.com/kk-media/image/upload/v1752879208/notes-assets/images/Introduction-to-OpenAI-Embeddings/embedding-model-3d-vector-visualization.jpg)
</Frame>

Each point in the 3D scatter plot represents an object; similar items appear closer together. This spatial arrangement enables efficient comparison, retrieval, and analysis across diverse data types.

## What Are Embeddings?

Embeddings are lists of floating-point numbers that capture the semantic features of text, images, or audio. The closer two vectors are in the embedding space, the more related their underlying data.

<Frame>
  ![The image explains embeddings as vectors (lists) of floating-point numbers, with the distance between two vectors indicating their relatedness.](https://kodekloud.com/kk-media/image/upload/v1752879209/notes-assets/images/Introduction-to-OpenAI-Embeddings/embeddings-vectors-floating-point-numbers.jpg)
</Frame>

### Common Applications of Embeddings

| Application           | Description                                                   |
| --------------------- | ------------------------------------------------------------- |
| Semantic Search       | Rank results by relevance to a query across large corpora.    |
| Clustering            | Group similar texts (e.g., articles, feedback) automatically. |
| Recommendations       | Suggest related items based on user or item vectors.          |
| Anomaly Detection     | Detect outliers by measuring low similarity scores.           |
| Diversity Measurement | Analyze similarity distributions within a dataset.            |
| Classification        | Assign labels by comparing to prototype embeddings.           |

<Callout icon="lightbulb">
  Embedding distances are computed via metrics like cosine similarity or Euclidean distance. Choose the metric that best suits your task.
</Callout>

## Why Embeddings Matter

* **Semantic Understanding:** Retrieve documents by meaning, not just keyword matches (e.g., “best smartphones” → “top mobile devices”).
* **Contextual Search:** Capture intent and context for more relevant search results.
* **Personalization:** Align recommendations with user preferences based on past interactions.
* **Zero-Shot Learning:** Predict unseen categories by positioning new labels near related known concepts.

## How Embeddings Work

1. **High-Dimensional Mapping:** Each word, phrase, or document is converted into a vector in a multi-dimensional space.
2. **Clustering by Similarity:** Semantically related items (e.g., “cat,” “feline”) cluster together.
3. **Separation of Unrelated Data:** Dissimilar items (e.g., “cat,” “car”) lie far apart.

This arrangement supports rapid **semantic search**, **clustering**, and **relationship analysis** across large datasets.

<Frame>
  ![The image illustrates how embeddings work, showing words grouped by sentiment: positive (e.g., "pretty," "elegant"), negative (e.g., "dirty," "ugly"), and neutral (e.g., "neutral," "impartial").](https://kodekloud.com/kk-media/image/upload/v1752879210/notes-assets/images/Introduction-to-OpenAI-Embeddings/embeddings-sentiment-words-illustration.jpg)
</Frame>

## Generating Embeddings with the OpenAI API

Use the OpenAI [Embeddings API](https://platform.openai.com/docs/guides/embeddings) to convert text into vectors:

```python theme={null}
import openai

openai.api_key = "YOUR_OPENAI_API_KEY"

response = openai.Embeddings.create(
    model="text-embedding-ada-002",
    input="Your text here"
)
embedding = response["data"][0]["embedding"]
print(embedding)
```

Sample output:

```text theme={null}
[0.05133137, 0.024704147, 0.0031928015, -0.031632155, 0.009103798, ...]
```

<Frame>
  ![The image lists three uses: text search, clustering, and recommendations, on a dark background.](https://kodekloud.com/kk-media/image/upload/v1752879212/notes-assets/images/Introduction-to-OpenAI-Embeddings/text-search-clustering-recommendations-dark.jpg)
</Frame>

<Callout icon="triangle-alert">
  Keep your API key secure. Avoid exposing it in public repositories or client-side code.
</Callout>

## Key Use Cases

| Use Case           | Description                                                                     | Example                                                                   |
| ------------------ | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Semantic Search    | Convert queries and documents into embeddings, then retrieve nearest items.     | Building a FAQ chatbot that finds the most relevant answer by similarity. |
| Clustering         | Group similar documents to detect topics or trends.                             | Organizing customer feedback into thematic clusters for analysis.         |
| Recommendations    | Compare item and user embeddings for personalized suggestions.                  | Suggesting products based on a user’s purchase history.                   |
| Zero-Shot Learning | Relate new labels to existing embeddings for classification without retraining. | Classifying support tickets into unseen categories.                       |

## Example: Question Answering with Chat Models

This Python snippet embeds a Wikipedia article on the 2022 Winter Olympics and uses a chat model to answer a query:

```python theme={null}
query = f"""Use the below article on the 2022 Winter Olympics to answer the subsequent question.
Article:
{wikipedia_article_on_curling}
Question: Which athletes won the gold medal in curling at the 2022 Winter Olympics?"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You answer questions about the 2022 Winter Olympics."},
        {"role": "user",   "content": query},
    ],
    temperature=0,
)

print(response.choices[0].message.content)
```

## Best Practices

<Frame>
  ![The image outlines three best practices for text processing: preprocessing text, using consistent embedding models, and leveraging pre-trained embeddings.](https://kodekloud.com/kk-media/image/upload/v1752879213/notes-assets/images/Introduction-to-OpenAI-Embeddings/text-processing-best-practices-embedding.jpg)
</Frame>

1. **Preprocess Text:** Lowercase, remove punctuation, and filter stop words.
2. **Use Consistent Models:** Stick to one embedding model per project for reliable comparisons.
3. **Leverage Pre-trained Embeddings:** Save time and compute by using OpenAI’s optimized models.

## Links and References

* [OpenAI Embeddings API Guide](https://platform.openai.com/docs/guides/embeddings)
* [Chat Completions API](https://platform.openai.com/docs/guides/chat)
* [Cosine Similarity Explained](https://en.wikipedia.org/wiki/Cosine_similarity)
* [Semantic Search Techniques](https://towardsdatascience.com/semantic-search-using-embeddings-9d59f2c1114e)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-openai/module/b6b7bec7-ed21-47d5-afbb-663df59f5e97/lesson/435a4245-e969-4407-877a-1b17861c3cf3" />
</CardGroup>
