# Legacy Use Cases

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/GCP-Core-Fundamentals-Understanding/Legacy-Use-Cases/page

Discusses modernizing decades-old insurance data systems, challenges of legacy on-premises stacks, and migration strategies to cloud-native streaming, governance, and observability.

Welcome back. This article dives into a common—and often intimidating—challenge for data engineers: legacy use cases. These are systems that have run for a decade or more and that teams are reluctant to change. Using a fictional enterprise, Blue Shield Insurance Corporation, we’ll walk through how their data landscape evolved, the technical constraints that accumulated over time, and why modernization requires more than a straight “lift-and-shift” to cloud.

We’ll cover three perspectives:

* Industry context and scale
* Historical data footprint and on‑premises systems
* Business needs that drove the demand for modernization

Industry context and scale
Blue Shield is a large, global insurer operating across 20+ countries. They manage policies for over 50 million policyholders and process millions of claims annually. Every policy, claim, and customer interaction generates logs, transaction records, and reporting artifacts. Over decades, this led to a layered environment combining legacy mainframes, relational databases, and newer components—creating an increasingly complex data estate.

<Frame>
  <img alt="Slide titled &#x22;Large Insurance Company – Data Landscape&#x22; with panels for Industry and Size, Data Footprint and Business Needs, and three metric cards noting 20+ countries, 50 million policyholders, and millions of claims processed annually." />
</Frame>

Historical footprint and on‑premises systems
Blue Shield retains 30–40 years of customer, claims, and risk data—some records date back to floppy‑disk era systems. The core storage and processing was built around on‑premises Oracle databases and mainframes, with ETL jobs moving and cleaning data between systems. Those systems were resilient for their era, but they are difficult to scale and expensive to maintain.

<Frame>
  <img alt="A presentation slide titled &#x22;Large Insurance Company – Data Landscape&#x22; with left-side panels for Industry and Size, Data Footprint, and Business Needs. The main area shows boxes for decades of data (Customers, Claims, Risk Data) and underlying data sources (On‑Premises Oracle Database, Mainframes, ETL Jobs)." />
</Frame>

Evolving business needs and regulatory pressure
Business priorities shifted from daily/overnight reporting to near‑real‑time insights—fraud detection, improved risk modeling, and personalized customer experiences all depend on low‑latency data. Extracting timely intelligence from mainframes and batch ETL is impractical without substantial architectural change. At the same time, increasingly strict regulatory requirements (audit trails, security, cross‑border data governance) added further constraints.

<Frame>
  <img alt="A slide titled &#x22;Large Insurance Company – Data Landscape&#x22; showing three left-side boxes (Industry and Size, Data Footprint, Business Needs) and a central panel highlighting priorities like Real-Time Insights (fraud detection, risk modelling, customer personalization) and increased regulatory pressure (audit trails, security, data governance)." />
</Frame>

Legacy data engineering stack (high level)
Below is a concise summary of the production stack Blue Shield relied on before modernizing. These components were coherent in their time but accumulated technical debt and operational rigidity.

* Data ingestion: multiple sources (CRM, mainframes, relational DBs, Kafka) fed an in‑house ingestion tool.
* Central processing: a 140‑node on‑premises Hadoop cluster was the primary batch engine for large‑volume transforms.
* Fast access layer: processed data was pushed to a NoSQL database acting as a cache for low‑latency reads.
* Batch tooling: Pig scripts and Hive queries implemented most ETL/transform logic—optimized for batch throughput, not low latency.
* BI & reporting: Tableau dashboards surfaced analytics, often reflecting data hours or days old.
* Monitoring: Zabbix provided server and host monitoring but lacked deep pipeline observability for multi‑stage distributed workflows.

<Frame>
  <img alt="A diagram titled &#x22;Legacy Data Engineering Architecture&#x22; showing data sources (DB, CRM, Mainframe, Kafka) feeding a Data Ingestion layer into a 140-node Hadoop cluster and NoSQL DB. Pig and Hive jobs handle processing, Zabbix provides monitoring, and Tableau is used for visualization." />
</Frame>

Common pain points and architectural consequences
This stack delivered business value for many years but exhibits classic legacy drawbacks:

* Strong hardware dependency and expensive scale‑up operations
* Batch‑only workflows that create stale insights for time‑sensitive use cases
* Fragile maintenance processes and high operational burden (specialized talent required)
* Single points of failure (e.g., master nodes in Hadoop)
* Limited observability across long, multi‑stage pipelines
* Difficulty integrating modern streaming and real‑time analytics tools

Table: Legacy components and primary challenges

| Legacy component                |                                      Role | Primary challenge                                                    |
| ------------------------------- | ----------------------------------------: | -------------------------------------------------------------------- |
| On‑premises Oracle / Mainframes | Source of truth and transactional systems | Closed systems, limited streaming capability, costly to scale        |
| 140‑node Hadoop cluster         |                  Central batch processing | Hardware-bound, slow job turnaround, single points of failure        |
| Pig / Hive jobs                 |                  Batch ETL and transforms | Designed for throughput, not low latency; hard to maintain over time |
| NoSQL DB (fast cache)           |                         Low-latency reads | Adds operational complexity and potential data staleness             |
| In‑house ingestion tool         |      Data collection from diverse sources | Hard to extend and maintain as sources evolve                        |
| Tableau dashboards              |                          BI and reporting | Visualizes stale data; not ideal for operational analytics           |
| Zabbix monitoring               |                 Infrastructure monitoring | Limited pipeline-level observability and lineage tracking            |

Key takeaway: modernization is not merely moving workloads to a cloud provider. It demands rethinking data flow, carefully handling long-lived historical datasets, and adopting combined streaming + batch patterns with improved governance and observability.

<Callout icon="lightbulb">
  Modernization is not only about adopting cloud services. It’s also about resolving decades of data design choices—reconciling historical data formats, decoupling tightly coupled systems, and improving observability and governance.
</Callout>

What this article will cover next
The remainder of this lesson maps each legacy component to cloud‑native alternatives (focusing on Google Cloud Platform), outlines trade‑offs, and discusses migration strategies—how to preserve historical data, introduce streaming where it matters, and add observability and governance controls that scale.

Links and references

* [Google Cloud Platform documentation](https://cloud.google.com/docs)
* [Apache Hadoop](https://hadoop.apache.org/)
* [Tableau product documentation](https://help.tableau.com/)

That wraps up this lesson. Subsequent material will map this legacy stack to cloud services and present migration patterns and best practices.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/54d4f17c-56da-41a4-b998-2a2c63f0ee3f/lesson/6527c740-98d0-43ca-9e5a-67a8494984b5" />
</CardGroup>
