# => 35.188.139.128
```

***

## 8. Summary of Key Steps

| Step                         | Action                                                            |
| ---------------------------- | ----------------------------------------------------------------- |
| 1. Create Runner Group       | Enterprise settings → Policies → Actions → Runner groups → New    |
| 2. Move Runner               | Select runner → Move → Choose group                               |
| 3. Update Labels             | Edit runner labels (e.g., replace `enterprise` with `production`) |
| 4. Set Repository Access     | Runner group → Edit → Select repos                                |
| 5. Configure Workflow Access | Runner group → Edit → Allow specific/all workflows                |
| 6. Troubleshoot Pending Jobs | Confirm access settings at both enterprise and org levels         |

<Frame>
  ![The image shows a GitHub settings page for managing runner groups, with options for repository and workflow access. It includes details about a specific runner named "enterprise-linux-runner" which is active.](https://kodekloud.com/kk-media/image/upload/v1752876263/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part-2/github-settings-runner-groups-management.jpg)
</Frame>

***

## Links and References

* [Managing Access to Self-Hosted Runners](https://docs.github.com/en/enterprise-cloud@latest/actions/hosting-your-own-runners/managing-access-to-self-hosted-runners)
* [GitHub Actions Runner Groups](https://docs.github.com/en/enterprise-cloud@latest/admin/policies/runner-groups)
* [Ifconfig.me Service](https://ifconfig.me)

In this lesson, you learned how to create runner groups, move runners, configure labels and access controls, and troubleshoot pending workflows. Always ensure your runner groups have the correct repository and workflow permissions to avoid unexpected pending jobs.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/9b181319-216b-42b5-8069-9d56650f2d53/lesson/95158347-254b-45e1-939e-b4f9dd64a511" />
</CardGroup>


# Managing self hosted runners using groups Part1

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/GitHub-Actions-in-the-Enterprise-Cloud/Managing-self-hosted-runners-using-groups-Part1/page

This guide explains configuring and managing self-hosted GitHub Actions runners across GitHub Enterprise and organization scopes.

In this guide, you’ll learn how to configure and manage self-hosted GitHub Actions runners across GitHub Enterprise and organization scopes. We’ll cover:

* Reviewing Enterprise vs. Organization settings
* Creating and renaming runner groups
* Assigning runners to repositories (including public repos)
* Installing a self-hosted runner on Linux
* Running a sample workflow on your new runner

***

## 1. Compare Enterprise and Organization Dashboards

First, open two browser tabs side by side:

Tab 1: **Enterprise Overview**

<Frame>
  ![The image shows a GitHub enterprise dashboard for "kodekloud-training-enterprise," featuring navigation options like Overview, Getting Started, and Settings, with a prompt to create a README.](https://kodekloud.com/kk-media/image/upload/v1752876264/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part1/github-enterprise-dashboard-kodekloud-training.jpg)
</Frame>

Tab 2: **Organization Home**

<Frame>
  ![The image shows a GitHub organization page for "kodekloud-training-organization," which is part of "kodekloud-training-enterprise." It includes options for inviting members, customizing permissions, and setting up discussions.](https://kodekloud.com/kk-media/image/upload/v1752876266/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part1/github-organization-kodekloud-training.jpg)
</Frame>

Notice the UI placement:

* Enterprise settings live in the **left sidebar**.
* Organization and user settings appear in the **top navigation**.

***

## 2. View and Rename Organization Runner Groups

1. In your organization, navigate to **Settings > Actions > Runner groups**.
2. You’ll see the **default** runner group:

<Frame>
  ![The image shows a GitHub organization settings page for "kodekloud-training-organization," specifically focusing on the "Runner groups" section, where users can manage access to shared organization runners.](https://kodekloud.com/kk-media/image/upload/v1752876267/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part1/github-organization-settings-runner-groups.jpg)
</Frame>

3. Click into the default group and observe that **public repository support** cannot be toggled here:

<Frame>
  ![The image shows a GitHub organization settings page for "kodekloud-training-organization," focusing on runner group settings and repository access options.](https://kodekloud.com/kk-media/image/upload/v1752876268/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part1/github-organization-settings-runner-group.jpg)
</Frame>

<Callout icon="triangle-alert">
  Public repository support for a runner group is only configurable at the **enterprise** level. You won’t be able to enable it within the organization settings.
</Callout>

***

## 3. Configure Enterprise Runner Group Policies

Switch to **Enterprise > Policies > Actions > Runner groups**:

<Frame>
  ![The image shows a GitHub interface for updating a runner group, with options for setting the group name, organization access, and workflow access. The sidebar includes navigation links for various settings and features.](https://kodekloud.com/kk-media/image/upload/v1752876269/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part1/github-runner-group-update-interface.jpg)
</Frame>

Here you can:

| Option                     | Description                                                |
| -------------------------- | ---------------------------------------------------------- |
| Group Name                 | Rename (e.g., `default enterprise runner group`)           |
| Organization Access        | Restrict to specific orgs or allow all                     |
| Repository Access          | Choose **All**, **Selected**, and include **Public** repos |
| Workflow File Restrictions | Limit to certain workflow filenames                        |

Apply your changes and save.

***

## 4. Assign Runner Group to Organization Repositories

Return to the organization’s **Runner groups** page and refresh. The renamed enterprise group will appear. Click **Add repository access**:

<Frame>
  ![The image shows a GitHub settings page for a runner group in the "kodekloud-training-organization," with a pop-up window for selecting repository access.](https://kodekloud.com/kk-media/image/upload/v1752876270/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part1/github-settings-runner-group-repository-access.jpg)
</Frame>

Select:

* **All repositories**
* **Include public repositories**

Save to propagate the policy.

***

## 5. Install a Self-Hosted Runner on Linux

In the enterprise settings, go to **Policies > Actions > Runners**:

<Frame>
  ![The image shows a GitHub interface for managing GitHub-hosted runners, indicating no active jobs and displaying various labels for different operating systems. The sidebar includes options like Overview, Organizations, and Actions.](https://kodekloud.com/kk-media/image/upload/v1752876271/notes-assets/images/GitHub-Actions-Certification-Managing-self-hosted-runners-using-groups-Part1/github-runners-interface-no-active-jobs.jpg)
</Frame>

Click **New self-hosted runner**, choose **Linux** → **x64**, and follow the prompts. On your Linux VM, run:

```bash theme={null}
