# Start a CloudWatch Logs Insights query
aws logs start-query \
  --log-group-names "/aws/lambda/my-function" \
  --start-time $(date -v-1H +%s) \
  --end-time $(date +%s) \
  --query-string "fields @timestamp, @message | sort @timestamp desc | limit 20"

# Retrieve recent X-Ray traces
aws xray get-trace-summaries \
  --start-time $(date -v-1H +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date +%Y-%m-%dT%H:%M:%SZ)
```

***

## Further Reading

* [Amazon CloudWatch Documentation](https://docs.aws.amazon.com/cloudwatch/index.html)
* [AWS X-Ray Developer Guide](https://docs.aws.amazon.com/xray/latest/devguide/)
* [Monitoring Best Practices](https://aws.amazon.com/architecture/well-architected/monitor/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloudwatch/module/d95c04dd-f122-4f6b-93dc-d0b2fe015b29/lesson/0632ec18-1125-4033-83c2-ccfa37ded075" />
</CardGroup>


# Container InsightsLambda InsightsContributor InsightsApplication Insights

Source: https://notes.kodekloud.com/docs/AWS-CloudWatch/Cloudwatch-Insights-X-Ray-and-Service-Map/Container-InsightsLambda-InsightsContributor-InsightsApplication-Insights/page

This guide explores four AWS CloudWatch Insights tools to monitor, troubleshoot, and optimize applications under various workloads.

Welcome back! In this guide, we’ll explore four AWS CloudWatch Insights tools—Container Insights, Lambda Insights, Contributor Insights, and Application Insights—and show how they help you monitor, troubleshoot, and optimize your applications under any workload.

Use case scenario: Imagine preparing an e-commerce platform for Black Friday traffic. You need real-time visibility across containers, serverless functions, and microservices to ensure uptime and performance. Let’s dive in.

| Insight Type         | Primary Use Case                                             | Key Benefit                               |
| -------------------- | ------------------------------------------------------------ | ----------------------------------------- |
| Container Insights   | Monitoring containerized applications (EKS, ECS, Kubernetes) | Unified metrics and logs for clusters     |
| Lambda Insights      | Observability for AWS Lambda functions                       | Spot function outliers and memory leaks   |
| Contributor Insights | High-cardinality event analytics for microservices           | Pinpoint source of errors and slowdowns   |
| Application Insights | End-to-end web application monitoring                        | Auto-detect errors and performance issues |

***

## Container Insights

When running microservices in containers, you need a holistic view of CPU, memory, network, and logs—all in one dashboard. Container Insights collects, aggregates, and visualizes these metrics so you can take action before small issues become outages.

<Frame>
  ![The image illustrates a concept of "Container Insights" with icons representing containers, gears, and users, leading to a central insight symbol surrounded by settings icons.](https://kodekloud.com/kk-media/image/upload/v1752862498/notes-assets/images/AWS-CloudWatch-Container-InsightsLambda-InsightsContributor-InsightsApplication-Insights/container-insights-icons-gears-users.jpg)
</Frame>

### Key Features

| Feature                         | Description                                                           |
| ------------------------------- | --------------------------------------------------------------------- |
| Performance Monitoring          | Track CPU, memory, disk I/O, and network throughput in real time.     |
| Log Analytics & Troubleshooting | Search, filter, and correlate container logs across clusters.         |
| Auto-Scaling Integration        | Trigger scaling policies based on custom metrics from your workloads. |
| Pay-As-You-Go Pricing           | Only pay for the metrics and logs you collect; no upfront costs.      |

<Callout icon="lightbulb">
  You can enable Container Insights via the AWS Management Console, CLI, or CloudFormation in just a few clicks—no code changes required.
</Callout>

<Frame>
  ![The image is a slide titled "Container Insights" with three sections: Performance Monitoring, Log Analytics and Troubleshooting, and Pricing, each with an icon and number.](https://kodekloud.com/kk-media/image/upload/v1752862499/notes-assets/images/AWS-CloudWatch-Container-InsightsLambda-InsightsContributor-InsightsApplication-Insights/container-insights-performance-log-pricing.jpg)
</Frame>

***

## Lambda Insights

If your architecture relies on AWS Lambda for event-driven workloads (e.g., S3 triggers, EventBridge rules), Lambda Insights centralizes performance metrics and logs so you don’t have to investigate each function separately.

<Frame>
  ![The image illustrates a process flow involving Lambda functions, tools, and users, leading to a central "Lambda Insight" component, surrounded by configuration icons.](https://kodekloud.com/kk-media/image/upload/v1752862500/notes-assets/images/AWS-CloudWatch-Container-InsightsLambda-InsightsContributor-InsightsApplication-Insights/lambda-functions-process-flow-diagram.jpg)
</Frame>

### Key Features

* Easy Setup: Enable instrumentation without modifying your existing code or deployment pipeline.
* Real-Time Metrics: Monitor execution duration, memory usage, cold starts, and concurrency.
* Bottleneck Detection: Quickly identify functions that exceed thresholds or show anomalous behavior.
* Cost Allocation: Break down Lambda charges by function to optimize spend.

<Callout icon="lightbulb">
  Lambda Insights incurs a small additional cost per metric and log, but gives you actionable data to reduce overall Lambda spend.
</Callout>

<Frame>
  ![The image is a slide titled "Lambda Insights" with four sections: Easy Setup, Operational Visibility, Monitoring and Optimization, and Pricing, each represented by an icon and number.](https://kodekloud.com/kk-media/image/upload/v1752862501/notes-assets/images/AWS-CloudWatch-Container-InsightsLambda-InsightsContributor-InsightsApplication-Insights/lambda-insights-setup-visibility-monitoring-pricing.jpg)
</Frame>

***

## Contributor Insights

Contributor Insights provides real-time analytics on high-cardinality data (user IDs, API endpoints, order IDs) so you can pinpoint which component in your transaction pipeline is causing issues.

<Frame>
  ![The image outlines three aspects of "Contributor Insights": High-Cardinality Data Analysis, Performance Impact Identification, and Data Aggregation and Discovery.](https://kodekloud.com/kk-media/image/upload/v1752862502/notes-assets/images/AWS-CloudWatch-Container-InsightsLambda-InsightsContributor-InsightsApplication-Insights/contributor-insights-data-analysis-performance.jpg)
</Frame>

### Key Features

| Feature                           | Benefit                                                              |
| --------------------------------- | -------------------------------------------------------------------- |
| High-Cardinality Analysis         | Drill into unique keys (e.g., user ID, session ID) to spot hotspots. |
| Performance Impact Identification | Correlate slow API calls or retries with downstream resource errors. |
| Trend Aggregation & Alerts        | Aggregate events over time, set thresholds, and receive alerts.      |

<Callout icon="lightbulb">
  Contributor Insights shines as your microservice count grows. Use it proactively in production to detect anomalies early.
</Callout>

***

## Application Insights

For full-stack web applications—like a live video streaming site—Application Insights offers automatic error detection, performance tracing, and dependency mapping to keep end users happy.

<Frame>
  ![The image shows a slide titled "Application Insights" with two sections: "Web Application Monitoring" and "Telemetry Data Utilization," each with an icon and number.](https://kodekloud.com/kk-media/image/upload/v1752862503/notes-assets/images/AWS-CloudWatch-Container-InsightsLambda-InsightsContributor-InsightsApplication-Insights/application-insights-web-monitoring-telemetry.jpg)
</Frame>

### Key Features

* Web Application Monitoring: Auto-discover exceptions, HTTP 5XX errors, and latency spikes.
* Dependency Mapping: Visualize calls to databases, caches, and external APIs.
* Telemetry Dashboard: Combine user, performance, and operational data in one view.

<Callout icon="triangle-alert">
  Application Insights adds overhead—enable it for mission-critical applications where user experience metrics are essential.
</Callout>

***

## Links and References

* AWS CloudWatch Container Insights
* AWS Lambda Insights
* AWS Contributor Insights
* AWS Application Insights
* [AWS CloudWatch Documentation](https://docs.aws.amazon.com/cloudwatch)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloudwatch/module/d95c04dd-f122-4f6b-93dc-d0b2fe015b29/lesson/4fd5cf99-a4b3-4068-8f06-5264c6887e73" />
</CardGroup>
