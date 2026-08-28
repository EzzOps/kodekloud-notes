# Boot reboot and shutdown a system safely

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/Operation-of-Running-Systems/Boot-reboot-and-shutdown-a-system-safely/page

This guide covers managing Linux system power states, including rebooting, shutting down, forcing operations, scheduling, and notifying users.

Managing a Linux system’s power state correctly ensures data integrity and gives users time to save work before the machine goes offline. In this guide, you’ll learn how to:

* Reboot or power off immediately with `systemctl`
* Force a reset when the system is unresponsive
* Schedule shutdowns or reboots with `shutdown`
* Notify logged-in users in advance

***

## 1. Managing System States with systemctl

Most modern Linux distributions use systemd, and `systemctl` is the primary tool to control power states.

<Callout icon="lightbulb">
  All `systemctl` commands require root privileges. Prepend `sudo` if you’re not running as root.
</Callout>

| Action        | As Root                | As Non-Root User            |
| ------------- | ---------------------- | --------------------------- |
| Reboot now    | `# systemctl reboot`   | `$ sudo systemctl reboot`   |
| Power off now | `# systemctl poweroff` | `$ sudo systemctl poweroff` |

### Reboot

```bash theme={null}
