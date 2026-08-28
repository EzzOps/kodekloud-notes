# Basics of SCM

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Introduction-and-Basics/Basics-of-SCM/page

This article explains the fundamentals of Source Code Management, its benefits, popular platforms, and basic commands for effective software development collaboration.

Source Code Management (SCM), also known as version control, is the backbone of collaborative software development. Without an SCM, teams face chaotic workflows, untraceable edits, and endless merge conflicts.

<Frame>
  ![The image illustrates the need for Source Code Management Systems (SCMs), showing multiple developers editing a document, with SCMs acting as a central library to track changes over time.](https://kodekloud.com/kk-media/image/upload/v1752870582/notes-assets/images/Certified-Jenkins-Engineer-Basics-of-SCM/source-code-management-developers-diagram.jpg)
</Frame>

## Why Use an SCM?

An SCM system stores every change to your codebase in a central repository, allowing multiple developers to work in parallel. Key benefits include:

| Feature                 | Benefit                                                       |
| ----------------------- | ------------------------------------------------------------- |
| Real-time Collaboration | Developers push and pull changes simultaneously               |
| Code Review             | Comment on pull requests before merging                       |
| Conflict Resolution     | Detect and resolve edit conflicts efficiently                 |
| Secure Sharing          | Grant controlled access to internal and external contributors |
| Full Change History     | Audit decisions and review past code versions                 |
| Rollback Capability     | Revert to stable versions when issues arise                   |

<Frame>
  ![The image is an infographic titled "Source Code Management Systems (SCMs)" highlighting six features: Seamless Collaboration, Code Review, Conflict Resolution, Effortless Sharing, Unveiling the Past, and Rollback Ready.](https://kodekloud.com/kk-media/image/upload/v1752870583/notes-assets/images/Certified-Jenkins-Engineer-Basics-of-SCM/source-code-management-infographic.jpg)
</Frame>

<Callout icon="lightbulb">
  Consistent, descriptive commit messages make it easier to track your project’s evolution over time.\
  Example: `git commit -m "Fix authentication bug in login flow"`
</Callout>

## Popular SCM Platforms

Most modern SCMs are built on Git, a distributed version control system. Below is a comparison of common cloud-based and self-hosted solutions:

| Platform  | Type           | Hosting Model     | URL                                            |
| --------- | -------------- | ----------------- | ---------------------------------------------- |
| GitHub    | Git            | Cloud             | [https://github.com](https://github.com)       |
| GitLab    | Git            | Cloud/Self-hosted | [https://gitlab.com](https://gitlab.com)       |
| Bitbucket | Git, Mercurial | Cloud             | [https://bitbucket.org](https://bitbucket.org) |
| Gitea     | Git            | Self-hosted       | [https://gitea.io](https://gitea.io)           |
| Gogs      | Git            | Self-hosted       | [https://gogs.io](https://gogs.io)             |

## Getting Started

```bash theme={null}
