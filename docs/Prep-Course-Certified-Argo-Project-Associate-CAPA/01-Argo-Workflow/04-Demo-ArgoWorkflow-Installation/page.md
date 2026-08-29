# Demo ArgoWorkflow Installation

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/Demo-ArgoWorkflow-Installation/page

Guide to install and configure Argo Workflows on Kubernetes, expose the Argo Server, install the Argo CLI, and run example workflows.

In this lesson you'll install Argo Workflows into a Kubernetes cluster, expose the Argo Server for local access, and install the matching `argo` CLI so you can interact with the server and run workflows.

Start by opening the Argo Workflows documentation and navigating to the Getting Started page.

<Frame>
  <img alt="A browser screenshot of the Argo Workflows documentation homepage, showing the header/navigation and a main article titled &#x22;What is Argo Workflows?&#x22; with bullet points and a right-hand table of contents." />
</Frame>

## 1. Choose a release and install the quick-start

Pick an Argo Workflows release (this guide uses v3.7.3). The quick-start minimal manifest creates the Workflow Controller, Argo Server, example services (httpbin), bundled MinIO artifact store, and the required CRDs.

Commands to install:

```bash theme={null}
