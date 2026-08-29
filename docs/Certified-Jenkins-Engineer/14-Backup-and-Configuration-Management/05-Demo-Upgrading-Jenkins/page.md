# Demo Upgrading Jenkins

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Backup-and-Configuration-Management/Demo-Upgrading-Jenkins/page

This guide covers safely upgrading Jenkins with minimal downtime using the Prepare for Shutdown feature.

Upgrading Jenkins with minimal downtime requires planning and the built-in **Prepare for Shutdown** feature. In this guide, we’ll cover:

* Checking for new Jenkins releases
* Reviewing changelogs
* Preventing new builds during the update
* Performing the WAR file upgrade
* Verifying the new version

***

## 1. Choose Your Jenkins Release

Navigate to the [Jenkins download and deployment page](https://www.jenkins.io/download/). Compare the Stable (LTS) and Weekly packages:

<Frame>
  ![The image shows a webpage from Jenkins.io detailing the download and deployment options for Jenkins, including Stable (LTS) and Weekly releases, along with instructions for downloading Jenkins.](../../../../images/kodekloud.com/kk-media/image/upload/v1752870428/notes-assets/images/Certified-Jenkins-Engineer-Demo-Upgrading-Jenkins/jenkins-download-deployment-options.jpg)
</Frame>

| Release Type | Update Frequency | Ideal For                                   |
| ------------ | ---------------- | ------------------------------------------- |
| LTS          | Every 12 weeks   | Production environments requiring stability |
| Weekly       | Weekly           | Testing the latest features and bug fixes   |

***

## 2. Check for Updates on Your Dashboard

Log in to Jenkins and go to **Manage Jenkins**. The dashboard shows pending updates and plugin advisories:

<Frame>
  ![The image shows a Jenkins dashboard interface with various management options and warnings about deprecated plugins and security issues. It also indicates that a new version of Jenkins is available for download.](../../../../images/kodekloud.com/kk-media/image/upload/v1752870430/notes-assets/images/Certified-Jenkins-Engineer-Demo-Upgrading-Jenkins/jenkins-dashboard-management-warnings.jpg)
</Frame>

Click **Changelog** to review the release notes:

<Frame>
  ![The image shows a webpage displaying the Jenkins LTS Changelog for version 2.492.1, detailing enhancements and notable changes.](../../../../images/kodekloud.com/kk-media/image/upload/v1752870431/notes-assets/images/Certified-Jenkins-Engineer-Demo-Upgrading-Jenkins/jenkins-lts-changelog-2-492-1.jpg)
</Frame>

For example, upgrading from **2.462.1** to **2.492.1** brings critical security fixes and performance improvements. Copy the WAR URL (e.g., `https://updates.jenkins.io/download/war/2.492.1/jenkins.war`) for the next step.

***

## 3. Prepare Jenkins for Upgrade

Before replacing the WAR, enter shutdown mode so existing builds finish and no new builds start:

1. Go to **Manage Jenkins → Prepare for Shutdown**
2. Add a reason (e.g., “Planning for upgrade”) and confirm

A banner appears and all new build requests queue:

<Frame>
  ![The image shows a Jenkins interface indicating a shutdown in progress for an upgrade, with options to update the reason or cancel the shutdown.](../../../../images/kodekloud.com/kk-media/image/upload/v1752870432/notes-assets/images/Certified-Jenkins-Engineer-Demo-Upgrading-Jenkins/jenkins-shutdown-upgrade-interface.jpg)
</Frame>

Monitor the build queue to ensure no jobs are running:

<Frame>
  ![The image shows a Jenkins dashboard displaying a list of build jobs with details such as last success, last failure, and duration. The interface includes navigation options and a build queue status.](../../../../images/kodekloud.com/kk-media/image/upload/v1752870433/notes-assets/images/Certified-Jenkins-Engineer-Demo-Upgrading-Jenkins/jenkins-dashboard-build-jobs-status.jpg)
</Frame>

Any attempt to start a new job—like **ascii-build-job**—will now wait until after the upgrade:

<Frame>
  ![The image shows a Jenkins dashboard for a project named "ascii-build-job," displaying build flow details, downstream projects, and permalinks. A red banner indicates "planning for an upgrade."](../../../../images/kodekloud.com/kk-media/image/upload/v1752870434/notes-assets/images/Certified-Jenkins-Engineer-Demo-Upgrading-Jenkins/jenkins-dashboard-ascii-build-job.jpg)
</Frame>

<Callout icon="lightbulb">
  Ensure all running builds complete and no new tasks remain in the queue before stopping the Jenkins service.
</Callout>

***

## 4. Upgrade the Jenkins WAR

On your Jenkins host, run the following commands:

```bash theme={null}
