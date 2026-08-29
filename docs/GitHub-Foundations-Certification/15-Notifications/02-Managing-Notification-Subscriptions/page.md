# Managing Notification Subscriptions

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Notifications/Managing-Notification-Subscriptions/page

Guide to managing GitHub notification subscriptions, controlling repository and conversation notifications, using custom filters and delivery destinations to reduce noise and route important events.

Notifications are the primary mechanism for tracking important activity across repositories and teams. Proper subscription management helps you focus on high-priority updates while reducing noise from low-value events.

You can control notification delivery at the repository level using four states:

| State                  | What it means                                                                                                                  | When to use it                                                                                         |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| Watching               | You receive notifications for all activity in the repository.                                                                  | Use for repositories you maintain or need to audit closely.                                            |
| Not watching (default) | You receive notifications only when you are @mentioned, participating in a thread, or explicitly subscribed to a conversation. | Default for repositories you contribute to occasionally.                                               |
| Ignoring               | All notifications for the repository are suppressed, including @mentions.                                                      | Use for forks, archived repos, or noisy projects you never need updates from.                          |
| Custom                 | Select which event types generate notifications (for example: issues, pull requests, releases).                                | Use to follow a subset of events without full noise (e.g., only release announcements or CI failures). |

In addition to repository-level settings, you can subscribe to individual conversations—issues, pull requests, or discussions—so you receive updates even when you are not otherwise participating. Use the Subscribe control in the right sidebar of an issue, pull request, or discussion to opt in.

<Frame>
  <img alt="The image displays a screenshot of a pull request on a code repository platform with an option to subscribe for notifications. A &#x22;Manual Subscription&#x22; button is highlighted at the bottom." />
</Frame>

To quickly find every conversation where you have been tagged, use the `mentions:` search qualifier in the GitHub search bar. For example:

```bash theme={null}
mentions:octocat
```

This is a fast way to audit outstanding items that require your attention.

You can also route notifications to different delivery destinations depending on your workflow. Manage these options under Settings → Notifications (your account settings). Common delivery destinations include:

| Destination         | Description                                                                                                                    | Typical usage                                                                           |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| Web                 | View alerts directly within the GitHub.com dashboard.                                                                          | Default for most developers who review notifications in the browser.                    |
| Email               | Receive notifications at your registered email address.                                                                        | Use for long-running threads or summaries that you want in your inbox.                  |
| Mobile              | Receive push notifications via the official GitHub mobile app.                                                                 | Good for urgent alerts when you're away from your desktop.                              |
| Custom destinations | Route events to external systems (for example, `Slack` or a CI dashboard) using integrations, third-party apps, or `webhooks`. | Forward only actionable events (like failed CI runs) to reduce noise in external tools. |

Use repository-level Custom settings together with per-conversation Subscribe controls to balance broad coverage with low noise. Filter which event types trigger integrations so that only relevant events (for example, failed builds or release tags) are forwarded to external tools.

<Callout icon="lightbulb">
  Tip: Combine repository-level Custom settings and per-conversation Subscriptions to get comprehensive coverage while minimizing interruptions. Route only high-action events (e.g., CI failures, security alerts, or release notes) to external tools like Slack or a monitoring dashboard.
</Callout>

<Callout icon="warning">
  Warning: If you set a repository to Ignoring, all notifications—including `@mentions`—are suppressed. Use Ignoring only when you are certain you will not miss critical calls to action.
</Callout>

Links and references

* [Searching on GitHub: Search qualifiers](https://docs.github.com/en/search-github/searching-on-github/searching-on-github)
* [Managing notifications on GitHub](https://docs.github.com/en/account-and-profile/managing-subscriptions-and-notifications-on-github/managing-notifications)
* [Webhooks and events on GitHub](https://docs.github.com/en/developers/webhooks-and-events/about-webhooks)
* [Slack](https://slack.com)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/25862af1-db21-4e01-8bab-ff285c39506d/lesson/33040505-610d-4737-bdc7-533b79b3df14" />
</CardGroup>
