# Demo Install and Configure Audit Trail

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Jenkins-Administration-and-Monitoring-Part-2/Demo-Install-and-Configure-Audit-Trail/page

This guide explains how to install, configure, and test the Audit Trail plugin in Jenkins for tracking user activities.

Enhance your Jenkins security posture by tracking user activities—such as job configuration changes, system restarts, and build triggers—using the **Audit Trail** plugin. This guide walks you through installation, configuration, testing, and advanced logging options.

## 1. Install the Audit Trail Plugin

1. From the Jenkins dashboard, go to **Manage Jenkins** → **Manage Plugins**.
2. Select the **Available** tab and search for **Audit Trail**.
3. Check the box next to **Audit Trail** and click **Install without restart**.

<Frame>
  ![The image shows a webpage from the Jenkins plugins site, specifically detailing the "Audit Trail" plugin. It includes information on logger configuration, file logger, and syslog logger settings.](https://kodekloud.com/kk-media/image/upload/v1752870696/notes-assets/images/Certified-Jenkins-Engineer-Demo-Install-and-Configure-Audit-Trail/jenkins-audit-trail-plugin-settings.jpg)
</Frame>

## 2. Configure the Audit Trail Plugin

1. Navigate to **Manage Jenkins** → **Configure System**.
2. Scroll down to the **Audit Trail** section.
3. Under **Logger**, choose **Log file (daily rotation)**.
4. In **Log file pattern**, enter:

   ```text theme={null}
   /var/log/jenkins/custom-audit-%g.log
   ```

<Callout icon="lightbulb">
  Use `%g` to rotate logs daily and prevent oversized files.
</Callout>

5. Keep other settings at their defaults and click **Save**.

<Frame>
  ![The image shows a Jenkins system configuration page focused on setting up an audit trail, including log file rotation settings.](https://kodekloud.com/kk-media/image/upload/v1752870699/notes-assets/images/Certified-Jenkins-Engineer-Demo-Install-and-Configure-Audit-Trail/jenkins-audit-trail-configuration.jpg)
</Frame>

## 3. Test Your Audit Trail Setup

### 3.1 Make a Job Configuration Change

* From the dashboard, select an existing job (for example, **monitor-jenkins**).
* Click **Configure**, tweak a build step or description, then click **Apply** → **Save**.
* Trigger a new build and wait for it to finish.

### 3.2 Inspect the Audit Logs

```bash theme={null}
cd /var/log/jenkins
ls
cat custom-audit-0.log-2024-11-10
