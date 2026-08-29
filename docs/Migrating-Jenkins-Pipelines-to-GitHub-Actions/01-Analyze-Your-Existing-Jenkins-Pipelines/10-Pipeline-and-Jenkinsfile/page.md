# Pipeline and Jenkinsfile

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Analyze-Your-Existing-Jenkins-Pipelines/Pipeline-and-Jenkinsfile/page

Guide to Jenkins Pipelines and Jenkinsfile, explaining stages, steps, Declarative versus Scripted styles, examples, benefits over Freestyle jobs, and migration best practices

Let's take a concise tour of Jenkins Pipeline projects and the Jenkinsfile that defines them. This guide explains what a pipeline is, how stages and steps map to real work, the two Jenkinsfile styles (Declarative vs Scripted), and why modern CI/CD favors pipelines over Freestyle jobs.

A Jenkins Pipeline is a versioned, code-defined workflow for automating build, test, and deployment tasks. Think of it as a recipe for your CI/CD process—stages organize related work, steps are the commands you run, and parallel stages help speed up execution for independent tasks (for example, running linting and unit tests at the same time).

<Frame>
  <img alt="A Jenkins Pipeline diagram showing sequential stages. It lists Building, Unit Testing, Linting, Dockerizing, Security, Deployment, and Tests with purple icons." />
</Frame>

Key concepts

* Stage: a logical grouping of steps (e.g., Build, Test, Deploy).
* Step: an individual command or action executed within a stage.
* Agent: the executor where steps run (for example: `agent any`, `agent { docker { ... } }`).
* Parallel: run independent tasks concurrently to reduce overall pipeline duration.
* Jenkinsfile: the repository file that defines the pipeline using a Groovy-based DSL.

Example Declarative Jenkinsfile
Below is a simple Declarative Jenkinsfile that demonstrates a common four-stage pipeline: Build, Unit Test, Dockerize, and Deploy.

```groovy theme={null}
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'mvn package'
            }
        }
        stage('Unit Test') {
            steps {
                sh 'mvn test'
            }
        }
        stage('Dockerize') {
            steps {
                sh 'docker build -t imageName:version .'
                sh 'docker push imageName:version'
            }
        }
        stage('Deploy') {
            steps {
                sh 'kubectl apply -f deployment.yaml'
            }
        }
    }
}
```

Notes on this example:

* `agent any` instructs Jenkins to run the pipeline on any available agent.
* Each `stage` groups related `steps`—those `sh` shells could be replaced with plugin-provided steps.
* Store this `Jenkinsfile` alongside your application code so it is versioned with the project.

Why use a Jenkinsfile?

* Code-as-configuration: the pipeline lives in your repository and is reviewable.
* Portability: the same script can be run across different environments.
* Extensibility: plugins and shared libraries extend pipeline capabilities.
* Resilience: pipelines are designed to survive controller restarts and support manual approvals and human interactions.

Pipeline styles: Scripted vs Declarative

<Frame>
  <img alt="A slide titled &#x22;Types of Pipeline Projects&#x22; that compares two approaches: Scripted Pipeline on the left and Declarative Pipeline on the right. The Scripted column lists &#x22;Code Centric,&#x22; &#x22;Flexibility,&#x22; and &#x22;Learning Curve,&#x22; while the Declarative column lists &#x22;Human Readable,&#x22; &#x22;Easier to Learn,&#x22; and &#x22;Limited Complexity.&#x22;" />
</Frame>

Which style should you choose? Use the table below to compare the two.

| Style         | When to use                                                                   | Pros                                                   | Cons                                          |
| ------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------ | --------------------------------------------- |
| `Declarative` | Standard CI/CD pipelines where readability and maintainability are priorities | Human-readable, opinionated structure, easier to learn | Can be restrictive for highly dynamic logic   |
| `Scripted`    | Complex, programmatic pipelines requiring advanced Groovy logic               | Maximum flexibility and control                        | Steeper learning curve; you write Groovy code |

* Scripted Pipeline: code-centric and effectively a Groovy program (often using `node { ... }`). Use this for complex conditionals, dynamic stage generation, or other advanced runtime constructs.
* Declarative Pipeline: starts with `pipeline { ... }` and is intentionally structured for clarity and standardization; best for most teams and simpler CI/CD flows.

Pipelines vs Freestyle jobs

<Frame>
  <img alt="A slide titled &#x22;Pipeline vs Freestyle&#x22; showing a three-row comparison of Aspect, Structure, Configuration, and Complexity. It notes pipelines allow parallel stages, use Jenkinsfile and suit complex workflows, while freestyle is sequential, configured via the web, and fits basic tasks." />
</Frame>

Pipelines have largely superseded Freestyle jobs for modern CI/CD. The following table highlights the differences.

| Aspect          | Pipeline                                               | Freestyle                    |
| --------------- | ------------------------------------------------------ | ---------------------------- |
| Definition      | `Jenkinsfile` stored in repo                           | Configured in Jenkins UI     |
| Execution model | Stages, parallelism, durable execution                 | Sequential build steps       |
| Version control | Yes (in-repo)                                          | No (job config in Jenkins)   |
| Best fit        | Complex workflows, orchestration, multi-stage releases | Simple tasks or one-off jobs |

Benefits of using pipelines

* Version-controlled configuration and easier code review
* Resilient execution across controller restarts
* Built-in support for human interactions (approvals, input steps)
* Extensible with plugins and shared libraries
* Better orchestration: parallel stages, conditional logic, forking/joining

<Frame>
  <img alt="A presentation slide titled &#x22;Benefits of Pipelines&#x22; featuring six rounded tiles with icons. Each tile lists an advantage: Code as Configuration; Resilient by Design; Human Interaction Integration; Handling Complexity with Ease; Extensibility Beyond Limits; and Streamlined Build Management." />
</Frame>

> **lightbulb** Store your Jenkinsfile alongside your application code in the same repository. This enables versioning, code review, and reproducible CI/CD pipelines that travel with your code.

Getting started and next steps

* Start by converting simple Freestyle jobs to small Declarative Jenkinsfiles in the repo.
* Iterate: add stages, split long-running tasks into parallel jobs, and introduce manual approval gates where needed.
* Explore shared libraries to centralize common pipeline logic across projects.
* When you need dynamic behavior or runtime code generation, consider Scripted pipelines or a hybrid approach (Declarative with `script {}` blocks).

Links and references

* Jenkins Pipeline documentation: [https://www.jenkins.io/doc/book/pipeline/](https://www.jenkins.io/doc/book/pipeline/)
* Declarative Pipeline syntax: [https://www.jenkins.io/doc/book/pipeline/syntax/](https://www.jenkins.io/doc/book/pipeline/syntax/)
* Shared Libraries: [https://www.jenkins.io/doc/book/pipeline/shared-libraries/](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)

In this article we covered pipeline fundamentals—stages and steps, declarative vs scripted styles, and why pipelines often replace Freestyle jobs in modern CI/CD workflows. Recommended follow-ups: real-world pipeline patterns, handling parallelism, and designing resilient error handling and retry strategies.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/4ff3a393-a622-48d3-a0b5-4fb312c6c0a2/lesson/a73edd13-7bf6-474d-ad80-0b1a6f947ba3)
