# Policy Audit Mode

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Network-Policy/Policy-Audit-Mode/page

Explains Cilium's policy audit mode for observing would-be allows or denies, how to enable globally or per-endpoint, and how to inspect audited flows with Hubble

In this lesson you'll learn how Cilium's policy audit mode works and how to enable it. Policy audit mode lets you observe what a CiliumNetworkPolicy would do (allow or deny) without actually dropping traffic. This is useful for validating policies safely before enforcing them in production.

What does audit mode look like in practice? Consider three pods: frontend, backend, and db. You apply a policy that selects the db pod and allows ingress only from backend:

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "audit-example"
spec:
  endpointSelector:
    matchLabels:
      app: db
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: backend
```

With audit mode enabled, traffic that would normally be denied (for example, frontend -> db) is still allowed, but Cilium logs that the flow would have been denied. This enables safe, observable policy rollouts without blackholing traffic.

<Frame>
  <img alt="A diagram titled &#x22;Policy Audit Mode&#x22; showing Frontend and Backend pods trying to access a DB pod through a policy. The logs indicate Backend -> db allowed and Frontend -> db denied (audited)." />
</Frame>

Why use policy audit mode?

* Validate policies by observing “would-be” denies without impacting live traffic.
* Identify false positives or unintended blocks before switching to enforcement.
* Roll out complex network policies gradually and safely.

Verdicts and their meanings (quick reference):

| Policy Verdict            | Meaning                                                                                              |
| ------------------------- | ---------------------------------------------------------------------------------------------------- |
| none (INGRESS AUDITED)    | Traffic would be denied by policy, but audit mode allowed the flow and recorded the audited verdict. |
| L3-Only (INGRESS ALLOWED) | Traffic is allowed by the policy (L3 match) and is permitted.                                        |
| other verdicts            | May indicate more specific L4/L7 evaluation — inspect Hubble logs for details.                       |

How to enable audit mode
There are two ways to enable policy audit mode:

1. Globally (all endpoints) via Helm — requires restarting Cilium components.
2. Per-endpoint (specific endpoints) using cilium-dbg — no cluster-wide restart required.

Enable audit mode globally

* Edit your Cilium Helm chart values to turn on audit mode:

```yaml theme={null}
policyAuditMode: true
```

* After updating Helm values, restart the Cilium operator and agent so the change takes effect:

```bash theme={null}
kubectl -n kube-system rollout restart deployment/cilium-operator
kubectl -n kube-system rollout restart daemonset/cilium
```

Enable audit mode for a specific endpoint

* Use cilium-dbg inside a cilium-agent pod to change a single endpoint's configuration. Replace variables with your values:

```bash theme={null}
