# InstallationSetup

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/2025-Updates-Kustomize-Basics/InstallationSetup/page

This guide explains how to install and configure Kustomize for customizing Kubernetes configurations.

In this guide, you'll learn how to install and configure Kustomize—a powerful tool for customizing Kubernetes configurations. Before you begin, ensure that you have the following prerequisites:

* A running Kubernetes cluster.
* [kubectl](https://kubernetes.io/docs/reference/kubectl/overview/) installed on your local machine and configured to connect to your cluster.
* A compatible operating system (Linux, Windows, or macOS).

The Kustomize installation script automatically detects your operating system and installs the appropriate version.

## Installing Kustomize

To install Kustomize, open your terminal and execute the command below. This command downloads and runs the installation script:

```bash theme={null}
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash
```

Once the installation is complete, verify the installation by running:

```bash theme={null}
kustomize version --short
```

You should see an output similar to the following:

```bash theme={null}
{kustomize/v4.4.1 2021-11-11T23:36:27Z}
```

<Callout icon="lightbulb">
  If you do not see the expected output or if you encounter any issues, it may be due to environment variables not being updated in your current terminal session. Close and reopen your terminal, then try the verification step again.
</Callout>

<Callout icon="triangle-alert">
  If problems persist after restarting your terminal, re-run the installation script to ensure that Kustomize is correctly set up.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/2503ab74-a871-4b65-a677-7180c001d5c5/lesson/14461618-374d-4ca2-983d-5ef86944661d" />
</CardGroup>
