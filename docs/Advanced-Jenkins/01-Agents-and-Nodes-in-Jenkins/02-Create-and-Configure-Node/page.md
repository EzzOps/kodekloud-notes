# local plugin files (example)
B:\JenkinsAdvanced\Jenkins-Advanced\plugins
kubernetes.hpi
kubernetes (1).hpi
```

Install a specific version using `jenkins-plugin-cli`:

```bash theme={null}
jenkins-plugin-cli --plugins kubernetes:4295.v7fa_01b_309c95
```

Or download directly from the update site:

```text theme={null}
https://updates.jenkins.io/download/plugins/kubernetes/4295.v7fa_01b_309c95/kubernetes.hpi
https://updates.jenkins.io/update-center.json
```

If installation fails, check the plugin install logs for dependency errors (for example, an out-of-date Credentials Plugin). Update any required plugins and restart Jenkins. After restart, confirm the Kubernetes plugin appears under Manage Plugins -> Installed.

Refer to the plugin documentation for full details and examples:

<Frame>
  <img alt="A screenshot of the Jenkins plugins website showing the &#x22;Kubernetes&#x22; plugin page with its documentation, description, and a Table of Contents. The right column shows version info, release date, install percentage and related links." />
</Frame>

## 2. Common pipeline primitives (quick reference)

These keywords appear frequently when using Kubernetes agents in Jenkins pipelines.

| Primitive            |                                         Purpose | Example usage                                       |
| -------------------- | ----------------------------------------------: | --------------------------------------------------- |
| `jnlp`               |                     The Jenkins agent connector | used within `podTemplate`                           |
| `container`          | Select a container inside the pod to run a step | `container('maven') { sh 'mvn -v' }`                |
| `node('some-label')` |                     Jenkins node label selector | `node('k8s-agent') { ... }`                         |
| `podTemplate`        |           Define pod shape for ephemeral agents | `podTemplate(containers: [containerTemplate(...)])` |

## 3. Prepare Kubernetes credentials (recommended: least-privilege)

When adding a Kubernetes cloud you can either upload an entire kubeconfig (not recommended if it contains cluster-admin credentials) or provide the Kubernetes API server URL and a restricted credential (recommended). The secure approach:

1. Create a namespace for Jenkins (e.g., `jenkins`).
2. Create a service account in that namespace.
3. Generate a long-duration token for the service account.
4. Add the token to Jenkins as a Secret Text credential and use it in the cloud configuration.

Show Kubernetes cluster info and kubeconfig examples:

```bash theme={null}
# view nodes
kubectl get nodes
# example output
# NAME                       STATUS   ROLES    AGE   VERSION
# pool-yikr9dzvx-g8ooq       Ready    "<none>"   9d    v1.29.9
```

Get the raw kubeconfig:

```bash theme={null}
kubectl config view --raw
```

Example (trimmed) kubeconfig:

```yaml theme={null}
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJ...
    server: https://7b73b07f-...k8s.ondigitalocean.com
  name: do-blr1-k8s-1-29-9-do-3-blr1-1730449013145
contexts:
- context:
    cluster: do-blr1-k8s-1-29-9-do-3-blr1-1730449013145
    user: do-blr1-k8s-1-29-9-do-3-blr1-1730449013145-admin
  name: do-blr1-k8s-1-29-9-do-3-blr1-1730449013145
current-context: do-blr1-k8s-1-29-9-do-3-blr1-1730449013145
kind: Config
preferences: {}
users:
- name: do-blr1-k8s-1-29-9-do-3-blr1-1730449013145-admin
  user:
    token: dop_v1_899c56131410f013fe406f3...
```

Do NOT upload a kubeconfig containing cluster-admin credentials to Jenkins unless you fully understand the security implications.

<Callout icon="lightbulb">
  Use least-privilege credentials: create a dedicated service account in a single namespace for Jenkins instead of using an admin kubeconfig.
</Callout>

### Create a namespace, service account, token, and bind privileges

Commands to set up a restricted service account for Jenkins:

```bash theme={null}
# create namespace
kubectl create namespace jenkins

# create a service account in the jenkins namespace
kubectl -n jenkins create serviceaccount jenkins-service-account

# create a token for the service account (Kubernetes 1.24+)
# adjust --duration as needed; here we set a long duration
kubectl -n jenkins create token jenkins-service-account --duration=9999999s
# example output: eyJh... (the JWT token string)
```

If your cluster version doesn't create legacy secrets, use `kubectl create token` as shown above.

Add the token to Jenkins as a credential:

* Kind: Secret text
* Secret: paste the token value
* ID: e.g. `k8s-jenkins-agent-token`
* Description: optional

## 4. Configure the Kubernetes cloud in Jenkins

After the plugin is installed, go to Manage Jenkins -> Configure System -> Clouds (or Manage Jenkins -> Clouds depending on Jenkins version). Add a new cloud and select "Kubernetes".

In the cloud configuration provide:

| Field          | Suggested value / example                                                                |
| -------------- | ---------------------------------------------------------------------------------------- |
| Name           | `dasher-prod-k8s-us-east`                                                                |
| Kubernetes URL | Use the `server` value from kubeconfig e.g. `https://7b73b07f-...k8s.ondigitalocean.com` |
| Namespace      | `jenkins`                                                                                |
| Credentials    | The Secret Text credential you created (token)                                           |
| CA Certificate | Upload CA cert or leave blank and disable certificate check (not recommended)            |
| Pod labels     | `organization=KodeKloud-Dasher-Org` (optional)                                           |
| Pod retention  | `Never`, `On Failure`, or `Always` (choose per debugging needs)                          |

If Jenkins cannot validate the cluster certificate, either upload the CA certificate in the cloud options or temporarily disable TLS verification (not recommended for production).

If you set everything correctly, click "Test Connection" to validate Jenkins can talk to the Kubernetes API.

<Callout icon="warning">
  Disabling TLS verification is insecure. Only use it for short-term debugging in a trusted environment. For production, upload the cluster CA certificate or ensure certificates are valid.
</Callout>

## 5. RBAC: Grant the service account the needed permissions

Without proper RBAC, the token will fail with 403 Forbidden responses. For example:

```text theme={null}
Error testing connection ... Message: pods is forbidden: User "system:anonymous" cannot list resource "pods" in the namespace "jenkins". Received status: ..., code=403
```

To enable Jenkins to create and manage pods in the `jenkins` namespace, bind an appropriate role. A simple binding to the `admin` ClusterRole scoped to the namespace:

```bash theme={null}
kubectl -n jenkins create rolebinding jenkins-admin-binding \
  --clusterrole=admin \
  --serviceaccount=jenkins:jenkins-service-account
# rolebinding.rbac.authorization.k8s.io/jenkins-admin-binding created
```

If you truly need only specific permissions, craft a `Role` with minimal verbs (e.g., `get`, `list`, `watch`, `create`, `delete`) for resources such as `pods`, `pods/exec`, `services`, `configmaps`, and bind it to the service account.

Note: If you scope the service account to only the `jenkins` namespace, testing another namespace (e.g., `jenkins-123`) will return 403 — this is expected behavior for least-privilege credentials.

## 6. Connectivity options and agent lifecycle

* By default, agent pods connect back to Jenkins over the JNLP (TCP) port. If your Jenkins instance disables the TCP agent port, configure WebSocket or Direct Connection.
* WebSocket agents use HTTP(S), which is useful where TCP is blocked.
* You can set a custom Jenkins URL in global settings if Jenkins is reachable behind a different endpoint.
* Pod labels allow easy filtering and organization for created agent pods.
* Pod retention:
  * Never (default): delete pods after build completes.
  * On Failure: keep pods if the build fails for debugging.
  * Always: retain pods regardless of outcome.

After saving the cloud configuration, Jenkins will be able to spin up agent pods in the configured namespace when a job requests a matching agent.

<Frame>
  <img alt="A screenshot of the Jenkins &#x22;Clouds&#x22; settings page showing one cloud entry named &#x22;dasher-prod-k8s-us-east&#x22; and a &#x22;New cloud&#x22; button in the top-right. The page uses a dark theme and shows navigation/header elements for Jenkins." />
</Frame>

## 7. Test by running jobs

Create or run a pipeline that requests a Kubernetes agent (via label or `podTemplate`) and confirm Jenkins creates a pod in the `jenkins` namespace. Verify pod creation using:

```bash theme={null}
kubectl -n jenkins get pods
```

Watch logs for failures and adjust RBAC, credentials, or TLS settings as needed.

## Useful links and references

* Jenkins Kubernetes plugin: [https://plugins.jenkins.io/kubernetes/](https://plugins.jenkins.io/kubernetes/)
* jenkins-plugin-cli (Plugin installation manager tool): [https://github.com/jenkinsci/plugin-installation-manager-tool](https://github.com/jenkinsci/plugin-installation-manager-tool)
* Kubernetes documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

You have now configured Jenkins to connect to Kubernetes and create ephemeral agent pods. Run pipeline jobs that use this cloud to observe pod lifecycle and logs.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-jenkins/module/d1f217e1-bfef-4ba3-adf8-1411e911e0bc/lesson/1dc5ff53-dfac-4010-82b1-f592cc555ede" />
</CardGroup>


# Create and Configure Node

Source: https://notes.kodekloud.com/docs/Advanced-Jenkins/Agents-and-Nodes-in-Jenkins/Create-and-Configure-Node/page

Guide to creating and connecting a permanent Jenkins agent on an Ubuntu VM, including UI setup, running the agent jar, security settings, troubleshooting, and monitoring.

In distributed Jenkins setups, the controller (master) orchestrates jobs while agents (nodes) execute build steps. This guide shows how to create a permanent Jenkins node and connect an external Ubuntu VM so it can run pipeline stages.

In my environment I created a VM named `ubuntu-docker-jdk17-node20` to act as a dedicated agent. Example shell prompts:

```bash theme={null}
