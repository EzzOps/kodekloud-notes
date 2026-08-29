# Making sure Chart is working as intended

Source: https://notes.kodekloud.com/docs/Helm-for-Beginners/Helm-Charts-Anatomy/Making-sure-Chart-is-working-as-intended/page

This article explains methods to validate Helm charts, including linting, template rendering, and dry run installation.

After developing your first Helm chart, it’s crucial to verify its functionality. There are three primary methods to validate your Helm chart before installation:

1. Linting – Checks that the chart and its YAML syntax are correct.
2. Template Rendering – Confirms that the templating logic generates the expected manifest.
3. Dry Run Install – Simulates an installation on Kubernetes to catch issues that only Kubernetes validation can reveal.

Below, we detail each verification method.

***

## 1. Linting the Chart

Linting helps catch formatting errors and typos (for example, misaligned spaces or incorrect variable names such as a misspelling of "release"). Use the following command to lint your chart:

```bash theme={null}
$ helm lint ./nginx-chart
==> Linting ./nginx-chart/
[INFO] Chart.yaml: icon is recommended
[ERROR] templates/: template: nginx-chart/templates/deployment.yaml:4:19: executing "nginx-chart/templates/deployment.yaml" at <.Release.Name>: nil pointer evaluating interface {}.Name
[ERROR] templates/deployment.yaml: unable to parse YAML: error converting YAML to JSON: yaml: line 20: did not find expected '-' indicator
Error: 1 chart(s) linted, 1 chart(s) failed
```

The above output indicates:

* An error on line 4 due to a typo in the variable name.
* A YAML indentation issue on line 20.

After addressing these issues, re-run the lint command. A successful linting process will output:

```bash theme={null}
$ helm lint ./nginx-chart
==> Linting ./nginx-chart/
[INFO] Chart.yaml: icon is recommended
1 chart(s) linted, 0 chart(s) failed
```

> **lightbulb** Including an icon in the Chart.yaml file is recommended as it enhances chart identification.

***

## 2. Verifying Template Rendering

Once linting confirms correct formatting, the next step is to ensure that the templating logic produces the intended Kubernetes manifest. This process renders placeholders such as .Release.Name and variables defined in the values file.

Run the command below to render the template locally:

```bash theme={null}
$ helm template hello-world-1 ./nginx-chart
```

The rendered output may look similar to this:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-world-1-nginx
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
---
apiVersion: v1
kind: Service
metadata:
  name: hello-world-1-nginx
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: http
      protocol: TCP
      name: http
  selector:
    app: hello-world
---
