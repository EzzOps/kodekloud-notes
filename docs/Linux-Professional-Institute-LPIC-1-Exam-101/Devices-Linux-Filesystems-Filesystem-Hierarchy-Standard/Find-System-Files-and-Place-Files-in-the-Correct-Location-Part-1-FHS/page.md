# Example: create a shortcut to an image
ln -s /home/aaron/Pictures/family_dog.jpg family_dog_shortcut.jpg
```

* `<path_to_target>`: File or directory you want to reference.
* `<path_to_link>`: Name (and optional path) for the symlink.

<Callout icon="lightbulb">
  You can use absolute or relative paths. Relative links remain valid if you move the containing directory, as long as the relative structure doesn’t change.
</Callout>

## 2. Verify a Symlink

List files with detailed info:

```bash theme={null}
ls -l family_dog_shortcut.jpg
```

Output:

```text theme={null}
lrwxrwxrwx 1 aaron aaron 33 Apr  5 10:00 family_dog_shortcut.jpg -> /home/aaron/Pictures/family_dog.jpg
```

* Leading `l` denotes a symlink.
* Arrow (`->`) shows the target path.

To print only the target path without truncation:

```bash theme={null}
readlink family_dog_shortcut.jpg
# /home/aaron/Pictures/family_dog.jpg
```

## 3. Permissions and Access

Symbolic links always display full permissions (`rwxrwxrwx`), but actual access is governed by the target’s permissions:

```bash theme={null}
echo "Test" >> fstab_shortcut
# bash: fstab_shortcut: Permission denied
```

<Callout icon="triangle-alert">
  Even though the symlink appears writable, you’re blocked because the real file (`/etc/fstab`) isn’t writable by your user.
</Callout>

## 4. Absolute vs. Relative Paths

Absolute paths may break if you rename or move parent directories:

```bash theme={null}
# Create with absolute path
ln -s /home/aaron/Pictures/family_dog.jpg abs_shortcut
# Rename /home/aaron to /home/alex
mv /home/aaron /home/alex
ls -l abs_shortcut
# abs_shortcut -> /home/aaron/Pictures/family_dog.jpg  # Broken link
```

Better: use a relative link from the same directory:

```bash theme={null}
cd /home/aaron
ln -s Pictures/family_dog.jpg rel_shortcut
ls -l rel_shortcut
# rel_shortcut -> Pictures/family_dog.jpg
```

This link stays valid under `/home/alex` as long as the relative tree is preserved.

## 5. Linking Directories & Cross-Filesystem

Since symlinks store paths, you can reference directories and even across different filesystems:

```bash theme={null}
ln -s /var/log logs_shortcut
ls -l logs_shortcut
# logs_shortcut -> /var/log
```

<Frame>
  ![The image is a diagram explaining soft links, showing how they can link to files and folders, including across different filesystems.](https://kodekloud.com/kk-media/image/upload/v1752881382/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Create-and-Change-Soft-Links/soft-links-diagram-files-folders.jpg)
</Frame>

## Further Reading

* [GNU ln manual](https://www.gnu.org/software/coreutils/manual/html_node/ln-invocation.html)
* [readlink(1) Manual Page](https://man7.org/linux/man-pages/man1/readlink.1.html)
* Linux Filesystem Hierarchy: [Filesystem layout](https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/de71b96a-9dc0-4e92-987a-6c7055c44e8b/lesson/4f82c772-77a6-468a-81bc-b99cab3372f3" />
</CardGroup>


# Find System Files and Place Files in the Correct Location Part 1 FHS

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/Devices-Linux-Filesystems-Filesystem-Hierarchy-Standard/Find-System-Files-and-Place-Files-in-the-Correct-Location-Part-1-FHS/page

This article explains the Filesystem Hierarchy Standard for Unix-like operating systems, detailing directory layouts and their purposes.

## Introduction

The Filesystem Hierarchy Standard (FHS) defines a common directory layout and its contents for Unix-like operating systems. Maintained by the [Linux Foundation](https://www.linuxfoundation.org/) and detailed in the [FHS 3.0 specification](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html), this standard ensures that users and administrators can predict where to find system files, binaries, and configuration data. While FHS compliance is not mandatory, most Linux distributions follow it closely.

<Callout icon="lightbulb">
  FHS compliance guarantees a consistent directory layout, simplifying system administration, backups, and package management.
</Callout>

## Top-Level Directory Overview

| Path       | Purpose                                             | Common Contents / Examples           |
| ---------- | --------------------------------------------------- | ------------------------------------ |
| `/`        | Root of the filesystem hierarchy                    | Everything lives under `/`           |
| `/bin`     | Essential command binaries available to all users   | `ls`, `cp`, `mv`                     |
| `/boot`    | Static files for the bootloader                     | Kernel images (`vmlinuz`), initrd    |
| `/dev`     | Device nodes for hardware & virtual devices         | `/dev/sda`, `/dev/null`              |
| `/etc`     | Host-specific configuration files                   | `fstab`, `hosts`, service configs    |
| `/home`    | User home directories                               | `/home/alice`, `/home/bob`           |
| `/lib`     | Shared libraries needed by `/bin` and `/sbin`       | `libc.so.6`, kernel modules          |
| `/media`   | Mount points for removable media (USB, CD/DVD)      | `/media/usb`, `/media/cdrom`         |
| `/mnt`     | Temporary mount points for administrators           | `/mnt/shared`                        |
| `/opt`     | Optional or third-party software packages           | `/opt/google`, `/opt/mysql`          |
| `/root`    | Superuser’s home directory                          | `/root/.bashrc`, `/root/.ssh/`       |
| `/run`     | Runtime data (PID files, sockets)                   | `/run/docker`, `/run/sshd.pid`       |
| `/sbin`    | System binaries for booting & maintenance           | `fsck`, `ip`, `iptables`             |
| `/srv`     | Data served by system services                      | `/srv/www/`, `/srv/ftp/`             |
| `/tmp`     | Temporary files cleared at reboot                   | `/tmp/session_12345`                 |
| `/usr`     | Secondary hierarchy for read-only user applications | `/usr/bin`, `/usr/lib`, `/usr/share` |
| `/proc`    | Virtual filesystem for process & kernel information | `/proc/cpuinfo`, `/proc/<pid>/`      |
| `/var`     | Variable data files (logs, spools, caches)          | `/var/log`, `/var/spool/mail`        |
| `/var/tmp` | Temporary files preserved between reboots           | `/var/tmp/install_cache`             |

<Frame>
  ![The image displays a list of directories from the Filesystem Hierarchy Standard, commonly used in Unix-like operating systems.](https://kodekloud.com/kk-media/image/upload/v1752881383/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Find-System-Files-and-Place-Files-in-the-Correct-Location-Part-1-FHS/filesystem-hierarchy-standard-directories-list.jpg)
</Frame>

## Summary Tree

```bash theme={null}
/
├── bin
├── boot
├── dev
├── etc
├── home
├── lib
├── media
├── mnt
├── opt
├── root
├── run
├── sbin
├── srv
├── tmp
├── usr
├── proc
└── var
    └── tmp
```

## Further Reading

* [Filesystem Hierarchy Standard (FHS 3.0)](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html)
* [Linux Directory Structure Explained](https://www.tldp.org/LDP/Linux-Filesystem-Hierarchy/html/)
* [The Linux Documentation Project](https://www.tldp.org/)

Ready to test your understanding? Proceed to the quiz section!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/de71b96a-9dc0-4e92-987a-6c7055c44e8b/lesson/7dcca80c-10d9-496d-8c44-31fd1c86f583" />
</CardGroup>
