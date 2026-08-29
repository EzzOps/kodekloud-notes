# Authentication

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Securing-Workloads/Authentication/page

Describes zero trust authentication principles, signals, implementation mechanisms, and best practices for verifying identities, device posture, context, and policies to enforce least privilege and continuous verification

You may have heard the term "zero trust." In practical terms for authentication, zero trust means "never trust, always verify": every request, connection, and identity must be authenticated and authorized — even when originating from inside your network.

<Frame>
  <img alt="The image illustrates the Zero Trust Security Model, emphasizing &#x22;Never trust, always verify,&#x22; with focus areas such as devices, identities, data, applications, infrastructure, and network." />
</Frame>

Zero-trust authentication relies on validating multiple signals before granting access. These signals reduce attack surface and enforce least privilege by evaluating identity, device posture, context, and policy together.

## Core signals evaluated in zero-trust authentication

| Signal                  | What it answers                       | Examples                                                        |
| ----------------------- | ------------------------------------- | --------------------------------------------------------------- |
| Identity                | Who or what is requesting access?     | User accounts, service accounts, workloads, device certificates |
| Device posture          | Is the device trusted and compliant?  | Patch level, disk encryption, endpoint protection status        |
| Context                 | Where/how is the request originating? | IP location, time of day, network type (LAN vs public)          |
| Policy                  | Which access rules apply?             | Role-based, attribute-based, least-privilege policies           |
| Continuous verification | Is the session still valid over time? | Re-authentication, token revocation, anomaly detection          |

## Common mechanisms for implementing zero-trust authentication

Use a combination of strong identity, short-lived credentials, and centralized policy enforcement:

| Mechanism                     | Purpose                                                   | Typical use case                                                    |
| ----------------------------- | --------------------------------------------------------- | ------------------------------------------------------------------- |
| Mutual TLS (mTLS)             | Strong service-to-service identity and encrypted channels | Workload-to-workload authentication inside clusters or service mesh |
| JWT / OAuth2 / OpenID Connect | User authentication and authorization claims              | API access, single sign-on (SSO), federated identity                |
| Short-lived credentials       | Minimize impact of credential compromise                  | Session tokens, temporary cloud credentials                         |
| Centralized policy engines    | Enforce consistent access decisions                       | Gate authorization checks across services (RBAC/ABAC)               |

> **lightbulb** Zero trust is not a single product — it’s an architecture. Combine identity validation, device posture checks, contextual signals, and policy enforcement to achieve effective zero-trust authentication.

## How to evaluate an identity request (practical checklist)

When a request arrives, apply this sequence:

1. Verify identity:
   * Confirm the credential (certificate, JWT, OAuth token) is valid and signed by a trusted issuer.
   * Check token expiration and revocation status.
2. Assess device posture:
   * Ensure the requesting device meets compliance requirements (encryption, patch level).
3. Inspect context:
   * Evaluate request origin (IP, region), time, and recent behavior for anomalies.
4. Apply policy:
   * Map the identity and attributes to access policies (RBAC/ABAC), ensure least privilege.
5. Enforce step-up controls if needed:
   * Require multi-factor authentication (MFA), additional approvals, or limited session scopes.
6. Continuously re-evaluate:
   * Re-check on sensitive actions or periodically during long-lived sessions.

## Implementation patterns and best practices

* Use mTLS for workload-to-workload authentication where possible (service mesh like Istio can automate this).
* Prefer short-lived tokens and automatic refresh flows to limit credential lifetime.
* Centralize policy evaluation to keep authorization consistent across services.
* Monitor and log authentication decisions for auditing and anomaly detection.
* Apply least privilege: start with deny-by-default and grant the minimum required access.

> **warning** Misconfigured identity providers, long-lived tokens, or inconsistent policies undermine zero-trust. Validate token issuers, use secure defaults, and automate policy propagation.

## Further reading and references

* [Zero Trust Architecture (NIST)](https://csrc.nist.gov/publications/detail/sp/800-207/final)
* [OAuth 2.0](https://oauth.net/2/)
* [OpenID Connect](https://openid.net/connect/)
* [Mutual TLS (mTLS) Concepts](https://tools.ietf.org/html/rfc5246)

Use these resources to deepen your understanding and to implement zero-trust authentication across users, devices, and services.

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/17ba1cac-61f4-48b6-b354-c2c735f5791d/lesson/8ed665e7-46f4-4399-b00c-ffd3262dc9d6)
