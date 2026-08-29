# Demo Notifications Demo

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Notifications/Demo-Notifications-Demo/page

Guide to configuring GitHub notifications, watch settings, email verification, delivery preferences, custom routing, and alert types to control where and when repository and account updates are received.

In this lesson we’ll walk through GitHub’s notification options and how to control where and when you receive updates—at both the repository and account level. You’ll learn how to tune the volume and types of notifications you get, route them to specific email addresses, and understand what to expect in notification emails.

## Repository-level watch settings

Repository watch settings let you control the overall scope of events you receive from a repository. Choose one of the built-in levels or select a custom set of events.

<Frame>
  <img alt="The image shows a GitHub repository page named &#x22;block-buster&#x22; with the files and directories listed, along with a notification settings menu open." />
</Frame>

Watch options at a glance:

| Watch level   | Description                                                                                              | Recommended for                            |
| ------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| All Activity  | Receive notifications for virtually all activity in the repo (issues, PRs, releases, discussions, etc.). | Maintainers, core contributors             |
| Participating | Only notifications for conversations you’re directly involved in (comments, reviews, assignments).       | Contributors keeping involvement-limited   |
| Mentions      | Only when you are explicitly mentioned.                                                                  | Stakeholders who only want direct mentions |
| Ignoring      | No notifications from this repository.                                                                   | Unrelated projects or archived repos       |

You can also choose a custom subscription to follow only particular event types for a repository (issues, pull requests, releases, discussions, etc.). This gives finer control than the global watch levels.

## Subscribe to specific repository events

The repository subscription popup provides granular selection of event types so you only receive the notifications you need.

<Frame>
  <img alt="The image shows a GitHub repository page titled &#x22;block-buster&#x22; with a popup window for subscribing to repository events like issues, pull requests, releases, and discussions." />
</Frame>

Use custom subscriptions when you want:

* Issue-only updates for triage teams.
* Pull request notifications for reviewers.
* Release alerts for product managers.
* Discussion updates for community leads.

## Account-level settings and email verification

Account-level settings determine where notifications are delivered. The first step is to add and verify the email addresses you want GitHub to use.

<Frame>
  <img alt="This image shows the email settings page of a GitHub account, where a verified email address is connected to Google. Various options for managing emails and privacy settings are visible." />
</Frame>

Verified addresses will appear as targets when configuring default delivery and routing rules.

## Default notification delivery and preferences

The Notifications settings page controls the default delivery channel and other preferences—whether notifications go to your primary email, to the GitHub web UI (the bell icon), or both.

<Frame>
  <img alt="The image shows the notifications settings page of a GitHub account, where various email notification preferences and subscriptions are being managed." />
</Frame>

Common preferences to review:

* Default delivery method: email, web, or both.
* Automatically apply participating subscriptions.
* Which notification types send email vs. only web alerts.
* Notification frequency and batching options (if available).

## Custom routing for organizations and advanced recipients

If you’re part of multiple organizations or need different addresses for different notification sources, use custom routing rules. These allow you to send notifications from specific organizations or repositories to different emails.

<Frame>
  <img alt="The image shows a GitHub settings page for notifications, specifically the custom routing section, with options to add new routes and manage email notifications." />
</Frame>

Examples:

* Route Organization A to `eng-notifications@example.com`.
* Route Organization B to `security-alerts@example.com`.
* Keep personal project notifications on your primary email.

<Callout icon="lightbulb">
  Verify any email addresses you add to your account. Only verified emails can be used as notification targets or custom routing destinations.
</Callout>

## Other important notification settings

* Subscription defaults for repositories and teams: choose whether new repositories you join default to GitHub, email, or both.
* Participating subscriptions: enable or disable auto-application when you participate in conversations.
* GitHub Actions notifications: choose between receiving status updates for all workflow runs or only failed runs.
* Dependabot and security alerts: enable email/web alerts for dependency and security findings.
* Sessions and audit-related alerts: available for organizations or accounts with audit logging.

<Frame>
  <img alt="The image shows a GitHub notification settings page, where options like email updates and notification channels for repositories are customizable. There is a pop-up open for selecting notification channels with options for GitHub and email." />
</Frame>

## What notification emails contain

* Repository notifications: who opened or commented on an issue/PR, assignment changes, labels, and links to view the full conversation.
* Pull request emails: PR title and description, key comments (including inline review comments), status checks, and direct links to the PR and changed files.
* Actions notifications: workflow run status (success, failure), links to logs and the specific workflow run for debugging.
* Security/Dependabot alerts: vulnerability details, affected package, severity, and recommended fixes or PRs.

## Quick checklist

* Review repository watch settings for active repos.
* Verify every email you want to use for notifications.
* Set default delivery on the Notifications settings page.
* Create custom routing rules per organization when necessary.
* Configure GitHub Actions and Dependabot alerts to avoid missing critical failures.

That covers the main ways to control where and how GitHub notifies you about repository activity and account events. Adjust repository watch settings and account notification preferences to match the volume and types of alerts you want to receive.

## Links and references

* [GitHub Notifications documentation](https://docs.github.com/en/account-and-profile/managing-subscriptions-and-notifications-on-github)
* [Watching and unwatching a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/watching-and-unwatching-a-repository)
* [Configuring notification routing](https://docs.github.com/en/account-and-profile/managing-subscriptions-and-notifications-on-github/configuring-notification-routing)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/25862af1-db21-4e01-8bab-ff285c39506d/lesson/1484fa01-d31d-43aa-ac4e-ba16ee087ee7" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/25862af1-db21-4e01-8bab-ff285c39506d/lesson/efca5324-375e-4f5e-96b7-bb7a463c3c14" />
</CardGroup>
