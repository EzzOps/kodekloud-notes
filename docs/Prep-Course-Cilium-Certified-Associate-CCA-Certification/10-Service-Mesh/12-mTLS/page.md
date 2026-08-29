# mTLS

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Service-Mesh/mTLS/page

Explains how Cilium uses SPIFFE and SPIRE to provide node‑agent mutual TLS with eBPF enforcement, and how to enable, enforce, observe, and troubleshoot mTLS in Kubernetes

In this lesson we explain how mutual TLS (mTLS) is implemented in Cilium and how to enable, enforce, and debug it. mTLS provides authenticity, integrity, and confidentiality between two communicating endpoints by requiring both client and server to present and validate certificates.

Cilium integrates mTLS using the SPIFFE identity framework. SPIRE is the most common open-source SPIFFE implementation and is used by Cilium to issue identities (SVIDs) and certificates that agents use to establish mTLS sessions.

<Frame>
  <img alt="A slide titled &#x22;Mutual Authentication in Cilium&#x22; showing Cilium, SPIFFE, and SPIRE logos with arrows indicating Cilium uses SPIFFE and SPIFFE is implemented by SPIRE. Captions note SPIFFE is a framework for secure identity management and SPIRE is an open-source implementation." />
</Frame>

> **lightbulb** Quick overview: Cilium performs mTLS at the node-agent level. The Cilium agent uses SPIRE-issued SPIFFE identities (SVIDs) to establish TLS sessions with other node agents. Pods are not directly involved in the certificate exchange; the node agents handle authentication on their behalf.

## How mTLS works in a cluster

High-level components:

* Spire server (control plane) — issues SVIDs.
* Spire agent — runs on each node and obtains SVIDs from the Spire server.
* Cilium agent — performs TLS session management on behalf of pods.
* eBPF programs — enforce policies and maintain an auth table used to decide whether traffic is authenticated.

Typical sequence when a pod on Node A sends traffic to a pod on Node B:

1. eBPF looks up the auth table and policy to decide if authentication is required.
2. If authentication is required but not yet established, the initial packet is dropped by eBPF.
3. eBPF notifies the local Cilium agent that authentication is needed.
4. The Cilium agent requests SVIDs from its local Spire agent. The agent may contact the Spire server to obtain certificates.
5. Cilium TLS session managers on the two nodes establish a mutual TLS session using those certificates. (Cilium agents perform the TLS handshake; pods do not.)
6. After successful authentication, the auth table is updated and subsequent packets matching the same policy are allowed and forwarded.

This node-agent-based approach centralizes authentication at the host level rather than inside each pod, simplifying certificate management and reducing workload changes.

<Frame>
  <img alt="An architecture diagram of mTLS on Cilium showing a spire-server and spire-agents in cilium pods issuing SVIDs to TLS session managers. It illustrates auth caches, a pluggable auth interface, eBPF-populated auth tables, and secure pod-to-pod authentication." />
</Frame>

## Key components and their roles

|     Component | Role                                                                                             |
| ------------: | ------------------------------------------------------------------------------------------------ |
|  Cilium agent | Manages TLS sessions and enforces policies on behalf of pods.                                    |
| eBPF programs | Enforce network policy and maintain an auth table used to decide forwarding vs. triggering auth. |
|  Spire server | Issues SPIFFE Verifiable Identity Documents (SVIDs) to agents.                                   |
|   Spire agent | Runs on each node, obtains SVIDs from the Spire server for local workloads.                      |
|        SPIFFE | Identity framework used to represent workload identities (URI-based).                            |

Useful links:

* [Cilium](https://cilium.io/)
* [SPIFFE](https://spiffe.io/)
* [SPIRE](https://spiffe.io/spire/)
* [eBPF](https://ebpf.io/)
* [CiliumNetworkPolicy language](https://docs.cilium.io/en/stable/policy/language/)

## Enabling mTLS in Cilium

At a minimum you must:

1. Enable encryption for node-to-node traffic (IPsec or WireGuard).
2. Enable Cilium authentication and the SPIRE integration.
3. Optionally allow Cilium to install SPIRE for you (convenience install).

Example Helm / operator values snippet to enable encryption and SPIRE integration:

```yaml theme={null}
encryption:
  enabled: true
  type: ipsec

authentication:
  enabled: true
  mutual:
    spire:
      # Enable SPIRE integration (beta)
      enabled: true
      install:
        # Enable SPIRE installation (only takes effect if
        # authentication.mutual.spire.enabled is true)
        enabled: true
```

After deployment you should see one Spire agent per node and a Spire server:

```bash theme={null}
› kubectl get pod -A
NAMESPACE           NAME                 READY   STATUS    RESTARTS   AGE
cilium-spire        spire-agent-cx9h6    1/1     Running   0          68m
cilium-spire        spire-agent-hrkrm    1/1     Running   0          68m
cilium-spire        spire-agent-zvpfn    1/1     Running   0          68m
cilium-spire        spire-server-0       2/2     Running   0          68m

› kubectl get svc -A
NAMESPACE           NAME            TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)     AGE
cilium-spire        spire-server    ClusterIP  10.96.75.71    <none>        8081/TCP    69m
```

## Enforcing mTLS for specific traffic

To require mTLS, create a CiliumNetworkPolicy that matches the traffic and sets authentication mode to required. You only need one matching policy in one direction: either an ingress policy on the destination or an egress policy on the source.

Example: require authentication for ingress on port 80 to pods labeled app=pod2

```yaml theme={null}
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: all-server
spec:
  endpointSelector:
    matchLabels:
      app: pod2
  ingress:
  - toPorts:
    - ports:
      - port: "80"
        protocol: TCP
    authentication:
      mode: required
```

This policy only allows TCP traffic to port 80 for pods with label app=pod2 when a mutual authentication session exists between the endpoints.

> **lightbulb** Cilium agents perform the mTLS authentication on behalf of pods. Pods themselves do not exchange certificates — Cilium's TLS session managers handle authentication between node agents.

## Observability — checking logs and debugging

Enable debug logging in Cilium (via Helm values or CiliumConfig) to see the authentication flow in agent logs. Useful commands:

```bash theme={null}
