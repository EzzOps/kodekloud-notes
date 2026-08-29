# Demo Controller Failure Freestyle Project

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Extending-Jenkins-and-Administration/Demo-Controller-Failure-Freestyle-Project/page

This tutorial demonstrates the impact of a Jenkins controller failure on a long-running Freestyle project and explores job termination behavior.

In this tutorial, we’ll demonstrate how a Jenkins controller failure affects a long-running **Freestyle** project. You will learn how to:

| Step | Action                           | Description                                  |
| ---- | -------------------------------- | -------------------------------------------- |
| 1    | Prepare Deploy Job               | Add a `sleep` command to simulate long tasks |
| 2    | Trigger Build & Test             | Execute upstream jobs and inspect failures   |
| 3    | Rerun & Deploy                   | Fix test failures, queue the deploy job      |
| 4    | Simulate Controller Failure      | Stop the controller during deployment        |
| 5    | Analyze Outcome                  | Observe job termination behavior             |
| 6    | Review Jenkins Dashboard & Icons | Explore build status icons and legend        |

By the end, you’ll understand why **Freestyle** jobs do not survive controller restarts and what alternatives exist.

***

## 1. Prepare a Long-Running Deploy Job

Edit the **ascii-deploy-job** and insert a `sleep` before the actual deployment steps. This will simulate a long-running process.

```bash theme={null}
#!/bin/bash
