# Security Architecture Concerns and Thoughts

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Migration-Structuring-your-Platform/Security-Architecture-Concerns-and-Thoughts/page

Checklist summarizing security and reliability concerns for enterprise architecture reviews, guiding design decisions on data residency, access control, availability, networking, retention, and encryption

This lesson summarizes common security and reliability concerns to surface early in an enterprise architecture design review. Some issues are resolved at the design stage; others become implementation blockers if ignored. Use this as a checklist to identify potential showstoppers and to align engineering, legal, and compliance stakeholders before committing to a design.

## At-a-glance checklist

| Topic                      | Primary question to answer                              | Typical mitigations                                                                                 |
| -------------------------- | ------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Data sovereignty           | Where must customer data physically and legally reside? | Choose provider regions with residency guarantees; contractual controls; data localization features |
| Access (IAM)               | Who needs access and with what privileges?              | RBAC/ABAC, least privilege, MFA, short-lived creds, centralized auditing                            |
| Availability & reliability | What uptime, latency, and fault tolerance are required? | Multi-AZ/region redundancy, SLOs/SLAs, autoscaling, chaos testing                                   |
| Networking                 | How will traffic flow and be protected?                 | VPC segmentation, private subnets, encryption in transit, NGFWs                                     |
| Retention                  | How long must logs, traces, and artifacts be kept?      | Tiered storage, lifecycle rules, legal hold capabilities                                            |
| Encryption                 | How will data and keys be protected?                    | TLS, at-rest encryption, KMS/HSM, key rotation and access controls                                  |

## Data sovereignty

The physical and legal location of stored data matters for compliance, contracts, and customer expectations. When evaluating cloud or SaaS vendors, verify:

* Which geographic regions and availability zones the provider operates in, and whether they guarantee data residency.
* Contractual and technical controls that prevent data from leaving specified jurisdictions.
* Available cross-border transfer mechanisms (e.g., Standard Contractual Clauses, adequacy decisions) and whether those satisfy your legal team.

<Callout icon="lightbulb">
  Engage legal and compliance teams early to confirm residency requirements and acceptable technical/contractual controls—this reduces rework and procurement delays.
</Callout>

## Access (Identity and Access Management)

Identity and access control are foundational for security and operational hygiene. Best practices include:

* Implement least-privilege access: define narrowly scoped roles and group-level permissions.
* Choose an access model that fits your environment: RBAC for role-centric control, ABAC when attribute-based decisions are required.
* Prefer short-lived credentials and enforce Multi-Factor Authentication (MFA) for sensitive roles.
* Centralize identity providers and audit logging in a tamper-evident system.
* Separate duties for critical operations (e.g., production deploys, key management, security config changes).

Consider integrating identity into CI/CD pipelines and emergency (break-glass) procedures with logging and post-incident reviews.

## Availability and reliability

Availability and reliability are SRE concerns that also affect security (e.g., access to logs during incidents). Design systems to meet defined SLOs and SLAs:

* Architect for redundancy: multi-AZ, and where needed, multi-region failover.
* Define SLOs, SLAs, and error budgets aligned with business priorities.
* Use health checks, circuit breakers, retries with backoff, and graceful degradation to avoid cascading failures.
* Plan capacity and autoscaling with limits to prevent resource exhaustion.
* Regularly test backups, DR procedures, and failover runbooks.

## Networking

Network architecture influences performance, cost, observability, and security posture. Key considerations:

* Estimate egress and internal data volumes to avoid bandwidth saturation and unexpected costs.
* Segment networks: VPCs, private subnets, microsegmentation, and service mesh where appropriate to limit blast radius.
* Enforce secure ingress/egress controls: firewalls, NACLs, NGFWs, and API gateways.
* Encrypt traffic in transit (TLS), and standardize mutual TLS or service mesh mTLS for internal services.
* Account for on-prem constraints: limited bandwidth, latency to cloud endpoints, and integration complexity.

## Retention (logs and artifacts)

Retention policies should meet business, regulatory, and legal requirements while balancing cost and query performance:

* Define retention durations per data type (logs, metrics, traces, artifacts) and business/legal drivers.
* Implement tiered storage and lifecycle policies for cold vs hot data.
* Ensure support for legal holds and forensic queries with proper access controls and auditing.
* Use WORM or append-only storage when immutable audit trails are required.
* Validate retention and purge processes regularly and document retention-related SLAs.

<Callout icon="lightbulb">
  Align retention policy decisions with legal, compliance, and security teams before selecting storage platforms to avoid costly migrations or compliance gaps.
</Callout>

## Encryption

Encryption is mandatory for protecting sensitive data and meeting compliance needs:

* Encrypt data in transit using TLS and enforce strong cipher suites.
* Encrypt data at rest: disk/block, databases, and object storage.
* Use managed Key Management Services (KMS), customer-managed keys (BYOK), or hardware-backed HSMs for key protection.
* Implement key lifecycle management: rotation, backup/escrow, revocation, and least-privilege access to key material.
* Audit key usage and monitor for anomalous access patterns.
* Avoid implementing custom cryptography; rely on vetted libraries and provider-managed services.

<Callout icon="warning">
  Do not transmit or store sensitive data unencrypted. Validate encryption end-to-end during design and deployment and include encryption checks in automated audits.
</Callout>

## Tying security and reliability together

Security and reliability are complementary objectives—both must be considered in design and operations:

* Protect backups and retention stores with the same controls as production data and test recoverability frequently.
* Apply least privilege to observability and diagnostic data to ensure incident responders have access while limiting abuse.
* Prepare recovery playbooks for security incidents that can affect availability (compromised keys, revoked certificates, compromised identities).
* Ensure audit logs and forensic data remain available under attack or during outages to support incident response.

***

That concludes this lesson. Use the checklist above during architecture reviews to surface security- and reliability-related risks early, align stakeholders, and avoid late-stage implementation blockers.

## Links and references

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Identity and Access Management (IAM) overview](https://learn.kodekloud.com/user/courses/aws-iam)
* [SRE / DevOps fundamentals](https://learn.kodekloud.com/user/courses/devops-basics)
* [VPC and cloud networking concepts](https://learn.kodekloud.com/user/courses/aws-networking-fundamentals)
* [Service mesh (Istio) primer](https://learn.kodekloud.com/user/courses/istio-service-mesh)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/fd555480-82df-40f4-b8ad-2ea920d51077/lesson/86191132-d6e4-406f-b7d0-37d6bf0e3d58" />
</CardGroup>
