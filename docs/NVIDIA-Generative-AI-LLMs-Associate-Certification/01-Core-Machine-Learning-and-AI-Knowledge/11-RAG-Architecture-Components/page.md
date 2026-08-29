# Install spaCy and a model that includes vectors
pip install spacy
python -m spacy download en_core_web_lg
```

Python example:

```python theme={null}
import spacy

# Load a spaCy model that includes pre-trained vectors
nlp = spacy.load("en_core_web_lg")

doc = nlp("This is a sample sentence for semantic search.")
vector = doc.vector  # dense NumPy array representing the whole document

print(type(vector))   # <class 'numpy.ndarray'>
print(vector.shape)   # commonly (300,) for many spaCy vectors
```

Notes:

* spaCy’s `.vector` on a `Doc` or `Token` returns a dense `numpy.ndarray` that you can use directly for similarity computations (cosine similarity), indexing into vector stores, or as input to downstream models.
* For improved semantic-search accuracy at sentence/paragraph level, consider transformer-based encoders such as [`sentence-transformers`](https://www.sbert.net/) or Hugging Face embedding models; these typically yield higher-quality embeddings than classic spaCy vectors for sentence semantics.
* Use `sklearn.metrics.pairwise.cosine_similarity` or `scipy.spatial.distance.cosine` (or faiss/annoy for large-scale search) to compute nearest neighbors efficiently.

## References and further reading

* spaCy models: [https://spacy.io/models/en\_core\_web\_lg](https://spacy.io/models/en_core_web_lg)
* sentence-transformers: [https://www.sbert.net/](https://www.sbert.net/)
* Hugging Face: [https://huggingface.co/](https://huggingface.co/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/875d98e8-3b09-4f35-b877-2758b84443ca/lesson/2ab2521e-4861-45d9-a718-e201f5d20011" />
</CardGroup>


# RAG Architecture Components

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-Certification/Core-Machine-Learning-and-AI-Knowledge/RAG-Architecture-Components/page

Describes RAG architecture components, including retrieval, chunking, vector databases and generation, and explains why gradient descent continual learning is not part of inference.

Now let's get started on the course for the [NVIDIA Generative AI LLMs Associate Certification](https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification). We will begin with Core Machine Learning and AI Knowledge.

Consider this question:

A developer is tasked with implementing a retrieval-augmented generation, or RAG, system. Which of the following is NOT a typical component of a RAG architecture?

* A vector database for storing document embeddings
* A text generation model for producing responses
* A gradient descent optimizer for continual learning
* A document chunking mechanism for preprocessing

Answer: A gradient descent optimizer for continual learning.

Why this is the correct choice

Retrieval-augmented generation (RAG) integrates an external retrieval step with a generative language model. The usual RAG pipeline focuses on fetching relevant context and conditioning a generator on that context; it does not perform live gradient-based training during inference. Typical components include:

* Retrieval — finding relevant documents, passages, or knowledge snippets using embeddings and similarity search (commonly backed by a vector database).
* Preprocessing / Chunking — splitting long documents into model-friendly passages or chunks so the retriever and generator can work effectively.
* Generation — a language model (decoder, encoder-decoder, or instruction-following LLM) that conditions on retrieved context to produce the final response.

Quick overview table

| Component                         | Typical in RAG? | Purpose / Example                                                                      |
| --------------------------------- | --------------- | -------------------------------------------------------------------------------------- |
| Retrieval                         | Yes             | Find relevant passages using embeddings and nearest-neighbor search (e.g., vector DB). |
| Vector database                   | Yes             | Store and index embeddings for fast similarity search.                                 |
| Document chunking / preprocessing | Yes             | Split documents into chunks that match model context windows.                          |
| Text generation model             | Yes             | Produce answers conditioned on retrieved context.                                      |
| Gradient descent optimizer        | No              | Used for training/fine-tuning models offline, not for live inference in RAG.           |

<Frame>
  <img alt="The image depicts a flowchart with three stages: Retrieval, Chunking, and Generation, each connected by arrows." />
</Frame>

Note on continual learning and gradient descent

* RAG systems typically keep the generation model fixed at query time and rely on an external retrieval index to surface current knowledge.
* Continuous model updates via gradient descent are not part of the inference pipeline. When you need the model to learn from new data, typical approaches include periodic offline fine-tuning, parameter-efficient updates (e.g., adapters), or re-embedding the index and refreshing the vector database.
* In short: keep retrieval fast and up-to-date; apply training and weight updates as separate, controlled offline processes.

<Callout icon="lightbulb">
  RAG architectures center on retrieval, preprocessing/chunking, and generation. Continuous weight updates via gradient descent during inference are not part of the standard RAG pipeline—updates are handled separately when needed.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/875d98e8-3b09-4f35-b877-2758b84443ca/lesson/ae9a459b-6631-4149-9a67-19696cd617c9" />
</CardGroup>
