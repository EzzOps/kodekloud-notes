# Step 1: Identify the lost branch reference
git reflog

# Step 2: Recreate the branch at the desired commit (e.g., abc1234)
git branch feature-x abc1234

# Step 3: Push the restored branch to Azure Repos
git push origin feature-x
```

> **triangle-alert** Avoid using `git push --force` on shared branches—it can overwrite history and disrupt other collaborators. Use `--force-with-lease` when you need safer history rewrites.

## 2. Restoring deleted branches in the Azure Repos UI

If you prefer a visual approach, Azure Repos provides a point-and-click interface to restore branches:

1. In Azure DevOps, navigate to **Repos** > **Branches**.
2. Toggle **Show deleted branches** in the filter bar.
3. Search for the branch name (e.g., `dev`).
4. Click **Restore** next to the deleted branch.

![The image shows a screenshot of Azure Repos with a section for recovering deleted branches, highlighting a deleted "dev" branch. It includes a note about restoring branches by searching for their names.](https://kodekloud.com/kk-media/image/upload/v1752867524/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Recovering-Data-From-Source-Control-Using-Azure-Repos/azure-repos-recover-deleted-branches.jpg)

No matter which method you choose—Git CLI or Azure Repos UI—you can quickly recover commits, branches, and deleted data with confidence.

Next, we’ll explore how to purge sensitive or unwanted data from your source control to meet security and compliance requirements.

## References

* [Azure Repos Documentation](https://docs.microsoft.com/azure/devops/repos/git/)
* [Git Documentation: git-revert](https://git-scm.com/docs/git-revert)
* [Git Documentation: git-reflog](https://git-scm.com/docs/git-reflog)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-400/module/e7d3282b-80bc-4acd-8009-2fcf5dee0c86/lesson/292b1f1a-798c-48a0-b88f-7ac180999a4f)


# Recovering Data by Using Git Commands

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Configuring-and-Managing-Repositories/Recovering-Data-by-Using-Git-Commands/page

This guide explains how to recover lost Git data using reflog and various Git commands.

Git’s built-in history tracking and reflog functionality serve as a powerful “time machine” for your repository. In this guide, you’ll learn how to:

* Restore deleted commits
* Undo recent commits
* Recover deleted branches

These techniques help you safely navigate and recover from mistakes in your Git workflow.

## 1. Restoring a Deleted Commit

When a commit disappears (e.g., via a force-push or a branch deletion), Git’s reflog can track its SHA-1 hash.

```bash theme={null}
git reflog
```

This displays a chronological list of all `HEAD` movements. Locate the desired commit hash in the reflog output.

```bash theme={null}
git checkout <commit-hash>
```

You’re now in a “detached HEAD” state. To preserve this commit on a branch:

```bash theme={null}
git checkout -b restore-branch <commit-hash>
```

This creates a new branch named `restore-branch` pointing at the recovered commit.

> **lightbulb** By default, Git keeps reflog entries for 90 days. If you don’t find your commit, it may have been pruned. Configure retention with [`gc.reflogExpire`](https://git-scm.com/docs/git-config#Documentation/git-config.txt-gcreflogExpire).

## 2. Undoing the Last Commit

If you simply want to undo the very last commit on your current branch, use `git reset`. Choose between a **soft** or **hard** reset based on whether you need to preserve your worktree and index.

| Reset Type | Description                                      | Command                   |
| ---------- | ------------------------------------------------ | ------------------------- |
| Soft       | Undo commit, keep changes staged                 | `git reset --soft HEAD~1` |
| Mixed      | Undo commit, unstage changes (default behavior)  | `git reset HEAD~1`        |
| Hard       | Undo commit and discard staged & working changes | `git reset --hard HEAD~1` |

### 2.1 Soft Reset

```bash theme={null}
git reset --soft HEAD~1
```

* Moves the branch pointer back by one commit.
* Leaves your working directory and index untouched.

### 2.2 Hard Reset

```bash theme={null}
git reset --hard HEAD~1
```

* Moves the branch pointer back by one commit.
* Resets both your index and working directory to the new `HEAD`.

> **triangle-alert** `git reset --hard` irreversibly discards all uncommitted changes. Make sure you really want to lose those changes.

For more on reset modes, see [Git Reset Documentation](https://git-scm.com/docs/git-reset).

## 3. Recovering a Deleted Branch

Accidentally deleted a branch? You can bring it back if its commits still exist in the reflog.

1. View the reflog:

   ```bash theme={null}
   git reflog
   ```

2. Find the commit hash where your branch last pointed.

3. Recreate the branch:

   ```bash theme={null}
   git checkout -b <branch-name> <commit-hash>
   ```

Your deleted branch is now restored, complete with its history.

***

## Links and References

* [Git Reflog](https://git-scm.com/docs/git-reflog)
* [Git Checkout](https://git-scm.com/docs/git-checkout)
* [Git Reset](https://git-scm.com/docs/git-reset)
* [Git Configuration](https://git-scm.com/docs/git-config)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-400/module/e7d3282b-80bc-4acd-8009-2fcf5dee0c86/lesson/a2a881b2-be7c-4537-8387-a94c9d93be60)
