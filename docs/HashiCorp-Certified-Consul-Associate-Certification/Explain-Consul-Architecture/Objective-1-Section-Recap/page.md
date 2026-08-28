# Objective 1 Section Recap

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Explain-Consul-Architecture/Objective-1-Section-Recap/page

This lesson reviews the foundational elements of Consul’s internal architecture and core design principles.

In this lesson, we’ve reviewed the foundational elements of Consul’s internal architecture and core design principles. Below is a quick summary to reinforce what you’ve learned before moving on to more advanced topics.

<Frame>
  ![The image outlines objectives for explaining Consul architecture, including identifying components, preparing for high availability, understanding core functionality, and differentiating agent roles. It also indicates a difficulty level of 2 out of 5.](https://kodekloud.com/kk-media/image/upload/v1752877849/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Objective-1-Section-Recap/consul-architecture-objectives-components-high-availability.jpg)
</Frame>

## Key Takeaways

| Area                    | Description                                                                                       |
| ----------------------- | ------------------------------------------------------------------------------------------------- |
| Core Functionality      | Service discovery, health checking, the key/value store, and multi-datacenter support.            |
| Consul Components       | Server and client agents (including development mode) and their interactions within a datacenter. |
| Communication Protocols | Gossip for cluster membership and Raft for strong data consistency.                               |
| High Availability       | Clustered server configuration to maintain fault tolerance and automatic failover.                |
| Read Scalability        | Non-voting server agents (read-only replicas) to scale query throughput.                          |

<Callout icon="lightbulb">
  You now have a solid understanding of Consul’s architecture and design. In the upcoming lessons, we’ll explore specific features—starting with service registration and discovery.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/bb95f43b-3acb-4ce2-88ae-0c79beb3e569/lesson/59e90c96-479c-4973-8667-260947639779" />
</CardGroup>
