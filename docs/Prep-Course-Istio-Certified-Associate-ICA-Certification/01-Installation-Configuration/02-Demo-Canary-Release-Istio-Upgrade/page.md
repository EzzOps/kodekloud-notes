# Istio operator uninstall (purge data and CRDs)
istioctl uninstall --purge

# Helm uninstall (example namespace)
helm uninstall istio-ingress -n istio-ingress
```

***

The Istio operator provides flexible control over which components and settings are installed. Practice by making small, incremental changes (resource overrides, enabling gateways, or applying overlays) in a local cluster to become comfortable with the workflow and exam-style scenarios.

## Useful links and references

* Istio Installation Options (Operator schema): [https://istio.io/latest/docs/reference/config/installation-options/](https://istio.io/latest/docs/reference/config/installation-options/)
* Istioctl documentation: [https://istio.io/latest/docs/ops/diagnostic-tools/istioctl/](https://istio.io/latest/docs/ops/diagnostic-tools/istioctl/)
* Helm charts for Istio: [https://github.com/istio/istio/tree/master/manifests/charts](https://github.com/istio/istio/tree/master/manifests/charts)

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/65ee174b-536e-4657-9b6f-85c90c7612da/lesson/3f6daee7-6e1d-485b-b175-97c15083d129)


# Demo Canary Release Istio Upgrade

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Installation-Configuration/Demo-Canary-Release-Istio-Upgrade/page

Guide to performing a revisioned canary upgrade of Istio control plane, running old and new revisions side-by-side, migrating workloads, and uninstalling the old revision safely

In this lesson we will walk through a canary upgrade of Istio control plane from 1.26.2 to 1.26.3 and how to migrate workloads safely to the new revision. The process uses Istio revisioned installs so you can run the old and new control planes side-by-side, move workloads to the new revision, and then uninstall the old one.

Prerequisites used in this article:

* A Kubernetes cluster with Istio installed (profile: demo).
* Bookinfo sample application for testing.

1. Check the current Istio and workload state

First, verify the Istio system components and the Bookinfo workloads.

```bash theme={null}
kubectl get pods -n istio-system
```

Example output:

```text theme={null}
NAME                                   READY   STATUS    RESTARTS   AGE
istio-egressgateway-5478b96959-h7gzm   1/1     Running   0          5m10s
istio-ingressgateway-7dddb56f89-wjsp4  1/1     Running   0          5m10s
istiod-57dcc6d8b-wkf2n                 1/1     Running   0          5m20s
```

Check the running Bookinfo workloads:

```bash theme={null}
kubectl get pods
```

Example output:

```text theme={null}
NAME                                    READY   STATUS    RESTARTS   AGE
details-v1-65599dcf88-rqwm8             2/2     Running   0          4m14s
productpage-v1-9487c9c5b-mw6rv          2/2     Running   0          4m13s
ratings-v1-5b999c644-7674h              2/2     Running   0          4m14s
reviews-v1-5985998544-s5tvt             2/2     Running   0          4m13s
reviews-v2-866dcc668-pz289              2/2     Running   0          4m13s
reviews-v3-dbb5fb5d-c52wl               2/2     Running   0          4m13s
```

Confirm the client, control plane, and data plane versions:

```bash theme={null}
istioctl version
```

Example output:

```text theme={null}
client version: 1.26.2
control plane version: 1.26.2
data plane version: 1.26.2 (8 proxies)
```

To inspect what proxy version a pod's sidecar is running, you can describe the pod and look at the istio-proxy image:

```bash theme={null}
kubectl describe pod <pod-name>
```

Example snippet from `kubectl describe pod ratings-...`:

```text theme={null}
istio-proxy:
  Image: docker.io/istio/proxyv2:1.26.2
  ...
```

Or use `istioctl proxy-status` to get a concise mapping of proxies to control plane revisions:

```bash theme={null}
istioctl proxy-status
```

2. Download the new istioctl (1.26.3)

Download the new Istio release and add it to your PATH. Replace the ISTIO\_VERSION if you want a different version.

```bash theme={null}
curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.26.3 sh -
export PATH="$PATH:$(pwd)/istio-1.26.3/bin"
```

After exporting PATH, verify the client version has updated while your control and data planes remain on the old version:

```bash theme={null}
istioctl version
```

Example output:

```text theme={null}
client version: 1.26.3
control plane version: 1.26.2
data plane version: 1.26.2 (8 proxies)
```

3. Install the new Istio control plane as a revision

Install Istio 1.26.3 as a new revision (revision name chosen here is `1-26-3`). We keep the demo profile for this example.

```bash theme={null}
istioctl install --set profile=demo --revision=1-26-3
```

Confirm the new control plane pods appear alongside the old ones:

```bash theme={null}
kubectl get pods -n istio-system
```

Example output:

```text theme={null}
NAME                                         READY   STATUS    RESTARTS   AGE
istio-egressgateway-7bd9c1c56c-82vs2         1/1     Running   0          33s
istio-ingressgateway-7c7f65d5d9-tgjqq        1/1     Running   0          33s
istiod-1-26-3-774f5b659-xgx82                 1/1     Running   0          44s
istiod-57dcc6d8b-wkf2m                        1/1     Running   0          8m44s
```

4. Create a revision tag and label namespaces for injection

Create a human-friendly tag (e.g., `latest`) that points to the new control plane revision:

```bash theme={null}
istioctl tag set latest --revision 1-26-3
```

This command outputs guidance: to enable injection using this revision tag, label the namespace:

```text theme={null}
Revision tag "latest" created, referencing control plane revision "1-26-3".
To enable injection using this revision tag, use:
  kubectl label namespace <NAMESPACE> istio.io/rev=latest
```

Label the namespace where your app lives (for this demo the `default` namespace):

```bash theme={null}
kubectl label namespace default istio.io/rev=latest --overwrite
```

Verify the namespace label:

```bash theme={null}
kubectl get ns default --show-labels
```

Example output:

```text theme={null}
NAME      STATUS   AGE   LABELS
default   Active   21m   istio.io/rev=latest,kubernetes.io/metadata.name=default
```

Note: Using `istio.io/rev=<tag>` enables automatic sidecar injection for that namespace to target the specified control plane revision.

5. Migrate workloads to the new revision

There are two common ways to move workloads to the new revision:

* Redeploy the workloads (delete and reapply or use `kubectl rollout restart`) so the injected sidecar uses the new revision tag.
* Alternatively, if pods were created with manual injection, update them accordingly.

Example: redeploy Bookinfo workloads by deleting and reapplying the sample:

```bash theme={null}
kubectl delete -f https://raw.githubusercontent.com/istio/istio/release-1.11/samples/bookinfo/platform/kube/bookinfo.yaml
kubectl apply  -f https://raw.githubusercontent.com/istio/istio/release-1.11/samples/bookinfo/platform/kube/bookinfo.yaml
```

Check pod status while pods initialize:

```bash theme={null}
kubectl get pods
```

Once pods are running, describe a pod to confirm the istio-proxy image version:

```bash theme={null}
kubectl describe pod details-v1-<id>
```

Example excerpt showing the proxy is now 1.26.3:

```text theme={null}
istio-proxy:
  Image: docker.io/istio/proxyv2:1.26.3
  ...
```

Also check `istioctl proxy-status` to ensure the proxies are attached to the new istiod revision:

```bash theme={null}
istioctl proxy-status
```

Example output (all proxies pointing to istiod 1.26.3):

```text theme={null}
NAME                                  ISTIOD                                   VERSION
details-v1-...                         istiod-1-26-3-774fb5c659-xgx82           1.26.3
productpage-v1-...                     istiod-1-26-3-774fb5c659-xgx82           1.26.3
...
```

You can also use `kubectl rollout restart deployment/<deployment-name>` to trigger a restart and pick up the new revision tag.

> **lightbulb** Before uninstalling the old control plane, ensure every workload has been migrated to the new revision. Uninstalling the old revision while proxies still point to it will detach those proxies and break traffic.

6. Uninstall the old revision

Once you're confident all workloads and gateways are using the new revision, uninstall the old control plane revision (for example the default revision). First confirm which pods are still associated with the `default` revision (labels and `istioctl proxy-status` help with this).

Uninstall the old revision:

```bash theme={null}
istioctl uninstall --revision default
```

If there are still proxies pointing to the revision, `istioctl` will warn you and list those proxies. Confirm only after you have migrated everything.

Example uninstall output:

```text theme={null}
There are still 8 proxies pointing to the control plane revision default
details-v1-...default
productpage-v1-...default
...
If you proceed with the uninstall, these proxies will become detached from any control plane and will not function correctly.
Proceed? (y/n) y

Removed apps/v1, Kind-Deployment/istio-istio-system
Removed v1, Kind-Service/istio-istio-system
...
✔ Uninstall complete
```

7. Final verification

Check that only the new revision remains in the istio-system namespace and that all application pods are using the new proxy:

```bash theme={null}
kubectl get pods -n istio-system --show-labels
kubectl get pods
istioctl proxy-status
```

Example istio-system output after cleanup:

```text theme={null}
NAME                                  READY   STATUS    RESTARTS   AGE
istio-egressgateway-...               1/1     Running   0          7m27s
istio-ingressgateway-...              1/1     Running   0          7m27s
istiod-1-26-3-774fb5c659-xg82         1/1     Running   0          7m38s
```

And your workloads should show 2/2 with the updated sidecar proxy version (1.26.3).

Summary

* Download and use a new istioctl client for the target control plane version.
* Install the new control plane as a revision with `--revision=...`.
* Create a tag (e.g., `latest`) pointing to the new revision with `istioctl tag set`.
* Label namespaces with `istio.io/rev=<tag>` to route injection to the new revision.
* Redeploy or restart workloads to pick up the new sidecar (or reapply manifests).
* After confirming all proxies are attached to the new control plane, uninstall the old revision.

This revision-based canary install flow lets you upgrade Istio with minimal disruption and a straightforward rollback path if needed.

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/65ee174b-536e-4657-9b6f-85c90c7612da/lesson/c2888591-eda8-4a20-9b25-793310c0ccc8)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/65ee174b-536e-4657-9b6f-85c90c7612da/lesson/928905b6-7868-4098-96a2-a602291ffdc6)
