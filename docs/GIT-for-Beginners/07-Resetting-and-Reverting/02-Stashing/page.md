# Stashing

Source: https://notes.kodekloud.com/docs/GIT-for-Beginners/Resetting-and-Reverting/Stashing/page

Learn to use Git stash for temporarily saving changes, allowing quick context switching without committing incomplete work.

In this guide, you'll learn how to use Git stash to temporarily save modifications from your working area. This allows you to switch contexts quickly without committing incomplete work.

Imagine you're working on the third story on the *sarah* branch when a colleague notices a typo in the first story on the *master* branch that needs immediate fixing. Rather than committing your unfinished work, you can quickly stash your changes, leaving a clean working area for the urgent fix.

> **lightbulb** Git stash is especially useful when working with multiple features or hotfixes. It helps maintain a clean working directory while switching between tasks.

## Basic Stashing Commands

To stash all modifications in your working directory, run:

```bash theme={null}
$ git stash
```

This command saves your changes in a stack-like structure, similar to stacking books. When you're ready to continue working on the third story, you can retrieve the most recent stash with:

```bash theme={null}
$ git stash pop
```

As you keep working, you might add more changes to your stash, which will accumulate over time. To view all stored stashes, use:

```bash theme={null}
$ git stash list
```

For example, you might see output like:

```bash theme={null}
stash@{0}: WIP on sarah: f4e8304 Added third story
stash@{1}: WIP on sarah: s53fwe4 Added fourth story
stash@{2}: WIP on sarah: k4e5432 Added fifth story
```

## Inspecting and Restoring Specific Stashes

If you want to inspect the contents of a specific stash, use the `git stash show` command followed by the stash identifier:

```bash theme={null}
$ git stash show stash@{1}
fourth_story.md | 1 +
1 file changed, 1 addition(+)
```

To restore a specific stash instead of the most recent one, simply specify its identifier with the `pop` command:

```bash theme={null}
$ git stash pop stash@{1}
Dropped stash@{1} (2cfe…)
```

> **triangle-alert** Always verify your current branch before applying a stash to avoid merging changes into the wrong context.

## Conclusion

This guide has provided an overview of how to use Git stash to manage your work-in-progress changes. Practice these commands regularly to gain confidence and streamline your Git workflow.

For more information on Git and version control best practices, check out the [Git Documentation](https://git-scm.com/doc).

- [Watch Video](https://learn.kodekloud.com/user/courses/git-for-beginners/module/6d339cba-e512-4329-a340-dccbb0454385/lesson/ba1e0661-e910-42d7-9b01-b7ec43cb83bb)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/git-for-beginners/module/6d339cba-e512-4329-a340-dccbb0454385/lesson/45ba4652-f090-46df-826f-787a596d2fd9)
