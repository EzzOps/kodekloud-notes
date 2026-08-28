# Demo Migrating Jenkins to Another Node

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Jenkins-Administration-and-Monitoring-Part-2/Demo-Migrating-Jenkins-to-Another-Node/page

This article provides a step-by-step guide to migrate a Jenkins controller from one VM to another without data loss.

In this step-by-step guide, you’ll learn how to migrate your Jenkins controller—including all configurations, plugins, and jobs—from one VM to another. We’ll walk through creating a backup on the **source node**, transferring it to the **target node**, and restoring everything so Jenkins comes up with zero data loss.

## Environment Overview

| VM Name                    | IP Address      | Role        |
| -------------------------- | --------------- | ----------- |
| jenkins-controller-1       | 64.227.x.x      | Source node |
| ubuntu-docker-jdk17-node20 | 165.232.191.207 | Target node |

## Prerequisites

* Jenkins versions must match on both VMs.
* JDK versions must be identical.
* You need `root` (or sudo) access on both machines.

<Callout icon="triangle-alert">
  If the Jenkins or JDK versions differ, you risk plugin incompatibilities or startup failures.\
  Always verify versions before proceeding.
</Callout>

***

## 1. Archive Jenkins on the Source Node

### 1.1 Connect via SSH

```bash theme={null}
ssh root@64.227.x.x
```

### 1.2 Verify the Jenkins Home Directory

```bash theme={null}
cd /var/lib
ls -ld jenkins
```

<Callout icon="lightbulb">
  You should see `jenkins` owned by the `jenkins` user with proper read/write permissions.
</Callout>

### 1.3 Stop and Disable Jenkins

```bash theme={null}
systemctl stop jenkins
systemctl disable jenkins
```

### 1.4 Create a Compressed Backup

```bash theme={null}
cd /var/lib
tar -czf jenkins-backup.tar.gz jenkins
```

### 1.5 Confirm the Backup

```bash theme={null}
ls -lh jenkins-backup.tar.gz
```

***

## 2. Copy the Backup to the Target Node

Use `scp` to securely transfer the backup file:

```bash theme={null}
scp /var/lib/jenkins-backup.tar.gz root@165.232.191.207:/tmp/
```

***

## 3. Prepare the Target Node

### 3.1 SSH into the Target

```bash theme={null}
ssh root@165.232.191.207
```

### 3.2 Inspect Current Jenkins Status

```bash theme={null}
systemctl status jenkins
```

<Callout icon="lightbulb">
  On fresh installs, Jenkins displays a “Getting Started” page and prompts for an initial admin password. Retrieve it from:

  ```text theme={null}
  /var/[AWS_SECRET_ACCESS_KEY]
  ```
</Callout>

### 3.3 Stop and Disable Jenkins

```bash theme={null}
systemctl stop jenkins
systemctl disable jenkins
```

### 3.4 Deploy the Backup

```bash theme={null}
