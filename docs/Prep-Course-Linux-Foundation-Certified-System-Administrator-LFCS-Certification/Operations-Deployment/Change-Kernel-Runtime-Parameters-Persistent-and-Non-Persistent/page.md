# Check the current default target
jeremy@kodekloud:~$ systemctl get-default
graphical.target

# Set the default target to multi-user
jeremy@kodekloud:~$ sudo systemctl set-default multi-user.target
[sudo] password for jeremy:
Removed "/etc/systemd/system/default.target".
Created symlink /etc/systemd/system/default.target → /lib/systemd/system/multi-user.target.
jeremy@kodekloud:~$
```

The multi-user target is named so because it supports simultaneous logins by multiple users, while still keeping network services active to ensure continuous connectivity.

After changing the default target, reboot the system. Instead of the usual graphical login screen, you will encounter a text-based login console, similar to the following:

```bash theme={null}
Ubuntu 23.10 kodekloud tty1
kodekloud: jeremy
Password:
Welcome to Ubuntu 23.10 (GNU/Linux 6.5.0-27-generic x86_64)
 * Documentation: https://help.ubuntu.com
 * Management: https://landscape.canonical.com
 * Support: https://ubuntu.com/advantage

68 updates can be applied immediately.
To see these additional updates run: apt list --upgradeable

The list of available updates is more than a week old.
To check for new updates, run: sudo apt update
Last login: Tue May 28 12:25:21 PDT 2024 on tty1
jeremy@kodekloud:~$
```

If you temporarily need a graphical interface—perhaps to work with a 3D modeling application—you don't have to permanently switch the boot target. Instead, you can start the graphical environment immediately using:

```bash theme={null}
sudo systemctl isolate graphical.target
```

This command activates the graphical interface on demand without altering the system's default text-based boot mode.

Additional systemd targets include emergency.target and rescue.target. The table below summarizes the most commonly used targets and their purposes:

| Target            | Description                                               | Use Case                                                  | Command Example                              |
| ----------------- | --------------------------------------------------------- | --------------------------------------------------------- | -------------------------------------------- |
| graphical.target  | Boots into a full graphical desktop environment           | Standard desktop usage                                    | systemctl get-default                        |
| multi-user.target | Boots into a text-based environment with network services | Server or low-resource environments                       | sudo systemctl set-default multi-user.target |
| emergency.target  | Boots with minimal system services; root FS is read-only  | Critical troubleshooting when other services cause issues | (Invoked automatically when selected)        |
| rescue.target     | Loads essential services with a root shell access         | Administrative tasks in a minimal environment             | (Invoked automatically when selected)        |

<Callout icon="triangle-alert">
  When booting into emergency.target or rescue.target, ensure that the root account has a password set. Without a root password, these modes will not be accessible.
</Callout>

This concludes the demonstration on changing systemd targets and boot modes. For further details on system management and troubleshooting, be sure to refer to the official [systemd documentation](https://www.freedesktop.org/wiki/Software/systemd/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-foundation-certified-system-administrator-lfcs/module/cb813f7f-73bd-40ee-a088-d31ba20c51de/lesson/99c33a5f-0308-4bf8-925b-9436fc8c0c7c" />
</CardGroup>


# Change Kernel Runtime Parameters Persistent and Non Persistent

Source: https://notes.kodekloud.com/docs/Prep-Course-Linux-Foundation-Certified-System-Administrator-LFCS-Certification/Operations-Deployment/Change-Kernel-Runtime-Parameters-Persistent-and-Non-Persistent/page

Learn to modify Linux kernel runtime parameters temporarily and permanently, influencing system behavior like memory management and networking.

In this article, you will learn how to modify Linux kernel runtime parameters both temporarily (non-persistent) and permanently (persistent). Kernel runtime parameters control essential aspects of the Linux kernel, such as memory management, networking, and filesystem behavior.

## Viewing Current Kernel Parameters

Kernel parameters influence how the system operates. You can see all active settings using:

```bash theme={null}
$ sysctl -a
fs.pipe-user-pages-hard = 0
fs.pipe-user-pages-soft = 16384
sysctl: permission denied on key 'fs.protected_fifos'
sysctl: permission denied on key 'fs.protected_hardlinks'
sysctl: permission denied on key 'fs.protected_regular'
```

If you encounter permission issues, run the command with root privileges:

```bash theme={null}
$ sudo sysctl -a
net.ipv6.conf.default.addr_gen_mode = 0
net.ipv6.conf.default.autoconf = 1
net.ipv6.conf.default.dad_transmits = 1
net.ipv6.conf.default.disable_ipv6 = 0
net.ipv6.conf.default.disable_policy = 0
vm.admin_reserve_kbytes = 8192
```

Notice that naming conventions give clues about parameters’ purposes:

* Parameters beginning with `net.` relate to networking.
* Parameters starting with `vm.` pertain to virtual memory.
* Filesystem settings use the `fs.` prefix.

## Adjusting a Specific Kernel Parameter (Non-Persistent)

Let’s consider the parameter `net.ipv6.conf.default.disable_ipv6`. A value of 0 indicates that IPv6 is enabled. To disable IPv6 temporarily, change its value to 1:

```bash theme={null}
$ sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1
net.ipv6.conf.default.disable_ipv6 = 1
```

You can verify the updated setting with:

```bash theme={null}
$ sudo sysctl net.ipv6.conf.default.disable_ipv6
net.ipv6.conf.default.disable_ipv6 = 1
```

<Callout icon="lightbulb">
  Non-persistent changes will revert upon reboot, reverting to the default values.
</Callout>

To check a specific parameter without listing all parameters, append its name to the `sysctl` command. Use `sudo` if permissions are insufficient.

## Making Changes Persistent

Persistent adjustments require adding a configuration file in the `/etc/sysctl.d` directory. These files must have a `.conf` extension, ensuring that your custom settings are applied automatically at system boot.

<Frame>
  ![The image shows a directory path "/etc/sysctl.d/" with a configuration file named "Filename.conf" to make changes persistent.](https://kodekloud.com/kk-media/image/upload/v1752881327/notes-assets/images/Linux-Foundation-Certified-System-Administrator-LFCS-Change-Kernel-Runtime-Parameters-Persistent-and-Non-Persistent/etc-sysctl-d-filename-conf.jpg)
</Frame>

For more details, refer to the manual page:

```bash theme={null}
$ man sysctl.d
```

Listing the directory contents with `ls /etc/sysctl.d` will also display sample configuration files that serve as formatting examples.

## Filtering Specific Parameters

To view only memory-related settings (prefixed with `vm.`), use the following command:

```bash theme={null}
$ sysctl -a | grep vm
vm.panic_on_oom = 0
vm.percpu_pagelist_fraction = 0
vm.stat_interval = 1
vm.swappiness = 60
```

The parameter `vm.swappiness`, currently set to 60, controls swap behavior. A higher value increases swapping, while a lower value reduces swap usage.

## Making vm.swappiness Persistent

To permanently change `vm.swappiness` to 20, follow these steps:

1. Create a configuration file in `/etc/sysctl.d`. For example, name it `swap-less.conf` to indicate reduced swapping:

   ```bash theme={null}
   $ sudo vim /etc/sysctl.d/swap-less.conf
   ```

2. Add the following line to set the swappiness value:

   ```conf theme={null}
   vm.swappiness=20
   ```

3. Save the file. Although the setting will be applied on boot, the current session continues using the old value until reloading the settings. To immediately apply your change, run:

   ```bash theme={null}
   $ sudo sysctl -p /etc/sysctl.d/swap-less.conf
   ```

<Callout icon="lightbulb">
  Editing kernel parameters in `/etc/sysctl.conf` is an alternative, though this file may be overwritten during system upgrades. It is recommended to use `/etc/sysctl.d` for persistent customizations.
</Callout>

## Summary Table

| Configuration Scope | Change Method                     | Example Command                                                     |
| ------------------- | --------------------------------- | ------------------------------------------------------------------- |
| Non-Persistent      | Temporary setting change          | sudo sysctl -w net.ipv6.conf.default.disable\_ipv6=1                |
| Persistent          | Create conf file in /etc/sysctl.d | sudo vim /etc/sysctl.d/swap-less.conf <br /> (add vm.swappiness=20) |

With these techniques, you can modify kernel runtime parameters for your Linux system effectively—using both non-persistent methods for immediate changes and persistent methods for settings that survive reboots. For further details on Linux kernel parameters, consider browsing related documentation provided by your Linux distribution or the official [Linux Kernel Documentation](https://www.kernel.org/doc/html/latest/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-foundation-certified-system-administrator-lfcs/module/cb813f7f-73bd-40ee-a088-d31ba20c51de/lesson/42afda02-1c10-4a8c-9069-a54b3ee2c18b" />
</CardGroup>
