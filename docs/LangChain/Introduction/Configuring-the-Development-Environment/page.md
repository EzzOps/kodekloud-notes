# DB_PASSWORD=password1
```

<Callout icon="triangle-alert">
  Kubernetes does **not** automatically redeploy pods when a referenced ConfigMap or Secret is updated. You must manually trigger a restart.
</Callout>

## Manual Rollout Restart

To pick up the new password, force a rollout restart of the deployment:

```bash theme={null}
kubectl rollout restart deployment nginx-deployment
```

Watch for the new pod:

```bash theme={null}
kubectl get pods
```

Verify the updated environment variable:

```bash theme={null}
NEW_POD=$(kubectl get pods -l component=nginx -o jsonpath="{.items[0].metadata.name}")
kubectl exec "$NEW_POD" -- printenv | grep -i db
# DB_PASSWORD=password2
```

## Common Kubectl Commands

| Command                                     | Purpose                              |
| ------------------------------------------- | ------------------------------------ |
| `kubectl apply -f configmap.yaml`           | Create or update a ConfigMap         |
| `kubectl apply -f deployment.yaml`          | Create or update a Deployment        |
| `kubectl get pods`                          | List all pods                        |
| `kubectl exec <pod> -- printenv`            | Inspect environment variables in pod |
| `kubectl rollout restart deployment <name>` | Restart pods to pick up changes      |

## The Challenge

Every time a ConfigMap or Secret changes, Kubernetes leaves existing pods untouched. Manually restarting each deployment can become error-prone at scale.

In the next section, we’ll introduce config generators to automate this process, ensuring your applications always run with the latest configuration.

## References

* [Kubernetes ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/)
* [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/)
* [kubectl rollout restart](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#rollout)
* [Kubernetes Documentation](https://kubernetes.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kustomize/module/51823d3e-7be4-4792-836a-2c4690c0c547/lesson/1481509c-b71c-4836-8e1b-d55117f5c673" />
</CardGroup>


# Configuring the Development Environment

Source: https://notes.kodekloud.com/docs/LangChain/Introduction/Configuring-the-Development-Environment/page

Guide to configuring a local Python environment for using the OpenAI API including installing Python and packages, creating and exporting an API key, and testing with curl and Jupyter

This guide walks through configuring a local Python development environment to experiment with the OpenAI API. The steps work whether you’re using a pre-configured environment (e.g., KodeKloud) or your own workstation.

Quick overview of the setup flow:

1. Install Python (3.10+).
2. Create and activate a Python virtual environment.
3. Install required Python packages (`openai` and `jupyter`).
4. Create an OpenAI API key and export it as an environment variable.
5. Test the API from the command line (curl).
6. Test the API from a Python Jupyter notebook.

<Frame>
  <img alt="The image outlines six steps for setting up a Python environment to work with OpenAI and Jupyter, including installing Python and PIP, creating a virtual environment, installing necessary modules, obtaining an API key, setting an environment variable, and testing the setup." />
</Frame>

For quick reference, here’s a condensed table of common commands used in this guide:

| Task                             | Command / Notes                                     |
| -------------------------------- | --------------------------------------------------- |
| Verify Python                    | `python -V`                                         |
| Create venv (Unix/macOS/Windows) | `python -m venv venv`                               |
| Activate venv (macOS/Linux)      | `source venv/bin/activate`                          |
| Activate venv (PowerShell)       | `.\venv\Scripts\Activate.ps1`                       |
| Install packages                 | `pip install openai jupyter`                        |
| Export API key (bash)            | `export OPENAI_API_KEY="sk-REDACTED-YOUR-KEY-HERE"` |
| Temp set API key (PowerShell)    | `$env:OPENAI_API_KEY = "sk-REDACTED-YOUR-KEY-HERE"` |
| Start Jupyter                    | `jupyter notebook`                                  |

## 1) Install Python

Download and install Python 3.10 or later from the official site: [https://www.python.org/downloads/](https://www.python.org/downloads/). Choose the installer that matches your OS (Windows, macOS, Linux).

Example usage (can be run in the Python REPL or a script):

```python theme={null}
