# SLOSLASLI

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Associate-KCNA/Cloud-Native-Observability/SLOSLASLI/page

This article explains Service Level Objectives, Indicators, and Agreements, focusing on their roles in measuring and ensuring service reliability and performance.

When designing a robust system or application, it is essential for teams to define clear, measurable targets and goals. These targets allow organizations to strike a balance between product development and operational work while giving customers a concrete expectation of service reliability. For instance, an application might be required to deliver a minimum of 97% uptime over a rolling 30-day period.

A Service Level Indicator (SLI) is a quantitative metric that evaluates a specific aspect of service performance. In simpler terms, an SLI measures how well a service operates based on key performance indicators.

<Frame>
  ![The image discusses setting measurable targets for system reliability, emphasizing a 97% uptime goal over a 30-day period.](https://kodekloud.com/kk-media/image/upload/v1752880558/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-SLOSLASLI/frame_30.jpg)
</Frame>

Common SLIs include:

* Request latency
* Error rates
* Saturation or throughput
* Availability (e.g., ensuring 99% uptime)

<Frame>
  ![The image explains Service Level Indicators (SLIs) as quantitative measures of service levels, listing common SLIs: request latency, error rate, saturation, throughput, and availability.](https://kodekloud.com/kk-media/image/upload/v1752880559/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-SLOSLASLI/frame_60.jpg)
</Frame>

It is important to understand that not every metric qualifies as an SLI. The most effective SLIs closely mirror the user’s experience with the service. For example, high CPU usage or memory consumption may be a concern from a technical perspective but do not necessarily translate into a degraded user experience. Instead, metrics such as response time and error rates serve as more accurate indicators of service quality from the customer's viewpoint.

<Frame>
  ![The image explains that not all metrics are suitable for Service Level Indicators (SLIs), emphasizing user experience over technical metrics like high CPU usage.](https://kodekloud.com/kk-media/image/upload/v1752880560/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-SLOSLASLI/frame_100.jpg)
</Frame>

A Service Level Objective (SLO) represents the target value or acceptable range for an SLI. For example, if an SLI reads latency, an SLO might be set to keep latency below 100 milliseconds. Similarly, an availability SLO could state that the service must achieve 99.9% uptime. Essentially, an SLO provides a clear, measurable goal aligned with the customer experience.

<Frame>
  ![The image explains Service Level Objectives (SLOs) as target values for Service Level Indicators (SLIs), focusing on latency and availability to enhance customer experience.](https://kodekloud.com/kk-media/image/upload/v1752880561/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-SLOSLASLI/frame_150.jpg)
</Frame>

<Callout icon="lightbulb">
  While it might be tempting to push for extremely high targets such as 100% uptime or 99.999% uptime, this approach often leads to unnecessary costs without delivering significant benefits to customers.
</Callout>

A Service Level Agreement (SLA) is a formal contract between a vendor and a user that commits to meeting a specific SLO. SLAs are typically legally binding, and failure to meet the agreed-upon targets may result in financial penalties or other corrective measures.

<Frame>
  ![The image explains a Service Level Agreement (SLA) as a contract ensuring a Service Level Objective (SLO) between a vendor and user, with potential financial or other consequences for non-compliance.](https://kodekloud.com/kk-media/image/upload/v1752880562/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-SLOSLASLI/frame_200.jpg)
</Frame>

In summary, SLIs are used to measure the quality of a service, SLOs set the target performance levels for these indicators, and SLAs formalize these targets in a binding agreement. Together, they play a critical role in ensuring that customers receive a consistent and high-quality service.

For further reading on service reliability management, explore our [Kubernetes Documentation](https://kubernetes.io/docs/) and [Docker Hub](https://hub.docker.com/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-associate-kcna/module/70e17eea-7e9b-4f65-87a4-1cdb5631e0dc/lesson/d3739406-fce9-4bb1-be46-8f771528532c" />
</CardGroup>
