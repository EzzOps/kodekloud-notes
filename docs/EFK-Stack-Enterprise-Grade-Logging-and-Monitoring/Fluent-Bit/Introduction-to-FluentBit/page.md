# Input section: Collect Nginx logs from the access log file
[INPUT]
  Name   tail
  Path   /var/log/nginx/access.log
  Tag    nginx.access
  Parser nginx

# Filter section: Filter only the logs that include error messages
[FILTER]
  Name  grep
  Match nginx.access
  Regex message error

# Output section: Send the filtered logs to Elasticsearch for analysis
[OUTPUT]
  Name  es
  Match *
  Host  127.0.0.1
  Port  9200
  Index fluentbit
  Type  _doc
```

This configuration instructs Fluent Bit to continuously collect logs with the Tail plugin, process them with the Grep plugin by filtering error messages, and finally send the output to Elasticsearch using the ES plugin.

## Conclusion

Fluent Bit’s powerful architecture based on input, filter, and output plugins provides a scalable and flexible solution for log collection and processing. Mastering these components will enable you to build efficient logging pipelines tailored to your environment. For more details on log management solutions and best practices, explore the resources below:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Elasticsearch Documentation](https://www.elastic.co/guide/index.html)
* [Fluent Bit Documentation](https://docs.fluentbit.io/)

Thank you for reading this article. Stay tuned for more deep dives into advanced log processing and monitoring solutions!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/efk-stack-enterprise-grade-logging-and-monitoring/module/fde8c25d-412a-4b83-95dd-b2a21ea186f3/lesson/0614c267-ecec-47e3-9f30-bf9102236569" />
</CardGroup>


# Introduction to FluentBit

Source: https://notes.kodekloud.com/docs/EFK-Stack-Enterprise-Grade-Logging-and-Monitoring/Fluent-Bit/Introduction-to-FluentBit/page

This article explores modern log management, comparing Logstash and Fluent Bit, and highlights Fluent Bits efficiency in resource-constrained environments.

Welcome to our deep dive into modern log management and analysis. In this article, we explore key aspects of logging architectures while comparing two critical tools: Logstash and Fluent Bit.

## The Role of Logstash in the EFK Stack

Logstash is a cornerstone component of the EFK (Elasticsearch, Fluentd/Fluent Bit, Kibana) stack, renowned for its ability to ingest, transform, and route data from diverse sources. Organizations around the world rely on Logstash for its robust log processing flows and its capacity to manage complex log data architectures.

## Comparing Logstash and Fluent Bit

Understanding the strengths and differences between Logstash and Fluent Bit is crucial:

* **Architectural Differences**: Logstash offers extensive plugin options and a mature ecosystem, while Fluent Bit is a lightweight, efficient log shipper.
* **Plugin Ecosystems**: Both tools support a range of plugins for different scenarios, but Fluent Bit is often chosen for its optimized performance in high-throughput, low-resource environments.
* **Performance Considerations**: Fluent Bit is particularly favored in edge computing and containerized setups due to its resource efficiency.

## Spotlight on Fluent Bit

Fluent Bit is designed for scenarios where lightweight, high-performance log shipping is necessary. It excels in environments demanding low resource usage while still delivering high throughput.

<Frame>
  ![The image features the Fluent Bit logo with a colorful bird design, accompanied by text highlighting its features: "Lightweight Lock Shipper Design," "Resource Efficiency," "Optimized for High Throughput," and "Low Resource."](https://kodekloud.com/kk-media/image/upload/v1752874213/notes-assets/images/EFK-Stack-Enterprise-Grade-Logging-and-Monitoring-Introduction-to-FluentBit/fluent-bit-logo-bird-design.jpg)
</Frame>

<Callout icon="lightbulb">
  Fluent Bit is especially suitable for edge computing, where resource constraints are common, and speed is essential.
</Callout>

## Core Components of Fluent Bit

Fluent Bit’s architecture is built around three main components:

* **Input Plugins**: Capture log data from various sources.
* **Filter Plugins**: Process and modify log entries.
* **Output Plugins**: Forward processed logs to desired destinations.

These components enable the creation of flexible and efficient log processing pipelines.

<Frame>
  ![The image shows the Fluent Bit logo with options for "Input," "Filter," "Plugins," and "Log Processing Pipeline" below it.](https://kodekloud.com/kk-media/image/upload/v1752874214/notes-assets/images/EFK-Stack-Enterprise-Grade-Logging-and-Monitoring-Introduction-to-FluentBit/fluent-bit-logo-input-filter-plugins.jpg)
</Frame>

## What You Will Learn

By the end of this article, you will have a comprehensive understanding of how Logstash and Fluent Bit work within logging architectures. You will also learn how to leverage these tools to set up robust log processing pipelines that meet your specific needs.

Let's get started on enhancing your logging infrastructure with Fluent Bit.

<Frame>
  ![The image features the Fluent Bit logo alongside two check-marked items: "Knowledge of the Tools" and "How to leverage?"](https://kodekloud.com/kk-media/image/upload/v1752874215/notes-assets/images/EFK-Stack-Enterprise-Grade-Logging-and-Monitoring-Introduction-to-FluentBit/fluent-bit-logo-knowledge-checks.jpg)
</Frame>

Thank you for reading!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/efk-stack-enterprise-grade-logging-and-monitoring/module/fde8c25d-412a-4b83-95dd-b2a21ea186f3/lesson/0931b32a-c877-4543-925b-a8c214a8a953" />
</CardGroup>
