# Image Embedding Models

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/From-Data-to-Vectors-The-Embedding-Layer/Image-Embedding-Models/page

Overview of image embedding models CLIP ResNet and ViT comparing their architectures strengths embedding sizes and use cases for visual search retrieval and downstream vision tasks

Hello and welcome back.

This lesson builds on earlier coverage of text embedding models and moves into the visual domain. Not all data is text — image embedding models convert pixels into semantic vectors that encode visual meaning. These embeddings power many real-world systems: visual search, content moderation, facial recognition, medical imaging, product recommendations, and more. A familiar consumer example is Pinterest Lens: snap a photo and it finds visually similar home decor, recipes, or fashion items — that’s image embeddings working in real time.

What follows is a concise introduction to three widely used image embedding model families, how they differ, and where each is most applicable.

* CLIP (Contrastive Language–Image Pre-training) — strong multimodal alignment between images and text; excellent for zero-shot tasks and cross-modal retrieval.
* ResNet family (e.g., ResNet-50, ResNet-101) — reliable convolutional features widely used as off-the-shelf visual embeddings.
* Vision Transformer (ViT) — applies Transformer-style attention to image patches and scales particularly well with large datasets.

## CLIP (Contrastive Language–Image Pre-training)

CLIP, released by OpenAI in January 2021, was trained on roughly 400 million image–text pairs and learns to align images with natural language. By learning a joint image–text embedding space, CLIP supports zero-shot classification and multimodal retrieval: you can score the compatibility of an image and a text prompt directly in the same vector space.

<Frame>
  <img alt="The image provides an overview of image embedding models, highlighting CLIP, a language-image pre-training model developed by OpenAI, with real-world use cases like visual search and content moderation." />
</Frame>

This joint training enables tasks such as:

* Zero-shot classification (label without supervised fine-tuning)
* Cross-modal retrieval (image → text and text → image search)
* Multimodal semantic search (search images using natural language queries)

CLIP is particularly useful when you need strong semantic alignment between language and vision or when you want robust performance on concepts not explicitly seen during training.

## ResNet family (ResNet-50, ResNet-101)

Introduced by Microsoft Research in 2015, ResNet popularized residual (skip) connections that mitigate the vanishing gradient problem and enable much deeper convolutional networks. In many pipelines, the penultimate pooled feature vector (e.g., the pooled output before the final classification layer) from a ResNet-50 or ResNet-101 is used as a fixed image embedding.

Key points:

* Typical pooled feature dimension: 2,048 (for ResNet-50/101 architectures)
* Strong, well-understood convolutional features that work reliably across many vision tasks
* Commonly used for transfer learning, feature extraction, and classic image-similarity applications

## Vision Transformer (ViT)

Vision Transformer (ViT), introduced by Google Research in 2020, adapts the Transformer architecture to images by splitting an image into patches, projecting each patch to an embedding, and applying self-attention across patches. Given large-scale training data, ViT variants often outperform traditional CNNs like ResNet.

<Frame>
  <img alt="The image presents a comparison of three image embedding models: CLIP, ResNet-50/101, and Vision Transformer (ViT), highlighting their developers, release dates, and key features. It also mentions real-world use cases such as visual search, content moderation, and medical imaging." />
</Frame>

ViT advantages:

* Scales well with very large datasets and compute
* Learns long-range dependencies across image patches via attention
* Flexible architecture that can be adapted for fine-grained tasks when trained at scale

## Why image embeddings matter

Image embeddings convert raw pixels into compact vectors that encode semantic concepts, making tasks like similarity search, clustering, and downstream classification feasible without manual tagging. Instead of labeling thousands of images, systems can find similar images by measuring distances in embedding space — a technique that underlies Google Photos search, Instagram Explore, Shopify visual search, diagnostic aids in medical imaging, and autonomous perception systems.

<Frame>
  <img alt="The image compares three image embedding models: CLIP, ResNet-50/101, and Vision Transformer (ViT), highlighting their release dates, developers, and key features. It also explains the importance and applications of image embeddings." />
</Frame>

## Quick comparison

| Model           | Strengths                                                        |               Typical embedding size | Common use cases                                                                                 |
| --------------- | ---------------------------------------------------------------- | -----------------------------------: | ------------------------------------------------------------------------------------------------ |
| CLIP            | Strong image↔text alignment; zero-shot and multimodal retrieval  |       `512–1024` (variant-dependent) | Visual search with natural language, cross-modal retrieval, zero-shot classification             |
| ResNet (50/101) | Robust convolutional features, widely used for transfer learning | `2048` (pooled penultimate features) | Feature extraction, similarity matching, classic computer vision tasks                           |
| ViT             | Transformer-style attention over patches; scales with data       |       `768–1024` (variant-dependent) | Large-scale pretraining, fine-grained visual understanding, tasks benefiting from global context |

> **lightbulb** Choose a model based on your goals:

  * Use CLIP when you need natural-language queries or zero-shot capabilities.
  * Use ResNet for reliable, off-the-shelf visual features and smaller compute budgets.
  * Use ViT when you can leverage large-scale pretraining and want attention-based representations.

## Practical notes

* Embedding dimensionality and model size vary by architecture and implementation—always check the specific pretrained checkpoint you plan to use.
* For production systems, evaluate retrieval latency, embedding storage cost (vector dimensionality × number of items), and indexing strategy (e.g., ANN libraries like Faiss, Milvus).
* When aligning images with text (search, captions, multimodal prompts), CLIP-like models simplify scoring because both modalities share an embedding space.

## Links and further reading

* CLIP (OpenAI) paper: [https://openai.com/research/clip](https://openai.com/research/clip)
* ResNet (He et al., Microsoft Research): [https://arxiv.org/abs/1512.03385](https://arxiv.org/abs/1512.03385)
* Vision Transformer (Dosovitskiy et al., Google Research): [https://arxiv.org/abs/2010.11929](https://arxiv.org/abs/2010.11929)

Audio embedding models are another important modality and are covered in a separate lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/47c71900-9efe-47e3-ac4c-502d14eafd06/lesson/e55b7fb1-f6f5-4e98-8675-72296295e3a4)
