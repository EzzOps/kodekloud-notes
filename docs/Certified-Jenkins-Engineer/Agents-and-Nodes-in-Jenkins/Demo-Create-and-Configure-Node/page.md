# Demo Create and Configure Node

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Agents-and-Nodes-in-Jenkins/Demo-Create-and-Configure-Node/page

This tutorial demonstrates how to create and configure a Jenkins node to enhance build execution scalability and performance.

This tutorial shows how to offload build execution from your Jenkins controller to a dedicated agent (node), improving scalability and performance. We’ll provision an Ubuntu VM (`ubuntu-docker-jdk17-node20`) and connect it as a Jenkins agent using JNLP.

## Prerequisites

* A running Jenkins controller ([installation guide](https://www.jenkins.io/doc/))
* A VM with a matching JDK installed
* Network connectivity between controller and agent

## 1. Add a New Node in Jenkins

1. On the Jenkins controller, go to **Manage Jenkins** → **Manage Nodes and Clouds**.
2. Click **New Node**, enter a name (e.g., `Ubuntu-Agent`), select **Permanent Agent**, and **OK**.

<Frame>
  ![The image shows a Jenkins dashboard displaying node information, including architecture, clock difference, and disk space details. The interface is dark-themed with options to manage nodes and configure monitors.](https://kodekloud.com/kk-media/image/upload/v1752870292/notes-assets/images/Certified-Jenkins-Engineer-Demo-Create-and-Configure-Node/jenkins-dashboard-node-info-dark.jpg)
</Frame>

3. Fill in the node configuration:

| Field                 | Purpose                                                    | Example                                                     |
| --------------------- | ---------------------------------------------------------- | ----------------------------------------------------------- |
| Description           | Brief summary of this agent’s role                         | `Ubuntu build executor`                                     |
| # of Executors        | Max concurrent builds this agent can run                   | `2`                                                         |
| Remote Root Directory | Directory on the agent for workspaces, logs, and artifacts | `/home/jenkins-agent`                                       |
| Labels                | Tags for targeting in jobs or pipelines                    | `docker jdk17 ubuntu`                                       |
| Usage                 | Restrict builds to labels matching this node               | `Only build jobs with label expressions matching this node` |
| Launch method         | How the agent connects (e.g., JNLP)                        | `Launch agent by connecting from the controller`            |
| Availability          | Agent online policy                                        | `Keep this agent online as much as possible`                |

<Frame>
  ![The image shows a Jenkins configuration page for creating a new node, with fields for description, number of executors, remote root directory, and labels.](https://kodekloud.com/kk-media/image/upload/v1752870294/notes-assets/images/Certified-Jenkins-Engineer-Demo-Create-and-Configure-Node/jenkins-new-node-configuration.jpg)
</Frame>

<Callout icon="lightbulb">
  Under **Node Properties**, you can add environment variables or enable disk space monitoring to maintain agent health.
</Callout>

<Frame>
  ![The image shows a Jenkins dashboard interface with node properties settings, including disk space monitoring thresholds and environment variables. There are options to add variables and save changes.](https://kodekloud.com/kk-media/image/upload/v1752870295/notes-assets/images/Certified-Jenkins-Engineer-Demo-Create-and-Configure-Node/jenkins-dashboard-node-properties-settings.jpg)
</Frame>

4. Click **Save**. The agent remains **offline** until it connects to the controller.

## 2. Enable TCP Inbound Agent Port

1. Navigate to **Manage Jenkins** → **Configure Global Security**.
2. Under **Agents** → **TCP port for inbound agents**, select **Fixed** or **Random**.
3. Click **Save**.

## 3. Connect the Agent from the Command Line

On the agent VM (`ubuntu-docker-jdk17-node20`):

```shell theme={null}
