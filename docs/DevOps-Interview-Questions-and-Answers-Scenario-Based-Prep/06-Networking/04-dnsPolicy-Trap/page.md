# Compare using constant-time comparison
if hmac.compare_digest(sig_header.split("=", 1)[1], expected):
    # Process the webhook
    print("Valid signature")
else:
    # Reject the webhook
    print("Invalid signature")
```

Additional security best practices:

* Only accept requests over HTTPS.
* Validate the payload schema and required fields before processing.
* Log received events and verification outcomes for auditing and debugging.
* Optionally implement IP allowlisting if the provider publishes their sending IP ranges.

## Polling vs Webhooks — quick comparison

| Approach |                                 When to use | Pros                                              | Cons                                                     |
| -------- | ------------------------------------------: | ------------------------------------------------- | -------------------------------------------------------- |
| Polling  |        Simple integrations, sporadic events | Easy to implement, works without public endpoints | Inefficient, higher latency, scales poorly               |
| Webhooks | Real-time notifications, high volume events | Low latency, efficient, event-driven              | Requires public endpoint, must handle security & retries |

## Examples and references

Popular services that use webhooks:

* GitHub triggers CI/CD with webhooks: [https://docs.github.com/en/developers/webhooks-and-events/webhooks](https://docs.github.com/en/developers/webhooks-and-events/webhooks)
* Slack uses webhooks to post messages into channels: [https://api.slack.com/messaging/webhooks](https://api.slack.com/messaging/webhooks)

When designing integrations, choose webhooks for near-instant notifications and efficiency, and reserve polling only for simple or constrained scenarios.

- [Watch Video](https://learn.kodekloud.com/user/courses/devops-interview-prep/module/c1eb3967-23d3-4a34-b23d-14a892f95e1d/lesson/41f5da65-39ef-4dbc-8d86-a2a5156d1c66)


# dnsPolicy Trap

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/Networking/dnsPolicy-Trap/page

Explains Kubernetes pod DNS failures caused by dnsPolicy and /etc/resolv.conf misconfiguration, causing external names to resolve but cluster service names like kubernetes.default to fail.

If you run `nslookup` from inside a pod and `kubernetes.default` fails while `google.com` still resolves, the pod can reach some DNS server but not the cluster DNS. This typically happens because of one file and one setting: `/etc/resolv.conf` inside the pod and the pod's `dnsPolicy`.

Example failure:

```bash theme={null}
$ nslookup kubernetes.default
** server can't find kubernetes.default: NXDOMAIN

$ nslookup google.com
Name:    google.com
Address: 142.250.4.100
```

Summary: external names resolve (node DNS works), but internal cluster names fail (cluster DNS not being used).

## Why this happens

Every pod has its own `/etc/resolv.conf`. Kubernetes (kubelet) writes that file for the pod based on the pod's `dnsPolicy` and whether the pod uses the host network. A typical pod's `/etc/resolv.conf` contains three important parts:

* `nameserver` — usually the cluster DNS (kube-dns/CoreDNS) service IP.
* `search` — includes the pod's namespace, `svc`, and `cluster.local` so short service names expand correctly.
* `options` — e.g., `ndots` value.

Example `/etc/resolv.conf` inside a normal pod:

```text theme={null}
