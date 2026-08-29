# Default values for nginx-chart.
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.
replicaCount: 2
image: nginx
```

Notice that the release name is incorporated as "hello-world-1" from the command. If no name is provided, Helm defaults to a generated release name. If there is a YAML indentation or templating error, you might see an error message like:

```bash theme={null}
$ helm template ./nginx-chart
Error: YAML parse error on nginx-chart/templates/deployment.yaml: error converting YAML to JSON: yaml: line 5: mapping values are not allowed in this context
```

In such cases, use the debug flag to help diagnose the issue:

```bash theme={null}
$ helm template ./nginx-chart --debug
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-world
spec:
  replicas: 2
  selector:
    matchLabels:
      app: hello-world
  template:
    metadata:
      labels:
        app: hello-world
    spec:
      containers:
      - name: hello-world
        image: {{ .Values.image }}
        ports:
        - name: http
          containerPort: 80
          protocol: TCP

# Default values for nginx-chart.
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.
replicaCount: 2
image: nginx
```

This debug output aids in identifying and fixing any rendering issues.

***

## 3. Simulating an Installation with a Dry Run

Linting and template rendering catch many issues; however, they might not detect errors within the final manifest applied to Kubernetes. For example, if the Deployment spec mistakenly uses "container" instead of "containers", the issue won't be caught by earlier checks.

Consider the following incorrect manifest snippet:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-nginx
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: hello-world
  template:
    metadata:
      labels:
        app: hello-world
    spec:
      container:  # Incorrect field; should be "containers"
        - name: hello-world
          image: {{ .Values.image }}
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
```

Since the YAML structure and templating appear correct, neither linting nor template rendering flags this error. To validate the entire manifest against Kubernetes standards, execute the following dry-run command:

```bash theme={null}
$ helm install hello-world-1 ./nginx-chart --dry-run
Error: unable to build kubernetes objects from release manifest: error validating "": error validating data: [ValidationError(Deployment.spec.template.spec): unknown field "container" in io.k8s.api.core.v1.PodSpec, ValidationError(Deployment.spec.template.spec): missing required field "containers" in io.k8s.api.core.v1.PodSpec]
```

After correcting the mistake and re-running the dry run, you should observe a successful simulated installation with detailed manifest output:

```bash theme={null}
$ helm install hello-world-1 ./nginx-chart --dry-run
NAME: hello-world-1
LAST DEPLOYED: Fri Nov 19 18:34:51 2021
NAMESPACE: default
STATUS: pending-install
REVISION: 1
TEST SUITE: None
HOOKS:
MANIFEST:
---
# Source: nginx-chart/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: hello-world-1-nginx
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: http
```

> **lightbulb** Using the dry run option is instrumental in verifying that Kubernetes accepts your final manifests. This step minimizes the risk of encountering runtime errors during actual deployment.

***

## Summary

In this guide, we explored the three critical methods to verify your Helm charts:

* **Linting** checks for formatting and syntax errors.
* **Template Rendering** confirms correct variable substitution and manifest creation.
* **Dry Run Installation** validates the final manifest against Kubernetes APIs.

Implement these practices to confidently build, validate, and deploy your Helm charts. Happy charting!

***

## Quick Reference Table

| Verification Method  | Primary Purpose                                           | Example Command                                      |
| -------------------- | --------------------------------------------------------- | ---------------------------------------------------- |
| Linting              | Validate chart formatting and syntax                      | `helm lint ./nginx-chart`                            |
| Template Rendering   | Render and inspect final Kubernetes manifest              | `helm template hello-world-1 ./nginx-chart`          |
| Dry Run Installation | Simulate deployment to catch Kubernetes validation errors | `helm install hello-world-1 ./nginx-chart --dry-run` |

For additional insights and detailed Kubernetes concepts, visit the [Kubernetes Documentation](https://kubernetes.io/docs/).

- [Watch Video](https://learn.kodekloud.com/user/courses/helm-for-beginners/module/b90a4aa4-31b5-43d3-a7aa-383d48c50db0/lesson/abdf0a80-9375-49af-9954-8007f4106d8c)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/helm-for-beginners/module/b90a4aa4-31b5-43d3-a7aa-383d48c50db0/lesson/ef6d5919-cd28-4d13-8298-1f3f1961f07e)


# Named Templates

Source: https://notes.kodekloud.com/docs/Helm-for-Beginners/Helm-Charts-Anatomy/Named-Templates/page

Learn to use named templates in Helm to reduce repetitive code in Kubernetes manifests and improve maintainability.

In this lesson, you'll learn how to use named templates to eliminate repetitive code in your Helm charts. When creating Kubernetes manifests, you might notice that labels or other blocks often repeat across multiple objects. For instance, consider the following YAML snippets for a Service and a Deployment where identical label definitions appear in several sections:

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}-nginx
  labels:
    app.kubernetes.io/name: nginx
    app.kubernetes.io/instance: nginx
spec:
  ports:
    - port: 80
      targetPort: http
      protocol: TCP
      name: http
  selector:
    app: hello-world
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-nginx
  labels:
    app.kubernetes.io/name: nginx
    app.kubernetes.io/instance: nginx
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: nginx
      app.kubernetes.io/instance: nginx
  template:
    metadata:
      labels:
        app.kubernetes.io/name: nginx
        app.kubernetes.io/instance: nginx
    spec:
      containers:
        - name: nginx
          image: "nginx:1.16.0"
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
```

As your codebase expands, duplicating these definitions increases the risk of errors and inconsistencies during updates.

***

> **lightbulb** Keep your Helm charts DRY (Don't Repeat Yourself) by consolidating common code blocks in a helper file.

## Moving Common Labels to a Helper File

To address this redundancy, you can transfer the shared lines to a helper file (commonly named `_helpers.tpl`). The underscore in the filename tells Helm to ignore this file when generating Kubernetes manifests. For example, if you start with a Service template like this:

```yaml theme={null}
