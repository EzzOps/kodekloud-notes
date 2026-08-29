# Generating a Change Log

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Branching-Strategies-for-Source-Code/Generating-a-Change-Log/page

Learn to automate changelog generation with Git and Azure Pipelines, and publish it directly to your Azure DevOps Wiki.

Maintaining a clear, up-to-date changelog is essential for tracking project history and communicating updates. In this guide, you’ll learn how to automate changelog generation with Git and Azure Pipelines, then publish it directly to your Azure DevOps Wiki.

## 1. Quick Git Log Examples

Start by extracting commit history in chronological order:

```bash theme={null}
git log --pretty=format:"%s" -s --reverse
```

Example output:

```text theme={null}
- Initial Commit
- Adding Wiki
- Set up CI with Azure Pipelines
- Update azure-pipelines.yml for Azure Pipelines
- adding push
- trying git push
- testing build
- changing yml
- changing a few things
- will it work
- Update release notes in wiki folder
```

To include author and relative date, adjust the format string:

```bash theme={null}
git log --pretty=format:"%s - %an, %ar" --reverse
```

Sample entries:

```text theme={null}
Initial Commit - Alice, 2 years ago
Adding Wiki - Bob, 2 years ago
Set up CI with Azure Pipelines - Carol, 1 year ago
...
```

### Git Log Format Options

| Placeholder | Description                               |
| ----------- | ----------------------------------------- |
| %h          | Abbreviated commit hash                   |
| %s          | Commit subject (message)                  |
| %an         | Author name                               |
| %ar         | Author date, relative (e.g. “2 days ago”) |

For a full list of placeholders, see the [Git log documentation](https://git-scm.com/docs/git-log#_pretty_formats).

## 2. Integrating with Azure Pipelines

### 2.1 Generating Release Notes

If you’re already using the **Generate Release Notes** task in your `azure-pipelines.yml`, it might look like this:

```yaml theme={null}
