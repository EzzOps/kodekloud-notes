# Manage Kubernetes secrets

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Security-Specialist-CKS/Minimize-Microservice-Vulnerabilities/Manage-Kubernetes-secrets/page

This article provides a guide on securing applications with Kubernetes Secrets, detailing creation, injection, and best practices for managing sensitive data.

Welcome to this comprehensive guide on securing your applications with Kubernetes Secrets. In this lesson, you'll learn how to replace hardcoded sensitive data in your applications with a more secure approach using Kubernetes Secrets. We will walk through a Python web application example, demonstrate both imperative and declarative methods for creating Secrets, and explain how to inject these Secrets into your Pods securely.

## Example Application Overview

In our example, a simple Python web application connects to a MySQL database. On a successful connection, the application displays a success message. However, the code currently hardcodes the database hostname, username, and password. Although non-sensitive data such as hostnames or usernames can be stored in a ConfigMap, using the same approach for sensitive information like passwords is not recommended.

Below is an excerpt of the Python application code:

```python theme={null}
import os
from flask import Flask, render_template  # Added render_template import

app = Flask(__name__)

@app.route("/")
def main():
    # Warning: Hardcoding credentials (host, user, password) is not secure.
    mysql.connector.connect(host="mysql", database="mysql",
                            user="root", password="paswrd")
    return render_template('hello.html', color=fetchcolor())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")
```

<Callout icon="triangle-alert">
  Hardcoding credentials in your application code is insecure. Use Kubernetes Secrets to manage sensitive configuration data securely.
</Callout>

A sample ConfigMap for non-sensitive configurations might look like this:

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  # Non-sensitive configuration data can be placed here.
```

While a ConfigMap can hold non-sensitive values safely, passwords require an extra layer of security. This is where Kubernetes Secrets become essential—they store sensitive information in an encoded format rather than plain text.

## Steps to Work with Kubernetes Secrets

Creating and using Secrets generally involves two main steps:

1. **Create the Secret.**
2. **Inject the Secret into a Pod.**

### Mapping Plain Text to Base64 Encoded Values

Consider the following mapping between plain text values and their corresponding base64-encoded values:

Plain text:

```text theme={null}
DB Host:      mysql
DB User:      root
DB Password:  paswrd
```

Encoded format:

```text theme={null}
DB_Host:      bXlzcWw=
DB_User:      cm9vdA==
DB_Password:  cGFzd3Jk
```

<Callout icon="lightbulb">
  Always encode your sensitive data using base64 when creating a declarative Secret. Avoid using plain text values.
</Callout>

## Creating a Secret

There are two primary methods to create a Kubernetes Secret: the imperative and declarative approaches.

### Imperative Approach

With the imperative approach, you can directly add key-value pairs from the command line. For example, to create a secret named "app-secret" with values for DB\_Host, DB\_User, and DB\_Password, use:

```bash theme={null}
kubectl create secret generic app-secret --from-literal=DB_Host=mysql --from-literal=DB_User=root --from-literal=DB_Password=paswrd
```

Alternatively, if you have your data stored in a file, you can create the secret with:

```bash theme={null}
kubectl create secret generic app-secret --from-file=app_secret.properties
```

### Declarative Approach

For a more controlled process, create a YAML definition for the Secret. Note that all values must be base64 encoded. Here is an example:

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

Create the Secret by applying the YAML file:

```bash theme={null}
kubectl create -f secret-data.yaml
```

> Note: When specifying data values in plain text, the information is not secure. Ensure that the secret values are base64 encoded using one of the available encoding methods.

### Encoding Secret Data

On a Linux system, you can generate the base64-encoded version of your secret by running:

```bash theme={null}
echo -n 'mysql' | base64
echo -n 'root' | base64
echo -n 'paswrd' | base64
