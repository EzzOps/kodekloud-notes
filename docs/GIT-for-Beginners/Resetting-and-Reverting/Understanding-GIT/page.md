# Understanding GIT

Source: https://notes.kodekloud.com/docs/GIT-for-Beginners/Resetting-and-Reverting/Understanding-GIT/page

This article explains Gits internal mechanisms, focusing on its key-value store model, command types, and object types for effective version control.

In this lesson, we dive into Git's internal mechanisms, explaining how Git uses a key-value store model to manage files. Each file added to a commit is hashed using the SHA-1 algorithm, and the resulting hash uniquely identifies the folder where the file's contents are stored.

Git commands are divided into two main categories:

* **Porcelain Commands:** These are user-friendly commands such as `git add`, `git status`, `git commit`, and `git stash`.
* **Plumbing Commands:** These commands, including `git hash-object` and `git cat-file`, allow you to interact directly with Git's internal data structures.

Below is an overview of these commands:

```text theme={null}
