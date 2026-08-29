# TYPE promhttp_metric_handler_requests_in_flight gauge
promhttp_metric_handler_requests_in_flight 1
# HELP promhttp_metric_handler_requests_total Total number of scrapes by HTTP status code.
# TYPE promhttp_metric_handler_requests_total counter
promhttp_metric_handler_requests_total{code="200"} 0
promhttp_metric_handler_requests_total{code="500"} 0
promhttp_metric_handler_requests_total{code="503"} 0
```

Alternatively, open your web browser and navigate to:\
[http://localhost:9100/metrics](http://localhost:9100/metrics)

## Example with a Different Version

The process remains the same if you are using a different version, such as `node_exporter-1.4.0.linux-amd64`. Your working directory may resemble:

```bash theme={null}
user2 in ~
> ls
Desktop    Downloads    node_exporter-1.4.0.linux-amd64    Pictures    pushgateway-1.4.3.linux-amd64    snap    Videos    Documents    Music    Public    pushgateway-1.4.3.linux-amd64.tar.gz    Templates
```

Change into the specific directory:

```bash theme={null}
cd node_exporter-1.4.0.linux-amd64
```

Verify the contents:

```bash theme={null}
ls -la
```

Sample output:

```bash theme={null}
total 19208
drwxr-xr-x 2 user2 user2     4096 Sep 26 08:39 .
drwxr-xr-x 17 user2 user2     4096 Nov 12 23:43 ..
-rw-r--r-- 1 user2 user2    11357 Sep 26 20:39 LICENSE
-rwxr-xr-x 1 user2 19640886 Sep 26 08:33 node_exporter
-rw-r--r-- 1 user2 user2      463 Sep 26 08:39 NOTICE
```

Run the exporter:

```bash theme={null}
./node_exporter
```

Verify the metrics with:

```bash theme={null}
curl localhost:9100/metrics
```

A sample output provides various system metrics, including CPU, memory, and network statistics:

```plaintext theme={null}
# TYPE node_timex_tick_seconds gauge
node_timex_tick_seconds 0.01
# HELP node_udp_queues Number of allocated memory in the kernel for UDP datagrams in bytes.
# TYPE node_udp_queues gauge
node_udp_queues{ip="v4",queue="rx"} 0
node_udp_queues{ip="v4",queue="tx"} 0
node_udp_queues{ip="v6",queue="rx"} 0
node_udp_queues{ip="v6",queue="tx"} 0
# HELP node_uname_info Labeled system information as provided by the uname system call.
node_uname_info{domainname="(none)",machine="x86_64",nodename="user2",release="5.15.0-52-generic",sysname="Linux",version="#58-Ubuntu SMP Thu Oct 13 08:03:55 UTC 2022"} 1
...
```

## Conclusion

With these steps, the Prometheus Node Exporter is now set up to collect host metrics, allowing Prometheus to scrape them from the /metrics endpoint. This installation is a key component for monitoring system performance and reliability.

> **lightbulb** For further customization and enhancements, explore additional Prometheus exporters and check out the [Prometheus Documentation](https://prometheus.io/docs/).

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-associate-kcna/module/70e17eea-7e9b-4f65-87a4-1cdb5631e0dc/lesson/9d9bdd41-a5a2-4531-88a6-9bed011d6e32)


# Prometheus Use Case

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Associate-KCNA/Cloud-Native-Observability/Prometheus-Use-Case/page

This article explores Prometheus use cases, showcasing its applications in infrastructure monitoring, including metrics aggregation, proactive alerting, and performance analysis.

In this lesson, we explore several Prometheus use cases, demonstrating both its origins and its practical applications in modern infrastructure monitoring.

## Unified Metrics Aggregation

Organizations with multiple data centers and cloud services, such as AWS, face challenges in monitoring distributed environments. Imagine an enterprise with data centers spread across the West, Central, and East regions, alongside cloud-based services. The objective is to aggregate metrics from these diverse sources and present them in a single, easy-to-read dashboard.

Prometheus is designed to scrape metrics from various locations, whether on-premises or cloud-based, and provides built-in dashboarding utilities to display the data in a consolidated view.

![The image illustrates a network diagram with data centers (West, Central, East) and AWS, connected to a central dashboard displaying analytics.](https://kodekloud.com/kk-media/image/upload/v1752880555/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-Prometheus-Use-Case/frame_40.jpg)

## Proactive Alerting for Server Health

A common scenario for Prometheus involves monitoring server resources. Consider a MySQL database server that experiences high memory usage, potentially leading to outages. Operations teams need to be alerted when memory consumption reaches a critical level (for example, 80% usage) so they can intervene before users experience disruptions.

Prometheus offers built-in alerting mechanisms. When a metric exceeds a predefined threshold, it can trigger notifications through various channels such as email, Slack, or SMS.

![The image describes a use case where the operations team wants email notifications when a MySQL server's memory reaches 80% capacity to prevent outages.](https://kodekloud.com/kk-media/image/upload/v1752880556/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-Prometheus-Use-Case/frame_80.jpg)

> **lightbulb** To configure alerting:

  * Define metric queries in Prometheus.
  * Set threshold rules.
  * Integrate with your preferred notification systems.

## Performance Analysis for New Features

When introducing new functionalities, such as a video upload feature on a website, performance monitoring becomes crucial. For instance, if large file uploads lead to increased latency, it is important to determine the file size at which performance degrades significantly.

By collecting metrics on both average file size and request latency, Prometheus enables teams to correlate these values and pinpoint the threshold at which performance issues occur. Its visualization tools graphically represent this analysis, supporting further performance optimization.

![The image describes a use case for analyzing video upload impact on application performance, focusing on average file size and latency to identify degradation points.](https://kodekloud.com/kk-media/image/upload/v1752880557/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-Prometheus-Use-Case/frame_130.jpg)

## Summary of Prometheus Capabilities

Prometheus is a versatile tool that provides critical monitoring solutions, including:

* **Aggregated Metrics Display:** Collect metrics from distributed data centers and cloud services into a unified dashboard.
* **Proactive Alerting:** Monitor key performance indicators and trigger alerts to prevent potential outages.
* **Feature Performance Analysis:** Analyze the impact of new application features to maintain optimal performance.

> **lightbulb** Leveraging Prometheus allows teams to maintain reliable, high-performing infrastructure by proactively identifying and addressing potential issues.

These use cases highlight how Prometheus can help organizations continuously monitor and improve their infrastructure and application performance, ensuring a robust and responsive digital environment.

## Learn More

For further details on Prometheus and advanced monitoring techniques, explore these additional resources:

* [Prometheus Documentation](https://prometheus.io/docs/)
* [Monitoring Best Practices](https://www.datadoghq.com/)

By following this guide, you can effectively utilize Prometheus to enhance your system monitoring strategy and improve overall performance management.

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-associate-kcna/module/70e17eea-7e9b-4f65-87a4-1cdb5631e0dc/lesson/759f4d77-053a-4e2f-aec5-554c9fdbe6bb)
