# Route 53 Routing Policies

Source: https://notes.kodekloud.com/docs/AWS-Certified-CloudOps-Engineer-Associate/Domain-5-Networking-and-Content-Delivery/Route-53-Routing-Policies/page

This article explores the eight routing policies of Amazon Route 53, detailing their implementation and use cases for efficient traffic management.

Welcome to this comprehensive guide on Route 53 routing policies. In this article, we explore the eight routing policies offered by Amazon Route 53—Amazon's robust DNS service—and demonstrate their implementation and use cases. Mastering these policies is essential not only for the AWS SysOps exam but also for designing efficient, resilient production environments.

Route 53 supports eight distinct routing policies:

* Simple Routing Policy
* Failover Routing Policy
* Geolocation Routing Policy
* Geoproximity Routing Policy
* Latency Routing Policy
* IP-Based Routing Policy
* Multivalue Answer Routing Policy
* Weighted Routing Policy

<Frame>
  ![The image lists different types of routing policies, including Simple, Failover, Geolocation, Geoproximity, Latency, IP-Based, Multivalue Answer, and Weighted Routing Policies. Each policy is represented with an icon and a label.](https://kodekloud.com/kk-media/image/upload/v1752860896/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Route-53-Routing-Policies/routing-policies-icons-list.jpg)
</Frame>

Understanding the functionalities and nuances of these policies will help you answer exam questions confidently and build robust architectures for dynamic traffic management. Let’s delve into each policy with detailed explanations and implementation steps.

***

## 1. Simple Routing Policy

The Simple Routing Policy creates a direct one-to-one mapping between DNS queries and a single resource, such as an IP address or server. It excludes advanced configurations like traffic distribution, redundancy, or geo-based routing.

<Frame>
  ![The image illustrates a simple routing policy, showing a flow from a user to a Route 53 icon, then to a computing icon, and finally to a web page icon.](https://kodekloud.com/kk-media/image/upload/v1752860898/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Route-53-Routing-Policies/routing-policy-user-to-webpage.jpg)
</Frame>

To implement this policy, select a public or private hosted zone, create the necessary record (A, AAAA, CNAME, etc.), and configure the details. Note that DNS health checks are not part of this simple configuration.

<Callout icon="lightbulb">
  Route 53 is reputed for its 100% SLA, ensuring high availability even when using simple routing.
</Callout>

***

## 2. Failover Routing Policy

The Failover Routing Policy enhances disaster recovery and high availability. It works by designating primary and secondary resources, automatically redirecting traffic to the standby resource if the primary one fails a health check. Only one resource remains active at any moment.

<Frame>
  ![The image illustrates a failover routing policy, showing a user connecting to a Route 53 service, which directs traffic to a primary active resource and a secondary passive resource.](https://kodekloud.com/kk-media/image/upload/v1752860899/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Route-53-Routing-Policies/failover-routing-policy-route53-traffic.jpg)
</Frame>

While you can use reverse policies, a weighted routing policy might be preferable for active-active configurations. The setup process involves:

1. Creating a hosted zone.
2. Setting primary and secondary records.
3. Configuring DNS or load balancer health checks.

<Frame>
  ![The image outlines the steps for implementing a failover routing policy, including choosing hosted zones, creating a primary record, configuring primary and secondary resources, and setting up health checks.](https://kodekloud.com/kk-media/image/upload/v1752860900/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Route-53-Routing-Policies/failover-routing-policy-implementation.jpg)
</Frame>

***

## 3. Geolocation Routing Policy

Geolocation routing directs traffic based on the geographical location of users at the continent or country level. This policy is useful for tailoring content or services to specific regions. For more granular needs (e.g., state or county level), consider third-party solutions.

For example, you can configure Route 53 to route users located in France, Spain, or Ireland to designated endpoints. The configuration process mirrors other routing policies: select the hosted zone, create a DNS record, and configure geolocation settings with the appropriate resource details.

<Frame>
  ![The image illustrates a geolocation routing policy, showing a user near Region B being directed through a Route 53 service to the appropriate server in Region B.](https://kodekloud.com/kk-media/image/upload/v1752860902/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Route-53-Routing-Policies/geolocation-routing-policy-route53.jpg)
</Frame>

***

## 4. Geoproximity Routing Policy

Unlike geolocation, Geoproximity Routing takes actual physical proximity into account. It routes users by determining the closest resource based on the distance between the user and your data centers. Additionally, you can apply a bias to favor a particular location.

For instance, users in northern Great Britain might be routed to an Ireland data center if it is closer than a data center in London. The implementation steps are similar:

1. Choose your hosted zone.
2. Create the required record.
3. Configure the geoproximity settings.
4. Provide resource details.

<Frame>
  ![The image shows a geoproxity map divided into five colored regions, each marked with a number, illustrating a routing policy.](https://kodekloud.com/kk-media/image/upload/v1752860903/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Route-53-Routing-Policies/geoproxity-map-routing-policy-regions.jpg)
</Frame>

***

## 5. Latency Routing Policy

Latency Routing Policy improves user experience by directing traffic to the region that offers the lowest network latency. It bases decisions on performance testing rather than strict geography, meaning that the fastest responding region may not always be the nearest geographically.

The setup mirrors that of other policies: create a hosted zone, establish the record, and configure latency settings for each targeted region.

<Frame>
  ![The image illustrates a latency routing policy, showing how a user is directed to the lowest latency region between two options, Region A and Region B, using a Route 53 service.](https://kodekloud.com/kk-media/image/upload/v1752860904/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Route-53-Routing-Policies/latency-routing-policy-route53.jpg)
</Frame>

***

## 6. IP-Based Routing Policy

IP-Based Routing directs traffic according to the IP address of the requester. This policy is especially useful for filtering out malicious traffic or routing internal corporate traffic to dedicated resources. You can also set a catch-all rule for traffic not matching specified IP ranges.

To implement this policy, follow these steps:

1. Choose your hosted zone.
2. Create the required DNS record.
3. Configure the IP-based settings.
4. Provide the necessary resource details.

<Frame>
  ![The image outlines the steps for implementing an IP-based routing policy, including choosing hosted zones, creating a record, configuring IP-based settings, and entering resource details.](https://kodekloud.com/kk-media/image/upload/v1752860905/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Route-53-Routing-Policies/ip-based-routing-policy-implementation.jpg)
</Frame>

***

## 7. Multivalue Answer Routing Policy

The Multivalue Answer Routing Policy enables Route 53 to return up to eight healthy records in response to a single DNS query. This policy supports health checks and offers built-in load balancing by randomly selecting one healthy record among many.

It is an excellent option when you need to distribute traffic across multiple endpoints without the complexity of advanced configurations.

<Frame>
  ![The image illustrates a multivalue answer routing policy, showing how Route 53 randomly selects from healthy records to balance traffic across multiple resources.](https://kodekloud.com/kk-media/image/upload/v1752860907/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Route-53-Routing-Policies/route-53-multivalue-routing-policy.jpg)
</Frame>

Setup involves creating a hosted zone, adding multiple records with their respective health checks, and specifying the resource details.

***

## 8. Weighted Routing Policy

The Weighted Routing Policy allows you to distribute traffic based on assigned weight values, making it ideal for A/B testing or gradually shifting traffic between environments—such as production versus staging. For example, you may assign 80% of traffic to the production endpoint and 20% to staging, or any other desired distribution.

A weight set to zero effectively removes a resource from serving traffic. Implementation details include:

1. Creating your hosted zone.
2. Adding the DNS record.
3. Specifying the weights and resource details.

<Frame>
  ![The image illustrates a weighted routing policy, showing a user's IP address being directed to production and staging environments with weights of 80% and 20%, respectively.](https://kodekloud.com/kk-media/image/upload/v1752860908/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Route-53-Routing-Policies/weighted-routing-policy-ip-address.jpg)
</Frame>

<Frame>
  ![The image outlines the implementation steps for a weighted routing policy, including choosing hosted zones, creating records, specifying weights, and entering resource details.](https://kodekloud.com/kk-media/image/upload/v1752860909/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Route-53-Routing-Policies/weighted-routing-policy-implementation-steps.jpg)
</Frame>

***

## Conclusion

In summary, Amazon Route 53 provides a versatile set of eight routing policies designed to manage various traffic scenarios—from basic one-to-one routing to complex configurations involving failover, geolocation, geoproximity, latency, IP-based filtering, multivalue responses, and weighted distribution.

A thorough understanding of these policies is key for both the AWS SysOps exam and the creation of robust, high-performance architectures. Make sure to explore each policy in depth to determine the best approach for your specific requirements.

Happy routing, and stay tuned for more insights into AWS and traffic management best practices!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-certified-sysops-administrator-associate/module/fd99c412-5efc-46e2-99ce-bb9c581fec27/lesson/5f51ed8b-1365-49db-8257-39381301b758" />
</CardGroup>
