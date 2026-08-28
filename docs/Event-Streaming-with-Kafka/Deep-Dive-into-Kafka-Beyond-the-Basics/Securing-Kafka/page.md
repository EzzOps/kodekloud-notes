# Securing Kafka

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Deep-Dive-into-Kafka-Beyond-the-Basics/Securing-Kafka/page

Guide to securing Kafka clusters by implementing authentication methods, enforcing ACLs, and protecting data at rest with encryption and best practices.

Hello, and welcome back.

Earlier we discussed why Kafka infrastructure requires security. In this lesson we’ll cover the practical ways to secure a Kafka cluster: authenticating clients, enforcing access control, and protecting data at rest. These controls together reduce the blast radius of compromised services and help you meet compliance requirements.

Authentication methods

Before applications or microservices interact with Kafka, they must be authenticated. Common authentication approaches include username/password (SASL/SCRAM), Kerberos (SASL/GSSAPI), and certificate-based TLS (mutual TLS or mTLS). Each option has trade-offs in deployment complexity, operational overhead, and suitability for different environments.

<Frame>
  <img alt="The image is an informative graphic about authentication methods, highlighting Username/Password, Kerberos, and SSL/TLS, each with brief descriptions of their characteristics and uses." />
</Frame>

* Username/password (SASL/SCRAM): Simple to configure and common for development or small deployments. Works well with existing user stores but should be paired with network/TLS protections in production.
* Kerberos (SASL/GSSAPI): Enterprise-grade identity verification with strong single sign-on capabilities. Great for large, security-conscious organizations but requires running and maintaining a Kerberos infrastructure.
* TLS certificates (mutual TLS / mTLS): Certificate-based authentication using PKI. Widely adopted in production due to strong identity guarantees and compatibility with certificate rotation and automation tooling.

Authentication method comparison

| Method                           | Strengths                                          | Typical use cases                                                                |
| -------------------------------- | -------------------------------------------------- | -------------------------------------------------------------------------------- |
| `SASL/SCRAM` (username/password) | Easy to set up; supported by clients and tooling   | Development, QA, small clusters                                                  |
| `Kerberos` (SASL/GSSAPI)         | Strong enterprise identity, SSO support            | Large enterprises with existing Kerberos infrastructure                          |
| `mTLS` (Mutual TLS)              | Strong cryptographic identity, integrates with PKI | Production clusters, cloud-native environments, automated certificate management |

<Callout icon="lightbulb">
  If you don't have engineers experienced with Kerberos, prefer TLS-based certificate authentication (mTLS) for production. It provides strong identity assurance without the operational overhead of Kerberos.
</Callout>

Access control (ACLs)

Authentication proves who is connecting. After that, you must control what each principal can do. Kafka uses Access Control Lists (ACLs) to grant or deny operations such as READ, WRITE (PRODUCE), CREATE, DELETE, and cluster-level actions on resources like topics and consumer groups.

Example ACL rules might look like:

```text theme={null}
User 'LoginEventMicroService' can PRODUCE to topic LoginEvents
User 'CardPaymentService' can PRODUCE to topic CardPaymentEvents
User 'ProcessCardEvents' can CONSUME from topic CardPaymentEvents
```

<Frame>
  <img alt="The image illustrates examples of Access Control Lists (ACLs) for controlling user actions, such as producing or consuming data, on specific topics. It provides three examples of users with different permissions related to event topics." />
</Frame>

A few practical notes:

* Apply least privilege: grant each principal only the exact operations required (e.g., PRODUCE to a specific topic, not cluster-wide WRITE).
* Use distinct principals: assign unique usernames or certificate subjects per service to simplify ACL management and audits.
* Separate consumer and admin privileges: consumers typically need READ; avoid giving consumer principals DELETE or admin rights.
* Manage ACLs programmatically: store ACL intents in version control and apply them via automation to avoid drift.

Data at rest

Kafka brokers persist messages to disk. Kafka does not encrypt data at rest by itself, so rely on the underlying OS or storage provider for disk encryption. Options include filesystem-level encryption, full-disk OS encryption, or storage-provider encryption (for example, encrypted block storage).

<Frame>
  <img alt="The image illustrates data protection methods for keeping messages safe at rest, focusing on disk encryption through operating system encryption, hardware-level encryption, and Kafka's at-rest encryption." />
</Frame>

Example (AWS): if your Kafka cluster runs on EC2 instances with EBS volumes, enable `EBS` encryption (see AWS docs) so the volumes storing Kafka logs are encrypted at rest. Managed Kafka services (e.g., Amazon MSK, Confluent Cloud) typically offer encryption-at-rest as a configurable option.

Putting it together

* Authenticate every client (producer or consumer) using an appropriate mechanism: `SASL/SCRAM`, `Kerberos`, or `mTLS`.
* Enforce ACLs so authenticated principals can perform only permitted actions (produce to specific topics, consume from specific topics, etc.).
* Protect data at rest via OS or storage-level encryption (disk, volume, or managed-service options).
* Keep staging and QA environments as close to production as practical: use the same auth model and similar ACLs to catch security misconfigurations early.

<Callout icon="lightbulb">
  Apply strict ACLs and certificate-based authentication in QA and production to mirror production behavior. For simple local development you can loosen restrictions, but avoid wide-open access in shared QA environments.
</Callout>

<Frame>
  <img alt="The image illustrates Kafka security measures, including message transit security, data at rest security, user access control, and consumer authentication. It shows a flow of data topics like &#x22;LoginEvents&#x22; and &#x22;CardPaymentEvent&#x22; between producers and consumers." />
</Frame>

Quick checklist

* Enable TLS for client-broker traffic and consider mTLS for strong client identity.
* Choose an authentication mechanism that matches your operational expertise.
* Implement least-privilege ACLs and automate their application.
* Ensure storage volumes are encrypted at rest and manage keys securely.
* Monitor and audit Kafka principals and ACL changes.

Further reading and references

* [Apache Kafka Security Documentation](https://kafka.apache.org/documentation/#security)
* [AWS EBS Encryption](https://docs.aws.amazon.[SECRET_REDACTED].html)
* [Confluent: Authentication and Authorization](https://docs.confluent.io/platform/current/security/index.html)

That is it for this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/9aa104e8-faa5-4099-977f-71744306b99d/lesson/4517203b-1d19-4a12-83ce-d36a92094b8a" />
</CardGroup>
