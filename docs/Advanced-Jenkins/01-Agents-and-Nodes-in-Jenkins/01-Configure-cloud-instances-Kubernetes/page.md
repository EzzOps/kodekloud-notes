# Configure cloud instances Kubernetes

Source: https://notes.kodekloud.com/docs/Advanced-Jenkins/Agents-and-Nodes-in-Jenkins/Configure-cloud-instances-Kubernetes/page

Guide to configure Jenkins Kubernetes cloud for dynamic agent pods, covering plugin installation, least privilege credentials, RBAC, pod templates, connection options, testing, and troubleshooting.

In this lesson you will configure a Kubernetes cloud in Jenkins so Jenkins can dynamically spin up agent pods. This guide covers plugin installation, credential setup (least-privilege), RBAC, and common troubleshooting tips.

Open the Jenkins UI and navigate to Manage Jenkins to begin configuring a cloud.

<Frame>
  <img alt="A dark-themed Jenkins web dashboard showing a table of CI jobs with status icons, last success/failure times, and durations. The left sidebar contains navigation links and the top bar shows a search field and user account controls." />
</Frame>

## 1. Install the Kubernetes plugin

Go to Manage Jenkins -> Manage Plugins and install the plugin that provides Kubernetes cloud support.

<Frame>
  <img alt="A screenshot of the Jenkins &#x22;Manage Plugins&#x22; -> &#x22;Available plugins&#x22; page showing a search for &#x22;Cloud Providers&#x22; and a list of plugins (Docker, Kubernetes, Amazon EC2, vSphere, Azure VM Agents) with descriptions and release timestamps. The left sidebar shows navigation items like Updates, Available plugins, Installed plugins, and Advanced settings." />
</Frame>

I selected the Kubernetes plugin. If you need a specific version, download the `.hpi` or use the `jenkins-plugin-cli` tool. Example local files from my machine:

```bash theme={null}
