# Demo Working with Freestyle Job

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Jenkins-Setup-and-Interface/Demo-Working-with-Freestyle-Job/page

Learn to set up a Jenkins Freestyle project that fetches advice from an API and renders it as ASCII art using the Cowsay library.

In this tutorial, you’ll learn how to set up a Jenkins Freestyle project that fetches a random piece of advice from the AdviceSlip REST API and renders it as fun ASCII artwork using the [Cowsay library](https://github.com/shiena/cowsay). This example demonstrates REST integration, shell scripting, and environment configuration in Jenkins.

## 1. Create a New Freestyle Project

1. Log into Jenkins and click **New Item**.
2. Enter **generate ASCII artwork** as the project name.
3. Select **Freestyle project** and click **OK**.

![The image shows a Jenkins dashboard where a user is creating a new item, with options to select different project types such as Freestyle project, Pipeline, and Multibranch Pipeline.](https://kodekloud.com/kk-media/image/upload/v1752870854/notes-assets/images/Certified-Jenkins-Engineer-Demo-Working-with-Freestyle-Job/jenkins-dashboard-new-item-projects.jpg)

## 2. Configure General Settings

Under **General**, set up the project metadata:

* **Description**: Generate ASCII artwork using the Cowsay library and AdviceSlip REST API
* Leave **Discard old builds**, **This project is parameterized**, and other options at their defaults.
* **Source Code Management**: **None**
* **Build Triggers**: (none)
* **Build Environment**: Enable **Add timestamps to the console output** (requires the [Timestamp Plugin](https://plugins.jenkins.io/timestamper/)).

![The image shows a Jenkins configuration page for a project titled "Generate ASCII Artwork," with options for build settings and a description mentioning the use of the Cowsay library and AdviceSlip Rest API.](https://kodekloud.com/kk-media/image/upload/v1752870855/notes-assets/images/Certified-Jenkins-Engineer-Demo-Working-with-Freestyle-Job/jenkins-generate-ascii-artwork-config.jpg)

![The image shows a configuration page for a project, likely in a software development environment, with options for setting parameters, source code management, build triggers, and more. There are checkboxes for various settings and a section explaining parameterized builds.](https://kodekloud.com/kk-media/image/upload/v1752870857/notes-assets/images/Certified-Jenkins-Engineer-Demo-Working-with-Freestyle-Job/project-configuration-settings-diagram.jpg)

![The image shows a configuration screen for a software build system, with options for build triggers, environment settings, and post-build actions. The interface includes checkboxes and dropdown menus for various settings.](https://kodekloud.com/kk-media/image/upload/v1752870857/notes-assets/images/Certified-Jenkins-Engineer-Demo-Working-with-Freestyle-Job/software-build-system-configuration.jpg)

## 3. Add Build Step: Execute Shell

Choose **Add build step → Execute shell** and paste this script. It fetches advice, validates it, installs Cowsay, adjusts the PATH, and prints the ASCII art.

```bash theme={null}
#!/bin/bash
set -e
