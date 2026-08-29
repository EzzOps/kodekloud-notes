# Cronjobs

Source: https://notes.kodekloud.com/docs/Learning-Linux-Basics-Course-Labs/Security-and-File-Permissions/Cronjobs/page

Learn to schedule tasks in Linux using Cron for efficient and reliable system maintenance.

In this article, you’ll learn how to schedule tasks in Linux using Cron. Cron allows you to automate commands by specifying the date, time, and frequency for execution. Once configured, the cron daemon runs the task without human intervention, making your system maintenance efficient and reliable.

Consider a practical example: Michael needs to run the command `uptime` and redirect its output to the file `/tmp/system-report.txt` every day at 9 p.m. Running the command manually can be tedious, so a Cron job automates this process. The command to append the output is:

```bash theme={null}
uptime >> /tmp/system-report.txt
```

## Scheduling a Cron Job

To schedule this task, log in as Michael and edit Michael’s crontab:

```bash theme={null}
[michael@caleston-lp01 ~]$ crontab -e
```

This command opens the crontab file in the default editor (typically VI). At the bottom of the file, add the following Cron job configuration:

```bash theme={null}
0 21 * * * uptime >> /tmp/system-report.txt
```

The first five fields specify the schedule:

* **Minute (0):** The task runs at the 0th minute.
* **Hour (21):** The task runs at 9 p.m. (21:00 in 24-hour format).
* **Day of Month (\*):** Every day of the month.
* **Month (\*):** Every month.
* **Day of Week (\*):** Every day of the week.

<Callout icon="lightbulb">
  Avoid using `sudo` with the `crontab` command if you intend the task to run as Michael; using `sudo` would schedule the job for the root user.
</Callout>

## Understanding Cron Syntax

Here are some examples to help you better understand the scheduling syntax:

* **Run a job on February 19th at 8:10:**

  ```bash theme={null}
  10 8 19 2 *
  ```

* **Run a job on February 19th at 8:10 only if it’s a Monday** (where 1 represents Monday):

  ```bash theme={null}
  10 8 19 2 1
  ```

* **Run a job every day at 8:10:**

  ```bash theme={null}
  10 8 * * *
  ```

* **Run a job every minute of every hour on all days:**

  ```bash theme={null}
  * * * * *
  ```

* **Run a job every two minutes using step values:**

  ```bash theme={null}
  */2 * * * *
  ```

For a quick reference, here is the format of a crontab entry:

```bash theme={null}
