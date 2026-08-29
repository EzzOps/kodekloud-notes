# systemctl reboot
```

```bash theme={null}
$ sudo systemctl reboot
[sudo] password for aaron:
```

### Power Off (Shutdown)

```bash theme={null}
# systemctl poweroff
```

```bash theme={null}
$ sudo systemctl poweroff
[sudo] password for aaron:
```

For more options, refer to the official [systemctl documentation](https://www.freedesktop.org/software/systemd/man/systemctl.html).

***

## 2. Forcing a Reboot or Shutdown

If your system is hung or won’t shut down cleanly, you can force the operation. Use these commands sparingly—they bypass the normal shutdown sequence and risk data loss.

> **triangle-alert** Forced shutdowns do not allow applications to close gracefully. Always try a standard reboot first.

| Severity        | Command                                                                                |
| --------------- | -------------------------------------------------------------------------------------- |
| Single force    | `sudo systemctl reboot --force`<br />`sudo systemctl poweroff --force`                 |
| Immediate reset | `sudo systemctl reboot --force --force`<br />`sudo systemctl poweroff --force --force` |

***

## 3. Scheduling with shutdown

The `shutdown` utility lets you schedule a shutdown or reboot and broadcast a warning message to all users.

| Task                       | Command Syntax                     |
| -------------------------- | ---------------------------------- |
| Shutdown at specific time  | `sudo shutdown HH:MM`              |
| Shutdown after a delay     | `sudo shutdown +<minutes>`         |
| Reboot instead of shutdown | Add `-r`: `sudo shutdown -r HH:MM` |
| Reboot after a delay       | `sudo shutdown -r +<minutes>`      |

### Schedule by Clock Time

```bash theme={null}
$ sudo shutdown 02:00
```

(Times use 24-hour format, e.g., `0000`–`2359`.)

### Schedule by Delay

```bash theme={null}
$ sudo shutdown +15
```

(The system will shut down in 15 minutes.)

### Reboot with shutdown

```bash theme={null}
$ sudo shutdown -r 02:00
$ sudo shutdown -r +15
```

***

## 4. Notifying Logged-In Users

To give users advance notice, append a quoted message at the end of the `shutdown` command:

```bash theme={null}
$ sudo shutdown -r +5 'System maintenance: scheduled reboot in 5 minutes'
```

This message appears on all connected terminals, allowing users to save work before the system goes down.

***

## References and Further Reading

* [systemctl Manual](https://www.freedesktop.org/software/systemd/man/systemctl.html)
* [shutdown(8) Manual](https://man7.org/linux/man-pages/man8/shutdown.8.html)
* [Linux System Administration Basics](https://linuxhandbook.com/learn-linux/)

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/ca5e9d7c-9dac-4ecc-9e21-dafef5ef2641/lesson/cfb03e11-b5b6-46a5-a71d-04714a0435c6)


# Diagnose and manage processes

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/Operation-of-Running-Systems/Diagnose-and-manage-processes/page

This article explains how to diagnose and manage processes in Linux for effective system administration.

When you start any application, Linux creates a *process* that runs until completion or termination. Understanding how to monitor and control these processes is essential for effective system administration and performance tuning.

## Short-Lived vs. Long-Lived Processes

### Short-Lived Processes

Commands like `ls` spawn a process that exits immediately after running:

```bash theme={null}
$ ls
absolute_picture_shortcut  all_output.txt        archive.zip
archive.tar               Desktop               Documents
…  
$  # Process ends when directory listing is complete
```

### Long-Lived Processes

Daemons such as `sshd` or long-running services remain active until explicitly stopped. To inspect active processes, the `ps` command is your first stop.

***

## Inspecting Processes with `ps`

`ps` provides a snapshot of processes. It supports two option syntaxes:

| Syntax Style | Example  | Description                           |
| ------------ | -------- | ------------------------------------- |
| Unix (POSIX) | `ps -e`  | Standard options prefixed with a dash |
| BSD          | `ps axu` | Options without a dash                |

> **lightbulb** Use `man ps` to explore all options and compare Unix vs. BSD syntax.

### Common `ps` Usage

* Show processes in the current terminal:

  ```bash theme={null}
  $ ps
    PID TTY          TIME CMD
   7726 pts/0    00:00:00 bash
   7796 pts/0    00:00:00 ps
  ```

* List **all** system processes in user-oriented format:

  ```bash theme={null}
  $ ps aux
  USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
  root         1  0.0  0.3 241296  14000 ?        Ss   Mar23   0:01 /usr/lib/systemd/systemd
  aaron    7726  0.0  0.4 3142460 185096 pts/0   S+   10:00   0:00 gnome-system-monitor
  …
  ```

The mnemonic **aux** (a: all with terminal, u: user format, x: include daemons) helps recall this combination.

![The image shows a terminal window displaying the manual page for the ps command, which reports a snapshot of current processes. It includes sections like NAME, SYNOPSIS, and DESCRIPTION.](https://kodekloud.com/kk-media/image/upload/v1752881489/notes-assets/images/Linux-System-Administration-for-Beginners-Diagnose-and-manage-processes/ps-command-manual-terminal-snapshot.jpg)

Excerpt from `man ps`:

```text theme={null}
To see every process on the system using standard syntax:
  ps -e
  ps -ef

Using BSD syntax:
  ps ax
  ps axu

To print a process tree:
  ps -ejH
  ps axjf
```

***

## Real-Time Monitoring with `top`

For continuous updates:

```bash theme={null}
$ top
top - 10:15:03 up 1 day,  2:34,  1 user,  load average: 0.05, 0.03, 0.01
Tasks: 236 total,   1 running, 235 sleeping
%Cpu(s):  1.2 us,  0.5 sy, 98.3 id
MiB Mem :  3731.4 total, 1588.9 free,  915.5 used, 1227.0 buff/cache

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
 6601 aaron    20   0 3142460 185096 104268 S   6.2  4.8   0:06.60 gnome-shell
 1    root     20   0  241296  14000   8912 S   0.0  0.4   0:01.26 systemd
…
```

* Use Up/Down arrows or `Page Up`/`Page Down` to scroll.
* Press `q` to exit.

***

## Filtering Processes

| Filter Type | Command Example                        |
| ----------- | -------------------------------------- |
| By PID      | `ps -p 1 -o pid,tty,stat,time,command` |
| By User     | `ps -U aaron -u`                       |
| By Name     | `pgrep -a syslog`                      |

```bash theme={null}
$ pgrep -a syslog
1455 /usr/sbin/rsyslogd -n
```

***

## Adjusting Niceness (Priority)

Process priority (`nice` value) ranges from **–20** (highest) to **+19** (lowest).

* Launch with niceness 11:

  ```bash theme={null}
  $ nice -n 11 bash
  ```

* View niceness:

  ```bash theme={null}
  $ ps -l
  F   UID   PID  PPID PRI  NI VSZ   RSS STAT TTY      TIME COMMAND
  0  1000  6543  6540  20  11 658840 19268 S+   tty2     0:00 bash
  ```

* Change niceness of an existing PID:

  ```bash theme={null}
  $ sudo renice 7 6543
  6543 (process ID) old priority 11, new priority 7
  ```

***

## Parent/Child Process Trees

Display processes as a hierarchy:

```bash theme={null}
$ ps faxu
```

![The image shows a terminal window displaying a list of running processes on a CentOS system, including details like user, PID, CPU and memory usage, and command paths.](https://kodekloud.com/kk-media/image/upload/v1752881490/notes-assets/images/Linux-System-Administration-for-Beginners-Diagnose-and-manage-processes/centos-terminal-running-processes-list.jpg)

***

## Sending Signals

Linux signals control process behavior. Common signals include:

| Signal  | Number | Default Action         |
| ------- | ------ | ---------------------- |
| SIGHUP  | 1      | Hangup (reload config) |
| SIGINT  | 2      | Interrupt              |
| SIGTERM | 15     | Graceful termination   |
| SIGKILL | 9      | Force kill             |
| SIGSTOP | 19     | Pause                  |
| SIGCONT | 18     | Continue               |

List all signals:

```bash theme={null}
$ kill -l
 1) SIGHUP  2) SIGINT  3) SIGQUIT  9) SIGKILL
15) SIGTERM 18) SIGCONT 19) SIGSTOP
```

Examples:

```bash theme={null}
