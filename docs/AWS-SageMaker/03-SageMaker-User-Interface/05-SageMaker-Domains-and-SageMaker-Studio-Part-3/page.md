# SageMaker Domains and SageMaker Studio Part 3

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/SageMaker-User-Interface/SageMaker-Domains-and-SageMaker-Studio-Part-3/page

Guide to adding SageMaker Studio user profiles to a Domain, configuring apps and storage, distinguishing Studio new EBS from Classic EFS, and following security and resource best practices

This guide walks through adding a new SageMaker Studio user profile to a SageMaker Domain, explains the key configuration choices, and highlights best practices for security, storage, and resource management. Follow the steps in sequence and use the checks described to confirm whether a Studio space uses EBS (Studio new) or EFS (Studio Classic).

Step 1 — Add a user profile from the SageMaker Domain "User profiles" tab. In a quick-start domain you often begin with one default user. To add another, open the User profiles tab and click Add user.

<Frame>
  <img alt="The image shows a screenshot of an Amazon SageMaker &#x22;Domain details&#x22; page under the &#x22;User profiles&#x22; tab, with a list of user profiles and an &#x22;Add user&#x22; button. The slide title reads &#x22;Workflow: Adding Another User.&#x22;" />
</Frame>

A dialog opens to capture the new user settings. Provide a user name (for example, user2) and select an execution role. The execution role is an IAM role that controls what AWS resources the user can access when using Studio.

<Frame>
  <img alt="A screenshot titled &#x22;Workflow: Adding Another User&#x22; showing the General settings form for creating a new user, with a Name field filled with &#x22;user2&#x22;, an Execution role dropdown, and an optional Tags section. The left sidebar lists steps (Configure Applications, Customize Studio UI, etc.) and there's a Cancel/Next button at the bottom-right." />
</Frame>

Step 2 — Configure the applications available to this user. AWS is deprecating SageMaker Studio Classic, so the default and recommended selection is SageMaker Studio — new (Studio v2). Only select Studio Classic for specific legacy needs.

<Frame>
  <img alt="A screenshot titled &#x22;Workflow: Adding Another User&#x22; showing the Amazon SageMaker &#x22;Add user profile&#x22; Configure Applications page with options for SageMaker Studio, JupyterLab, and Canvas. The left sidebar lists setup steps while the main pane displays settings and toggles for choosing a default studio and idle shutdown." />
</Frame>

Best practice: a SageMaker user profile should represent a single person. The audit, security, and billing models assume one Identity Center (or IAM) user maps to exactly one Studio user profile. Sharing profiles across people undermines auditability and isolation.

<Frame>
  <img alt="A presentation slide titled &#x22;Workflow: Adding Another User&#x22; that lists Identity Center best practices: one Identity Center user = one SageMaker profile, and profiles are auto-created when assigned to SageMaker Studio." />
</Frame>

> **lightbulb** One Identity Center user should normally equal one SageMaker profile. In enterprise setups, you can auto-create profiles when users are assigned access via AWS Identity Center / SSO.

Security benefits from one-profile-per-user include clear audit trails, resource isolation, and role-based access control mapped to individuals.

<Frame>
  <img alt="A presentation slide titled &#x22;Workflow: Adding Another User&#x22; showing &#x22;Security Benefits&#x22; with a shield icon and four items: audit trails, proper isolation, role-based access, and secure workspaces. The slide has a dark blue background and a small © KodeKloud note." />
</Frame>

From a resource management perspective, per-user profiles allow quotas, isolated storage accounting, separate execution roles, and clearer compute usage metrics for cost attribution.

<Frame>
  <img alt="A presentation slide titled &#x22;Workflow: Adding Another User&#x22; describing Resource Management, with a gear icon on the left and four colored bullet points outlining quotas, personal storage allocation, separate execution roles, and better tracking of compute usage per user." />
</Frame>

Avoid generic team or shared profiles. Each team member should have a distinct profile — do not reuse a profile for multiple IAM or Identity Center users.

<Frame>
  <img alt="A presentation slide titled &#x22;Workflow: Adding Another User&#x22; showing three boxed tips with icons. Each tip warns against sharing user profiles, creating generic team profiles, or using a single profile for multiple IAM/Identity Center users." />
</Frame>

> **warning** Do not share a single SageMaker profile across multiple people. Shared profiles break security, audit logs, and cost allocation.

When you continue the wizard, Studio (new) offers UI customization toggles — you can enable or hide JupyterLab, Code Editor, Canvas, RStudio, and third-party integrations. Expose only the apps the user needs to reduce UI clutter and accidental usage.

<Frame>
  <img alt="A presentation slide titled &#x22;Workflow: Customizing UI&#x22; showing a screenshot of an application settings page (Amazon SageMaker Studio) where you can toggle which apps — like JupyterLab, Code Editor, RStudio and others — are displayed in the studio UI. The right side shows a preview of the selected application icons." />
</Frame>

Note: these toggles only change visibility. To actually restrict a user from using a capability, adjust the IAM permissions attached to the execution role for that profile.

When the wizard reaches Data and Storage, the UI may still show an AutoMountHomeEFS option even if you selected Studio (new). This is a legacy artifact: Studio Classic uses EFS, while Studio (new) uses EBS for notebook spaces.

<Frame>
  <img alt="A slide titled &#x22;Workflow: Data and Storage&#x22; showing an Amazon SageMaker &#x22;Add user profile&#x22; screen with Data and Storage settings like AutoMountHomeEFS and CustomPosixUserConfig. The panel shows options (e.g., &#x22;Inherit settings from domain&#x22;) and navigation buttons including Back and Next." />
</Frame>

After creating the profile you will see it listed under the User profiles tab. You can then launch Studio as that new user and open a JupyterLab space.

Step 3 — Confirm whether a JupyterLab space is backed by EFS (Classic) or EBS (new). Open a terminal inside JupyterLab and run df -h:

```bash theme={null}
