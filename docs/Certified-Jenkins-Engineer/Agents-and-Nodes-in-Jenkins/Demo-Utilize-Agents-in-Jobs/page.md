# Go to a working directory
cd /home

# Download the Jenkins agent JAR
curl -sO http://<JENKINS_HOST>:8080/jnlpJars/agent.jar

# (Optional) Store the agent secret securely
echo <SECRET_TOKEN> > secret-file
chmod 600 secret-file

# Launch the agent with JNLP
java -jar agent.jar \
  -url http://<JENKINS_HOST>:8080/ \
  -secret @secret-file \
  -name "ubuntu-agent" \
  -workDir "/home/jenkins-agent"
```

<Callout icon="triangle-alert">
  Keep the `secret-file` secure. Exposing the JNLP secret allows unauthorized agents to connect.
</Callout>

A successful connection shows:

```text theme={null}
INFO: Connected
Inbound agent connected from 165.233.191.207:55522
This is a Unix agent
Agent successfully connected and online
```

## 4. Verify the Agent in Jenkins

Return to **Manage Nodes and Clouds** and confirm `Ubuntu-Agent` is **online**:

<Frame>
  ![The image shows a Jenkins interface displaying system information for an "ubuntu-agent," with options to view system properties, environment variables, and other details. The sidebar includes various menu options like status, configure, and log.](https://kodekloud.com/kk-media/image/upload/v1752870296/notes-assets/images/Certified-Jenkins-Engineer-Demo-Create-and-Configure-Node/jenkins-ubuntu-agent-interface.jpg)
</Frame>

Use [JavaMelody Monitoring](https://javamelody.github.io/) for system reports:

<Frame>
  ![The image shows a Jenkins dashboard with JavaMelody Monitoring options for system reports and actions on an "ubuntu-agent" node. It includes options like viewing threads, OS processes, memory histograms, and executing system actions.](https://kodekloud.com/kk-media/image/upload/v1752870297/notes-assets/images/Certified-Jenkins-Engineer-Demo-Create-and-Configure-Node/jenkins-dashboard-javamelody-monitoring.jpg)
</Frame>

## 5. Inspect the Agent Workspace

On the agent VM:

```shell theme={null}
root@ubuntu-docker-jdk17-node20:/home# ls
agent.jar  jenkins-agent

root@ubuntu-docker-jdk17-node20:/home# cd jenkins-agent
root@ubuntu-docker-jdk17-node20:/home/jenkins-agent# ls
remoting
```

As builds run, Jenkins creates `workspaces`, `logs`, and `artifacts` directories under `/home/jenkins-agent`.

Next, we’ll run a sample job on this agent to demonstrate distributed execution.

## Links and References

* [Jenkins Documentation](https://www.jenkins.io/doc/)
* [Jenkins JNLP Agents](https://www.jenkins.io/doc/book/using/remote-agents/)
* [JavaMelody](https://javamelody.github.io/)
* [Jenkins CLI & Remoting](https://www.jenkins.io/doc/book/managing/cli/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/2175ebff-1a0f-4c0f-90ea-04e5fa96956f/lesson/34e5d199-7df1-4413-a04c-e9407edaee06" />
</CardGroup>


# Demo Utilize Agents in Jobs

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Agents-and-Nodes-in-Jenkins/Demo-Utilize-Agents-in-Jobs/page

Demonstrates using Jenkins agents to run Freestyle and Declarative Pipeline jobs on labeled external nodes, including stage-level agent overrides and workspace verification.

In this lesson we demonstrate how to use Jenkins agents (nodes) with both Freestyle and Declarative Pipeline jobs. You will learn how to:

* Run Freestyle jobs on an external agent using labels.
* Pin specific pipeline stages to a particular agent.
* Inspect workspace locations to verify where each stage or job executed.

Prerequisites: a running external agent registered with your Jenkins controller.

<Frame>
  <img alt="A screenshot of the Jenkins &#x22;Nodes&#x22; page showing two nodes (Built-In Node and ubuntu-agent) with architecture, free disk/swap/temp space, clock sync and response times. The left sidebar shows Build Queue and Build Executor Status and the top bar has the Jenkins header and user menu." />
</Frame>

## 1) Freestyle Job on an External Agent

Create a new Freestyle job — for example, name it `freestyle-external-agent`.

<Frame>
  <img alt="Screenshot of Jenkins' &#x22;New Item&#x22; page in dark mode. The item name field is filled with &#x22;freestyle-ex&#x22; and job-type options (Freestyle project, Pipeline, Multi-configuration project, Folder) are listed." />
</Frame>

In the job configuration:

* Add a build step "Execute shell" and include commands to print OS and Node/NPM versions:

```bash theme={null}
cat /etc/os-release
node -v
npm -v
```

* Under "Restrict where this project can be run", paste the external agent's label (for example `ubuntu-docker-jdk17-node20`) so the job executes on that agent.

After saving, the node should list the job as a project assigned to it.

<Frame>
  <img alt="A Jenkins web UI screenshot showing the node &#x22;ubuntu-docker-jdk17-node20&#x22; with one project listed (&#x22;freestyle-external-agent&#x22;) and columns for last success, failure, and duration. The left sidebar shows options like Overview, Configure, Load Statistics, and Open Blue Ocean." />
</Frame>

Example console output from a successful Freestyle build on the Ubuntu agent (note the "Building remotely" message and the workspace path on the agent):

```text theme={null}
Started by user siddharth
Running as SYSTEM
Building remotely on ubuntu-agent (ubuntu-docker-jdk17-node20) in workspace /home/jenkins-agent/workspace/freestyle-external-agent
[freestyle-external-agent] $ /bin/sh -xe /tmp/jenkins17351491148126919661.sh
+ cat /etc/os-release
PRETTY_NAME="Ubuntu 24.04 LTS"
...
+ node -v
v22.11.0
+ npm -v
10.9.0
[Gitea] do not publish assets due to source being no GiteaSCMSource
Finished: SUCCESS
```

<Callout icon="lightbulb">
  Running Freestyle jobs on labeled agents is an easy way to direct platform-specific or dependency-heavy builds to machines prepared with the required environment.
</Callout>

## 2) Pipeline Job with Stage-Level Agent Selection

Next, demonstrate the same checks using a Declarative Pipeline and show how to override the pipeline-level agent for a specific stage.

Import or create a repository in your Git hosting (Gitea in this example) and include a Jenkinsfile in the repo. In the UI, create a Pipeline job (for example `pipeline-external-agent`) and point its Pipeline script to the Jenkinsfile stored in the repository.

<Frame>
  <img alt="A dark-themed screenshot of a Gitea organization page for &#x22;dasher-org&#x22; showing a list of repositories (like shared-libraries and solar-system), with buttons for &#x22;New Repository&#x22; and &#x22;New Migration&#x22; and panels for Members and Teams. The top-right menu is open showing options to create a new repository, migration, or organization." />
</Frame>

If you need to import/migrate a repository, use your Git UI to clone or migrate into the desired organization (example below).

<Frame>
  <img alt="A screenshot of a web UI for migrating or cloning a Git repository. It shows fields for the source URL and access token, migration options, owner set to &#x22;dasher-org&#x22;, repository name &#x22;exploring-agents&#x22;, visibility and description inputs, and a &#x22;Migrate Repository&#x22; button." />
</Frame>

A compact Declarative Jenkinsfile that demonstrates a global agent with a stage-level agent override:

```groovy theme={null}
pipeline {
    agent any

    stages {
        stage('S1-Any Agent') {
            steps {
                sh 'cat /etc/os-release'
                sh 'node -v'
                sh 'npm -v'
            }
        }

        stage('S2-Ubuntu Agent') {
            agent {
                label 'ubuntu-docker-jdk17-node20'
            }
            steps {
                sh 'cat /etc/os-release'
                sh 'node -v'
                sh 'npm -v'
            }
        }
    }
}
```

<Callout icon="lightbulb">
  Defining an `agent` inside a `stage` overrides the pipeline-level agent for that stage — useful for running platform-specific builds or tests on dedicated machines.
</Callout>

Tip: Jenkins includes a Declarative Directive Generator (choose "agent" → "label") which can produce the correct agent snippet for you.

<Frame>
  <img alt="A screenshot of the Jenkins web UI showing the Declarative Directive Generator, with a form for configuring an agent (including a required label field) and a sidebar of documentation links. The top bar shows search, notifications and a user menu along with several browser tabs." />
</Frame>

After configuring the Pipeline job to use the repository Jenkinsfile and running a build, Jenkins performs a checkout and then runs stage steps. The pipeline UI highlights each stage and shows where each executed.

<Frame>
  <img alt="Screenshot of a Jenkins pipeline page for &#x22;pipeline-external-agent&#x22; showing a horizontal stage progress bar with completed stages (Checkout SCM, S1-Any Agent, S2-Ubuntu Agent) and the Jenkins left navigation menu." />
</Frame>

Example console output snippets to illustrate agent selection and workspace locations:

* Checkout and stage S1 run on the pipeline-level (global) agent — often the controller when `agent any` is satisfied there. Workspace example: `/var/lib/jenkins/workspace/pipeline-external-agent`.

```text theme={null}
Started by user siddharth
Obtained Jenkinsfile from git http://64.227.187.25:5555/dasher-org/exploring-agents
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins in /var/lib/jenkins/workspace/pipeline-external-agent
...
+ node -v
v20.16.0
+ npm -v
10.8.1
```

* Stage S2 uses the stage-level agent and runs on the specified Ubuntu agent. Workspace example on the agent: `/home/jenkins-agent/workspace/pipeline-external-agent`.

```text theme={null}
[Pipeline] stage
[Pipeline] { (S2-Ubuntu Agent)
[Pipeline] node
Running on ubuntu-agent in /home/jenkins-agent/workspace/pipeline-external-agent
...
+ cat /etc/os-release
PRETTY_NAME="Ubuntu 24.04 LTS"
...
+ node -v
v22.11.0
+ npm -v
10.9.0
```

## Workspace and Agent Comparison

| Agent scope                                     | Where it runs                     | Example workspace path                                 | Use case                                               |
| ----------------------------------------------- | --------------------------------- | ------------------------------------------------------ | ------------------------------------------------------ |
| Pipeline-level (`agent any`)                    | Controller or any available agent | /var/lib/jenkins/workspace/pipeline-external-agent     | General pipeline steps and SCM checkout                |
| Stage-level (`stage { agent { label '...' } }`) | Specified external agent          | /home/jenkins-agent/workspace/pipeline-external-agent  | Platform-specific build/test or dependency-heavy tasks |
| Freestyle job with label                        | Specified agent                   | /home/jenkins-agent/workspace/freestyle-external-agent | Jobs targeted to agents with required tools            |

<Callout icon="warning">
  Avoid running long-running or resource-intensive builds on the controller (master). Use labels to route those builds to dedicated agents to keep the controller responsive.
</Callout>

## Summary

* Use "Restrict where this project can be run" to pin Freestyle jobs to an agent by label.
* Use a stage-level `agent` in Declarative Pipeline to run a single stage on a specific node without affecting other stages.
* Verify where stages executed by inspecting console logs and the workspace paths shown for each node.

Further reading and references:

* [Jenkins Documentation — Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
* [Jenkins — Distributed builds and agents](https://www.jenkins.io/doc/book/using/using-agents/)
* [Gitea — Self-hosted Git service](https://gitea.io/en-us/)

That's all for now.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/2175ebff-1a0f-4c0f-90ea-04e5fa96956f/lesson/b51764ee-79f9-4a2f-ada8-f386a22ffe8a" />
</CardGroup>
