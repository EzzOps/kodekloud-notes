# Demo InstallSetup NodeJS Build Tool

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Setting-up-CI-Pipeline/Demo-InstallSetup-NodeJS-Build-Tool/page

This tutorial explains how to integrate Node.js into Jenkins pipelines using host installation and Jenkins-managed tools.

In this tutorial, you will learn how to integrate Node.js into your Jenkins pipelines by using both the host installation and Jenkins-managed Node.js tool. By the end, you'll be able to run Node.js commands in freestyle jobs across controllers and agents.

> **lightbulb** * A running Jenkins controller (version 2.x or later).
  * Shell access to the Jenkins host machine.
  * Administrative privileges to install plugins.

## 1. Verify Node.js on the Jenkins Host

SSH into the Jenkins server and confirm that Node.js and npm are installed:

```bash theme={null}
node -v
npm -v
systemctl status jenkins
