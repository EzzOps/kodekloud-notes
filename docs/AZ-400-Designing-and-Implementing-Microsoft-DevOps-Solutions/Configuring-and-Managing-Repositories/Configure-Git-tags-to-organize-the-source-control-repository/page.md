# Configure Git tags to organize the source control repository

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Configuring-and-Managing-Repositories/Configure-Git-tags-to-organize-the-source-control-repository/page

This article explains how to configure Git tags for organizing source control repositories and managing version releases effectively.

Git tags serve as fixed points—or landmarks—in your commit history, helping you mark version releases and other significant milestones. By leveraging tags, you can easily reference builds, rollback to stable states, and integrate seamlessly with CI/CD pipelines in Azure Repos or any Git-based workflow.

<Frame>
  ![The image explains the role of Git tags, showing them as landmarks for important commits, typically used for version releases or highlighting significant changes. It includes a visual with a Git logo and version numbers V01 to V04.](https://kodekloud.com/kk-media/image/upload/v1752867508/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Configure-Git-tags-to-organize-the-source-control-repository/git-tags-role-version-landmarks-diagram.jpg)
</Frame>

## Why use Git tags?

* Create immutable release points for reproducibility
* Simplify collaboration by referencing a specific state of the code
* Automate deployments by targeting a tag in your pipeline

## Types of Git tags

| Tag Type    | Description                                    | Typical Use Case          |
| ----------- | ---------------------------------------------- | ------------------------- |
| Lightweight | A simple ref to a commit                       | Quick local markers       |
| Annotated   | A full Git object (message, author, timestamp) | Official release versions |

<Callout icon="lightbulb">
  Annotated tags include metadata—such as the tagger’s name, date, and a descriptive message—making them ideal for public releases.
</Callout>

## Creating tags

```bash theme={null}
