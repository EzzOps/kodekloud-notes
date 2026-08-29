# Install via Quickwit install script (downloads a release)
curl -L https://install.quickwit.io | sh
cd ./quickwit-*
./quickwit --version
```

Run the Quickwit container to check version:

```bash theme={null}
# Run the Quickwit container locally
mkdir -p qwdata
docker run --rm quickwit/quickwit --version

# On Apple Silicon or other multi-arch hosts, force linux/amd64
docker run --rm --platform linux/amd64 quickwit/quickwit --version
```

For a guided quickstart and more examples, see Quickwit's official quickstart: [https://quickwit.io/docs/quickstart/](https://quickwit.io/docs/quickstart/)

<Frame>
  <img alt="This image shows the homepage of quickwit.io, highlighting features of a search and analytics engine on cloud storage, with options to try it and book a demo." />
</Frame>

## Installing Quickwit with Glasskube

1. Open the Glasskube UI and go to the Packages tab. Locate the Quickwit package (namespaced) and click it to open the configuration form.

2. Create the namespace if it doesn't exist. For this lesson we create `quickwit-kodekloud`.

Example: list and create the namespace:

```bash theme={null}
# List namespaces
kubectl get ns

# Create the Quickwit namespace
kubectl create namespace quickwit-kodekloud
# namespace/quickwit-kodekloud created
```

3. In Glasskube’s package configuration form:
   * Select the namespace: `quickwit-kodekloud`.
   * Set the deployment name (for example: `quickwit`).
   * Provide `defaultIndexUri` and `metastoreUri` (e.g., `s3://quickwit-indexes`).
   * Enter `s3AccessKeyId` and `s3SecretAccessKey` (use temporary credentials or an IAM-backed mechanism if possible).
   * Set `s3Region` (e.g., `us-east-1`).
   * Leave optional fields blank unless needed (e.g., `s3Endpoint` for MinIO).

<Frame>
  <img alt="This image appears to show a dashboard interface for installing &#x22;quickwit&#x22; with configuration options, such as version selection, namespace, name, and several URI fields. It includes a section for configuring default index and metastore URIs among other settings." />
</Frame>

4. Click Install. Deployment usually completes within 1–2 minutes depending on cluster resources.

Monitor pods in the namespace:

```bash theme={null}
kubectl get pods -n quickwit-kodekloud
# Example output while pods are starting
NAME                                               READY   STATUS      RESTARTS   AGE
quickwit-quickwit-control-plane-5d9dc9b99f-761th   0/1     ContainerCreating   0          10s
quickwit-quickwit-indexer-0                        0/1     ContainerCreating   0          10s
quickwit-quickwit-janitor-56864c9b77-6sfwc         0/1     ContainerCreating   0          10s
quickwit-quickwit-metadata-cd49886bf-z8jrh         0/1     ContainerCreating   0          10s
quickwit-quickwit-searcher-0                       0/1     ContainerCreating   0          10s
```

Wait a short time and re-run the command; pods should move to Running/Ready:

```bash theme={null}
kubectl get pods -n quickwit-kodekloud
# Example output when ready
NAME                                               READY   STATUS    RESTARTS   AGE
quickwit-quickwit-control-plane-5d9dc9b99f-761th   1/1     Running   0          1m
quickwit-quickwit-indexer-0                        1/1     Running   0          1m
quickwit-quickwit-janitor-56864c9b77-6sfwc         1/1     Running   0          1m
quickwit-quickwit-metadata-cd49886bf-z8jrh         1/1     Running   0          1m
quickwit-quickwit-searcher-0                       1/1     Running   0          1m
```

Once pods are running, use Glasskube’s entry point to open the Quickwit web UI.

<Frame>
  <img alt="The image shows a screenshot of the Quickwit UI featuring an &#x22;Indexes panel&#x22; with a list of indexes and a &#x22;Query editor&#x22; section for selecting and querying indexes." />
</Frame>

## Using the Quickwit web UI

From the Quickwit web UI you can:

* Create and manage indexes.
* Run queries using the Query editor.
* Inspect cluster and node status.
* Use the HTTP API for ingestion and queries.

The demo environment typically provides pre-provisioned S3 credentials and example indexes so you can explore the UI without an AWS account.

<Frame>
  <img alt="The image shows a Quickwit UI interface displaying a table with two index entries, each with an ID, URI, creation date, and source count. The sidebar offers navigation options such as Query editor, Indexes, Cluster, Node info, and API." />
</Frame>

## Verification and next steps

* Confirm pods are Running and Ready in the `quickwit-kodekloud` namespace.
* Open the Quickwit web UI via Glasskube to create or query indexes.
* For production use, secure credentials via Kubernetes Secrets, consider an S3 lifecycle policy for index retention, and configure ingress/ingress TLS or a custom domain.

<Frame>
  <img alt="The image shows a Glasskube interface displaying installed and available packages, with quickwit installed and ingress-nginx available for installation." />
</Frame>

## References

* Quickwit Quickstart — [https://quickwit.io/docs/quickstart/](https://quickwit.io/docs/quickstart/)
* Quickwit Documentation — [https://quickwit.io/docs/](https://quickwit.io/docs/)
* Kubernetes Documentation — [https://kubernetes.io/docs/](https://kubernetes.io/docs/)
* Glasskube — check your platform docs or Glasskube UI for package-specific instructions

Wrapping up

You now know the essentials for installing Quickwit as a namespaced package with Glasskube: required configuration values, namespace creation, installation steps, and basic verification. Try the hands-on exercise: follow the steps and install Quickwit in your cluster. Have fun and good luck!

- [Watch Video](https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/c3806869-7f9e-4cc2-8dc5-aa10304e3d1c/lesson/84ca0040-df39-4160-b462-a1e4b6ceb8aa)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/c3806869-7f9e-4cc2-8dc5-aa10304e3d1c/lesson/7d24f4ad-94fb-4099-b2a2-c0a8ee1837f8)


# Demo Create A Helm Based Operator

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Alternative-Approaches-Operator-SDK-Helm-Operator/Demo-Create-A-Helm-Based-Operator/page

Guide demonstrating how to build a Helm-based Kubernetes Operator with Operator SDK, mapping custom resources to Helm charts to manage install, upgrades, and uninstall without writing Go reconciler.

In this lesson we wrap a Helm chart with an Operator using the Operator SDK Helm plugin. The goal is to avoid writing a Go reconciler: the Operator SDK will scaffold a controller that watches a Custom Resource (CR) and uses Helm to install, upgrade, and uninstall chart releases.

<Frame>
  <img alt="The image is a presentation slide featuring the text &#x22;Create A Helm Based Operator&#x22; and &#x22;Demo&#x22; with a minimalistic design. It also includes a copyright credit to KodeKloud." />
</Frame>

## What you get from a Helm-based Operator

A Helm-based operator uses Helm to manage the application lifecycle. Instead of writing reconciliation logic in Go, you map a Kubernetes API (CRD) to a Helm chart. The Operator SDK Helm plugin generates a smaller project surface than the Go plugin: you get a Helm chart, a `watches.yaml` mapping, and Kustomize manifests under `config`. The operator reconciles CRs by rendering the chart with values derived from the CR `spec`.

Key benefits:

* No custom Go reconciler required.
* Leverages Helm charts and existing chart life-cycle semantics (install/upgrade/uninstall).
* CR `spec` fields are passed into the chart as Helm values.

Recommended reading:

* Operator SDK docs: [https://sdk.operatorframework.io](https://sdk.operatorframework.io)
* Helm docs: [https://helm.sh](https://helm.sh)
* Kubernetes CRD overview: [https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)

## Initialize a Helm-based Operator project

Start in a clean directory and initialize an Operator SDK project with the Helm plugin:

```bash theme={null}
operator-sdk init --plugins=helm --domain=example.com
```

Example output:

```text theme={null}
INFO[0000] Writing kustomize manifests for you to edit...
Next: define a resource with:
$ operator-sdk create api
```

## Create the API surface (CRD + chart for the resource)

Create an API for a sample NGINX resource using group `demo`, version `v1`, and kind `Nginx`. This command generates a Helm chart under `helm-charts/nginx` and scaffolds the sample CR manifest:

```bash theme={null}
operator-sdk create api --group=demo --version=v1 --kind=Nginx
```

Example output:

```text theme={null}
INFO[0000] Writing kustomize manifests for you to edit...
Created helm-charts/nginx
Generating RBAC rules
WARN[0000] The RBAC rules generated in config/rbac/role.yaml are based on the chart's default manifest. Some rules may be missing for resources that are only enabled with custom values, and some existing rules may be overly broad. Double check the rules generated in config/rbac/role.yaml to ensure they meet the operator's permission requirements.
```

> **warning** The RBAC rules are derived from the chart's default manifests. Review `config/rbac/role.yaml` and tighten permissions if needed before deploying to production.

## How the mapping works: watches.yaml

The `watches.yaml` file maps the Kubernetes API to the chart:

* If you see a `Nginx` object in the API group `demo.example.com`, reconcile it using the chart in `helm-charts/nginx`.
* The operator reads the CR `spec` and injects those values into Helm rendering.

This mapping is the core of a Helm-based operator: CR → Helm values → rendered Kubernetes resources.

## Chart design and values

Design your Helm chart to expose the values you want users to control via the CR `spec`. Fields under `spec` in the CR are translated into Helm chart values, so chart authors should treat these values as the operator-facing surface.

Example snippets from the generated chart's `values.yaml` (these become the operator surface):

```yaml theme={null}
podLabels: {}

podSecurityContext: {}
  # fsGroup: 2000

securityContext: {}
  # capabilities:
  #   drop:
  #     - ALL
  # readOnlyRootFilesystem: true
  # runAsNonRoot: true
  # runAsUser: 1000
```

> **lightbulb** Design your Helm chart with operator usage in mind: expose the values you expect operators (or users) to modify via the custom resource `spec`.

Common example values that the generated chart exposes:

| Value key          | Purpose                                   | Example                                                           |
| ------------------ | ----------------------------------------- | ----------------------------------------------------------------- |
| `replicaCount`     | Controls Deployment replica count         | `replicaCount: 1`                                                 |
| `image`            | Container image configuration             | `yaml image: repository: nginx pullPolicy: IfNotPresent tag: "" ` |
| `imagePullSecrets` | Image pull secrets for private registries | `imagePullSecrets: []`                                            |

## Install the CRD and run the operator locally

Install the generated CRD so the API server recognizes the `Nginx` resource type:

```bash theme={null}
make install
