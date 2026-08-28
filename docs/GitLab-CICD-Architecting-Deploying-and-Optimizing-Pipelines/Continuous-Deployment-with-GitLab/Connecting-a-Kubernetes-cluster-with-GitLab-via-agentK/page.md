# You should see "STATUS: deployed"
helm status kk-gitlab-agent -n gitlab-agent-kk-gitlab-agent
```

## 5. Inspect Deployed Resources

Check pods, deployments, replica sets, config maps, and secrets:

```bash theme={null}
kubectl -n gitlab-agent-kk-gitlab-agent get all
kubectl -n gitlab-agent-kk-gitlab-agent get configmap,secrets,ingress
```

Retrieve the agent token secret in YAML:

```bash theme={null}
kubectl -n gitlab-agent-kk-gitlab-agent get secret kk-gitlab-agent-token -o yaml
```

## 6. Confirm Connection in GitLab

Return to **Operate** → **Kubernetes clusters** in your project and refresh.\
The cluster’s **Connection Status** should now display **Connected** and active.

<Frame>
  ![The image shows a GitLab interface displaying Kubernetes cluster details, including connection status, version, and configuration options. There's also a notification about Google Cloud Platform credits and a feedback section.](https://kodekloud.com/kk-media/image/upload/v1752877180/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Configure-Gitlab-Agent/gitlab-kubernetes-cluster-details.jpg)
</Frame>

<Callout icon="lightbulb">
  By default, GitLab applies the agent’s built-in config. To customize it, create a file at:

  ```text theme={null}
  .gitlab/agents/kk-gitlab-agent/config.yaml
  ```

  Refer to the [official documentation](https://docs.gitlab.com/ee/user/clusters/agent/) for configuration options.
</Callout>

## Next Steps

* Define a custom `config.yaml` to enable GitOps and environment deployments
* Create and annotate environments to surface cluster metrics in the GitLab UI

Happy deploying!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/df17ec22-8cda-4af7-af44-10f9f061d4a8/lesson/2efda6da-1fe0-4af8-93cc-88e1e6add6b4" />
</CardGroup>


# Connecting a Kubernetes cluster with GitLab via agentK

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Continuous-Deployment-with-GitLab/Connecting-a-Kubernetes-cluster-with-GitLab-via-agentK/page

This guide explains how to use GitLab Kubernetes Agent for secure connectivity between Kubernetes clusters and GitLab, simplifying CI/CD processes.

In this guide, you’ll learn how to leverage the GitLab Kubernetes Agent (AgentK) for secure, bi-directional connectivity between your Kubernetes clusters and GitLab. AgentK eliminates the need to store raw Kubeconfig credentials in CI/CD variables, simplifies firewall/NAT traversal, and lays the foundation for GitOps-style workflows.

## Why Use the GitLab Kubernetes Agent?

Traditionally, CI/CD pipelines use a stored Kubeconfig file to authenticate against Kubernetes. However:

* Kubeconfig files contain sensitive data (API server URL, tokens, certificates).
* Storing them as masked variables still poses a risk if compromised.
* Connecting to clusters behind firewalls or NAT gateways can be complex.

AgentK solves these challenges by initiating an outbound gRPC connection to GitLab’s Agent Server (KAS), enabling:

* Secure, credential-free communication
* Firewall/NAT traversal without port forwarding
* Bi-directional streaming for push and pull operations

<Callout icon="lightbulb">
  AgentK is a lightweight pod running inside your cluster. It uses a token-based handshake with KAS to establish a persistent, encrypted channel—removing the need for direct API server exposure.
</Callout>

<Frame>
  ![The image is a diagram illustrating the GitLab Kubernetes Agent architecture, showing the interaction between the GitLab server, CI/CD variables, pipelines, and multiple Kubernetes environments (dev, prod, staging) via gRPC bidirectional streaming.](https://kodekloud.com/kk-media/image/upload/v1752877181/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Connecting-a-Kubernetes-cluster-with-GitLab-via-agentK/gitlab-kubernetes-agent-architecture-diagram.jpg)
</Frame>

## Prerequisites

* A GitLab account with **Maintainer** or **Owner** access.
* A GitLab project to register the agent and store its configuration.
* A Kubernetes cluster v1.17+ (AgentK compatibility).
* `helm` CLI installed locally.

## 1. Register the GitLab Agent

1. In your GitLab project, navigate to **Operate > Kubernetes clusters**.
2. Click **Add Kubernetes cluster** and choose **GitLab Agent**.
3. Provide a unique **Agent name**.
4. GitLab will display a token and the Helm commands required for installation.

## 2. Install AgentK via Helm

Copy the Helm commands from the GitLab UI and execute them with your token:

```bash theme={null}
helm repo add gitlab https://charts.gitlab.io
helm repo update

helm upgrade --install my-agent gitlab/gitlab-agent \
  --namespace gitlab-agent \
  --create-namespace \
  --set config.token=<YOUR_AGENT_TOKEN> \
  --set config.kasAddress=wss://kas.gitlab.com \
  --set image.tag=v16.9.0
```

<Callout icon="triangle-alert">
  Keep your `<YOUR_AGENT_TOKEN>` secret. Rotate the token if it is ever exposed.
</Callout>

After installation, AgentK will connect to GitLab automatically. You should see the agent status under **Operate > Kubernetes clusters**.

## 3. Configure the Agent

AgentK’s behavior is defined in your project’s repository at `.gitlab/agent/<agent-name>/config.yaml`. Customize this file to control deployments, security, and remote workspaces.

```yaml theme={null}
gitops:
  # Projects containing Kubernetes manifests to deploy
  manifest_projects:
    - id: gitlab-org/my-project
      default_namespace: production

  # Which projects can trigger CI/CD through this agent
  ci_access:
    projects:
      - id: gitlab-org/my-project
