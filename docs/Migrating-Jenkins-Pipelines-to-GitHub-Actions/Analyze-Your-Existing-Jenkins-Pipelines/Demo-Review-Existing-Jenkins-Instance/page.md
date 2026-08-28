# Demo Review Existing Jenkins Instance

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Analyze-Your-Existing-Jenkins-Pipelines/Demo-Review-Existing-Jenkins-Instance/page

Reviewing and inventorying an existing Jenkins controller, jobs, agents, plugins, and credentials to plan migration to GitHub Actions or other CI platforms

Before migrating pipelines or running migrations, perform a focused review of the existing Jenkins controller, its job types, agents, plugins, and credentials. This helps identify compatibility issues, credentials that must be re-created, and any agent configuration needed when migrating to GitHub Actions or other CI platforms.

I’m running Jenkins on a VM reachable at `http://139.84.149.70:8080` and the controller version is 2.504.1. The instance hosts roughly four projects of mixed types (Freestyle, Declarative Pipeline, Scripted Pipeline) with various triggers (poll-based and SCM-based).

Here’s the Jenkins process observed on the host (Java flags shown):

```bash theme={null}
root@jenkins:~#
ps aux | grep -i jenkins
jenkins      940  0.5 10.0 6892276 1649636 ?        Ssl  May19   5:56 /usr/bin/java -Xms1G -Xmx2G -Djava.awt.headless=true -jar /usr/share/java/jenkins.war --webroot=/var/cache/jenkins/war --httpPort=8080
root        28174  0.0  0.0  6544  2304 pts/0    S+   12:45   0:00 grep --color=auto -i jenkins
```

The dashboard shows several pipelines and jobs (visible statuses, last build times, durations):

<Frame>
  <img alt="A Jenkins continuous-integration dashboard in dark mode showing several pipeline jobs with status icons, last success/failure times, and durations. The left sidebar displays navigation items like New Item, Build History, and Build Queue." />
</Frame>

## Quick configuration summary

| Item                   | Value                                              |
| ---------------------- | -------------------------------------------------- |
| Jenkins home directory | `/var/lib/jenkins`                                 |
| Controller executors   | `2`                                                |
| Jenkins URL            | Configured in System Settings (UI)                 |
| Controller version     | `2.504.1`                                          |
| Common job types       | Freestyle, Declarative Pipeline, Scripted Pipeline |
| Typical triggers       | Poll SCM, SCM webhooks                             |

<Frame>
  <img alt="A dark-themed Jenkins &#x22;System&#x22; settings page. It shows the Jenkins home directory (/var/lib/jenkins), a system message box, executors set to 2, and Save/Apply buttons." />
</Frame>

## Installed tools and notable plugins

This environment is primarily used for Node.js-based pipelines. High-level tools and plugins observed:

| Tool / Plugin                                      | Purpose                                                   |
| -------------------------------------------------- | --------------------------------------------------------- |
| Node.js installer                                  | Provides Node runtime for builds                          |
| OWASP Dependency-Check (`dependency-check 12.1.1`) | Dependency vulnerability scanning                         |
| Sysdig-related tool                                | Security/monitoring integrations                          |
| Local Docker                                       | Image build/push during pipelines                         |
| Various Jenkins plugins                            | Pipeline, SCM, JUnit, and others (some updates available) |

<Frame>
  <img alt="A dark‑theme screenshot of the Jenkins &#x22;Manage Jenkins → Tools&#x22; configuration page showing an OWASP-DepCheck tool entry. The &#x22;Install automatically&#x22; box is checked and the installer is set to &#x22;dependency-check 12.1.1&#x22;, with Add Docker, Save and Apply buttons visible." />
</Frame>

Plugin updates are visible in the UI; consider reviewing change logs before upgrading plugins during a migration:

<Frame>
  <img alt="A screenshot of the Jenkins web UI on the Plugins > Updates page showing a list of plugins available for update (e.g., bouncycastle API, commons-text, JUnit, Pipeline Graph Analysis). The interface includes a search bar, an &#x22;Update&#x22; button, and navigation links on the left." />
</Frame>

## Nodes and agents

* The built-in controller node provides two executors.
* There is an additional agent named `us-west-1-ubuntu-22`, which was offline at the time of inspection.

<Frame>
  <img alt="A screenshot of the Jenkins &#x22;Nodes&#x22; management page in dark theme showing a Built-In Node (Linux amd64) with free disk/swap stats and an offline agent named &#x22;us-west-1-ubuntu-22&#x22; reporting N/A metrics. The top toolbar shows a &#x22;New Node&#x22; button and the logged-in user &#x22;siddharth.&#x22;" />
</Frame>

### Connecting the agent manually

In this environment the controller is not configured for HTTPS agent communication, so the agent is launched manually using the agent JAR. On the agent host:

```bash theme={null}
