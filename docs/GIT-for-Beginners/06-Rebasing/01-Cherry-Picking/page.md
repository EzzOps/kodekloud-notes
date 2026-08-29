# Cherry Picking

Source: https://notes.kodekloud.com/docs/GIT-for-Beginners/Rebasing/Cherry-Picking/page

Cherry-picking is a Git technique to apply a specific commit from one branch to another without merging all changes.

Cherry-picking is a powerful Git technique that allows you to apply a specific commit from one branch onto another without merging all the changes from the source branch. This method is especially useful when you need an isolated change from another branch without incorporating all of its commits.

## When to Use Cherry-Picking

If you're working on the master branch and identify a single commit in a feature branch (for example, the Sarah branch) that introduces a vital fix or enhancement, cherry-picking enables you to import that specific change without merging the entirety of the feature branch.

<Callout icon="lightbulb">
  Before proceeding with cherry-picking, ensure that your target branch is up-to-date and that you understand how the changes from the commit will integrate with your current code base.
</Callout>

## How to Cherry-Pick a Commit

To cherry-pick a commit, you'll use the commit's unique hash value. In the scenario where you wish to apply the changes from a commit on the Sarah branch to your master branch, follow these steps:

1. Switch to your master branch.
2. Execute the cherry-pick command with the hash of the desired commit.

Below is an example command to cherry-pick the commit with the hash `aaba5`:

```bash theme={null}
$ git cherry-pick aaba5
```

After running this command, the changes introduced in that specific commit will be applied to your current branch (master).

<Callout icon="lightbulb">
  Cherry-picking only transfers the changes from the specified commit. Other commits and modifications from the source branch remain separate.
</Callout>

## Summary

Cherry-picking is an essential Git strategy for applying targeted changes across branches. It streamlines the process of integrating critical updates from one branch to another without merging entire branches. For a deeper dive into Git commands and workflows, consider exploring the [official Git documentation](https://git-scm.com/doc).

Happy coding!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/git-for-beginners/module/a6f9b38c-d180-4e22-aabc-786d19f78672/lesson/c4ebb7bc-a8f0-4a13-9285-8ec347c5ac79" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/git-for-beginners/module/a6f9b38c-d180-4e22-aabc-786d19f78672/lesson/f9bf8788-ce67-46b4-ae3a-f22f7387db87" />
</CardGroup>
