# Example crontab entries (run every minute)
* * * * * /bin/echo "Just testing cron"
* * * * * /bin/echo "Just testing cron again"
```

Cron records job execution events in /var/log/cron. The log lines include the literal "CMD" for executed commands, making it easy to filter for executions:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ sudo grep 'CMD' /var/log/cron
Mar 24 01:05:01 LFCS-CentOS CROND[9203]: (aaron) CMD (/bin/echo "Just testing cron")
Mar 24 01:05:01 LFCS-CentOS CROND[9204]: (aaron) CMD (/bin/echo "Just testing cron again")
Mar 24 01:06:01 LFCS-CentOS CROND[9264]: (aaron) CMD (/bin/echo "Just testing cron")
Mar 24 01:06:01 LFCS-CentOS CROND[9265]: (aaron) CMD (/bin/echo "Just testing cron again")
Mar 24 01:07:02 LFCS-CentOS CROND[9347]: (aaron) CMD (/bin/echo "Just testing cron again")
Mar 24 01:07:02 LFCS-CentOS CROND[9348]: (aaron) CMD (/bin/echo "Just testing cron")
...
```

Note: Some systems include the command output in the logs under keys like "CMDOUT" or similar. If you expect output from a cron job, search /var/log/cron for CMDOUT or query the journal with journalctl.

When finished testing, remove the user crontab entry:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ crontab -r
```

## System-wide crontab (/etc/crontab)

The system-wide crontab at /etc/crontab sets environment variables and shows the expected syntax (including the user field). It also contains MAILTO, which cron/anacron uses to email job output if system mail is configured:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ cat /etc/crontab
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# * * * * *  user-name  command to be executed
```

## Anacron — for machines not running 24/7

Anacron is designed for systems that may be powered off periodically. Jobs use a named identifier, which simplifies searching logs. Example /etc/anacrontab:

```bash theme={null}
# /etc/anacrontab: configuration file for anacron
SHELL=/bin/sh
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root
RANDOM_DELAY=45
START_HOURS_RANGE=3-22

# period in days  delay in minutes  job-identifier  command
1       5        cron.daily       nice run-parts /etc/cron.daily
7       25       cron.weekly      nice run-parts /etc/cron.weekly
@monthly 45      cron.monthly     nice run-parts /etc/cron.monthly
1       10       test_job         /bin/echo "Testing anacron"
```

To run anacron jobs immediately (suppress random delay), use:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ sudo anacron -n
```

Force execution regardless of last-run timestamps with -f:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ sudo anacron -n -f
```

Anacron logs show start/stop events in /var/log/cron, but they typically only note that output was produced rather than including the full stdout. Example:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ sudo grep anacron /var/log/cron
Mar 24 01:01:01 LFCS-CentOS anacron[8903]: Anacron started on 2022-03-24
Mar 24 01:01:01 LFCS-CentOS anacron[8903]: Will run job `test_job' in 12 min.
Mar 24 01:13:01 LFCS-CentOS anacron[8903]: Job `test_job' started
Mar 24 01:13:01 LFCS-CentOS anacron[8903]: Job `test_job' terminated (produced output)
Mar 24 01:13:01 LFCS-CentOS anacron[8903]: Normal exit (1 job run)
```

Capture anacron job output in the systemd journal by piping to systemd-cat. Edit the job entry:

```bash theme={null}
1 10 test_job /bin/echo "Testing anacron" | systemd-cat --identifier=test_job
```

Force anacron to run and then inspect the journal:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ sudo anacron -n -f
[aaron@LFCS-CentOS ~]$ journalctl -e | grep test_job -C3
Mar 24 01:19:38 LFCS-CentOS anacron[9869]: Job `test_job' started
Mar 24 01:19:38 LFCS-CentOS test_job[9887]: Testing anacron
Mar 24 01:19:38 LFCS-CentOS anacron[9869]: Job `test_job' terminated
```

Remember to remove any temporary test entries from /etc/anacrontab after testing.

## at (one-off scheduled jobs)

at schedules one-time jobs. To schedule a job to run in one minute and capture its output to the journal:

1. Create the at job; after entering your commands finish with Ctrl-D:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ at 'now + 1 minute'
warning: commands will be executed using /bin/sh
at> echo "My at job produced this output" | systemd-cat --identifier=at_scheduled_backup
at> <Ctrl-D>
job 4 at Thu Mar 24 01:22:00 2022
```

The at daemon logs job starts to /var/log/cron:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ sudo grep atd /var/log/cron
Mar 24 01:04:00 LFCS-CentOS atd[9079]: Starting job 2 (a0000201a3224c) for user 'aaron' (1000)
Mar 24 01:07:00 LFCS-CentOS atd[9319]: Starting job 3 (a0000301a3224f) for user 'aaron' (1000)
```

Because we piped the job to systemd-cat, its output appears in the journal:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ journalctl | grep at_scheduled_backup
Mar 24 01:07:00 LFCS-CentOS at_scheduled_backup[9326]: My at job produced this output
Mar 24 01:23:14 LFCS-CentOS at_scheduled_backup[10028]: My at job produced this output
```

## Quick comparison: cron, anacron, and at

| Scheduler                | Typical use case                                  | Where to check                | Captures stdout by default?                        |
| ------------------------ | ------------------------------------------------- | ----------------------------- | -------------------------------------------------- |
| cron (per-user & system) | Regular, recurring jobs on always-on systems      | /var/log/cron (or journalctl) | Sometimes (depends on config); logs CMD lines      |
| anacron                  | Jobs on systems that are periodically powered off | /var/log/cron and journalctl  | Logs events; pipe to systemd-cat to capture stdout |
| at                       | One-off, ad-hoc jobs                              | /var/log/cron and journalctl  | Pipe to systemd-cat to capture stdout              |

## Practical tips

* Use journalctl to search by custom identifiers when you pipe output through systemd-cat.
* If your distribution doesn’t use /var/log/cron, check /var/log/messages or /var/log/syslog, or query the journal directly.
* Configure MAILTO in /etc/crontab or per-user crontab if you have local mail delivery enabled and prefer email notifications for output.

<Callout icon="lightbulb">
  On some distributions, scheduled-job messages are recorded in /var/log/messages or /var/log/syslog instead of /var/log/cron. If you don't find entries in /var/log/cron, search those files or use journalctl to query the systemd journal.
</Callout>

## Summary

* Check /var/log/cron for CROND/CMD messages to verify cron job execution.
* Anacron reports job starts/stops; to capture output, pipe the job to systemd-cat and then inspect journalctl.
* at logs job starts in the system logs; use systemd-cat to capture output into the journal when needed.
* Use MAILTO for email delivery of job outputs if you have the mail system configured.

Links and references

* [cron man page](https://man7.org/linux/man-pages/man5/crontab.5.html)
* [anacron documentation](https://man7.org/linux/man-pages/man8/anacron.8.html)
* [systemd-cat and journalctl](https://www.freedesktop.org/software/systemd/man/systemd-cat.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/ca5e9d7c-9dac-4ecc-9e21-dafef5ef2641/lesson/ba0f4b36-8642-44b2-9c0d-36272ae0319f" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/ca5e9d7c-9dac-4ecc-9e21-dafef5ef2641/lesson/ded19bd0-d9b1-4d02-9b28-401f88d30ad2" />
</CardGroup>


# Verify the integrity and availability of resources

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/Operation-of-Running-Systems/Verify-the-integrity-and-availability-of-resources/page

This guide teaches monitoring and verifying the integrity of key resources on Linux servers, including disk usage, memory, CPU statistics, and service health checks.

In this guide, you’ll learn how to monitor and verify the integrity of key resources on Linux servers. We cover disk and directory usage, memory and CPU statistics, file system repair (XFS and ext4), and service health checks.

## Disk Space Usage

Over time, server storage fills up as applications grow and users store more data. Use `df` to inspect overall disk usage:

```bash theme={null}
