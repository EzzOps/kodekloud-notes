# List all environment variables
$ env
PATH=/home/aaron/.local/bin:/home/aaron/bin:/usr/local/bin:/usr/bin
HISTSIZE=1000
GJS_DEBUG_TOPICS=JS ERROR;JS LOG
SESSION_MANAGER=local/unix:@tmp/.ICE-unix/2260

# Show HOME directory
$ printenv HOME
/home/aaron
```

To modify a variable for your current session, simply reassign it:

```bash theme={null}
# Increase Bash history size for this session
$ HISTSIZE=2000
$ echo $HISTSIZE
2000
```

You can reference variables in scripts. For example, create a file in each user’s home directory:

```bash theme={null}
$ touch "$HOME/saved_file"
```

This ensures the file lands in the right directory regardless of username.

## Setting System-Wide Environment Variables

While individual users often tweak `~/.bashrc`, you can enforce variables globally by editing `/etc/environment`:

```bash theme={null}
$ sudo vim /etc/environment
```

Append lines in the format `KEY="value"`:

```text theme={null}
KodeKloud="https://www.kodekloud.com"
```

Save and log out, then back in to apply changes:

```bash theme={null}
$ echo $KodeKloud
https://www.kodekloud.com
```

<Callout icon="lightbulb">
  The file `/etc/environment` only supports simple `KEY="value"` assignments. You cannot use shell expansions or commands here.
</Callout>

## Running Commands at Login

To execute scripts for every user at login, place them in `/etc/profile.d/`. For example, to record the last login timestamp:

```bash theme={null}
$ sudo vim /etc/profile.d/lastlogin.sh
```

Add:

```bash theme={null}
# Log the last login time into a file in the user’s home
echo "Your last login was at:" > "$HOME/lastlogin"
date                       >> "$HOME/lastlogin"
```

Scripts in `/etc/profile.d/` are sourced by login shells automatically—you do **not** need a shebang (`#!/bin/bash`).

```bash theme={null}
# After logging out and back in
$ cat $HOME/lastlogin
Your last login was at: Thursday DEC 16 11:19:27 CDT 2021
```

<Callout icon="triangle-alert">
  Avoid syntax errors in `/etc/profile.d/` scripts. A malformed script can prevent users from logging in properly.
</Callout>

## Further Reading & References

* [Bash Manual: Environment](https://www.gnu.org/software/bash/manual/html_node/Environment.html)
* [Linux `env` Command](https://linux.die.net/man/1/env)
* [Filesystem Hierarchy Standard: /etc](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/ch03s14.html)

***

In the next article, we’ll explore advanced shell initialization techniques, including per-shell configuration and custom prompts.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/7e2b6f48-e58c-4d05-82e2-feb0f5f876f5/lesson/05b7aa04-573d-4d14-8b9a-734e5c15ecef" />
</CardGroup>


# Manage template user environment

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/User-and-Group-Management/Manage-template-user-environment/page

The article explains how to manage default user environments in Linux using the `/etc/skel` directory for configuration files and welcome messages.

The skeleton directory `/etc/skel` provides the blueprint for every new user account on a Linux system. By placing files here, you ensure they are automatically copied into each new home directory—ideal for default configuration files, welcome notices, or policy reminders.

## Add a Custom Welcome Notice

To display a standard reminder or welcome message for all new users, create a file in `/etc/skel`:

```bash theme={null}
sudo vim /etc/skel/README
```

Insert your message, for example:

```text theme={null}
Please don’t run CPU-intensive processes between 8 AM and 10 PM.
```

Save and exit.

<Callout icon="lightbulb">
  Files placed in `/etc/skel` are automatically replicated to every new user's home directory. Use this to distribute common configurations or reminders.
</Callout>

## Verify Replication with a New User

Create a test user (e.g., `trinity`) to confirm the welcome notice appears:

```bash theme={null}
sudo adduser trinity
```

List all files, including hidden ones:

```bash theme={null}
ls -a /home/trinity
```

Expected output:

```bash theme={null}
.               .bash_logout  .profile
..              .bashrc       README
```

Display the notice:

```bash theme={null}
cat /home/trinity/README
```

## Customize the PATH for an Individual User

If a specific user needs a custom directory like `/opt/bin` in their `PATH`, update their `~/.bashrc`:

```bash theme={null}
sudo vim /home/trinity/.bashrc
```

Find the existing `PATH` line and prepend your directory:

```bash theme={null}
PATH="$HOME/.local/bin:$HOME/bin:/opt/bin:$PATH"
```

Save and close. When the user opens a new shell session, `/opt/bin` will be included:

```bash theme={null}
echo $PATH
```

Example:

```bash theme={null}
/home/trinity/.local/bin:/home/trinity/bin:/opt/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
```

Now `specialtool` in `/opt/bin` runs directly:

```bash theme={null}
specialtool
```

## Apply Default PATH Changes for All New Users

To make the custom `PATH` part of every future account, modify the skeleton `.bashrc`:

```bash theme={null}
sudo vim /etc/skel/.bashrc
```

Add your directory:

```bash theme={null}
PATH="$HOME/.local/bin:$HOME/bin:/opt/bin:$PATH"
```

Every user created after this change inherits the updated `PATH` automatically.

<Callout icon="triangle-alert">
  Be cautious when editing system-wide skeleton files. Incorrect settings in `/etc/skel` may affect all new user environments.
</Callout>

## Common Files in /etc/skel

| Filename      | Purpose                           |
| ------------- | --------------------------------- |
| .bashrc       | Interactive shell configuration   |
| .profile      | Login shell environment variables |
| .bash\_logout | Commands to run at logout         |
| README        | Custom welcome or policy messages |

***

## References

* [man skel - Linux manual](https://man7.org/linux/man-pages/man5/skel.5.html)
* [adduser command](https://linux.die.net/man/8/adduser)
* [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/7e2b6f48-e58c-4d05-82e2-feb0f5f876f5/lesson/29581ccd-25ee-4d70-b802-cc1ece802392" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/7e2b6f48-e58c-4d05-82e2-feb0f5f876f5/lesson/fa4bc4e7-76bb-4161-9a55-7803ed67fd89" />
</CardGroup>
