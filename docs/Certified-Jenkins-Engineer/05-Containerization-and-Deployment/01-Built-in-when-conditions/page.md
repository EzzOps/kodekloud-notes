# Built in when conditions

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Containerization-and-Deployment/Built-in-when-conditions/page

This article explains the use of built-in `when` conditions in Jenkins Declarative Pipelines to control stage execution based on specific criteria.

In Jenkins Declarative Pipelines, the `when` directive controls whether a stage should be executed. A stage with a `when` block runs only if at least one of its conditions evaluates to true. You can also combine conditions for more advanced logic.

<Callout icon="lightbulb">
  Using `when` conditions can help you skip unnecessary stages, save build time, and reduce resource consumption.
</Callout>

## Base Pipeline Example

Below is a simple pipeline without any conditional logic. It has three sequential stages that always run:

```groovy theme={null}
pipeline {
    agent any
    stages {
        stage('Stage-1') {
            steps {
                echo 'Stage-1'
            }
        }
        stage('Stage-2') {
            steps {
                echo 'Stage-2'
            }
        }
        stage('Stage-3') {
            steps {
                echo 'Stage-3'
            }
        }
    }
}
```

## Overview of Built-in `when` Conditions

| Condition     | Description                               | Example                                         |
| ------------- | ----------------------------------------- | ----------------------------------------------- |
| branch        | Matches the current branch name           | `branch 'main'`                                 |
| environment   | Checks an environment variable’s value    | `environment name: 'deploy', value: 'pre-prod'` |
| expression    | Evaluates any Groovy boolean expression   | `expression { params.MANUAL_TEST }`             |
| changeRequest | Triggers when the build is a pull request | `changeRequest()`                               |
| buildingTag   | Runs only on builds started by a Git tag  | `buildingTag()`                                 |
| tag           | Matches a specific tag pattern            | `tag 'feature-*'`                               |

## Basic `when` Examples

### 1. Branch Selection

Run a stage only on the `main` branch:

```groovy theme={null}
stage('Run on main') {
    when {
        branch 'main'
    }
    steps {
        echo 'This runs only on the main branch.'
    }
}
```

### 2. Environment Variable Check

Execute the stage if `DEPLOY` equals `pre-prod`:

```groovy theme={null}
stage('Pre-prod deployment') {
    when {
        environment name: 'DEPLOY', value: 'pre-prod'
    }
    steps {
        echo "Deploying to pre-prod because DEPLOY=$DEPLOY"
    }
}
```

### 3. Groovy Expression

Use a custom Groovy expression to gate a manual test stage:

```groovy theme={null}
stage('Manual test stage') {
    when {
        expression {
            return params.MANUAL_TEST == true
        }
    }
    steps {
        echo 'Manual test parameter is true.'
    }
}
```

<Callout icon="triangle-alert">
  Avoid placing expensive computations or external calls in `expression` blocks—they run during pipeline evaluation and can slow down the build.
</Callout>

### 4. Pull Request Builds

Run validations only for pull requests:

```groovy theme={null}
stage('PR validation') {
    when {
        changeRequest()
    }
    steps {
        echo 'Running validations on pull request.'
    }
}
```

#### Filter by Author Email

```groovy theme={null}
stage('PR by Alice') {
    when {
        changeRequest authorEmail: 'alice@kk.com'
    }
    steps {
        echo 'This PR was opened by alice@kk.com.'
    }
}
```

### 5. Tag Checks

#### Any Tag Build

```groovy theme={null}
stage('Tag build') {
    when {
        buildingTag()
    }
    steps {
        echo 'Building from a tag, not a branch or commit.'
    }
}
```

#### Specific Tag Pattern

```groovy theme={null}
stage('Feature tag build') {
    when {
        tag 'feature-*'
    }
    steps {
        echo 'Running on a feature-* tag.'
    }
}
```

## Advanced Condition Combinations

### Evaluate Before Agent Allocation

Avoid checking out the workspace unless needed by evaluating conditions before the agent is allocated:

```groovy theme={null}
stage('Sandbox only') {
    when {
        beforeAgent true
        branch 'sandbox'
    }
    agent any
    steps {
        echo 'This runs on sandbox without checking out workspace on other branches.'
    }
}
```

### Negation

Invert a condition to exclude certain branches:

```groovy theme={null}
stage('Exclude pre-prod') {
    when {
        not {
            branch 'pre-prod'
        }
    }
    steps {
        echo 'This runs on all branches except pre-prod.'
    }
}
```

### anyOf

Run the stage if at least one nested condition is true:

```groovy theme={null}
stage('UAT or QA') {
    when {
        anyOf {
            branch 'uat'
            branch 'qa'
        }
    }
    steps {
        echo 'This runs on either uat or qa branch.'
    }
}
```

### allOf

Run the stage only if all nested conditions are met:

```groovy theme={null}
stage('Main pre-prod') {
    when {
        allOf {
            branch 'main'
            environment name: 'DEPLOY', value: 'pre-prod'
        }
    }
    steps {
        echo 'This runs only on main branch when DEPLOY=pre-prod.'
    }
}
```

## Further Reading

* [Pipeline Syntax Reference: when](https://www.jenkins.io/doc/book/pipeline/syntax/#when)
* [Jenkins Declarative Pipeline](https://www.jenkins.io/doc/book/pipeline/syntax/)
* [Jenkins Parameters](https://www.jenkins.io/doc/book/pipeline/syntax/#parameters)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/e16e4b93-31c4-479b-96b8-f0d26cde31cd/lesson/6ee17ad3-2eb9-40a7-8b39-7abd44917da3" />
</CardGroup>
