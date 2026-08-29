# Distributed Tracing with Jaeger

Source: https://notes.kodekloud.com/docs/Istio-Service-Mesh/Observability/Distributed-Tracing-with-Jaeger/page

This article discusses using Jaeger for distributed tracing in Istio-managed environments to monitor service behavior and identify latency issues.

Distributed tracing is a critical component for monitoring individual requests as they travel through a service mesh. By tracking how requests propagate across various services, developers can gain valuable insights into service behavior, detect interdependencies, and quickly identify latency issues.

![The image is a blue background slide with the text "Distributed Tracing with Jaeger" in the center. There is also a downward arrow icon below the text.](https://kodekloud.com/kk-media/image/upload/v1752879368/notes-assets/images/Istio-Service-Mesh-Distributed-Tracing-with-Jaeger/distributed-tracing-jaeger-slide.jpg)

Istio leverages Envoy proxies to integrate distributed tracing seamlessly within a service mesh. It supports a variety of tracing systems—such as Zipkin, Jaeger, Lightstep, and Datadog—to fit different monitoring needs. In this lesson, we focus on how to use Jaeger for tracing in an Istio-managed environment.

> **lightbulb** Distributed tracing with Jaeger not only helps in identifying performance bottlenecks but also enhances the observability of complex microservice architectures.

![The image shows logos of four software tools: Zipkin, Lightstep, Jaeger, and Datadog. Each logo is distinct, featuring unique designs and colors.](https://kodekloud.com/kk-media/image/upload/v1752879369/notes-assets/images/Istio-Service-Mesh-Distributed-Tracing-with-Jaeger/zipkin-lightstep-jaeger-datadog-logos.jpg)

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-service-mesh/module/7696566a-6631-4367-9fbc-ce86b23cd608/lesson/7777f526-3275-413f-82d0-f1367d700824)
