# .  ..  .bash_logout  .bash_profile  .bashrc  README
```

Confirm the contents:

```bash theme={null}
cat /home/trinity/README
# Please don’t run CPU-intensive processes between 8 am and 10 pm.
```

## 3. Setting Up a Custom `PATH` for One User

If **trinity** needs access to tools in `/opt/bin`, prepend that directory to her `PATH`. Edit her `.bashrc`:

```bash theme={null}
sudo vim /home/trinity/.bashrc
```

Add or modify the `PATH` line:

```bash theme={null}
PATH="$HOME/.local/bin:$HOME/bin:/opt/bin:$PATH"
```

Save and exit. For immediate effect, have Trinity run:

```bash theme={null}
source ~/.bashrc
echo $PATH
# /home/trinity/.local/bin:/home/trinity/bin:/opt/bin:/usr/local/bin:/usr/bin:...
specialtool  # runs /opt/bin/specialtool
```

<Callout icon="lightbulb">
  Always ensure each entry is separated by a colon (`:`) and that `$PATH` remains at the end.
</Callout>

## 4. Customizing the Default `.bashrc` for All New Users

To apply the same `PATH` change (or any other environment tweaks) site-wide, modify the skeleton `.bashrc`:

```bash theme={null}
sudo vim /etc/skel/.bashrc
```

Insert your custom lines—such as the `PATH` definition—then save. Now, every new account created on this system will inherit these settings automatically.

<Callout icon="triangle-alert">
  Be careful when editing `/etc/skel/.bashrc`. Errors in this file may prevent newly created users from logging in correctly.
</Callout>

***

Now you’re ready to manage default user environments using `/etc/skel`. Practice by adding more config files or policies to streamline onboarding for every new account!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/2490f961-886c-4531-be8c-915cccff60a9/lesson/6b11f23a-a1bc-412e-b7c3-74020bc89bea" />
</CardGroup>


# Work on the Command Line Part 2 Modify shell environment and variables

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/GNU-and-Unix-Commands/Work-on-the-Command-Line-Part-2-Modify-shell-environment-and-variables/page

Learn to view, customize, and persist environment variables on Linux, covering session tweaks, system settings, and automating tasks at login.

In this lesson, you’ll learn how to view, customize, and persist environment variables on Linux. We cover session-level tweaks, system-wide settings, and automating tasks at login.

## What Are Environment Variables?

Environment variables are key–value pairs that your shell and applications use to determine behavior, file locations, and settings. You can list all of them with either:

```bash theme={null}
printenv
env
```

Example output:

```bash theme={null}
$ env
PATH=/home/aaron/.local/bin:/home/aaron/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin
HISTSIZE=1000
GJS_DEBUG_TOPICS=JS ERROR;JS LOG
SESSION_MANAGER=local/unix:@/tmp/.ICE-unix/2260,unix/unix:/tmp/.ICE-unix/2260
```

### Modifying Bash History Size

By default, `HISTSIZE=1000` limits your Bash history to 1 000 commands. To increase it for the current session:

```bash theme={null}
export HISTSIZE=2000
```

Verify:

```bash theme={null}
history
```

Sample:

```bash theme={null}
    1  sudo nano -w /etc/hosts
    2  ssh student@192.168.0.18
    3  ssh student@LFCS-CentOS2
    4  ls
    5  ls -laF
    6  cd .ssh
    7  ls
    8  nano -w known_hosts
    9  exit
   10  rm .ssh/known_hosts
```

## Common Environment Variables

Here are a few variables you’ll encounter frequently:

| Variable | Description                    | Example Usage    |
| -------- | ------------------------------ | ---------------- |
| HOME     | Current user’s home directory  | `echo $HOME`     |
| PWD      | Current working directory      | `echo $PWD`      |
| PATH     | Directories to search commands | `echo $PATH`     |
| HISTSIZE | Max number of history entries  | `echo $HISTSIZE` |

To display a variable’s value:

```bash theme={null}
echo $HOME
