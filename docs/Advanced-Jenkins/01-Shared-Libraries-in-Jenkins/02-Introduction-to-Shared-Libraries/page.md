# MEDIUM severity scan (exit code 0 keeps pipeline going)
trivy image siddharth67/solar-system:$GIT_COMMIT \
  --severity LOW,MEDIUM,HIGH \
  --exit-code 0 \
  --quiet \
  --format json -o trivy-image-MEDIUM-results.json

# CRITICAL severity scan (exit code 1 on finding CRITICAL issues)
trivy image siddharth67/solar-system:$GIT_COMMIT \
  --severity CRITICAL \
  --exit-code 1 \
  --quiet \
  --format json -o trivy-image-CRITICAL-results.json
```

Convert the JSON results to HTML and JUnit XML:

```bash theme={null}
trivy convert \
  --format template --template "@/usr/local/share/trivy/templates/html.tpl" \
  --output trivy-image-MEDIUM-results.html trivy-image-MEDIUM-results.json

trivy convert \
  --format template --template "@/usr/local/share/trivy/templates/html.tpl" \
  --output trivy-image-CRITICAL-results.html trivy-image-CRITICAL-results.json

trivy convert \
  --format template --template "@/usr/local/share/trivy/templates/junit.tpl" \
  --output trivy-image-MEDIUM-results.xml trivy-image-MEDIUM-results.json

trivy convert \
  --format template --template "@/usr/local/share/trivy/templates/junit.tpl" \
  --output trivy-image-CRITICAL-results.xml trivy-image-CRITICAL-results.json
```

Publish JUnit/XML and HTML reports inside the Trivy stage `post` block:

```groovy theme={null}
post {
    always {
        sh '''
          # trivy convert commands above
        '''

        // Publish JUnit results converted from Trivy JSON -> JUnit
        junit allowEmptyResults: true, testResults: 'trivy-image-MEDIUM-results.xml'
        junit allowEmptyResults: true, testResults: 'trivy-image-CRITICAL-results.xml'

        // Publish HTML reports
        publishHTML([allowMissing: true,
                     alwaysLinkToLastBuild: true,
                     keepAll: true,
                     reportDir: './',
                     reportFiles: 'trivy-image-MEDIUM-results.html',
                     reportName: 'Trivy MEDIUM Report'])

        publishHTML([allowMissing: true,
                     alwaysLinkToLastBuild: true,
                     keepAll: true,
                     reportDir: './',
                     reportFiles: 'trivy-image-CRITICAL-results.html',
                     reportName: 'Trivy CRITICAL Report'])
    }
}
```

Cleaning up the global `post` section

To keep the pipeline concise and visually clear in the Jenkins UI, we removed or commented out global `junit` and `publishHTML` calls and instead publish results in the specific stage that produces them. The top-level `post` block now contains only notifications and optional workspace cleanup:

```groovy theme={null}
post {
    always {
        slackNotificationMethod("${currentBuild.result}")

        script {
            if (fileExists('solar-system-gitops-argocd')) {
                sh 'rm -rf solar-system-gitops-argocd'
            }
        }
    }
}
```

Creating and pushing a new feature branch

Rather than editing the original `feature/enabling-slack` branch directly, create a new branch `feature/advanced-demo`. Example git flow:

```bash theme={null}
root@jenkins-controller-1 in solar-system on feature/enabling-slack via v20.16.0 on (us-east-2)
# create & switch to new branch
git checkout -b feature/advanced-demo

# edit Jenkinsfile, save changes, then commit and push
git add Jenkinsfile
git commit -m "refactored Jenkinsfile for advanced demos"
git push -u origin feature/advanced-demo
```

As soon as the branch is pushed, the multibranch pipeline (Git Organization job) detects the new branch and triggers a build when it finds the `Jenkinsfile`.

Build execution and handling expected failures

The refactor reduces stage count (from \~20 to \~4–5), which is ideal for demos. During early runs you may encounter Trivy failures that originate outside your environment (e.g., rate-limiting when Trivy downloads its vulnerability DB). These failures are external and should be handled separately (e.g., use a cached local DB, adjust Trivy exit codes, or re-run).

Sample console excerpt showing a Trivy DB download rate-limit error:

```text theme={null}
+ trivy image siddharth67/solar-system:23ac3d5c61f666daf3f8795cc229693d3e3af78e \
  --severity LOW,MEDIUM,HIGH --exit-code 0 --quiet --format json -o trivy-image-MEDIUM-results.json
2024-11-10T03:03:22Z        FATAL    Fatal error   init error: DB error: failed to download vulnerability DB: database download error: oci download error: failed to fetch the layer: GET https://ghcr.io/v2/aquasecurity/trivy-db/blobs/sha256:...: TOOMANYREQUESTS: retry-after: 160.753µs, allowed: 44000/minute
script returned exit code 1
```

> **warning** Trivy failures like the example above are usually due to external rate-limiting of Trivy DB downloads. Consider these mitigations:

  * Use a local Trivy DB cache (mirror) for CI.
  * Adjust `--exit-code` thresholds to avoid failing builds on lower-severity issues.
  * Add retry logic or fallback behavior for DB downloads.

Summary of the refactor

* Focused and reduced the Jenkinsfile to key CI stages for demos: dependencies, unit tests/coverage, Docker build, and Trivy scans.
* Preserved and reused Slack notification logic; simplified the global `post` block to notifications and cleanup.
* Moved Trivy report conversion and publishing into the Trivy stage `post` block for logical grouping of artifacts and easier debugging.
* Disabled long-running/deployment-specific stages in-place (commented) so they can be re-enabled later if needed.
* Created `feature/advanced-demo` branch to test the refactor without modifying the original branch.

Next steps

* Implement Trivy DB caching or retry strategies to avoid rate-limit issues.
* Consider moving shared helper functions (like `slackNotificationMethod`) to a Jenkins shared library if they will be reused across multiple pipelines.
* Re-enable additional stages gradually when demonstration requirements expand (for example, SonarQube or K8s deployment stages).

Links and references

* [Jenkins Pipelines course](https://learn.kodekloud.com/user/courses/jenkins-pipelines)
* [Trivy documentation](https://aquasecurity.github.io/trivy/)
* [Jenkins Pipeline Syntax / Declarative Pipeline](https://www.jenkins.io/doc/book/pipeline/syntax/)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-jenkins/module/7e7be52f-69f5-496b-8a46-322d6b8df0ce/lesson/32202656-91f4-4d7c-b4d9-3587ca0bd877)


# Introduction to Shared Libraries

Source: https://notes.kodekloud.com/docs/Advanced-Jenkins/Shared-Libraries-in-Jenkins/Introduction-to-Shared-Libraries/page

Explains Jenkins shared libraries and how to create, configure, and use reusable Groovy pipeline steps to centralize logic, reduce duplication, and simplify Jenkinsfile maintenance.

What are shared libraries in Jenkins?

A shared library is a repository of Groovy scripts and classes that provide reusable steps, functions, and helpers for Jenkins Pipelines. By centralizing common pipeline logic, shared libraries make Jenkinsfiles shorter, easier to read, and simpler to maintain across many projects.

<Frame>
  <img alt="A presentation slide titled &#x22;Shared Library – Overview&#x22; with a folder/share icon and two colored callouts reading &#x22;Encapsulates common tasks&#x22; and &#x22;Makes your pipelines more concise and readable.&#x22;" />
</Frame>

Example: a simple Node.js pipeline

A typical Jenkinsfile that builds and tests a Node.js app might look like this:

```groovy theme={null}
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }

        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
    }
}
```

If many repositories run the same build/test commands, copying these steps into each Jenkinsfile quickly causes duplication. That duplication leads to:

* A maintenance burden: updating the same logic across multiple files.
* Inconsistency: differing pipeline behavior across projects.
* Increased complexity: scattered changes that are hard to track.

Shared libraries follow the DRY (Don't Repeat Yourself) principle: implement the logic once and reuse it across pipelines.

Reusable helper example

A typical helper that lives in a shared library could be a notification helper. Put it under `vars/notifyBuild.groovy` in the shared library repository:

```groovy theme={null}
// vars/notifyBuild.groovy
def call(String buildStatus = 'STARTED') {
    buildStatus = buildStatus ?: 'SUCCESS'

    def color
    def emoji

    if (buildStatus == 'SUCCESS') {
        color = '#47ec05'
        emoji = ':white_check_mark:'
    } else if (buildStatus == 'UNSTABLE') {
        color = '#ffea00'
        emoji = ':warning:'
    } else if (buildStatus == 'FAILURE') {
        color = '#ff4c4c'
        emoji = ':x:'
    } else {
        color = '#cccccc'
        emoji = ':information_source:'
    }

    // Example: send notification (implementation depends on your notifier)
    echo "Build status: ${buildStatus} ${emoji} (color: ${color})"
}
```

Shared libraries are typically stored in source control (for example, Git) so Jenkins can fetch them. They make it easy to apply organization-wide changes from a single place.

Onboarding example: removing a hard-coded welcome message

A new DevOps team requires every pipeline to display a welcome message as the first stage. Initially, teams hard-code the message in each Jenkinsfile:

```groovy theme={null}
pipeline {
  agent any
  stages {
    stage('Welcome') {
      steps {
        sh 'echo Welcome to DevOps team from Dash Organization'
      }
    }
    stage('Build') {
      steps {
        // build steps ...
      }
    }
  }
}
```

As the organization grows, dozens or hundreds of Jenkinsfiles may duplicate that message. If the organization renames from Dash to KodeKloud, every file needs editing.

Instead, create a shared-library step that prints the welcome message. Update the message once in the library and all pipelines using it will reflect the change.

High-level adoption steps

<Frame>
  <img alt="An infographic titled &#x22;Steps to Shared Library&#x22; showing a four-step flow: Repository Setup, Jenkins Config, Write Custom Steps, and Integrate in Pipelines. Each colored step has a short note (create SCM repo; set up global pipeline library; develop Groovy functions; use @Library in Jenkinsfile) and they’re connected by arrows." />
</Frame>

1. Create a dedicated SCM repository to store your shared library code.
2. Configure a Global Pipeline Library in Jenkins (see Manage Jenkins → Configure System → Global Pipeline Libraries and the official docs at [https://www.jenkins.io/doc/book/pipeline/shared-libraries/](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)).
3. Develop reusable Groovy functions and classes in that repository.
4. Load and call the shared-library functions from Jenkinsfiles using the `@Library` annotation.

Recommended repository layout

A common layout for a Jenkins shared library repository:

```text theme={null}
root
├─ src                       # 📁 Groovy source files (optional; compiled classes)
│  └─ org
│     └─ foo
│        └─ Bar.groovy       # 📄 for org.foo.Bar class
│
├─ vars
│  ├─ welcomeMessage.groovy  # 📄 for global 'welcomeMessage' step
│  └─ welcomeMessage.txt     # 📄 help/usage for 'welcomeMessage' (optional)
│
└─ resources                 # 📁 resource files (optional)
   └─ org
      └─ foo
         └─ bar.json         # 📄 static helper data for org.foo.Bar
```

Directory purposes (quick reference)

| Directory   | Purpose                                                  | When to use                                                                |
| ----------- | -------------------------------------------------------- | -------------------------------------------------------------------------- |
| `src`       | Compiled Groovy/Java classes on the Pipeline classpath   | For complex logic or classes referenced by steps                           |
| `vars`      | Global pipeline steps; each file defines a callable step | Required for simple, globally available functions (file name => step name) |
| `resources` | Non-Groovy files accessible with `libraryResource`       | For static JSON, templates, or other assets used by steps                  |

Note: name files in `vars` using camelCase for multi-word step names (single word names are fine).

Example: welcome step in `vars`

Create `vars/welcome.groovy` in the shared library to centralize the welcome message:

```groovy theme={null}
// vars/welcome.groovy
def call() {
    sh 'echo Welcome to DevOps team from Dash Organization'
}
```

Configuring the shared library in Jenkins

In Jenkins: Manage Jenkins → Configure System → Global Pipeline Libraries. Important settings:

* Library name: identifier used in `@Library`.
* Default version: branch (for example, `main`) used if pipelines don't specify a branch.
* Allow default version to be overridden: permits pipelines to test different library branches with `@Library`.
* Load implicitly: when enabled, the default branch is available without adding `@Library` to Jenkinsfiles.
* Retrieval method/SCM: configure Git (use Modern SCM for Git repositories).

> **lightbulb** Tip: Use a stable default branch (for example, `main`) for production-ready shared library code. Allow pipelines to override the default version to test library changes on feature branches before promoting them.

Using a shared library in a Jenkinsfile

Add the `@Library` annotation at the top of your Jenkinsfile (replace `shared-library` with the configured library name). The underscore after the annotation ensures the library is available to the scripted pipeline portion.

```groovy theme={null}
@Library('shared-library') _
pipeline {
    agent any

    stages {
        stage('Welcome') {
            steps {
                // call the shared library step defined in vars/welcome.groovy
                welcome()
            }
        }

        stage('Build') {
            steps {
                // remaining pipeline steps...
            }
        }
    }
}
```

This makes `welcome()` (the `call` method in `vars/welcome.groovy`) available, removing hard-coded messages from individual Jenkinsfiles.

Summary

Shared libraries allow you to:

* Centralize reusable pipeline logic (Groovy steps, classes, and resources).
* Reduce duplication across Jenkinsfiles and teams.
* Maintain consistent pipeline behavior by updating the library in one place.
* Enable teams to test library changes by overriding versions per pipeline.

For more details and advanced patterns, see the Jenkins documentation on Shared Libraries: [https://www.jenkins.io/doc/book/pipeline/shared-libraries/](https://www.jenkins.io/doc/book/pipeline/shared-libraries/) and consider organizing library changes with versioning and CI for the library itself (for example, unit tests on `src` classes or linting for `vars` steps).

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-jenkins/module/7e7be52f-69f5-496b-8a46-322d6b8df0ce/lesson/8a6eb6c9-043f-4db3-ab3c-dce38e2f3f1e)
