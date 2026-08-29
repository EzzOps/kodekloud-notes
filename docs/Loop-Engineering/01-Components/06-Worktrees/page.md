# Worktrees

Source: https://notes.kodekloud.com/docs/Loop-Engineering/Components/Worktrees/page

Explains Git worktrees and how to create, list, remove, and prune separate working copies for safe experiments and CI.

When an automated loop or CI job needs to try bold changes, something must keep the main codebase safe. That something is a worktree — a separate working copy where experiments can run without risking the main repository.

What is a worktree?

* A worktree is a separate working copy of the same Git repository.
* Every worktree lives in its own folder with its own checked-out files.
* Worktrees share a single repository history stored in the main `.git` directory.
* Each worktree contains a small `.git` *file* (not a directory) that points back to the shared git data (for example, a `gitdir:` reference into `.git/worktrees/...`).

Because the history is shared, creating a worktree is fast and storage-efficient. Think of a worktree like a scratch copy of a shared document: you can experiment locally without duplicating the entire project history.

<Frame>
  <img alt="The image illustrates the concept of &#x22;Worktrees&#x22; in a Git repository, showing how a main repo with all history can be linked to multiple worktrees, which are fast and project-connected." />
</Frame>

How the original repo and worktree relate

* The original repository (the main folder) stays put and untouched while the worktree is the place for messy or experimental work.
* Changes made inside a worktree do not affect the original until you commit, merge, and push from that worktree.

<Frame>
  <img alt="The image illustrates a concept of &#x22;Worktrees&#x22; with a central source branching into an &#x22;Original&#x22; version that &#x22;Stays put&#x22; and a &#x22;Scratch copy&#x22; for &#x22;Messy work.&#x22;" />
</Frame>

Why use a separate copy?

* Some experiments succeed and some fail. Running experiments directly in the main code risks breaking the primary branch.
* A worktree gives you an isolated place to make large changes, run tests, and iterate, without endangering the main codebase.

<Frame>
  <img alt="The image compares working straight on the main code versus inside a worktree, highlighting the risks of breaking everything versus the safety of the main code." />
</Frame>

Common git worktree operations
Below are the most commonly used `git worktree` commands for creating, listing, removing, and cleaning up worktrees.

|                       Command | Purpose                                                       | Example                                      |
| ----------------------------: | ------------------------------------------------------------- | -------------------------------------------- |
|            `git worktree add` | Create a new worktree and optionally a branch                 | `git worktree add ../try-login -b try-login` |
|           `git worktree list` | Show all registered worktrees                                 | `git worktree list`                          |
|         `git worktree remove` | Remove a worktree (refuses if modified/untracked files exist) | `git worktree remove ../try-login`           |
| `git worktree remove --force` | Force-remove a worktree including changes                     | `git worktree remove --force ../try-login`   |
|          `git worktree prune` | Prune stale worktree entries after manual deletion            | `git worktree prune`                         |

Example workflows

Create a new worktree and branch:

```bash theme={null}
