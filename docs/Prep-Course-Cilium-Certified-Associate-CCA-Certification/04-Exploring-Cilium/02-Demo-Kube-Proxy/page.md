# list Cilium pods (typically in the kube-system namespace)
kubectl -n kube-system get pods -l k8s-app=cilium

# view logs from a specific Cilium pod
kubectl -n kube-system logs <cilium-pod-name>
```

When debug is enabled, logs will contain more detailed information about policy decisions, BPF loading, and datapath events. Use pod logs combined with `cilium status` and `cilium endpoint list` for deeper troubleshooting.

> **lightbulb** Enabling debug logging produces verbose output and can increase log volume significantly. Use it for troubleshooting and disable it (set debug false) when finished.

> **warning** Do not leave debug logging enabled in production for long periods. Increased log volume can impact storage and performance and may expose sensitive internal details.

## Links and references

* [Cilium documentation](https://cilium.io/docs/)
* [Kubernetes documentation - ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
* [kubectl reference](https://kubernetes.io/docs/reference/kubectl/)

- [Watch Video](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/0807e400-fd1b-4f25-bba5-d0fdb0f4e3f2/lesson/85a788b7-157b-4a8e-afda-d67aa52cf9d3)


# Demo Kube Proxy

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Exploring-Cilium/Demo-Kube-Proxy/page

Guide to configuring Cilium to run alongside or replace kube-proxy using eBPF on a kind cluster, including installation, kube-proxy removal, iptables cleanup and service connectivity tests.

In this lesson you will learn how to configure Cilium to either run alongside kube-proxy (default) or act as a complete replacement using Cilium's eBPF-based datapath. The walkthrough uses a kind cluster, but the steps apply to other Kubernetes variants (Minikube, kubeadm) with minor adjustments.

<Frame>
  <img alt="A presentation slide with the word &#x22;Demo&#x22; on the left and &#x22;Kube Proxy&#x22; displayed on the right over a blue-green curved shape. A small &#x22;© Copyright KodeKloud&#x22; appears in the bottom-left." />
</Frame>

## Prerequisites

* kind (Kubernetes in Docker) — [https://kind.sigs.k8s.io/](https://kind.sigs.k8s.io/)
* kubectl — [https://kubernetes.io/docs/tasks/tools/](https://kubernetes.io/docs/tasks/tools/)
* Helm — [https://helm.sh/](https://helm.sh/)
* Basic familiarity with CNI/Cilium and kube-proxy concepts

## Create a kind cluster

Save the following as `kind.config` and create a cluster named `my-cluster`. This configuration disables the default CNI so we can install Cilium:

```yaml theme={null}
