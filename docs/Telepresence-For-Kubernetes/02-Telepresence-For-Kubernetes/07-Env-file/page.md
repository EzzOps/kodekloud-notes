# prod.db
```

You now have file-based access to the ConfigMap data.

## Customizing the Local Mount Path

1. End the current intercept:
   ```bash theme={null}
   telepresence leave products-depl
   ```
2. Start a new intercept with a custom mount location:
   ```bash theme={null}
   telepresence intercept products-depl \
     --port 8000 \
     --env-file .env \
     --mount=/tmp/example123
   ```

Files now appear under `/tmp/example123/tmp`:

```bash theme={null}
cd /tmp/example123/tmp
ls
# DB_HOST  DB_PASSWORD  DB_USERNAME
```

Adjust your application or use symbolic links to consume these local files seamlessly.

## References

* [Telepresence Documentation](https://www.telepresence.io/docs/)
* [Kubernetes ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/)
* [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
* [Express.js Guide](https://expressjs.com/en/starter/installing.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/telepresence-for-kubernetes/module/0eb5dcb6-2e2a-40d9-9caa-bd3149741aeb/lesson/c92e854c-3059-4a2d-9082-e9c021269560)


# Env file

Source: https://notes.kodekloud.com/docs/Telepresence-For-Kubernetes/Telepresence-For-Kubernetes/Env-file/page

This guide explains how to capture and reuse environment variables from a Kubernetes container using Telepresence.

In this guide, we’ll show you how to capture and reuse environment variables from a remote Kubernetes container when intercepting a service with Telepresence. By exporting these variables into a local `.env` file, you ensure your local process runs with the exact same configuration as in the cluster.

## 1. Intercept the Remote Service

Suppose you have a `products` service deployed in your Kubernetes cluster. To forward traffic from that service to your local machine, run:

```bash theme={null}
telepresence intercept products-depl --port 8000:3000
```

This command maps remote port `3000` to your local port `8000`, but it doesn’t pull in any environment variables by default.

## 2. Inspect the Deployment’s Environment Variables

Your Kubernetes deployment might define variables like this:

```yaml theme={null}
spec:
  containers:
    - name: products
      image: sanjeevkt720/telepresence-products
      ports:
        - containerPort: 3000
          name: web
      env:
        - name: API_URL
          value: http://inventory-service:3000/
        - name: LOG_LEVEL
          value: debug
```

When you run your service locally, it needs access to `API_URL`, `LOG_LEVEL`, and any other container-specific settings.

## 3. Generate a Local `.env` File

Telepresence can automatically dump all container environment variables into a file. Simply add the `--env-file` flag to your intercept command:

```bash theme={null}
telepresence intercept products-depl \
  --port 8000:3000 \
  --env-file .env
```

After the command runs, you’ll find a `.env` file in your current directory containing:

```dotenv theme={null}
API_URL=http://inventory-service:3000/
LOG_LEVEL=debug
