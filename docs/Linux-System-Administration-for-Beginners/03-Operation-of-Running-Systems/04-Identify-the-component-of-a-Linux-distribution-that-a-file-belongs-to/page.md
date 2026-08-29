# Reload sshd configuration
$ sudo kill -SIGHUP <sshd-PID>

# Graceful shutdown
$ kill <PID>

# Force kill
$ kill -9 <PID>

# Kill by name
$ pkill -KILL bash
```

> **triangle-alert** Killing your login shell (e.g., `bash`) will close your terminal or SSH session.

***

## Job Control: Background & Foreground

* **Ctrl+C**: Interrupt
* **Ctrl+Z**: Suspend

```bash theme={null}
$ vim /etc/hostname
[1]+ Stopped vim /etc/hostname
$ fg
vim /etc/hostname
```

* Start in background: `sleep 300 &`
* List jobs: `jobs`
* Bring to foreground: `fg %1`
* Send to background: `bg %1`

***

## Inspecting Open Files with `lsof`

List files held by a process:

```bash theme={null}
$ lsof -p $(pgrep -n bash)
COMMAND PID USER FD   TYPE DEVICE SIZE/OFF NODE NAME
bash    8401 aaron cwd  DIR  253,0   4096     262658 /home/aaron
bash    8401 aaron txt  REG  253,0 925360    514014 /usr/bin/bash
…
```

View root-owned processes:

```bash theme={null}
$ sudo lsof -p 1
```

Find processes using a specific file:

```bash theme={null}
$ sudo lsof /var/log/messages
```

***

## Links and References

* [ps(1) Manual](https://man7.org/linux/man-pages/man1/ps.1.html)
* [top(1) Manual](https://man7.org/linux/man-pages/man1/top.1.html)
* [kill(1) Manual](https://man7.org/linux/man-pages/man1/kill.1.html)
* [lsof(8) Manual](https://man7.org/linux/man-pages/man8/lsof.8.html)
* [Linux Process Management Guide](https://linux.die.net/man/1/ps)

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/ca5e9d7c-9dac-4ecc-9e21-dafef5ef2641/lesson/484c790f-dbad-440d-a4e4-1128d0cceb54)


# Identify the component of a Linux distribution that a file belongs to

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/Operation-of-Running-Systems/Identify-the-component-of-a-Linux-distribution-that-a-file-belongs-to/page

This guide explores DNF-based commands to identify packages owning files, list package contents, and filter file listings on Linux systems.

Discovering which package installed a specific file on your Linux system is invaluable when you need to restore default configurations after unintended edits. In this guide, we’ll explore DNF-based commands to:

* Find the package providing a file or command
* List all files in a package
* Filter package file listings

> **lightbulb** These examples assume a DNF-based distribution (Fedora, RHEL, CentOS Stream). On older systems using `yum`, substitute `yum provides` and `yum repoquery`.

***

## Table of Common DNF Queries

| Command                                        | Purpose                                  | Example                        |                |
| ---------------------------------------------- | ---------------------------------------- | ------------------------------ | -------------- |
| `dnf provides <file>`                          | Identify package owning a file           | `dnf provides /etc/anacrontab` |                |
| `dnf provides <command>`                       | Find package that supplies a CLI command | `dnf provides docker`          |                |
| `dnf repoquery --list <pkg>`                   | List every file in *any* package         | `dnf repoquery --list nginx`   |                |
| `dnf repoquery --list <pkg> \| grep <pattern>` | Filter listed files by name or extension | \`...                          | grep '.conf'\` |

***

## 1. Find Which Package Owns a File

Suppose you’ve modified `/etc/anacrontab` and want to revert it to the distribution’s original version. Use:

```bash theme={null}
$ dnf provides /etc/anacrontab
cronie-anacron-1.5.2-4.el8.x86_64 : Utility for running regular jobs
Repo        : baseos
Matched from:
Filename    : /etc/anacrontab

cronie-anacron-1.5.2-6.el8.x86_64 : Utility for running regular jobs
Repo        : @system
Matched from:
Filename    : /etc/anacrontab
```

The output shows `cronie-anacron` as the provider. To restore:

```bash theme={null}
$ sudo rm /etc/anacrontab
$ sudo dnf install --refresh cronie-anacron
```

After reinstalling, the original `/etc/anacrontab` is back in place.

> **triangle-alert** Removing system files can affect service behavior. Always backup configurations before deletion.

***

## 2. Discover Which Package Supplies a Command

Want the `docker` CLI but unsure which package includes it? Run:

```bash theme={null}
$ dnf provides docker
podman-docker-3.1.0-0.13.module_el8.5.0+733+9bb5dffa.noarch : Emulate Docker CLI
Repo        : appstream
Matched from:
Provide     : docker = 3.1.0-0.13.module_el8.5.0+733+9bb5dffa

podman-docker-3.3.0-0.17.module_el8.5.0+874+6db8bee3.noarch : Emulate Docker CLI
Repo        : appstream
Matched from:
Provide     : docker = 3.3.0-0.17.module_el8.5.0+874+6db8bee3
```

Here, `podman-docker` emulates the Docker CLI, so install it to use `docker`.

***

## 3. List All Files in a Package

To inspect every file a package ships—even if it isn’t installed locally—use:

```bash theme={null}
$ dnf repoquery --list nginx
/etc/logrotate.d/nginx
/etc/nginx/fastcgi.conf
/etc/nginx/fastcgi.conf.default
...
/usr/lib/.build-id
```

This complete list helps you identify configuration files, binaries, libraries, and other assets.

***

## 4. Filter the File Listing

Narrow down to specific file types (e.g., configuration files) by piping to `grep`:

```bash theme={null}
$ dnf repoquery --list nginx | grep '\.conf'
/etc/nginx/fastcgi.conf
/etc/nginx/fastcgi.conf.default
/etc/nginx/nginx.conf
/etc/nginx/nginx.conf.default
```

Use any regex pattern to quickly locate files of interest.

***

## Further Reading

* [DNF Command Reference](https://dnf.readthedocs.io/)
* [Fedora Package Management](https://docs.fedoraproject.org/en-US/quick-docs/dnf/)
* [Red Hat Enterprise Linux Subscription Guide](https://access.redhat.com/documentation/en-us/red_hat_subscription_management/)

Practice these commands to become confident in managing package-owned files and restoring default configurations on your DNF-based Linux system.

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/ca5e9d7c-9dac-4ecc-9e21-dafef5ef2641/lesson/d354e7d0-1479-4964-a400-65bc444ffdfa)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/ca5e9d7c-9dac-4ecc-9e21-dafef5ef2641/lesson/1c82b7ef-7485-4d29-bff1-adf3706193db)
