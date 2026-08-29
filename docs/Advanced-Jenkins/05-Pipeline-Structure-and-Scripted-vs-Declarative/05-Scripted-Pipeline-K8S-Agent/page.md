# Scripted Pipeline K8S Agent

Source: https://notes.kodekloud.com/docs/Advanced-Jenkins/Pipeline-Structure-and-Scripted-vs-Declarative/Scripted-Pipeline-K8S-Agent/page

Guide to running scripted Jenkins Pipeline stages inside Kubernetes pods using podTemplate and containerTemplate, sharing files with stash/unstash, and mixing static agents with ephemeral pod agents

This lesson shows how to run scripted Jenkins Pipeline stages inside Kubernetes pods using the Jenkins Kubernetes plugin. In declarative pipelines you typically use `agent { kubernetes { ... } }` to provision pods automatically. In scripted pipelines, you get the same behavior with `podTemplate` and `containerTemplate` constructs.

You will learn how to:

* define pod and container templates (either in the Jenkins cloud configuration or inline in the Jenkinsfile),
* run specific stages inside a Kubernetes pod container with `container('<name>')`,
* share files between a static agent and a Kubernetes pod using `stash`/`unstash`.

The examples below demonstrate using multiple containers in the same pod, configuring pod templates from the Jenkins UI, and mixing static agents with ephemeral Kubernetes pod agents.

## Example: podTemplate with multiple containers

The snippet below (from the [Kubernetes plugin examples](https://plugins.jenkins.io/kubernetes/)) shows a `podTemplate` that defines two container templates (`maven` and `golang`) and how to run different stages inside those containers using `container(...)`:

```groovy theme={null}
podTemplate(
    agentContainer: 'maven',
    agentInjection: true,
    containers: [
        containerTemplate(name: 'maven', image: 'maven:3.9.9-eclipse-temurin-17'),
        containerTemplate(name: 'golang', image: 'golang:1.16.5', command: 'sleep', args: '99d')
    ]) {

    node(POD_LABEL) {
        stage('Get a Maven project') {
            git 'https://github.com/jenkinsci/kubernetes-plugin.git'
            container('maven') {
                stage('Build a Maven project') {
                    sh 'mvn -B -ntp clean install'
                }
            }
        }

        stage('Get a Golang project') {
            git url: 'https://github.com/hashicorp/terraform.git', branch: 'main'
            container('golang') {
                stage('Build a Go project') {
                    sh '''
mkdir -p /go/src/github.com/hashicorp
ln -s `pwd` /go/src/github.com/hashicorp/terraform
cd /go/src/github.com/hashicorp/terraform && make
'''
                }
            }
        }
    }
}
```

Key points from this example:

* `podTemplate` wraps the `node(POD_LABEL)` block that runs inside the pod.
* Use `container('<name>')` to run commands inside a specific container in the pod.
* You can run different parts of your build in different containers within the same pod (e.g., build and test toolchains).

## Define pod templates in the Jenkins UI (recommended for reuse)

You can define pod templates at the cloud level in Jenkins. This is recommended when you want to reuse the same pod definition across multiple pipelines. Below is the Jenkins Cloud UI where you can add Pod Templates for a Kubernetes cloud.

<Frame>
  <img alt="Screenshot of the Jenkins &#x22;Clouds&#x22; settings page in dark theme showing one configured cloud named &#x22;dasher-prod-k8s-us-east.&#x22; A &#x22;New cloud&#x22; button and a gear/settings icon for the listed cloud are also visible." />
</Frame>

If you use the Jenkins UI to create pod templates, the [Pipeline Syntax (Snippet Generator)](https://www.jenkins.io/doc/book/pipeline/syntax/#using-the-snippet-generator) can generate the corresponding Groovy snippet. The generated script includes many optional fields — you can keep only the fields you need (cloud name, pod label, container name, image, `command`, `args`, TTY, privileged, etc.).

Here we set the cloud, label, namespace, and add a `node-18` container template via the Pipeline Syntax UI:

<Frame>
  <img alt="A dark-themed Jenkins Pipeline Syntax page showing a Kubernetes podTemplate configuration with fields like &#x22;Cloud to use&#x22; (dasher-prod-k8s-us-east), &#x22;Label&#x22; (nodejs-pod), namespace and name. The left sidebar displays links to documentation and examples." />
</Frame>

Additional Pod Template options such as supplemental groups, pod retention, working directory, and workspace volumes can be tuned to your needs:

<Frame>
  <img alt="A dark-themed web UI screenshot (Jenkins Pipeline Syntax for a k8s cloud agent) showing form fields like Supplemental Groups, time to retain agent when idle, Pod deadline, Service Account, Node Selector, working directory (/home/jenkins/agent) and workspace volume." />
</Frame>

## Compact inline podTemplate example

If you choose to inline a pod template inside your Jenkinsfile, here is a compact snippet that targets a cloud named `dasher-prod-k8s-us-east` and creates a pod labeled `nodejs-pod` with a `node-18` container:

```groovy theme={null}
podTemplate(
  cloud: 'dasher-prod-k8s-us-east',
  label: 'nodejs-pod',
  containers: [
    containerTemplate(
      args: '9999999',
      command: 'sleep',
      image: 'node:18-alpine',
      name: 'node-18',
      privileged: true,
      ttyEnabled: true
    )
  ]
) {
    // pipeline node blocks go inside this closure
}
```

Place `podTemplate` at the root of your scripted pipeline. The closure created by `podTemplate { ... }` must wrap any `node` blocks that should use that pod template.

## Mixing a static agent and a Kubernetes pod (stash/unstash example)

A common pattern is to use a static agent to perform checkout and build/cache dependencies, then use a Kubernetes pod for running tests. The static agent can build `node_modules`, `stash` them, and the pod can `checkout scm` again (required when switching agents) and `unstash` the dependencies before running tests.

> **lightbulb** In scripted pipelines, `checkout scm` happens only on the node where it is invoked. If you run stages on multiple, different agents (or pods), you must explicitly run `checkout scm` on each agent that needs access to the workspace files.

Warning: stashing large directories may slow your pipeline. Use caching (e.g., external caches or the `cache` step if available) to reduce transfer time and keep stashes minimal.

> **warning** Stashing large dependency directories (like `node_modules`) can be slow and may hit size limits. Prefer build caches or selective stashing (only what’s necessary) to optimize pipeline performance.

Below is a full minimal Jenkinsfile that demonstrates using an inline `podTemplate`, a static agent for checkout and `npm install`, then a Kubernetes pod container (`node-18`) for running unit tests with `unstash`.

```groovy theme={null}
// Use the pod template (inline). This wraps the pipeline nodes that use this pod.
podTemplate(
  cloud: 'dasher-prod-k8s-us-east',
  label: 'nodejs-pod',
  containers: [
    containerTemplate(
      args: '9999999',
      command: 'sleep',
      image: 'node:18-alpine',
      name: 'node-18',
      privileged: true,
      ttyEnabled: true
    )
  ]
) {

  // Static agent (e.g., an Ubuntu Docker node) to perform checkout and install dependencies
  node('ubuntu-docker-jdk17-node20') {
    env.NODEJS_HOME = "${tool 'nodejs-22-6-0'}"
    env.PATH = "${env.NODEJS_HOME}/bin:${env.PATH}"
    env.MONGO_URI = "mongodb+srv://supercluster.d83jj.mongodb.net/superData"

    stage('Checkout') {
      checkout scm
    }

    wrap([$class: 'TimestamperBuildWrapper']) {
      stage('Installing Dependencies') {
        // Use a build cache (if configured) and stash node_modules for reuse in other agents
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
          stash(includes: 'node_modules/**', name: 'solar-system-node-modules')
        }
      }
    }
  }

  // Run unit tests inside the Kubernetes pod (container name node-18)
  node('nodejs-pod') {
    container('node-18') {
      stage('Unit Testing') {
        // Checkout is required here because this node is a different agent (K8s pod)
        checkout scm

        // Restore node_modules that were built on the static agent
        unstash 'solar-system-node-modules'

        withCredentials([usernamePassword(credentialsId: 'mongo-db-credentials', usernameVariable: 'MONGO_USER', passwordVariable: 'MONGO_PASSWORD')]) {
          sh 'node -v'
          sh 'npm test'
        }
      }
    }
  }
}
```

## Quick reference

| Concept                        | Purpose                                                | Example                                                                                                           |
| ------------------------------ | ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| Define pod template            | Reuse pod definitions across pipelines                 | `podTemplate(cloud: 'dasher-prod-k8s-us-east', label: 'nodejs-pod', ...)`                                         |
| Run inside specific container  | Execute commands in a container inside the pod         | `container('node-18') { sh 'npm test' }`                                                                          |
| Switch agents                  | Run stages on different agents (static vs pod)         | `node('ubuntu-docker-jdk17-node20') { ... }` then `node('nodejs-pod') { ... }`                                    |
| Share artifacts between agents | Transfer files from producing agent to consuming agent | `stash(includes: 'node_modules/**', name: 'solar-system-node-modules')` and `unstash 'solar-system-node-modules'` |
| Required per-agent checkout    | Ensure repo files are available on each agent          | `checkout scm` inside each `node(...)` block that needs the workspace                                             |

## Key takeaways

* Pod templates can be configured at the cloud level (recommended for reuse) or inline in the Jenkinsfile.
* Use the `label` from the pod template in `node('<label>')` to run steps inside that pod.
* Use `container('<container-name>')` inside `node` to execute commands inside a specific container in the pod.
* In scripted pipelines, `checkout scm` is not automatic for every agent — explicitly run `checkout scm` on any agent that needs repository files.
* To share files between agents, use `stash` on the producing agent and `unstash` on the consuming agent.
* Combining static agents and Kubernetes pods gives you consistent setup for build/caching and dynamic, disposable environments for running tests.

Further reading and references:

* [Kubernetes plugin for Jenkins](https://plugins.jenkins.io/kubernetes/)
* [Jenkins Pipeline Syntax (Snippet Generator)](https://www.jenkins.io/doc/book/pipeline/syntax/#using-the-snippet-generator)
* [Jenkins Pipeline: Stash and Unstash](https://www.jenkins.io/doc/pipeline/steps/workflow-basic-steps/#stash-stash-files-for-later-use)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-jenkins/module/cffedc7a-8318-433c-83ff-5ec8f272486f/lesson/cb96f010-03c3-42fc-a8be-6d58ee742f1c)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/advanced-jenkins/module/cffedc7a-8318-433c-83ff-5ec8f272486f/lesson/6578e055-38f1-45eb-b447-773d0f3e2fea)
