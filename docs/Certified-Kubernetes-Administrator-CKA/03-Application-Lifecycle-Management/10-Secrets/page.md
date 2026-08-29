# Secrets

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Application-Lifecycle-Management/Secrets/page

This article explains how to securely manage sensitive data in Kubernetes using Secrets while avoiding common security pitfalls.

Welcome to this comprehensive guide on managing Secrets in Kubernetes. In this article, we explain how to securely handle sensitive data (such as passwords and keys) in your Kubernetes deployments while avoiding common pitfalls like hardcoding credentials in your application.

## Problem with Hardcoding Sensitive Data

Consider a simple Python web application connecting to a MySQL database. When the connection succeeds, the application displays a success message. However, the code includes hardcoded values for hostname, username, and password, which poses a serious security risk.

Previously, configuration data like these values might have been stored in a ConfigMap. For example:

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

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  # Configuration data goes here
```

While storing non-sensitive details like hostnames or usernames in a ConfigMap is acceptable, placing a password in such a resource is not secure. Kubernetes Secrets provide a mechanism to safely store sensitive information by encoding the data (note: this is not encryption by default).

<Callout icon="lightbulb">
  Secrets encode data using Base64. Although it provides obfuscation, it is not a substitute for encryption.
</Callout>

## Understanding Kubernetes Secrets

Working with Secrets in Kubernetes involves two main steps:

1. **Create the Secret.**
2. **Inject it into a Pod.**

Below is an illustration of Secret data in their encoded and decoded forms:

### Encoded Values

```plaintext theme={null}
DB_Host: bXlzcWw=
DB_User: cm9vdA==
DB_Password: cGFzd3Jk
```

### Decoded Values

```plaintext theme={null}
DB Host: mysql
DB User: root
DB Password: paswrd
```

There are two primary approaches to creating a Secret:

* **Imperative Creation:** Using the command line to create Secrets on the fly.
* **Declarative Creation:** Defining Secrets in YAML files.

## Imperative Creation of a Secret

With the imperative method, you can supply key-value pairs directly via the command line. For example, to create a Secret named "app-secret" with the key-value pair `DB_Host=mysql`:

```bash theme={null}
kubectl create secret generic app-secret --from-literal=DB_Host=mysql
```

To include multiple key-value pairs, use the `--from-literal` option repeatedly:

```bash theme={null}
kubectl create secret generic app-secret \
  --from-literal=DB_Host=mysql \
  --from-literal=DB_User=root \
  --from-literal=DB_Password=paswd
```

Alternatively, create a Secret from a file with the `--from-file` option:

```bash theme={null}
kubectl create secret generic app-secret --from-file=app_secret.properties
```

## Declarative Creation of a Secret

For a more manageable approach, define a Secret in a YAML file. This file should include the API version, kind, metadata, and encoded data. Below is a sample YAML definition for a Secret:

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
data:
  DB_Host: bXlzcWw=
  DB_User: cm9vdA==
  DB_Password: cGFzd3Jk
```

Apply the definition with the following command:

```bash theme={null}
kubectl create -f secret-data.yaml
```

## Converting Plaintext to Base64

On Linux hosts, you can convert plaintext values to Base64-encoded strings using the `echo -n` command piped to `base64`. For example:

```bash theme={null}
echo -n 'mysql' | base64
echo -n 'root' | base64
echo -n 'paswrd' | base64
