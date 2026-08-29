# Demo Argo Rollouts Installation and UI

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Rollouts/Demo-Argo-Rollouts-Installation-and-UI/page

Guide to installing Argo Rollouts in Kubernetes, setting up the kubectl-argo-rollouts plugin, and launching the local Rollouts dashboard

Argo Rollouts is a Kubernetes controller and a set of CRDs that enable advanced deployment strategies such as canary releases, blue-green deployments, and progressive delivery. It extends native Kubernetes Deployment semantics with fine-grained rollout control, traffic shifting, metrics-driven analysis, and automated rollbacks.

This guide walks through installing Argo Rollouts into a cluster, installing the kubectl plugin that provides the local dashboard proxy, and verifying the controller and UI are running.

## What you’ll install

* Argo Rollouts controller and CRDs
* RBAC and ConfigMap for the controller
* A ClusterIP metrics Service (exposes metrics internally)
* kubectl-argo-rollouts plugin to access the UI locally

Useful links and references:

* [Argo Rollouts documentation](https://argoproj.github.io/argo-rollouts/)
* [Argo Rollouts Releases on GitHub](https://github.com/argoproj/argo-rollouts/releases)

## Install Argo Rollouts

Apply the official install manifest. This creates the `argo-rollouts` namespace, CRDs, RBAC, the controller Deployment, Service, ConfigMap, and related resources.

Run:

```bash theme={null}
kubectl apply -f https://github.com/argoproj/argo-[SECRET_REDACTED].yaml
```

The install manifest creates several resource types. Example of common resources created:

| Resource Type                  | Purpose                                                                           |
| ------------------------------ | --------------------------------------------------------------------------------- |
| CustomResourceDefinition (CRD) | rollouts.argoproj.io, experiments.argoproj.io, etc. — defines Rollout API objects |
| ServiceAccount / RBAC          | Controller permissions                                                            |
| Deployment                     | argo-rollouts controller Deployment                                               |
| Service                        | ClusterIP service for controller metrics                                          |
| ConfigMap / Secret             | Controller configuration and notifications                                        |

Example output you may see after applying the manifest:

```bash theme={null}
customresourcedefinition.apiextensions.k8s.io/clusteranalysistemplates.argoproj.io created
customresourcedefinition.apiextensions.k8s.io/experiments.argoproj.io created
customresourcedefinition.apiextensions.k8s.io/rollouts.argoproj.io created
serviceaccount/argo-rollouts created
clusterrole.rbac.authorization.k8s.io/argo-rollouts created
clusterrole.rbac.authorization.k8s.io/argo-rollouts-aggregate-to-admin created
clusterrole.rbac.authorization.k8s.io/argo-rollouts-aggregate-to-edit created
clusterrole.rbac.authorization.k8s.io/argo-rollouts-aggregate-to-view created
clusterrolebinding.rbac.authorization.k8s.io/argo-rollouts created
configmap/argo-rollouts-config created
secret/argo-rollouts-notification-secret created
service/argo-rollouts-metrics created
deployment.apps/argo-rollouts created
```

Confirm the controller pod and service are running in the `argo-rollouts` namespace:

```bash theme={null}
kubectl -n argo-rollouts get all
```

Example output:

```bash theme={null}
NAME                                    READY   STATUS    RESTARTS   AGE
pod/argo-rollouts-64d959676c-m6h4w      1/1     Running   0          23s

NAME                                TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)     AGE
service/argo-rollouts-metrics       ClusterIP   10.101.96.18   <none>        8090/TCP    24s

NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/argo-rollouts     1/1     1            1           24s

NAME                                         DESIRED   CURRENT   READY   AGE
replicaset.apps/argo-rollouts-64d959676c     1         1         1       24s
```

<Callout icon="lightbulb">
  The Rollouts controller exposes metrics via a ClusterIP Service (internal to the cluster). It does not provide an externally hosted dashboard by default — to view the Rollouts UI locally, install the kubectl plugin which proxies the dashboard to your machine.
</Callout>

## Install the kubectl-argo-rollouts plugin

The Rollouts UI is accessed through the kubectl plugin binary `kubectl-argo-rollouts`, which registers as `kubectl argo rollouts`. Download the appropriate binary for your OS/architecture from the Argo Rollouts GitHub releases page.

<Frame>
  <img alt="A dark-themed GitHub release page showing the &#x22;Assets&#x22; list for an argo-rollouts release, with file names like install.yaml, dashboard-install.yaml, kubectl-argo-rollouts binaries for multiple OS/architectures, checksums and YAML/JSON assets. Each entry shows a sha256 hash, file size and the Jun 5 date in a scrollable table." />
</Frame>

Download, make executable, and move the binary into your PATH. Adjust the URL and filename to match the release and platform you chose:

```bash theme={null}
