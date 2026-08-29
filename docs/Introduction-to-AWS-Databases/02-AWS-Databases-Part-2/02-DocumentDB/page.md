# Example: arn:aws:iam::111122223333:role/my-administrator
```

Specify a master username and a strong password (for example `admin` + a strong password). If fine-grained access control is enabled, OpenSearch Dashboards will require these credentials on login.

<Frame>
  <img alt="A screenshot of the AWS OpenSearch domain creation page showing fine-grained access control enabled with a created master user (username &#x22;admin&#x22;) and a masked password, alongside a Summary panel listing engine version, data node, network and encryption settings." />
</Frame>

> **warning** Using public access makes your cluster reachable from the internet. For production use a VPC and restrictive security groups. Only use public access for short-lived demos.

Other optional settings: SAML or Amazon Cognito authentication, index-level access policies, encryption at rest and in transit, automatic software updates, and advanced cluster parameters. After reviewing settings, create the domain — provisioning typically takes 15–20 minutes.

***

## 2) Connect to the cluster

* When the domain status becomes **Active**, open domain details to find the **Cluster endpoint** and the **OpenSearch Dashboards URL**.
* Use the cluster endpoint for API calls and the Dashboards URL for the UI.
* Log in to OpenSearch Dashboards with the master username/password. On first login you’ll be prompted about tenants — the default Global tenant is fine for demos.

> **lightbulb** Keep your domain endpoint and master credentials private. Consider storing credentials in a secrets manager for repeatable scripts.

<Frame>
  <img alt="A screenshot of the Amazon OpenSearch Service console displaying the &#x22;demo&#x22; domain details — showing domain status (Active), cluster health (Green), OpenSearch version, and domain endpoint links. The left sidebar shows navigation for Managed clusters, Serverless, and other OpenSearch settings." />
</Frame>

***

## 3) Add sample data in OpenSearch Dashboards

1. Open OpenSearch Dashboards and choose **Add data**.
2. Select a sample dataset (e.g., Sample eCommerce orders, Sample flight data, or Sample web logs).
3. Click **Add data** to install the dataset and then **View Data** to open its dashboard and indices.

<Frame>
  <img alt="A screenshot of the OpenSearch Dashboards &#x22;Add sample data&#x22; page showing three sample dataset cards: Sample eCommerce orders, Sample flight data, and Sample web logs, each with preview visualizations and &#x22;Add data&#x22; buttons. The page header and navigation bar are visible at the top." />
</Frame>

After installing the eCommerce dataset, open its dashboard to review metrics and visualizations.

<Frame>
  <img alt="A screenshot of an OpenSearch eCommerce Revenue Dashboard showing key metrics and visualizations. It displays transactions per day (139), average order value (75.25), average items per order (2.163), total revenue (77,583.36) and charts for sales by gender and category." />
</Frame>

***

## 4) Inspect indices and mappings

* In OpenSearch Dashboards go to **Management → Index Management → Indices** to see indices created by the sample dataset.
* Select an index and open the **Mappings** tab to view defined fields and types. Reviewing mappings helps you plan queries, aggregations, and future index settings.

<Frame>
  <img alt="A screenshot of the OpenSearch Dashboards index detail view showing the &#x22;Mappings&#x22; tab for a sample ecommerce index. It lists field mappings in the Visual Editor (e.g., category, currency, customer_first_name, customer_id, geoip.continent_name)." />
</Frame>

***

## 5) Explore documents with Discover

* Open **Discover** in Dashboards, choose the correct index pattern for your dataset, and browse documents.
* Adjust the time range (e.g., last 7 days) and use the left-hand field list to filter or add fields to the display.
* Example: add filters for `manufacturer` = `Pyramid Distribution` and `days_of_week` = `Saturday` to show documents matching both conditions.

<Frame>
  <img alt="A screenshot of an OpenSearch Dashboards &#x22;Discover&#x22; view showing a histogram and filtered e-commerce log results: a left panel of available fields and a right pane listing JSON-like order records with highlighted terms." />
</Frame>

***

## 6) Indexing documents via the REST API (curl)

AWS documentation includes curl examples for indexing. Replace `admin`, `Password123!`, and the domain endpoint with your master username, password, and the domain endpoint URL.

Reference:

* [Amazon OpenSearch Service Developer Guide](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/)

### Index a single document (PUT)

Example PUT request to index one document into an index named `movies`:

```bash theme={null}
curl -XPUT -u 'admin:Password123!' 'https://search-demo-xxxxxxxxxxxx.us-east-1.es.amazonaws.com/movies/_doc/1' \
  -H 'Content-Type: application/json' \
  -d '{"director":"Burton, Tim","genre":["Comedy","Sci-Fi"],"year":1996,"actor":["Jack Nicholson","Pierce Brosnan","Sarah Jessica Parker"],"title":"Mars Attacks!"}'
```

Expected response (trimmed):

```json theme={null}
{"_index":"movies","_id":"1","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":0,"_primary_term":1}
```

### Bulk indexing (multiple documents)

1. Create a local file `bulk_movies.json` containing newline-delimited JSON (action/metadata line followed by the document source line for each item). Example `bulk_movies.json`:

```json theme={null}
{ "index" : { "_index": "movies", "_id" : "2" } }
{"director":"Frankenheimer, John","genre":["Drama","Mystery","Thriller","Crime"],"year":1962,"actor":["Lansbury, Angela","Sinatra, Frank"]}
{ "index" : { "_index": "movies", "_id" : "3" } }
{"director":"Baird, Stuart","genre":["Action","Crime","Thriller"],"year":1998,"actor":["Downey Jr., Robert","Jones, Tommy Lee"]}
{ "index" : { "_index": "movies", "_id" : "4" } }
{"director":"Ray, Nicholas","genre":["Drama","Romance"],"year":1955,"actor":["Hopper, Dennis","Wood, Natalie","Dean, James"],"title":"Rebel Without a Cause"}
```

Note: The bulk file must use newline-separated JSON lines and should end with a newline.

2. Call the bulk API:

```bash theme={null}
curl -XPOST -u 'admin:Password123!' 'https://search-demo-xxxxxxxxxxxx.us-east-1.es.amazonaws.com/_bulk' \
  --data-binary @bulk_movies.json \
  -H 'Content-Type: application/json'
```

Expected response (trimmed):

```json theme={null}
{"took":61,"errors":false,"items":[{"index":{"_index":"movies","_id":"2","result":"created"}},{"index":{"_index":"movies","_id":"3","result":"created"}},{"index":{"_index":"movies","_id":"4","result":"created"}}]}
```

***

## 7) Verify documents in Dashboards

* In OpenSearch Dashboards go to **Management → Index Patterns** and create an index pattern named `movies`.
* Open **Discover**, select the `movies` pattern, and search for terms (for example, `Downey Jr., Robert`) to validate newly indexed documents.

***

## 8) Clean up

To avoid ongoing charges, delete the OpenSearch domain when you finish:

* Open the OpenSearch console → Domains → select your domain → **Delete**.

***

## Links and references

* Amazon OpenSearch Service Developer Guide: [https://docs.aws.amazon.com/opensearch-service/latest/developerguide/](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/)
* OpenSearch project: [https://opensearch.org/](https://opensearch.org/)
* More on indexing and the Bulk API: [https://opensearch.org/docs/latest/opensearch/rest-api/bulk/](https://opensearch.org/docs/latest/opensearch/rest-api/bulk/)

This completes the lesson on provisioning an Amazon OpenSearch domain, using OpenSearch Dashboards with sample data, and indexing documents via the REST API.

- [Watch Video](https://learn.kodekloud.com/user/courses/introduction-to-aws-databases/module/6b775562-0b27-41e9-93fc-bb16dab05d87/lesson/167596e5-3d9c-4e78-8802-b343bff462ea)


# DocumentDB

Source: https://notes.kodekloud.com/docs/Introduction-to-AWS-Databases/AWS-Databases-Part-2/DocumentDB/page

Overview of Amazon DocumentDB, a managed MongoDB-compatible document database covering architecture, replication, scalability, global clusters, read preferences, and migration considerations.

In this lesson, we’ll cover Amazon DocumentDB — AWS’s managed, MongoDB-compatible document database. Learn what DocumentDB provides, how clusters and instances are organized, replication and read-scaling models, common use cases, and key operational considerations for migrating or running MongoDB workloads on AWS.

MongoDB is a widely used document (NoSQL) database known for flexible schemas and horizontal scalability. On AWS exams and in architecture discussions, remember that MongoDB is a NoSQL document database in the same broad category as Amazon DynamoDB, but running a production MongoDB cluster requires skills for scaling, backups, failover, and operations.

Amazon DocumentDB provides a managed MongoDB-compatible experience: AWS operates the underlying storage, replication, patching, and availability, similar to how Amazon RDS manages relational databases.

> **lightbulb** DocumentDB is MongoDB-compatible and works with many `MongoDB` drivers and tools. Always verify compatibility for the specific MongoDB driver version and features your application depends on before migrating.

## DocumentDB clusters: storage and instances

When you create a DocumentDB deployment you provision a cluster. A cluster separates storage from compute and consists of:

* A single cluster volume that manages the stored data for all instances in the cluster.
  * Uses cloud-native storage and replicates data six ways across three Availability Zones for high durability and availability.
  * Supports up to 64 TB of data.
* One or more instances (compute) that provide processing capacity for reads and writes to the shared cluster volume.
  * Instances read from and write to the cluster volume.
  * A cluster supports between 1 and 16 instances.

Instances can be provisioned or terminated independently and are not required to be the same instance class. This decoupling lets you scale compute without changing storage.

Table: Cluster components and behavior

| Component           | Purpose                       | Notes                                          |
| ------------------- | ----------------------------- | ---------------------------------------------- |
| Cluster volume      | Central storage for data      | Replicated 6x across 3 AZs; up to 64 TB        |
| Primary instance    | Handles reads and writes      | Exactly one primary per cluster                |
| Replica instance(s) | Dedicated read-only instances | Up to 15 replicas; CPU/memory serve reads only |
| Instance scaling    | Change compute independently  | Mix and match instance classes per cluster     |

### Instance roles

* Primary instance
  * Exactly one primary per cluster.
  * Supports reads and writes; performs data modifications to the cluster volume.
* Replica instances
  * Up to 15 replicas in addition to the primary.
  * Read-only: dedicated to serving read traffic against the cluster volume.

Because replication occurs at the storage (cluster volume) layer, compute instances don’t perform instance-to-instance replication work. That frees CPU and memory to serve application requests.

## Global clusters

DocumentDB global clusters allow low-latency, highly available global workloads:

* Replicate data automatically from the primary cluster to up to five secondary clusters in other AWS Regions.
* Use fast storage-based physical replication from the primary to secondaries.
* Let you scale secondary clusters independently (different instance counts or sizes) from the primary, enabling cost/performance trade-offs across regions.

Replication is handled by the storage layer, so compute instances in each region serve local application workloads and don’t participate in replication.

## Key features

* MongoDB compatibility: Many MongoDB drivers and tools work with DocumentDB, but confirm feature parity for your application.
* Storage auto-repair: Automatically detects failed segments of the cluster volume and reconstructs repaired segments using other replicas.
* Page cache (buffer pool) managed outside the main database process: The cache can survive a DB process restart, keeping the buffer pool warm and reducing recovery time.
* Fast crash recovery: Crash recovery runs asynchronously on a parallel thread so the database can be available quickly after a crash.
* Write durability: Writes are durably recorded on a majority of storage nodes before being acknowledged to clients.

<Frame>
  <img alt="A presentation slide titled &#x22;DocumentDB – Features&#x22; showing three colored feature cards labeled &#x22;MongoDB-Compatible,&#x22; &#x22;Storage Auto-Repair,&#x22; and &#x22;Cache Warming,&#x22; each with a small icon." />
</Frame>

> **warning** DocumentDB aims for MongoDB compatibility, but there are differences and unsupported features (e.g., some storage engine internals, specific server-side features). Test your application against DocumentDB in a staging environment before full migration.

## Replicas and read scaling

Replica instances are optimized for read scaling. Because replication is done at the cluster volume level, replica instances’ CPU and memory are dedicated to serving read operations. This architecture makes it easy to add or remove replicas to match read capacity and cost requirements.

Use replicas to:

* Offload read-heavy workloads from the primary.
* Serve analytic or reporting queries that can tolerate slightly stale data (depending on read preference).
* Distribute read traffic across Availability Zones for higher availability.

<Frame>
  <img alt="A slide titled &#x22;DocumentDB – Features&#x22; showing an AWS Cloud region with three Availability Zones, depicting one primary database instance and multiple replica instances. The diagram uses dotted boundaries and cylinder icons to illustrate a primary-replica deployment across zones." />
</Frame>

## Read preferences

DocumentDB supports MongoDB client-side read preferences so applications can tune consistency, latency, and throughput. Common read preferences:

* primary
  * Routes reads to the primary. If the primary is unavailable, reads fail.
* primaryPreferred
  * Prefer the primary but fall back to a secondary if the primary is unavailable.
  ```javascript theme={null}
  db.example.find().readPref('primaryPreferred')
  ```
* secondary
  * Routes reads to secondary replicas only. If no replicas are available, reads fail.
* secondaryPreferred
  * Prefer a secondary, but fall back to the primary if no secondary is available.
  ```javascript theme={null}
  db.example.find().readPref('secondaryPreferred')
  ```
* nearest
  * Routes reads to the instance with the lowest measured client latency.

Choose a read preference that aligns with your application’s requirements for consistency, latency, and durability.

## Common use cases

* Content management systems that benefit from flexible document schemas.
* User profiles, preferences, and session stores mapped naturally to documents.
* Read-scalable applications, including global low-latency reads using global clusters.
* Analytics or reporting workloads run against replica instances to avoid primary impact.

## Summary

Amazon DocumentDB is a fully managed, MongoDB-compatible document database that reduces the operational burden of running MongoDB workloads on AWS. Key advantages include:

* Storage replicated six ways across three Availability Zones for durability.
* Decoupled compute and storage so instances can be scaled independently.
* Global clusters for cross-region replication and low-latency reads.
* Client-side MongoDB read preferences to balance latency and consistency.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary DocumentDB&#x22; with a teal left panel. The right side lists short points about DocumentDB features—global clusters for multi-region deployment and read preferences for optimizing latency, throughput, or consistency." />
</Frame>

## Links and references

* Amazon DocumentDB overview: [https://aws.amazon.com/documentdb/](https://aws.amazon.com/documentdb/)
* MongoDB documentation: [https://www.mongodb.com/docs/](https://www.mongodb.com/docs/)
* MongoDB drivers and read preferences: [https://www.mongodb.com/docs/manual/core/read-preference/](https://www.mongodb.com/docs/manual/core/read-preference/)
* Amazon RDS (managed relational databases): [https://aws.amazon.com/rds/](https://aws.amazon.com/rds/)

- [Watch Video](https://learn.kodekloud.com/user/courses/introduction-to-aws-databases/module/6b775562-0b27-41e9-93fc-bb16dab05d87/lesson/efcc75fd-0c1f-40c1-b426-83f61f87c47e)
