# Controller Failure Freestyle Project

Source: https://notes.kodekloud.com/docs/Jenkins-For-Beginners/Extending-Jenkins/Controller-Failure-Freestyle-Project/page

This article demonstrates the impact of controller failures on long-running Freestyle projects in Jenkins and how to simulate such failures.

In this article, we demonstrate how a controller failure can impact a long-running Freestyle project in Jenkins. We simulate a long-running job using a sleep command to mimic work in progress and then introduce a controller failure during its execution. Follow along to see how the process unfolds.

![The image shows a Jenkins dashboard with a list of jobs, their last success and failure times, and durations. The interface includes options for managing Jenkins and viewing build history.](https://kodekloud.com/kk-media/image/upload/v1752879441/notes-assets/images/Jenkins-For-Beginners-Controller-Failure-Freestyle-Project/jenkins-dashboard-jobs-history.jpg)

## Simulating a Long-Running Job

The example simulates a long-running build by inserting a sleep command for 3600 seconds before deploying. During the sleep period, we simulate a controller failure. Use the following script to reproduce the procedure:

```bash theme={null}
sleep 3600
