# Audit Logging

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Kubernetes-Security-Fundamentals/Audit-Logging/page

Audit logging in Kubernetes captures API server requests to detect unauthorized activities and control event logging through defined audit policies.

Audit logging in Kubernetes captures detailed records of all API server requests, helping you detect suspicious or unauthorized activities within your cluster. By defining audit policies, you can control which events to log, reducing noise and focusing on critical operations.

<Callout icon="lightbulb">
  Audit logging is disabled by default in Kubernetes. Enabling it requires configuring the API server to use an audit policy and log backend.
</Callout>

## Why Audit Logging Matters

* **Security:** Track changes and identify unauthorized access.
* **Compliance:** Maintain an immutable record of user actions.
* **Troubleshooting:** Correlate events with incidents for diagnostics.

## Viewing Falco Alerts

Before diving into Kubernetes-native auditing, you might already be using Falco to detect suspicious container activities. For example:

```bash theme={null}
kubectl logs -f falco-6t2dd
