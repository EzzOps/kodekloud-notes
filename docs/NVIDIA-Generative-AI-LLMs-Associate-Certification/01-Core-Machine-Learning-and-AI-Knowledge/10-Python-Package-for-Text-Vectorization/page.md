# Example few-shot prompt: instruction -> command pairs
Instruction: List files in the current directory
Command: ls

Instruction: Show the current working directory
Command: pwd

Instruction: Create a directory named projects
Command: mkdir projects

# Target query (model should infer the pattern and respond with a command)
Instruction: Remove the file old.txt
Command:
```

Given those demonstrations, the model should infer the mapping from "Instruction" to "Command" and complete the last "Command" with the correct shell command, for example:

```bash theme={null}
rm old.txt
```

<Callout icon="lightbulb">
  Few-shot prompts provide examples that shape the model's output format and style at inference time. They do not train the model or change its weights; they simply bias the model toward the pattern shown in the prompt.
</Callout>

Quick comparison

| Option                                      | What it does                                                                          | Correct? |
| ------------------------------------------- | ------------------------------------------------------------------------------------- | -------- |
| Increase the model's vocabulary             | Not affected by few-shot prompts; vocabulary is defined by the pre-trained model      | No       |
| Guide the model's response format and style | Provides in-context examples so the model mimics the demonstrated structure and tone  | Yes      |
| Reduce computational cost of inference      | Few-shot examples can increase prompt length and cost per query rather than reduce it | No       |
| Fine-tune model weights in real time        | Few-shot prompting is not training; it does not update model parameters               | No       |

Further reading and references

* [In-context learning and few-shot prompting — OpenAI blog](https://openai.com/blog/instruction-following)
* [Prompting strategies and best practices — Practical guides on prompt engineering](https://learnprompting.org/)
* [Research overview: Few-shot learning and in-context learning](https://arxiv.org/abs/2103.10385)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/875d98e8-3b09-4f35-b877-2758b84443ca/lesson/8da9d9e9-78bf-45aa-b511-bb4b1244c34f" />
</CardGroup>


# Python Package for Text Vectorization

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-Certification/Core-Machine-Learning-and-AI-Knowledge/Python-Package-for-Text-Vectorization/page

Guide comparing Python libraries for creating dense text embeddings, recommending spaCy with vector models and transformer alternatives, plus usage examples and similarity search tips.

Question 2.

Which Python package is most appropriate for creating dense vector representations of text for a semantic search application? Would it be NumPy, spaCy, matplotlib, or scikit-learn?

Answer: [spaCy](https://spacy.io)

spaCy is a production-ready natural language processing library that includes easy access to pre-trained dense word and document vectors when you use models that ship with vectors (for example, `en_core_web_lg`). While:

* [NumPy](https://numpy.org) is the core numerical library used to manipulate vectors (arrays)
* [matplotlib](https://matplotlib.org) is for visualization
* [scikit-learn](https://scikit-learn.org) offers ML utilities and some vectorizers (e.g., TF-IDF)

spaCy directly provides token and document `.vector` embeddings that are convenient for semantic search workflows.

<Callout icon="lightbulb">
  Use a spaCy model that includes vectors (for example, `en_core_web_lg`) when you need ready-made dense embeddings. For higher-quality sentence or paragraph embeddings, consider transformer-based libraries such as [`sentence-transformers`](https://www.sbert.net/) (SBERT) or Hugging Face models, and combine those embeddings with spaCy or your retrieval pipeline as needed.
</Callout>

## Quick comparison

| Library                                | Typical use for embeddings                          | Notes / Recommendation                                                 |
| -------------------------------------- | --------------------------------------------------- | ---------------------------------------------------------------------- |
| `spaCy`                                | Dense word & document vectors via model `.vector`   | Best for fast, production NLP with built-in vectors (`en_core_web_lg`) |
| `sentence-transformers` / Hugging Face | State-of-the-art sentence embeddings                | Often yields better semantic similarity for sentences/paragraphs       |
| `scikit-learn`                         | Feature extraction (TF-IDF, hashing)                | Good for sparse representations; not dense semantic embeddings         |
| `NumPy`                                | Numerical operations on vectors                     | Essential for handling arrays returned by embedding libraries          |
| `matplotlib`                           | Visualization of embeddings (e.g., PCA/t-SNE plots) | Not used to create embeddings                                          |

## Install and load a spaCy model with vectors

Shell:

```bash theme={null}
