# Jenkins controller
root@jenkins-controller-1 in shared-libraries on ⬢ featureTrivyScan on ☁ (us-east-2)

# agent VM
root@ubuntu-docker-jdk17-node20 in ~
❯
```

## 1. Create the node in the Jenkins UI

Navigate to Manage Jenkins → Manage Nodes → New Node. Give the node a name (I used `ubuntu-agent`) and choose "Permanent Agent".

<Frame>
  <img alt="A screenshot of the Jenkins web UI on the &#x22;New node&#x22; page showing a node named &#x22;ubuntu-agent&#x22; with &#x22;Permanent Agent&#x22; selected. The dark-themed page includes a &#x22;Create&#x22; button to add the node." />
</Frame>

## 2. Configure node details

Fill out the node configuration form. Key fields and recommended values:

| Field                 | Purpose                                            | Example / Recommendation                                            |
| --------------------- | -------------------------------------------------- | ------------------------------------------------------------------- |
| Description           | Short description for admins                       | `Ubuntu agent for Docker & JDK17 builds`                            |
| Number of executors   | How many concurrent builds the node can run        | `1` (adjust based on resources)                                     |
| Remote root directory | Where the agent stores workspaces, logs, artifacts | `/home/jenkins-agent`                                               |
| Labels                | Tags to target jobs/pipeline stages to this node   | `ubuntu-docker-jdk17-node20`                                        |
| Usage                 | Node allocation policy                             | `Use this node as much as possible` or `Only build jobs with label` |
| Launch method         | How the node connects to controller                | `Launch agent by connecting it to the controller (JNLP)`            |
| Availability          | Keep online or bring online as needed              | `Keep this agent online as much as possible`                        |
| Node properties       | Extra monitoring, env vars, tool locations         | Optional: enable disk-space threshold, set Java path                |

<Frame>
  <img alt="A screenshot of a Jenkins &#x22;Manage Nodes&#x22; configuration page showing node settings like Number of executors (1), Remote root directory (/home/jenkins-agent) and Labels (ubuntu-docker-jdk17-node20). The Usage dropdown is open and set to &#x22;Use this node as much as possible.&#x22;" />
</Frame>

You can enable monitoring (disk-space threshold, environment variables, tool locations) in the Node properties section. In my example I enabled disk-space threshold monitoring and saved the node. After saving, the node will appear as created but offline until the agent process connects.

<Callout icon="lightbulb">
  Ensure the node's remote root directory exists or is writable by the user that will run the agent. Jenkins will create subdirectories (for example, `remoting`, workspaces) under that directory.
</Callout>

## 3. Download and run the agent on the node VM

On the agent machine, Jenkins provides `agent.jar`. The UI shows platform-specific launch instructions; the Unix commands below work on most Linux agents.

* Directly pass the secret on the command line:

```bash theme={null}
curl -sO http://64.227.187.25:8080/jnlpJars/agent.jar
java -jar agent.jar -url http://64.227.187.25:8080/ \
  -secret [SECRET_REDACTED] \
  -name "ubuntu-agent" -workDir "/home/jenkins-agent"
```

* (Safer) store the secret in a file and reference it:

```bash theme={null}
echo [SECRET_REDACTED] > secret-file
curl -sO http://64.227.187.25:8080/jnlpJars/agent.jar
java -jar agent.jar -url http://64.227.187.25:8080/ \
  -secret @secret-file -name "ubuntu-agent" -workDir "/home/jenkins-agent"
```

Requirements and notes:

* The agent machine must have Java (JRE or JDK) installed. Matching the controller's major Java version is recommended for remoting compatibility.
* `-workDir` is where remoting stores logs and data (e.g., `/home/jenkins-agent/remoting`).

## 4. Troubleshooting common connection errors

If the agent cannot connect, the remoting client logs will show errors. A common failure is this 404 when the controller's inbound TCP agent listener is disabled:

```text theme={null}
Nov 10, 2024 6:17:12 AM org.jenkinsci.remoting.engine.WorkDirManager setupLogging
INFO: Both error and output logs will be printed to /home/jenkins-agent/remoting
Nov 10, 2024 6:17:12 AM hudson.remoting.Launcher createEngine
INFO: Setting up agent: ubuntu-agent
Nov 10, 2024 6:17:12 AM hudson.remoting.Engine startEngine
INFO: Using Remoting version: 3248.3250.v3277a_8e88c9b_
Nov 10, 2024 6:17:12 AM hudson.remoting.Launcher$CuiListener status
INFO: Locating server among [http://64.227.187.25:8080/]
Nov 10, 2024 6:17:12 AM hudson.remoting.Launcher$CuiListener status
INFO: Could not locate server among [http://64.227.187.25:8080/]; waiting 10 seconds before retry
java.io.IOException: http://64.227.187.25:8080/tcpSlaveAgentListener/ is invalid: 404 Not Found
    at org.jenkinsci.remoting.engine.JnlpAgentEndpointResolver.resolve(JnlpAgentEndpointResolver.java:229)
    at hudson.remoting.Engine.innerRun(Engine.java:829)
    at hudson.remoting.Engine.run(Engine.java:574)
```

This 404 indicates the controller's inbound TCP agent listener is disabled (the default for security reasons). To enable JNLP/inbound agents:

* Go to Manage Jenkins → Configure Global Security → Agents → TCP port for inbound agents.
* Choose a fixed port or allow a random port.
* Save and retry the agent run.

<Frame>
  <img alt="A dark-mode browser screenshot of the Jenkins &#x22;Manage Jenkins → Security&#x22; settings page showing the Markup Formatter set to &#x22;Safe HTML&#x22; and the Agents section with TCP port options (Fixed selected and a port input field). Save and Apply buttons are visible at the bottom." />
</Frame>

<Callout icon="warning">
  Enabling an inbound TCP port allows agents to connect to the controller. Secure this by restricting access with firewalls, VPNs, or IP allowlists and always use the agent secret. Exposing Jenkins' agent listener to untrusted networks can lead to unauthorized access.
</Callout>

## 5. Successful connection example

After enabling the TCP listener and running the agent, the remoting logs will show a successful handshake and connection:

```text theme={null}
Nov 10, 2024 6:18:34 AM org.jenkinsci.remoting.engine.WorkDirManager setupLogging
INFO: Both error and output logs will be printed to /home/jenkins-agent/remoting
Nov 10, 2024 6:18:34 AM hudson.remoting.Launcher createEngine
INFO: Setting up agent: ubuntu-agent
Nov 10, 2024 6:18:34 AM hudson.remoting.Engine startEngine
INFO: Using Remoting version: 3248.3250.v3277a_8e88c9b_
Nov 10, 2024 6:18:34 AM org.jenkinsci.remoting.engine.JnlpAgentEndpointResolver resolve
INFO: Remoting server accepts the following protocols: [JNLP4-connect, Ping]
Nov 10, 2024 6:18:34 AM hudson.remoting.Launcher$CuiListener status
INFO: Agent discovery successful
    Agent address: 64.227.187.25
    Agent port: 42851
    Identity: 67:e8:89:86:98:92:ee:21:8a:73:c2:77:fc:2d:07:37
Nov 10, 2024 6:18:34 AM hudson.remoting.Launcher$CuiListener status
INFO: Handshaking
Nov 10, 2024 6:18:34 AM hudson.remoting.Launcher$CuiListener status
INFO: Connecting to 64.227.187.25:42851
Nov 10, 2024 6:18:38 AM hudson.remoting.Launcher$CuiListener status
INFO: Remote identity confirmed: 67:e8:89:86:98:92:ee:21:8a:73:c2:77:fc:2d:07:37
Nov 10, 2024 6:18:38 AM hudson.remoting.Launcher$CuiListener status
INFO: Connected
```

On the agent filesystem you will see the agent files and the `remoting` directory Jenkins creates:

```bash theme={null}
root@ubuntu-docker-jdk17-node20 in /home via v17.0.12
$ ls
agent.jar  jenkins-agent

$ cd jenkins-agent/
$ ls
remoting
```

## 6. Inspect the node in the Jenkins UI

Once online, the node shows additional information and management options in Manage Nodes:

* Agent configuration history (view and restore previous node configs)
* Monitoring (JavaMelody) for threads, memory, and processes
* Node logs and load statistics
* Actions like disconnect or mark offline

<Frame>
  <img alt="A Jenkins web UI screenshot showing the &#x22;Agent Configuration History&#x22; page for an &#x22;ubuntu-agent&#x22; node. The left sidebar lists node actions (Delete Agent, Configure, Build History) and a table shows a config entry by user &#x22;siddharth.&#x22;" />
</Frame>

<Frame>
  <img alt="A screenshot of the Jenkins web UI showing the &#x22;JavaMelody Monitoring&#x22; page for an &#x22;ubuntu-agent&#x22; node. The page lists system reports (View Threads, OS Processes, Memory histogram, MBeans) and system actions (execute garbage collector, generate a heap dump) with left-side navigation." />
</Frame>

Example console info when the agent is connected:

```text theme={null}
Inbound agent connected from 165.232.191.207/165.232.191.207:55522
Remoting version: 3248.3250.v3277a_8e88c9b_
Launcher: JNLPLauncher
Communication Protocol: JNLP4-connect
This is a Unix agent
Agent successfully connected and online
```

## Next steps and references

* Target pipeline stages to this node by its label in a declarative pipeline:

```groovy theme={null}
pipeline {
  agent none
  stages {
    stage('Build on Ubuntu agent') {
      agent { label 'ubuntu-docker-jdk17-node20' }
      steps {
        sh 'uname -a && java -version'
      }
    }
  }
}
```

Useful links:

* Jenkins agents documentation: [https://www.jenkins.io/doc/book/using/using-agents/](https://www.jenkins.io/doc/book/using/using-agents/)
* Jenkins remoting and JNLP agents: [https://www.jenkins.io/doc/book/architectures/agents/](https://www.jenkins.io/doc/book/architectures/agents/)
* Jenkins security and node management: [https://www.jenkins.io/doc/book/managing/security/](https://www.jenkins.io/doc/book/managing/security/)

You can now use this node to run builds and pipeline stages targeted by label.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-jenkins/module/d1f217e1-bfef-4ba3-adf8-1411e911e0bc/lesson/8fb04397-a436-418a-af28-1f6f99967190" />
</CardGroup>


# Types of Agents

Source: https://notes.kodekloud.com/docs/Advanced-Jenkins/Agents-and-Nodes-in-Jenkins/Types-of-Agents/page

Overview of Jenkins agent types, their uses, and Declarative Pipeline agent declarations with examples and best practices for choosing between permanent, Docker, cloud, and label-based agents.

Let's review common Jenkins agent types and how to declare them in a Jenkinsfile. Agents extend the Jenkins controller by running executors on remote nodes and provide the execution environment for pipeline steps. An agent defines how a node connects to the controller — including the communication protocol and authentication method (for example, JNLP or SSH) — and the node where build tools and dependencies must be installed.

<Frame>
  <img alt="A slide titled &#x22;Jenkins Architecture&#x22; showing a pink &#x22;Agent&#x22; box with two blue &#x22;Executors&#x22; inside. To the right are two numbered notes: &#x22;Agents use executors on remote nodes&#x22; and &#x22;Agents connect to controller via protocols.&#x22;" />
</Frame>

In addition to long-lived (static) agents, Jenkins supports container- and cloud-based agents that spawn ephemeral environments. Docker-based agents run each job in a fresh container built from a specified image, which is ideal when jobs require precise software versions or complex dependencies. This isolation ensures reproducible builds and prevents dependency conflicts between projects.

<Frame>
  <img alt="A Jenkins architecture diagram showing a Jenkins Controller Node (with Plugins, Jobs, Nodes, Credentials, Configurations). It connects via SSH and JNLP to Jenkins Worker Nodes (Linux and Windows) that run agents and executors." />
</Frame>

Agents are simply worker machines — physical, virtual, or containerized — that connect to the Jenkins controller and execute pipeline steps. Choosing the right agent type helps you balance cost, performance, and reproducibility for your CI/CD workloads.

<Frame>
  <img alt="A slide titled &#x22;Jenkins Architecture&#x22; with a large blue Docker whale icon on the left. Three numbered callouts on the right explain using Docker containers as Jenkins build agents: pre-defined images, support for specific software versions/dependencies, and isolated clean environments." />
</Frame>

Common agent types and when to use them:

| Agent Type                                | When to use                                                                                                                     | Notes / Example                                                                             |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Permanent (dedicated) agents              | When you need stable, long-lived machines with preinstalled tools (for example, corporate build servers with licensed software) | Use when consistency is more important than elasticity; can be resource-intensive if idle   |
| Docker agents                             | When builds need specific tool versions or isolated environments (for example, Node.js or Python builds)                        | Each job runs in a fresh container based on a Docker image; ideal for reproducible builds   |
| Cloud-based agents (including Kubernetes) | For on-demand scaling and pay-as-you-go CI/CD (for example, AWS EC2, Azure, or K8s pods)                                        | Jenkins provisions ephemeral VMs or pods and terminates them after the job completes        |
| Label-based agents                        | When you want flexible assignment based on capabilities (for example, `java`, `windows`, `nodejs`)                              | Pipelines request a label and Jenkins matches the job to an available agent with that label |

Below are Declarative Pipeline examples showing common agent declarations inside a Jenkinsfile.

Example 1 — Run the pipeline on any available agent:

```groovy theme={null}
pipeline {
    agent any   // Use any available agent
    stages {
        stage('Build') {
            steps {
                sh 'echo "Running on $NODE_NAME"'
            }
        }
    }
}
```

Example 2 — Run the pipeline on an agent with a specific label:

```groovy theme={null}
pipeline {
    agent {
        label 'my-agent'   // Run on an agent labeled "my-agent"
    }
    stages {
        stage('Build') {
            steps {
                sh 'echo "Running on $NODE_NAME"'
            }
        }
    }
}
```

Example 3 — Use a Docker image as the agent:

```groovy theme={null}
pipeline {
    agent {
        docker {
            image 'node:latest'                   // Use a Docker image with Node.js
            args  '-v $HOME/.npm:/root/.npm'     // Optional: mount npm cache
        }
    }
    stages {
        stage('Build') {
            steps {
                sh 'node --version'
                sh 'npm --version'
            }
        }
    }
}
```

Example 4 — Default (root-level) agent with a stage-level override:

```groovy theme={null}
pipeline {
    agent {
        label 'MyAgent'   // Default agent used by stages unless overridden
    }
    stages {
        stage('Build') {
            agent { label 'nodejs-agent' }   // This stage uses a different agent
            steps {
                sh 'echo "Running build on $NODE_NAME"'
                sh 'node --version'
            }
        }
        stage('Test') {
            steps {
                sh 'echo "Running tests on $NODE_NAME"'   // Uses default MyAgent
            }
        }
    }
}
```

<Callout icon="lightbulb">
  Best practice: set a root-level agent to provide sensible defaults for most stages, and override at the stage level when a specific environment is required (for example, a `nodejs` Docker image or a `windows` agent). When using shell steps, reference the agent name with `"$NODE_NAME"` (or `$NODE_NAME` in POSIX shells) so the job output clearly indicates which node executed the step.

  See also: [Jenkins Agents Documentation](https://www.jenkins.io/doc/book/system-administration/agents/) and [Using Docker with Jenkins](https://www.jenkins.io/doc/book/pipeline/docker/).
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-jenkins/module/d1f217e1-bfef-4ba3-adf8-1411e911e0bc/lesson/16fb202a-ae53-4ebf-bed1-74b7e3d00170" />
</CardGroup>
