# Demo Crossplane Functions

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Platform-APIs-and-Self-Service-Capabilities/Demo-Crossplane-Functions/page

Demo showing how to use Crossplane Patch-and-Transform functions to map composite resource fields into provider configuration using Composition transforms like map, combine, convert, and status writeback

This demo shows how to use Crossplane's Patch-and-Transform function to translate high-level platform inputs (for example, `tier: large`) into concrete provider values (for example, `db.r5.large`). We'll walk through each of the four transform types supported by the Patch-and-Transform function and add them to a Composition so you can observe their effects.

We use a simple WebApp composite resource with the following spec fields:

* `tier` (free | standard | premium)
* `environment` (string)
* `replicas` (integer)

The platform (Composition) decides the actual resource configuration that will be created from those inputs — in this example the Composition constructs a Kubernetes ConfigMap.

> **lightbulb** When you modify an existing Composition, append new patches/transforms to the existing `patches` array — do not replace the existing entries. Appending preserves prior behavior while adding new transformations.

***

## 1) CompositeResourceDefinition (XRD)

Create an XRD for the WebApp composite resource. Note the `spec` fields and the `status.configName` property — the latter is required if you intend to write back values into the XR status using `ToCompositeFieldPath`.

```yaml theme={null}
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: webapps.platform.example.com
spec:
  group: platform.example.com
  names:
    kind: WebApp
    plural: webapps
  scope: Namespaced
  versions:
    - name: v1
      served: true
      referenceable: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                tier:
                  type: string
                  enum: ["free", "standard", "premium"]
                environment:
                  type: string
                replicas:
                  type: integer
              required: ["tier", "environment", "replicas"]
            status:
              type: object
              properties:
                configName:
                  type: string
          x-kubernetes-preserve-unknown-fields: true
```

Apply and verify the XRD:

```bash theme={null}
kubectl apply -f webapp-xrd.yaml
kubectl get compositeresourcedefinition webapps.platform.example.com -o yaml
```

***

## 2) Base Composition (ConfigMap resource)

This base Composition creates a ConfigMap named `webapp-config` in the `function-lab` namespace. It uses the Patch-and-Transform function (`pt.fn.crossplane.io/v1beta1`, function name `function-patch-and-transform`) with `Resources` input. Start by mapping `spec.environment` from the XR into the ConfigMap `data.environment`.

```yaml theme={null}
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: webapp-kubernetes
spec:
  compositeTypeRef:
    apiVersion: platform.example.com/v1
    kind: WebApp
  mode: Pipeline
  pipeline:
    steps:
      - name: patch-and-transform
        functionRef:
          name: function-patch-and-transform
          apiVersion: pt.fn.crossplane.io/v1beta1
        input:
          apiVersion: pt.fn.crossplane.io/v1beta1
          kind: Resources
          resources:
            - name: webapp-config
              base:
                apiVersion: kubernetes.m.crossplane.io/v1alpha1
                kind: Object
                metadata:
                  name: webapp-config
                  namespace: function-lab
                spec:
                  providerConfigRef:
                    name: ClusterProviderConfig
                  forProvider:
                    manifest:
                      apiVersion: v1
                      kind: ConfigMap
                      metadata:
                        name: webapp-config
                        namespace: function-lab
                      data: {}
              patches:
                - type: FromCompositeFieldPath
                  fromFieldPath: spec.environment
                  toFieldPath: spec.forProvider.manifest.data.environment
```

Apply the Composition:

```bash theme={null}
kubectl apply -f webapp-composition.yaml
kubectl get composition webapp-kubernetes -o yaml
```

***

## 3) Transform type: map (value mapping)

Use the `map` transform to translate user-friendly values into concrete provider values. For example, map `spec.tier` to `data.cpuLimit` in the ConfigMap.

Append this patch to `resources[].patches` in your Composition:

```yaml theme={null}
- type: FromCompositeFieldPath
  fromFieldPath: spec.tier
  toFieldPath: spec.forProvider.manifest.data.cpuLimit
  transforms:
    - type: map
      map:
        free: "100m"
        standard: "500m"
        premium: "2000m"
```

Apply the updated Composition:

```bash theme={null}
kubectl apply -f webapp-composition.yaml
```

Create an example WebApp XR to test mapping:

```yaml theme={null}
