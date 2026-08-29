# Neptune

Source: https://notes.kodekloud.com/docs/Introduction-to-AWS-Databases/AWS-Databases-Part-2/Neptune/page

Overview of Amazon Neptune, a fully managed graph database service for high-performance graph queries, global deployments, serverless scaling, and graph machine learning integrations.

In this lesson we'll explore Amazon Neptune, a fully managed graph database service for building applications that work with highly connected data. Neptune is optimized for graph traversals, supports graph-aware machine learning, and integrates with other AWS services for analytics and automation.

Why use a graph database?

Graph databases are purpose-built for modeling relationships as first-class citizens. They make it simple and efficient to represent and query connections between entities — something relational databases can struggle with when relationships are deep or highly connected.

A helpful analogy is a police investigation board: documents, photos, suspects, and evidence are pinned up and linked with lines. Those lines (relationships) are often the most important data. Graph databases model those relationships directly, so traversals and pattern queries are fast and expressive.

What is Amazon Neptune?

Amazon Neptune is a fully managed, high-performance graph database service. It removes operational overhead (backups, patching, scaling) and supports both provisioned and serverless deployment options so you can match capacity to workload patterns. Neptune supports the two primary graph models:

* Property Graph (Apache TinkerPop Gremlin and openCypher in supported setups)
* RDF (W3C SPARQL)

Neptune integrates with services such as AWS Glue, Amazon SageMaker, AWS Lambda, Amazon Athena, AWS Database Migration Service, and AWS Backup to support ingestion, analytics, and ML workflows.

Neptune Global Database

Neptune supports global deployments via Neptune Global Database. You can deploy a primary Neptune cluster in one AWS Region and asynchronously replicate data to up to five secondary read-only clusters in other Regions. This provides low-latency reads around the world and enhances availability in case of regional disruptions.

<Callout icon="warning">
  Neptune Global Database secondaries are read-only. All writes must go to the primary cluster; those writes are asynchronously replicated to secondaries for read scalability and geographic distribution.
</Callout>

<Frame>
  <img alt="A diagram of AWS Neptune Global Database showing a primary region (P) and multiple secondary regions (S) on a world map. A detailed schematic on the right shows a primary DB cluster (writer/reader + reader) in US West and a secondary DB cluster (readers) in US East with storage replication between them." />
</Frame>

Neptune Serverless

Neptune Serverless is an on-demand deployment option that automatically adjusts database capacity to match your application's needs. It removes the need to provision and manage instances, letting you pay for capacity consumed. Serverless is ideal for variable or unpredictable workloads and for development/test environments where cost efficiency is important.

For details, see the Neptune Serverless docs: [https://docs.aws.amazon.com/neptune/latest/userguide/neptune-serverless.html](https://docs.aws.amazon.com/neptune/latest/userguide/neptune-serverless.html)

Neptune ML

Neptune ML applies graph neural networks (GNNs) and other graph-aware machine learning techniques to Neptune data. It automates graph feature engineering and model training, often using Amazon SageMaker, so you can build models for tasks like link prediction, node classification, or recommendations directly from your graph datasets.

<Callout icon="lightbulb">
  Neptune ML leverages GNNs to extract structure-aware features and typically uses SageMaker for training. This approach often yields better predictive accuracy on graph problems than non-graph methods.
</Callout>

<Frame>
  <img alt="A slide titled &#x22;Amazon Neptune – ML&#x22; with two rounded panels: the left highlights &#x22;Graph Neural Networks (GNNs)&#x22; with a neural circuit icon, and the right shows &#x22;Fast and Accurate Predictions&#x22; with a stopwatch/speed icon." />
</Frame>

Key features

| Feature                        | Description                                                               | Example / Link                                                                                         |
| ------------------------------ | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Deployment options             | Choose provisioned clusters or serverless to match workload patterns      | See Neptune Serverless: `https://docs.aws.amazon.com/neptune/latest/userguide/neptune-serverless.html` |
| Performance                    | High throughput and low latency for traversals and graph queries          | Ideal for deep relationship queries                                                                    |
| Storage auto-scaling           | Auto-resizes storage to accommodate growth without manual intervention    | No need to pre-allocate storage                                                                        |
| Read replicas                  | Horizontal read scaling and low-latency reads                             | Supports read replicas for high read throughput                                                        |
| Graph models & query languages | Supports Property Graph (Gremlin, openCypher) and RDF (SPARQL)            | `https://tinkerpop.apache.org/`, `https://www.w3.org/TR/rdf-sparql-query/`                             |
| Integration                    | Integrates with AWS Glue, SageMaker, Lambda, Athena, DMS, AWS Backup      | Useful for ETL, ML, serverless triggers, analytics                                                     |
| Security                       | VPC isolation, IAM authentication, encryption at rest, SSL/TLS in transit | Meets enterprise security requirements                                                                 |

Common use cases

| Use case                          | Why Neptune fits                                                                   |
| --------------------------------- | ---------------------------------------------------------------------------------- |
| Identity graphs / Customer 360    | Unite customer data across systems to enable personalization and unified profiles  |
| Fraud detection                   | Model multi-hop relationships to detect complex fraud patterns across entities     |
| Recommendations & personalization | Graph traversals and GNNs power item and social recommendations                    |
| IT ops & dependency analysis      | Map infrastructure components and dependencies for impact analysis and root cause  |
| Graph ML                          | Use Neptune ML to prepare features and train models for graph-specific predictions |

<Frame>
  <img alt="A presentation slide titled &#x22;Neptune – Use Cases&#x22; showing three colored cards: &#x22;Personalization With Customer 360,&#x22; &#x22;Detect Fraud Patterns,&#x22; and &#x22;ML Predictions.&#x22; Each card has a matching icon (user targeting, fraud alert on a monitor, and a brain with circuit lines)." />
</Frame>

Best practices and considerations

* Choose the deployment model (provisioned vs serverless) based on traffic patterns and cost sensitivity.
* Use read replicas and Global Database to serve low-latency reads across regions.
* For ML use cases, export graph data through Neptune ML workflows and use SageMaker for scalable training.
* Secure your cluster with VPC isolation, IAM authentication, and encryption to meet compliance and organization security policies.
* Monitor performance and queries using Amazon CloudWatch and query profiling to optimize traversals and indexing.

Summary

Amazon Neptune is a fast, reliable, fully managed graph database service engineered for complex, highly connected datasets. It supports Property Graph and RDF models, provides flexible deployment options (including serverless), enables global reads through Neptune Global Database, and integrates with Neptune ML for graph-based machine learning. Neptune automates operational tasks so teams can focus on building graph applications that scale and deliver intelligent insights.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary Neptune&#x22; with a turquoise panel on the left and numbered icons down the right. The text summarizes Neptune as a fast, fully managed graph database that automates admin tasks and supports Property Graph and RDF query languages." />
</Frame>

Neptune Global Database combined with Neptune ML enables globally distributed, high-performance graph applications that can also take advantage of graph machine learning for better predictions and insights.

Links and references

* Amazon Neptune: [https://aws.amazon.com/neptune/](https://aws.amazon.com/neptune/)
* Neptune Serverless docs: `https://docs.aws.amazon.com/neptune/latest/userguide/neptune-serverless.html`
* Apache TinkerPop (Gremlin): [https://tinkerpop.apache.org/](https://tinkerpop.apache.org/)
* openCypher: [https://opencypher.org/](https://opencypher.org/)
* SPARQL (W3C): [https://www.w3.org/TR/rdf-sparql-query/](https://www.w3.org/TR/rdf-sparql-query/)
* AWS Glue: [https://aws.amazon.com/glue/](https://aws.amazon.com/glue/)
* Amazon SageMaker: [https://aws.amazon.com/sagemaker/](https://aws.amazon.com/sagemaker/)
* AWS Lambda: [https://aws.amazon.com/lambda/](https://aws.amazon.com/lambda/)
* Amazon Athena: [https://aws.amazon.com/athena/](https://aws.amazon.com/athena/)
* AWS Database Migration Service: [https://aws.amazon.com/dms/](https://aws.amazon.com/dms/)
* AWS Backup: [https://aws.amazon.com/backup/](https://aws.amazon.com/backup/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-aws-databases/module/6b775562-0b27-41e9-93fc-bb16dab05d87/lesson/698a3428-13a2-4787-9f54-0127d218eaa1" />
</CardGroup>
