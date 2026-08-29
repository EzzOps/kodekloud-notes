# Demo Deploy Cert Manager In 60 Seconds

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Introduction-to-Operator-Fundamentals/Demo-Deploy-Cert-Manager-In-60-Seconds/page

Walkthrough to install cert-manager on Kubernetes, apply its manifest, inspect CRDs and API kinds, create a ClusterIssuer, and verify controller reconciliation.

In this short walkthrough you'll install a production-grade Kubernetes operator (cert-manager), inspect the new API kinds it provides, and create a simple ClusterIssuer to prove the controller is reconciling custom resources. The sequence below demonstrates the standard operator installation pattern you'll use repeatedly:

1. Confirm the cluster is clean.
2. Apply the operator release manifest (CRDs + controllers).
3. Wait for controller deployments to become available.
4. Inspect new API resources.
5. Create a custom resource and verify reconciliation.

Step one — confirm the cluster is empty

Before installing cert-manager, verify there is no `cert-manager` namespace and no cert-manager CRDs present on the cluster:

```bash theme={null}
kubectl get ns cert-manager; kubectl get crds | grep cert-manager | wc -l
```

Expected output on a clean cluster:

```text theme={null}
Error from server (NotFound): namespaces "cert-manager" not found
No resources found
0
```

Step two — apply the cert-manager release manifest

A single `kubectl apply` against the official v1.19.1 release manifest installs the namespace, CRDs, controller deployment, webhook, CA injector, RBAC, and other cluster-scoped resources:

```bash theme={null}
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.19.1/cert-manager.yaml
```

Wait for the three core cert-manager deployments to become available:

```bash theme={null}
kubectl wait --for=condition=Available deployment --all -n cert-manager --timeout=120s
```

Example rollout output:

```text theme={null}
deployment.apps/cert-manager condition met
deployment.apps/cert-manager-cainjector condition met
deployment.apps/cert-manager-webhook condition met
```

What the release manifest installs

| Resource type  | Purpose                                                                          |
| -------------- | -------------------------------------------------------------------------------- |
| Namespace      | `cert-manager` isolates operator resources                                       |
| CRDs           | CustomResourceDefinitions that add cert-manager API kinds                        |
| Deployments    | Controller(s): `cert-manager`, `cert-manager-cainjector`, `cert-manager-webhook` |
| RBAC & Webhook | Permissions and webhook configuration for secure operation                       |

Inspect the API resources added by the operator

List the API resources for the `cert-manager.io` API group to see the new Kubernetes kinds:

```bash theme={null}
kubectl api-resources --api-group=cert-manager.io
```

Example output (key cert-manager kinds):

| NAME                | SHORTNAMES   | APIVERSION         | NAMESPACED | KIND               |
| ------------------- | ------------ | ------------------ | ---------- | ------------------ |
| certificaterequests | `cr,crs`     | cert-manager.io/v1 | true       | CertificateRequest |
| certificates        | `cert,certs` | cert-manager.io/v1 | true       | Certificate        |
| clusterissuers      | `ciss`       | cert-manager.io/v1 | false      | ClusterIssuer      |
| issuers             | `iss`        | cert-manager.io/v1 | true       | Issuer             |

Prove it works — create a self-signed ClusterIssuer

Apply a minimal ClusterIssuer manifest. The cert-manager controller will reconcile this custom resource into a Ready state:

```bash theme={null}
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: selfsigned
spec:
  selfSigned: {}
EOF
```

kubectl will report the created resource:

```text theme={null}
clusterissuer.cert-manager.io/selfsigned created
```

Wait for the ClusterIssuer to report Ready:

```bash theme={null}
kubectl wait --for=condition=Ready clusterissuer/selfsigned --timeout=10s
```

Example wait output:

```text theme={null}
clusterissuer.cert-manager.io/selfsigned condition met
```

Verify the ClusterIssuer status:

```bash theme={null}
kubectl get clusterissuer selfsigned
```

Example output:

```text theme={null}
NAME        READY   AGE
selfsigned  True    10s
```

<Callout icon="lightbulb">
  This demonstrates the operator pattern in \~60 seconds: apply an operator manifest (CRDs + controllers), observe new API kinds, create a custom resource, and let the controller reconcile it to the desired state.
</Callout>

Summary checklist

| Task                        | Command / Check                                                                                                        |                   |         |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ----------------- | ------- |
| Confirm cluster clean       | \`kubectl get ns cert-manager; kubectl get crds                                                                        | grep cert-manager | wc -l\` |
| Install cert-manager        | `kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.19.1/cert-manager.yaml`            |                   |         |
| Wait for deployments        | `kubectl wait --for=condition=Available deployment --all -n cert-manager --timeout=120s`                               |                   |         |
| List cert-manager API kinds | `kubectl api-resources --api-group=cert-manager.io`                                                                    |                   |         |
| Create ClusterIssuer        | apply the `ClusterIssuer` manifest shown above                                                                         |                   |         |
| Verify readiness            | `kubectl wait --for=condition=Ready clusterissuer/selfsigned --timeout=10s` and `kubectl get clusterissuer selfsigned` |                   |         |

Links and references

* cert-manager releases: [https://github.com/cert-manager/cert-manager/releases](https://github.com/cert-manager/cert-manager/releases)
* cert-manager docs: [https://cert-manager.io/docs/](https://cert-manager.io/docs/)
* Kubernetes docs — CustomResourceDefinitions: [https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/7d198de7-d651-4c7e-a61d-166023fc1031/lesson/e05a5c27-dcf1-4107-8ad7-9f2c4602e011" />
</CardGroup>
