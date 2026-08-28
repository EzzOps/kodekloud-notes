# Deploy
sudo apt-get install cowsay -y
export PATH="$PATH:/usr/games:/usr/local/games"
cat advice.message | cowsay -f $(ls /usr/share/cowsay/cows | shuf -n 1)
```

After applying these changes and saving them, trigger the build job. The build begins execution and queues the test job. As the test job runs, the Jenkins interface displays a dynamic visualization. In this scenario, the test job fails because one of the conditions to trigger the deploy job—a stable build of the test job—is not met. Review the build logs below to understand the failure:

```bash theme={null}
Started by upstream project "ascii-build-job" build number 5
originally caused by:
  Started by user Dasher Admin
Running as SYSTEM
Building in workspace /var/lib/jenkins/workspace/ascii-test-job
Copied 1 artifact from "ascii-build-job" build number 5
[ascii-test-job] $ /bin/sh -xe /tmp/jenkins156712682140079493978.sh
+ ls advice.json
advice.json
+ cat advice.json
+ jq -r '.slip.advice'
+ wc -w
+ [ 4 -gt 5 ]
+ cat advice.message
+ echo Advice -  Slate in the shower.
Advice -  Slate in the shower. has 5 words or less
+ exit 1
Build step 'Execute shell' marked build as failure
Skipped archiving because build is not successful
Finished: FAILURE
```

<Callout icon="lightbulb">
  The failure is not related to the simulated controller failure. It occurs because the test job's condition expects an advice message containing more than five words.
</Callout>

After re-triggering the build job, the test job passes in a subsequent run, and build number five completes successfully—causing the deploy job to be queued.

## Simulating a Controller Failure

When the deploy job starts, it executes the same sleep command for 3600 seconds. To simulate a controller failure manually, stop the Jenkins server with the following command:

```bash theme={null}
systemctl stop jenkins
```

After stopping Jenkins, attempting to refresh the Jenkins webpage will result in an "unreachable" error. To restart Jenkins, execute:

```bash theme={null}
systemctl start jenkins
```

Wait a few moments for Jenkins to come back online. Verify the server status using:

```bash theme={null}
systemctl status jenkins
```

An example output is as follows:

```bash theme={null}
● jenkins.service - Jenkins Continuous Integration Server
   Loaded: loaded (/usr/lib/systemd/system/jenkins.service; enabled; preset: enabled)
   Active: active (running) since Mon 2024-08-19 10:51:25 UTC; 3s ago
 Main PID: 37656 (java)
    Tasks: 49 (limit: 4607)
   Memory: 310.4M (peak: 310.9M)
      CPU: 15.008s
   CGroup: /system.slice/jenkins.service
           └─37656 /usr/bin/java -Djava.awt.headless=true -jar /usr/share/java/jenkins.war --webroot=/var/cache/jenkins/war

Aug 19 10:51:25 jenkins-controller-1 jenkins[37656]: 2024-08-19 10:51:25.575+0000 [id=31] INFO  jenkins.InitReac...
Aug 19 10:51:25 jenkins-controller-1 jenkins[37656]: 2024-08-19 10:51:25.612+0000 [id=33] INFO  jenkins.InitReac...
Aug 19 10:51:25 jenkins-controller-1 jenkins[37656]: 2024-08-19 10:51:25.613+0000 [id=32] INFO  jenkins.InitReac...
Aug 19 10:51:25 jenkins-controller-1 jenkins[37656]: 2024-08-19 10:51:25.619+0000 [id=32] INFO  c.a.s.j.p.d.cache...
Aug 19 10:51:25 jenkins-controller-1 jenkins[37656]: 2024-08-19 10:51:25.619+0000 [id=31] INFO  jenkins.InitReac...
Aug 19 10:51:25 jenkins-controller-1 jenkins[37656]: 2024-08-19 10:51:25.632+0000 [id=47] INFO  jenkins.InitReac...
Aug 19 10:51:25 jenkins-controller-1 jenkins[37656]: 2024-08-19 10:51:25.640+0000 [id=30] INFO  jenkins.InitReac...
Aug 19 10:51:25 jenkins-controller-1 jenkins[37656]: 2024-08-19 10:51:25.612+0000 [id=30] INFO  hudson.lifecycle...
Aug 19 10:51:25 jenkins-controller-1 jenkins[37656]: 2024-08-19 10:51:25.746+0000 [id=47] INFO  c.a.s.j.p.d.cache...
```

After you log in again (due to Jenkins security protocols), you will notice that the deploy job has been terminated and is marked as a failure. This outcome occurs because Freestyle Projects stop the build execution permanently if a controller failure—whether manual or accidental—happens during a running build.

The following snippet reaffirms this behavior:

```bash theme={null}
Building in workspace /var/lib/jenkins/workspace/ascii-deploy-job
Copied 1 artifact from "ascii-test-job" build number 5
[ascii-deploy-job] $ /bin/sh -xe /tmp/jenkins98367258698972721042.sh
+ sleep 3600
Build step 'Execute shell' marked build as failure
Finished: FAILURE
```

<Callout icon="triangle-alert">
  A significant downside of using Freestyle Projects is that they do not support resuming tasks after a controller failure. For critical workflows, consider using Pipeline Projects.
</Callout>

## Understanding the Jenkins Dashboard

For newcomers, the Jenkins dashboard might be overwhelming at first, especially when you encounter various icons like the sun or clouds. These icons provide quick visual feedback about build statuses and overall project health. Click on “More Actions” in the dashboard to view an icon legend with detailed descriptions.

<Frame>
  ![The image shows a Jenkins dashboard displaying the status of various build jobs, including their last success, last failure, and duration.](https://kodekloud.com/kk-media/image/upload/v1752879442/notes-assets/images/Jenkins-For-Beginners-Controller-Failure-Freestyle-Project/jenkins-dashboard-build-status.jpg)
</Frame>

<Frame>
  ![The image shows a Jenkins dashboard with an "Icon legend" pop-up explaining various build statuses using different colored icons.](https://kodekloud.com/kk-media/image/upload/v1752879443/notes-assets/images/Jenkins-For-Beginners-Controller-Failure-Freestyle-Project/jenkins-dashboard-build-status-icons.jpg)
</Frame>

## Conclusion

This article has explored how Freestyle Projects in Jenkins handle controller failures. As demonstrated, if a controller failure occurs during a running build, the job is terminated and does not resume automatically. In future discussions, we will examine how Pipeline Projects can overcome this challenge by supporting build continuity and recovery.

Thank you for reading!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/jenkins-for-beginners/module/6a945431-1040-4467-b874-ef7d24d5a6a0/lesson/c29203da-190c-46a5-9a4f-1f490acf7f0d" />
</CardGroup>


# Jenkins Fingerprints

Source: https://notes.kodekloud.com/docs/Jenkins-For-Beginners/Extending-Jenkins/Jenkins-Fingerprints/page

Jenkins fingerprints track file usage across jobs, helping manage dependencies and improve workflow efficiency in interconnected projects.

Jenkins fingerprints are a powerful feature that allows you to track file usage across different jobs. This mechanism is especially useful when managing multiple interconnected projects. By recording fingerprints at the project level, Jenkins can identify which versions of a file are used throughout your builds. Essentially, the fingerprint is an MD5 checksum stored with metadata about which builds have utilized the file, without actually storing the file itself. You can review these details on the Jenkins home/fingerprints page.

In the demonstrated workflow, an ASCII build job generates an artifact, which is then used by a test job. This test job creates another artifact that is later consumed by a deploy job. The dependency chain is as follows:

* The deploy job depends on the test job.
* The test job depends on the build job.

To effectively track this process, manual configuration of fingerprint recording is required. Follow these steps to set it up:

1. Open the job configuration page.
2. Scroll down to the **Post-build Actions** section.
3. Select the option to **Record fingerprints of files to track usage**.

<Callout icon="lightbulb">
  Click the help button for further clarification on this feature.
</Callout>

4. Enter the file name(s) you wish to track. In this example, the file is named `advice.json`.

<Frame>
  ![The image shows a Jenkins configuration screen for a job named "ascii-build-job," with options for triggering builds and recording file fingerprints.](https://kodekloud.com/kk-media/image/upload/v1752879459/notes-assets/images/Jenkins-For-Beginners-Jenkins-Fingerprints/jenkins-ascii-build-job-config.jpg)
</Frame>

After setting up the configuration for the build job, click **Save**. Although you can repeat this process for the test and deploy jobs, this demonstration focuses solely on configuring the build job.

Once you trigger a build (for instance, build number 8), the `advice.json` file will be generated and assigned a fingerprint. Clicking on the fingerprint link will display the MD5 checksum for the file, along with a detailed list of jobs and their build IDs that have utilized this file. This method offers a clear view of how Jenkins tracks file dependencies across various builds.

Furthermore, Jenkins provides an option to track additional files through the dashboard's fingerprint feature. You can upload any file and retrieve comprehensive usage details, such as when the file was used, the dependent projects, and the associated build IDs.

<Frame>
  ![The image shows a Jenkins dashboard with a list of jobs, their statuses, last success and failure times, and durations. The interface includes options like "New Item," "Build History," and "Manage Jenkins."](https://kodekloud.com/kk-media/image/upload/v1752879460/notes-assets/images/Jenkins-For-Beginners-Jenkins-Fingerprints/jenkins-dashboard-jobs-statuses.jpg)
</Frame>

For a hands-on approach, utilize the **Check File Fingerprint** tool available on the Jenkins dashboard. This feature allows you to upload a file, verify its fingerprint against the Jenkins database, and receive an in-depth analysis of its use across projects.

<Frame>
  ![The image shows a Jenkins dashboard with the "Check File Fingerprint" feature, allowing users to upload a file to check its fingerprint against the database. The interface includes options like "New Item," "Build History," and "Manage Jenkins."](https://kodekloud.com/kk-media/image/upload/v1752879461/notes-assets/images/Jenkins-For-Beginners-Jenkins-Fingerprints/jenkins-dashboard-file-fingerprint.jpg)
</Frame>

<Callout icon="lightbulb">
  By following these steps, you can efficiently monitor and manage file dependencies in your Jenkins projects using fingerprints.
</Callout>

This guide has detailed how Jenkins utilizes fingerprints to track file usage across different builds and jobs. Implementing these practices will improve your project's dependency management and overall workflow efficiency. Happy building!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/jenkins-for-beginners/module/6a945431-1040-4467-b874-ef7d24d5a6a0/lesson/e23db1d6-105b-4068-8524-929518a5f977" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/jenkins-for-beginners/module/6a945431-1040-4467-b874-ef7d24d5a6a0/lesson/c7258333-58e2-440c-822b-507a056998f2" />
</CardGroup>
