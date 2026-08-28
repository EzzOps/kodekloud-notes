# Demo Jenkins Folder Part 4

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Jenkins-Administration-and-Monitoring-Part-1/Demo-Jenkins-Folder-Part-4/page

Learn to propagate the worst child build status to parent folders for accurate dashboard health metrics in Jenkins.

Welcome to Part 4 of our Jenkins Folders series. In this lesson, you’ll learn how to propagate the worst child build status up to parent folders so that your dashboard weather icons always reflect nested pipeline health.

## Why Folder-Level Health Matters

By default, Jenkins folder icons display an aggregate health based only on direct children. This means a failure deep inside a nested folder might not be visible at a glance on your main dashboard.

<Callout icon="lightbulb">
  Make sure you have the [Folder Health Metrics Plugin](https://plugins.jenkins.io/cloudbees-folder-health-metrics/) installed before proceeding.
</Callout>

## Understanding Jenkins Weather Icons

On the Jenkins dashboard, each job and folder shows a "weather" icon indicating its health:

| Weather Icon     | Health % | Meaning             |
| ---------------- | -------- | ------------------- |
| ☀️ Sunny         | > 80%    | Excellent stability |
| 🌤️ Partly Sunny | 60–80%   | Good stability      |
| ☁️ Cloudy        | 40–60%   | Moderate stability  |
| 🌧️ Rainy        | 20–40%   | Unstable            |
| ⛈️ Stormy        | \< 20%   | Critical failures   |

<Frame>
  ![The image shows a Jenkins dashboard displaying a list of jobs with their statuses, build times, and other related information.](https://kodekloud.com/kk-media/image/upload/v1752870626/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-Folder-Part-4/jenkins-dashboard-jobs-statuses.jpg)
</Frame>

The legend below maps these icons to build success rates and status symbols:

<Frame>
  ![The image shows a Jenkins dashboard with an icon legend explaining various project statuses and health indicators. The legend includes symbols for build progress and project health percentages.](https://kodekloud.com/kk-media/image/upload/v1752870627/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-Folder-Part-4/jenkins-dashboard-project-status-legend.jpg)
</Frame>

## Default vs. Worst-Child Health

Consider the **Shared Infrastructure** folder:

* It shows a ☀️ sunny icon (≥ 80% healthy), yet the nested **Team B** folder inside has a failing build.
* When you open **Team B**, you see a stormy icon and the message *“build stability: all recent builds failed.”*

However, that failure does **not** bubble up to **Shared Infrastructure**—by default, only direct children count.

## Step-by-Step: Propagate Worst-Child Health

Follow these steps to ensure a parent folder reflects the worst health of all nested items:

1. From the dashboard, **click** the target folder (e.g., **Team B**).
2. Select **Configure** from the sidebar.
3. Scroll to the **Health metrics** section.
4. Click **Add** and choose **Worst child health**.
5. **Check** the **Recursive** box to include all nested descendants.
6. Click **Apply** and then **Save**.

<Frame>
  ![The image shows a Jenkins configuration screen for a job named "team-b" under "shared-infrastructure," with options for setting display name, description, and health metrics.](https://kodekloud.com/kk-media/image/upload/v1752870628/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-Folder-Part-4/jenkins-team-b-job-configuration.jpg)
</Frame>

<Callout icon="lightbulb">
  The **Recursive** option ensures that failures at any depth are included in the parent folder’s health calculation.
</Callout>

### Verify the Result

1. Return to **Shared Infrastructure** view.
2. Confirm the folder icon now matches the worst status of its children (including **Team B** failures).
3. Repeat this configuration for any other folders in your hierarchy.

## Links and References

* [Jenkins Folders Plugin](https://plugins.jenkins.io/cloudbees-folder/)
* [Folder Health Metrics Plugin](https://plugins.jenkins.io/cloudbees-folder-health-metrics/)
* [Jenkins Documentation](https://www.jenkins.io/doc/)
* [Managing Build Stability](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)

Thank you for following this lesson. Your Jenkins dashboard will now always surface the true health of nested pipelines!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/bf3ddc28-a03d-4738-9f98-2779d81482f5/lesson/ff549034-ac35-43ff-86e0-1097ba8b0d79" />
</CardGroup>
