# Demo Scripted Pipeline K8S Agent

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Pipeline-Structure-and-Scripted-vs-Declarative/Demo-Scripted-Pipeline-K8S-Agent/page

Explains running scripted Jenkins pipelines with Kubernetes agents, defining pod templates, handling explicit checkouts, and transferring dependencies using stash and unstash.

This lesson shows how to run scripted Jenkins pipeline stages inside Kubernetes pods using the Jenkins Kubernetes plugin. Unlike declarative pipelines where an `agent` block often handles checkout and workspace for you, scripted pipelines require more explicit control: define pod templates, manage checkouts on each node, and transfer artifacts between agents with `stash`/`unstash`.

You will learn:

* How to define a Kubernetes pod via `podTemplate` and `containerTemplate`.
* How to run some stages on a static Jenkins agent and other stages inside Kubernetes containers.
* How to move installed dependencies (for example `node_modules`) between agents using `stash`/`unstash`.

## Inline podTemplate example

Below is a pod template you can generate from Jenkins "Pipeline Syntax" and then simplify for use inside a Jenkinsfile. This example defines a pod with two Node.js container templates:

```groovy theme={null}
podTemplate(
  cloud: 'dasher-prod-k8s-us-east',
  label: 'nodejs-pod',
  containers: [
    containerTemplate(
      name: 'node-18',
      image: 'node:18-alpine',
      command: 'sleep',
      args: '9999999',
      ttyEnabled: true,
      privileged: true
    ),
    containerTemplate(
      name: 'node-19',
      image: 'node:19-alpine',
      command: 'sleep',
      args: '9999999',
      ttyEnabled: true,
      privileged: true
    )
  ]
) {
  // node(POD_LABEL) { ... } will be added by the pipeline below where needed
}
```

Explanation:

* `cloud` selects the Kubernetes cloud configured in Jenkins.
* `label` is the pod label that binds a Jenkins `node(...)` to this pod template.
* Each `containerTemplate` becomes a container inside the created pod. Using `sleep` keeps the container alive while the Jenkins agent communicates with it.

You can also configure these pod templates at the cloud level in the Jenkins UI so they are reusable across pipelines:

<Frame>
  <img alt="A screenshot of the Jenkins web UI on the &#x22;Clouds&#x22; page showing one configured cloud named &#x22;dasher-prod-k8s-us-east&#x22; and a &#x22;+ New cloud&#x22; button. The page header and navigation are visible across the top." />
</Frame>

### Use the "Pipeline Syntax" generator

To produce the initial Groovy block, use Jenkins' "Pipeline Syntax" generator. The form looks like this when creating a pod template for a cloud:

<Frame>
  <img alt="A dark-themed Jenkins Pipeline Syntax page showing a podTemplate configuration form with fields like &#x22;Cloud to use&#x22; (set to dasher-prod-k8s-us-east), Name, Namespace, Label (nodejs-pod), and usage/inheritance options. The browser window and several tabs are visible along the top." />
</Frame>

When adding container templates in the UI, make sure to set fields such as image, command, args, and allocate a TTY if required:

<Frame>
  <img alt="A dark-themed screenshot of a Jenkins Pipeline Syntax / k8s cloud agent configuration page showing container settings. It shows fields like Docker image &#x22;node:18-alpine&#x22;, command &#x22;sleep&#x22; with argument &#x22;9999999&#x22;, and the &#x22;Allocate pseudo-TTY&#x22; checkbox checked." />
</Frame>

The generator often emits a verbose, YAML-like Groovy snippet including probes and resource defaults. Trim it to the essentials: cloud, label, and containers with name, image, command, args, tty, and privileged flags as needed. For example:

```groovy theme={null}
podTemplate(
  cloud: 'dasher-prod-k8s-us-east',
  label: 'nodejs-pod',
  containers: [
    containerTemplate(
      name: 'node-18',
      image: 'node:18-alpine',
      command: 'sleep',
      args: '9999999',
      ttyEnabled: true,
      privileged: true
    )
  ]
) {
  // pipeline code that references node('nodejs-pod') and container('node-18') ...
}
```

Other pod-level settings (namespace, service account, volumes, workspace directory) can be configured at the cloud level or overridden inline:

<Frame>
  <img alt="A dark-themed screenshot of a web UI (Jenkins Pipeline Syntax / k8s cloud agent settings) showing various form fields. Visible fields include Supplemental Groups, time to retain agent when idle, Pod deadline, Service Account, Node Selector, Working directory (/home/jenkins/agent) and Workspace Volume." />
</Frame>

## Practical scripted Jenkinsfile pattern

This common pattern uses:

* A static Jenkins agent (e.g., long-lived Ubuntu/Docker executor) to perform checkout and install dependencies (fast, cache-friendly).
* `stash` on that agent to capture installed dependencies.
* A Kubernetes pod/container to run unit tests after `unstash`ing the artifacts and `checkout scm` on that node.

Full example Jenkinsfile (scripted pipeline):

```groovy theme={null}
// Jenkinsfile (scripted pipeline)
podTemplate(
  cloud: 'dasher-prod-k8s-us-east',
  label: 'nodejs-pod',
  containers: [
    containerTemplate(
      name: 'node-18',
      image: 'node:18-alpine',
      command: 'sleep',
      args: '9999999',
      ttyEnabled: true,
      privileged: true
    )
  ]
) {
  node('ubuntu-docker-jdk17-node20') { // static agent for heavy operations, checkout, caching
    // Tools and env setup on static node
    env.NODEJS_HOME = "${tool 'nodejs-22-6-0'}"
    env.PATH = "${env.NODEJS_HOME}/bin:${env.PATH}"
    env.MONGO_URI = "mongodb+srv://supercluster.d83jj.mongodb.net/superData"

    properties([])

    stage('Checkout') {
      checkout scm
    }

    wrap([$class: 'TimestamperBuildWrapper']) {
      stage('Installing Dependencies') {
        // Example cache wrapper (plugin-specific)
        cache(maxCacheSize: 550, caches: [
          arbitraryFileCache(
            cacheName: 'npm-dependency-cache',
            cacheValidityDecidingFile: 'package-lock.json',
            includes: '**/*',
            path: 'node_modules'
          )
        ]) {
          sh 'node -v'
          sh 'npm install --no-audit'
          // stash node_modules to transfer to the k8s container later
          stash(includes: 'node_modules/**', name: 'solar-system-node-modules')
        }
      }
    }
  }

  // Run Unit Testing inside the Kubernetes pod/container
  stage('Unit Testing') {
    // node label must match the podTemplate label defined above
    node('nodejs-pod') {
      // select the container inside that pod
      container('node-18') {
        // In scripted pipelines you must explicitly checkout when switching nodes/pods
        checkout scm

        // restore the dependencies
        unstash 'solar-system-node-modules'

        // Run tests
        sh 'node -v'
        sh 'npm test'
      }
    }
  }
}
```

<Callout icon="lightbulb">
  * In scripted pipelines, switching to a different agent/node (for example from a static agent to a Kubernetes pod via `node('label')`) does not carry over the workspace or checked-out files. Always run `checkout scm` on the node where you will execute build/test commands, or use `stash`/`unstash` to transfer files between agents.
  * `stash` the produced artifacts on the producer agent (where you installed dependencies) and `unstash` them on the consumer agent (the Kubernetes container) to make tools and dependencies available where they are needed.
</Callout>

## Common failure examples (and fixes)

1. Missing repository files on the Kubernetes container (ENOENT: package.json).\
   Cause: forgetting to `checkout scm` inside the k8s `node(...)` block. Failing log example:

```text theme={null}
+ node -v
v18.20.4

+ npm test
npm ERR! code ENOENT
npm ERR! syscall open
npm ERR! path /home/jenkins/agent/workspace/n_solar-system_pipeline_scripted/package.json
npm ERR! errno -2
npm ERR! enoent Could not read package.json Error: ENOENT: no such file or directory, open '/home/jenkins/agent/workspace/n_solar-system_pipeline_scripted/package.json'
npm ERR! enoent This is related to npm not being able to find a file.
```

Fix: run `checkout scm` on the same node/container where you invoke `npm test`.

2. Missing dev/test tools (e.g., mocha: not found).\
   Cause: dependencies were installed on a different agent and not transferred. Symptom: `sh: mocha: not found`.\
   Fix: `stash` node\_modules on the installing agent and `unstash` on the test agent, or install dependencies inside the test container.

<Callout icon="warning">
  Be mindful of stash size and limits: stashing large directories (e.g., entire build artifacts) may increase build time and storage use. Prefer caching plugins or artifact repositories for large dependencies. Also ensure workspace paths and ownership are compatible across agents (uid/gid differences can affect file access).
</Callout>

After adding `checkout scm` and `unstash` to the unit testing stage, the pipeline should successfully provision pods and run tests. Monitor pod provisioning, logs, and step output in the Jenkins UI (Blue Ocean or classic UI):

<Frame>
  <img alt="A Jenkins web dashboard showing the &#x22;Gitea-Organization / solar-system&#x22; pipeline activity with a table of recent builds (status, run number, commit, branch, message, duration, and completion time). The list shows green, red, and in-progress builds for branches like pipeline/scripted and feature/advanced-demo." />
</Frame>

When the pod is provisioned, Jenkins prints the generated Pod YAML and container details in the agent logs. Example snippet you may see in the console output:

```text theme={null}
Created Pod: dasher-prod-k8s-us-east jenkins/nodejs-pod-3tll4-11lvm
Agent nodejs-pod-3tll4-11lvm is provisioned from template nodejs-pod-3tll4
---
apiVersion: "v1"
kind: "Pod"
metadata:
  name: "nodejs-pod-3tll4-11lvm"
  namespace: "jenkins"
spec:
  containers:
  - name: "node-19"
    image: "node:19-alpine"
    command: ["sleep"]
    args: ["9999999"]
    tty: true
    securityContext:
      privileged: true
    volumeMounts:
    - mountPath: "/home/jenkins/agent"
      name: "workspace-volume"
  - name: "node-18"
    image: "node:18-alpine"
    command: ["sleep"]
    args: ["9999999"]
    tty: true
    securityContext:
      privileged: true
    volumeMounts:
    - mountPath: "/home/jenkins/agent"
      name: "workspace-volume"
  serviceAccount: "agent"
  volumes:
  - emptyDir: {}
    name: "workspace-volume"
```

## Quick reference table

| Field                   | Purpose                                       | Example                                            |
| ----------------------- | --------------------------------------------- | -------------------------------------------------- |
| cloud                   | Kubernetes cloud configured in Jenkins        | `dasher-prod-k8s-us-east`                          |
| label                   | Node label used by `node('label')`            | `nodejs-pod`                                       |
| containerTemplate.name  | Container identifier inside the pod           | `node-18`                                          |
| containerTemplate.image | Docker image for the container                | `node:18-alpine`                                   |
| command / args          | Command to keep container alive for the agent | `sleep` / `9999999`                                |
| ttyEnabled              | Allocate pseudo-TTY for interactive runs      | `true`                                             |
| stash / unstash         | Transfer files between agents                 | `stash(includes: 'node_modules/**', name: 'deps')` |

## Summary

* Use `podTemplate` and `containerTemplate` to define Kubernetes pods and containers for scripted pipelines.
* Reference the pod via `node('label')` and execute inside a container with `container('name')`.
* Always `checkout scm` or use `stash`/`unstash` when switching between different agents or pods.
* Define pod templates either inline in the Jenkinsfile (good for one-off pipelines) or in the Jenkins UI/cloud level (recommended for reuse).

## Links and References

* [Jenkins Kubernetes Plugin](https://plugins.jenkins.io/kubernetes/)
* [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Jenkins Documentation](https://www.jenkins.io/doc/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/956fce34-baa6-4655-a3cf-7b12d2364544/lesson/1d7d2201-c167-4e3c-951a-888cc6a54d36" />
</CardGroup>
