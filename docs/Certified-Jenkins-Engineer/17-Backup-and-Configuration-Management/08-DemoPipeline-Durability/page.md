# DemoPipeline Durability

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Backup-and-Configuration-Management/DemoPipeline-Durability/page

Pipeline durability in Jenkins controls how pipeline state is written to disk for build recovery after crashes or restarts.

## What Is Pipeline Durability?

Pipeline durability in Jenkins controls how pipeline state is written to disk so that builds can recover after a crash or restart. Choosing the right durability level helps you balance:

* **Resilience**: Ability to resume an in-progress build.
* **Performance**: Disk I/O overhead when recording pipeline checkpoints.

### Durability Levels

| Level                   | Description                                                                           |
| ----------------------- | ------------------------------------------------------------------------------------- |
| MAX\_SURVIVABILITY      | Writes state after every step. Safest but introduces the most disk I/O overhead.      |
| PERFORMANCE\_OPTIMIZED  | Minimizes disk writes for faster execution. Builds cannot resume on unclean shutdown. |
| SURVIVABLE\_NON\_ATOMIC | Compromise between state safety and performance.                                      |

> **lightbulb** Use **MAX\_SURVIVABILITY** for critical pipelines that must resume after crashes, and **PERFORMANCE\_OPTIMIZED** when speed is more important than resumability.

## Configuring Durability Settings

You can override the default durability level at three scopes:

1. **Global** (all pipelines)
2. **Branch** (multibranch projects)
3. **Per-Pipeline** (individual job)

### 1. Global Configuration

To set the default durability level for every pipeline:

1. Navigate to **Manage Jenkins → Configure System**.
2. Search for “Pipeline Speed/Durability.”
3. Choose your preferred default level.

![The image shows a webpage from the Jenkins documentation, specifically focusing on pipeline speed and durability settings. It includes a navigation menu on the left and detailed instructions on configuring these settings on the right.](https://kodekloud.com/kk-media/image/upload/v1752870441/notes-assets/images/Certified-Jenkins-Engineer-DemoPipeline-Durability/jenkins-pipeline-speed-durability-settings.jpg)

In the same screen, use the dropdown to finalize your choice:

![The image shows a Jenkins system configuration screen with options for setting pipeline speed and durability levels, including a dropdown menu for selecting the default speed/durability level.](https://kodekloud.com/kk-media/image/upload/v1752870442/notes-assets/images/Certified-Jenkins-Engineer-DemoPipeline-Durability/jenkins-system-configuration-pipeline-settings.jpg)

### 2. Branch-Level (Multibranch Projects)

For [multibranch pipelines](https://www.jenkins.io/doc/book/pipeline/multibranch/), you can assign durability per branch:

1. Go to your project’s **Configure** page.
2. Under **Repository Sources → Property strategy**, choose **Named branches**.
3. Add a property for `main` (or `master`) with **MAX\_SURVIVABILITY**.
4. Set **PERFORMANCE\_OPTIMIZED** (or another level) for all other branches.

![The image shows a configuration screen for a Jenkins pipeline, with options for setting the script path and selecting a pipeline branch speed/durability level.](https://kodekloud.com/kk-media/image/upload/v1752870443/notes-assets/images/Certified-Jenkins-Engineer-DemoPipeline-Durability/jenkins-pipeline-configuration-screen.jpg)

![The image shows a configuration screen for a Jenkins pipeline, with options for setting the script path and property strategy, and a dropdown menu for selecting build properties.](https://kodekloud.com/kk-media/image/upload/v1752870444/notes-assets/images/Certified-Jenkins-Engineer-DemoPipeline-Durability/jenkins-pipeline-configuration-screen-2.jpg)

### 3. Per-Pipeline Job

To set durability for a single pipeline job:

1. Open the job and click **Configure**.
2. Scroll to **Pipeline Speed and Durability**.
3. Select the desired durability level from the dropdown.

![The image shows a configuration screen from Jenkins, displaying various pipeline settings and options for a project.](https://kodekloud.com/kk-media/image/upload/v1752870445/notes-assets/images/Certified-Jenkins-Engineer-DemoPipeline-Durability/jenkins-pipeline-settings-configuration.jpg)

## Live Demo

### Demo 1: MAX\_SURVIVABILITY

This demo writes numbers to a file once per second. With **MAX\_SURVIVABILITY**, the build will resume after a Jenkins restart.

```groovy theme={null}
pipeline {
    agent any
    stages {
        stage('Durability Test Loop') {
            steps {
                script {
                    sh 'touch numbers.txt'
                    for (int i = 0; i < 100; i++) {
                        sh "echo ${i} >> numbers.txt"
                        sleep 1
                    }
                }
            }
        }
    }
}
```

1. Save and start the build.
2. On the controller host, kill Jenkins:

```bash theme={null}
ps aux | grep -i jenkins.war
kill -9 <JENKINS_PID>
systemctl status jenkins
```

3. After Jenkins restarts, the console shows:

```bash theme={null}
[Pipeline] sleep
Sleeping for 1 sec
[Pipeline] sh
+ echo 39
[Pipeline] sleep
Sleeping for 1 sec
Resuming build at Sun Nov 10 17:22:47 UTC 2024 after Jenkins restart
No need to sleep any longer
Ready to run at Sun Nov 10 17:22:48 UTC 2024
[Pipeline] sh
+ echo 40
```

Build execution continues from where it left off.

### Demo 2: PERFORMANCE\_OPTIMIZED

Switch the same job to **PERFORMANCE\_OPTIMIZED**, rerun, and repeat the kill/restart:

```bash theme={null}
ps aux | grep -i jenkins.war
kill -9 <JENKINS_PID>
systemctl status jenkins
```

After restart, you’ll see:

```bash theme={null}
ERROR: Cannot resume build because FlowNode 42 for FlowHead 1 could not be loaded. This is expected when using the PERFORMANCE_OPTIMIZED durability setting and Jenkins is not shut down cleanly. Consider switching to the MAX_SURVIVABILITY setting to prevent this.
Finished: FAILURE
```

> **triangle-alert** Under **PERFORMANCE\_OPTIMIZED**, incomplete builds cannot resume after an unclean shutdown. Plan accordingly if you require resumability.

## Conclusion

* **MAX\_SURVIVABILITY**: Best for mission-critical pipelines that must survive crashes.
* **PERFORMANCE\_OPTIMIZED**: Ideal when speed is paramount and resumability is not required.
* **SURVIVABLE\_NON\_ATOMIC**: Use as a balanced choice between safety and performance.

## Links and References

* [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
* [Multibranch Pipeline](https://www.jenkins.io/doc/book/pipeline/multibranch/)
* [Managing Jenkins Configuration](https://www.jenkins.io/doc/book/managing/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/77043650-89c2-4ad3-bbd1-e06eabe35581/lesson/73aa9019-4949-437c-bc12-7156d55f394f)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/77043650-89c2-4ad3-bbd1-e06eabe35581/lesson/f57253b8-6b2b-4a65-9bb8-bc64f90272ef)
