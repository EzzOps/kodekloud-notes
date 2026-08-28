# Install a Boot Manager GRUB2

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/Linux-Installation-and-Package-Management/Install-a-Boot-Manager-GRUB2/page

This guide covers installing, configuring, and troubleshooting the GRUB2 bootloader on CentOS Stream 8.

Welcome to this comprehensive guide on installing, configuring, and troubleshooting the GRUB2 bootloader on CentOS Stream 8. You’ll learn how to recover a non-booting system using rescue media, install GRUB in BIOS or UEFI mode, customize its settings, and verify your changes.

<Frame>
  ![The image shows a boot menu for CentOS Stream 8-stream, offering options to install, test media, or troubleshoot.](https://kodekloud.com/kk-media/image/upload/v1752881426/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Install-a-Boot-Manager-GRUB2/centos-stream-8-boot-menu-options.jpg)
</Frame>

***

## 1. Prerequisites

Before you begin, ensure you have:

* A CentOS Stream 8 installation USB/DVD.
* Physical or virtual access to the target machine.
* A basic understanding of Linux shell commands.

<Callout icon="lightbulb">
  You will need root (or sudo) privileges to run most commands in this tutorial.
</Callout>

***

## 2. Boot into Rescue Environment

1. Insert your CentOS Stream 8 installation media and power on the machine.
2. At the main menu, select **Troubleshooting** → **Rescue a CentOS Stream System**.
3. Wait for system messages, then choose **1) Continue** at the rescue prompt:

   ```plain theme={null}
   The rescue environment will now attempt to find your Linux installation
   and mount it under /mnt/sysroot. You can then make any changes required.

   1) Continue
   2) Read-only mount
   3) Skip to shell
   4) Quit (Reboot)
   ```

The installer will mount your root filesystem at `/mnt/sysroot`.

***

## 3. Chroot into Your System

Change root into the mounted filesystem:

```bash theme={null}
chroot /mnt/sysroot
```

You’re now operating inside your installed system as if you had booted normally.

***

## 4. Generate a New GRUB Configuration

GRUB’s configuration file must be regenerated after installation or any changes to `/etc/default/grub`.

| Boot Mode | Configuration File Path         |
| --------- | ------------------------------- |
| BIOS      | `/boot/grub2/grub.cfg`          |
| UEFI      | `/boot/efi/EFI/centos/grub.cfg` |

Use one of these commands:

```bash theme={null}
