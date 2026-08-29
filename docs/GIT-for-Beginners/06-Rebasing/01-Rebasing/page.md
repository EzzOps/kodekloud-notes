# Rebase dc9ad3c..6a6f68b onto 6a6f68b (4 commands)
#
# Commands:
# p, pick <commit> = use commit
# r, reword <commit> = use commit, but edit the commit message
# e, edit <commit> = use commit, but stop for amending
# s, squash <commit> = use commit, but meld into previous commit
# f, fixup <commit> = like "squash", but discard this commit's log message
# x, exec <command> = execute command (the rest of the line) using shell
# b, break = stop here (continue rebase later with 'git rebase --continue')
# d, drop <commit> = remove commit
# l, label <label> = label current HEAD with a name
# r, reset <label> = reset HEAD to a label
# m, merge [-C <commit> | -c <commit> | <label> [# <oneline>]]
#   : <message> (or the oneline, if no original merge commit was
#     specified). Use <commit> to reword the commit message.
```

## Squashing Commits

The essential step in this interactive rebase is defining which commits to squash. In this case, change the commands for the second, third, and fourth commits from `pick` to `squash`. This instructs Git to combine these commits into the first one. Once you update the commands, save the file and exit the editor. Git will then squash the commits, resulting in a single commit that encapsulates all the changes from the selected commits.

> **lightbulb** Interactive rebase is not limited to squashing commits. It also allows you to edit commit messages, reorder commits, or drop commits entirely. These options help you maintain an informative and concise commit history.

## Why Use Interactive Rebasing?

Refining your commit history before merging is crucial for collaboration and future maintenance. By squashing related commits, you make your history easier to understand for team members and maintainers. This practice ultimately enhances the clarity and professionalism of your version control workflow.

Interactive rebasing is a powerful feature for managing your development history, ensuring that when changes finally merge into the main branch, they are both clean and logically organized.

## Additional Resources

For further information on Git and interactive rebasing, check out these resources:

* [Git Documentation](https://git-scm.com/doc)
* [Interactive Rebase Tutorial](https://www.atlassian.com/git/tutorials/rewriting-history)

By mastering interactive rebasing, you'll be better equipped to maintain a clean project history and improve your team's overall workflow.

- [Watch Video](https://learn.kodekloud.com/user/courses/git-for-beginners/module/a6f9b38c-d180-4e22-aabc-786d19f78672/lesson/308bc512-0c77-4c2d-b26b-3186053a703f)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/git-for-beginners/module/a6f9b38c-d180-4e22-aabc-786d19f78672/lesson/8ebeda6d-a4ba-4269-b0ff-130327adf46c)


# Rebasing

Source: https://notes.kodekloud.com/docs/GIT-for-Beginners/Rebasing/Rebasing/page

This article explains the differences between merging and rebasing in Git for incorporating updates from the master branch into a feature branch.

When working on a feature branch, it's essential to incorporate the latest updates from the master branch. There are two common approaches to achieve this: merging and rebasing. Both methods integrate changes from master but differ in how they manage commit history.

## Merging the Master Branch

Merging is a straightforward way to combine the master branch with your feature branch. This method creates a new merge commit that brings in all the changes from master:

```bash theme={null}
(sarah)$ git merge master
```

## Rebasing Branches

Rebasing involves reapplying your feature branch's commits onto the tip of the updated master branch, resulting in a cleaner, linear commit history. Unlike merging, rebasing creates new commit hashes because it rewrites the commit history.

```bash theme={null}
(sarah)$ git rebase master
```

> **lightbulb** Rebasing offers a streamlined history but requires careful coordination when working in a team environment. Ensure that your team is aware of the rewritten commit history to avoid confusion.

## Key Considerations

* Merging preserves the original commit history, including unique commit hash identifiers.
* Rebasing copies commits from one branch to another, which means new commit hashes are generated.
* Collaborating on a branch that has been rebased may require additional communication with team members to prevent integration issues.

## Summary

Rebasing provides an effective method to update your feature branch by placing its commits on top of the latest master branch changes. While this approach creates a cleaner commit history, it alters commit hashes by rewriting history, so proper coordination with your team is critical.

For further guidance on Git workflows, explore our [Git Documentation](https://git-scm.com/doc).

- [Watch Video](https://learn.kodekloud.com/user/courses/git-for-beginners/module/a6f9b38c-d180-4e22-aabc-786d19f78672/lesson/99b73565-87da-40dc-ac43-e2b6f48040b3)
