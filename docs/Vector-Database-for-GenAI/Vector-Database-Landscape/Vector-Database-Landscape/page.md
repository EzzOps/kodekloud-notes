# Vector Database Landscape

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Database-Landscape/Vector-Database-Landscape/page

Survey of vector database options, categories, representative projects, trade-offs, and key decision factors for selecting open-source, cloud-managed, or commercial vector search solutions

Welcome back. This lesson surveys the vector database landscape to help you pick the right option when building projects that require vector search or similarity search. There are many choices—and different operational models and trade-offs—so this guide groups them, highlights representative projects, and lists the key decision factors you should evaluate. Later lessons include deeper dives into several popular systems.

<Callout icon="lightbulb">
  Open-source typically means you self-host and operate the software (you control the code, configuration, and upgrades). Managed/cloud services reduce operational overhead but often incur ongoing costs. Commercial vendors may offer both open-source and managed variants—always check licensing, feature sets, and hosting options when comparing projects.
</Callout>

## Categories at a glance

Vector databases commonly fall into three categories:

| Category                       | What it means                                                         | Pros                                                                 | Cons                                                                         | Representative examples                                                                                                              |
| ------------------------------ | --------------------------------------------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Open-source / Self-hosted      | You run and maintain the system on-premises or in your cloud account. | Full control, no vendor lock-in, customizable code/configuration.    | You handle deployment, scaling, upgrades, backups, security, and monitoring. | [Milvus](https://milvus.io/), [Chroma](https://www.trychroma.com/), [Qdrant](https://qdrant.tech/), [Weaviate](https://weaviate.io/) |
| Cloud-managed / Cloud-native   | Vendor or cloud provider operates the infrastructure for you.         | Minimal ops overhead, built-in scaling, monitoring, often SLAs.      | Higher recurring cost, less low-level control, potential vendor lock-in.     | [AWS OpenSearch](https://aws.amazon.com/opensearch-service/), [Qdrant Cloud](https://qdrant.cloud/), managed Milvus, Weaviate Cloud  |
| Commercial / Enterprise (SaaS) | Fully-managed, production-ready services with enterprise features.    | Turnkey operation, enterprise support, optimizations for production. | Cost and potential vendor lock-in; pricing and features vary.                | [Pinecone](https://www.pinecone.io/), enterprise offerings from Zilliz (Milvus), Weaviate Enterprise                                 |

<Frame>
  <img alt="The image outlines different vector database options categorized into Open-Source (Self-Hosted), Cloud-Native (Managed Services), and Commercial/Enterprise (Paid Solutions), listing examples under each category." />
</Frame>

## Detailed category notes

* Open-source / self-hosted
  * Description: You deploy and operate the database yourself (on-prem or in your cloud account). You can modify source code and tune infrastructure to fit requirements.
  * When to choose: You need full control, strict compliance, custom features or on-prem deployments.
  * Trade-offs: Requires dedicated DevOps effort for scaling, backups, monitoring, and upgrades.

* Cloud-managed / cloud-native
  * Description: A vendor/cloud provider operates the service; you interact via APIs/SDKs.
  * When to choose: You want to minimize operational overhead and focus on application logic.
  * Trade-offs: You trade some control for convenience and pay recurring costs.

* Commercial / enterprise (SaaS)
  * Description: Turnkey vector search with enterprise SLAs, advanced tooling, and support.
  * When to choose: You need rapid production deployment with guaranteed support, security, and compliance.
  * Trade-offs: Price and long-term vendor dependency.

<Callout icon="warning">
  Some projects appear in multiple categories (open-source core + managed/enterprise offerings). When evaluating, verify the licensing, hosted options, and feature parity between open-source and paid versions to avoid unexpected limitations.
</Callout>

## A few important clarifications

* Projects often span categories:
  * Milvus is an open-source project (maintained by Zilliz) and also available as a managed/enterprise offering.
  * Weaviate and Qdrant provide both open-source software and managed cloud services.
* Pinecone is primarily a commercial SaaS vector database (managed service) rather than an open-source project.
* Compare vendors on technical features and operational guarantees. Important dimensions include:
  * Indexing algorithms (e.g., HNSW, IVF, PQ)
  * Distance metrics supported (cosine, dot-product, L2)
  * Metadata filtering and query capabilities
  * Hybrid search (dense vectors + sparse retrieval)
  * Vector compression/quantization approaches
  * Throughput, latency, and scalability (sharding/replication)
  * Durability, backups, and recovery semantics
  * SDKs, language support, and ecosystem connectors
  * Pricing model, SLAs, compliance, and enterprise support

## Key decision factors

When choosing a vector database, prioritize the items below based on your product and operational requirements:

| Decision area             | Questions to ask                                                                                                                       |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Scale & performance       | What latency and throughput requirements do you have? How many vectors and what dimensionality (e.g., 1536, 2048)?                     |
| Operational model         | Do you prefer self-hosting (control) or a fully managed service (less ops)?                                                            |
| Features & search types   | Do you need metadata filtering, hybrid search, approximate algorithms (HNSW/IVF), or vector compression (PQ)?                          |
| Integration & SDKs        | Which languages and frameworks do you need? Does the vendor provide connectors to your stack (e.g., Elasticsearch, PostgreSQL, Kafka)? |
| Cost & support            | What is your budget and required SLA? Do you need enterprise support or compliance certifications?                                     |
| Extensibility & licensing | Can you extend the engine (plugins/extensions)? Is the license compatible with your usage?                                             |

## Recommended evaluation checklist

* Run a small proof-of-concept with realistic data volumes and query patterns.
* Measure latency and recall for your indexed data and query types.
* Validate metadata filtering and complex query behavior.
* Test scaling behavior (index building, rebalancing, replica handling).
* Verify backup/restore workflows and failover behavior.
* Audit security, access controls, and compliance features.

## Further reading & references

* [Milvus documentation](https://milvus.io/)
* [Chroma](https://www.trychroma.com/)
* [Qdrant documentation](https://qdrant.tech/)
* [Weaviate documentation](https://weaviate.io/)
* [Pinecone](https://www.pinecone.io/)
* [AWS OpenSearch Service](https://aws.amazon.com/opensearch-service/)

A later lesson includes a deep dive into Pinecone—one of the widely used commercial vector databases—to examine its architecture, performance characteristics, and integration patterns in production.

See you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/4fee20e9-5def-4971-b7a9-9363aaeb73c2/lesson/837520a2-fe88-4826-bbff-28c2b719359e" />
</CardGroup>
