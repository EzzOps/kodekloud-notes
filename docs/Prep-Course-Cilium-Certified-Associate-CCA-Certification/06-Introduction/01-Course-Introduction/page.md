# Install Cilium onto the current kubeconfig cluster
cilium install

# Check cluster-level Cilium status from your workstation
cilium status
```

Inside a Cilium pod (advanced debug / diagnostic tools)

```bash theme={null}
# Run the in-pod 'cilium' binary for status or diagnostics
kubectl -n kube-system exec -it <cilium-pod> -- cilium status

# Use the dedicated debug binary inside the pod
kubectl -n kube-system exec -it <cilium-pod> -- cilium-dbg help
```

Key takeaway: treat the local CLI and the in-pod binaries as separate tools with different responsibilities. Use the local CLI primarily for installation and routine status checks, and drop into the pod (`cilium` or `cilium-dbg`) for low-level, in-cluster debugging.

Links and references

* [Cilium Documentation — CLI](https://docs.cilium.io/en/stable/gettingstarted/cli/)
* [kubectl exec reference](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#exec)

- [Watch Video](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/2fded455-95ea-4183-8cce-f17de214691f/lesson/cc56f4b0-1780-44b2-8ead-8b4fbec08f5d)


# Course Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Introduction/Course-Introduction/page

Hands-on course teaching Cilium networking, security, observability, installation, multi-cluster and exam prep for Kubernetes operators using eBPF

Welcome to the Cilium Certified Associate course. I’m Sanjeev — in this lesson I’ll walk you through the practical skills required to operate Cilium in production Kubernetes environments with confidence.

Cilium is a leading Kubernetes networking and security project powered by eBPF and used by organizations such as Adobe, Google, and Datadog. Many managed Kubernetes offerings support Cilium (for example, [AWS EKS](https://learn.kodekloud.com/user/courses/aws-eks) and [GKE — Google Kubernetes Engine](https://learn.kodekloud.com/user/courses/gke-google-kubernetes-engine)), and companies like GitHub use it to enhance security and observability.

This course follows a learn-by-doing approach: concepts are introduced, then immediately reinforced with hands-on labs where you can experiment, troubleshoot, and validate real-world scenarios.

What you’ll learn (high level)

* Kubernetes networking fundamentals and where Cilium fits into the stack.
* Cilium architecture and the role of eBPF in modern networking and security.
* Installation and lifecycle management with CLI and Helm.
* Core networking: IPAM modes, routing, kube-proxyless operation, and internal traffic flow.
* Advanced security with Cilium Network Policies (CNPs) beyond standard Kubernetes NetworkPolicies.
* Service mesh capabilities, integration with Ingress and the [Gateway API](https://gateway-api.sigs.k8s.io/), and TLS/encryption patterns.
* Multi-cluster connectivity using Cluster Mesh — global services and cross-cluster policies.
* Observability and troubleshooting with Hubble, Prometheus, and Grafana.
* Advanced topics: egress gateways, LoadBalancer IPAM, and BGP integration.
* Mock exams to measure readiness for certification.

This course includes step-by-step demos and labs so you can try each feature hands-on.

<Frame>
  <img alt="A slide titled &#x22;Cilium Certified Associate&#x22; with bullet points about Kubernetes networking and Cilium topics is shown on the left. On the right, a presenter wearing a KodeKloud shirt speaks into a microphone." />
</Frame>

Install and configure Cilium
You’ll see detailed demos that show the components Cilium deploys and how to maintain them. The demos include both quick CLI installs and Helm-based installations so you can use the approach that matches your environments.

Example — adding the official Cilium Helm repository:

```bash theme={null}
