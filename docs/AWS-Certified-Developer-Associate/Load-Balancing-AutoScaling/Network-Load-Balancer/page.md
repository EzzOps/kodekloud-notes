# Network Load Balancer

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/Load-Balancing-AutoScaling/Network-Load-Balancer/page

This article explores the Network Load Balancer, its features, advantages, and capabilities in routing traffic for performance-critical applications.

In this lesson, we will explore the Network Load Balancer and its key features. The Network Load Balancer (NLB) is designed to operate at Layer 4 of the OSI model, making it an ideal solution for routing traffic based on TCP, UDP, or TLS protocols.

<Callout icon="lightbulb">
  One distinct advantage of the NLB is that it assigns a fixed IP address (static or Elastic IP), which is critical for both exam requirements and real-world configurations.
</Callout>

## Advantages of the Network Load Balancer

The NLB offers several notable benefits:

* **Retains the Client's Source IP Address:**\
  Unlike the Application Load Balancer (ALB) that substitutes the client's IP with a specific header, the NLB preserves the original IP address. This is particularly useful for applications that require accurate source IP visibility.

* **High Performance and Low Latency:**\
  Designed for high throughput, the NLB minimizes latency making it suitable for performance-critical applications.

* **Robust Target Support:**\
  The NLB can forward incoming traffic to various backend targets, including:

  | Target Type               | Example                                                                                        |
  | ------------------------- | ---------------------------------------------------------------------------------------------- |
  | EC2 Instances             | [EC2 Instances](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2)     |
  | ECS Tasks                 | [ECS Tasks](https://learn.kodekloud.com/user/courses/amazon-elastic-container-service-aws-ecs) |
  | Lambda Functions          | [Lambda Functions](https://learn.kodekloud.com/user/courses/aws-lambda)                        |
  | Application Load Balancer | ALB for additional routing capabilities                                                        |

The diagram below illustrates a typical NLB setup:

<Frame>
  ![The image illustrates a network load balancer setup, showing a user connecting via TCP/UDP/TLS to a load balancer, which then routes traffic to various targets like EC2 instances, ECS tasks, Lambda functions, and ALB.](https://kodekloud.com/kk-media/image/upload/v1752859089/notes-assets/images/AWS-Certified-Developer-Associate-Network-Load-Balancer/network-load-balancer-setup-diagram.jpg)
</Frame>

## Routing Traffic to an Application Load Balancer

One of the unique capabilities of the NLB is its ability to forward traffic to an Application Load Balancer. This feature is not available with ALBs, as they cannot route traffic to other load balancers.

The workflow for routing traffic is as follows:

1. Traffic is sent to the Network Load Balancer.
2. The NLB's static (or fixed) IP can be integrated into DNS settings or firewall configurations.
3. The NLB forwards the incoming traffic to an Application Load Balancer.
4. The ALB then routes the traffic to its designated backend targets.

The following diagram further clarifies this process:

<Frame>
  ![The image is a diagram showing a network load balancer (NLB) and an application load balancer (ALB) within a VPC, directing traffic to HTTP(S) targets.](https://kodekloud.com/kk-media/image/upload/v1752859090/notes-assets/images/AWS-Certified-Developer-Associate-Network-Load-Balancer/network-load-balancer-diagram.jpg)
</Frame>

## Summary

The Network Load Balancer:

* Operates at Layer 4 of the OSI model using TCP/UDP protocols.
* Retains the client's original source IP address.
* Provides high performance with low latency.
* Offers a static IP address essential for secure DNS and firewall configurations.
* Supports routing to various backend targets, including the capability to integrate with Application Load Balancers.

This makes the Network Load Balancer an excellent choice for applications that require non-HTTP/HTTPS protocol support, enhanced performance, and reliable IP stability.

<Callout icon="lightbulb">
  For more insights on load balancing strategies in cloud environments, explore [AWS Load Balancers](https://aws.amazon.com/elasticloadbalancing/) and other cloud networking resources.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/c5fbed4d-288a-4e90-9f57-04fbe853f8a5/lesson/f9cea5ed-d219-4acf-8182-b9add0010df2" />
</CardGroup>
