# Boot or change system into different operating modes

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/Operation-of-Running-Systems/Boot-or-change-system-into-different-operating-modes/page

Learn to view, set, and switch between different systemd targets on a Linux system for optimized boot behavior.

In this guide, you’ll learn how to view, set, and temporarily switch between different systemd targets on a Linux system. A **systemd target** defines which services and programs run (or remain inactive) at boot time—ranging from a full graphical desktop to a minimal emergency shell.

Understanding these targets helps you optimize boot behavior for servers, desktops, or recovery scenarios.

***

## 1. Understand Common systemd Targets

| Target            | Description                                           | Typical Use Case                           |
| ----------------- | ----------------------------------------------------- | ------------------------------------------ |
| graphical.target  | Full desktop environment with display manager         | Workstations, desktops                     |
| multi-user.target | Text-mode login with networking and standard services | Servers, headless systems                  |
| rescue.target     | Single-user mode with essential services              | System maintenance, filesystem checks      |
| emergency.target  | Minimal shell on the root filesystem (read-only)      | Critical repairs, root filesystem recovery |

***

## 2. Check the Current Default Target

To display your system’s default boot target:

```bash theme={null}
systemctl get-default
```

Example output:

```plaintext theme={null}
graphical.target
```

`graphical.target` means the system will start the graphical interface by default.

***

## 3. Change the Default Target

You can switch your default boot target to control which mode the system enters on every reboot.

### 3.1 Set Default to Multi-User (Text Console)

```bash theme={null}
sudo systemctl set-default multi-user.target
```

Output:

```plaintext theme={null}
Removed /etc/systemd/system/default.target.
Created symlink /etc/systemd/system/default.target → /usr/lib/systemd/system/multi-user.target.
```

Rebooting now drops you to a text-based login:

```plaintext theme={null}
CentOS Stream 8
Kernel 4.18.0-365.el8.x86_64 on an x86_64

LFCS-CentOS login: aaron
Password:
[aaron@LFCS-CentOS ~]$
```

***

## 4. Temporarily Switch Targets without Reboot

Use the `isolate` command to move into another target immediately—this does **not** alter your default target.

```bash theme={null}
sudo systemctl isolate graphical.target
```

Your session switches to the graphical environment, but on the next reboot you’ll return to whatever default target is configured.

***

## 5. Rescue and Emergency Modes

For critical troubleshooting, systemd provides two minimal targets.

### 5.1 rescue.target

Loads essential services and drops you to a root shell:

```bash theme={null}
sudo systemctl isolate rescue.target
```

### 5.2 emergency.target

Mounts only the root filesystem (read-only) and gives you a minimal shell:

```bash theme={null}
sudo systemctl isolate emergency.target
```

> **lightbulb** Both `rescue.target` and `emergency.target` require a root password. Ensure `root` has a valid password before invoking these modes.

***

## 6. Restore Graphical Desktop as Default

To return to booting into the graphical interface by default:

```bash theme={null}
sudo systemctl set-default graphical.target
```

Output:

```plaintext theme={null}
Removed /etc/systemd/system/default.target.
Created symlink /etc/systemd/system/default.target → /usr/lib/systemd/system/graphical.target.
```

***

## Links and References

* [systemd Targets Documentation](https://www.freedesktop.org/software/systemd/man/systemd.special.html)
* [Managing systemd Services](https://www.freedesktop.org/software/systemd/man/systemctl.html)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Linux Command Line Cheat Sheet](https://www.linuxtrainingacademy.com/linux-commands-cheat-sheet/)

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/ca5e9d7c-9dac-4ecc-9e21-dafef5ef2641/lesson/e4327fde-ec56-4d9d-bd75-8b7625734abf)
