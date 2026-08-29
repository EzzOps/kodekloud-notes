# Analyzing Data

Source: https://notes.kodekloud.com/docs/DP-900-Microsoft-Azure-Data-Fundamentals/Analyzing-Data/Analyzing-Data/page

This article covers tools and frameworks for analyzing data using Azure services, including querying, open-source engines, and integration with Azure HDInsight.

In this lesson of the Azure Data Fundamentals course, we'll cover the primary tools and frameworks for analyzing data once it’s been ingested and transformed with Azure Data Factory and stored in Azure Data Lake or Azure Synapse Analytics. You’ll learn how to query data efficiently, leverage open-source engines, and integrate these technologies using Azure HDInsight.

***

## Querying with Azure Synapse Data Explorer and Kusto Query Language

When your data resides in Azure Synapse, **Azure Synapse Data Explorer** (formerly known as Kusto) is the go-to tool for interactive queries. It uses **Kusto Query Language (KQL)**, which builds on many SQL concepts but offers simplified syntax for telemetry, logs, and time-series data.

```kql theme={null}
// Sample KQL query: Top 5 pages by view count
StormEvents
| where StartTime between (datetime(2021-01-01) .. datetime(2021-12-31))
| summarize Events=count() by State
| top 5 by Events desc
| render columnchart
```

> **lightbulb** KQL supports built-in visualizations—you can append `| render <chartType>` to your query to instantly produce charts.\
  Familiarity with SQL eases your transition, but KQL’s pattern matching and time-series operators are unique.

***

## Open-Source Analytics Engines

Azure provides first-class support for popular open-source data engines. You can run adhoc SQL, batch, or streaming workloads at scale.

| Engine                  | Description                                                                                    | Use Case                          |
| ----------------------- | ---------------------------------------------------------------------------------------------- | --------------------------------- |
| [Apache Spark][spark]   | Fast, in-memory analytics engine for batch and streaming, with SQL, Python, Scala, and R APIs. | Large-scale ETL, machine learning |
| [Apache Hadoop][hadoop] | Distributed storage and processing framework; integrates with HBase for NoSQL and wide-column. | Batch processing, HDFS compute    |

![The image lists two open-source tools: Apache Spark, an analytics engine for processing large data using SQL, and Apache Hadoop, which distributes analytic processing across multiple servers and works with HBase.](https://kodekloud.com/kk-media/image/upload/v1752872821/notes-assets/images/DP-900-Microsoft-Azure-Data-Fundamentals-Analyzing-Data/apache-spark-hadoop-analytics-tools.jpg)

If you prefer writing custom code over SQL or KQL, leverage languages such as **[R][r]** or **[Python][python]** for statistical analysis and data science workflows.

![The image lists open-source tools for data processing, including Apache Spark, Apache Hadoop, and programming languages like R and Python.](https://kodekloud.com/kk-media/image/upload/v1752872822/notes-assets/images/DP-900-Microsoft-Azure-Data-Fundamentals-Analyzing-Data/open-source-data-processing-tools-list.jpg)

***

## Integrating Tools with Azure HDInsight

When your analytics solution combines multiple open-source frameworks, **[Azure HDInsight][hdinsight]** offers a fully managed cluster service. You can mix and match:

| Component               | Role                          |
| ----------------------- | ----------------------------- |
| [Apache Spark][spark]   | In-memory analytics           |
| \[Apache Hive]\[hive]   | SQL-based data warehousing    |
| \[Apache Kafka]\[kafka] | Real-time stream ingestion    |
| [Hadoop][hadoop]        | Distributed storage & compute |

![The image describes HDInsight as a framework for combining open-source tools like Apache Spark, Apache Hive, Kafka, and Hadoop, with their logos displayed.](https://kodekloud.com/kk-media/image/upload/v1752872823/notes-assets/images/DP-900-Microsoft-Azure-Data-Fundamentals-Analyzing-Data/hdinsight-open-source-tools-logos.jpg)

> **lightbulb** HDInsight clusters can auto-scale and integrate with Azure Active Directory for secure, enterprise-grade deployments.

***

## Choosing the Right Analytics Platform

As your analytics requirements evolve, consider purpose-built, fully integrated platforms:

* **[Azure Synapse Analytics][synapse]** – Unified experience for data warehousing, big data, and data integration.
* **[Azure Databricks][databricks]** – Optimized Apache Spark environment with collaborative notebooks and ML integration.

***

## Links and References

* [Apache Spark][spark]
* [Apache Hadoop][hadoop]
* [R Project][r]
* [Python][python]
* [Azure Synapse Analytics][synapse]
* [Azure Databricks][databricks]
* [Azure HDInsight][hdinsight]
* [Kusto Query Language Overview][kql]

[spark]: https://spark.apache.org/

[hadoop]: https://hadoop.apache.org/

[r]: https://www.r-project.org/

[python]: https://www.python.org/

[synapse]: https://azure.microsoft.com/services/synapse-analytics/

[databricks]: https://azure.microsoft.com/services/databricks/

[hdinsight]: https://azure.microsoft.com/services/hdinsight/

[kql]: https://docs.microsoft.com/azure/data-explorer/kusto/query/overview

- [Watch Video](https://learn.kodekloud.com/user/courses/dp-900-microsoft-azure-data-fundamentals/module/a4f1a604-4743-4a3a-81ac-8210d6f9bb96/lesson/de652741-32d1-4f45-b195-789eca6e05cd)
