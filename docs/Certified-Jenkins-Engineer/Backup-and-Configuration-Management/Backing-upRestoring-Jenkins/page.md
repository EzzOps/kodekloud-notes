# Backing upRestoring Jenkins

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Backup-and-Configuration-Management/Backing-upRestoring-Jenkins/page

This guide covers methods for backing up and restoring Jenkins to ensure data integrity and disaster recovery.

Ensuring regular backups of your Jenkins instance is vital for disaster recovery, maintaining data integrity, and quickly restoring accidentally deleted configurations. This guide walks you through various backup methods and highlights the critical directories and files you should preserve.

<Callout icon="lightbulb">
  Schedule your backups according to your change management policy—daily incremental snapshots plus weekly full backups often strike a good balance between data safety and storage cost.
</Callout>

## Backup Approaches

Choose one or combine multiple methods to build a resilient backup strategy:

| Method                 | Description                                                                                 | Pros                                 | Cons                                       |
| ---------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------ | ------------------------------------------ |
| Filesystem Snapshots   | Use Linux LVM snapshots or cloud provider block snapshots for point-in-time consistency.    | Fast, consistent                     | Requires compatible storage subsystem      |
| Jenkins Backup Plugins | ThinBackup is the only actively maintained plugin for automated backup of Jenkins home.     | Easy setup, schedules automated jobs | Plugin limitations; may not catch all data |
| Custom Shell Scripts   | Scripts to `rsync` or `tar` the essential Jenkins directories to remote storage.            | Fully customizable                   | Requires maintenance and testing           |
| Hybrid Strategy        | Perform local backups first, then transfer archives to offsite or object storage (S3, GCS). | Maximizes redundancy                 | Involves additional network/config steps   |

## Essential Files and Directories

Jenkins stores all configuration, job definitions, plugins, and credentials in the **JENKINS\_HOME** directory (default: `/var/lib/jenkins`). Backing up the entire directory is feasible but may be overkill. Focus on the components below:

```bash theme={null}
$ tree /var/lib/jenkins
builds
├── [BUILD_ID]
│   ├── build.xml
│   └── changelog.xml
config.xml
*.xml
fingerprints
identity.key.enc
jobs
├── [JOBNAME]
│   └── config.xml
plugins
secrets
├── hudson.util.Secret
├── master.key
└── InstanceIdentity.KEY
userContent
workspace
```

| Component        | Purpose                                                                                         |
| ---------------- | ----------------------------------------------------------------------------------------------- |
| **config.xml**   | Main Jenkins system settings (global configuration).                                            |
| **\*.xml**       | Other site-wide configs (e.g., credentials.xml, nodes.xml).                                     |
| **jobs/**        | Job definitions and build histories. Exclude large artifacts if storage is limited.             |
| **plugins/**     | Installed plugins (`.jpi`, `.hpi`). You can reinstall plugins from the update center if needed. |
| **secrets/**     | Encryption keys and credentials.                                                                |
| **userContent/** | Static files served via `https://<jenkins>/userContent/`.                                       |
| **workspace/**   | Working directories for SCM checkouts (typically safe to skip; recreated on build).             |

<Callout icon="triangle-alert">
  Never store unencrypted secret keys or credentials in public or shared backup locations. Always encrypt backups that include the `secrets/` directory.
</Callout>

## Restoring Jenkins

1. Stop the Jenkins service:
   ```bash theme={null}
   sudo systemctl stop jenkins
   ```
2. Restore your backup archive or snapshot to `JENKINS_HOME`.
3. Ensure correct ownership and permissions:
   ```bash theme={null}
   sudo chown -R jenkins:jenkins /var/lib/jenkins
   ```
4. Start Jenkins and verify logs for any errors:
   ```bash theme={null}
   sudo systemctl start jenkins
   sudo journalctl -u jenkins -f
   ```

## Links and References

* [Jenkins Backup and Restore Documentation][jenkins-backup]
* [ThinBackup Plugin][thinbackup-plugin]

[jenkins-backup]: https://www.jenkins.io/doc/book/managing/system-administration/backup-restore/

[thinbackup-plugin]: https://plugins.jenkins.io/thinBackup/

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/77043650-89c2-4ad3-bbd1-e06eabe35581/lesson/8fdf9718-2e16-4fb8-9b31-87c44cfafebb" />
</CardGroup>
