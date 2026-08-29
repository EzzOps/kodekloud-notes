# Demo Hubble

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Observability/Demo-Hubble/page

Guide to enable and use Hubble with Cilium to observe Kubernetes L3/L4 flows and L7 HTTP, install CLI and UI, deploy samples, and validate network policies.

In this guide you'll learn how to enable and use Hubble (the observability component of Cilium) to inspect L3/L4 flows and, when L7 rules are present, HTTP request/response details inside a Kubernetes cluster. This walkthrough assumes you already have a three-node cluster with Cilium installed via Helm using default values.

## 1. Confirm cluster nodes

Run:

```bash theme={null}
kubectl get nodes
```

Example output:

```text theme={null}
NAME                       STATUS   ROLES           AGE     VERSION
my-cluster-control-plane   Ready    control-plane   4d14h   v1.32.2
my-cluster-worker          Ready    <none>          4d14h   v1.32.2
my-cluster-worker2         Ready    <none>          4d14h   v1.32.2
```

## 2. Enable Hubble Relay and Hubble UI via Helm values

Hubble is bundled with Cilium, but Relay and UI are commonly disabled. To enable them, add the fields below to your Helm `values.yaml`. See Helm chart values docs for details: [https://helm.sh/docs/topics/charts\_values/](https://helm.sh/docs/topics/charts_values/)

```yaml theme={null}
