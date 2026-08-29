# Demo Backing upRestoring Jenkins

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Backup-and-Configuration-Management/Demo-Backing-upRestoring-Jenkins/page

This tutorial explains how to install, configure, and use the Thin Backup plugin for backing up and restoring Jenkins settings and job configurations.

In this tutorial, you’ll learn how to install, configure, and use the **Thin Backup** plugin to back up and restore Jenkins global settings, job configurations, and optionally build artifacts.

***

## 1. What Is the Thin Backup Plugin?

The Thin Backup plugin provides lightweight, configurable backups of Jenkins home content:

* Global configuration (`config.xml`, credentials).
* Job-specific configurations.
* Plugin definitions (optional).
* Build results and artifacts (optional).

![The image shows a webpage for the Jenkins plugin "ThinBackup," detailing its features, version information, and documentation links. It includes a description of the plugin's functionality and installation statistics.](https://kodekloud.com/kk-media/image/upload/v1752870409/notes-assets/images/Certified-Jenkins-Engineer-Demo-Backing-upRestoring-Jenkins/jenkins-thinbackup-plugin-details.jpg)

> **lightbulb** Thin Backup only stores essential configuration files by default. Use the optional settings to include plugins, artifacts, and zip archives.

***

## 2. Installing the Thin Backup Plugin

1. Navigate to **Manage Jenkins** → **Manage Plugins** → **Available**.
2. Search for **Thin Backup**.
3. Select and click **Install without restart** (or **Download now and install after restart**).

***

## 3. Configuring the Backup

1. Go to **Manage Jenkins** → **Configure System**.

2. Scroll to the **Thin Backup** section.

3. Set the **Backup Directory** to a path on disk, for example:

   ```bash theme={null}
   /var/lib/jenkins/Jenkins_backup
   ```

4. Configure scheduling and retention:

| Option                    | Description                                     | Default  |
| ------------------------- | ----------------------------------------------- | -------- |
| Schedule                  | Cron expression for automated backups           | (none)   |
| Differential backups      | Store only changed files since last full backup | Disabled |
| Max number of backup sets | Retain N backup sets                            | 10       |
| Exclude files             | Regex patterns to exclude specific files        | (none)   |

5. Choose additional settings:

   * Archive plugin files
   * Zip backup folders
   * Include build results and artifacts

> **triangle-alert** Backing up build results and artifacts can consume significant disk space. Monitor storage usage if you enable this option.

6. Click **Apply** then **Save**.

***

## 4. Triggering a Manual Backup

1. Go to **Manage Jenkins**.
2. Under **Tools and Actions**, click **Backup Now**.

This initiates an on-demand backup using your current configuration.

***

## 5. Monitoring Backup Logs

View progress and any issues in **Manage Jenkins** → **System Log** → **All Jenkins Logs**. Look for entries like:

```text theme={null}
INFO   ThinBackupMgmtLink      Starting manual backup.
INFO   HudsonBackup            No previous full backup found, creating one.
INFO   HudsonBackup            Found 16 jobs to back up.
INFO   HudsonBackup            Backup process finished successfully.
```

***

## 6. Verifying Backup Files on Disk

On the Jenkins server shell:

```bash theme={null}
cd /var/lib/jenkins/Jenkins_backup
ls
cd FULL-$(date +%Y-%m-%d)_$(date +%H-%M)/
ls
```

You should see directories for:

* `config.xml`
* `jobs/`
* `plugins/`
* `builds/` (if enabled)

***

## 7. Deleting and Restoring a Job

1. In the Jenkins UI, delete a sample job (e.g., **Monitor-Jenkins**).
2. Navigate to **Manage Jenkins** → **Thin Backup** → **Restore Configuration**.
3. Select the desired backup date and click **Restore**.

![The image shows a Jenkins interface with a "Restore Configuration" screen, where a backup date is selected for restoration. The sidebar includes options like "Manage Jenkins" and "Build History."](https://kodekloud.com/kk-media/image/upload/v1752870410/notes-assets/images/Certified-Jenkins-Engineer-Demo-Backing-upRestoring-Jenkins/jenkins-restore-configuration-interface.jpg)

4. Restart Jenkins for the restored items to appear.
5. Log back in and confirm the deleted job is restored with its build history.

***

## 8. Optional: Backing Up Build Results

To include build logs and artifacts in your backups:

1. Open **Manage Jenkins** → **Configure System**.
2. Under **Thin Backup**, enable **Backup build results and artifacts**.
3. Save changes and run a manual backup to capture builds.

![The image shows a Jenkins system configuration page with backup settings, including options for backup frequency and data to be backed up.](https://kodekloud.com/kk-media/image/upload/v1752870411/notes-assets/images/Certified-Jenkins-Engineer-Demo-Backing-upRestoring-Jenkins/jenkins-system-configuration-backup-settings.jpg)

***

## 9. Summary

You’ve now:

* Installed the Thin Backup plugin.
* Configured backup paths, schedules, and retention.
* Performed manual backups and monitored logs.
* Restored deleted jobs and configurations.
* Enabled optional build-data backups.

For advanced usage, explore differential backups, custom exclusion patterns, and integration with external storage.

## Links and References

* [Jenkins Thin Backup Plugin](https://plugins.jenkins.io/thinbackup/)
* [Jenkins Configuration as Code](https://www.jenkins.io/projects/jcasc/)
* [Managing Jenkins](https://www.jenkins.io/doc/book/managing/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/77043650-89c2-4ad3-bbd1-e06eabe35581/lesson/7cf62c6c-d25f-4f46-b3ff-ae5407f33d5f)
