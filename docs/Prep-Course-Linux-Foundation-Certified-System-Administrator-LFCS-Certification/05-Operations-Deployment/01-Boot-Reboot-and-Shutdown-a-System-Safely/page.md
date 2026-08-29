# Boot Reboot and Shutdown a System Safely

Source: https://notes.kodekloud.com/docs/Prep-Course-Linux-Foundation-Certified-System-Administrator-LFCS-Certification/Operations-Deployment/Boot-Reboot-and-Shutdown-a-System-Safely/page

Learn methods to safely boot, reboot, and shut down a Linux system using system commands and administrative privileges.

In this lesson, you will learn several methods to boot, reboot, and shut down a Linux system safely using system commands. Linux uses the systemctl command (short for "system control") to manage system states, and many of these commands require administrative privileges. The root account inherently has these privileges; however, regular users can execute them by prefixing commands with sudo.

<Callout icon="lightbulb">
  If you are logged in as root, you do not need the sudo prefix for any of these commands.
</Callout>

Below, we present a summary of the fundamental commands for rebooting and shutting down your system.

## Rebooting the System

### As the Root User

When you are logged in as the root user, simply execute:

```bash theme={null}
$ systemctl reboot
```

### As a Regular User with Elevated Privileges

If you are a regular user, use sudo to obtain temporary root privileges:

```bash theme={null}
$ sudo systemctl reboot
[sudo] password for aaron:
```

### Summary of Reboot Commands

```bash theme={null}
