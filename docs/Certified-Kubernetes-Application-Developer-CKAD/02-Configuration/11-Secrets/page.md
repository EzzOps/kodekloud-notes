# limit-range-memory.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: memory-resource-constraint
spec:
  limits:
  - type: Container
    default:
      memory: "1Gi"
    defaultRequest:
      memory: "1Gi"
    max:
      memory: "1Gi"
    min:
      memory: "500Mi"
```

These LimitRanges ensure that any container created without specific resource settings receives the defined default values. Note that updates to LimitRange configurations impact new or updated pods only.

## Using ResourceQuotas

To control the overall resource usage within a namespace, you can implement ResourceQuotas. A ResourceQuota object sets hard limits on the total CPU and memory consumption (both requested and actual usage) across all pods in the namespace.

For example, a ResourceQuota might restrict the namespace to a total of 4 CPUs and 4 Gi of memory in requests while enforcing a maximum usage of 10 CPUs and 10 Gi of memory across all pods. This mechanism is essential for preventing uncontrolled resource consumption in multi-tenant environments.

## Conclusion

In this guide, we detailed how Kubernetes manages resource requests and limits, ensuring proper resource allocation and preventing overuse. We covered pod scheduling based on resource availability, the importance of setting appropriate resource requests and limits, and how LimitRanges and ResourceQuotas help maintain overall cluster stability.

For further insights on Kubernetes resource management, refer to the [official Kubernetes documentation](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) on managing CPU, memory, and API resources.

![The image lists documentation references for managing memory, CPU, and API resources in Kubernetes, including links for CPU and memory LimitRange.](https://kodekloud.com/kk-media/image/upload/v1752871145/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Resource-Requirements/frame_890.jpg)

> **lightbulb** Continue exploring hands-on labs to reinforce these resource management fundamentals and optimize your cluster’s performance.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/a2ce8bef-967b-48a9-9f58-253035a96c98/lesson/13fb5923-5a5c-44c3-99d3-d5d87b96cb38)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/a2ce8bef-967b-48a9-9f58-253035a96c98/lesson/e3490a78-bb84-4895-bd97-d6ea2494a278)


# Secrets

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Configuration/Secrets/page

This article explains how to securely manage sensitive data using Secrets in Kubernetes.

Welcome to this comprehensive guide on managing Secrets in Kubernetes. In this article, we explain how to securely handle sensitive data for your applications. We begin by reviewing a Python web application that connects to a MySQL database. Upon a successful connection, the application displays a success message. However, the application currently contains hardcoded values for the hostname, username, and password. While moving configuration data to a ConfigMap is suitable for non-sensitive information, it is not recommended for handling passwords and other sensitive data.

Below is an excerpt from the Python application:

```python theme={null}
import os
from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

@app.route("/")
def main():
    mysql.connector.connect(host="mysql", database="mysql",
                              user="root", password="paswrd")
    return render_template('hello.html', color=fetchcolor())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")
```

## Storing Sensitive Data: ConfigMaps vs Secrets

While ConfigMaps are a great option for storing configuration data in plain text, they are not designed to keep passwords or keys secure. This is where Secrets come in. Kubernetes Secrets store sensitive information in an encoded format, making them more secure than using ConfigMaps for these purposes.

Here is an example of a ConfigMap definition:

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
```

> **lightbulb** Storing passwords in plain text—even in a ConfigMap—exposes them to potential security risks. Using Secrets ensures that sensitive data is handled more securely.

## Working with Secrets

Similar to ConfigMaps, handling Secrets typically involves two steps:

1. Creating the Secret.
2. Injecting the Secret into a Pod.

Below are some sample encoded values corresponding to your application's configuration:

```plaintext theme={null}
DB_Host: bXlzcWw=
DB_User: cm9vdA==
DB_Password: cGFzd3Jk
```

And here is the plain text corresponding to those encoded values:

```plaintext theme={null}
DB Host: mysql
DB User: root
DB Password: paswrd
```

There are two primary methods for creating a Secret: the imperative approach and the declarative approach.

## Imperative Method

The imperative method allows you to create a Secret directly from the command line without a definition file. For example:

```bash theme={null}
kubectl create secret generic <secret-name> --from-literal=<key>=<value>
```

A practical example would be:

```bash theme={null}
kubectl create secret generic \
  app-secret --from-literal=DB_Host=mysql \
  --from-literal=DB_User=root \
  --from-literal=DB_Password=paswrd
```

Alternatively, you can create a Secret from a file:

```bash theme={null}
kubectl create secret generic <secret-name> --from-file=<path-to-file>
```

For instance:

```bash theme={null}
kubectl create secret generic \
  app-secret --from-file=app_secret.properties
```

If you need to include multiple key-value pairs, use additional `--from-literal` options. For larger datasets, creating the Secret from a file might be more efficient.

## Declarative Method

The declarative approach leverages a definition file to create a Secret, similar to how ConfigMaps are defined. A typical Secret definition includes the API version, kind, metadata, and data fields. Note that sensitive values should always be encoded in base64. Below is an example of a Secret definition file. Although the values appear in plain text here for demonstration, they must be encoded for production use:

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
data:
  DB_Host: mysql
  DB_User: root
  DB_Password: paswrd
```

You can then create the Secret using:

```bash theme={null}
kubectl create -f secret-data.yaml
```

To encode data on a Linux host, you can use the base64 command. For example:

```bash theme={null}
echo -n 'mysql' | base64
