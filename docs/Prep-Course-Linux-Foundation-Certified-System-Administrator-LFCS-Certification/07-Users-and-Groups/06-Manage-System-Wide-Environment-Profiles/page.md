# Manage System Wide Environment Profiles

Source: https://notes.kodekloud.com/docs/Prep-Course-Linux-Foundation-Certified-System-Administrator-LFCS-Certification/Users-and-Groups/Manage-System-Wide-Environment-Profiles/page

Learn to manage system-wide environment profiles on Linux, including environment variables, command line usage, and applying changes locally and system-wide.

In this article, you'll learn how to manage system-wide environment profiles on Linux. We will explore the role of environment variables, how to use them on the command line and in scripts, and how to apply changes both locally and system-wide.

## Understanding Environment Variables

An environment variable is a dynamic value stored in your shell that can affect how running processes behave. For example, the environment variable `HISTSIZE` (as seen below) controls the maximum number of commands Bash will remember in its history.

To display your current user's environment variables, run:

```bash theme={null}
$ printenv  # equivalent to: $ env
PATH=/home/aaron/.local/bin:/home/aaron/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin
HISTSIZE=1000
GJS_DEBUG_TOPICS=JS ERROR;JS LOG
SESSION_MANAGER=local/unix:@/tmp/.ICE-unix/2260,unix/unix:/tmp/.ICE-unix/2260
```

## Using Environment Variables on the Command Line

Environment variables can be referenced directly in commands. Many applications use the `HOME` variable to locate a user's home directory. You can verify this usage with the following commands:

```bash theme={null}
$ printenv
PWD=/home/aaron
SSH_ASKPASS=/usr/libexec/openssh/gnome-ssh-askpass
HOME=/home/aaron

$ echo $HOME
/home/aaron
```

When you prefix a variable with the dollar sign (`$`), the shell substitutes it with its current value. This feature is particularly beneficial for scripting.

## Dynamically Incorporating Environment Variables in Scripts

Environment variables allow scripts to adapt to the user running them. For instance, when saving a file to the user's home directory, using `$HOME` ensures the path is correctly set without hardcoding it. Consider this example:

```bash theme={null}
$ printenv
PWD=/home/aaron
SSH_ASKPASS=/usr/libexec/openssh/gnome-ssh-askpass
HOME=/home/aaron

$ echo $HOME
/home/aaron

$ touch $HOME/saved_file  # equivalent to: $ touch /home/aaron/saved_file
$ touch /home/jane/saved_file
```

If Aaron runs the script, it will create `/home/aaron/saved_file`; if Jane runs it, her file will be created in `/home/jane/saved_file`. This dynamic adjustment is one of the key benefits of using environment variables.

> **lightbulb** If you want users to maintain personalized environment variables, you can modify their `.bashrc` file. However, for system-wide settings that affect all users, update the `/etc/environment` file.

## Configuring Environment Variables

To set a personal environment variable, you can modify your `.bashrc` file. For system-wide changes that affect all users, edit the configuration file located at `/etc/environment`.

First, inspect your `.bashrc` file:

```bash theme={null}
$ cat .bashrc
