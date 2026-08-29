# Log in (one-time per host/session)
$ docker login ghcr.io \
  --username sidd-harth \
  --password <<GITHUB_PERSONAL_ACCESS_TOKEN>>
Login Succeeded

# Confirm the local image (example: nginx)
$ docker images nginx
REPOSITORY   TAG       IMAGE ID    CREATED        SIZE
nginx        latest    8873639     8 days ago     142MB

# Tag the local image with your registry path and version
$ docker tag nginx ghcr.io/sidd-harth/nginx:1.1.0

# Push the image to the OCI registry
$ docker push ghcr.io/sidd-harth/nginx:1.1.0
6cffb086835: Pushed
2d75b87993c: Pushed
ec43a899918: Pushed
sha256:a4a4a4d...: digest: sha256:a4a4a4d... size: 1570
```

Once pushed, Kubernetes workloads (or other consumers) can pull the image using the `ghcr.io/sidd-harth/nginx:1.1.0` reference provided they have access.

## Pushing Helm charts to an OCI registry

Modern Helm supports saving and pushing charts as OCI artifacts. Typical flow:

1. Create or have a chart (e.g., `helm create app1`).
2. Package the chart as a `.tgz`.
3. Login to the registry with Helm.
4. Save/push the chart as an OCI artifact.

Example (replace `<<GITHUB_PERSONAL_ACCESS_TOKEN>>` with your token):

```bash theme={null}
# Create a chart scaffold
$ helm create app1
Creating app1

# Package the chart to a tgz
$ helm package app1
Successfully packaged chart and saved it to: ./app1-1.0.0.tgz

# Login to the registry using Helm
$ helm registry login ghcr.io \
  --username sidd-harth \
  --password <<GITHUB_PERSONAL_ACCESS_TOKEN>>
Login Succeeded

# Save and push the chart as an OCI artifact (Helm >=3.7+)
$ helm chart save ./app1-1.0.0.tgz ghcr.io/sidd-harth/app1:1.0.0
$ helm chart push ghcr.io/sidd-harth/app1:1.0.0
Pushed: ghcr.io/sidd-harth/app1:1.0.0
Digest: sha256:81de917eaf38356b1145bdde2984dc2fdf14...
```

After pushing, consumers can pull the chart directly from the OCI registry using Helm's OCI registry support.

## Publishing plain Kubernetes manifests to an OCI registry (using Flux)

You can package a directory of Kubernetes manifests and push it as an OCI artifact. Flux provides `flux push artifact` to create a manifest bundle and push it to an OCI registry; a GitOps operator can then reference that bundle.

Example using Flux (replace `<<GITHUB_PERSONAL_ACCESS_TOKEN>>` with your token):

```bash theme={null}
# Ensure Docker login (if your registry requires it)
$ docker login ghcr.io \
  --username sidd-harth \
  --password <<GITHUB_PERSONAL_ACCESS_TOKEN>>
Login Succeeded

# Example manifests tree
$ tree nginx/
nginx/
└── manifests
    ├── deployment.yaml
    └── service.yaml

# Push manifests as an OCI artifact with Flux
$ flux push artifact oci://ghcr.io/sidd-harth/nginx-2:$(git rev-parse --short HEAD) \
  --path="./nginx/manifests/" \
  --source="$(git config --get remote.origin.url)" \
  --revision="$(git branch --show-current)/$(git rev-parse HEAD)"
pushing to ghcr.io/sidd-harth/nginx-2:1b31558
artifact successfully pushed to ghcr.io/sidd-harth/nginx-2@sha256:235b486df4a38f0151...
```

Once the manifest bundle is published, configure your GitOps operator (e.g., Flux or Argo CD) to reference the OCI artifact location and reconciliation will apply those manifests to your cluster.

## How GitOps operators consume OCI artifacts

* Argo CD and Flux both support pulling from OCI registries:
  * Argo CD: supports OCI images and some extensions for OCI-based applications.
  * Flux: has first-class support for `Kustomization`/`HelmRepository` using `oci://` sources and `flux push artifact`.
* Typical operator flow: fetch OCI artifact → verify digest/revision → render/apply manifests or charts → report status.

## Registry examples and links

| Provider                                                                                                                                               | Notes                                               |
| ------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------- |
| [GitHub Container Registry (ghcr.io)](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) | Supports OCI artifacts and fine-grained permissions |
| [Docker Hub](https://hub.docker.com/)                                                                                                                  | Popular image registry with OCI support             |
| [Azure Container Registry](https://learn.microsoft.com/en-us/azure/container-registry/)                                                                | Enterprise-grade registry with RBAC and ACR Tasks   |
| [Google Artifact Registry](https://cloud.google.com/artifact-registry)                                                                                 | Supports multiple artifact formats including OCI    |

## Best practices

* Consolidate related artifacts under predictable repository paths (e.g., `ghcr.io/<org>/<app>`).
* Use image and artifact digests (sha256) in production manifests to guarantee immutability.
* Use short-lived credentials or OIDC where possible; avoid embedding PATs in long-lived scripts.
* Apply RBAC and least privilege on the registry to limit artifact access.

## References

* [Open Container Initiative (OCI)](https://opencontainers.org/)
* [Helm documentation](https://helm.sh/)
* [FluxCD documentation](https://fluxcd.io/)
* [Argo CD documentation](https://argo-cd.readthedocs.io/en/stable/)

That's all for this lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/24630e6a-9f49-42d1-abd0-75bafc02ce01/lesson/f1ba2352-52cb-4d07-868d-026818023a60)


# Customize Istio Installation

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Installation-Configuration/Customize-Istio-Installation/page

How to customize Istio installations using IstioOperator manifests, overlays, resource overrides, Helm, and istioctl to enable or disable components, manage revisions, upgrade, and uninstall

You can customize Istio installations instead of relying on the default profile. Istio profiles (for example: `demo`, `default`, `ambient`, etc.) control which core components are enabled and which features are included by default.

<Frame>
  <img alt="The image depicts a table of Istio profiles and their core components, showing different profiles like default, demo, and others with checkmarks indicating their inclusion of specific components like &#x22;istio-egressgateway&#x22; and &#x22;ztunnel.&#x22;" />
</Frame>

> **lightbulb** The `istioctl profile dump` command that produced a ready-to-edit IstioOperator manifest was removed. You now author an IstioOperator manifest yourself to customize an installation. If you need to find an option in the operator schema, consult the Istio Operator reference: [https://istio.io/latest/docs/reference/config/installation-options/](https://istio.io/latest/docs/reference/config/installation-options/)

Below are practical examples and a recommended workflow for customizing Istio with an IstioOperator manifest, patch overlays, resource overrides, and Helm alternatives.

## Basic IstioOperator skeleton

Create an `IstioOperator` YAML to override defaults. This skeleton shows how to set image hub/tag and toggle core components and gateways:

```yaml theme={null}
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  hub: docker.io/istio
  tag: 1.18.2
  components:
    base:
      enabled: true
    cni:
      enabled: false
    egressGateways:
      - enabled: false
        name: istio-egressgateway
    ingressGateways:
      - enabled: true
        name: istio-ingressgateway
    istiodRemote:
      enabled: false
    pilot:
      enabled: true
```

Quick one-off setting using `istioctl`:

```bash theme={null}
istioctl install --set values.pilot.traceSampling=0.1
```

## Disable istiod (Pilot) via IstioOperator

To disable the control plane component (historically called Pilot; functionality resides in `istiod`), set the component to disabled:

```yaml theme={null}
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  components:
    pilot:
      enabled: false
```

Apply with:

```bash theme={null}
istioctl install -f disable-pilot.yaml
```

## Override Kubernetes resources (CPU, memory, HPA)

Override resource requests/limits and HPA settings for control-plane deployments (example shows `pilot`/`istiod`):

```yaml theme={null}
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  components:
    pilot:
      k8s:
        resources:
          requests:
            cpu: 1000m     # override from default 500m
            memory: 4096Mi # override from default 2048Mi
        hpaSpec:
          minReplicas: 2
          maxReplicas: 10
```

Apply the configuration:

```bash theme={null}
istioctl install -f samples/operator/pilot-k8s.yaml
```

## Patching generated manifests with overlays

Use `k8s.overlays` in the IstioOperator to patch generated Kubernetes resources. Overlays are useful for small targeted edits (changing args, ports, annotations, etc.):

```yaml theme={null}
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  profile: empty
  hub: docker.io/istio
  tag: 1.1.6
  components:
    pilot:
      enabled: true
      namespace: istio-control
  k8s:
    overlays:
      - kind: Deployment
        name: istiod
        patches:
          # Example: change an arg from "30m" to "60m"
          - path: spec.template.spec.containers[name:discovery].args.[30m]
            value: "60m"
          # Example: change a containerPort value
          - path: spec.template.spec.containers[name:discovery].ports.[containerPort:8080].containerPort
            value: 9080
```

Generate the patched manifest to inspect changes:

```bash theme={null}
istioctl manifest generate -f patch.yaml
```

A truncated example of the resulting Deployment shows patched values:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: istiod
spec:
  template:
    spec:
      containers:
      - name: discovery
        args:
        - --some-arg=60m        # patched from 30m
        ports:
        - containerPort: 9080   # patched from 8080
```

## Revisions and meshConfig

You can set the `revision` field in the IstioOperator to manage control-plane revisions during upgrades and to enable side-by-side control plane installations:

```yaml theme={null}
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  profile: default
  hub: gcr.io/istio-testing
  tag: latest
  revision: 1-8-0
  meshConfig:
    accessLogFile: /dev/stdout
    enableTracing: true
  components:
    egressGateways:
      - name: istio-egressgateway
        enabled: true
```

<Frame>
  <img alt="The image is a screenshot from the Istio documentation, describing how to identify an Istio component using the IstioOperator API. It includes a table of component names and instructions for configuring settings." />
</Frame>

## Common exam-style changes (quick checklist)

Be familiar with the following modifications and how to express them in an `IstioOperator` or via `istioctl`:

* Enable/disable a specific component (egress/ingress gateway)
* Rename a gateway (change `name:`)
* Install a gateway into a non-default namespace (`namespace:` under the gateway entry)
* Change CPU/memory requests and limits for control-plane components
* Set `hub`, `tag`, and `revision` for image sources and version control

Quick example — enable the egress gateway and change its name and namespace:

```yaml theme={null}
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  components:
    base:
      enabled: true
    cni:
      enabled: false
    egressGateways:
      - enabled: true
        name: istio-egress
        namespace: istio-egress-ns
    ingressGateways:
      - enabled: true
        name: istio-ingressgateway
    istiodRemote:
      enabled: false
    pilot:
      enabled: true
```

Apply or upgrade with:

```bash theme={null}
istioctl upgrade -f default.yaml
```

## Quick reference table

| Action                          | Example command or field                                |
| ------------------------------- | ------------------------------------------------------- |
| Install from IstioOperator file | `istioctl install -f <file>`                            |
| One-off set value with istioctl | `istioctl install --set values.pilot.traceSampling=0.1` |
| Generate patched manifest       | `istioctl manifest generate -f patch.yaml`              |
| Upgrade using IstioOperator     | `istioctl upgrade -f <file>`                            |
| Uninstall (purge CRDs/data)     | `istioctl uninstall --purge`                            |
| Helm show default values        | `helm show values istio/istiod > istiod.yaml`           |

## Helm-based customization

If you prefer Helm, inspect default values, edit a values file, and then install or upgrade the chart:

```bash theme={null}
helm show values istio/base > istio_base.yaml
helm install istio-base istio/base -n istio-system -f istio_base.yaml

helm show values istio/istiod > istiod.yaml
helm install istiod istio/istiod -n istio-system -f istiod.yaml

helm show values istio/gateway > istio_gateway.yaml
```

After editing values files, apply changes with `helm upgrade`.

> **warning** Be careful when running `istioctl uninstall --purge`. This removes Istio resources and CRDs and can destroy stored configuration and telemetry. Always back up important configuration before purging.

## Upgrade and uninstall

* To update an existing installation, edit your `IstioOperator` and run:

```bash theme={null}
istioctl upgrade -f <file>
```

* To uninstall:

```bash theme={null}
