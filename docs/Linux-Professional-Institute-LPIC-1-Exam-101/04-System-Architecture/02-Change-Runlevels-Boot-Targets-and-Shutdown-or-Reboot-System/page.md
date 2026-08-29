# Change Runlevels Boot Targets and Shutdown or Reboot System

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/System-Architecture/Change-Runlevels-Boot-Targets-and-Shutdown-or-Reboot-System/page

This article explains managing runlevels, configuring boot targets, and performing system shutdown or reboot in Linux administration.

In this lesson, we’ll cover how to manage runlevels with SysV init, configure boot targets, and perform system shutdown or reboot. Controlling which services start or stop is essential for Linux administration—whether you’re running web servers, mail daemons, or network services.

## SysV init and Runlevels

On SysV-based systems, `/sbin/init` (PID 1) manages services through predefined runlevels (0–6). Each runlevel corresponds to a different system state:

| Runlevel | Description                                          |
| -------- | ---------------------------------------------------- |
| 0        | Halt (shutdown)                                      |
| 1, S     | Single-user mode (no networking), maintenance        |
| 2        | Multi-user mode without NFS (custom on some distros) |
| 3        | Full multi-user mode with networking (console login) |
| 4        | Unused/reserved (user-defined)                       |
| 5        | Graphical multi-user mode (desktop environment)      |
| 6        | Reboot                                               |

![The image is a text-based explanation of SysVinit runlevels, detailing their purposes and functions, such as system shutdown, single-user mode, and multi-user modes. It also mentions the role of /sbin/init in managing runlevels and services.](https://kodekloud.com/kk-media/image/upload/v1752881455/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Change-Runlevels-Boot-Targets-and-Shutdown-or-Reboot-System/sysvinit-runlevels-explanation-diagram.jpg)

Runlevels and their associated services are defined in two places:

* `/etc/inittab`: Specifies which scripts or processes to start at each runlevel
* `/etc/init.d/`: Contains the actual service scripts

### Common `/etc/inittab` Actions

| Action      | Description                                                                 |
| ----------- | --------------------------------------------------------------------------- |
| sysinit     | Run once during system initialization (ignores runlevels)                   |
| boot        | Run at boot time, but init does not wait for completion (ignores runlevels) |
| bootwait    | Run at boot time—init waits until it finishes (ignores runlevels)           |
| wait        | Run when entering listed runlevels—init waits for it to complete            |
| respawn     | Always restart the process if it terminates                                 |
| ctrlaltdel  | Triggered on `SIGINT` (CTRL+ALT+DEL)                                        |
| initdefault | Sets the default runlevel (values 1–5, not 0 or 6)                          |

![The image is a text-based explanation of SysVinit configuration files and runlevels, detailing the purpose of /etc/inittab and /etc/init.d/, along with descriptions of boot actions.](https://kodekloud.com/kk-media/image/upload/v1752881457/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Change-Runlevels-Boot-Targets-and-Shutdown-or-Reboot-System/sysvinit-configuration-runlevels-inittab.jpg)

## Editing `/etc/inittab`

Before making changes, back up the file:

```bash theme={null}
sudo cp /etc/inittab /etc/inittab.bak
```

Open it in your favorite editor:

```bash theme={null}
sudo vi /etc/inittab
```

A typical configuration might include:

```ini theme={null}
