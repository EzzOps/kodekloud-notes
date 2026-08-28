# Key Features of S3 Vector Buckets

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Building-Vector-Storage-on-AWS-S3/Key-Features-of-S3-Vector-Buckets/page

Overview of AWS S3 Vector Buckets' features, scale limits, similarity search, metadata filtering, serverless billing, integrations, and security for production vector search workflows.

Welcome back. This lesson explains the core capabilities, limits, and tunable options of AWS S3 Vector Buckets so you understand what they provide and how to apply them for production vector search workflows.

Big picture: S3 Vector Buckets are purpose-built, serverless vector storage with built-in similarity search. They are distinct from standard S3 buckets and optimized for storing and querying vector embeddings at scale.

First: Vector buckets and indexes

* S3 Vector Buckets introduce a new bucket type dedicated to vector data. These are separate from standard S3 buckets—designed, indexed, and managed specifically for vector workloads.
* By default, a single vector bucket supports up to 10,000 vector indexes (quota-based; request increases through AWS Service Quotas may be possible).
* Each index can hold up to 2 billion vectors (subject to service limits and quotas).
* Across an entire bucket the default general-availability ceiling is up to 20 trillion vectors (account-, region-, and quota-dependent).
* These per-index and per-bucket limits provide a very large scale ceiling suitable for enterprise AI and retrieval applications.

Limits summary

| Resource                  |        Default limit | Notes                                                    |
| ------------------------- | -------------------: | -------------------------------------------------------- |
| Vector indexes per bucket |             `10,000` | Quotas subject to increase via AWS Service Quotas        |
| Vectors per index         |      `2,000,000,000` | Subject to service limits                                |
| Total vectors per bucket  | `20,000,000,000,000` | Account/region quotas may apply                          |
| Top-K results per query   |                `100` | Default with typical top-10 or top-50 common in web apps |

Second: Similarity search

* Native similarity search is the core capability: perform semantic nearest-neighbor queries directly over embeddings stored in the bucket.
* Typical latencies for well-cached or frequently accessed indexes can be sub-100 ms; colder or more complex queries are often sub-second. Actual latency depends on index configuration, query complexity, and workload characteristics.
* Supported distance metrics include cosine and Euclidean, letting you pick the metric that best matches your embedding model and retrieval objective.
* Top-k search supports returning up to 100 results per query by default, allowing multiple ranked matches (e.g., top 10 most relevant documents).

Third: Metadata filtering

* Each vector can include up to 50 metadata key-value pairs (constraints on per-key and overall metadata size still apply).
* Supported metadata types: string, number, boolean, and list.
* You can combine metadata filters with similarity search in a single query. That enables results scoped by project, user, date range, or other attributes while still returning semantically similar matches.
* Example: services like [Supabase](https://supabase.com) can restrict semantic search results to a specific project or user in the same query, which is useful for multi-tenant applications and RBAC scenarios.

<Frame>
  <img alt="The image is an infographic titled &#x22;S3 Vector Buckets – Key Features,&#x22; detailing features of vector buckets and indexes, including similarity search and metadata filtering capabilities. Each section outlines specific functionalities and specifications related to vector data management and search efficiency." />
</Frame>

Fourth: Serverless and pay-as-you-go model

* S3 Vector Buckets are fully serverless: there is no cluster or VM provisioning required, and no manual cluster tuning.
* The service auto-optimizes data layout and indexing for price/performance behind the scenes.
* Billing is usage-based: you pay for PUTs, storage, and queries (there are no separate cluster-hour charges).
* The service provides strong write consistency, so newly ingested vectors are generally queryable immediately—important for streaming or high-ingest pipelines.

Fifth: AWS service integration
S3 Vector Buckets integrate tightly with the AWS ecosystem, simplifying retrieval-augmented generation (RAG) and ML workflows:

* Native integration with [AWS Bedrock](https://aws.amazon.com/bedrock/) Knowledge Bases helps power RAG applications without custom glue code.
* Export or integrate with [Amazon OpenSearch Service](https://aws.amazon.com/opensearch-service/) for advanced search features and analytics.
* Work with [Amazon SageMaker](https://aws.amazon.com/sagemaker/) (Unified Studio) to combine vector retrieval with model training and evaluation.
* Manage resources and automation using [AWS CloudFormation](https://aws.amazon.com/cloudformation/).
* Secure connectivity with [AWS PrivateLink](https://aws.amazon.com/privatelink/) and enforce permissions through [AWS IAM](https://aws.amazon.com/iam/).

Sixth: Security and access control

* Vector buckets use a dedicated set of IAM actions and resource types for vector-specific permissions, keeping vector ACLs separate from standard S3 policies.
* Data at rest can be encrypted using `SSE-S3` or `SSE-KMS` (including customer-managed keys through KMS).
* Public access block is enabled by default for vector buckets to reduce accidental public exposure.
* Service Control Policies (SCPs) are supported to enforce organization-wide governance.

<Callout icon="lightbulb">
  Security notes: S3 Vector Buckets separate vector permissions from standard S3 and enable public access block by default. Use IAM, SCPs, and `SSE-KMS` when customer-managed keys are required for compliance.
</Callout>

Recap: Six key features to remember

1. Dedicated vector bucket type and massive scale (indexes, per-index and per-bucket limits; quotas may be adjusted).
2. Native, low-latency similarity search with cosine and Euclidean distance metrics.
3. Rich metadata filtering combined with similarity queries.
4. Serverless, auto-optimized, pay-as-you-go model with strong write consistency.
5. Deep AWS integrations (Bedrock, OpenSearch, SageMaker, CloudFormation, PrivateLink, IAM).
6. Dedicated security controls, encryption options, and enforced public access block.

Next steps
A follow-up lesson will demonstrate how to load embeddings into an S3 Vector Bucket, persist them, and run similarity-and-filter searches to retrieve and rank results.

Links and References

* [AWS Bedrock](https://aws.amazon.com/bedrock/)
* [Amazon OpenSearch Service](https://aws.amazon.com/opensearch-service/)
* [Amazon SageMaker](https://aws.amazon.com/sagemaker/)
* [AWS CloudFormation](https://aws.amazon.com/cloudformation/)
* [AWS PrivateLink](https://aws.amazon.com/privatelink/)
* [Supabase](https://supabase.com)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/afa51fbf-32d5-4459-a9de-0a764b24682b/lesson/c593c978-cfbb-4777-91f1-988d076c8e2a" />
</CardGroup>
