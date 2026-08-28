# Demo Visualization of Vectors in vectorDB

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Introduction-to-Vector-Databases-and-Generative-AI/Demo-Visualization-of-Vectors-in-vectorDB/page

Demo showing PDF text converted to sentence-transformer embeddings stored in ChromaDB and visualized in 3D via PCA and Plotly, with chunking and metadata previews.

Welcome back.

In this lesson we demonstrate how text from a large PDF is converted into vector embeddings, stored in a vector database (ChromaDB), and visualized in 3D after dimensionality reduction. This walkthrough helps you understand how semantic similarity appears spatially when embeddings are projected to three principal components.

What you'll learn:

* Extract text from a PDF and chunk it for embedding
* Create embeddings with a sentence-transformer model
* Persist embeddings and chunk metadata in ChromaDB
* Retrieve embeddings, reduce dimensionality with PCA, and plot an interactive 3D scatter using Plotly

Let’s jump into the demo.

<Frame>
  <img alt="The image shows a Jupyter Notebook interface displaying a file directory, which includes various files like Jupyter notebooks, a markdown file, a requirements text file, and a PDF document." />
</Frame>

Overview of the demo flow:

1. Load a PDF document.
2. Extract and split text into overlapping chunks.
3. Embed each chunk with a sentence-transformer.
4. Store embeddings and chunk text/metadata in ChromaDB.
5. Retrieve embeddings, run PCA → 3 components.
6. Render an interactive 3D Plotly scatter with chunk previews on hover.

The demo uses a large PDF (U.S. Government Budget FY 2025, \~188 pages) to illustrate how real-world documents produce many chunks and embeddings.

<Frame>
  <img alt="The image shows a digital PDF viewer open to the document &#x22;Budget of the U.S. Government, Fiscal Year 2025,&#x22; displaying its cover page and thumbnails of the first few pages." />
</Frame>

Required imports (run once at the top of the notebook)

```python theme={null}
