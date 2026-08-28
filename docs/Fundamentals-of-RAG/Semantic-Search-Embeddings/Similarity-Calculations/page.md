# Similarity Calculations

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Semantic-Search-Embeddings/Similarity-Calculations/page

Explains using embeddings and cosine similarity to measure semantic relevance for effective semantic search and retrieval augmented generation, improving document retrieval and grounding model outputs.

In this lesson we explain how similarity calculations let us find the most semantically relevant passages — the “needles” in a large digital haystack — without scanning every document. This is essential for semantic search and Retrieval-Augmented Generation (RAG), where the quality of retrieved context directly affects model output reliability.

A traditional keyword search matches literal characters and phrases. For example, asking about how plants communicate with a keyword search will only surface passages that contain your exact words and may miss related concepts expressed with different vocabulary.

<Frame>
  <img alt="The image shows a bookshelf filled with books and a stack of books in front, alongside text comparing traditional keyword search terms: &#x22;Plants&#x22; and &#x22;Communicate.&#x22;" />
</Frame>

Because keyword matching is literal, it can miss related concepts such as root signaling, nutrient-sharing networks, or fungal connections beneath the soil — passages that are semantically relevant but do not include your exact search terms.

<Frame>
  <img alt="The image shows an illustration of a bookshelf with stacked books and a list titled &#x22;What Gets Missed,&#x22; highlighting points about tree communication, forest networks, and fungal connections." />
</Frame>

Similarity-based methods avoid this problem by measuring how close two pieces of text are in meaning rather than comparing characters. This is done by mapping words, sentences, or documents into high-dimensional vectors called embeddings.

Conceptually, embeddings are like GPS coordinates in a much higher-dimensional space. A single embedding might look like:

```python theme={null}
