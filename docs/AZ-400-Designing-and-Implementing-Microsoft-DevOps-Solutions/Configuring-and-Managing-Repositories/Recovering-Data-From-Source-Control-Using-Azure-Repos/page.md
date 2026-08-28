# Using BFG Repo-Cleaner:
bfg --delete-files archive.tar.gz

# Or with Git filter-repo:
git filter-repo --path archive.tar.gz --invert-paths
```

### 2. Removing Sensitive Content

First, list sensitive patterns in `passwords.txt` (one per line):

```text theme={null}
PASSWORD
API_KEY
```

Then run:

```bash theme={null}
# Using BFG Repo-Cleaner:
bfg --replace-text passwords.txt

# Or with Git filter-repo:
git filter-repo --replace-text passwords.txt
```

<Callout icon="triangle-alert">
  Force-pushing rewritten history will overwrite the remote. Coordinate with your team to avoid conflicts.
</Callout>

## Final Steps

After rewriting history, complete these actions:

1. **Force-push the cleaned history**
   ```bash theme={null}
   git push --force
   ```
2. **Notify your team** to reclone or reset their local copies:
   ```bash theme={null}
   git fetch --all
   git reset --hard origin/main
   ```

<Callout icon="lightbulb">
  Ensure everyone is on the same page to prevent divergent histories.
</Callout>

## Links and References

* [Git filter-repo Documentation](https://github.com/newren/git-filter-repo)
* [BFG Repo-Cleaner Homepage](https://rtyley.github.io/bfg-repo-cleaner/)
* [Git Tools – Rewriting History](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-400/module/e7d3282b-80bc-4acd-8009-2fcf5dee0c86/lesson/943bcd6f-88f2-40b8-b367-dd47615b7726" />
</CardGroup>


# Recovering Data From Source Control Using Azure Repos

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Configuring-and-Managing-Repositories/Recovering-Data-From-Source-Control-Using-Azure-Repos/page

This article explains how to recover lost or deleted data using Azure Repos with Git commands and the Azure Repos UI.

When working with Azure Repos, you can leverage the full power of Git along with a rich web interface to recover lost or deleted data. Whether you prefer command-line operations or a GUI, Azure DevOps provides the tools you need.

<Callout icon="lightbulb">
  Ensure you have a local clone of your Azure Repos repository and the latest Git version installed. You will also need sufficient permissions to push changes back to the remote.
</Callout>

## 1. Recovering with Git commands

All standard Git recovery commands work seamlessly with Azure Repos. Here are common scenarios:

| Recovery Task            | Git Command                                   | Description                                                   |
| ------------------------ | --------------------------------------------- | ------------------------------------------------------------- |
| Undo a specific commit   | `git revert <commit>`                         | Creates a new commit that reverses the changes in `<commit>`. |
| Reset working directory  | `git reset --hard HEAD`                       | Discards all uncommitted changes in your working tree.        |
| Recover a deleted branch | `git reflog` → `git branch <branch> <commit>` | Locate the commit in reflog and recreate the branch.          |

Example: Recover a deleted branch named `feature-x`

```bash theme={null}
