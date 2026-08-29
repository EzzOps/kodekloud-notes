# When logged in as root:
$ systemctl reboot

# When using sudo as a regular user:
$ sudo systemctl reboot
[sudo] password for aaron:
```

## Shutting Down the System

To safely shut down the system, whether as root or using sudo, execute:

```bash theme={null}
$ sudo systemctl power off
[sudo] password for aaron:
```

In certain cases, an unresponsive or misbehaving program may cause the system to refuse a normal reboot or shutdown. In such instances, you can force the operation by appending the --force flag. Use this option only when absolutely necessary.

```bash theme={null}
$ sudo systemctl reboot --force
```

or

```bash theme={null}
$ sudo systemctl power off --force
```

If a single force does not succeed, you may specify the force flag twice. This method functions similar to pressing the physical reset button, immediately rebooting the system without allowing programs to close properly or save their data.

> **triangle-alert** Forcing a reboot or shutdown can result in data loss. Use the force option only as a last resort.

## Scheduling Reboots and Shutdowns

In managed server environments, you might need to perform scheduled reboots or shutdowns without manual intervention, often during off-peak hours. The shutdown command is ideal for this purpose.

### Schedule a Shutdown at a Specific Time

Use the 24-hour format when specifying a shutdown time:

```bash theme={null}
$ sudo shutdown 02:00
[sudo] password for aaron:
```

### Schedule a Shutdown after a Delay

To schedule a shutdown a certain number of minutes in the future, replace the time with a plus sign (+) followed by the delay in minutes. For example, to shut down after 15 minutes:

```bash theme={null}
$ sudo shutdown +15
[sudo] password for aaron:
```

### Schedule a Reboot

To schedule a reboot, simply include the -r option. For instance:

```bash theme={null}
# Schedule a reboot at 2 a.m.
$ sudo shutdown -r 02:00
[sudo] password for aaron:

# Schedule a reboot after 15 minutes
$ sudo shutdown -r +15
[sudo] password for aaron:
```

## Utilizing the Wall Message Feature

The shutdown command supports a wall message feature that notifies all logged-in users about an impending reboot or shutdown. This feature gives users time to save their work or prepare for disconnection.

For example, to schedule a reboot in one minute while displaying a message about a scheduled Linux kernel upgrade, use:

```bash theme={null}
$ sudo shutdown -r +1 'Scheduled restart to upgrade our Linux kernel'
[sudo] password for aaron:
```

## Conclusion

By following these system commands and scheduling techniques, you can manage the boot, reboot, and shutdown processes of a Linux system safely and efficiently. Make sure to use forced options only when absolutely necessary to prevent potential data loss, and always provide clear notifications to your users when scheduling system maintenance.

For additional Linux administration tips, please refer to [the official Linux documentation](https://www.kernel.org/doc/html/latest/).

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-foundation-certified-system-administrator-lfcs/module/cb813f7f-73bd-40ee-a088-d31ba20c51de/lesson/d65ba901-1f95-4591-a0ce-5d4442a085b9)


# Boot or Change System Into Different Operating Modes Optional

Source: https://notes.kodekloud.com/docs/Prep-Course-Linux-Foundation-Certified-System-Administrator-LFCS-Certification/Operations-Deployment/Boot-or-Change-System-Into-Different-Operating-Modes-Optional/page

This article explains how to use systemd targets in Linux to control the boot process and modify the default boot target for different environments.

In this article, we explore how Linux leverages systemd targets to control the boot process and how you can modify the default boot target to suit different system environments. By understanding systemd targets, you gain flexibility in managing resource usage and operational modes.

Currently, the Linux system boots to a graphical login screen. At startup, the operating system loads various programs and services in a specific order using instructions defined in systemd target files. To see which boot target is active by default, run:

```bash theme={null}
systemctl get-default
```

If the output is "graphical.target," it means the system is configured to boot into a full graphical environment. The corresponding graphical.target file contains the necessary instructions to start services and programs required for a graphical login.

Booting into the graphical target requires additional system resources due to the loading of the graphical user interface. If you do not need the graphical environment, you can change the default boot target to a more resource-efficient option, such as the multi-user target. This target provides essential services—like daemons and network services—running in a text-based mode. To switch the default boot target, execute:

```bash theme={null}
sudo systemctl set-default multi-user.target
```

> **lightbulb** Changing the default boot target means that on the next reboot, the system will operate in text mode rather than launching a graphical interface.

Below is an example session showing how to check and change the default boot target:

```bash theme={null}
