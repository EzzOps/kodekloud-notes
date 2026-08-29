# Demo Validating Backup

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Backup-and-Configuration-Management/Demo-Validating-Backup/page

This guide explains how to manually back up and validate a Jenkins home directory to ensure complete restoration in case of failure.

In this guide, we'll walk through manually backing up your Jenkins home directory and validating the archive in an isolated environment. This process helps ensure you can fully restore Jenkins configuration, jobs, plugins, and credentials in the event of a failure.

## 1. Locate the Jenkins Home Directory

List the contents of `/var/lib` and filter for “jenkins” to identify the home directory and any existing backups:

```bash theme={null}
root@host:/var/lib# ls | grep -i jenkins
drwxr-xr-x 28 jenkins jenkins    12288 Feb  7 07:05 jenkins/
-rw-r--r--  1 root    root 2209944892 Feb  3 09:00 jenkins-EOF.tar.gz
drwxr-xr-x 10 jenkins jenkins     4096 Feb  3 08:59 jenkins.bak/
```

You should see:

* **jenkins/** – the active Jenkins home directory.
* Any previous archives like `jenkins-EOF.tar.gz`.

The default Jenkins home path is `/var/lib/jenkins`.

## 2. Create a Compressed Backup

Use `tar` to archive and compress the entire Jenkins home directory, saving it under `/tmp` with a timestamped filename:

```bash theme={null}
root@host:/var/lib# tar -zcvf \
  /tmp/jenkins_home-$(date +"%Y%m%d%H%M").tar.gz \
  jenkins
```

This command will:

* Recursively package `jenkins/`.
* Compress the archive (`.tar.gz`).
* Name it with the current date and time (e.g., `202502070714`).

<Callout icon="lightbulb">
  Using a timestamp in your backup filename (e.g., `$(date +"%Y%m%d%H%M")`) makes tracking and rotating archives much easier.
</Callout>

Depending on the data size, this may take a few minutes.

## 3. Verify the Backup Archive

After the `tar` command completes, confirm the archive exists and check its size:

```bash theme={null}
root@host:/var/lib# ls -lh /tmp/jenkins_home-*.tar.gz
-rw-r--r-- 1 root root 2.0G Feb  7 07:17 /tmp/jenkins_home-202502070714.tar.gz
```

A few gigabytes is common for Jenkins installations with extensive job history and plugins.

## 4. Prepare a Test Environment

To validate the integrity of your backup without impacting production, create a sandbox copy:

1. **Stop the Jenkins service** to avoid data changes during copy.
2. **Copy** the home directory to `/tmp/jenkins-backup`.
3. **Inspect** the backup contents.

### 4.1 Stop Jenkins

<Callout icon="triangle-alert">
  Stopping the production Jenkins service may interrupt active builds. Perform this step during a maintenance window.
</Callout>

```bash theme={null}
root@host:/var/lib# systemctl stop jenkins
```

### 4.2 Extract or Copy

```bash theme={null}
root@host:/var/lib# cp -r jenkins /tmp/jenkins-backup
root@host:/var/lib# cd /tmp/jenkins-backup
root@host:/tmp/jenkins-backup# ls
config.xml    jobs/       plugins/    secrets/    users/
queue.xml     scriptApproval.xml  tools/    updates/    workspace/
```

Common subdirectories in a Jenkins home backup:

| Subdirectory | Contents                        |
| ------------ | ------------------------------- |
| config.xml   | Main Jenkins configuration file |
| jobs/        | Job definitions & build history |
| plugins/     | Installed plugins               |
| secrets/     | Credentials and secret storage  |
| users/       | User accounts and permissions   |
| updates/     | Update-center metadata          |
| workspace/   | Active build workspaces         |

## 5. Point a Jenkins Instance at the Backup

Launch a standalone Jenkins instance using your sandboxed backup directory as `JENKINS_HOME`:

1. **Export the environment variable**:
   ```bash theme={null}
   root@host:/tmp/jenkins-backup# export JENKINS_HOME=/tmp/jenkins-backup
   ```
2. **Run the Jenkins WAR** on a non-standard port (e.g., 9999):
   ```bash theme={null}
   root@host:~# cd ~/jenkins-war
   root@host:~/jenkins-war# java -jar jenkins.war --httpPort=9999
   ```
3. **Monitor startup output**:
   ```text theme={null}
   Running from: /root/jenkins-war/jenkins.war
   Webroot: /tmp/jenkins-backup/war
   2025-02-07 07:21:04.103+0000 [id=1]  INFO  winstone.Logger#logInternal:
     Beginning extraction from war file
   2025-02-07 07:21:05.357+0000 [id=1]  INFO  hudson.WebAppMain#contextInitialized:
     Jenkins home directory: /tmp/jenkins-backup found at: EnvVars.masterEnvVars.get("JENKINS_HOME")
   2025-02-07 07:21:11.141+0000 [id=33] INFO  jenkins.lifecycle.Lifecycle#onReady:
     Jenkins is fully up and running
   ```

## 6. Validate in the Browser

Open your browser and navigate to:

```text theme={null}
http://<host>:9999
```

You should see the Jenkins login screen. After authentication, verify that:

* All your jobs are listed.
* Plugin manager shows installed plugins.
* Credentials, system configurations, and user accounts match production.

This successful validation confirms that your backup archive is complete and restorable.

***

## Links and References

* [Jenkins Backups and Restoration](https://www.jenkins.io/doc/book/system-administration/backing-up/)
* [Jenkins CLI Documentation](https://www.jenkins.io/doc/book/managing/cli/)
* [Jenkins War Runtime Options](https://www.jenkins.io/doc/book/managing/cli/#running-jenkins-cli-standalone)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/77043650-89c2-4ad3-bbd1-e06eabe35581/lesson/6e3f884d-f3c9-49be-853d-504e2008212d" />
</CardGroup>
