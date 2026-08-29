# Demo Image Embedding

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/From-Data-to-Vectors-The-Embedding-Layer/Demo-Image-Embedding/page

Tutorial demonstrating embedding images with CLIP, storing vectors in LanceDB, and performing text-to-image searches in a Jupyter Notebook

In this lesson you'll embed real images into a vector database, then perform text-based searches that retrieve matching images. We'll use a CLIP image+text model (via sentence-transformers) to generate embeddings and LanceDB to store and search vectors. All work is done inside a Jupyter Notebook.

What you'll learn:

* How to compute image embeddings with CLIP (sentence-transformers).
* How to store image vectors and metadata in LanceDB.
* How to run text-to-image searches and visualize results.

Prerequisites

* Python 3.8+
* Jupyter Notebook or JupyterLab
* Packages: `lancedb`, `sentence-transformers`, `Pillow`, `matplotlib`, `numpy`, `pandas`

Tools and libraries used

| Tool / Library               |                                          Purpose | Link                                                     |
| ---------------------------- | -----------------------------------------------: | -------------------------------------------------------- |
| LanceDB                      | Vector database for storing/searching embeddings | [https://www.lancedb.ai/](https://www.lancedb.ai/)       |
| sentence-transformers (CLIP) |                          Image + text embeddings | [https://www.sbert.net/](https://www.sbert.net/)         |
| Pillow (PIL)                 |                  Image loading and preprocessing | [https://python-pillow.org/](https://python-pillow.org/) |
| matplotlib                   |            Visualizing image preview and results | [https://matplotlib.org/](https://matplotlib.org/)       |
| Jupyter Notebook             |                          Interactive environment | [https://jupyter.org/](https://jupyter.org/)             |

Getting started — setup and preview images

1. Set up paths and preview the images you'll embed (a cat, a dog, and a fox).
2. Run this code cell in a notebook to locate images and display them.

```python theme={null}
