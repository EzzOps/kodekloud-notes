# Install a Boot Manager GRUB Legacy

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/Linux-Installation-and-Package-Management/Install-a-Boot-Manager-GRUB-Legacy/page

This guide explains how to install, configure, and manage the GRUB Legacy bootloader on Linux systems.

In this guide, you’ll learn how to install, reinstall, and configure the GRUB Legacy bootloader on your Linux system. We cover both methods—installing from a running system and from the GRUB shell on a rescue disk—plus how to edit your `menu.lst` and chainload Windows.

## Table of Contents

1. [Overview](#overview)
2. [Installing from a Running System](#installing-from-a-running-system)
3. [Reinstalling via the GRUB Shell](#reinstalling-via-the-grub-shell)
4. [Editing `/boot/grub/menu.lst`](#editing-bootgrubmenulst)
5. [Chainloading Windows](#chainloading-windows)
6. [Command Reference](#command-reference)
7. [Links and References](#links-and-references)

## Overview

GRUB Legacy (version 0.9x) remains a popular choice for legacy hardware or minimal setups. You’ll install its core files to `/boot/grub` and write stage1 into the Master Boot Record (MBR).

> **triangle-alert** Always double-check your target device (e.g., `/dev/sda`) before running `grub-install` or `setup`. Installing to the wrong disk can overwrite critical data.

***

## Installing from a Running System

Use the `grub-install` utility to deploy GRUB Legacy without rebooting:

```bash theme={null}
sudo grub-install <device>
```

Example: install to the first disk (`/dev/sda`):

```bash theme={null}
sudo grub-install /dev/sda
```

By default, GRUB places its core files under `/boot/grub`. To change this directory, pass:

```bash theme={null}
sudo grub-install --boot-directory=/custom/boot /dev/sda
```

> **lightbulb** The `--boot-directory` option is helpful if you’re using a custom EFI or boot partition layout.

***

## Reinstalling via the GRUB Shell

When your system fails to boot, use a GRUB Legacy rescue disk:

1. Boot from the rescue media and press `c` to open the `grub>` prompt.

2. Identify and mount your boot partition (where `/boot/grub` resides):

   ```bash theme={null}
   grub> root (hd0,0)
   ```

3. If unsure, locate `stage1` with `find`:

   ```bash theme={null}
   grub> find /boot/grub/stage1
   (hd0,0)
   ```

4. Write GRUB’s stage1 into the MBR of the first disk:

   ```bash theme={null}
   grub> setup (hd0)
   ```

5. Reboot—the GRUB menu should appear.

***

## Editing `/boot/grub/menu.lst`

The GRUB Legacy configuration file is a simple plain-text list of menu entries. Open it with your favorite editor:

```bash theme={null}
sudo vi /boot/grub/menu.lst
```

Lines starting with `#` and blank lines are ignored.

### Basic Linux Entry

```bash theme={null}
title   My Linux Distribution
root    (hd0,0)
kernel  /vmlinuz root=/dev/sda1 ro quiet splash
```

| Directive | Description                                                           | Example                                |
| --------- | --------------------------------------------------------------------- | -------------------------------------- |
| `title`   | Label shown in the GRUB menu                                          | `My Linux Distribution`                |
| `root`    | GRUB device containing kernel & modules (disks/partitions start at 0) | `(hd0,0)`                              |
| `kernel`  | Path to kernel (relative to `root`) plus boot parameters              | `/vmlinuz root=/dev/sda1 ro quiet`     |
| `initrd`  | Initial RAM disk (if required)                                        | `/initrd.img`                          |
| `module`  | GRUB module to load (e.g., filesystem support, framebuffer)           | `/boot/grub/i386-pc/915resolution.mod` |

### Omitting the `root` Directive

You can embed the device specifier within the `kernel` path:

```bash theme={null}
title   Alt Linux Entry
kernel  (hd0,0)/vmlinuz root=/dev/sda1 ro
```

***

## Chainloading Windows

To boot Windows or another OS via chainloading:

```bash theme={null}
title   Windows XP
root    (hd0,1)
makeactive
chainload +1
boot
```

* **root (hd0,1)**: Second partition of the first disk.
* **makeactive**: Marks this partition as active (necessary for DOS/Windows).
* **chainload +1**: Loads its first sector.
* **boot**: Handoffs control to the loaded bootloader.

***

## Command Reference

| Command                                  | Purpose                                                  |
| ---------------------------------------- | -------------------------------------------------------- |
| `grub-install <device>`                  | Install GRUB from a running Linux system                 |
| `--boot-directory=<path>`                | Specify custom location for GRUB files                   |
| `root (hdX,Y)`                           | Set the GRUB root device in rescue shell                 |
| `find /boot/grub/stage1`                 | Search for the stage1 file to identify correct partition |
| `setup (hdX)`                            | Write stage1 into the MBR                                |
| `title` / `kernel` / `initrd` / `module` | Define menu entries in `menu.lst`                        |
| `makeactive` / `chainload`               | Chainload another bootloader (e.g., Windows)             |

***

## Links and References

* [GNU GRUB Manual (Legacy)](https://www.gnu.org/software/grub/manual/grub/grub.html)
* [Linux Documentation Project: BootPrompt](https://tldp.org/HOWTO/BootPrompt-HOWTO/)
* [GRUB Rescue Disk 101](https://wiki.archlinux.org/title/GRUB)

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/78ca0fa8-2083-408a-bf8a-2775b09fbf1d/lesson/839ddf40-72e9-4be9-965d-7f7543a765d3)
