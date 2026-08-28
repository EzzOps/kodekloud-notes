# 1. Fetch advice from AdviceSlip API
curl -s https://api.adviceslip.com/advice > advice.json

# 2. Extract the advice text and validate word count (>5)
jq -r '.slip.advice' advice.json > advice.message
WORD_COUNT=$(wc -w < advice.message)
if [ "$WORD_COUNT" -le 5 ]; then
  echo "Advice: $(cat advice.message) has $WORD_COUNT words or less."
  exit 1
fi

# 3. Install cowsay and ensure the binary is in PATH
sudo apt-get update -y
sudo apt-get install cowsay -y
export PATH="$PATH:/usr/games:/usr/local/games"

# 4. Generate ASCII artwork
cat advice.message | cowsay -f "$(shuf -n 1 /usr/share/cowsay/cows)"
```

<Frame>
  ![The image shows a configuration screen for a build environment, with options to execute shell commands and add timestamps to the console output. There are sections for build steps and post-build actions, with buttons to save or apply changes.](https://kodekloud.com/kk-media/image/upload/v1752870859/notes-assets/images/Certified-Jenkins-Engineer-Demo-Working-with-Freestyle-Job/build-environment-configuration-screen.jpg)
</Frame>

### Script Breakdown

| Script Section           | Purpose                                                      |
| ------------------------ | ------------------------------------------------------------ |
| `curl` fetch             | Download JSON from AdviceSlip API                            |
| `jq` + `wc`              | Extract text and enforce a minimum of 6 words                |
| `apt-get install cowsay` | Install the Cowsay package                                   |
| `export PATH`            | Add `/usr/games` and `/usr/local/games` to the PATH          |
| `cowsay` render          | Pipe advice into a random cowsay template to produce artwork |

### Sample AdviceSlip API Response

```json theme={null}
{
  "slip": {
    "id": 135,
    "advice": "If you want to be happily married, marry a happy person."
  }
}
```

## 4. Save and Run the Job

* Click **Save**, then **Build Now**.
* On the first run, you may see an error because the workspace doesn’t exist yet:

<Frame>
  ![The image shows a Jenkins dashboard with an error message stating "Error: no workspace," indicating that a project needs a build to create a workspace. Various options like "Build Now" and "Configure" are visible on the left sidebar.](https://kodekloud.com/kk-media/image/upload/v1752870859/notes-assets/images/Certified-Jenkins-Engineer-Demo-Working-with-Freestyle-Job/jenkins-dashboard-error-workspace.jpg)
</Frame>

## 5. Investigate a Failed Build

A common failure occurs when Cowsay isn’t found in the PATH:

```console theme={null}
09:23:12 + curl -s https://api.adviceslip.com/advice
09:23:13 + sudo apt-get install cowsay -y
...
09:23:16 + cowsay -f unipony-smaller.cow
/tmp/jenkins*.sh: line 14: cowsay: not found
Build step 'Execute shell' marked build as failure
Finished: FAILURE
```

<Callout icon="triangle-alert">
  The Jenkins service user’s default environment may exclude `/usr/games`. Always export or globally configure PATH so that Jenkins can locate installed binaries.
</Callout>

## 6. Update the Script and Rebuild

After adding the `export PATH` line, save and run **Build Now** again. Success output:

<Frame>
  ![The image shows a Jenkins dashboard displaying the status of a build job titled "Generate ASCII Artwork." It includes details such as the start time, user, and duration of the build process.](https://kodekloud.com/kk-media/image/upload/v1752870861/notes-assets/images/Certified-Jenkins-Engineer-Demo-Working-with-Freestyle-Job/jenkins-dashboard-generate-ascii-artwork.jpg)
</Frame>

```console theme={null}
14:58:24 + sudo apt-get install cowsay -y
14:58:24 + export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/snap/bin:/usr/games:/usr/local/games
14:58:24 + cat advice.message
14:58:24 + cowsay -f vader.cow
  / Some people would be better off if they    \
  | took their own advice.                    |
   -------------------------------------------
          \   ^__^
           \  (oo)\_______
              (__)\       )\/\
                  ||----w |
                  ||     ||
              Cowth Vader

Finished: SUCCESS
```

## 7. Review Build History and Workspace

You can inspect past runs, access permalinks, and browse the workspace files:

<Frame>
  ![The image shows a Jenkins dashboard for a project called "Generate ASCII Artwork," displaying build history and permalinks for recent builds. The interface includes options like "Build Now," "Configure," and "Delete Project."](https://kodekloud.com/kk-media/image/upload/v1752870862/notes-assets/images/Certified-Jenkins-Engineer-Demo-Working-with-Freestyle-Job/jenkins-dashboard-generate-ascii-artwork-2.jpg)
</Frame>

<Frame>
  ![The image shows a Jenkins dashboard displaying the status of a build job named "Generate ASCII Artwork #2," which was completed successfully in 1.5 seconds. The build was started by a user and shows details like waiting time and build duration.](https://kodekloud.com/kk-media/image/upload/v1752870864/notes-assets/images/Certified-Jenkins-Engineer-Demo-Working-with-Freestyle-Job/jenkins-dashboard-generate-ascii-artwork-3.jpg)
</Frame>

## 8. (Optional) Configure Global Environment Variables

To avoid repeating `export PATH` in every job:

1. Go to **Manage Jenkins → Configure System**.
2. Under **Global properties**, check **Environment variables**.
3. Add:
   * **Name**: `PATH`
   * **Value**: `/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/snap/bin:/usr/games:/usr/local/games`

<Callout icon="lightbulb">
  When you override `PATH` globally, include the full default PATH. Jenkins does not expand environment variables in the value field. Alternatively, adjust `/etc/default/jenkins` or use the [Environment Injector Plugin](https://plugins.jenkins.io/envinject/) to append directories.
</Callout>

<Frame>
  ![The image shows a Jenkins system configuration page where environment variables are being set, with fields for "Name" and "Value" under "Global properties."](https://kodekloud.com/kk-media/image/upload/v1752870866/notes-assets/images/Certified-Jenkins-Engineer-Demo-Working-with-Freestyle-Job/jenkins-system-configuration-environment-variables.jpg)
</Frame>

***

## Links and References

* [Jenkins Freestyle Project](https://www.jenkins.io/doc/book/managing/projects/)
* [AdviceSlip REST API](https://api.adviceslip.com)
* [Cowsay GitHub Repository](https://github.com/shiena/cowsay)
* [Timestamp Plugin](https://plugins.jenkins.io/timestamper/)
* [Environment Injector Plugin](https://plugins.jenkins.io/envinject/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/7ab00946-0edd-4a13-b5c8-1b5001779f1c/lesson/a0827f66-dfb3-4e34-a723-5bc7c82e88fc" />
</CardGroup>


# Jenkins Architecture

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Jenkins-Setup-and-Interface/Jenkins-Architecture/page

Overview of Jenkins distributed architecture explaining controller, agents, nodes, executors, and deployment strategies for scalable, resilient CI/CD pipelines.

In this lesson we explain the Jenkins architecture and how its components interact to deliver scalable CI/CD automation. Understanding these roles helps you design resilient pipelines, distribute workloads, and scale build capacity as your projects grow.

Jenkins uses a distributed architecture to run pipelines across multiple machines. This model provides:

* Scalability — run builds and tests in parallel on many worker machines.
* Resilience — isolate failures to worker nodes and protect controller state.
* Centralized control — one controller coordinates jobs, plugins, and configuration.

## Jenkins Controller (the coordination hub)

The central component is the Jenkins Controller (historically called the "master"). The controller is responsible for:

* Authentication and authorization (user management and access control).
* Defining, scheduling, and monitoring jobs and pipelines.
* Hosting the web UI, managing plugins, and handling global configuration.
* Persisting metadata such as credentials, job definitions, and job history.

<Frame>
  <img alt="A Jenkins architecture diagram showing a Jenkins Controller Node containing Plugins, Jobs, Nodes, Credentials, and Configurations, labeled as &#x22;the mastermind&#x22; coordinating the CI/CD process. Below it are three colored tiles for Management Tasks, Job Management, and Providing Web Interface." />
</Frame>

For small or experimentation setups, a single Jenkins instance can act both as the controller and the build executor. This is convenient for getting started but is not recommended for production workloads.

## Deployment topologies: single-node vs. distributed

Separating the controller from worker nodes is the recommended production practice. Benefits include:

* Protecting controller configuration and state from job-side effects.
* Improving throughput by distributing build workloads.
* More predictable scaling—add more worker nodes when demand increases.

<Frame>
  <img alt="A Jenkins architecture diagram showing a Jenkins Controller Node containing Plugins, Jobs, Nodes, Credentials, and Configurations. Below it are two deployment options: Basic Deployment (controller and worker are the same) and Advanced Deployment (separate controller and worker nodes) with brief benefits." />
</Frame>

Use the basic (single-node) setup for demos, POCs, or very small projects. Use the distributed topology for team environments, CI pipelines that run resource-heavy tasks, or when compliance and isolation are required.

## Nodes, agents, and executors

Nodes (also called agents; legacy docs may use "slaves") are the worker machines that perform builds, tests, and deployments. They can be physical or virtual machines, VMs, containers, or pods.

* Connection protocols: Nodes connect to the controller via SSH or JNLP (Java Network Launching Protocol). See SSH and JNLP for details.
* Executors: Each node exposes a configurable number of executors — each executor is a slot that can run one build at a time. The number of executors determines concurrency on that node.
  * Assign more executors for parallel builds if the node has sufficient CPU, memory, and I/O.
  * Limit executors to avoid resource contention and unstable builds.

<Callout icon="lightbulb">
  Best practice: For isolation, assign one executor per node for critical or heavy tasks. On powerful machines, starting with one executor per CPU core is common—measure resource usage and tune executors accordingly.
</Callout>

An "agent" refers to the runtime/connection method enabling a node to accept work from the controller. Common agent approaches:

* SSH agents — controller connects over [SSH](https://www.openssh.com/) and launches the agent process on the node.
* JNLP agents — the node initiates a connection to the controller using [JNLP](https://www.jenkins.io/doc/book/using/agents/#jnlp-agents).
* Docker agents — builds execute inside containers using a specified Docker image, ensuring reproducible environments.
* Kubernetes agents — Jenkins provisions ephemeral pods in a Kubernetes cluster to run jobs on-demand and scale dynamically.

Tools and build dependencies must be available on the node or inside the container used by the agent. Container-based agents (Docker/Kubernetes) are especially useful when jobs need specific tool versions or isolated environments.

<Frame>
  <img alt="A Jenkins architecture diagram showing a central Jenkins Controller Node (with Plugins, Jobs, Nodes, Credentials, Configurations) connecting to multiple Jenkins Worker Nodes. The workers include Linux and Windows nodes running agents (Docker, Kubernetes or standard agents) with executors, connected via SSH or JNLP." />
</Frame>

## Quick comparison table

|        Component | Role                                      | When to use                                                       |
| ---------------: | ----------------------------------------- | ----------------------------------------------------------------- |
|       Controller | Coordinates jobs, stores config, hosts UI | Mandatory—central control plane                                   |
|     Node / Agent | Runs build/test/deploy tasks              | Use when you need isolation, platform-specific tools, or scaling  |
|         Executor | Concurrency slot on a node                | Tune per-node based on CPU/memory and job resource needs          |
|     Docker agent | Containerized, reproducible builds        | When you need specific toolsets per job or ephemeral environments |
| Kubernetes agent | Ephemeral pods, autoscaling               | For large-scale dynamic workloads and auto-provisioning builds    |

## How Jenkins schedules and runs work

* Define jobs and pipelines on the controller using the web UI, CLI, or REST API.
* The controller maintains the inventory of connected nodes and their free executors.
* When a job is triggered, the controller selects an appropriate node and allocates an executor.
* The agent on that node runs the build using available tools or inside a container, producing logs and artifacts.
* On completion, the node returns build status, artifacts, and logs to the controller for display, storage, and downstream processing.

This distributed model enables Jenkins to handle more concurrent builds and complex pipelines while retaining centralized visibility and management.

<Callout icon="warning">
  Do not run resource-intensive builds directly on the controller in production. Keep the controller focused on coordination, and run builds on dedicated worker nodes or containerized agents to avoid impacting Jenkins availability.
</Callout>

## References and further reading

* [Jenkins - Using Agents](https://www.jenkins.io/doc/book/using/agents/)
* [Jenkins - Remote Access API](https://www.jenkins.io/doc/book/using/remote-access-api/)
* [Jenkins - Managing Jenkins (CLI)](https://www.jenkins.io/doc/book/managing/cli/)
* [OpenSSH](https://www.openssh.com/)
* [Docker](https://www.docker.com/)
* [Kubernetes](https://kubernetes.io/)

This architecture—controller plus distributed agents—gives you flexibility to scale CI/CD pipelines, adopt container-based reproducibility, and maintain centralized administration of your Jenkins environment.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/7ab00946-0edd-4a13-b5c8-1b5001779f1c/lesson/ef254aa0-d7ac-49b4-b1da-cad4ea2b4bf7" />
</CardGroup>
