# Submit workflow with a single parameter from the CLI
argo submit wf.yaml -p message="message from the CLI"
```

* Submit the workflow using a parameter file (YAML or JSON). Example `params.yaml` content:

```yaml theme={null}
message: "This is from a parameter file"
```

Submit with:

```bash theme={null}
# Submit workflow with multiple parameters from a file
argo submit wf.yaml --parameter-file params.yaml
```

* Invoke a different template (entrypoint) in the same workflow without editing the workflow YAML by using `--entrypoint`:

```bash theme={null}
# Submit workflow using a different entrypoint/template
argo submit wf.yaml --entrypoint cowsay-loudly
```

* Combine entrypoint override and custom parameters:

```bash theme={null}
# Combine entrypoint override and custom parameter
argo submit wf.yaml \
  --entrypoint cowsay-loudly \
  -p message="Custom message"
```

By combining `--entrypoint` with `-p` (or `--parameter-file`), you can call any template in your workflow and supply or override any parameter values at submission time.

> **warning** Always quote substitutions and parameter values when they include spaces or
  characters that YAML/CLI might interpret (for example, `-p message="Hello,
      world!"`). Unquoted braces or special characters may cause parsing errors.

Links and references

* [Argo Workflows — Parameters](https://argoproj.github.io/argo-workflows/workflow-parameters/)
* [Argo CLI documentation](https://argoproj.github.io/argo-workflows/cli-overview/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/4540622d-951e-489f-a69f-503d1e226dbb)


# Application health

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/Application-health/page

Explains how ArgoCD assesses Kubernetes application health using built-in checks and customizable Lua scripts to surface resource status and enforce application-specific invariants

Let's look at how ArgoCD performs application health checks. ArgoCD continuously monitors the Kubernetes resources it manages and surfaces a single health status per Application by aggregating checks across those resources.

<Frame>
  <img alt="A diagram titled &#x22;Application Health Checks&#x22; showing an agent that polls a Git repo and applies manifests to a Kubernetes cluster. The cluster box shows a deployment expecting 3 replicas but only 1 is running (marked with a red X)." />
</Frame>

If a resource fails — for example, a Deployment that cannot reach its desired replica count — ArgoCD will mark that resource (and potentially the overall Application) as Unhealthy or Degraded depending on the observed condition.

## Built-in health statuses

ArgoCD exposes a concise set of health states describing resource condition:

| Status      | Meaning                                                                            |
| ----------- | ---------------------------------------------------------------------------------- |
| Healthy     | The resource is functioning as expected.                                           |
| Progressing | The resource is not yet healthy but is in the process of being created or updated. |
| Degraded    | The resource has failed or cannot reach a healthy state.                           |
| Missing     | The resource is defined in Git but not found in the cluster.                       |
| Suspended   | The resource is intentionally paused (for example, a suspended CronJob).           |
| Unknown     | ArgoCD could not determine the health (health assessment failed).                  |

## What ArgoCD checks by default

ArgoCD includes built-in checks for many common Kubernetes resources. The following table summarizes typical checks:

| Resource Type                      | What ArgoCD verifies                                                                |
| ---------------------------------- | ----------------------------------------------------------------------------------- |
| Deployment, StatefulSet, DaemonSet | Observed replicas match the desired replica count; rollout status for readiness.    |
| Service (type=LoadBalancer)        | A LoadBalancer service has an assigned external IP/hostname.                        |
| Ingress                            | Backing service endpoints exist and Ingress status is populated (where applicable). |
| PersistentVolumeClaim              | The PVC is bound to a PV.                                                           |
| CronJob (suspended)                | Suspended CronJobs are reported as Suspended.                                       |

These defaults cover many use cases, but sometimes you need checks tailored to application semantics.

> **lightbulb** Custom health Lua scripts run inside ArgoCD and should defensively handle missing fields to avoid runtime errors. Place these customizations in the argocd-cm ConfigMap (in the argocd namespace).

## Custom health checks with Lua

When default checks are insufficient—for example, you want to validate the content of a ConfigMap or enforce an application-specific invariant—ArgoCD supports custom health checks written in Lua. Customizations live in the argocd-cm ConfigMap under keys like:

resource.customizations.health.\<Kind>

Below is a simple, practical example that flags a ConfigMap as Degraded if it contains an invalid color choice.

color-cm.yaml

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: php-color-cm
data:
  TRIANGLE_COLOR: "white"
```

argocd-cm.yaml (adds a custom health check for ConfigMap)

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
data:
  resource.customizations.health.ConfigMap: |
    -- hs is the health status object returned to ArgoCD
    hs = {}
    hs.status = "Healthy"

    -- Guard against nil to avoid runtime errors when fields are missing
    if obj ~= nil and obj.data ~= nil and obj.data.TRIANGLE_COLOR == "white" then
      hs.status = "Degraded"
      hs.message = "Use a different COLOR"
    end

    return hs
  timeout.reconciliation: "300s"
```

How this works:

* ArgoCD executes the Lua function for each ConfigMap evaluated by the Application because ConfigMap health was customized.
* The Lua script checks obj.data.TRIANGLE\_COLOR; if it equals "white", the script returns a Degraded status and a message.
* ArgoCD surfaces the Degraded state in the Application view, making the misconfiguration visible immediately and simplifying troubleshooting.

## Best practices for custom health checks

* Validate inputs: always check for nil/missing fields to prevent runtime errors in Lua.
* Keep checks focused: prefer small, targeted checks that reflect a single application invariant.
* Limit side effects: health checks should be read-only and deterministic.
* Use meaningful messages: return hs.message so operators can quickly understand what to fix.
* Test locally: iterate on Lua scripts in a development ArgoCD instance before applying in production.

## Links and references

* Argo CD documentation — Health checks: [https://argo-cd.readthedocs.io/en/stable/operator-manual/health/](https://argo-cd.readthedocs.io/en/stable/operator-manual/health/)
* Kubernetes documentation — Concepts: [https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

By combining ArgoCD's built-in checks with focused custom Lua health checks, you can build precise, application-aware health assessments that help teams detect and fix configuration problems faster.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/9114675a-4f04-4296-8b66-53397dbe44a1)
