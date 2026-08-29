# Migrating Jenkins to Another Node

Source: https://notes.kodekloud.com/docs/Advanced-Jenkins/Jenkins-Administration-and-Monitoring/Migrating-Jenkins-to-Another-Node/page

Step-by-step guide to migrate a self-managed Jenkins controller between VMs by archiving and restoring JENKINS_HOME, preserving jobs plugins credentials and configurations.

This guide walks through a simple, reliable process to migrate a self-managed Jenkins controller from one VM to another. The core steps are:

* Stop Jenkins on the source node
* Archive `JENKINS_HOME`
* Transfer the archive to the target
* Restore the archive on the target and fix ownership
* Start Jenkins on the target and verify

This approach preserves jobs, plugin data, credentials and other configuration stored under `JENKINS_HOME`.

<Frame>
  <img alt="Screenshot of a Jenkins CI dashboard in dark mode showing a list of build jobs with status icons, last success/failure times, and run durations. The left sidebar displays navigation items like New Item, Build History, Manage Jenkins, and a Build Queue." />
</Frame>

Example environment in this walkthrough:

* Source Jenkins VM IP: `64.227.*.*`
* Target (fresh Jenkins install) VM IP: `165.3.22.*`

Important: For package-based Jenkins installs the initial admin password for a fresh installation is stored at:

```bash theme={null}
$JENKINS_HOME/secrets/initialAdminPassword
