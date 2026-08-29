# Read background color from environment; default to "red"
color = os.environ.get("APP_COLOR", "red")

@app.route("/")
def main():
    print(f"Current color: {color}")
    return render_template("hello.html", color=color)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

To test locally:

```bash theme={null}
export APP_COLOR=blue
python app.py
```

Visit `http://localhost:8080`—the page background will reflect your `APP_COLOR`. If you don’t set `APP_COLOR`, it gracefully falls back to **red**.

> **triangle-alert** Never commit sensitive environment variables (like credentials) to your code repository. Consider using a secrets manager for production.

***

## Step 2: Pass Variables into Docker

Once your app is containerized, leverage Docker’s `-e` flag (or `--env-file`) to inject runtime configuration.

1. **Build the image**
   ```bash theme={null}
   docker build -t simple-webapp-color .
   ```
2. **Run with a custom color**
   ```bash theme={null}
   docker run -e APP_COLOR=blue simple-webapp-color
   ```
3. **Scale with different settings**
   ```bash theme={null}
   docker run -e APP_COLOR=green simple-webapp-color
   docker run -e APP_COLOR=yellow simple-webapp-color
   ```

By externalizing `APP_COLOR`, you keep one image for all environments—no code changes required.

***

## Docker Commands Reference

| Command                            | Purpose                                 | Example                                                |
| ---------------------------------- | --------------------------------------- | ------------------------------------------------------ |
| `docker build`                     | Build an image from a `Dockerfile`      | `docker build -t simple-webapp-color .`                |
| `docker run -e VAR=VALUE`          | Run a container with an environment var | `docker run -e APP_COLOR=blue simple-webapp-color`     |
| `docker run --env-file ./env.list` | Load multiple vars from a file          | `docker run --env-file ./env.list simple-webapp-color` |

***

## Further Reading

* [Flask Official Documentation](https://flask.palletsprojects.com/)
* [Docker ENV and ARG](https://docs.docker.com/engine/reference/builder/#env)
* [The Twelve-Factor App: Config](https://12factor.net/config)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/d9358627-4fc7-4acc-ab96-fa25232555c6/lesson/0e0f5842-508b-4a14-905f-9a55be61d342)


# Environment Variables

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Kubernetes/Environment-Variables/page

This article explains how to set environment variables in Kubernetes Pods using direct assignment and external sources like ConfigMaps and Secrets.

Kubernetes lets you inject configuration data into Pods via environment variables. This declarative approach mirrors Docker’s `-e` flag but offers tighter integration with Kubernetes primitives like ConfigMaps and Secrets.

## Why Use Environment Variables?

* Decouple configuration from container images
* Simplify application customization across environments
* Secure sensitive data using Secrets

## Prerequisites

* A running Kubernetes cluster
* `kubectl` configured against your cluster
* Basic knowledge of Pods and YAML manifests

***

## 1. Direct Assignment with `value`

To set an environment variable directly in your Pod spec, use the `env` array under the container definition:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp-color
spec:
  containers:
    - name: simple-webapp-color
      image: simple-webapp-color
      ports:
        - containerPort: 8080
      env:
        - name: APP_COLOR
          value: pink
```

This makes `APP_COLOR=pink` available inside the container.

> **lightbulb** Direct assignment is ideal for non-sensitive, static configuration values.

You can replicate this behavior in Docker with:

```bash theme={null}
docker run -e APP_COLOR=pink simple-webapp-color
```

***

## 2. Decoupling Config with `valueFrom`

Rather than embedding values in your Pod spec, you can reference external sources:

```yaml theme={null}
env:
  # From a ConfigMap
  - name: APP_COLOR
    valueFrom:
      configMapKeyRef:
        name: my-configmap
        key: color.value

  # From a Secret
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: my-secret
        key: db.password
```

> **triangle-alert** Secrets are only base64-encoded by default and not encrypted at rest. Use encryption providers or external secret stores for stronger security.

***

## 3. Comparison at a Glance

| Configuration Source | Field                       | When to Use                                      |
| -------------------- | --------------------------- | ------------------------------------------------ |
| Direct               | `value`                     | Static, non-sensitive values                     |
| ConfigMap            | `valueFrom.configMapKeyRef` | Application settings shared across Pods          |
| Secret               | `valueFrom.secretKeyRef`    | Sensitive data (passwords, tokens, certificates) |

***

## 4. References

* [Kubernetes: Assign Environment Variables to Containers](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/)
* [Docker Environment Variables](https://docs.docker.com/engine/reference/run/#env-environment-variables)
* [ConfigMap Documentation](https://kubernetes.io/docs/concepts/configuration/configmap/)
* [Secrets Documentation](https://kubernetes.io/docs/concepts/configuration/secret/)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/d9358627-4fc7-4acc-ab96-fa25232555c6/lesson/af5b907c-f817-4e5e-92a7-76f3644ffd57)
