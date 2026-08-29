# Or from a local network path
sudo yum-config-manager --add-repo http://192.168.1.220/BaseOS.repo
```

This creates a `.repo` file in `/etc/yum.repos.d/`. Verify it:

```bash theme={null}
sudo yum repolist -v | grep Repo-filename
```

***

## 5. Understanding a `.repo` File

Open the Docker repo for inspection:

```bash theme={null}
sudo vi /etc/yum.repos.d/docker-ce.repo
```

```ini theme={null}
[docker-ce-stable]
name=Docker CE Stable - $basearch
baseurl=https://download.docker.com/linux/rhel/$releasever/$basearch/stable
enabled=1
gpgcheck=1
gpgkey=https://download.docker.com/linux/rhel/gpg
```

| Field       | Description                                       |
| ----------- | ------------------------------------------------- |
| `[repo-id]` | Unique identifier in brackets                     |
| `name=`     | Human-readable repository name                    |
| `baseurl=`  | URL to fetch packages                             |
| `enabled=`  | `1` to enable, `0` to disable                     |
| `gpgcheck=` | `1` enforces GPG signature checking (recommended) |
| `gpgkey=`   | URL or file path to the GPG public key            |

To completely remove a repository, delete its file:

```bash theme={null}
sudo rm /etc/yum.repos.d/docker-ce.repo
```

***

## 6. Searching for Packages

If you’re unsure of the exact name, use `yum search`. Single terms match any, quotes require both terms.

```bash theme={null}
# Matches "web" OR "server"
sudo yum search web server

# Matches packages containing both "web" AND "server"
sudo yum search 'web server'
```

Example result:

```text theme={null}
nginx.x86_64 : A high performance web server and reverse proxy server
```

***

## 7. Viewing Package Information

Inspect a package before installation:

```bash theme={null}
sudo yum info nginx
```

Sample output:

```text theme={null}
Name        : nginx
Version     : 1.20.1
Release     : 1.el8
Architecture: x86_64
Summary     : High performance web server and reverse proxy
Description : NGINX is a web server and a reverse proxy server for HTTP, SMTP, POP3 and
              IMAP protocols with a focus on high concurrency, performance and low
              memory usage.
```

***

## 8. Installing, Reinstalling, and Removing Packages

Install a new package:

```bash theme={null}
sudo yum install nginx
```

Reinstall (e.g., to restore missing config files):

```bash theme={null}
sudo yum reinstall nginx
```

Remove a package and its dependencies:

```bash theme={null}
sudo yum remove nginx
```

Clean up unneeded dependencies:

```bash theme={null}
sudo yum autoremove
```

***

## 9. Managing Package Groups

YUM supports predefined groups (e.g., “Server with GUI”).

| Command                               | Description              |
| ------------------------------------- | ------------------------ |
| `sudo yum group list`                 | List available groups    |
| `sudo yum group list --hidden`        | Include hidden groups    |
| `sudo yum group install 'Group Name'` | Install a specific group |
| `sudo yum group remove 'Group Name'`  | Remove a specific group  |

Example:

```bash theme={null}
sudo yum group install 'Server with GUI'
```

***

## 10. Installing from a Local RPM File

After downloading an RPM:

```bash theme={null}
sudo wget https://download.nomachine.com/download/7.7/Linux/nomachine_7.7.4_1_x86_64.rpm
sudo yum install ./nomachine_7.7.4_1_x86_64.rpm
```

Remove it when no longer needed:

```bash theme={null}
sudo yum remove nomachine
```

***

## 11. Updating and Upgrading Packages

Check for available updates:

```bash theme={null}
sudo yum check-update
```

Apply all updates:

```bash theme={null}
sudo yum update
```

> **triangle-alert** If a kernel or critical component is updated, reboot to ensure changes take effect:

  ```bash theme={null}
  sudo reboot
  ```

***

## Links and References

* [Red Hat Subscription Management](https://access.redhat.com/documentation/en-us/red_hat_subscription_management/)
* [YUM Official Documentation](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/managing_packages_with_yum/index)
* [Docker CE Repository for RHEL](https://docs.docker.com/engine/install/centos/)

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/78ca0fa8-2083-408a-bf8a-2775b09fbf1d/lesson/4c5f841d-94ae-4b1d-bb25-4f3564494554)


# Boot the System

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/System-Architecture/Boot-the-System/page

This guide explains the Linux boot process, covering stages from firmware to the init system for troubleshooting and optimization.

Understanding the Linux boot process is essential for troubleshooting and optimizing system startup. This guide walks through each stage—from firmware to the init system—detailing BIOS/UEFI, the GRUB bootloader, kernel initialization with initramfs, and the init process.

![The image is a flowchart illustrating the system boot process, showing the sequence from BIOS or UEFI to Bootloader, Kernel, and Init.](https://kodekloud.com/kk-media/image/upload/v1752881446/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Boot-the-System/system-boot-process-flowchart.jpg)

## 1. BIOS and the Master Boot Record (MBR)

The Basic Input/Output System (BIOS) resides on a motherboard chip and executes immediately after power-on. It performs:

1. **Power-On Self-Test (POST):** Verifies basic hardware (CPU, memory, etc.).
2. **Device Initialization:** Activates video, keyboard, and storage controllers.
3. **MBR Read:** Loads the first 512 bytes—the Master Boot Record—from the configured disk.
4. **Bootstrap Loader:** Executes the first-stage bootloader (440 bytes), reads the partition table, then transfers control to the second stage to load the bootloader and kernel.

> **lightbulb** The MBR format supports disks up to 2 TiB and allows a maximum of four primary partitions. Consider GPT for larger disks.

![The image illustrates a comparison between two storage sections: one with 440 bytes for the first device bootstrap and another with 512 bytes for the MBR and DOS partition.](https://kodekloud.com/kk-media/image/upload/v1752881447/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Boot-the-System/storage-comparison-bootstrap-mbr-dos.jpg)

![The image is a slide explaining the BIOS POST process, detailing its functions like identifying hardware failures, activating components, loading the bootstrap from the MBR, and loading the bootloader's second stage.](https://kodekloud.com/kk-media/image/upload/v1752881448/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Boot-the-System/bios-post-process-explanation-slide.jpg)

## 2. UEFI (Unified Extensible Firmware Interface)

UEFI modernizes BIOS by using non-volatile memory (NVRAM) to locate EFI applications on an EFI System Partition (ESP). Key aspects:

1. **UEFI POST:** Hardware diagnostics similar to BIOS.
2. **Component Activation:** Initializes video, input, and storage.
3. **EFI Application:** Loads the bootloader or OS selector from `/EFI` on the ESP (FAT12/16/32 or ISO 9660).
4. **Kernel Loading:** Transfers control to the bootloader, which loads the Linux kernel.

UEFI’s Secure Boot verifies digital signatures, preventing unauthorized kernels and bootloaders.

> **triangle-alert** Disabling Secure Boot is often required when installing unsigned or custom kernels. Ensure you understand the security implications.

![The image is a diagram related to UEFI, showing components like NVRAM, EFI applications, FAT filesystems or ISO-9660, and the EFI System Partition (ESP).](https://kodekloud.com/kk-media/image/upload/v1752881449/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Boot-the-System/uefi-diagram-nvram-efi-applications.jpg)

![The image is a slide describing the functions of UEFI, including identifying hardware failures, activating components, executing EFI applications, loading the kernel, and supporting Secure Boot.](https://kodekloud.com/kk-media/image/upload/v1752881450/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Boot-the-System/uefi-functions-hardware-failures-secure-boot.jpg)

## 3. GRUB: The Grand Unified Bootloader

GRUB is the most common x86 bootloader for BIOS and UEFI systems. Press **Shift** (BIOS) or **Esc** (UEFI) to access the menu if it doesn’t appear.

![The image is an informational graphic about the Grand Unified Bootloader (GRUB), showing key combinations for BIOS (SHIFT) and UEFI (ESC) booting.](https://kodekloud.com/kk-media/image/upload/v1752881451/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Boot-the-System/grub-bootloader-bios-uefi-graphic.jpg)

From GRUB, you can select kernels and pass parameters in `option=value` format:

| Parameter                        | Description                                          |
| -------------------------------- | ---------------------------------------------------- |
| `acpi=off`                       | Disable ACPI support                                 |
| `init=/bin/bash`                 | Boot directly to a Bash shell                        |
| `systemd.unit=multi-user.target` | Set the systemd target (e.g., multi-user, graphical) |
| `mem=512M`                       | Limit maximum RAM available                          |
| `maxcpus=2`                      | Restrict CPU cores                                   |
| `quiet`                          | Suppress most boot messages                          |
| `vga=ask`                        | Prompt for video mode                                |
| `root=/dev/sda3`                 | Specify root filesystem partition                    |
| `rootflags=ro` or `rootflags=rw` | Mount root filesystem read-only or read-write        |

![The image is a list of bootloader commands and their descriptions, including examples for setting system parameters like ACPI, system initialization, RAM, processors, and root filesystem options.](https://kodekloud.com/kk-media/image/upload/v1752881452/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Boot-the-System/bootloader-commands-system-parameters-list.jpg)

We’ll cover permanent GRUB configuration in a later lesson.

## 4. Kernel Initialization and initramfs

After GRUB loads the kernel:

1. **Kernel Startup:** Initializes CPU, memory management, and drivers.
2. **initramfs Mount:** Unpacks the initial RAM filesystem, which includes essential modules and tools.
3. **Real Root Mount:** Switches to the actual root partition defined in `/etc/fstab`.
4. **Exec Init:** The kernel runs:

```bash theme={null}
exec /sbin/init
```

This launches the init system and frees the initramfs from memory.

![The image is a slide explaining the Linux boot process, detailing how the kernel is loaded into RAM, mounts filesystems, and loads the init program.](https://kodekloud.com/kk-media/image/upload/v1752881453/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Boot-the-System/linux-boot-process-kernel-init-slide.jpg)

## 5. Init Systems: SysV, systemd, and Upstart

Linux distributions may use different init managers:

| Init System | Type            | Key Features                                                                    |
| ----------- | --------------- | ------------------------------------------------------------------------------- |
| SysV init   | Runlevel-based  | Sequential startup with scripts, runlevels 0–6                                  |
| systemd     | Service manager | Parallel startup, socket/D-Bus activation, cgroups, dependency-based units      |
| Upstart     | Event-driven    | Responds to system events for parallel service startup (legacy Ubuntu releases) |

![The image is a comparison of three init systems: SysV standard, systemd, and Upstart, describing their functions and usage.](https://kodekloud.com/kk-media/image/upload/v1752881454/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Boot-the-System/init-systems-comparison-sysv-systemd-upstart.jpg)

## Viewing and Analyzing Boot Messages

The kernel logs boot messages in a ring buffer. To inspect them:

```bash theme={null}
dmesg | less
```

On systems with systemd, use `journalctl`:

* List recorded boots:

  ```bash theme={null}
  journalctl --list-boots
  ```

* View the current boot log (`boot 0`):

  ```bash theme={null}
  journalctl -b 0
  ```

To read logs from a different directory:

```bash theme={null}
journalctl -D /var/log/other_directory
```

## Links and References

* [Linux Kernel Newbies – Boot Process](https://kernelnewbies.org/BootProcess)
* [GNU GRUB Manual](https://www.gnu.org/software/grub/manual/)
* [systemd Documentation](https://www.freedesktop.org/wiki/Software/systemd/)
* [BIOS Basics on Wikipedia](https://en.wikipedia.org/wiki/BIOS)
* [Unified Extensible Firmware Interface Forum](https://uefi.org/)

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/55c2d118-3a85-4da1-8a7f-e9f8671cc818/lesson/f59861cb-06f6-4c38-8d5f-f19970b20ea2)
