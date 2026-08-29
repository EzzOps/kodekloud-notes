# 1. Initialize Vault (if not done yet)
vault operator init

# 2. Enable Kubernetes auth backend
vault write auth/kubernetes/config \
  token_reviewer_jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
  kubernetes_host="https://$KUBE_API_HOST:443" \
  kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt

# 3. Create a role for 'app' service account in 'demo' namespace
vault write auth/kubernetes/role/phapp \
  bound_service_account_names=app \
  bound_service_account_namespaces=demo \
  policies=app \
  ttl=1h

# 4. Define and write the 'app' policy
cat <<EOF > app-policy.hcl
path "crds/data/my/*" {
  capabilities = ["read"]
}
EOF
vault policy write app app-policy.hcl
```

> **triangle-alert** Ensure your policy paths match the KV engine mount and data structure in Vault. Incorrect paths will result in denied access.

## Fetching and Rendering Secrets

1. **Init Container** retrieves secrets:
   ```bash theme={null}
   vault kv get -field=value crds/data/my/config
   ```
2. Writes them into a shared volume (e.g., mounted at `/vault`).
3. **Application Container** reads secrets as files:
   ```bash theme={null}
   kubectl exec -it my-app -- ls /vault
   ```

This design allows your application to consume Vault-managed secrets like local files—no Vault client library needed in your code.

***

## Links and References

* [HashiCorp Vault Official Documentation](https://www.vaultproject.io/docs)
* [Kubernetes Authentication Overview](https://kubernetes.io/docs/reference/access-authn-authz/authentication/)
* [Helm Charts for Vault](https://artifacthub.io/packages/helm/hashicorp/vault)

- [Watch Video](https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/baf5859d-32c2-4e7c-9808-f3486d6b9827/lesson/f798a147-de48-4512-a94e-ed94e13f4016)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/baf5859d-32c2-4e7c-9808-f3486d6b9827/lesson/05fec374-366a-4571-886b-b4751c57ab2a)


# CIS Benchmarking and Kube bench

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/Kubernetes-Operations-and-Security/CIS-Benchmarking-and-Kube-bench/page

This guide covers CIS Benchmarking for Kubernetes and demonstrates using Kube-bench to validate cluster security posture.

In this guide, we’ll dive into **CIS Benchmarking** for Kubernetes and demonstrate how to use **Kube-bench** to validate your cluster’s security posture. You’ll learn:

* What the CIS Kubernetes Benchmark covers
* How to run Kube-bench via **Docker** or as a **standalone binary**
* Techniques for filtering checks and producing JSON output for CI/CD

## What Is the CIS Benchmark?

The Center for Internet Security (CIS) publishes **CIS Benchmarks**, which are consensus-driven best practices for securing various platforms. The [CIS Kubernetes Benchmark][cis-k8s] offers detailed recommendations for locking down a Kubernetes cluster by release version.

For fully managed offerings like GKE or EKS, use the cloud provider–specific benchmarks:

| Managed Service | Benchmark Link               |
| --------------- | ---------------------------- |
| GKE             | [CIS GKE Benchmark][cis-gke] |
| EKS             | [CIS EKS Benchmark][cis-eks] |

These child benchmarks inherit controls from the upstream CIS Kubernetes Benchmark, removing checks you can’t configure and adding provider-specific rules.

In this article, we focus on a **kubeadm**-provisioned cluster using the upstream [CIS Kubernetes Benchmark][cis-k8s].

## Introducing Kube-bench

[Kube-bench][kube-bench] is an open-source tool written in Go that scans your Kubernetes nodes against the CIS Benchmark controls. It will output `PASS` or `FAIL` for each test, so you can quickly identify misconfigurations.

You can execute Kube-bench in two primary ways:

1. **Docker container**
2. **Standalone binary**

> **lightbulb** Always match the `--version` flag to your Kubernetes release. Mismatched versions may yield incorrect results.

***

## 1. Running Kube-bench with Docker

Using Docker is the quickest method since it requires no local installation. Mount your host’s `/etc` and `/var` directories so Kube-bench inside the container can read necessary config files.

```bash theme={null}
docker run --rm \
  --pid host \
  -v /etc:/etc:ro \
  -v /var:/var:ro \
  -t aquasec/kube-bench:latest master --version 1.19
```

| Option            | Description                                                                                                 |
| ----------------- | ----------------------------------------------------------------------------------------------------------- |
| `--pid host`      | Grants the container access to host process information.                                                    |
| `-v /etc:/etc:ro` | Mounts host `/etc` in read-only mode (for kubelet and control plane configs).                               |
| `-v /var:/var:ro` | Mounts host `/var` in read-only mode (for runtime data).                                                    |
| `master`          | Runs checks for the master node. You can also specify `node`, `etcd`, `scheduler`, or `controller-manager`. |
| `--version 1.19`  | Targets the CIS Benchmark for Kubernetes v1.19.                                                             |

> **triangle-alert** Ensure your Docker user has permission to mount `/etc` and `/var`. Running as root or with `sudo` may be required.

### Sample Output

```plaintext theme={null}
1 Master Node Security Configuration
[INFO] 1.1 API Server
[FAIL] 1.1.1 Ensure that the --allow-privileged argument is set to false (Scored)
[FAIL] 1.1.2 Ensure that the --anonymous-auth argument is set to false (Scored)
[PASS] 1.1.4 Ensure that the --insecure-allow-any-token argument is not set (Scored)
…
[FAIL] 1.1.21 Ensure that the --kubelet-certificate-authority argument is set as appropriate (Scored)
```

***

## 2. Installing and Running the Standalone Binary

If you prefer not to use Docker, download the latest Kube-bench release, extract it, and place the binary in your `PATH`:

```bash theme={null}
