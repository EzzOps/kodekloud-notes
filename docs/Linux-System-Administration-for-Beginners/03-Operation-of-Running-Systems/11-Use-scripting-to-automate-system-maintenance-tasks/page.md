# Use scripting to automate system maintenance tasks

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/Operation-of-Running-Systems/Use-scripting-to-automate-system-maintenance-tasks/page

Learn to automate system maintenance tasks on CentOS using Bash scripting for backups, archiving, and managing exit statuses.

Automating routine system maintenance on CentOS (or similar Linux distributions) saves time and reduces human error. In this guide, you’ll learn how to:

* Write and run simple Bash scripts
* Archive directories reliably
* Manage multiple backup generations
* Use exit statuses in conditions
* Examine a real-world example (Anacron)

***

## Table of Contents

1. [Understanding the Bash Shell](#understanding-the-bash-shell)
2. [Creating Your First Script](#creating-your-first-script)
3. [Automating Backups](#automating-backups)
   * [Archiving a Directory](#archiving-a-directory)
   * [Keeping Two Generations of Backups](#keeping-two-generations-of-backups)
4. [Using Exit Status in Conditions](#using-exit-status-in-conditions)
5. [Real-World Example: Anacron](#real-world-example-anacron)
6. [Quick Reference: Shell Constructs](#quick-reference-shell-constructs)
7. [Further Resources](#further-resources)

***

## Understanding the Bash Shell

When you log in, you land at a shell prompt managed by **bash**, the Bourne Again SHell. It interprets commands you type or reads and executes commands from a file (a *script*) in sequence.

```bash theme={null}
$ date
Mon Dec  6 16:28:09 CST 2021
```

Bash supports redirection, pipelines, variables, loops, functions, and more—the same features you use interactively are available in scripts.

***

## Creating Your First Script

Follow these steps to build and run a basic maintenance script.

### 1. Create the Script File

```bash theme={null}
$ touch script.sh
$ vim script.sh
```

### 2. Add Script Contents

```bash theme={null}
#!/bin/bash
