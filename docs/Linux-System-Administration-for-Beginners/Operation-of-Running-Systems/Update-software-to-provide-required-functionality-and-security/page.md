# /etc/crontab
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root

# ┌──────── minute (0 - 59)
# │ ┌────── hour (0 - 23)
# │ │ ┌──── day of month (1 - 31)
# │ │ │ ┌── month (1 - 12 or jan–dec)
# │ │ │ │ ┌ day of week (0 - 6 or sun–sat)
# │ │ │ │ │
35 6 * * * root /bin/some_command --some_options
```

### Field Descriptions

* **Minute**: `0–59`
* **Hour**: `0–23` (0 = midnight)
* **Day of Month**: `1–31`
* **Month**: `1–12` or `jan`–`dec`
* **Day of Week**: `0–6` (Sunday = 0 or 7) or `sun`–`sat`

Special operators:

* `*` : every valid value
* `,` : value list (e.g., `15,45`)
* `-` : range (e.g., `2-4`)
* `/` : step (e.g., `*/4` for every 4th unit)

<Callout icon="lightbulb">
  Always use full paths in your cron jobs. For example, find `touch` with `which touch` and use `/usr/bin/touch`.
</Callout>

### Edit Your User Crontab

1. Open the editor:
   ```bash theme={null}
   crontab -e
   ```
2. Add a job (runs daily at 06:35):
   ```cron theme={null}
   35 6 * * * /usr/bin/touch ~/test_passed
   ```

### Common cron Examples

* Every Sunday at 03:00:
  ```cron theme={null}
  0 3 * * sun /usr/bin/touch weekly_backup
  ```
* On the 15th of each month at 03:00:
  ```cron theme={null}
  0 3 15 * * /usr/bin/touch midmonth_task
  ```
* Daily at 03:00:
  ```cron theme={null}
  0 3 * * * /usr/bin/touch daily_task
  ```
* Hourly on the hour:
  ```cron theme={null}
  0 * * * * /usr/bin/touch hourly_task
  ```

### Managing crontabs

| Action                        | Command                       |
| ----------------------------- | ----------------------------- |
| List your crontab             | `crontab -l`                  |
| List root’s crontab           | `sudo crontab -l`             |
| Edit another user’s crontab   | `sudo crontab -u username -e` |
| Remove your crontab           | `crontab -r`                  |
| Remove another user’s crontab | `sudo crontab -u username -r` |

### `/etc/cron.*` Directories

Place scripts in these directories to run at fixed intervals:

* `/etc/cron.hourly/`
* `/etc/cron.daily/`
* `/etc/cron.weekly/`
* `/etc/cron.monthly/`

Example—install an hourly script:

```bash theme={null}
touch myscript.sh
sudo cp myscript.sh /etc/cron.hourly/
sudo chmod +x /etc/cron.hourly/myscript.sh
```

Remove it with:

```bash theme={null}
sudo rm /etc/cron.hourly/myscript.sh
```

## 2. anacron

When a system is off during a scheduled job, `anacron` runs missed tasks at boot. The file `/etc/anacrontab` uses this format:

```text theme={null}
# period days   delay minutes   job-identifier   command
1               5               cron.daily       nice run-parts /etc/cron.daily
7              25               cron.weekly      nice run-parts /etc/cron.weekly
@monthly       45               cron.monthly     nice run-parts /etc/cron.monthly
3              10               test_job         /usr/bin/touch /root/anacron_created_this
```

* **period days**: `1` = daily; `7` = weekly; `@monthly`
* **delay minutes**: wait before running
* **job-identifier**: unique name for logging
* **command**: full path to execute

Example: Runs `test_job` every 3 days, 10 minutes after boot.

Verify your configuration without executing jobs:

```bash theme={null}
sudo anacron -T
```

A silent output means the syntax is correct.

## 3. at

Use `at` for one-off tasks. Schedule in 24-hour or relative formats:

```bash theme={null}
# Schedule a one-time job at 15:00 today
at 15:00
# at> /usr/bin/touch file_created_by_at
# at> <Ctrl+D>
```

Supported time formats:

* Absolute: `at '2:30 Aug 20 2022'`
* Relative: `at 'now + 30 minutes'`
* Other: `at 'now + 3 days'`, `at 'now + 3 weeks'`, etc.

<Callout icon="triangle-alert">
  Ensure the `atd` daemon is running; otherwise `at` jobs won’t execute.
</Callout>

### Managing at Jobs

| Action            | Command              |
| ----------------- | -------------------- |
| List pending jobs | `atq`                |
| View job details  | `at -c <job-number>` |
| Remove a job      | `atrm <job-number>`  |

Example—list and remove:

```bash theme={null}
atq
atrm 20
```

***

Practice with these tools to automate backups, cleanup tasks, and custom scripts. Proper scheduling keeps your Linux system reliable and maintenance-free.

## Links & References

* [cron Manual Page](https://man7.org/linux/man-pages/man5/crontab.5.html)
* [anacron Documentation](https://man7.org/linux/man-pages/man5/anacrontab.5.html)
* [at Manual Page](https://man7.org/linux/man-pages/man1/at.1.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/ca5e9d7c-9dac-4ecc-9e21-dafef5ef2641/lesson/4e728479-499c-4899-b48c-ddc5384c394e" />
</CardGroup>


# Update software to provide required functionality and security

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/Operation-of-Running-Systems/Update-software-to-provide-required-functionality-and-security/page

This article explains how to use the DNF package manager on CentOS Stream to update software for security and functionality.

Keeping your Linux system up to date is critical—most online attacks exploit known vulnerabilities in outdated software. In this guide, you’ll learn how to use the DNF package manager on CentOS Stream (and other RHEL‐based distributions) to check for updates, apply upgrades, and reboot when necessary.

<Callout icon="lightbulb">
  Regular updates not only patch security holes but also introduce new features and performance improvements.
</Callout>

## Package Management with DNF

DNF (Dandified YUM) handles software installations, removals, and upgrades on CentOS Stream 8 and similar distributions. Before applying updates, always list the packages that have newer versions available.

### Checking for Available Updates

Run the following command to see which packages can be updated:

```bash theme={null}
dnf check-update
```

Sample output:

```bash theme={null}
CentOS Stream 8 - AppStream                         11 kB/s |  4.4 kB     00:00
CentOS Stream 8 - BaseOS                            14 kB/s |  3.9 kB     00:00
CentOS Stream 8 - Extras                            7.5 kB/s |  3.0 kB     00:00

Installing:
 kernel                          x86_64  4.18.0-348.2.1.el8_5   baseos   7.0 M
 kernel-devel                    x86_64  4.18.0-348.2.1.el8_5   baseos  20 M
 alsa-sof-firmware.noarch        1.9-1.el8                       baseos 
 bpftool.x86_64                  4.18.0-348.2.1.el8_5           baseos
 device-mapper.x86_64            8:1.02.181-1.el8                baseos

Obsoleting Packages
 kernel-headers.x86_64           4.18.0-348.2.1.el8_5            baseos
 kernel-headers.x86_64           4.18.0-348.el8                  @baseos
```

This output categorizes packages that will be installed, upgraded, or removed.

## Upgrading All Out‐of‐Date Packages

To perform a full system upgrade, use:

```bash theme={null}
sudo dnf upgrade
```

You’ll receive a transaction summary like this:

```bash theme={null}
Transaction Summary
================================================================================
 Install  4 Packages
 Upgrade  17 Packages

Total download size: 137 M
Is this ok [y/N]:
```

* **Install**: New dependencies required by updated packages
* **Upgrade**: Packages being replaced with newer versions

Type `y` and press Enter to proceed.

<Callout icon="triangle-alert">
  Pay attention to the download size and package count. Large upgrades on production servers may require scheduled maintenance windows.
</Callout>

## Reboot After Core Updates

Upgrading the kernel, system services, or libraries often requires a reboot. To apply these changes, reboot the system:

```bash theme={null}
sudo reboot
```

<Callout icon="lightbulb">
  Always verify critical services after rebooting to ensure they’ve started correctly.
</Callout>

## Summary of Common Commands

| Command            | Purpose                                  |
| ------------------ | ---------------------------------------- |
| `dnf check-update` | List all packages with available updates |
| `sudo dnf upgrade` | Upgrade every out‐of‐date package        |
| `sudo reboot`      | Restart the system to load core updates  |

## Links and References

* [CentOS Stream Documentation](https://docs.centos.org/en-US/stream/)
* [DNF Package Manager Guide](https://dnf.readthedocs.io/)
* [Linux Security Best Practices](https://www.kernel.org/doc/html/latest/admin-guide/security.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/ca5e9d7c-9dac-4ecc-9e21-dafef5ef2641/lesson/a06d2741-99f5-4523-b00e-f909c8ece853" />
</CardGroup>
