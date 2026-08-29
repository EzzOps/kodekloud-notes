# Demo Load TrivyScanScript Library in Jenkins Pipeline

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Shared-Libraries-in-Jenkins/Demo-Load-TrivyScanScript-Library-in-Jenkins-Pipeline/page

Learn to integrate a custom TrivyScanScript shared library into a Jenkins pipeline for consistent vulnerability scanning across projects.

In this guide, you’ll learn how to import a custom `TrivyScanScript` shared library into your Jenkins pipeline and run vulnerability scans at various severity levels. By centralizing your Trivy logic, you can maintain consistency across projects and simplify pipeline definitions.

***

## Prerequisites

* A Jenkins instance with [Pipeline Shared Libraries](https://www.jenkins.io/doc/book/pipeline/shared-libraries/) enabled
* A Git repository for your shared library
* An application repository containing a `Jenkinsfile`
* Docker image registry credentials (if needed)

***

## 1. Define the `vulnerability` Step in the Shared Library

In your shared library repo, open or create `vars/TrivyScanScript.groovy` and add the `vulnerability` function:

```groovy theme={null}
// vars/TrivyScanScript.groovy

def vulnerability(Map config = [:]) {
    loadScript(name: 'trivy.sh')
    sh "./trivy.sh ${config.imageName} ${config.severity} ${config.exitCode}"
}
```

Commit and push these changes:

| Command                                                  | Description                   |
| -------------------------------------------------------- | ----------------------------- |
| `git checkout -b featureTrivyScan`                       | Create a feature branch       |
| `git add vars/TrivyScanScript.groovy`                    | Stage the new step definition |
| `git commit -m "Add TrivyScanScript.vulnerability step"` | Commit with a clear message   |
| `git push -u origin featureTrivyScan`                    | Push branch to remote         |

***

## 2. Invoke the Shared Library from Your `Jenkinsfile`

In your application repository, update the `Jenkinsfile` to load and call `trivyScanScript.vulnerability`:

```groovy theme={null}
pipeline {
    agent any
    libraries {
        // Reference your shared library and feature branch
        library identifier: 'your-shared-lib@featureTrivyScan'
    }
    stages {
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t myorg/app:$GIT_COMMIT .'
            }
        }
        stage('Trivy Vulnerability Scanner') {
            steps {
                script {
                    // Run scans for each severity level
                    ['LOW','MEDIUM','HIGH','CRITICAL'].each { sev ->
                        def exitCode = sev == 'CRITICAL' ? '1' : '0'
                        trivyScanScript.vulnerability(
                            imageName: "myorg/app:$GIT_COMMIT",
                            severity:  sev,
                            exitCode:  exitCode
                        )
                    }
                }
            }
            post {
                always {
                    script {
                        // Convert results to HTML
                        trivyScanScript.reportsConverter()
                    }
                    publishHTML(
                        allowMissing:        true,
                        alwaysLinkToLastBuild: true,
                        keepAll:             true,
                        reportDir:           './'
                    )
                }
            }
        }
    }
}
```

Commit and push:

```bash theme={null}
git add Jenkinsfile
git commit -m "Invoke TrivyScanScript.vulnerability in pipeline"
git push
```

***

## 3. Troubleshooting: `MissingPropertyException`

If Jenkins logs show:

```Groovy theme={null}
java.lang.MissingPropertyException: No such property: trivy for class: TrivyScanScript
```

that usually means the `loadScript` invocation wasn’t using a string literal for the script name.

<Callout icon="triangle-alert">
  Ensure you wrap the script name in quotes. Otherwise, Groovy tries to resolve an undefined property.
</Callout>

***

## 4. Fixing the `loadScript` Invocation

Update `vars/TrivyScanScript.groovy` to use a quoted name:

```groovy theme={null}
def vulnerability(Map config = [:]) {
    loadScript(name: 'trivy.sh')
    sh "./trivy.sh ${config.imageName} ${config.severity} ${config.exitCode}"
}
```

Then:

```bash theme={null}
git add vars/TrivyScanScript.groovy
git commit -m "Fix loadScript name quoting"
git push
```

Rerun or trigger the Jenkins build.

***

## 5. Verifying a Successful Run

After Jenkins picks up the fix, you should see output similar to:

```bash theme={null}
Loading library your-shared-lib@featureTrivyScan
...
chmod +x ./trivy.sh
./trivy.sh myorg/app:abcd1234 LOW 0
./trivy.sh myorg/app:abcd1234 MEDIUM 0
./trivy.sh myorg/app:abcd1234 HIGH 0
./trivy.sh myorg/app:abcd1234 CRITICAL 1
...
trivy convert --format template \
  --template "@/usr/local/share/trivy/templates/html.tpl" \
  --output trivy-image-LOW-results.html trivy-image-LOW-results.json
```

You will also find the generated HTML reports under your build’s artifacts.

***

## Conclusion

By extracting the Trivy vulnerability scan into a shared library step, you:

* Promote reuse and consistency across pipelines
* Reduce duplication in `Jenkinsfile`s
* Simplify maintenance when updating scan logic

For more details on Trivy and Jenkins integration, see:

* [Aqua Security Trivy Documentation](https://aquasecurity.github.io/trivy/)
* [Jenkins Pipeline Shared Libraries](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/b0fefde6-7fea-44da-9509-27007d27869f/lesson/3957f436-3833-4717-bb21-39d4588d9402" />
</CardGroup>
