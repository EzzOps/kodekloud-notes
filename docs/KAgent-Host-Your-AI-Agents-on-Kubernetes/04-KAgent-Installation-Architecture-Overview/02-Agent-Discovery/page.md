# Agent A - Makes itself available via A2A
apiVersion: kagent.dev/v1alpha1
kind: Agent
metadata:
  name: flight-agent
spec:
  systemMessage: "I book flights"
  a2aConfig:
    skills:
      - name: "book_flight"
        description: "Books international flights"

---
# Agent B - Uses Agent A via A2A
apiVersion: kagent.dev/v1alpha1
kind: Agent
metadata:
  name: travel-planner
spec:
  systemMessage: "I plan trips"
  tools:
    - type: Agent
      agent:
        ref: flight-agent  # Uses Agent A via the A2A protocol
```

When the travel-planner receives a request requiring a flight booking, it invokes `flight-agent`'s `book_flight` skill over A2A and uses the returned result as part of the itinerary.

## Summary

A2A is a protocol that standardizes agent-to-agent communication to support multi-agent orchestration, secure discovery and authentication, and streaming task lifecycles. It enables agents across organizations and environments to interoperate while remaining agnostic to underlying model frameworks.

Further reading and references

* OpenID Connect: [https://openid.net/connect/](https://openid.net/connect/)
* JWT (JSON Web Tokens): [https://jwt.io/](https://jwt.io/)
* Well-known URIs (RFC 5785): [https://datatracker.ietf.org/doc/html/rfc5785](https://datatracker.ietf.org/doc/html/rfc5785)
* Kubernetes documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

That's it for this lesson. The course also covers KAgent architecture.

- [Watch Video](https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/45e1f0ac-8ec5-4cb3-8804-9953a96a67b5/lesson/424b0a61-376b-4ab7-8a27-fbc3f78a3bd7)


# Agent Discovery

Source: https://notes.kodekloud.com/docs/KAgent-Host-Your-AI-Agents-on-Kubernetes/KAgent-Installation-Architecture-Overview/Agent-Discovery/page

Describes agent card discovery methods for A2A systems, comparing well-known URIs, registries, and direct configuration, plus security practices and deployment trade-offs.

When two AI agents need to collaborate over the A2A protocol, they first must find one another and understand what each can do. The A2A specification standardizes agent self-descriptions as "agent cards" (digital business cards for A2A servers), but how clients discover those cards depends on the environment and requirements. This lesson explains common discovery strategies, trade-offs, and security considerations so you can choose the right approach for public, enterprise, or private deployments.

An agent card typically provides the information a client needs to:

* Understand an agent's capabilities and skills.
* Learn how to communicate with the agent (endpoints and message formats).
* Authenticate and establish a secure connection.
* Construct requests appropriate to the agent's capabilities.

Below are the most common discovery strategies and practical considerations for each.

## Well-Known URI (recommended for public agents)

The well-known URI approach follows web standards ([RFC 8615](https://datatracker.ietf.org/doc/html/rfc8615)). Each A2A server exposes its agent card at a predictable path under its domain:

`/.well-known/agent-card.json`

Example: if the client discovers the domain `smartthermostat.example.com`, it can fetch the card at:

```http theme={null}
https://smartthermostat.example.com/.well-known/agent-card.json
```

Typical discovery flow:

1. Client knows or learns a candidate domain (DNS, search, or user input).
2. Client performs an HTTP GET to the well-known path on that domain.
3. If available and accessible, the server returns a JSON agent card describing the agent(s) and connection details.

Example using curl:

```bash theme={null}
curl -sS https://smartthermostat.example.com/.well-known/agent-card.json
```

Notes and considerations:

* The card may describe a single agent or multiple agents hosted at the domain.
* Sensitive fields (internal URIs, auth endpoints) should be protected; authentication on the well-known endpoint may be required.
* Advantages: easy to implement, friendly to automated discovery, suitable for public or domain-controlled agents.
* Best suited for: open discovery scenarios, public-facing agents, or where domain-based discovery is appropriate.

## Curated Registries (catalog-based discovery)

Registries act as an intermediary catalog (like an app store) that index and serve agent cards. Clients query the registry for agents matching desired capabilities.

Typical flow:

1. A2A servers publish (push) agent cards to the registry.
2. Clients query the registry API using search criteria (skills, tags, provider).
3. The registry returns matching agent cards, potentially filtered by client permissions.

Advantages:

* Centralized governance, auditing, and lifecycle management.
* Capability-based discovery: search by skill, tag, or provider.
* Built-in access control and trust networks.
* Enables discovery without knowing individual agent domains.

Considerations:

* Requires deploying and operating registry infrastructure.
* A2A spec currently does not define a standard registry API; implementations vary.
* The registry becomes a critical component for availability and trust.

Use cases:

* Enterprise agent catalogs and marketplaces.
* Skill-based discovery in multi-tenant environments.
* Public marketplaces and curated app stores.

## Direct Configuration (private or tightly-coupled discovery)

Direct configuration is the simplest approach for closed, static, or development environments. The client receives agent card information directly (config file, environment variables, or a proprietary API).

Typical pattern:

* Agent card details are provisioned to the client at deployment or startup.

Example configuration (JSON):

```json theme={null}
{
  "agent_id": "internal-thermostat-1",
  "agent_card": {
    "name": "Internal Thermostat Agent",
    "endpoint": "https://10.0.1.42:8443/a2a",
    "auth": {
      "type": "mTLS"
    },
    "capabilities": ["temperature.read", "temperature.set"]
  }
}
```

Advantages:

* Simple and reliable for known relationships.
* Ideal for development, testing, and tightly coupled microservices.
* No discovery infrastructure required; full control over agent relationships.

Considerations:

* Limited flexibility in dynamic environments.
* Updating agent details often requires redeployment or reconfiguration.
* Not standardized or scalable for large, dynamic agent networks.

Use cases:

* Development and QA.
* Private/internal agent networks.
* Tightly-coupled microservice integrations.

## Strategy comparison

| Discovery Method     |                          Best for | Pros                                                                                                | Cons                                                                   |
| -------------------- | --------------------------------: | --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Well-Known URI       |        Public/domain-based agents | Easy to implement, automated discovery friendly, standardized path (`/.well-known/agent-card.json`) | May expose sensitive info unless protected; relies on domain knowledge |
| Curated Registry     | Enterprise catalogs, marketplaces | Centralized search and governance, RBAC, capability-based discovery                                 | Needs infrastructure and custom APIs; single point of availability     |
| Direct Configuration |        Private/static deployments | Simple, reliable, no discovery infra needed                                                         | Not flexible or scalable; updates require redeploy/reconfig            |

Remember: agent cards are often the first thing exchanged between client and agent. Because they can include sensitive information (internal endpoints, auth details, or descriptions of privileged skills), you should protect agent cards appropriately.

> **lightbulb** Consider the sensitivity of the information exposed in agent cards and choose discovery and access controls accordingly.

## Securing Agent Cards

<Frame>
  <img alt="A dark-themed slide titled &#x22;Securing Agent Cards&#x22; showing four numbered cards with icons and labels: 01 URLs for internal or restricted agents, 02 Descriptions of sensitive skills, 03 Authentication endpoints, and 04 Internal service details. Each card is color-accented and arranged horizontally." />
</Frame>

Common protection mechanisms:

* Authenticated agent cards
  * Serve extended or sensitive fields only to authenticated, authorized clients.
  * Provide different card versions depending on client permissions (selective disclosure).

* Secure endpoints
  * Use mutual TLS (mTLS) for certificate-based authentication of clients.
  * Apply network-level controls (IP allowlists, private network access).
  * Protect APIs with OAuth 2.0, API keys, signed tokens, or equivalent HTTP auth.

* Registry-based selective disclosure
  * Registries can return filtered agent cards depending on client identity and access rights.
  * Role-based access control (RBAC) lets registries hide sensitive fields from unauthorized clients.

Combine mechanisms (authentication + transport security + access control) based on the sensitivity of the card fields and your deployment requirements.

## Best practices

<Frame>
  <img alt="A slide titled &#x22;Best Practices&#x22; with four numbered panels listing recommendations. The items advise using out-of-band dynamic credentials, implementing proper authentication and authorization, protecting endpoints serving agent cards, and considering different card versions for different audiences." />
</Frame>

* Prefer out-of-band dynamic credentials (short-lived tokens or ephemeral certificates) rather than embedding long-lived static credentials in agent cards.
* Implement strong authentication and authorization for endpoints that serve agent cards.
* Protect discovery endpoints (well-known URIs and registry APIs) with appropriate transport and network security (HTTPS, mTLS, allowlists).
* Consider publishing multiple card views (public summary vs. internal full card) and only reveal sensitive details to authorized clients.
* Audit access to agent cards and monitor discovery traffic for anomalies and abuse.

## Future considerations

The A2A community is working toward:

* Standardized registry APIs and discovery protocols.
* Enhanced selective disclosure and privacy-preserving card formats.
* Improved scalability for large agent networks and federated discovery.
* Better tooling for catalog governance and trust establishment.

Choose discovery and security strategies that match your deployment goals (public, enterprise, private) and plan to evolve them as standards and tooling progress.

## Links and references

* [RFC 8615 — Well-Known URIs](https://datatracker.ietf.org/doc/html/rfc8615)
* OAuth 2.0 overview: [https://oauth.net/2/](https://oauth.net/2/)
* mTLS concept summary: [https://en.wikipedia.org/wiki/Mutual\_authentication](https://en.wikipedia.org/wiki/Mutual_authentication)

- [Watch Video](https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/45e1f0ac-8ec5-4cb3-8804-9953a96a67b5/lesson/f721d92d-9e70-4265-8cae-4c55a230d034)
