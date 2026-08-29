# Discussions

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Discussions/Discussions/page

Guidance on using GitHub Discussions including purpose, enabling and configuration steps, use cases, moderation roles, conversion between issues and discussions, and best practices for community engagement.

## What are GitHub Discussions?

GitHub Discussions provides a forum-style space inside a repository for threaded, community-oriented conversations that do not require immediate code changes. It’s ideal for:

* Technical Q\&A and troubleshooting
* Brainstorming features and collecting ideas
* Onboarding, community support, and announcements
* General feedback and project coordination

Because Discussions is part of the repository, it follows the repository’s visibility and access controls: public repositories expose Discussions publicly, while private repositories keep them restricted to collaborators.

<Callout icon="warning">
  Remember: Discussions inherit repository visibility. If your repository is public, Discussions will be public as well—plan moderation and privacy-sensitive conversations accordingly.
</Callout>

## Common use cases

| Use case                 | Example                                      |
| ------------------------ | -------------------------------------------- |
| Q\&A / Technical support | `How do I configure OAuth for this project?` |
| Ideas & Roadmap          | Feature proposals and voting on priorities   |
| Announcements            | Release notes, community updates             |
| Onboarding               | How-to guides, contributor welcome threads   |

## How do we enable and configure GitHub Discussions?

Only repository administrators (owners or users with admin permissions) can enable Discussions.

<Frame>
  <img alt="The image provides instructions for enabling the &#x22;Discussions&#x22; feature in a GitHub repository, showing where to access settings and set it up." />
</Frame>

Steps to enable and configure Discussions:

1. Go to the repository Settings.
2. Under Features, check the Discussions option to enable it.
3. After enabling, GitHub will prompt you to create a welcome post to introduce the community to the Discussions space.
4. Configure categories (for example: Q\&A, Ideas, Announcements) to organize threads and assign moderation roles as needed.

## Example: A welcome post template

Use a clear, concise welcome post to set expectations and make it easy for contributors to participate. Here is a starter template you can paste into a new Discussion:

```text theme={null}
Welcome to the [repo-name] Discussions!

Purpose
- This space is for Q&A, feature ideas, and community announcements.

How to participate
- Use clear titles and include steps to reproduce for technical questions.
- Use the appropriate category (Q&A, Ideas, Announcements).
- If a conversation turns into a bug or actionable task, we may convert it into an Issue.

Useful links
- Contribution guide: https://github.com/owner/repo/CONTRIBUTING.md
- Code of conduct: https://github.com/owner/repo/CODE_OF_CONDUCT.md

Thanks for contributing!
```

## How people interact with Discussions

Contributors can:

* Start new threads or browse existing ones
* Reply, react (emoji), and upvote helpful responses
* Mark an answer as the accepted solution in Q\&A-style threads
* Convert issues into discussions or convert discussions into issues when a conversation becomes actionable
* Pin important discussions for visibility (moderator action)

Tip: Encourage users to include a clear title, expected behavior, and reproduction steps when reporting problems—this increases the chance of getting a useful answer quickly.

## Moderation and permissions

| Role                         | Typical capabilities                                                                            |
| ---------------------------- | ----------------------------------------------------------------------------------------------- |
| Admin / Repo owner           | Enable/disable Discussions, manage categories, pin threads, assign moderators, moderate content |
| Maintainers / Moderators     | Categorize threads, pin/unpin, moderate posts, convert between issues and discussions           |
| Collaborators / Contributors | Create and reply to threads, react, upvote, mark accepted answers (where allowed)               |

Assign trusted contributors as moderators to scale moderation and keep the space healthy.

## When to convert between Issues and Discussions

* Convert a discussion into an issue when the conversation yields a clear bug report, feature request, or task that needs tracking.
* Convert an issue into a discussion when the topic requires broader community brainstorming or Q\&A rather than an immediate code change.

## Best practices for using Discussions effectively

* Use categories (Q\&A, Ideas, Announcements) consistently to make content discoverable.
* Pin and highlight canonical resources (FAQ, onboarding guides) to reduce duplicate questions.
* Encourage accepted answers for Q\&A threads to help future searchers find solutions quickly.
* Moderate respectfully and maintain a visible code of conduct and contribution guidelines.

<Callout icon="lightbulb">
  Enable Discussions to centralize community conversations—use clear categories, a concise welcome post, and active moderation to improve discoverability and reduce duplicate issues.
</Callout>

## Links and references

* [GitHub Discussions documentation](https://docs.github.com/en/discussions)
* [GitHub: About repository settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/f42f6458-b9ea-4ebb-8cbd-261b2393e622/lesson/65ae9069-e4db-4142-bdfa-e5c480f38e99" />
</CardGroup>
