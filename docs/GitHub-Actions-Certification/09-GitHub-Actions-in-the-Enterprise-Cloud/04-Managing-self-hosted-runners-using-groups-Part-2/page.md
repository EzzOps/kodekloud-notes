# Managing self hosted runners using groups Part 2

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/GitHub-Actions-in-the-Enterprise-Cloud/Managing-self-hosted-runners-using-groups-Part-2/page

This article covers managing self-hosted GitHub Actions runners, including creating custom groups, moving runners, and configuring access controls for secure workflows.

Welcome to Part 2 of our guide on managing self-hosted GitHub Actions runners at the enterprise level. In Part 1, we provisioned a runner and attached it to the default enterprise group. Now, we'll dive into creating custom runner groups, moving runners between them, and configuring access controls to ensure your workflows run securely and predictably.

> **lightbulb** If you haven’t set up your first self-hosted runner yet, check out [Part 1: Provisioning Self-Hosted Runners](#).

## What Are Runner Groups?

Runner groups let you organize your self-hosted runners under enterprise or organization scopes. You can apply consistent security, network, and repository access policies across each group. For comprehensive details, see the official [GitHub documentation on managing access to self-hosted runners using groups](https://docs.github.com/en/enterprise-cloud@latest/actions/hosting-your-own-runners/managing-access-to-self-hosted-runners).

![The image shows a GitHub Docs page about managing access to self-hosted runners using groups, with navigation options on the left and article content on the right.](https://kodekloud.com/kk-media/image/upload/v1752876250/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part-2/github-docs-managing-access-self-hosted-runners.jpg)

***

## 1. Creating a New Runner Group

1. Go to **Enterprise settings** > **Policies** > **Actions** > **Runner groups**.
2. Click **New runner group**.
3. Fill in the details:
   * **Name**: e.g., `Production Enterprise Group`
   * **Organization access**: select one or more orgs
   * **Public repositories**: enable if needed
   * **Workflow access**: leave unconfigured for now
4. Click **Create group**.

You’ll now see your new group alongside the default enterprise group.

![The image shows a GitHub interface for creating a new runner group, with options for group name, organization access, workflow access, and network configurations.](https://kodekloud.com/kk-media/image/upload/v1752876251/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part-2/github-new-runner-group-interface.jpg)

***

## 2. Viewing Runner Groups at the Organization Level

Switch to **Organization settings** > **Actions** > **Runner groups**. Both the **Default** group and your `Production Enterprise Group` (with zero runners) should be listed.

![The image shows a GitHub Enterprise interface with a focus on the "Runner groups" section under "Actions" settings, displaying options for managing runner groups.](https://kodekloud.com/kk-media/image/upload/v1752876253/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part-2/github-enterprise-runner-groups-actions.jpg)

***

## 3. Moving a Runner to the New Group

1. Return to **Enterprise settings** > **Actions** > **Runners**.
2. Select your **Enterprise Linux Runner** (currently under the default group).
3. Click **Move**, then choose **Production Enterprise Group**.
4. (Optional) Update labels—e.g., replace `enterprise` with `production`.
5. Refresh to see the updated label.

![The image shows a GitHub Enterprise interface for managing a self-hosted runner, with options to move the runner to different groups and a message indicating no active jobs.](https://kodekloud.com/kk-media/image/upload/v1752876254/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part-2/github-enterprise-self-hosted-runner-interface.jpg)

![The image shows a dashboard interface for a Linux x64 runner configuration, labeled with tags like "self-hosted" and "enterprise," indicating no active jobs currently running.](https://kodekloud.com/kk-media/image/upload/v1752876255/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part-2/linux-x64-runner-dashboard-self-hosted.jpg)

***

## 4. Verifying the Runner at the Organization Level

Back in **Organization settings** > **Actions** > **Runner groups**, open `Production Enterprise Group`. You should now see your runner listed.

![The image shows a GitHub settings page for a runner group named "production-enterprise-group" within the "kodekloud-training-organization." It includes options for repository and workflow access.](https://kodekloud.com/kk-media/image/upload/v1752876256/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part-2/github-settings-production-enterprise-group.jpg)

> At this stage, no repositories or workflows are allowed, so the group cannot pick up jobs yet.

***

## 5. Configuring Access Controls

Runner groups enable you to restrict which repos and workflows can use your self-hosted runners.

1. Edit **Production Enterprise Group**.
2. Under **Repository access**, select the repositories (e.g., `enterprise-actions-demo`).
3. (Optional) Allow public repositories.
4. Under **Workflow access**, leave at 0 for now.
5. Click **Save**.

![The image shows a GitHub settings page for managing runner groups, specifically for a group named "production-enterprise-group," with options for repository and workflow access.](https://kodekloud.com/kk-media/image/upload/v1752876258/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part-2/github-settings-runner-groups-production.jpg)

![The image shows a GitHub interface for updating a runner group, with options for setting organization access and workflow access. The sidebar includes navigation options like Overview, Organizations, and Actions.](https://kodekloud.com/kk-media/image/upload/v1752876259/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part-2/github-runner-group-update-interface.jpg)

***

## 6. Triggering and Troubleshooting a Workflow

1. In the `enterprise-actions-demo` repo, trigger a workflow run manually.
2. You’ll see the job remain **pending** because no workflows are yet allowed.

![The image shows a GitHub Actions interface displaying the details of a completed job named "demo\_job," including setup and execution steps.](https://kodekloud.com/kk-media/image/upload/v1752876260/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part-2/github-actions-demo-job-details.jpg)

> **triangle-alert** Pending jobs usually mean your runner group isn’t authorized to run any workflows. Update **Workflow access** to allow specific or all workflows.

3. Go back to **Enterprise settings** > **Actions** > **Runner groups** > **Production Enterprise Group**.
4. Set **Workflow access** to **All workflows** and save.

![The image shows a GitHub settings page for updating a runner group, with options for organization access, workflow access, and network configurations.](https://kodekloud.com/kk-media/image/upload/v1752876261/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part-2/github-settings-runner-group-update.jpg)

Once the settings propagate, the pending job will be picked up by your runner.

***

## 7. Inspecting the Job Output

In our example workflow, we use `curl` to display the runner’s public IP:

```bash theme={null}
curl -v http://httpbin.org/ip
```

Sample output:

```plaintext theme={null}
* TCP_NODELAY set
* Connected to httpbin.org (52.0.229.30) port 80 (#0)
> GET /ip HTTP/1.1
> Host: httpbin.org
> User-Agent: curl/7.68.0
> Accept: */*
< HTTP/1.1 200 OK
...
{
  "origin": "35.188.139.128"
}
```

You can also verify directly on your runner host:

```bash theme={null}
curl ifconfig.me
