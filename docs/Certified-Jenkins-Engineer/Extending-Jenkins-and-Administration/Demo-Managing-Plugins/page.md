# Demo Managing Plugins

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Extending-Jenkins-and-Administration/Demo-Managing-Plugins/page

This hands-on guide covers uninstalling the Copy Artifact plugin in Jenkins and ensuring no orphaned configurations remain.

In this hands-on guide, we’ll uninstall and clean up the **Copy Artifact** plugin in a simple chained-job workflow: **ascii-build-job** → **ascii-test-job** → **ascii-deploy-job**. By the end, you’ll know how to verify artifact handling, remove a plugin, and ensure no orphaned configuration remains.

## Table of Contents

1. [Job Workflow](#job-workflow)
2. [Step 1: Verify Build Job Generates Artifact](#step-1-verify-build-job-generates-artifact)
3. [Step 2: Configure Test Job to Copy Artifacts](#step-2-configure-test-job-to-copy-artifacts)
4. [Step 3: Trigger Builds and Observe Workflow](#step-3-trigger-builds-and-observe-workflow)
5. [Step 4: Confirm Plugin Installation](#step-4-confirm-plugin-installation)
6. [Step 5: Locate Plugin on Filesystem](#step-5-locate-plugin-on-filesystem)
7. [Step 6: Uninstall Copy Artifact Plugin](#step-6-uninstall-copy-artifact-plugin)
8. [Step 7: Re-run Jobs After Uninstallation](#step-7-re-run-jobs-after-uninstallation)
9. [Step 8: Inspect Job Configuration](#step-8-inspect-job-configuration)
10. [Conclusion](#conclusion)

## Job Workflow

| Job Name         | Purpose                                                                                  |
| ---------------- | ---------------------------------------------------------------------------------------- |
| ascii-build-job  | Fetches advice from API, archives `advice.json`                                          |
| ascii-test-job   | Copies `advice.json` with [Copy Artifact Plugin][copy-artifact] and validates word count |
| ascii-deploy-job | (Optional) Deploys validated advice to target system                                     |

[copy-artifact]: https://plugins.jenkins.io/copyartifact

***

## Step 1: Verify Build Job Generates Artifact

On the **ascii-build-job** dashboard, confirm the build archives `advice.json` successfully.

<Frame>
  ![The image shows a Jenkins dashboard for a project named "ascii-build-job," displaying build flow and downstream projects with links to build history and artifacts.](https://kodekloud.com/kk-media/image/upload/v1752870560/notes-assets/images/Certified-Jenkins-Engineer-Demo-Managing-Plugins/jenkins-dashboard-ascii-build-job.jpg)
</Frame>

***

## Step 2: Configure Test Job to Copy Artifacts

In **ascii-test-job**, add a **Build Step → Copy artifacts from another project**. Select:

* **Project name:** `ascii-build-job`
* **Which build:** Latest successful build
* **Artifacts to copy:** `advice.json`

<Frame>
  ![The image shows a Jenkins configuration screen for a job named "ascii-test-job," focusing on the "Build Steps" section where artifacts are being copied from another project. The interface includes options for selecting the project name, build type, and specific artifacts to copy.](https://kodekloud.com/kk-media/image/upload/v1752870561/notes-assets/images/Certified-Jenkins-Engineer-Demo-Managing-Plugins/jenkins-ascii-test-job-build-steps.jpg)
</Frame>

***

## Step 3: Trigger Builds and Observe Workflow

1. Click **Build Now** on **ascii-build-job**.
2. Review console output to ensure `advice.json` was archived:

```console theme={null}
$ ls advice.json
advice.json
$ cat advice.json
{"slip":{"advice":"Don't promise what you can't deliver."}}
$ jq -r .slip.advice
Don't promise what you can't deliver.
$ wc -w advice.json
6 advice.json
```

3. Both **ascii-build-job** and **ascii-test-job** should pass:

<Frame>
  ![The image shows a Jenkins dashboard for a job named "ascii-build-job," displaying its build flow, downstream projects, and build history. The job appears to have been successfully built recently.](https://kodekloud.com/kk-media/image/upload/v1752870563/notes-assets/images/Certified-Jenkins-Engineer-Demo-Managing-Plugins/jenkins-dashboard-ascii-build-job-2.jpg)
</Frame>

***

## Step 4: Confirm Plugin Installation

Navigate to **Manage Jenkins → Manage Plugins → Installed**. Verify **Copy Artifact** is listed:

```bash theme={null}
$ cd $JENKINS_HOME/plugins
$ ls | grep -i copy
copyartifact.jpi
```

<Frame>
  ![The image shows the Jenkins plugin management interface, specifically the "Installed plugins" section, with a search for "copy" displaying the "Copy Artifact" plugin.](https://kodekloud.com/kk-media/image/upload/v1752870564/notes-assets/images/Certified-Jenkins-Engineer-Demo-Managing-Plugins/jenkins-plugin-management-installed-copy-artifact.jpg)
</Frame>

***

## Step 5: Locate Plugin on Filesystem

From a terminal (or IDE), inspect the plugin file:

```bash theme={null}
$ cd $JENKINS_HOME/plugins
$ ls | grep -i copyartifact
copyartifact.jpi
```

<Frame>
  ![The image shows a terminal window in Visual Studio Code displaying a list of Jenkins plugin files with the ".jpi" extension. The terminal is connected to a remote server, and the files are organized in columns.](https://kodekloud.com/kk-media/image/upload/v1752870566/notes-assets/images/Certified-Jenkins-Engineer-Demo-Managing-Plugins/vscode-terminal-jenkins-plugins.jpg)
</Frame>

***

## Step 6: Uninstall Copy Artifact Plugin

1. Go to **Manage Plugins → Installed**.
2. Click **Uninstall** next to **Copy Artifact**.
3. Confirm the dialog to remove the plugin binary.

<Frame>
  ![The image shows a Jenkins interface with a confirmation dialog asking if the user wants to uninstall the "Copy Artifact" plugin, with options to cancel or proceed.](https://kodekloud.com/kk-media/image/upload/v1752870567/notes-assets/images/Certified-Jenkins-Engineer-Demo-Managing-Plugins/jenkins-uninstall-copy-artifact-dialog.jpg)
</Frame>

<Callout icon="lightbulb">
  Uninstalling removes `copyartifact.jpi` from `$JENKINS_HOME/plugins`, but job XMLs still reference the plugin until Jenkins is restarted.
</Callout>

***

## Step 7: Re-run Jobs After Uninstallation

Trigger **ascii-build-job** again, then **ascii-test-job**. You’ll see the copy step succeed (artifact already on disk), but Jenkins still internally uses the missing plugin reference:

```console theme={null}
[ascii-test-job] $ /bin/sh -xe /tmp/jenkinsXXXX.sh
+ ls advice.json
advice.json
+ cat advice.json
{"slip":{"advice":"Don't try and bump start a motorcycle on an icy road."}}
+ jq -r .slip.advice
Don't try and bump start a motorcycle on an icy road.
+ wc -w advice.json
11 advice.json
```

<Frame>
  ![The image shows a Jenkins dashboard for a job named "ascii-test-job," displaying build flow details, upstream and downstream projects, and build history.](https://kodekloud.com/kk-media/image/upload/v1752870568/notes-assets/images/Certified-Jenkins-Engineer-Demo-Managing-Plugins/jenkins-dashboard-ascii-test-job.jpg)
</Frame>

***

## Step 8: Inspect Job Configuration

Open `ascii-test-job/config.xml` and locate the plugin reference:

```xml theme={null}
<project>
  <builders>
    <hudson.plugins.copyartifact.CopyArtifact plugin="copyartifact@749.vfb_dca_a_9b_6549">
      <project>ascii-build-job</project>
      <filter>advice.json</filter>
      <selector class="hudson.plugins.copyartifact.StatusSelector">
        <stable>true</stable>
      </selector>
    </hudson.plugins.copyartifact.CopyArtifact>
    <!-- ... other builders ... -->
  </builders>
</project>
```

Without the plugin binary, this builder will error after a Jenkins restart. A full restart is required to purge these orphaned entries.

<Callout icon="triangle-alert">
  After uninstalling a plugin, always restart Jenkins to remove its XML elements from job configurations.
</Callout>

***

## Conclusion

To fully remove a plugin and its configuration:

1. **Uninstall** the plugin via **Manage Plugins**.
2. **Restart Jenkins** to clean up any residual `<plugin>` elements in job `config.xml` files.

For more information, see the [Jenkins Plugin Management documentation](https://www.jenkins.io/doc/book/managing/plugins/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/6113113b-7852-401b-9c41-c5bc8242ad99/lesson/ac5be1a1-10f4-4f3d-873a-d0cb417cf0c9" />
</CardGroup>
