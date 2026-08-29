# Backing upRestoring Jenkins Demo

Source: https://notes.kodekloud.com/docs/Advanced-Jenkins/Backup-and-Configuration-Management/Backing-upRestoring-Jenkins-Demo/page

Guide to using the ThinBackup Jenkins plugin to configure, schedule, inspect, and restore Jenkins configuration, jobs, and optional build artifacts.

This lesson demonstrates how to back up and restore Jenkins configuration and jobs using the ThinBackup plugin. ThinBackup captures global Jenkins configuration and job-level configuration, with support for scheduled backups, differential backups, limiting retained backup sets, and excluding files using regular expressions. You can also choose whether to archive backups (ZIP) and include build results or artifacts.

Key topics covered:

* Installing and configuring ThinBackup
* Triggering manual backups and viewing logs
* Inspecting backup sets on disk
* Restoring Jenkins and recovering deleted jobs
* Considerations for backing up build artifacts and history

<Frame>
  <img alt="A screenshot of the Jenkins plugin page for &#x22;ThinBackup,&#x22; showing the plugin documentation, badges, and details like Version 2.1.1 and installation stats. The dark-themed page also displays navigation tabs, descriptive text, and a small usage graph in the right sidebar." />
</Frame>

## Install and configure ThinBackup

1. Install the ThinBackup plugin from Manage Jenkins → Manage Plugins.
2. Open Manage Jenkins → Configure System and search for "Thin".
3. Configure the backup directory, schedule, type, and retention.

Example backup directory used in this demo:

```text theme={null}
/var/lib/jenkins/JENKINS_BACKUP
```

If the directory does not exist, ThinBackup creates it before the first run. Other relevant options include cron schedules (for automating backups), choosing Full vs Differential backups, limiting the maximum number of backup sets, and specifying regex patterns to exclude files from backups.

<Frame>
  <img alt="A dark-themed Jenkins system configuration page showing backup settings—fields for backup directory, full/differential schedules, max backup sets, excluded files, checkboxes for options, and Save/Apply buttons. An orange warning notes the specified backup directory does not exist and will be created before the first run." />
</Frame>

Recommended settings overview:

| Setting          | Purpose                                     | Example / Notes                                          |
| ---------------- | ------------------------------------------- | -------------------------------------------------------- |
| Backup directory | Where backup sets are stored                | `/var/lib/jenkins/JENKINS_BACKUP`                        |
| Schedule         | Automate backups                            | Cron expression, e.g., `H H * * *`                       |
| Backup type      | Full or differential                        | Use differential to reduce time/space after initial full |
| Max backup sets  | Retention to limit disk usage               | `5` (older backups removed automatically)                |
| Excluded files   | Avoid backing up large or unnecessary files | Use regex patterns                                       |

## Additional configuration options

After saving the ThinBackup configuration, you can select:

* Whether to include plugin archives in the backup
* Whether to include additional files
* Whether to compress backups (ZIP)
* Whether to include build archives (artifacts) and/or build results (history)

These options affect backup size and duration—select them according to recovery needs.

## Trigger a manual backup and view logs

To run a manual backup:
Manage Jenkins → Tools and Actions → Thin Backup → Backup Now.

ThinBackup logs only a few messages in its UI. For detailed messages, inspect Jenkins system logs:
Dashboard → Manage Jenkins → System Log → All Jenkins Logs.

Example condensed log output from a manual backup:

```text theme={null}
Nov 10, 2024 4:37:03 PM INFO org.jvnet.hudson.plugins.thinbackup.ThinBackupMgmtLink doBackupManual
Starting manual backup.

Nov 10, 2024 4:37:03 PM INFO org.jvnet.hudson.plugins.thinbackup.backup.HudsonBackup
No previous full backup found, thus creating one.

Nov 10, 2024 4:37:03 PM INFO org.jvnet.hudson.plugins.thinbackup.backup.HudsonBackup backupJobsDirectory
Found 16 jobs in /var/lib/jenkins/jobs to back up.

Nov 10, 2024 4:37:03 PM INFO org.jvnet.hudson.plugins.thinbackup.backup.HudsonBackup backupJobsDirectory
Found 3 jobs in /var/lib/jenkins/jobs/Gitea-Organization/jobs to back up.

Nov 10, 2024 4:37:21 PM INFO org.jvnet.hudson.plugins.thinbackup.ThinBackupPeriodicWork backupNow
Backup process finished successfully.
```

## Inspecting the backup on disk

ThinBackup writes each backup set into the configured backup directory as separate folders (for example, `FULL-YYYY-MM-DD_HH-MM`). To verify backup contents on the Jenkins controller:

```bash theme={null}
root@jenkins-controller-1:~# cd /var/lib/jenkins
root@jenkins-controller-1:/var/lib/jenkins# cd JENKINS_BACKUP/
root@jenkins-controller-1:/var/lib/jenkins/JENKINS_BACKUP# ls
FULL-2024-11-10_16-37
root@jenkins-controller-1:/var/lib/jenkins/JENKINS_BACKUP# cd FULL-2024-11-10_16-37/
root@jenkins-controller-1:/var/lib/jenkins/JENKINS_BACKUP/FULL-2024-11-10_16-37# ls
audit-trail.xml
backup-completed.info
com.cloudbees.hudson.plugins.folder.config.AbstractFolderConfiguration.xml
com.cloudbees.jenkins.plugins.bitbucket.endpoints.BitbucketEndpointConfiguration.xml
com.smartcodeltd.jenkinsci.plugins.buildmonitor.BuildMonitorView.xml
config.xml
credentials.xml
de.taimos.pipeline.aws.PluginImpl.xml
github-plugin-configuration.xml
hudson.model.UpdateCenter.xml
hudson.plugins.copyartifact.CopyArtifactConfiguration.xml
hudson.plugins.copyartifact.Triggered.xml
hudson.plugins.git.GitSCM.xml
hudson.plugins.git.GitTool.xml
hudson.plugins.sonar.MsBuildSQRunnerInstallation.xml
hudson.plugins.sonar.SonarGlobalConfiguration.xml
```

This folder contains global configuration files, plugin configuration, and job configuration XML files—everything ThinBackup considers essential for restoring Jenkins config and jobs.

## Restoring Jenkins from a backup

To restore:
Manage Jenkins → Thin Backup → Restore.

The plugin shows available backup sets. Select the desired backup and choose restore options—examples include restoring plugin archives and restoring next build number files. Click Restore to start the process.

<Frame>
  <img alt="A screenshot of the Jenkins web UI showing the &#x22;Restore Configuration&#x22; page from the ThinBackup plugin, with a dropdown to select a backup date (2024-11-10 16:37) and checkboxes to restore the next build number file and plugins. The Jenkins sidebar and build/executor status widgets are visible on the left." />
</Frame>

<Callout icon="warning">
  Restoring configuration may require a Jenkins restart for all changes to be applied cleanly. Plan restores during maintenance windows and ensure you have a current system snapshot in case you need to roll back.
</Callout>

### Example: restoring a deleted job

1. Delete the job you want to recover (for example, a pipeline named `monitor-jenkins`).
2. Use Manage Jenkins → Thin Backup → Restore and pick the backup set that contains that job.
3. After restoring, restart Jenkins if prompted or if the UI does not immediately reflect changes.

Example Pipeline configuration from the deleted job:

```groovy theme={null}
pipeline {
    agent any

    stages {
        stage('Hello') {
            steps {
                echo 'Hello World'
            }
        }
    }
}
```

After restart, the restored job and its build history should reappear in the Jenkins UI.

<Callout icon="lightbulb">
  Enabling backup of build results and artifacts will significantly increase backup size and duration. Consider whether you need full build archives or only job configuration and metadata for recovery. If you retain build artifacts, plan for additional storage and longer backups.
</Callout>

<Frame>
  <img alt="A dark-themed Jenkins pipeline page for a job called &#x22;monitor-jenkins,&#x22; showing a build history list on the left and Start/End timeline markers for several build numbers on the right." />
</Frame>

## Best practices and wrap-up

* Schedule regular full backups with periodic differential backups to balance recovery time and storage requirements.
* Limit the number of retained backup sets to avoid uncontrolled disk growth.
* Exclude large temporary files and workspace contents using regex exclusions unless you require them for recovery.
* Test restores periodically in a staging environment to ensure your backup strategy covers all critical data (jobs, credentials, plugin states).
* Keep plugin versions and Jenkins itself consistent between backup and restore environments to avoid compatibility problems.

You can run manual backups and restores at any time from Manage Jenkins → Thin Backup. ThinBackup provides a lightweight, configurable approach to saving Jenkins configuration and job definitions, with optional choices for plugins, build metadata, and artifacts.

<Frame>
  <img alt="A screenshot of the Jenkins web UI on the ThinBackup plugin page, with prominent &#x22;Backup now&#x22; and &#x22;Restore&#x22; buttons in the center. The dark-themed layout shows the Jenkins logo and a left navigation panel with items like Build History, Manage Jenkins, and Build Executor Status." />
</Frame>

Further reading and references:

* ThinBackup plugin: [https://plugins.jenkins.io/thinbackup/](https://plugins.jenkins.io/thinbackup/)
* Jenkins documentation: [https://www.jenkins.io/doc/](https://www.jenkins.io/doc/)
* Jenkins backups and disaster recovery best practices: [https://www.jenkins.io/doc/book/system-administration/backing-up/](https://www.jenkins.io/doc/book/system-administration/backing-up/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-jenkins/module/6f55f1ac-064a-4aec-a91a-450caaf82d63/lesson/931c35a2-7bf6-4a4d-96e3-8af677cb0149" />
</CardGroup>
