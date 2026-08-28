# Demo Job Configuration History Plugin

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Jenkins-Administration-and-Monitoring-Part-1/Demo-Job-Configuration-History-Plugin/page

Learn to install, configure, and use the Jenkins Job Configuration History plugin for tracking and managing job and system configuration changes.

In this guide, you’ll learn how to install, configure, and use the Jenkins [Job Configuration History](https://plugins.jenkins.io/jobConfigHistory/) plugin. This powerful plugin:

* Automatically archives every job and system configuration change
* Provides side-by-side diff views for quick comparison
* Restores older versions and recovers deleted jobs

<Frame>
  ![The image shows a webpage for the "Job Configuration History" plugin on the Jenkins website, detailing its features, version information, and links for further resources.](https://kodekloud.com/kk-media/image/upload/v1752870629/notes-assets/images/Certified-Jenkins-Engineer-Demo-Job-Configuration-History-Plugin/job-configuration-history-jenkins.jpg)
</Frame>

## Plugin Features

| Feature                | Description                                         | Example Use Case                             |
| ---------------------- | --------------------------------------------------- | -------------------------------------------- |
| Automatic Backups      | Saves config on every change                        | Track every build-job tweak                  |
| Diff Viewer            | Side-by-side comparison of configurations           | Identify exactly what changed between builds |
| Restore & Rollback     | Revert to any prior version or recover deleted jobs | Roll back failed changes                     |
| System Config Tracking | Monitors global Jenkins settings                    | Audit security or plugin updates             |

## 1. Installing the Plugin

1. Navigate to **Manage Jenkins** > **Manage Plugins**.
2. Under the **Available** tab, search for **Job Configuration History**.
3. Select the plugin, click **Install without restart**, then restart Jenkins:
   * Via **Manage Jenkins** > **Restart**
   * Or manually restart the Jenkins service

<Callout icon="triangle-alert">
  Keeping every configuration change can consume significant disk space over time. Monitor the storage and adjust limits in the plugin settings section.
</Callout>

<Frame>
  ![The image shows a webpage from the Jenkins plugin site, displaying a "Job Config History Revision Overview" with a table of job configuration changes and a "Job Diff Side-By-Side View" section.](https://kodekloud.com/kk-media/image/upload/v1752870630/notes-assets/images/Certified-Jenkins-Engineer-Demo-Job-Configuration-History-Plugin/jenkins-job-config-history-overview.jpg)
</Frame>

## 2. Navigating Configuration History

Once Jenkins restarts, a new **Job Config History** link appears in the dashboard sidebar. Click it to:

* View **All Configuration History**
* Filter by **Job Changes**, **System Changes**, **Created Jobs**, or **Deleted Jobs**
* Inspect individual revisions and metadata

<Frame>
  ![The image shows a Jenkins dashboard displaying the "All Configuration History" page, listing recent configuration changes with details like date, job configuration, operation, user, and file view options.](https://kodekloud.com/kk-media/image/upload/v1752870631/notes-assets/images/Certified-Jenkins-Engineer-Demo-Job-Configuration-History-Plugin/jenkins-dashboard-configuration-history.jpg)
</Frame>

## 3. Tracking Job Configuration Changes

Follow these steps to see how changes are recorded:

1. Open **Dasher\_testJob** from the Jenkins dashboard.
2. Click **Configure**, disable any restriction rules, then **Save**.
3. In **Build**, add an **Execute Shell** step:
   ```bash theme={null}
   echo "Hello Testing a new Plugin"
   ```
4. **Save** and select **Build Now**.
5. Re-enter **Configure**, add:
   ```bash theme={null}
   sleep 5
   ```
6. **Save** and **Build Now** again.

Return to **Job Config History**, click **Show All Configs**, and compare revisions:

```xml theme={null}
<!-- First revision -->
<command>echo Hello Testing a new Plugin</command>

<!-- Second revision -->
<command>echo Hello Testing a new Plugin</command>
<command>sleep 5</command>
```

### 3.1 Per-Job History and Diff View

To inspect a single job’s history:

* Open **Dasher\_testJob** > **Job Config History**
* You’ll see a list of revisions with user, timestamp, and operation
* Click **Show Difference** for a side-by-side XML diff

<Frame>
  ![The image shows a Jenkins interface displaying the "Job Configuration History" for a job named "Dasher\_testJob," listing changes made by a user named Siddharth. The interface includes options to view configurations as XML, restore old configurations, and delete entries.](https://kodekloud.com/kk-media/image/upload/v1752870632/notes-assets/images/Certified-Jenkins-Engineer-Demo-Job-Configuration-History-Plugin/jenkins-job-configuration-history-dasher.jpg)
</Frame>

```xml theme={null}
<!-- Older configuration -->
<command>echo Hello Testing a new Plugin</command>

<!-- Newer configuration -->
<command>echo Hello Testing a new Plugin</command>
<configuredLocalRules/>
<hudson.tasks.Shell/>
<command>sleep 5</command>
<configuredLocalRules/>
```

To revert to a previous version, click **Restore** next to the desired entry and confirm. Jenkins will apply the older `config.xml` and reflect only the restored build steps:

```bash theme={null}
echo "Hello Testing a new Plugin"
```

## 4. Restoring Deleted Jobs

The plugin logs deletions, allowing you to recover lost jobs:

1. Delete **Dasher\_testJob** from the dashboard.
2. Go to **Job Config History** and filter by **Deleted Jobs**.
3. Find the delete event and click **Restore** to recover the job.

<Frame>
  ![The image shows a Jenkins interface displaying a "Job Deletion History" page, listing operations performed on a job, including deletions and changes, with options to view files and delete entries.](https://kodekloud.com/kk-media/image/upload/v1752870633/notes-assets/images/Certified-Jenkins-Engineer-Demo-Job-Configuration-History-Plugin/jenkins-job-deletion-history-interface.jpg)
</Frame>

## 5. Plugin Settings and Storage Location

Configure history storage and limits:

1. Navigate to **Manage Jenkins** > **Configure System**.
2. Scroll to **Job Config History** settings:
   * **History Root Directory** (default: `/var/lib/jenkins/config-history`)
   * **Max entries per config**
   * **Max age of entries**

<Frame>
  ![The image shows a Jenkins system configuration page, specifically focusing on the "Job Config History" settings, with options for history directory and entry limits.](https://kodekloud.com/kk-media/image/upload/v1752870634/notes-assets/images/Certified-Jenkins-Engineer-Demo-Job-Configuration-History-Plugin/jenkins-job-config-history-settings.jpg)
</Frame>

On the controller:

```bash theme={null}
cd /var/lib/jenkins
ls -l
cd config-history/jobs/Dasher_testJob
ls -l
