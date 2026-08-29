# Example output:
# hubble-relay-59cc4d545b-dv2vc        1/1   Running   0   21h
kubectl get svc -n kube-system
# Example output:
# NAME           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
# hubble-peer    ClusterIP   10.96.168.58    <none>        443/TCP   21h
# hubble-relay   ClusterIP   10.96.219.164   <none>        80/TCP    21h
# hubble-ui      ClusterIP   10.96.132.144   <none>        80/TCP    21h
```

<Callout icon="lightbulb">
  Hubble server runs inside the Cilium agent on each node (no separate pod per node). Hubble relay and Hubble UI run as separate deployments/pods and aggregate/visualize node-level flow data.
</Callout>

Installing the Hubble CLI

Install the Hubble CLI on your workstation to query the relay or stream flows directly. The Hubble project provides prebuilt release binaries. Example (Linux):

```bash theme={null}
HUBBLE_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/hubble/master/stable.txt)
HUBBLE_ARCH=amd64
if [ "$(uname -m)" = "aarch64" ]; then HUBBLE_ARCH=arm64; fi

# Download the tarball and its checksum
curl -L --fail --remote-name-all \
  "https://github.com/cilium/hubble/releases/download/${HUBBLE_VERSION}/hubble-linux-${HUBBLE_ARCH}.tar.gz" \
  "https://github.com/cilium/hubble/releases/download/${HUBBLE_VERSION}/hubble-linux-${HUBBLE_ARCH}.tar.gz.sha256sum"

sha256sum --check "hubble-linux-${HUBBLE_ARCH}.tar.gz.sha256sum"

sudo tar xzvf "hubble-linux-${HUBBLE_ARCH}.tar.gz" -C /usr/local/bin
rm "hubble-linux-${HUBBLE_ARCH}.tar.gz" "hubble-linux-${HUBBLE_ARCH}.tar.gz.sha256sum"
```

Accessing Hubble relay/UI from your workstation

A common approach is to port-forward the hubble-relay service (or use the cilium helper). Example:

```bash theme={null}
kubectl -n kube-system port-forward service/hubble-relay 4245:80
# Forwarding from 127.0.0.1:4245 -> 4245
```

Or use the Cilium CLI helper:

```bash theme={null}
cilium hubble port-forward
```

<Callout icon="warning">
  Avoid exposing Hubble relay/UI to the public internet. Use port-forwarding, a secure tunnel, or an authenticated proxy when accessing Hubble from your workstation.
</Callout>

Using the Hubble CLI

The CLI supports expressive filters for drilling into specific flows. Use `--help` to view all options. Common examples:

Show flows to or from a pod named "green" (both directions):

```bash theme={null}
hubble observe --pod green
```

Show flows originating from the "green" pod:

```bash theme={null}
hubble observe --from-pod green
```

Show flows destined to the "green" pod:

```bash theme={null}
hubble observe --to-pod green
```

Filter by destination port and protocol (e.g., HTTP on port 3000):

```bash theme={null}
hubble observe --to-pod green --port 3000 --protocol http
```

Filter by verdict (result of packet handling). Valid verdicts include:

* FORWARDED
* DROPPED
* AUDIT
* REDIRECTED
* ERROR
* TRACED
* TRANSLATED

Example:

```bash theme={null}
hubble observe --to-pod green --port 3000 --protocol http --verdict DROPPED
```

Using the Hubble UI

The Hubble UI provides a graphical way to explore flows, dependency graphs, and policy denials. The cilium CLI can forward and open the UI for you:

```bash theme={null}
cilium hubble ui
# Opening "http://localhost:12000" in your browser...
```

The UI supports the same filtering options as the CLI (source/destination pod/service, status, protocol, ports, verdicts, time ranges) and is especially useful for interactive debugging and visualizing service dependencies.

Summary

Hubble (embedded in Cilium) together with Hubble relay and Hubble UI delivers low-overhead, high-fidelity network observability for Kubernetes clusters. Use the CLI for automation and quick inspections; use the UI for visual exploration, dependency graphs, and troubleshooting policy-related denials.

Links and references

* Hubble repository and releases: [https://github.com/cilium/hubble](https://github.com/cilium/hubble)
* Cilium documentation: [https://docs.cilium.io/](https://docs.cilium.io/)
* Kubernetes Concepts: [https://kubernetes.io/docs/concepts/](https://kubernetes.io/docs/concepts/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/b4c15752-3e42-43af-bedf-4a4c204ef5d8/lesson/73815b34-0105-4986-a487-e70deb12dcdd" />
</CardGroup>


# Prometheus and Grafana Metrics

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Observability/Prometheus-and-Grafana-Metrics/page

Guide to enable and expose Cilium, Hubble, and operator metrics for Prometheus and Grafana using Helm values, ServiceMonitors, and verification steps.

This guide shows how to enable and expose Cilium metrics so an external observability stack (Prometheus + Grafana) can collect and visualize them. Cilium can emit metrics for its datapath components, Hubble (flow telemetry), and the Cilium Operator — but these metrics are not enabled by default. Use Helm values to enable the relevant metric endpoints and ServiceMonitors so a Prometheus Operator can discover and scrape them.

<Frame>
  <img alt="A diagram of an observability setup where Prometheus scrapes metrics from Cilium running in a Kubernetes cluster (two nodes with pods) and Grafana queries Prometheus for visualization. A caption notes that Cilium, Hubble, and the Cilium Operator do not expose metrics by default." />
</Frame>

## Enable Cilium, Operator and Hubble metrics via Helm values

Below is a concise values file example for the Cilium Helm chart. Adjust the metric families in `hubble.metrics.enabled` to match the observability needs for your cluster and Cilium version.

```yaml theme={null}
