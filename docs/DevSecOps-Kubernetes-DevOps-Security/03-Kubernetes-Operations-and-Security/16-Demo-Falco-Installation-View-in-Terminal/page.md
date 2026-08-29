# Download and extract for Linux (amd64)
curl -L https://github.com/aquasecurity/kube-bench/releases/latest/download/kube-bench_$(uname -s)_amd64.tar.gz | tar xz

# Move the executable into your PATH
sudo mv kube-bench /usr/local/bin/
```

Then run:

```bash theme={null}
kube-bench master --version 1.15
```

***

## 3. Filtering Checks & JSON Output

To focus on specific controls or integrate results into CI/CD workflows, use the `--check` and `--json` flags.

### Docker Example

```bash theme={null}
docker run --rm \
  --pid host \
  -v /etc:/etc:ro \
  -v /var:/var:ro \
  -t aquasec/kube-bench:latest master \
  --version 1.19 \
  --check 1.2.7,1.2.8,1.2.9 \
  --json
```

### Binary Example

```bash theme={null}
kube-bench master \
  --version 1.15 \
  --check 1.2.7,1.2.8,1.2.9 \
  --json
```

The resulting JSON can be parsed to enforce compliance gates in your automation pipelines.

***

## Comparison: Docker vs Standalone Binary

| Aspect     | Docker                        | Standalone Binary                     |
| ---------- | ----------------------------- | ------------------------------------- |
| Setup      | No installation required      | Requires download and `mv` to `PATH`  |
| Isolation  | Fully containerized           | Runs directly on host                 |
| Versioning | Image tag (e.g., `latest`)    | Explicit download of specific release |
| Use Case   | Quick audits, ephemeral scans | Persistent, on-host integrations      |

***

## Links and References

* [CIS Kubernetes Benchmark][cis-k8s]
* [CIS GKE Benchmark][cis-gke]
* [CIS EKS Benchmark][cis-eks]
* [Kube-bench on GitHub][kube-bench]
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

[cis-k8s]: https://www.cisecurity.org/benchmark/kubernetes/

[cis-gke]: https://www.cisecurity.org/benchmark/google_kubernetes_engine/

[cis-eks]: https://www.cisecurity.org/benchmark/amazon_elastic_kubernetes_service/

[kube-bench]: https://github.com/aquasecurity/kube-bench

- [Watch Video](https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/fc1733bc-1e9c-4e38-ae86-84e6bd9af04d/lesson/4f92306b-dac3-4d34-acda-abcaad1ddbfc)


# Demo Falco Installation View in Terminal

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/Kubernetes-Operations-and-Security/Demo-Falco-Installation-View-in-Terminal/page

This hands-on guide teaches how to install Falco on Ubuntu, generate security alerts, and view them in the terminal.

In this hands-on guide, you’ll learn how to install Falco on an Ubuntu VM running a Kubernetes cluster, generate security alerts, and view them directly in your terminal. Falco is a runtime security tool for detecting anomalous activity in your containers and hosts.

## Prerequisites

* Ubuntu-based virtual machine (18.04+).
* Kubernetes cluster up and running.
* `kubectl` configured to talk to your cluster.
* Root or sudo privileges.

## 1. Install Falco on Ubuntu

First, add the Falco repository, import its GPG key, update package lists, install kernel headers, and then install Falco:

```bash theme={null}
