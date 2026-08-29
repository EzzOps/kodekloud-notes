# Preparing Datasets for RAG Systems

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-Certification/Core-Machine-Learning-and-AI-Knowledge/Preparing-Datasets-for-RAG-Systems/page

Explains why chunking documents into appropriate segments is vital for RAG systems, affecting embeddings, retrieval relevance, and LLM answers, with best practices and practical tips

Question 8.

When preparing content databases for a RAG system, which of the following techniques is most important for effective information retrieval?

* Translating all content to multiple languages.
* Chunking documents into appropriately sized segments.
* Filtering out all numeric data.
* Converting all text to lowercase.

In this question we are looking for the single most important technique.

Correct answer: Chunking documents into appropriately sized segments.

Answer summary:
Chunking documents into appropriately sized segments is the single most important preprocessing step for Retrieval-Augmented Generation (RAG) systems. Proper chunking has a direct effect on embedding quality, vector search relevance, and the downstream LLM’s ability to synthesize accurate answers.

<Frame>
  <img alt="The image is a question and answer about preparing datasets for a RAG (Retrieval-Augmented Generation) system, highlighting the importance of chunking documents into appropriately sized segments for effective information retrieval." />
</Frame>

Why chunking matters (SEO keywords: RAG, chunking, embeddings, vector search, context window)

* Embedding quality: Embedding models encode the semantic meaning of a chunk. Appropriately sized, topically coherent chunks produce focused embeddings that match user queries more reliably.
* Retrieval relevance: Indexing granular chunks increases the chance that a retrieved passage contains a concise, relevant answer rather than unrelated material.
* Context trade-offs: Very large chunks can mix topics and dilute embeddings; very small chunks can strip necessary context, harming the LLM’s reasoning.
* Efficiency and scalability: Smaller, well-formed chunks reduce search latency for nearest-neighbor (k-NN) lookups in vector databases and lower memory overhead.

Best practices for chunking

<Callout icon="lightbulb">
  * Target chunk sizes that match your embedding model and the downstream LLM’s context window — commonly `~200–1000` tokens depending on model choice.
  * Use semantic boundaries (sentences, paragraphs, section headings) instead of arbitrary byte/character splits to preserve coherence.
  * Include modest overlap between adjacent chunks (e.g., `10–30%`) to preserve continuity across boundaries.
  * Attach rich metadata to each chunk: `source`, `document_id`, `position`, `section_title`, and any domain tags for reranking and provenance.
  * Deduplicate near-duplicate chunks, normalize whitespace/formatting, and preserve numeric data unless you have a domain-specific reason to remove it.
</Callout>

Table — quick comparison of the listed techniques

| Technique                                            | Use Case / Effect on RAG                                                    | Recommendation                                                 |
| ---------------------------------------------------- | --------------------------------------------------------------------------- | -------------------------------------------------------------- |
| Chunking documents into appropriately sized segments | Directly improves embeddings, retrieval relevance, and LLM answers          | Primary preprocessing step — prioritize this                   |
| Translating all content to multiple languages        | Needed only for multilingual coverage; increases cost and complexity        | Optional — apply when multilingual support is required         |
| Filtering out all numeric data                       | Removes potentially critical factual information (dates, measurements, IDs) | Generally harmful — avoid unless domain-specific reasons exist |
| Converting all text to lowercase                     | Minor normalization; modern embeddings often handle case                    | Low impact — optional normalization step                       |

Notes on the other options

* Translating all content may be useful for a multilingual deployment, but it is not the primary factor for retrieval quality. Consider translation when user languages require it.
* Filtering out numeric data is usually detrimental: numbers are frequently essential for accurate answers in technical, financial, scientific, and date-sensitive domains.

<Callout icon="warning">
  Do not remove numeric data indiscriminately. Numbers often carry crucial semantic meaning and can be necessary for correct retrieval and factual responses.
</Callout>

* Converting all text to lowercase is a minor normalization step; many modern tokenizers and embedding models handle case in a way that preserves useful signals, so lowercasing is not a substitute for proper chunking.

Practical tips and references

* Start by profiling your documents: average paragraph length, common section sizes, and domain-specific indicators (tables, code blocks, numeric-heavy sections).
* Experiment with chunk sizes and retrieval metrics (recall\@k, MRR) to find the sweet spot for your pipeline.
* Consider hybrid approaches: combine semantic chunking with structured extraction for tables or code, and use specialized embeddings for tables or numeric data when needed.

Further reading

* [Retrieval-Augmented Generation — Wikipedia](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
* [OpenAI Embeddings guide](https://platform.openai.com/docs/guides/embeddings)

In summary: prioritize careful, semantically-aware chunking with appropriate size and overlap, enrich chunks with metadata, and reserve other transformations (translation, lowercasing, numeric filtering) for specific use cases rather than as default steps.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/875d98e8-3b09-4f35-b877-2758b84443ca/lesson/efb9f959-b845-43dc-9a89-4f602519c2b9" />
</CardGroup>
