# drwxr-xr-x  8 jenkins jenkins 4096 Oct 2 09:55 .
```

Each timestamped folder includes `config.xml` and `history.xml`:

```xml theme={null}
<?xml version='1.1' encoding='UTF-8'?>
<hudson.plugins.jobConfigHistory.HistoryDescr plugin='jobConfigHistory@1268.V75ce751da_911'>
  <user>siddharth</user>
  <userId>siddharth</userId>
  <operation>Changed</operation>
  <timestamp>2024-10-02_09-52-27</timestamp>
</hudson.plugins.jobConfigHistory.HistoryDescr>
```

With this setup, you’re equipped to track, compare, restore, and audit Jenkins configurations effortlessly.

## References

* [Job Configuration History Plugin](https://plugins.jenkins.io/jobConfigHistory/)
* [Jenkins User Documentation](https://www.jenkins.io/doc/)
* [Managing Jenkins Plugins](https://www.jenkins.io/doc/book/managing/plugins/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/bf3ddc28-a03d-4738-9f98-2779d81482f5/lesson/819f57b8-acc3-4529-9d72-6f9b3932ed64" />
</CardGroup>


# Demo Job Restrictions

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Jenkins-Administration-and-Monitoring-Part-1/Demo-Job-Restrictions/page

This tutorial explains using the Job Restrictions plugin in Jenkins to control job execution on specific nodes.

In this tutorial, you’ll learn how to use the **Job Restrictions** plugin in Jenkins to control which jobs can run on specific nodes. By leveraging job names, users, and logical operators, you can enforce security policies and prevent unintended builds.

## Table of Contents

1. [Install the Job Restrictions Plugin](#install-the-job-restrictions-plugin)
2. [Configure Node-Level Restrictions](#configure-node-level-restrictions)\
   2.1 [Navigate to the Built-In Node](#navigate-to-the-built-in-node)\
   2.2 [Enable Job Restrictions](#enable-job-restrictions)
3. [Test the Restriction](#test-the-restriction)\
   3.1 [Building an Unmatched Job](#building-an-unmatched-job)\
   3.2 [Creating a Matching Job](#creating-a-matching-job)
4. [Add User-Based Restrictions](#add-user-based-restrictions)
5. [Links and References](#links-and-references)

***

## 1. Install the Job Restrictions Plugin

1. Go to **Manage Jenkins** › **Manage Plugins**.
2. Under the **Available** tab, search for **Job Restrictions**.
3. Select the plugin and click **Install without restart**.
4. Once the installation completes, choose **Restart Jenkins when installation is complete and no jobs are running**.

<Frame>
  ![The image shows a Jenkins interface displaying the download progress of plugins, with some tasks marked as "Success" and others as "Pending." It includes options to go back to the top page and restart Jenkins after installation.](https://kodekloud.com/kk-media/image/upload/v1752870635/notes-assets/images/Certified-Jenkins-Engineer-Demo-Job-Restrictions/jenkins-plugin-download-progress.jpg)
</Frame>

<Callout icon="lightbulb">
  Ensure your Jenkins instance is at least version **2.387** or higher for full compatibility with the Job Restrictions plugin.
</Callout>

After Jenkins restarts, the plugin is ready for configuration.

***

## 2. Configure Node-Level Restrictions

### 2.1 Navigate to the Built-In Node

1. From the Jenkins dashboard, click **Manage Jenkins** › **Manage Nodes and Clouds**.
2. Select the **built-in node** (often labeled “built-in”).

<Frame>
  ![The image shows a Jenkins dashboard displaying node information, including architecture, clock difference, and disk space details. It also indicates the build queue and executor status, with options to add a new node or configure monitors.](https://kodekloud.com/kk-media/image/upload/v1752870635/notes-assets/images/Certified-Jenkins-Engineer-Demo-Job-Restrictions/jenkins-dashboard-node-info-status.jpg)
</Frame>

### 2.2 Enable Job Restrictions

1. Click **Configure** on the built-in node.
2. Scroll to **Node Properties** and check **Job Restrictions**.
3. Click **Add** and select **Regular Expression — Job Name**.
4. Enter a regex pattern that matches the jobs you want to allow. For example:

```regex theme={null}
^Dasher_.*
```

<Frame>
  ![The image shows a Jenkins configuration screen for a built-in node, with options for labels, usage, and node properties, including job restrictions using a regular expression.](https://kodekloud.com/kk-media/image/upload/v1752870637/notes-assets/images/Certified-Jenkins-Engineer-Demo-Job-Restrictions/jenkins-configuration-built-in-node.jpg)
</Frame>

Use **Add** again to combine rules with **AND**, **OR**, or **NOT** logic.

#### Common Restriction Types

| Restriction Type              | Purpose                                  | Example Pattern  |
| ----------------------------- | ---------------------------------------- | ---------------- |
| Regular Expression — Job Name | Permit jobs matching a name pattern      | `^Dasher_.*`     |
| Started by User               | Allow builds initiated by specific users | `Emma`           |
| Parameterized Job             | Restrict based on parameter values       | `env=production` |

***

## 3. Test the Restriction

### 3.1 Building an Unmatched Job

Attempt to build a job that does **not** match your regex—for example, **npm-version-test**. It will stay in the queue as **Pending**.

<Frame>
  ![The image shows a Jenkins dashboard for a project named "npm-version-test," displaying build status and history, with the last build occurring 9 days ago. The interface includes options like "Build Now," "Configure," and "Open Blue Ocean."](https://kodekloud.com/kk-media/image/upload/v1752870638/notes-assets/images/Certified-Jenkins-Engineer-Demo-Job-Restrictions/jenkins-dashboard-npm-version-test.jpg)
</Frame>

<Callout icon="triangle-alert">
  Jobs that don’t meet any restriction rules will remain queued indefinitely. Monitor the queue to avoid resource bottlenecks.
</Callout>

### 3.2 Creating a Matching Job

1. From the dashboard, click **New Item**.

2. Enter **Dasher\_testJob** and select **Freestyle project**.

3. In **Build** steps, add a shell step:

   ```shell theme={null}
   echo "Hello"
   ```

4. Click **Save**, then **Build Now**. This job matches the pattern and will execute.

<Frame>
  ![The image shows a Jenkins dashboard for a job named "Dasher\_testJob," displaying build status and permalinks for recent builds. The interface includes options like "Build Now," "Configure," and "Open Blue Ocean."](https://kodekloud.com/kk-media/image/upload/v1752870639/notes-assets/images/Certified-Jenkins-Engineer-Demo-Job-Restrictions/jenkins-dashboard-dasher-testjob.jpg)
</Frame>

***

## 4. Add User-Based Restrictions

To grant specific users the ability to run any job on this node:

1. Navigate back to **Manage Jenkins** › **Manage Nodes and Clouds** › **built-in node** › **Configure**.
2. Under **Job Restrictions**, click **Add** › **Started by User**.
3. Enter the username (e.g., `Emma`).
4. Set the logical operator to **OR** so that jobs match either the regex rule **or** the user rule.
5. Click **Save**.

<Frame>
  ![The image shows a configuration screen from Jenkins, where job restrictions are being set using a regular expression for job names and a user list.](https://kodekloud.com/kk-media/image/upload/v1752870639/notes-assets/images/Certified-Jenkins-Engineer-Demo-Job-Restrictions/jenkins-job-restrictions-configuration.jpg)
</Frame>

Now, user **Emma** can trigger any job on this node, while all other users must use the `Dasher_` prefix.

***

## Links and References

* [Job Restrictions Plugin](https://plugins.jenkins.io/job-restrictions/)
* [Jenkins Configure Nodes](https://www.jenkins.io/doc/book/managing/nodes/)
* [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)

With regex-based rules, user filters, and logical operators, you can precisely control job execution across your Jenkins nodes.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/bf3ddc28-a03d-4738-9f98-2779d81482f5/lesson/82655848-a718-49ec-aa7f-e49f5394b8cc" />
</CardGroup>
