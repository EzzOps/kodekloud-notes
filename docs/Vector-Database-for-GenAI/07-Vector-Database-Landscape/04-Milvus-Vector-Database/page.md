# Milvus Vector Database

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Database-Landscape/Milvus-Vector-Database/page

Introduction to Milvus, a scalable distributed open source vector database for billion scale AI search, offering cloud native deployment, multi index support, GPU acceleration, and high availability.

Welcome back. This article provides a focused introduction to Milvus — a production-ready, distributed vector database engineered for billion-scale AI retrieval and search applications.

If Weaviate is a well-organized shop for semantic search, Milvus is an industrial warehouse built to handle much larger capacity and throughput. First released in October 2019 as open source, Milvus was designed from day one with one priority: scale. It operates as a distributed system across multiple machines to reliably manage billions of high-dimensional vectors.

## Core capabilities

Milvus is optimized for large-scale vector search workloads and cloud-native deployments. Key capabilities include:

|                      Capability | What it delivers                                                                                                       |
| ------------------------------: | ---------------------------------------------------------------------------------------------------------------------- |
|       Cloud-native architecture | Designed for Kubernetes and orchestrated cloud environments, enabling scalable deployments and operational automation. |
| Billion-scale vector management | Consistent performance from millions up to billions of vectors through horizontal scaling.                             |
|               High availability | Clustered design with redundancy so services remain online despite node failures.                                      |
|    Distributed query processing | Parallelized search and filtering across worker nodes for lower latency and higher throughput.                         |
|     Hardware acceleration (GPU) | Optional GPU support for faster index building and high-throughput searches.                                           |
|             Multi-index support | Multiple index types (IVF, HNSW, PQ variants) to balance accuracy, memory, and latency.                                |

## Internal architecture overview

At a high level Milvus is organized into logical layers that separate concerns and enable scale:

| Layer              | Responsibility                                                                                        |
| ------------------ | ----------------------------------------------------------------------------------------------------- |
| Access layer       | Receives SDK/API requests, authenticates, and forwards requests to the coordinator.                   |
| Coordinator        | Schedules tasks, routes requests, manages metadata, and decides which worker nodes handle work.       |
| Worker nodes       | Store segments, build and maintain indexes, ingest vectors, and execute search and filter operations. |
| Persistent storage | External object storage (e.g., Amazon S3, MinIO) used for durable segment files and recovery.         |

<Frame>
  <img alt="The image provides an overview of Milvus, a scalable, distributed, open-source vector database, highlighting its core features and distributed architecture components." />
</Frame>

Coordinator components route incoming requests from the access layer to the appropriate worker nodes. Worker nodes do the heavy lifting — ingesting vector data, storing segment files, maintaining indexes, and executing vector search and filtering operations. Object storage such as S3 or MinIO persists segment files and other durable artifacts so nodes can recover or scale without data loss.

## Who uses Milvus?

* Enterprises that need full control over a scalable vector search infrastructure.
* Teams building large AI-driven applications that must scale from millions to hundreds of millions or billions of vectors.
* Organizations that require GPU acceleration for index building and large-scale search performance.

## What makes Milvus stand out?

* Horizontal scalability to billions of vectors with near-linear capacity growth as nodes are added.
* Flexible multi-indexing (IVF, HNSW, PQ variants) so you can choose the right tradeoff between memory, latency, and search accuracy.
* GPU acceleration for index building and search to support large models and high throughput.
* Active open-source community and enterprise support, driving integrations and continuous improvements.

Index choices (examples and tradeoffs):

| Index                                     | Best for                                        | Tradeoffs                                 |
| ----------------------------------------- | ----------------------------------------------- | ----------------------------------------- |
| IVF (Inverted File)                       | Balanced recall vs. speed for large datasets    | Requires training and tuning of centroids |
| HNSW (Hierarchical Navigable Small World) | High recall with low latency for many workloads | Higher memory footprint                   |
| PQ (Product Quantization)                 | Very high compression and reduced memory        | Lower recall vs exact indexes             |

<Frame>
  <img alt="The image is an infographic titled &#x22;Deep Dive: Milvus,&#x22; describing Milvus as a scalable, distributed, open-source vector database for AI applications. It highlights its core features, distributed architecture, target users, and key differentiators." />
</Frame>

## Scale perspective

Milvus is purpose-built to handle use cases ranging from millions of vectors up through hundreds of millions and into the billion-plus range. Its architecture ensures that performance can be maintained as the dataset grows, which makes Milvus a strong candidate for large-scale AI search and retrieval systems.

<Frame>
  <img alt="The image is an infographic about Milvus, detailing its features, target users, distributed architecture, and key differentiators. It highlights Milvus as a scalable, open-source vector database for large-scale AI applications." />
</Frame>

> **lightbulb** Choose Milvus when you need horizontal scale, advanced index options, and the ability to leverage GPU acceleration. For smaller projects or when you want a lighter setup with tighter semantic-search integrations out of the box, consider simpler vector stores or search engines.

That’s it for Milvus. Next, we'll compare vector databases and provide guidance on selecting the right platform for specific application needs.

## Links and references

* Milvus official site: [https://milvus.io/](https://milvus.io/)
* Kubernetes documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)
* Amazon S3: [https://aws.amazon.com/s3/](https://aws.amazon.com/s3/)
* MinIO: [https://min.io/](https://min.io/)
* Weaviate: [https://weaviate.io/](https://weaviate.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/4fee20e9-5def-4971-b7a9-9363aaeb73c2/lesson/abbe019f-862b-433b-ab13-24d10af129c3)
