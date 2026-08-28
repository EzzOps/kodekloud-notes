# Pipeline and Jenkinsfile

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Jenkins-Pipelines/Pipeline-and-Jenkinsfile/page

Jenkins Pipeline automates CI/CD workflows using code, enabling version-controlled, reusable, and maintainable pipelines through a Jenkinsfile.

Jenkins Pipeline enables you to automate complex Continuous Integration (CI) and Continuous Deployment (CD) workflows using code. By defining your build, test, and deploy steps in a `Jenkinsfile`, you gain version-controlled, reusable, and maintainable pipelines.

<Frame>
  ![The image shows a Jenkins Pipeline flowchart with stages: Building, Unit Testing, Linting, Dockerizing, Security, Deployment, and Tests. Each stage is represented by an icon and label.](https://kodekloud.com/kk-media/image/upload/v1752870797/notes-assets/images/Certified-Jenkins-Engineer-Pipeline-and-Jenkinsfile/jenkins-pipeline-flowchart-stages.jpg)
</Frame>

Breaking down your workflow into stages—like Build, Test, Lint, Dockerize, Security Scan, Deploy, and Post-deploy Tests—helps you:

* Achieve clear separation of concerns
* Easily spot failures and bottlenecks
* Parallelize independent tasks (e.g., linting alongside unit tests)

<Callout icon="lightbulb">
  Storing your pipeline stages in code lets you audit history, perform code reviews, and roll back changes through Git.
</Callout>

## 1. Writing Your Jenkinsfile

A `Jenkinsfile` is a Groovy-based script that describes your pipeline. There are two syntaxes:

```groovy theme={null}
pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'mvn clean package'
      }
    }
    stage('Unit Test') {
      steps {
        sh 'mvn test'
      }
    }
    stage('Dockerize') {
      steps {
        sh 'docker build -t myapp:${BUILD_NUMBER} .'
        sh 'docker push myapp:${BUILD_NUMBER}'
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

Key elements:

| Directive       | Purpose                                         |
| --------------- | ----------------------------------------------- |
| `pipeline`      | Top-level block defining the entire pipeline    |
| `agent any`     | Executes stages on any available Jenkins agent  |
| `stages`        | Container for all `stage` directives            |
| `stage('Name')` | Logical grouping of related `steps`             |
| `steps`         | Actual shell, script, or plugin commands to run |

## 2. Declarative vs. Scripted Pipelines

Jenkins supports two pipeline styles. Choose **Declarative** for simplicity or **Scripted** for advanced use cases.

<Frame>
  ![The image compares two types of pipeline projects: Scripted Pipeline, which is code-centric with flexibility and a learning curve, and Declarative Pipeline, which is human-readable and easier to learn.](https://kodekloud.com/kk-media/image/upload/v1752870798/notes-assets/images/Certified-Jenkins-Engineer-Pipeline-and-Jenkinsfile/pipeline-projects-scripted-declarative.jpg)
</Frame>

| Feature        | Declarative Pipeline                 | Scripted Pipeline                        |
| -------------- | ------------------------------------ | ---------------------------------------- |
| Syntax         | Opinionated, YAML-like structure     | Unrestricted Groovy code                 |
| Readability    | High—designed for easy understanding | Lower—requires Groovy/programming skills |
| Flexibility    | Supports standard workflows          | Full control with dynamic stages         |
| Error Handling | Built-in `post` conditions           | Custom try/catch logic                   |
| Learning Curve | Gentle—ideal for most teams          | Steeper—suited to experienced developers |

## 3. Pipeline vs. Freestyle Projects

Freestyle jobs are configured via the Jenkins UI, while Pipeline projects use code. Pipelines offer far greater power, versioning, and resilience.

<Frame>
  ![The image is a comparison chart between "Pipeline" and "Freestyle" in terms of structure, configuration, and complexity, highlighting their differences in task execution, configuration methods, and suitability for workflows.](https://kodekloud.com/kk-media/image/upload/v1752870800/notes-assets/images/Certified-Jenkins-Engineer-Pipeline-and-Jenkinsfile/pipeline-vs-freestyle-comparison-chart.jpg)
</Frame>

| Aspect        | Pipeline Projects                                   | Freestyle Projects                 |
| ------------- | --------------------------------------------------- | ---------------------------------- |
| Structure     | Stage-based, supports parallel execution            | Sequential build steps             |
| Configuration | `Jenkinsfile` in source control (Git, SVN)          | Job DSL or manual UI configuration |
| Resilience    | Resumes after controller restart                    | Restarts lost progress             |
| Scalability   | Complex workflows, shared libraries, reusable steps | Limited by UI plugins              |

<Callout icon="triangle-alert">
  Avoid using Freestyle jobs for multi-stage pipelines or complex branching logic. Migrating to Declarative Pipelines reduces job sprawl and improves traceability.
</Callout>

## 4. Key Benefits of Jenkins Pipelines

<Frame>
  ![The image lists the benefits of pipelines, including code as configuration, resilience by design, human interaction integration, handling complexity with ease, extensibility beyond limits, and streamlined build management.](https://kodekloud.com/kk-media/image/upload/v1752870801/notes-assets/images/Certified-Jenkins-Engineer-Pipeline-and-Jenkinsfile/benefits-of-pipelines-list.jpg)
</Frame>

1. **Code as Configuration**\
   Version your `Jenkinsfile` alongside application code for audit trails and collaborative editing.
2. **Resilience by Design**\
   Pipelines automatically resume after Jenkins controller restarts, preserving workflow state.
3. **Human Interaction**\
   Pause for manual approvals, input parameters, or interactive prompts.
4. **Advanced Workflow Control**\
   Use forks, joins, loops, and parallel stages to orchestrate complex CI/CD flows.
5. **Extensibility**\
   Leverage plugins or Shared Libraries to add custom pipeline steps.
6. **Unified Job Management**\
   Combine multiple build and deploy steps into a single Pipeline job, reducing maintenance overhead.

## Links and References

* [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
* [Declarative Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/syntax/#declarative-pipeline)
* [Scripted Pipeline Overview](https://www.jenkins.io/doc/book/pipeline/scripted/)
* [Official Jenkins GitHub Repository](https://github.com/jenkinsci/jenkins)
* [Jenkins Shared Libraries](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/054c2c42-f54a-42a4-ab39-4b432a36aaa1/lesson/13b11d65-9ce8-40bf-ae13-1f7f836e6e7b" />
</CardGroup>
