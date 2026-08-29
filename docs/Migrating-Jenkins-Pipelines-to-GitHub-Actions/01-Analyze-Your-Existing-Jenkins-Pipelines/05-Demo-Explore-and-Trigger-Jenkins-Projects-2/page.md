# Build — fetch an advice message
curl -s https://api.adviceslip.com/advice > advice.json
cat advice.json

# Extract advice text
# Requires jq to be installed on the agent. Install on Debian/Ubuntu with:
#   sudo apt-get update -y && sudo apt-get install -y jq
jq -r .slip.advice < advice.json > advice.message

# Test — ensure the advice has more than 5 words
if [ "$(wc -w < advice.message)" -gt 5 ]; then
  echo "Advice has more than 5 words"
else
  echo "Advice - $(cat advice.message) has 5 words or less"
  exit 1
fi

# Deploy — install cowsay (Debian/Ubuntu example; on other OSes use the appropriate package manager)
# Note: Installing packages requires the Jenkins user to have sudo privileges or to run on an agent with cowsay preinstalled.
sudo apt-get update -y
sudo apt-get install cowsay -y

# Ensure /usr/games and /usr/local/games are on PATH for the current run
export PATH="$PATH:/usr/games:/usr/local/games"
cat advice.message | cowsay -f "$(ls /usr/share/cowsay/cows | shuf -n 1)"
```

> **warning** The script assumes `jq` and `cowsay` are available or can be installed with `sudo`. Installing packages on shared agents can have security and stability implications—prefer pre-baked agent images or containerized runners when possible.

Triggering the job multiple times shows success and failure runs depending on the advice length.

Example console output for a successful run (truncated):

```text theme={null}
Started by user siddharth
Running as SYSTEM
Building on the built-in node in workspace /var/lib/jenkins/workspace/Generate ASCII Artwork
[Generate ASCII Artwork] $ /bin/sh -xe /tmp/jenkins-script.sh
+ curl -s https://api.adviceslip.com/advice
+ cat advice.json
{"slip": { "id": 167, "advice": "No one knows anyone else in the way you do."}}
+ jq -r .slip.advice < advice.json
+ wc -w < advice.message
+ [ 10 -gt 5 ]
+ echo Advice has more than 5 words
Advice has more than 5 words
+ sudo apt-get update -y
+ sudo apt-get install cowsay -y
Reading package lists...
Building dependency tree...
Reading state information...
cowsay is already the newest version (3.03+dfsg2-8).
0 upgraded, 0 newly installed, 0 to remove and 18 not upgraded.
+ export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/snap/bin:/usr/games:/usr/local/games
+ cat advice.message
No one knows anyone else in the way you do.
+ ls /usr/share/cowsay/cows
+ shuf -n 1
+ cowsay -f three-eyes.cow

/ No one knows anyone else in the way you \
\ do.                                          /
 ------------------------------- 
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

Example console output when the advice is too short and the build fails:

```text theme={null}
Started by user siddharth
Running as SYSTEM
Building on the built-in node in workspace /var/lib/jenkins/workspace/Generate ASCII Artwork
[Generate ASCII Artwork] $ /bin/sh -xe /tmp/jenkins-script.sh
+ curl -s https://api.adviceslip.com/advice
+ cat advice.json
{"slip": {"id": 3, "advice": "Don't eat non-snow-coloured snow."}}
+ jq -r .slip.advice < advice.json
+ wc -w < advice.message
+ [ 4 -gt 5 ]
+ echo Advice - Don't eat non-snow-coloured snow. has 5 words or less
Advice - Don't eat non-snow-coloured snow. has 5 words or less
+ exit 1
Build step 'Execute shell' marked build as failure
Finished: FAILURE
```

This Freestyle job demonstrates:

* How simple shell logic can control build success/failure.
* How external APIs and small utility tools (`jq`, `cowsay`) are often used in quick demo jobs.
* Why migrating these jobs may require translating shell steps into equivalent workflow actions or containerized steps.

***

## Scripted Pipeline

Next, inspect a scripted Pipeline job that contains a small hardcoded pipeline script in the Jenkins job configuration (again, no SCM and no triggers). The pipeline shows a simple three-stage flow: Greet, Build, and Results.

The pipeline activity page with recent runs:

<Frame>
  <img alt="A Jenkins pipeline web UI showing the &#x22;scripted-pipeline&#x22; activity page with a list of recent runs (1–7), each marked successful with green checkmarks and durations. The entries show &#x22;Started by user siddharth,&#x22; and the page includes Run/Disable buttons and navigation tabs." />
</Frame>

Opening a run shows the stage visualization and console output. The Build stage simulates work with `sleep`, and Results prints the completion time.

<Frame>
  <img alt="A screenshot of a Jenkins scripted-pipeline run showing stages (Start, Greet, Build, Results, End) with green checkmarks indicating success. The build log lists completed steps including &#x22;Pretending to build...&#x22; and a 5-second sleep." />
</Frame>

Scripted Pipeline used in the job:

```groovy theme={null}
node { // Runs on any available agent
    stage('Greet') {
        echo 'Hello, World!'
    }

    stage('Build') {
        echo 'Pretending to build...'
        sleep 5 // Simulate work
    }

    stage('Results') {
        def now = new Date()
        echo "Job completed at ${now}"
    }
}
```

When executed:

* The console shows the greeting, a simulated build pause (5 seconds), and the completion timestamp.
* The stage view makes it easy to visualize progress and success/failure per stage.

***

## Next steps and migration considerations

* Later lessons will cover how to migrate these Jenkins jobs (Freestyle and scripted Pipeline) to GitHub Actions and how to express the same logic in workflow files.
* When planning migration, consider:
  * Translating shell-driven Freestyle steps to individual CI actions or container steps.
  * Replacing inline package installs with prebuilt images or setup actions to avoid privileged operations on runners.
  * Converting scripted Pipeline stages into YAML-based workflows and grouping steps into reusable actions.

References:

* [adviceslip API](https://api.adviceslip.com/)
* [jq — JSON processor](https://stedolan.github.io/jq/)
* [cowsay](https://en.wikipedia.org/wiki/Cowsay)
* [Migrating Jenkins Pipelines to GitHub Actions](https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions)

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/4ff3a393-a622-48d3-a0b5-4fb312c6c0a2/lesson/39a8766a-9270-461c-ac87-b8ebd69b7c41)


# Demo Explore and Trigger Jenkins Projects 2

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Analyze-Your-Existing-Jenkins-Pipelines/Demo-Explore-and-Trigger-Jenkins-Projects-2/page

Explores Jenkins pipelines, running builds, dependency and image vulnerability scans, unit tests, coverage, Docker image build and push, and poll SCM trigger difference

In this lesson we explore the remaining two Jenkins projects, run builds, and inspect the results. Both pipelines reference the same repository and Jenkinsfile; the only functional difference is that the CI Pipeline (poll SCM) has a cron trigger configured.

Pipelines covered

* Solar System CI Pipeline
* CI Pipeline (poll SCM)

Both jobs use the same repository and pipeline script. The poll-SCM job adds a cron polling trigger to periodically check for changes.

I’ll sign in to Jenkins and show the pipeline configuration.

The Solar System job is configured to obtain its Pipeline script from SCM (Git). The repository and branch are set in the Pipeline configuration:

<Frame>
  <img alt="A dark-themed screenshot of a Jenkins job &#x22;Configure&#x22; page showing the Pipeline section set to &#x22;Pipeline script from SCM&#x22; with Git selected and the repository URL filled as &#x22;https://github.com/jenkins-demo-org/solar-system&#x22;. The left sidebar shows configuration tabs (General, Triggers, Pipeline, Advanced) and Save/Apply buttons are visible at the bottom." />
</Frame>

Repository and branch settings (example):

```text theme={null}
https://github.com/jenkins-demo-org/solar-system
*/main
```

The CI Pipeline (poll SCM) is identical except for the trigger; it polls the repository on a cron schedule:

```text theme={null}
00 00 * * *
```

Open the GitHub repository referenced by the pipeline to review the project structure and pipeline code.

<Frame>
  <img alt="A dark-themed GitHub repository page for &#x22;jenkins-demo-org/solar-system&#x22; showing the file list (Dockerfile, Jenkinsfile, README.md, app.js, app-test.js, package.json, etc.) on the main branch. The right sidebar shows repo details like commits, forks, stars, and languages." />
</Frame>

Repository overview

* Small Node.js application.
* Key files:
  * `Dockerfile` — image build
  * `Jenkinsfile` — declarative pipeline used by Jenkins
  * `app.js`, `app-test.js` — application and unit tests
  * `package.json` / `package-lock.json` — dependencies and scripts

Example Dockerfile from the repo:

```dockerfile theme={null}
FROM node:18-alpine3.17

WORKDIR /usr/app

COPY package*.json /usr/app/

RUN npm install

COPY . .

ENV MONGO_URI=uriPlaceholder
ENV MONGO_USERNAME=usernamePlaceholder
ENV MONGO_PASSWORD=passwordPlaceholder

EXPOSE 3000

CMD [ "npm", "start" ]
```

> **warning** Avoid placing secrets in `Dockerfile` via `ENV` for production images. Store sensitive values in a secrets manager or inject them at runtime (e.g., via Jenkins credentials or container runtime secrets).

Jenkinsfile — pipeline summary
The project’s declarative `Jenkinsfile` defines an end-to-end CI pipeline that runs inside Docker agents and uses Jenkins tools/credentials. Main stages include installing dependencies, dependency scanning, unit testing, code coverage, building & publishing a Docker image, and a Trivy image scan.

Representative (cleaned) Jenkinsfile excerpt:

```groovy theme={null}
pipeline {
    agent { label 'us-west-1-ubuntu-22' }

    tools { nodejs 'nodejs-22-6-0' }

    environment {
        MONGO_URI      = "mongodb+srv://supercluster.d83jj.mongodb.net/superData"
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
                        echo $?
                        '''
                    }
                }

                stage('OWASP Dependency Check') {
                    steps {
                        dependencyCheck additionalArguments: """
                            --scan './'
                            --out './'
                            --format 'ALL'
                            --disableYarnAudit
                            --prettyPrint --failOnCVSS 9
                        """, nvdCredentialsId: 'owasp-dependency-check', odcInstallation: 'OWASP-DepCheck-10'

                        // Fail the build only for CRITICAL findings
                        dependencyCheckPublisher failedTotalCritical: 1, pattern: 'dependency-check-report.xml', stopBuild: true

                        // You can publish the HTML report using publishHTML once uncommented
                        // publishHTML([allowMissing: true, alwaysLinkToLastBuild: true, keepAll: true, reportDir: './', reportFiles: 'dependency-check-jenkins.html', reportName: 'Dependency-Check Report'])
                    }
                }
            }
        }

        stage('Unit Testing') {
            agent {
                docker {
                    image 'node:24'
                    args '-u root:root'
                }
            }
            options { retry(2) }
            steps {
                sh 'npm test'
                // junit allowEmptyResults: true, testResults: 'test-results.xml'
            }
        }

        stage('Code Coverage') {
            agent {
                docker {
                    image 'node:24'
                    args '-u root:root'
                }
            }
            steps {
                // If coverage fails, mark stage unstable but keep overall build SUCCESS
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE', message: 'Coverage threshold not met') {
                    sh 'npm run coverage'
                }
                // publishHTML([...])  // optional HTML report publish
            }
        }

        stage('Build Publish Image') {
            steps {
                sh 'docker build -t siddharth67/solar-system:$GIT_COMMIT .'
                withDockerRegistry([credentialsId: 'docker-hub-credentials', url: ""]) {
                    sh 'docker push siddharth67/solar-system:$GIT_COMMIT'
                }
            }
        }

        stage('Trivy Vulnerability Scanner') {
            steps {
                sh '''
                trivy image siddharth67/solar-system:$GIT_COMMIT --severity CRITICAL --exit-code 1 --quiet --format json -o trivy-image-CRITICAL-results.json
                trivy convert --format template --template "@/usr/local/share/trivy/templates/html.tpl" --output trivy-image-CRITICAL-results.html trivy-image-CRITICAL-results.json
                '''
                // publishHTML(...) to show the Trivy HTML report in Jenkins
            }
        }
    }
}
```

Pipeline stages at a glance

| Stage                       | Purpose                                  | Key commands                       | Artifacts                               |
| --------------------------- | ---------------------------------------- | ---------------------------------- | --------------------------------------- |
| Installing Dependencies     | Install project dependencies             | `npm install --no-audit`           | `node_modules/` (workspace)             |
| NPM Dependency Audit        | Quick audit for npm vulnerabilities      | `npm audit --audit-level=critical` | audit output                            |
| OWASP Dependency-Check      | Comprehensive SBOM-based scan            | `dependencyCheck` plugin           | `dependency-check-report.xml/html/json` |
| Unit Testing                | Run unit tests                           | `npm test`                         | JUnit XML (optional)                    |
| Code Coverage               | Generate coverage metrics                | `npm run coverage`                 | coverage reports (`lcov`, cobertura)    |
| Build & Publish Image       | Build Docker image & push to registry    | `docker build`, `docker push`      | Docker image on Docker Hub              |
| Trivy Vulnerability Scanner | Scan container image for vulnerabilities | `trivy image` + `trivy convert`    | Trivy JSON/HTML                         |

Notes:

* Node.js tool is managed by Jenkins and the pipeline runs Node steps inside Docker agents.
* Credentials for MongoDB, Docker Hub, and NVD API key are stored in Jenkins and referenced via `credentials()` and plugin parameters.
* Dependency-Check and Trivy produce XML/HTML/JSON reports; the repository includes commented `publishHTML`/`junit` lines — uncomment to publish artifacts in Jenkins.

> **lightbulb** Obtain an NVD API key and store it in Jenkins credentials. Using the API key reduces the time Dependency-Check spends downloading the NVD feed and improves scan reliability.

How to request an NVD API key (registration form)

<Frame>
  <img alt="Screenshot of a &#x22;Request an API Key&#x22; webpage (NVD) showing input fields for Organization Name, Email Address, and Organization Type, a Terms of Use text box with a checked &#x22;I agree&#x22; box, and a Submit button. The browser window and tabs are visible along the top." />
</Frame>

* Request the API key at: `https://nvd.nist.gov/developers/request-an-api-key`
* After receiving the API key, create a Jenkins credential (Secret text) and reference that credential id in the Dependency-Check plugin configuration (`nvdCredentialsId`).

Triggering builds and inspecting results
I triggered the pipeline manually (this job does not leverage webhooks). Blue Ocean shows each stage and the step-by-step progress.

<Frame>
  <img alt="A screenshot of a Jenkins Blue Ocean pipeline page for &#x22;ci-pipeline-poll-scm #26&#x22; showing staged steps (Start, Installing Dependencies, Dependency Scanning, Unit Testing, Code Coverage, Build Publish Image, Trivy Vulnerability Scanner, End). The pipeline is queued with a message &#x22;Waiting for run to start&#x22; and shows NPM/OWASP dependency checks." />
</Frame>

Dependency scanning behavior

* Installing Dependencies stage runs `npm install` inside a Docker container.
* Dependency Scanning runs:
  * `npm audit --audit-level=critical`
  * OWASP Dependency-Check via the plugin which writes XML/HTML/JSON/SARIF/JUnit reports into the workspace.

When OWASP Dependency-Check finds vulnerabilities above configured thresholds, the `dependencyCheckPublisher` step will fail the build. In this project the publisher was initially set to fail on medium/low severities, which caused builds to fail. I adjusted the publisher to fail only on critical vulnerabilities by setting `failedTotalCritical: 1` and removing medium/low thresholds.

Dependency-Check update output (first run example):

```text theme={null}
[INFO] Checking for updates
[INFO] NVD API has 1,304 records in this update
[INFO] Downloaded 1,304/1,304 (100%)
[INFO] Begin database defrag
[INFO] End database defrag
[INFO] Check for updates complete
```

Dependency-Check analysis output (example):

```text theme={null}
[INFO] Analysis Started
[WARN] Analyzing `/home/jenkins-agent/workspace/ci-pipeline-poll-scm/package-lock.json` - however, the node_modules directory does not exist. Please run `npm install` prior to running dependency-check
[INFO] Analysis Complete
[INFO] Writing XML report to: /home/jenkins-agent/workspace/ci-pipeline-poll-scm/dependency-check-report.xml
[INFO] Writing HTML report to: /home/jenkins-agent/workspace/ci-pipeline-poll-scm/dependency-check-report.html
...
Collecting Dependency-Check artifact
Parsing file /home/jenkins-agent/workspace/ci-pipeline-poll-scm/dependency-check-report.xml
Findings exceed configured thresholds
```

The UI showed one Medium vulnerability (example: `formidable:2.1.2` CVE-2025-46653). Because the publisher was originally configured to stop builds on medium/low findings, the pipeline failed until thresholds were relaxed.

<Frame>
  <img alt="A screenshot of a Jenkins &#x22;Dependency-Check Results&#x22; page showing a severity distribution bar and a table listing a vulnerability for the package &#x22;formidable:2.1.2&#x22; (CVE-2025-46653) marked as Medium with weakness CWE-338. The Jenkins sidebar and build/job navigation are visible on the left." />
</Frame>

Unit tests and coverage

* Unit Testing runs `npm test` inside the Docker agent and uses `retry(2)` to handle transient failures.
* Code Coverage runs `npm run coverage` (nyc). Coverage did not meet the global threshold in this run (\~79% vs expected 90%), so the coverage stage failed its threshold check. Because coverage was wrapped with `catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE', ...)`, the overall build remained successful while the coverage stage was marked unstable.

Unit test output (truncated):

```text theme={null}
+ npm test
> Solar System@6.7.6 test
> mocha app-test.js --timeout 10000 --reporter mocha-junit-reporter --exit
Server successfully running on port - 3000
```

Coverage failure output (example):

```text theme={null}
+ npm run coverage
> Solar System@6.7.6 coverage
> nyc --reporter cobertura --reporter lcov --reporter text --reporter json-summary mocha app-test.js --timeout 10000 --exit

  11 passing (6s)

ERROR: Coverage for lines (79.06%) does not meet global threshold (90%)
---------------------------------------------------------------------------
File | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s
---------------------------------------------------------------------------
All files | 79.54 | 33.33 | 70 | 79.06 |
app.js    | 79.54 | 33.33 | 70 | 79.06 | 23,49-50,58,62-67
---------------------------------------------------------------------------
script returned exit code 1
```

Docker image build, push and Trivy scan
The Build & Publish Image stage builds a Docker image tagged with the Git commit and pushes it to Docker Hub using stored Docker Hub credentials:

```text theme={null}
docker build -t siddharth67/solar-system:$GIT_COMMIT .
withDockerRegistry([credentialsId: 'docker-hub-credentials', url: ""]) {
  docker push siddharth67/solar-system:$GIT_COMMIT
}
```

Build output shows the image was built and pushed. Docker lint warnings remind you not to place secrets in images.

<Frame>
  <img alt="A screenshot of the Docker Hub &#x22;My Hub&#x22; Repositories page for the user &#x22;siddharth67.&#x22; It shows a list of repositories (e.g., siddharth67/solar-system, vault-app, numeric-app, mongo-db) with last-pushed timestamps and visibility set to Public." />
</Frame>

After pushing the image, the pipeline runs a Trivy scan for CRITICAL severity (configured to exit with non-zero when CRITICALs are found):

```bash theme={null}
trivy image siddharth67/solar-system:$GIT_COMMIT --severity CRITICAL --exit-code 1 --quiet --format json -o trivy-image-CRITICAL-results.json
trivy convert --format template --template "@/usr/local/share/trivy/templates/html.tpl" --output trivy-image-CRITICAL-results.html trivy-image-CRITICAL-results.json
```

In this run, Trivy did not find CRITICAL vulnerabilities and returned successfully. The JSON/HTML output can be published with `publishHTML` to surface results in Jenkins.

Wrapping up

* Both pipelines use the same `Jenkinsfile` from `jenkins-demo-org/solar-system`; the poll-SCM job adds a cron trigger.
* OWASP Dependency-Check and Trivy are integrated for dependency and container-image vulnerability checks. Provide an NVD API key to speed Dependency-Check database updates.
* Tests and coverage execute inside Docker agents. Use `catchError` in the coverage stage to surface coverage issues without failing the entire build.
* Artifacts produced (Dependency-Check HTML, Trivy HTML, JUnit XML, coverage reports) are present but publishing calls are commented out — uncomment `publishHTML` or `junit` lines in the Jenkinsfile to show these reports in Jenkins.
* Next steps: migrate this pipeline to GitHub Actions and enable publishing of test, coverage, and security reports from the CI workflow. See [GitHub Actions course](https://learn.kodekloud.com/user/courses/github-actions) for guidance.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/4ff3a393-a622-48d3-a0b5-4fb312c6c0a2/lesson/9f51b321-5e14-495c-80aa-30c8f2a0bae4)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/4ff3a393-a622-48d3-a0b5-4fb312c6c0a2/lesson/622281cb-3902-4ea3-857d-4b5493649485)
