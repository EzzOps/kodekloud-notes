# Create a new branch named 'sarah'
$ git branch sarah

# Switch to an existing branch called 'sarah'
$ git checkout sarah

# Create a new branch named 'max' and switch to it immediately
$ git checkout -b max
```

The `git checkout -b` command is a shorthand that creates and switches to a new branch with one step. To delete a branch, you can use:

```bash theme={null}
$ git branch -d <branch_name>
```

And to list all branches in your repository:

```bash theme={null}
$ git branch
```

## Understanding HEAD in Git

In Git, HEAD is a reference to your current location in the repository. It always points to the latest commit on the branch you are working on. Changing branches moves the HEAD pointer to the tip of the target branch:

```bash theme={null}
$ git checkout master
```

> **lightbulb** The HEAD pointer is crucial for tracking the state of your work. Understanding how HEAD moves during commits and branch switches helps you navigate the repository more effectively.

- [Watch Video](https://learn.kodekloud.com/user/courses/git-for-beginners/module/f1029b40-9a1e-4ccc-bca9-46b9d8945ab7/lesson/b8fc40dc-f319-45a0-a0be-463e9f21281e)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/git-for-beginners/module/f1029b40-9a1e-4ccc-bca9-46b9d8945ab7/lesson/39af44d8-a989-4895-87cc-483d88da4be2)


# Cloning remote repositories

Source: https://notes.kodekloud.com/docs/GIT-for-Beginners/Initialize-Remote-Repositories/Cloning-remote-repositories/page

This article explains how to clone remote repositories using Git, focusing on obtaining a local copy from GitHub.

When a new team member joins a project, providing access to the remote repository is essential. Cloning the repository using Git is the standard method to obtain a complete local copy of your project data.

## How to Clone a Repository

To clone a repository, use the Git clone command followed by the SSH link of the remote repository. Below is the generic command format:

```bash theme={null}
$ git clone [ssh link]
```

For this guide, we focus on cloning a repository from GitHub.

> **lightbulb** When you visit a repository on GitHub, locate the prominent green "Clone" button. Clicking it reveals a flyout that contains the SSH link required for cloning.

After obtaining the SSH link, clone the repository locally by running:

```bash theme={null}
$ git clone git@github.com:account/remote-repo.git
Cloning into 'remote-repo'...
remote: Enumerating objects: 59, done.
remote: Counting objects: 100% (59/59), done.
remote: Compressing objects: 100% (43/43), done.
remote: Total 2948 (delta 28), reused 18 (delta 6)
Receiving objects: 100% (2948/2948), 1.93 MiB | 2.53 MiB/s, done.
Resolving deltas: 100% (1526/1526), done.
```

By default, Git creates a local folder with the same name as the remote repository.

## Navigating the Cloned Repository

After cloning, switch to the newly created repository directory with the following command:

```bash theme={null}
$ cd remote-repo
```

To review the complete history of the repository, use the git log command. This command displays all commits, allowing you to understand the project's evolution:

```bash theme={null}
$ git log
commit 67c833e3...ecb7df62f (HEAD -> origin/master)
Author: John Doe <john@doe>
Date:   Sun Jun 14 14:45:07 2020 -0700

    Added first story
```

> **lightbulb** The `git log` command is a useful tool not only for tracing the project history but also for identifying important changes made by your team.

With a cloned repository, you can now work locally and interact with the remote repository for seamless team collaboration.

For more information on Git commands and efficient project collaboration, visit the [Git Documentation](https://git-scm.com/docs).

- [Watch Video](https://learn.kodekloud.com/user/courses/git-for-beginners/module/299037d1-d4d5-4d22-8eb3-b8fc6af3f8d2/lesson/ccf54d0a-57ff-4001-a710-d4129f1708c7)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/git-for-beginners/module/299037d1-d4d5-4d22-8eb3-b8fc6af3f8d2/lesson/98603f2e-51a0-4029-bea4-5f53c7a1cd42)
