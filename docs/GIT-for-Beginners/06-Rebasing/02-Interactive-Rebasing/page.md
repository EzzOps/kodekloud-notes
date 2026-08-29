# Interactive Rebasing

Source: https://notes.kodekloud.com/docs/GIT-for-Beginners/Rebasing/Interactive-Rebasing/page

Interactive rebasing in Git allows modification of commit history, enabling consolidation of related commits into a single, meaningful commit for clearer project history.

Interactive rebasing in Git empowers you to modify your branch’s commit history before merging it into other branches. This process is particularly useful when you want to clean up a feature branch by consolidating several related commits into a single, meaningful commit.

Imagine you have been working on a feature branch and ended up with multiple commits that logically belong together. For example, several commits related to "the second story" could be merged into one commit to maintain a clear commit history. Interactive rebase lets you squash these commits into a single commit, streamlining your branch's history.

## How to Start an Interactive Rebase

To begin, you need to tell Git which commits you want to modify. In this example, we will update the last four commits. Run the following command to open an interactive editor with a list of these commits:

```bash theme={null}
git rebase -i HEAD~4
```

When you execute this command, Git displays a list of the selected commits along with the default command (usually "pick") and a set of instructions. The output may look like this:

```bash theme={null}
pick fb9f191 Added second story
pick aaba5e7 Changes to second story
pick 8ad5d7b Oops more changes to second story
pick 6a6f68b More changes to second story
