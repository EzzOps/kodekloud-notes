# Demo Steady State Pod Delete on EKS

Source: https://notes.kodekloud.com/docs/Chaos-Engineering/Chaos-Engineering-on-Kubernetes-EKS/Demo-Steady-State-Pod-Delete-on-EKS/page

This article explains how to establish a steady state for an application on Amazon EKS before conducting a pod deletion experiment.

In this walkthrough, we collect baseline metrics to define the application’s steady state. This is essential before running an AWS Fault Injection Simulator (FIS) experiment to delete an EKS pod.

## 1. Observe Container Insights Performance

Begin by reviewing your Amazon EKS service metrics with CloudWatch Container Insights. Track these core indicators:

| Metric                 | Description                         |
| ---------------------- | ----------------------------------- |
| Running pod count      | Number of pods currently in service |
| Pod CPU utilization    | CPU usage per pod                   |
| Pod memory utilization | Memory usage per pod                |

<Frame>
  ![The image shows an AWS CloudWatch dashboard for Container Insights, displaying performance metrics for a service named "PetSite," including running pods, CPU utilization, and memory utilization.](https://kodekloud.com/kk-media/image/upload/v1752871893/notes-assets/images/Chaos-Engineering-Demo-Steady-State-Pod-Delete-on-EKS/aws-cloudwatch-containers-petsite-dashboard.jpg)
</Frame>

<Callout icon="lightbulb">
  These charts represent the steady state of the `PetSite` service under normal conditions.
</Callout>

## 2. Verify End-User Experience with CloudWatch RUM

Next, validate real user metrics using CloudWatch RUM. This helps you understand page load performance and client-side errors:

<Frame>
  ![The image shows an AWS CloudWatch dashboard displaying performance metrics for a web application, including page loads, load time, and errors. It features various tabs and filters for monitoring application performance.](https://kodekloud.com/kk-media/image/upload/v1752871893/notes-assets/images/Chaos-Engineering-Demo-Steady-State-Pod-Delete-on-EKS/aws-cloudwatch-dashboard-performance-metrics.jpg)
</Frame>

Then, examine key web vitals like Largest Contentful Paint (LCP) and First Input Delay (FID):

<Frame>
  ![The image shows an AWS CloudWatch dashboard displaying web vitals, including metrics for "Largest Contentful Paint" and "First Input Delay," with graphs indicating performance levels categorized as positive, tolerable, and frustrating.](https://kodekloud.com/kk-media/image/upload/v1752871895/notes-assets/images/Chaos-Engineering-Demo-Steady-State-Pod-Delete-on-EKS/aws-cloudwatch-dashboard-web-vitals.jpg)
</Frame>

## 3. Simulate Load with k6

Generate realistic user traffic using k6 to ensure the baseline reflects production behavior. For example:

```bash theme={null}
k6 run script.js --vus 4 --duration 1h
```

During the test, you might see output like:

```bash theme={null}
running (@48m32.0s), 1/4 VUs, 1783 complete and 3 interrupted iterations
browser  X [ 69% ] 4 VUs @48m05.4s/1h4m59s
```

<Callout icon="lightbulb">
  Approximately 1% of virtual users experienced frustration, while the rest saw positive load times.
</Callout>

## 4. Inspect Distributed Tracing with CloudWatch Trace Map

Capture end-to-end request performance for the `petlistadoptions` endpoint on EKS Fargate:

<Frame>
  ![The image shows an AWS CloudWatch Trace Map interface displaying metrics for a service called "petlistadoptions" on EKS Fargate, including latency, requests, and fault rates.](https://kodekloud.com/kk-media/image/upload/v1752871896/notes-assets/images/Chaos-Engineering-Demo-Steady-State-Pod-Delete-on-EKS/aws-cloudwatch-trace-map-petlistadoptions.jpg)
</Frame>

Analyze latency, throughput, and error rates to solidify your steady state baseline.

***

## References

* [AWS Fault Injection Simulator (FIS)](https://aws.amazon.com/fis/)
* [Amazon EKS Documentation](https://docs.aws.amazon.com/eks/)
* [CloudWatch Container Insights Overview](https://docs.aws.amazon.[SECRET_REDACTED].html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/chaos-engineering/module/67947884-154a-43e4-a0cf-1137e1264eee/lesson/35627c0c-58bb-488a-8142-0c188eacb783" />
</CardGroup>
