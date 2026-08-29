# The path is relative to the spec.source.path directory defined above
valueFiles:
  - values-prod.yaml

# Ignore locally missing valueFiles when installing Helm chart. Defaults to false
ignoreMissingValueFiles: false

# Values file as block (YAML). Prefer to use valuesObject if possible (see below)
values: |
  ingress:
    enabled: true
    path: /
    hosts:
      - mydomain.example.com
    annotations:
      kubernetes.io/ingress.class: nginx
      kubernetes.io/tls-acme: "true"
    labels: {}
    tls:
      - secretName: mydomain-tls
        hosts:
          - mydomain.example.com

# Values as a native object. This takes precedence over `values`
valuesObject:
  ingress:
    enabled: true
    path: /
    hosts:
      - mydomain.example.com
    annotations:
      kubernetes.io/ingress.class: nginx
      kubernetes.io/tls-acme: "true"
    labels: {}
    tls:
      - secretName: mydomain-tls
        hosts:
          - mydomain.example.com
```

### Other Helm options

Argo CD supports additional Helm options that affect templating and installation:

```yaml theme={null}
# Skip custom resource definition installation if chart contains CRDs
skipCrds: false

# Skip schema validation if chart contains JSON schema validation. Defaults to false
skipSchemaValidation: false

# Optional Helm version to template with. If omitted, Argo CD will decide which Helm binary to use automatically.
# Valid values: 'v2' or 'v3'
version: v3

# You can specify the Kubernetes version to pass to Helm when templating manifests.
# The value must be semver formatted.
kubeVersion: "1.30.0"

# You can specify additional API versions to pass to Helm when templating.
# Format: [group]/version/kind (or just version/kind)
apiVersions:
  - traefik.io/v1alpha1/TLSOption
  - v1/Service

# Optional namespace to template with. If left empty, defaults to the app's destination.
namespace: custom-namespace
```

Argo CD also supports other customization tools such as Kustomize. This lesson focuses on Helm, but here is a reference Kustomize block for completeness:

```yaml theme={null}
kustomize:
  # Optional kustomize version. Note: version must be configured in argocd-cm ConfigMap
  version: v3.5.4
  namePrefix: prod-
  nameSuffix: -some-suffix
  commonLabels:
    foo: bar
  commonAnnotations:
    beep: boop-${ARGOCD_APP_REVISION}
  commonAnnotationsEnvsubst: true
  labelWithoutSelector: false
  labelIncludeTemplates: false
  forceCommonLabels: false
  forceCommonAnnotations: false
  images:
    - quay.io/argoprojlabs/argocd-e2e-container:0.2
    - my-app=gcr.io/my-repo/my-app:0.1
  namespace: custom-namespace
  replicas:
    - name: kustomize-guestbook-ui
      count: 4
  components:
    - ./component
```

***

## Example Helm chart (repo) — values and templates

The demo repository contains a simple Helm chart (v1.0.0) with a `values.yaml` and templates that render a ConfigMap and a Deployment.

Default `values.yaml` (chart defaults):

```yaml theme={null}
replicaCount: 1

image:
  repository: siddharth67/php-random-shapes:v1
  pullPolicy: IfNotPresent
  # Overrides the image tag whose default is the chart appVersion.
  tag: ""

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

service:
  type: ClusterIP
  port: 80
  targetPort: 80

color:
  circle: black
  oval: black
  triangle: black
  rectangle: black
  square: black
```

`templates/configmap.yaml` (reads color values from chart values):

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  CIRCLE_COLOR: {{ .Values.color.circle }}
  OVAL_COLOR: {{ .Values.color.oval }}
  SQUARE_COLOR: {{ .Values.color.square }}
  TRIANGLE_COLOR: {{ .Values.color.triangle }}
  RECTANGLE_COLOR: {{ .Values.color.rectangle }}
```

`templates/deployment.yaml` (uses values for replicas, image, envFrom configmap):

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-deploy
  labels:
    {{- include "random-shapes.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "random-shapes.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{- include "random-shapes.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          envFrom:
            - configMapRef:
                name: {{ .Release.Name }}-configmap
```

When Argo CD detects this chart in a repo, the UI pre-populates fields from the chart's default `values.yaml`. If you don't provide any overrides, Argo CD will deploy using those chart defaults.

<Frame>
  <img alt="Screenshot of a web UI for creating a Helm release, showing a parameters form with entries like color.circle, color.oval, color.rectangle all set to &#x22;black&#x22; and image repository/pullPolicy fields. A navigation sidebar with applications is visible on the left." />
</Frame>

Create the Application in Argo CD with your desired sync options (for example, automatic sync, auto-create namespace, destination server set to in-cluster). By default the chart renders with the chart's default values (all shapes black, service type ClusterIP, image from `values.yaml`). The Deployment and Pod should appear in the target namespace (for example, `helm-chart`).

Here is the Application resource tree showing the deployed resources:

<Frame>
  <img alt="A web dashboard screenshot (Argo CD) showing the &#x22;helm-random-shapes&#x22; application with &#x22;Healthy&#x22; and &#x22;Synced&#x22; status. The main pane displays a visual resource tree linking configmap, service, deployment, replica set and pod components." />
</Frame>

***

## Updating values from the Argo CD UI

Argo CD offers multiple ways to change Helm values after the Application has been created:

* Upload a `values.yaml` file to the Application
* Edit `values` (YAML block)
* Edit `valuesObject` (map form)
* Edit `parameters` (name/value list — highest precedence)

Example inline `values` override added in the UI or to the Application manifest:

```yaml theme={null}
color:
  circle: red
service:
  type: NodePort
```

After saving, Argo CD re-renders the manifests and applies the updated resources. For example, the ConfigMap will change to reflect the override:

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: helm-random-shapes-configmap
  namespace: helm-chart
data:
  CIRCLE_COLOR: red
  OVAL_COLOR: black
  RECTANGLE_COLOR: black
  SQUARE_COLOR: black
  TRIANGLE_COLOR: black
```

If you change service type to NodePort, the Service manifest updates accordingly:

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: helm-random-shapes-service
  namespace: helm-chart
spec:
  type: NodePort
  ports:
    - name: http
      nodePort: 31592
      port: 80
      protocol: TCP
      targetPort: 80
  selector:
    app.kubernetes.io/instance: helm-random-shapes
    app.kubernetes.io/name: random-shapes-chart
```

> **warning** Updating a ConfigMap consumed by a Deployment (via envFrom) does not automatically restart running pods. To make pods pick up the new environment variables, perform a rollout restart on the Deployment, or use Argo CD reconciliation policies to trigger pod replacement.

Example command to restart the deployment so new pods pick up updated ConfigMap values:

```bash theme={null}
kubectl rollout restart deployment helm-random-shapes-deploy -n helm-chart
```

After the rollout, new pods will read the updated environment variables and the application behavior (e.g., circle color) will change accordingly.

***

## Overriding using Parameters (highest precedence)

Argo CD exposes Helm `parameters` (a list of name/value pairs) that take the highest precedence when templating. Parameters are useful for single-value overrides or when you prefer a flat list.

Example `parameters` entry:

```yaml theme={null}
parameters:
  - name: "color.circle"
    value: "green"
```

If the same key is present in both `values` (or `valuesObject`) and `parameters`, the value from `parameters` will be used. For example:

* `values` sets `color.circle: red`
* `parameters` sets `color.circle: green`
* Result in rendered manifests: `CIRCLE_COLOR: green`

***

> **lightbulb** Precedence summary: when multiple Helm override mechanisms are used, Argo CD applies them in a defined order — last overrides win. Use the precedence table below to decide where to place your overrides.

## Helm values precedence (Argo CD ordering)

From lowest to highest precedence:

| Precedence rank | Source / Mechanism                      | Notes                                                              |
| --------------- | --------------------------------------- | ------------------------------------------------------------------ |
| 1 (lowest)      | chart defaults (`values.yaml` in chart) | Used only if not overridden                                        |
| 2               | valueFiles (`valueFiles` list)          | Files processed in listed order; later files override earlier ones |
| 3               | `values` (inline YAML block)            | Raw YAML block in Application spec                                 |
| 4               | `valuesObject` (map)                    | Native object; overrides `values`                                  |
| 5 (highest)     | `parameters` (name/value list)          | Highest precedence; last parameter entry wins for duplicate names  |

Additional notes on duplicates and ordering:

* If the same parameter is supplied multiple times, the last occurrence wins.
* If `valueFiles` includes multiple files, the last file in the list has the highest priority among them.
* If a single values file contains duplicate keys, the last occurrence in the file wins.
* `valuesObject` overrides `values` when both are present.
* `parameters` override everything else.

Examples:

valueFiles ordering:

```yaml theme={null}
valueFiles:
  - values-file-1.yaml
  - values-file-2.yaml
```

If `values-file-1.yaml` contains `param1: value1` and `values-file-2.yaml` contains `param1: value2`, the effective value is `value2`.

parameters duplicate example:

```yaml theme={null}
parameters:
  - name: "param1"
    value: value2
  - name: "param1"
    value: value1
```

Effective result: `param1=value1` (last parameter entry wins).

values block duplicate example:

```yaml theme={null}
values: |
  param1: value2
  param1: value5
```

Effective result: `param1=value5` (last value in the block wins).

***

## Additional example — Helm chart from a Helm repo

When using a Helm repository as `repoURL`, set `spec.source.chart` and `spec.source.targetRevision` (chart version). Example Application:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: sealed-secrets
  namespace: argocd
spec:
  project: default
  source:
    chart: sealed-secrets
    repoURL: https://bitnami-labs.github.io/sealed-secrets
    targetRevision: 1.16.1
    helm:
      releaseName: sealed-secrets
  destination:
    server: "https://kubernetes.default.svc"
    namespace: kubeseal
```

When using a Git repo as `repoURL`, `targetRevision` is a Git revision (branch/tag/commit), and `path` points to the chart inside the repository.

***

## References and further reading

* Argo CD Official Docs: [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/)
* Helm Documentation: [https://helm.sh/docs/](https://helm.sh/docs/)
* Kubernetes Concepts: [https://kubernetes.io/docs/concepts/](https://kubernetes.io/docs/concepts/)

This walkthrough covered deploying a Helm chart with Argo CD, how to update Helm values via UI or manifests, and how Argo CD determines which override mechanism wins during templating.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/be3c419c-89f4-4201-bde8-f015fe1ced7b)


# Demo Git Webhook Configuration

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/Demo-Git-Webhook-Configuration/page

How to configure Git webhooks so Argo CD receives immediate repository change notifications, plus setup examples, TLS troubleshooting, insecure testing, and validation in the Argo CD UI.

This guide shows how to configure Git webhooks so Argo CD receives repository change notifications immediately instead of waiting for the default three-minute poll. With webhooks configured, Argo CD can detect and apply manifest changes as soon as you push them, enabling true GitOps continuous delivery.

Key topics covered:

* Webhook endpoint for Argo CD
* Example repository manifest
* Adding the webhook in your Git provider
* Troubleshooting TLS / self-signed certificates
* Running Argo CD in insecure mode for testing
* Validating the webhook workflow in the Argo CD UI

> **lightbulb** This guide assumes you have Argo CD installed and an application configured to track your Git repository. For Argo CD installation and basic app creation, see the official Argo CD docs: [Argo CD Documentation](https://argo-cd.readthedocs.io/).

Webhook endpoint format

* The webhook endpoint for Argo CD accepts POST events at /api/webhook on the Argo CD server. Example forms of the endpoint:

```text theme={null}
/api/webhook
https://argocd.example.com/api/webhook
targetRevision: refs/tags/x
```

Add this URL (the Argo CD server API endpoint) as the payload URL in your Git provider's webhook configuration so push events are sent to Argo CD. See your Git provider docs for webhook setup details (for example, GitHub Webhooks).

<Frame>
  <img alt="A screenshot of an Argo CD documentation webpage showing the GitHub &#x22;Add webhook&#x22; form with fields for Payload URL, content type, secret, and event options. Navigation menus appear in sidebars on the left and right." />
</Frame>

Example repository and manifest

* In this example we have a GitOps repository containing an Nginx Deployment manifest. The goal is for Argo CD to update the cluster whenever this file changes.

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: nginx
  name: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  strategy: {}
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - image: nginx
        name: nginx
        imagePullPolicy: Always
        ports:
        - containerPort: 80
```

Add the webhook in your Git provider's repository settings and point it to your Argo CD server URL plus /api/webhook using the POST method and content-type application/json. If your Git server and Argo CD run in the same Docker or local environment, ensure the URL uses an address reachable from the Git server (IP or DNS).

Recommended webhook settings (summary):

| Setting      | Value / Recommendation                                         |
| ------------ | -------------------------------------------------------------- |
| Payload URL  | https\://\<argocd-host>/api/webhook                            |
| HTTP method  | POST                                                           |
| Content type | application/json                                               |
| Events       | Push events (or custom events that include push)               |
| Secret       | Optional — set and configure Argo CD if you use a secret token |

<Frame>
  <img alt="A dark-themed Gitea repository settings screen showing the &#x22;Add Webhook&#x22; form with the target URL set to https://192.168.65.254:31148/api/webhook, HTTP method POST, content type application/json, and &#x22;Push Events&#x22; selected as the trigger." />
</Frame>

Troubleshooting TLS / self-signed certificates

* If Argo CD is served over HTTPS with a self-signed certificate, Git providers may reject webhook delivery because the certificate is not trusted. A common delivery error looks like:

```text theme={null}
Delivery: Post "https://192.168.65.254:31148/api/webhook": tls: failed to verify certificate: x509: cannot validate certificate for 192.168.65.254
```

Options to resolve delivery failures:

* Provision a valid TLS certificate signed by a trusted CA and use that on the Argo CD server.
* Configure your Git provider to trust your test CA (if supported).
* For demo or local testing only, run Argo CD in insecure (HTTP) mode so webhooks can be delivered without TLS verification. Do not use insecure mode in production.

<Frame>
  <img alt="A dark-themed browser screenshot of a webhook settings page (served from localhost) showing trigger options (Push/All/Custom), a branch filter and authorization header field, plus &#x22;Update Webhook&#x22; and &#x22;Remove Webhook&#x22; buttons. Below is a &#x22;Recent Deliveries&#x22; panel showing a delivery entry marked with an error and request/response details." />
</Frame>

To allow insecure delivery (demo/testing only)

1. Edit the ConfigMap used by Argo CD command parameters (example: argocd-cmd-params-cm in the argocd namespace) and add the `server.insecure` key set to "true". This configures the Argo CD server to run in insecure HTTP mode for testing.

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cmd-params-cm
  namespace: argocd
data:
  server.insecure: "true"
```

2. Save the ConfigMap and restart the Argo CD server deployment so the change takes effect:

```bash theme={null}
kubectl -n argocd edit cm argocd-cmd-params-cm
kubectl -n argocd rollout restart deployment argocd-server
```

3. Verify pods are running:

```bash theme={null}
kubectl -n argocd get po
```

Example output (shortened):

```text theme={null}
NAME                                            READY   STATUS    RESTARTS   AGE
argocd-application-controller-0                 1/1     Running   1          4h30m
argocd-repo-server-6577b8fd64-bxvbq             1/1     Running   0          22m
argocd-server-648fc5d9df-x29st                  1/1     Running   2          23s
```

> **warning** Enabling server.insecure: "true" disables TLS on the Argo CD server and allows webhook delivery over plain HTTP. This is strictly for demo or test environments. For production, always provision TLS certificates from a trusted CA or configure your Git provider to trust your certificate authority.

Switch webhook URL to HTTP (if using insecure server)

* After setting `server.insecure: "true"` and restarting the server, update the webhook URL in your Git provider to use http\:// instead of https\:// so the provider posts to the insecure test endpoint. Re-trigger the webhook delivery and check for a successful response (HTTP 200/201 or other success code).

Successful delivery example (truncated):

```json theme={null}
{
  "request": { "method": "POST", "url": "http://192.168.65.254:31148/api/webhook" },
  "response": { "status": 201, "body": "9e6ccc14-4b36-4ab7-a733-4935a076e6b2" }
}
```

When webhook delivery succeeds, Argo CD receives the push event immediately and refreshes the repository to detect changes.

Validating the workflow in Argo CD

* Open the Argo CD UI and view your application (for example, an application named nginx-app-1). Before changes, the application should show Healthy and Synced when there are no pending updates.

<Frame>
  <img alt="A screenshot of the Argo CD web interface showing the &#x22;nginx-app-1&#x22; application with &#x22;Healthy&#x22; app health and &#x22;Synced&#x22; sync status. The resource graph displays the nginx deployment flowing to a replicaset and pod." />
</Frame>

Make a change to the repository (for example, reduce replicas from 3 to 1), commit, and push. The push will trigger a webhook event that Argo CD receives and processes.

<Frame>
  <img alt="A dark-themed Git repository web page (Gitea) showing a file/folder listing (folders like nginx-app, helm-chart, .gitignore, LICENSE) and recent commit messages. The right sidebar shows repository details including description, license and language statistics." />
</Frame>

Example push notification payload (snippet)

* The webhook payload contains commit metadata and the list of modified files. Argo CD uses this to refresh the repository and detect changed manifests.

```json theme={null}
{
  "total_commits": 1,
  "head_commit": {
    "id": "46585fdf428be401234aecb18b1931f34d51a009",
    "message": "Update nginx-app/deployment.yml",
    "timestamp": "2025-10-23T11:35:55Z",
    "modified": ["nginx-app/deployment.yml"]
  },
  "repository": {
    "id": 9,
    "owner": { "login": "kk-org" }
  }
}
```

When everything is configured correctly:

* Argo CD immediately detects the change from the webhook and refreshes the repository.
* If auto-sync is enabled for the application, Argo CD will apply the updated manifest automatically. Otherwise, you can sync manually from the UI or CLI.
* Occasionally you may need to refresh the Argo CD UI or re-login to see updated statuses.

Further reading and references

* [Argo CD Documentation](https://argo-cd.readthedocs.io/)
* [GitHub Webhooks](https://docs.github.com/en/developers/webhooks-and-events/about-webhooks)
* [Kubernetes kubectl Reference](https://kubernetes.io/docs/reference/kubectl/)

That completes the Git webhook configuration workflow for Argo CD.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/352bff5b-5b25-457a-9692-1aef5d98f0e8)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/31bc5140-91a3-45a9-a4be-931ed7988e53)
