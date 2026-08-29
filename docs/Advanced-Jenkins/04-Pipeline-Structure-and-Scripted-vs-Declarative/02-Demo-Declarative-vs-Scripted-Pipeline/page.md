# Demo Declarative vs Scripted Pipeline

Source: https://notes.kodekloud.com/docs/Advanced-Jenkins/Pipeline-Structure-and-Scripted-vs-Declarative/Demo-Declarative-vs-Scripted-Pipeline/page

Demo comparing Declarative and Scripted Jenkins pipelines, showing automatic SCM checkout, post versus finally cleanup, stage restart support, and required explicit checkout in scripted pipelines.

This lesson compares Declarative and Scripted Jenkins pipelines using a small demo repository. You'll create a single Pipeline job and run it twice: once using a Declarative Jenkinsfile and once using a Scripted Jenkinsfile to observe the differences in behavior (notably SCM checkout and `post`/`finally` execution).

Repository and branch

* Repository: `declarative-vs-scripted-pipeline` (hosted on the demo Gitea server)
* Branch: `demo-1`
* The branch contains two Jenkinsfiles:
  * `Jenkinsfile.declarative`
  * `Jenkinsfile.scripted`

Setup: create the Pipeline job

1. Create a Pipeline job named `D-v-s-pipeline`.
2. Under Pipeline → Definition select "Pipeline from SCM".
3. Point the job to the repository and branch `demo-1`.
4. For the first run set the Script Path to `Jenkinsfile.declarative` (so the job executes the Declarative pipeline).

Jenkinsfile.declarative

* This Jenkinsfile demonstrates a simple Declarative Pipeline with one stage and a `post` section.

```groovy theme={null}
pipeline {
    agent any

    stages {
        stage('Echo Message') {
            steps {
                sh 'ls -ltr'
                sh 'echo "This is executed within a DECLARATIVE Pipeline"'
            }
        }
    }

    post {
        always {
            sh 'echo "This will always run"'
            sh 'rm -rf *'
        }
    }
}
```

Key points about the Declarative pipeline

* By default, Declarative pipelines perform an SCM checkout before the first stage and display that as a separate stage (`Declarative: Checkout SCM`) in Blue Ocean or the classic stage view. This behavior can be disabled (for example with `skipDefaultCheckout` or when using `agent none`).
* The `post` block runs after the stages complete; `always` executes regardless of success or failure.

Representative pipeline log excerpt for Declarative (automatic checkout + `post` actions):

```text theme={null}
[Pipeline] { (Declarative: Checkout SCM)
[Pipeline] checkout
The recommended git tool is: NONE
No credentials specified
Cloning the remote Git repository
Cloning repository http://64.227.187.25:5555/dasher-org/declarative-vs-scripted-pipeline/
 > git init /var/lib/jenkins/workspace/d-v-s-pipeline # timeout=10
Fetching upstream changes from http://64.227.187.25:5555/dasher-org/declarative-vs-scripted-pipeline/
 > git --version # 'git version 2.43.0'
 > git fetch --tags --force --progress -- http://64.227.187.25:5555/dasher-org/declarative-vs-scripted-pipeline/ +refs/heads/*:refs/remotes/origin/* # timeout=10
Checking out Revision [AWS_SECRET_ACCESS_KEY] (origin/demo-1)
[Pipeline] }
[Pipeline] stage
[Pipeline] { (Echo Message)
[Pipeline] sh
+ ls -ltr
total 8
-rw-r--r-- 1 jenkins jenkins 301 Nov 10 12:24 Jenkinsfile.scripted
-rw-r--r-- 1 jenkins jenkins 342 Nov 10 12:24 Jenkinsfile.declarative
[Pipeline] sh
+ echo This is executed within a DECLARATIVE Pipeline
This is executed within a DECLARATIVE Pipeline
[Pipeline] }
[Pipeline] stage
[Pipeline] { (Declarative: Post Actions)
[Pipeline] sh
+ echo This will always run
This will always run
[Pipeline] sh
+ rm -rf Jenkinsfile.declarative Jenkinsfile.scripted
[Pipeline] }
```

Notes from the example:

* The checkout stage appears automatically by default (unless Declarative checkout behavior is disabled).
* The `Echo Message` stage runs after checkout and lists repository files.
* The `post` actions run at the end and, in this example, remove workspace files.

<Callout icon="lightbulb">
  Declarative pipelines are opinionated: they give a structured syntax (`pipeline {}`, `stages`, `post`) which enables features like automatic checkout, easier visualization in Blue Ocean, and stage restart support.
</Callout>

Scripted pipeline (no automatic checkout)

* Switch the job's Script Path to `Jenkinsfile.scripted` and run the job.
* Scripted pipelines do not perform SCM checkout automatically. If you want source code present in the workspace, you must explicitly call `checkout scm` (or use the `git` step or other SCM-specific steps).

Example `Jenkinsfile.scripted` without explicit checkout:

```groovy theme={null}
node {
    try {
        stage('Echo Message') {
            sh 'ls -ltr'
            sh 'echo This is executed within SCRIPTED Pipeline'
        }
    } catch (err) {
        echo "Failed: ${err}"
    } finally {
        sh 'echo "This will always run"'
        // sh 'rm -r *'
    }
}
```

Representative scripted pipeline log (no checkout performed; workspace empty):

```text theme={null}
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins in /var/lib/jenkins/workspace/d-v-s-pipeline
[Pipeline] stage
[Pipeline] { (Echo Message)
[Pipeline] sh
+ ls -ltr
total 0
[Pipeline] sh
+ echo This is executed within a SCRIPTED Pipeline
This is executed within a SCRIPTED Pipeline
[Pipeline] }
[Pipeline] sh
+ echo This will always run
This will always run
[Pipeline] End of Pipeline
Finished: SUCCESS
```

<Callout icon="warning">
  If your Scripted pipeline needs the repository files, remember to add an explicit checkout (e.g., `checkout scm`). Forgetting to do so will leave the workspace empty.
</Callout>

Add explicit checkout in Scripted pipeline

* To make the Scripted pipeline perform the SCM checkout, add `checkout scm` inside the `node` block (commonly inside a stage).

Updated `Jenkinsfile.scripted` (with explicit checkout):

```groovy theme={null}
node {
    try {
        stage('Echo Message') {
            checkout scm
            sh 'ls -ltr'
            sh 'echo This is executed within a SCRIPTED Pipeline'
        }
    } catch (err) {
        echo "Failed: ${err}"
    } finally {
        sh 'echo "This will always run"'
        // sh 'rm -r *'
    }
}
```

Representative log excerpt after adding `checkout scm`:

```text theme={null}
[Pipeline] stage
[Pipeline] { (Echo Message)
[Pipeline] checkout
The recommended git tool is: NONE
No credentials specified
Fetching changes from the remote Git repository
> git --version # 'git version 2.43.0'
> git fetch --tags --force --progress -- http://64.227.187.25:5555/dasher-org/declarative-vs-scripted-pipeline/ +refs/heads/*:refs/remotes/origin/* # timeout=10
Checking out Revision [AWS_SECRET_ACCESS_KEY] (origin/demo-1)
[Pipeline] sh
+ ls -ltr
total 8
-rw-r--r-- 1 jenkins jenkins 311 Nov 10 12:29 Jenkinsfile.scripted
-rw-r--r-- 1 jenkins jenkins 342 Nov 10 12:29 Jenkinsfile.declarative
[Pipeline] sh
+ echo This is executed within a SCRIPTED Pipeline
This is executed within a SCRIPTED Pipeline
```

Summary of differences demonstrated

* Automatic SCM checkout:
  * Declarative: Performs checkout automatically by default and shows a `Declarative: Checkout SCM` stage. This can be disabled with options like `skipDefaultCheckout`.
  * Scripted: No automatic checkout; you must call `checkout scm` explicitly.
* Restart-from-stage:
  * Declarative: Supports restarting from a specific stage (with stage checkpoints and appropriate plugins/features).
  * Scripted: Does not support restart-from-stage in the same way as Declarative.
* Structure and opinionation:
  * Declarative: Enforces a higher-level structure that enables built-in features (automatic checkout, visual stages, structured `post` handling).
  * Scripted: Offers full Groovy control and flexibility, but requires manual handling for common tasks (checkout, structured post actions, restart behavior).

Differences at a glance

|               Feature | Declarative Pipeline                                    | Scripted Pipeline                                             |
| --------------------: | ------------------------------------------------------- | ------------------------------------------------------------- |
|  Default SCM checkout | Yes — automatic; visible as `Declarative: Checkout SCM` | No — `checkout scm` must be invoked explicitly                |
|     Structured syntax | `pipeline {}`, `stages`, `post` — opinionated           | Free-form Groovy (`node {}` and manual stages)                |
| Post/cleanup handling | `post` blocks (`always`, `success`, `failure`)          | `try` / `catch` / `finally` blocks                            |
| Stage restart support | Supported (with proper plugins/checkpoints)             | Not supported in the same way                                 |
|              Best for | Standardized pipelines, team-friendly, visual stages    | Complex, highly custom logic that requires Groovy flexibility |

Links and references

* Jenkins Declarative Pipeline: [https://www.jenkins.io/doc/book/pipeline/syntax/](https://www.jenkins.io/doc/book/pipeline/syntax/)
* Jenkins Scripted Pipeline basics: [https://www.jenkins.io/doc/book/pipeline/scripted/](https://www.jenkins.io/doc/book/pipeline/scripted/)
* Blue Ocean (visual pipeline UI): [https://www.jenkins.io/projects/blueocean/](https://www.jenkins.io/projects/blueocean/)

That's all for this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-jenkins/module/cffedc7a-8318-433c-83ff-5ec8f272486f/lesson/3454a17d-b4d0-4b5c-ac4b-0c8c9080aacb" />
</CardGroup>
