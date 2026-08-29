# Section Overview

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Custom-Resource-Definitions-Deep-Dive/Section-Overview/page

Guidance on designing strict Kubernetes CustomResourceDefinitions to enforce schemas, defaults, enums, CEL validations, operational subresources, and safe versioning to prevent cross-environment validation failures.

You have a new Custom Resource running in your dev cluster and everything looks normal:

```bash theme={null}
$ kubectl apply -f photo.yaml --context dev
photo.kodekloud.dev/vacation-2024 created
$ kubectl get photo --context dev
NAME            QUALITY   AGE
vacation-2024   ultra     5s
```

However, applying the same object to staging fails with a validation error:

```bash theme={null}
$ kubectl apply -f photo.yaml --context staging
The Photo "vacation-2024" is invalid:
```

This kind of environment-dependent rejection usually points to a CRD that was never strict enough. A permissive schema can let invalid or incomplete objects be created in one environment and then cause validation failures in another.

For example, this simplified CRD lacks sufficient constraints (note how minimal the schema is):

```yaml theme={null}
