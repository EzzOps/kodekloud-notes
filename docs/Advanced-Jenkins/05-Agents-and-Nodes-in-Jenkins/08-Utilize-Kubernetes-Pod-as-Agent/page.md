# Utilize Kubernetes Pod as Agent

Source: https://notes.kodekloud.com/docs/Advanced-Jenkins/Agents-and-Nodes-in-Jenkins/Utilize-Kubernetes-Pod-as-Agent/page

Using Kubernetes pods as ephemeral Jenkins Pipeline build agents, with inline YAML or pod templates, multi container examples, pod selection, inspection, retention, and best practices

In this guide you'll learn how to use Kubernetes pods as ephemeral build agents for Jenkins Pipeline jobs. We'll use a configured Kubernetes cloud and Declarative Pipeline `kubernetes` agents that provision pods on demand. Examples show inline Pod YAML embedded in the pipeline; you can also use reusable pod templates configured in the Kubernetes cloud.

<Frame>
  <img alt="A screenshot of the Jenkins &#x22;Clouds&#x22; settings page in dark mode showing one configured cloud entry named &#x22;dasher-prod-k8s-us-east&#x22; and a &#x22;New cloud&#x22; button. The top bar shows the Jenkins logo, search, and user menu." />
</Frame>

## Create the Pipeline Job

Create a new Pipeline job: Dashboard → New Item → Pipeline. For the examples below we use Declarative Pipeline syntax with an inline YAML Pod definition inside the `agent { kubernetes { yaml '''...''' }}` block.

## Basic single-container example

This example demonstrates a minimal pod with a single Ubuntu container. The container runs `sleep infinity` so the pod remains available briefly for inspection while the build runs. We set `defaultContainer` so pipeline steps execute in that container unless overridden.

```groovy theme={null}
// Uses Declarative syntax to run commands inside a container.
pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: ubuntu-container
    image: ubuntu
    command:
    - sleep
    args:
    - "infinity"
'''
            defaultContainer 'ubuntu-container'
            retries 2
        }
    }
    stages {
        stage('Print Hostname') {
            steps {
                sh 'hostname'
                sh 'sleep 120s' // keep the pod alive briefly for inspection
            }
        }
    }
}
```

> **lightbulb** Pod retention: If the Kubernetes cloud's Pod Retention is set to `Never`, pods created for builds are deleted immediately when the build finishes. If you need to inspect a pod after a run, set retention appropriately or adjust the pipeline to pause before completion.

<Frame>
  <img alt="A screenshot of a dark-themed Jenkins &#x22;Configure&#x22; page for a Kubernetes cloud (dasher-prod-k8s-us-east) showing pod-related settings. Visible fields include &#x22;Pod Retention&#x22; set to &#x22;Never,&#x22; &#x22;Max connections to Kubernetes API&#x22; = 32, &#x22;Seconds to wait for pod&#x22; = 600, &#x22;Container Cleanup Timeout&#x22; = 5, and a Save button." />
</Frame>

When the pipeline runs, Jenkins prints the generated Pod spec to the console and executes the stage inside the provisioned pod. Example console output:

```text theme={null}
Running on k8s-cloud-agent-demo-1-36qw9-qdg7z-3mc58 in /home/jenkins/agent/workspace/k8s-cloud-agent-demo
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Print Hostname)
[Pipeline] sh
+ hostname
k8s-cloud-agent-demo-1-36qw9-qdg7z-3mc58
[Pipeline] sh
+ sleep 120s
```

## Pod templates vs inline YAML

You can either:

* Define pod templates in the Kubernetes cloud configuration (reusable, managed centrally), or
* Provide inline YAML in the pipeline (convenient for per-job customization).

For CI consistency, many teams store common pod templates in the cloud configuration and reference them from pipelines. For demos or job-specific requirements, inline YAML is quick and flexible.

<Frame>
  <img alt="A Jenkins web UI screenshot showing the &#x22;dasher-prod-k8s-us-east - Pod templates&#x22; page with no templates added and a prominent blue &#x22;Add a pod template&#x22; button. The left sidebar shows navigation items like Status, Pod Templates, Configure, and Delete Cloud." />
</Frame>

## Selecting the Kubernetes cloud

If multiple Kubernetes clouds are configured, explicitly select one using the `cloud` option inside the `kubernetes` agent block. If omitted, the plugin uses the first configured Kubernetes cloud.

The Pipeline editor / directives UI exposes fields like `Cloud to use`, `Namespace`, and `Default container` to help configure these options.

<Frame>
  <img alt="A dark-themed screenshot of a Jenkins web UI showing the &#x22;k8s-cloud-agent-demo&#x22; Directives page with a Sample Directive for the agent set to &#x22;kubernetes.&#x22; The form shows fields like &#x22;Cloud to use,&#x22; &#x22;Namespace,&#x22; and &#x22;Default container&#x22; for configuring a Kubernetes agent." />
</Frame>

<Frame>
  <img alt="A dark-themed screenshot of a Jenkins web UI showing a Kubernetes cloud/agent configuration form with fields like Namespace, Default container, Pod template to inherit from, and Raw YAML for the Pod. The browser tabs and address bar are visible at the top." />
</Frame>

## Multi-container pod example

To run different runtimes in the same pod (for example, a utility container with Node.js and a separate container for the agent), define multiple containers in the Pod YAML. Use `defaultContainer` to make most steps run in one container, and use the `container('name') { ... }` block to target a different container for specific steps.

Below is a pipeline that provisions two containers: `ubuntu-container` (default) and `node-container`. The `Print Node Version` stage runs explicitly inside `node-container` to access `node` and `npm`.

```groovy theme={null}
pipeline {
    agent {
        kubernetes {
            cloud 'dasher-prod-k8s-us-east'
            yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: node-container
    image: node:18-alpine
    command:
    - cat
    tty: true
  - name: ubuntu-container
    image: ubuntu
    command:
    - sleep
    args:
    - "infinity"
'''
            defaultContainer 'ubuntu-container'
            retries 2
        }
    }

    stages {
        stage('Print Hostname') {
            steps {
                sh 'hostname'
            }
        }

        stage('Print Node Version') {
            steps {
                // run these commands in the node-container
                container('node-container') {
                    sh 'node -v'
                    sh 'npm -v'
                }
            }
        }
    }
}
```

What goes wrong if you don't target the right container?

* If the `defaultContainer` lacks the runtime you need (e.g., `node`), steps will fail with `node: not found`. Always target the correct container with `container('name') { ... }` when you need a specific runtime.

Example failure when `node` is executed in the Ubuntu default container (console output, cleaned):

```text theme={null}
[Pipeline] sh
+ node -v
/home/jenkins/agent/workspace/.../script.sh.copy: 1: node: not found
```

Correct run when targeting the Node container (cleaned console output):

```text theme={null}
[Pipeline] sh
+ node -v
v18.20.4
[Pipeline] sh
+ npm -v
10.7.0
```

## Inspecting pods and events from the cluster

While a job is running, inspect Pod status, logs and cluster events with kubectl. Example assumes the Jenkins namespace is `jenkins`.

```bash theme={null}
