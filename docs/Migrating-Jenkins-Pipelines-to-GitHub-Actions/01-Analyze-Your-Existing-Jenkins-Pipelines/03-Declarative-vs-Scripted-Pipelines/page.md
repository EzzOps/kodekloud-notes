# Declarative vs Scripted Pipelines

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Analyze-Your-Existing-Jenkins-Pipelines/Declarative-vs-Scripted-Pipelines/page

Comparison of Jenkins Declarative and Scripted pipelines, their trade-offs, usage recommendations, examples, and guidance on when to use each style

In this lesson we compare the two primary styles for writing Jenkins pipelines: Declarative and Scripted. Both styles are saved in a `Jenkinsfile`, run by the same Jenkins Pipeline subsystem, use [Apache Groovy](https://groovy-lang.org/), and can share logic through shared libraries. Choosing the right style depends on team skills, maintainability goals, and the complexity of pipeline logic.

## Scripted Pipeline (Groovy-centric)

Scripted pipelines are written as full Groovy programs. They provide the maximum flexibility and control because you can use native Groovy constructs for complex logic, dynamic stage creation, loops, and advanced error handling.

Key points:

* Full access to Groovy language features.
* Best for highly customized automation and advanced logic.
* Requires Groovy knowledge and tends to have a steeper learning curve.

Example Scripted `Jenkinsfile`:

```groovy theme={null}
node {
  stage('Checkout') {
    checkout scm
  }

  stage('Build') {
    sh 'mvn -B -DskipTests package'
  }

  stage('Test') {
    sh 'mvn test'
    junit 'target/surefire-reports/*.xml'
  }

  stage('Deploy') {
    if (env.BRANCH_NAME == 'main') {
      sh './deploy-prod.sh'
    } else {
      sh './deploy-staging.sh'
    }
  }
}
```

Trade-offs:

* Pros: total control, dynamic behavior, complex branching logic.
* Cons: harder to read for non-developers, more prone to inconsistent formatting and patterns across teams.

## Declarative Pipeline (Structured and opinionated)

Declarative pipelines provide a structured, human-readable syntax with clearly defined top-level sections (for example: `pipeline`, `agent`, `stages`, `steps`, and `post`). This structure enforces best practices and consistency across teams.

Key points:

* Easier to learn and maintain—recommended as a default for most CI/CD workflows.
* Built-in validation and more predictable behavior.
* Intentionally limits arbitrary scripting to keep pipelines readable and standardized.

Example Declarative `Jenkinsfile`:

```groovy theme={null}
pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build') {
      steps {
        sh 'mvn -B -DskipTests package'
      }
    }

    stage('Test') {
      steps {
        sh 'mvn test'
        junit 'target/surefire-reports/*.xml'
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'target/*.jar', fingerprint: true
    }
  }
}
```

When you need a bit of Groovy logic inside Declarative pipelines, use a `script` block for localized scripting:

```groovy theme={null}
stage('Conditional') {
  steps {
    script {
      if (env.BRANCH_NAME == 'main') {
        sh './deploy-prod.sh'
      } else {
        sh './deploy-staging.sh'
      }
    }
  }
}
```

<Frame>
  <img alt="An infographic titled &#x22;Types of Pipeline Projects&#x22; comparing two pipeline styles: Scripted Pipeline and Declarative Pipeline. The left lists Scripted as code-centric, flexible, with a learning curve; the right lists Declarative as human-readable, easier to learn, and limited in complexity." />
</Frame>

The diagram above summarizes the trade-offs: scripted pipelines prioritize flexibility and programmatic control, while declarative pipelines prioritize readability, consistency, and convention.

## Quick comparison

|                  Feature | Scripted Pipeline          | Declarative Pipeline                                   |
| -----------------------: | -------------------------- | ------------------------------------------------------ |
|             Syntax style | Full Groovy script         | Structured DSL (`pipeline { ... }`)                    |
|              Ease of use | Lower (requires Groovy)    | Higher (clear layout)                                  |
|              Flexibility | Very high                  | Limited by design, but extendable with `script` blocks |
|                 Best for | Complex, dynamic workflows | Standard CI/CD flows, teams that value consistency     |
| Error handling & control | Programmatic via Groovy    | Declarative `post` and built-in stages                 |

## Choosing between Declarative and Scripted

* Use Declarative pipelines when you want:
  * A consistent, easy-to-read pipeline format.
  * Quick onboarding for new team members.
  * Predictable CI/CD flows that follow conventions.

* Use Scripted pipelines when you need:
  * Fine-grained control, dynamic stage generation, or advanced Groovy logic.
  * Custom behaviors that are impractical to express in Declarative form.

* Hybrid approach:
  * Start with Declarative for most work and use `script` blocks only where necessary.
  * Reserve pure Scripted pipelines for workflows that truly require full Groovy flexibility.

<Callout icon="lightbulb">
  If you’re starting or want standardized, maintainable CI/CD, begin with Declarative pipelines. Move to Scripted pipelines only when your workflows require patterns or dynamic behavior that Declarative syntax cannot express.
</Callout>

## Links and references

* [Jenkinsfile and Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
* [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
* [Apache Groovy — official site](https://groovy-lang.org/)
* [Shared Libraries — Jenkins](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/4ff3a393-a622-48d3-a0b5-4fb312c6c0a2/lesson/c3b5612d-c270-4105-8f9e-0d103a45ccc8" />
</CardGroup>
