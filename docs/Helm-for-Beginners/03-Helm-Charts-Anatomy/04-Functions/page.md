# values.yaml
replicaCount: 2
image: nginx
```

```yaml theme={null}
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}-nginx
spec:
  ports:
    - port: 80
      name: http
  selector:
    app: hello-world
```

Now, suppose different releases require different labels—for example, adding an organizational label to group objects. You can update your configuration as follows:

```yaml theme={null}
# values.yaml
replicaCount: 2
image: nginx
orgLabel: payroll
```

```yaml theme={null}
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}-nginx
  labels:
    org: payroll
spec:
  ports:
    - port: 80
      name: http
  selector:
    app: hello-world
```

However, when the `orgLabel` value is optional, you want these label lines to appear only when the value is provided. Similar to conditionally executing code in programming languages such as Python:

```python theme={null}
orgLabel = "payroll"
if orgLabel:
    print(orgLabel)
```

In Helm charts, you can achieve the same behavior using if blocks. Here’s an updated version of the `service.yaml` file that conditionally adds the organization label:

```yaml theme={null}
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}-nginx
  {{- if .Values.orgLabel }}
  labels:
    org: {{ .Values.orgLabel }}
  {{- end }}
spec:
  ports:
    - port: 80
      name: http
  selector:
    app: hello-world
```

> **lightbulb** The dash (`-`) after the opening braces (`{{-`) ensures that Helm trims any preceding whitespace, preventing extra blank lines in the rendered output.

## Trimming Whitespace in Templates

When Helm renders your templates, it may leave unintended whitespace between directives. To avoid this, use a dash after the opening braces—and before the closing braces, if needed—as shown below:

```yaml theme={null}
{{- if .Values.orgLabel }}
  labels:
    org: {{ .Values.orgLabel }}
{{- end }}
```

This simple trick ensures that your generated YAML files remain clean and free of extra spaces.

## Using If, Else If, and Else Blocks

Helm templates support conditional logic that includes `if`, `else if`, and `else` constructs. Similar to Python's conditional logic, you can use helper functions such as `eq` for equality comparisons. Consider this Python pseudocode:

```python theme={null}
orgLabel = "payroll"

if orgLabel:
    print(orgLabel)
elif orgLabel == "hr":
    print("human resources")
else:
    print("nothing")
```

You can achieve similar logic in a Helm template as follows:

```yaml theme={null}
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}-nginx
  {{- if .Values.orgLabel }}
  labels:
    org: {{ .Values.orgLabel }}
  {{- else if eq .Values.orgLabel "hr" }}
  labels:
    org: human resources
  {{- end }}
spec:
  ports:
    - port: 80
      name: http
  selector:
    app: hello-world
```

In this template, if `orgLabel` is provided, its value is used. If it specifically equals `"hr"`, the label is set to "human resources". This approach leverages Helm's helper functions for clear and concise conditional logic.

## Conditional Creation of Objects

A common use case for Helm conditionals is to control the creation of certain Kubernetes objects based on configuration. For example, you might want to create a ServiceAccount only if it is explicitly enabled in your `values.yaml` file.

In your default `values.yaml`, you can add a section like this:

```yaml theme={null}
# Default values for nginx-chart.
serviceAccount:
  # Specifies whether a ServiceAccount should be created
  create: true
```

Then, wrap the entire ServiceAccount template in a conditional block to ensure it is created only when needed:

```yaml theme={null}
{{- if .Values.serviceAccount.create }}
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {{ .Release.Name }}-robot-sa
{{- end }}
```

This technique provides significant flexibility, allowing users to control which resources are deployed according to their specific requirements.

***

This concludes our deep dive into using conditionals in Helm charts. We demonstrated how to add optional labels, trim whitespace in rendered templates, employ if-else logic using helper functions, and conditionally create resources like service accounts. By leveraging these techniques, you can create more dynamic, efficient, and maintainable Helm charts.

Happy templating!

For more information, explore the official [Helm Documentation](https://helm.sh/docs/).

- [Watch Video](https://learn.kodekloud.com/user/courses/helm-for-beginners/module/b90a4aa4-31b5-43d3-a7aa-383d48c50db0/lesson/b7c4132d-535f-49fd-9677-9faaf96b1320)


# Functions

Source: https://notes.kodekloud.com/docs/Helm-for-Beginners/Helm-Charts-Anatomy/Functions/page

This article explores how functions in Helm enhance templating by processing inputs and providing default values for manifest generation.

In this lesson, we explore how functions work in Helm and how they can enhance your templating process. When you combine a template with values defined in a values.yaml file, Helm generates a valid manifest file. However, if a field in values.yaml is not set, the corresponding section in the manifest may be omitted. For example, consider the following template:

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
      containers:
        - name: hello-world
          image: {{ .Values.image.repository }}
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
```

And the corresponding values.yaml file:

```yaml theme={null}
replicaCount: 2
image:
  repository: 
  pullPolicy: IfNotPresent
  tag: "1.16.0"
```

With these definitions, the generated manifest file will be:

```yaml theme={null}
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
          image: nginx
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
```

> **triangle-alert** If the repository name is not set in values.yaml, the rendered manifest will lack an image value, leading to pod startup failures.

To resolve this issue, the chart can define default values. If the user does not provide a value in values.yaml (or via the command line), Helm can fall back to a default specified using a function. In our example, we want the default image to be "nginx".

## Helm Functions Overview

Helm functions behave similarly to those in conventional programming languages: they process an input and return a transformed output. For instance, the `upper` function converts a string to uppercase, and the `trim` function removes surrounding whitespace. Consider these examples:

```plaintext theme={null}
upper("helm")  ➞  "HELM"
trim(" helm ")  ➞  "helm"
```

Applied within Helm templates, the value of a parameter can be transformed on the fly. For example, the snippet:

```yaml theme={null}
{{ .Values.image.repository }}
```

renders as:

```yaml theme={null}
image: nginx
```

However, if you wrap the same value with the `upper` function:

```yaml theme={null}
{{ upper .Values.image.repository }}
```

the output becomes:

```plaintext theme={null}
image: NGINX
```

Helm also provides other useful functions like `quote` (which surrounds a string with quotes) and `replace` (which substitutes characters within a string). Here are a few examples:

```plaintext theme={null}
{{ upper .Values.image.repository }}
{{ quote .Values.image.repository }}
{{ replace "x" "y" .Values.image.repository }}
{{ shuffle .Values.image.repository }}
```

These string manipulation functions are just a subset of what Helm offers. Additional functions cover areas such as cryptography, date handling, dictionary operations, Kubernetes object management, networking, type conversion, regular expressions, and URL handling. For a complete list of supported functions, refer to the [official Helm documentation](https://helm.sh/docs/).

![The image shows a grid of colored boxes labeled with different programming and technology-related categories, such as "Cryptographic and Security," "Kubernetes," and "Type Conversion." It appears to be a function list from a coding or software development context.](../../../../images/kodekloud.com/kk-media/image/upload/v1752878955/notes-assets/images/Helm-for-Beginners-Functions/programming-categories-function-list.jpg)

## Using the Default Function

Revisiting the earlier issue of a missing image repository value: if the value is not supplied in values.yaml or via the command line, the rendered manifest will omit an image, potentially causing a pod to fail. To ensure that your deployment always includes a valid image, use the `default` function. By specifying a default value (enclosed in quotes to treat it as a string), Helm will use "nginx" if no repository value is provided.

Consider the updated template snippet:

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
      containers:
      - name: hello-world
        image: {{ default "nginx" .Values.image.repository }}
        ports:
        - name: http
          containerPort: 80
          protocol: TCP
```

The values.yaml file remains:

```yaml theme={null}
replicaCount: 2
image:
  repository: ""
  pullPolicy: IfNotPresent
  tag: "1.16.0"
```

With this configuration, if the image repository is not specified, Helm substitutes the default "nginx", resulting in the following manifest:

```yaml theme={null}
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
        image: nginx
        ports:
        - name: http
          containerPort: 80
          protocol: TCP
```

> **lightbulb** Using the `default` function ensures that your deployments always have a valid image configuration, preventing potential pod failures due to missing settings.

That concludes our discussion on functions in Helm. In the next lesson, we will dive deeper into additional Helm templating features.

- [Watch Video](https://learn.kodekloud.com/user/courses/helm-for-beginners/module/b90a4aa4-31b5-43d3-a7aa-383d48c50db0/lesson/bc5b9ecd-38d7-4099-9f7b-13849b39d9f3)
