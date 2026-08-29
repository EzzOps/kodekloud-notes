# Demo GitHub Actions Workflow 1

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Fundamentals-of-GitHub-Actions/Demo-GitHub-Actions-Workflow-1/page

Guide to creating a basic GitHub Actions workflow and troubleshooting the common error of missing actions/checkout that leaves the runner workspace empty.

This guide walks through creating a simple GitHub Actions workflow and troubleshooting a common failure: forgetting to check out the repository, which leaves the runner workspace empty.

We'll pause our Jenkins pipeline for the moment and explore GitHub Actions instead.

<Frame>
  <img alt="A screenshot of the Jenkins Blue Ocean pipeline activity page for the job &#x22;ci-pipeline-poll-scm&#x22;, showing a list of recent pipeline runs with status icons, run numbers, messages and durations." />
</Frame>

Example: a Jenkins pipeline (for context) that we are not running while migrating to Actions:

```groovy theme={null}
pipeline {
    agent {
        label 'us-west-1-ubuntu-22'
    }
    tools {
        nodejs 'nodejs-22-6-0'
    }

    environment {
        MONGO_URI = "mongodb+srv://supercluster.d83jj.mongodb.net/superData"
        MONGO_DB_CREDS = credentials('mongo-db-credentials')
        MONGO_USERNAME = credentials('mongo-db-username')
        MONGO_PASSWORD = credentials('mongo-db-password')
    }

    stages {
        stage('Installing Dependencies') {
            agent {
                docker {
                    image 'node:24'
                    args '-u root:root'
                }
            }
            steps {
                sh 'npm install --no-audit'
            }
        }

        stage('Dependency Scanning') {
            parallel {
                stage('NPM Dependency Audit') {
                    steps {
                        sh '''
                            npm audit --audit-level=critical
                        '''
                    }
                }
            }
        }
    }
}
```

Create a new repository on GitHub (for example `actions-1`) and add a README. Open the repository's Actions tab and click Configure to create a starter workflow — GitHub will create `.github/workflows/<your-file>.yml` for you.

<Frame>
  <img alt="A dark-mode GitHub repository page for &#x22;actions-1&#x22; showing the main branch, an initial commit and a README.md file. The right sidebar displays repository metadata like stars, forks, releases, and package links." />
</Frame>

GitHub often provides this starter workflow template:

```yaml theme={null}
