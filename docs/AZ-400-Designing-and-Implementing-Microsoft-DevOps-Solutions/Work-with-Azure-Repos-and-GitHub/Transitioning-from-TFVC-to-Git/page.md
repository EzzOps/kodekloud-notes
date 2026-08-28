# Transitioning from TFVC to Git

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Work-with-Azure-Repos-and-GitHub/Transitioning-from-TFVC-to-Git/page

Migrating from TFVC to Git enhances workflows, collaboration, and branching strategies through a structured import process and highlights the benefits of adopting Git.

Migrating from Team Foundation Version Control (TFVC) to Git can unlock modern workflows, distributed collaboration, and more flexible branching strategies. In this guide, we’ll walk through a branch-by-branch import, compare migration scopes, and highlight the top benefits of moving your codebase to Git.

## Branch-Level Migration

A phased, branch-level approach lets you validate each import before proceeding, minimizing risk:

1. Select a single TFVC branch to import.
2. Use the Azure DevOps [Git import feature](https://learn.microsoft.com/en-us/azure/devops/repos/import/git-import?view=azure-devops) or a tool like [Git-TFS](https://github.com/git-tfs/git-tfs).

```bash theme={null}
