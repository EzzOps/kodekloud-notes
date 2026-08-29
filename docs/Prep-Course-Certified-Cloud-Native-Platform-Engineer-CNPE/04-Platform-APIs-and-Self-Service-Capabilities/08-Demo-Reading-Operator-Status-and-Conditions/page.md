# xr-example.yaml
apiVersion: platform.example.com/v1
kind: WebApp
metadata:
  name: my-app
  namespace: default
spec:
  environment: prod
  tier: premium
  replicas: 3
```

```bash theme={null}
kubectl apply -f xr-example.yaml
# wait for composition to reconcile, then:
kubectl get configmap -n function-lab webapp-config -o yaml
```

Expected ConfigMap (partial):

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: webapp-config
  namespace: function-lab
data:
  environment: "prod"
  cpuLimit: "2000m"
```

***

## 4) Transform type: CombineFromComposite (combine fields into one)

`CombineFromComposite` merges multiple XR fields into a single value. For example, concatenate `metadata.name` and `spec.environment` into `data.appId` formatted as `<name>-<environment>`.

Append this patch to `resources[].patches`:

```yaml theme={null}
- type: CombineFromComposite
  combine:
    variables:
      - fromFieldPath: metadata.name
      - fromFieldPath: spec.environment
    strategy: string
    fmt: "%s-%s"
  toFieldPath: spec.forProvider.manifest.data.appId
```

Apply the Composition, then (optionally) recreate the XR to force a new reconciliation:

```bash theme={null}
kubectl apply -f webapp-composition.yaml
kubectl delete -f xr-example.yaml || true
kubectl apply -f xr-example.yaml
kubectl get configmap -n function-lab webapp-config -o yaml
```

Expected ConfigMap (partial):

```yaml theme={null}
data:
  appId: "my-app-prod"
  cpuLimit: "2000m"
  environment: "prod"
```

***

## 5) Transform type: ToCompositeFieldPath (write back to XR status)

`ToCompositeFieldPath` writes a value from the composed resource back into the XR status. This is helpful to expose generated resource names or IDs to platform users.

Append this patch to `resources[].patches` to copy the composed resource's `metadata.name` into `status.configName` of the XR:

```yaml theme={null}
- type: ToCompositeFieldPath
  fromFieldPath: metadata.name
  toFieldPath: status.configName
```

<Callout icon="warning">
  The XRD must declare `status.configName` (or whatever status field you write to). If the XRD does not include the named status property, Crossplane will reject the status write. Reapply the XRD after updating it.
</Callout>

Apply the XRD and Composition, then recreate the XR:

```bash theme={null}
kubectl apply -f webapp-xrd.yaml
kubectl apply -f webapp-composition.yaml
kubectl delete -f xr-example.yaml || true
kubectl apply -f xr-example.yaml
kubectl get webapp my-app -o yaml
```

You should see `status.configName` populated with the composed resource name (for example `my-app-97c0b06087b`).

***

## 6) Transform type: convert (type conversion)

The `convert` transform converts values between types (for example, integer → string). This is required for ConfigMap `data` entries which must be strings.

Append this patch to `resources[].patches`:

```yaml theme={null}
- type: FromCompositeFieldPath
  fromFieldPath: spec.replicas
  toFieldPath: spec.forProvider.manifest.data.replicas
  transforms:
    - type: convert
      convert:
        toType: string
```

Apply the updated Composition and recreate the XR to observe the converted value in the ConfigMap:

```bash theme={null}
kubectl apply -f webapp-composition.yaml
kubectl delete -f xr-example.yaml || true
kubectl apply -f xr-example.yaml
kubectl get configmap -n function-lab webapp-config -o yaml
```

Expected ConfigMap (partial):

```yaml theme={null}
data:
  appId: "my-app-prod"
  cpuLimit: "2000m"
  environment: "prod"
  replicas: "3"    # replicas is now a string
```

***

## 7) Summary & quick reference

The four transforms covered here let you implement flexible, platform-driven mappings and derive provider configuration from high-level inputs.

| Transform type         | Purpose                                                   | Example                                                    |
| ---------------------- | --------------------------------------------------------- | ---------------------------------------------------------- |
| `map`                  | Map a set of input values to specific output values       | `tier` → `cpuLimit` (`free` → `100m`, `premium` → `2000m`) |
| `CombineFromComposite` | Combine multiple XR fields into one formatted value       | `metadata.name + spec.environment` → `appId` (`%s-%s`)     |
| `ToCompositeFieldPath` | Write a composed resource value back into the XR `status` | composed `metadata.name` → `status.configName`             |
| `convert`              | Convert between types (e.g., integer → string)            | `spec.replicas` (int) → `data.replicas` (string)           |

These transforms cover common composition needs: mapping platform-friendly inputs to provider values, aggregating identifiers, surfacing generated names back to users, and converting types for compatibility (e.g., ConfigMap data).

Next steps: experiment with these transforms in your own Composition to implement policy-driven defaults, computed values, and richer platform APIs.

## Links and references

* Crossplane docs: [https://crossplane.io/docs/](https://crossplane.io/docs/)
* Crossplane Functions: [https://doc.crds.example.org/](https://doc.crds.example.org/) (replace with your function docs or internal reference)
* Kubernetes ConfigMap: [https://kubernetes.io/docs/concepts/configuration/configmap/](https://kubernetes.io/docs/concepts/configuration/configmap/)
* Kubernetes API Extensions (CRDs/XRD): [https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/756ffaae-767b-4743-9724-c05d3fbf9a18/lesson/248dcf28-f81b-417f-ab7a-c9fd53237e28" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/756ffaae-767b-4743-9724-c05d3fbf9a18/lesson/5c8eaf8d-b487-45cc-be5d-bb228eea6645" />
</CardGroup>


# Demo Reading Operator Status and Conditions

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Platform-APIs-and-Self-Service-Capabilities/Demo-Reading-Operator-Status-and-Conditions/page

Guide showing how to read operator status and conditions with cert-manager, covering CRDs, Issuer and Certificate creation, status messages, Secrets, and reconciliation for troubleshooting

CRDs (CustomResourceDefinitions) define the API for custom resources, but an operator is the component that acts on those resources. An operator is a controller: it continuously watches custom resources and reconciles the cluster state to match the desired state declared in those resources. For example, you create a `Certificate` resource and the operator provisions the actual TLS certificate; delete the `Certificate` and the operator will clean up or re-create associated objects as needed.

This lesson walks through how to read operator status and conditions using cert-manager as a concrete example. In both exams and production troubleshooting, you often need to infer what an operator is doing without access to its source code. cert-manager exposes several CRDs that map to TLS lifecycle concepts (Certificate, Issuer, CertificateRequest, Order, Challenge, etc.). The operator watches these resources and reconciles them.

## Verify cert-manager CRDs exist

First, confirm that cert-manager's CRDs are installed:

```bash theme={null}
kubectl get crds | grep cert-manager
```

Example output:

```bash theme={null}
certificaterequests.cert-manager.io      2026-04-11T09:47:38Z
certificates.cert-manager.io             2026-04-11T09:47:38Z
challenges.acme.cert-manager.io          2026-04-11T09:47:38Z
clusterissuers.cert-manager.io           2026-04-11T09:47:38Z
issuers.cert-manager.io                  2026-04-11T09:47:38Z
orders.acme.cert-manager.io              2026-04-11T09:47:38Z
```

### Quick reference: cert-manager CRDs and their roles

|               Resource | Use case                                                          | Example              |
| ---------------------: | ----------------------------------------------------------------- | -------------------- |
|            Certificate | Declares the desired certificate (subject, DNS names, secretName) | `Certificate`        |
| Issuer / ClusterIssuer | Defines how certificates are obtained (ACME, selfSigned, CA)      | `Issuer`             |
|     CertificateRequest | Temporary resource used while issuing a certificate               | `CertificateRequest` |
|      Order / Challenge | ACME-specific resources used during domain validation             | `Order`, `Challenge` |

## Create a test Issuer (self-signed)

To issue a certificate you need two things: an Issuer that defines how the certificate will be issued and a Certificate resource that declares what you want. For quick testing, a self-signed Issuer is convenient.

Save this manifest as `/root/selfsigned-issuer.yaml`:

```yaml theme={null}
