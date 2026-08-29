# Schedule Tasks to Run at a Set Date and Time

Source: https://notes.kodekloud.com/docs/Prep-Course-Linux-Foundation-Certified-System-Administrator-LFCS-Certification/Operations-Deployment/Schedule-Tasks-to-Run-at-a-Set-Date-and-Time/page

This article explores scheduling tasks on Linux systems using Cron, Anacron, and At utilities for automation and system maintenance.

In this article, we explore how to schedule tasks to run at specified times on Linux systems. Automating tasks such as database backups every Sunday at 3:00 AM is crucial for consistent system maintenance. There are three primary tools available for task scheduling:

1. Cron Utility
2. Anacron
3. At Utility

Below, we detail how each tool works and how to configure them for your needs.

***

## Cron Utility

Cron is best suited for repetitive tasks that run at regular intervals—whether every few minutes, specific hours, days, or even months.

The basic syntax for a cron job consists of five time-and-date fields followed by the command to be executed. When editing the system-wide cron table (found at `/etc/crontab`), a username field is included. The time fields are as follows:

* Minute (0–59)
* Hour (0–23)
* Day of the month (1–31)
* Month (1–12)
* Day of the week (0–6, where 0 or 7 denotes Sunday)

You can use special characters in these fields:

* Asterisk (\*) denotes every possible value.
* Comma (,) separates multiple values. For example, "15,45" in the minute field runs the job at minute 15 and 45.
* Dash (-) specifies a range (e.g., "2-4" in the hour field).
* Slash (/) defines steps. For example, "\*/4" in the hour field indicates every 4 hours, and "0-8/4" represents 0 AM, 4 AM, and 8 AM.

The default system-wide cron table, located at `/etc/crontab`, usually includes explanatory comments. Below is a sample excerpt:

![The image illustrates a server setup for automated tasks, specifically a database backup every Sunday at 3:00 AM, using Cron, Anacron, and "at" for scheduling.](https://kodekloud.com/kk-media/image/upload/v1752881353/notes-assets/images/Linux-Foundation-Certified-System-Administrator-LFCS-Schedule-Tasks-to-Run-at-a-Set-Date-and-Time/server-setup-automated-backup-schedule.jpg)

```bash theme={null}
$ cat /etc/crontab
SHELL=/bin/sh
