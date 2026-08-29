# Set default runlevel to 3 (multi-user, console login)
id:3:initdefault:

# System initialization scripts
si::sysinit:/etc/init.d/rcS

# Single-user mode login
~:S:wait:/sbin/sulogin

# Runlevel scripts
l0:0:wait:/etc/init.d/rc 0
l1:1:wait:/etc/init.d/rc 1
l2:2:wait:/etc/init.d/rc 2
l3:3:wait:/etc/init.d/rc 3
l4:4:wait:/etc/init.d/rc 4
l5:5:wait:/etc/init.d/rc 5
l6:6:wait:/etc/init.d/rc 6

# Handle CTRL+ALT+DEL
ca::ctrlaltdel:/sbin/shutdown -r now

# Virtual consoles for runlevels 2 and 3
1:23:respawn:/sbin/getty tty1 VC linux
2:23:respawn:/sbin/getty tty2 VC linux

# Serial console on runlevel 3
S0:3:respawn:/sbin/getty -L 9600 ttyS0 vt320
```

> **lightbulb** After editing `/etc/inittab`, reload init’s configuration without rebooting:

  ```bash theme={null}
  sudo telinit q
  ```

## Init Scripts and Service Directories

Service scripts live in `/etc/init.d/`, while each runlevel directory in `/etc/rc*.d/` contains symlinks:

```bash theme={null}
ls /etc/rc*.d
# rc0.d/  rc1.d/  rc2.d/  rc3.d/  rc4.d/  rc5.d/  rc6.d/
```

Within each `rcN.d` directory, file prefixes determine actions:

| Prefix | Operation                     |
| ------ | ----------------------------- |
| Snn    | Start service when entering N |
| Knn    | Stop service when entering N  |

Example for runlevel 3:

```bash theme={null}
ls /etc/rc3.d
# K01networking  S01apache2  S02ssh  ...
```

## Checking and Changing Runlevels

* Show current and previous runlevels:
  ```bash theme={null}
  runlevel
  # Output: N 3
  ```
* Switch to single-user mode (runlevel 1):
  ```bash theme={null}
  sudo telinit 1
  ```
* Reboot using runlevel 6:
  ```bash theme={null}
  sudo telinit 6
  ```
* Halt using runlevel 0:
  ```bash theme={null}
  sudo telinit 0
  ```

> **triangle-alert** Switching runlevels will start or stop multiple services. Always save your work and notify other users before changing to runlevels 0, 1, or 6.

## Further Reading

* [SysV init Manual](https://man7.org/linux/man-pages/man8/init.8.html)
* [Linux Runlevels Explained](https://wiki.archlinux.org/title/Runlevels)

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/55c2d118-3a85-4da1-8a7f-e9f8671cc818/lesson/79e4cce3-a04c-47ef-b701-ad8f514bc406)


# Change Runlevels Upstart

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/System-Architecture/Change-Runlevels-Upstart/page

Learn to manage system services with Upstart, switch runlevels, and handle shutdowns and reboots using core commands and best practices.

In this lesson, you’ll learn how to manage system services with Upstart, switch runlevels, and handle system shutdowns and reboots. We’ll cover core commands, scheduling techniques, and best practices for both Upstart and systemd environments.

## Controlling Services with Upstart

Upstart job definitions reside in `/etc/init`. You can list all available services and their current states (including PIDs) using `initctl list`:

```bash theme={null}
$ sudo initctl list
avahi-cups-reload            stop/waiting
avahi-daemon                 start/running, process 1123
mountall-net                 stop/waiting
mountnfs-bootclean.sh        start/running
nmbd                         start/running, process 3085
passwd                       stop/waiting
```

> **lightbulb** Upstart jobs live under `/etc/init`. To add or modify a job, create or edit its `.conf` file in this directory.

Use these commands to control services:

| Command        | Action             | Example            |
| -------------- | ------------------ | ------------------ |
| start `<job>`  | Start the service  | `sudo start tty6`  |
| stop `<job>`   | Stop the service   | `sudo stop tty6`   |
| status `<job>` | Show state and PID | `sudo status tty6` |

```bash theme={null}
$ sudo start tty6
$ sudo status tty6
tty6 start/running, process 3282
$ sudo stop tty6
```

### Querying and Switching Runlevels

Although Upstart doesn’t use `/etc/inittab`, you can still use the legacy commands:

```bash theme={null}
$ runlevel        # Display current and previous runlevel
$ sudo telinit 3  # Switch to runlevel 3
```

> Note: Runlevels 0 and 6 correspond to halt and reboot in System V–style init.

## System Shutdown and Reboot

The `shutdown` utility wraps System V runlevel transitions with extra safeguards:

* Broadcasts a warning to all logged-in users
* Blocks new logins during shutdown
* Sends `SIGTERM` then `SIGKILL` to processes
* Transitions to runlevel 0 (halt) or 6 (reboot)

By default, `shutdown` without `-h` or `-r` switches to **single-user mode** (runlevel 1).

### Scheduling a Shutdown

The `<time>` argument is mandatory and accepts:

| Format     | Description           | Example |
| ---------- | --------------------- | ------- |
| `hh:mm`    | Specific 24-hour time | `02:00` |
| `+m`       | Minutes from now      | `+20`   |
| `now`/`+0` | Immediate shutdown    | `now`   |

Optionally include a broadcast message:

```bash theme={null}
$ sudo shutdown 02:00
$ sudo shutdown +20 "System maintenance in 20 minutes"
$ sudo shutdown now "Shutdown initiated"
```

> **triangle-alert** Scheduling or initiating a shutdown requires **root** privileges. Ensure you have the proper permissions before running these commands.

### SysV vs. systemd Commands

On System V–based distributions, `shutdown` handles power actions. On systemd-based systems, use the following equivalents:

| Action    | SysV Command           | systemd Command           |
| --------- | ---------------------- | ------------------------- |
| Reboot    | `sudo shutdown -r now` | `sudo systemctl reboot`   |
| Power off | `sudo shutdown -h now` | `sudo systemctl poweroff` |

For Ctrl+Alt+Delete behavior on SysV, you can limit authorized users in `/etc/shutdown.allow`.

## Broadcasting Messages with `wall`

If you only need to notify users without shutting down:

```bash theme={null}
$ sudo wall "System going into maintenance mode in 5 minutes!"
```

## Links and References

* [Upstart Documentation](https://upstart.ubuntu.com/)
* [systemd Man Pages](https://www.freedesktop.org/software/systemd/man/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/55c2d118-3a85-4da1-8a7f-e9f8671cc818/lesson/b47f3753-a80c-4c38-88de-e628e1b0924a)
