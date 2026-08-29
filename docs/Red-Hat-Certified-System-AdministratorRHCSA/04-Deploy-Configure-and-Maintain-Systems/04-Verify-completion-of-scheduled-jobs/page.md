# Example of job definition:
# --------------------------- minute (0 - 59)
# | ------------------------- hour (0 - 23)
# | | ----------------------- day of month (1 - 31)
# | | | --------------------- month (1 - 12) OR jan,feb,mar,apr ...
# | | | | ------------------- day of week (0 - 6) (Sunday=0 or 7) OR
# sun,mon,tue,wed,thu,fri,sat
# | | | | |
# * * * * * user-name  command to be executed
35 6 * * * root /bin/some_command --some_options
```

In a cron job, the first five fields define the schedule:

* **Minute:** 0–59
* **Hour:** 0–23 (0 indicates midnight, 23 indicates 11 PM)
* **Day of the Month:** 1–31
* **Month:** 1–12 (or short month names such as jan, feb, etc.)
* **Day of the Week:** 0–6 (0 or 7 represents Sunday; short names are also allowed, e.g., mon, tue)

You can modify these fields using special characters:

* An asterisk (\*) represents all possible values.
* A comma (,) separates multiple values.
* A dash (-) specifies a range (e.g., “2-4” means 2, 3, and 4).
* A slash (/) represents step values, for example, “\*/4” runs every 4 units.

For example, to run a job at hours 0, 4, and 8 (every hour from midnight to 8 AM), you can use the format “0-8/4” for the hour field.

### Editing a User's Crontab

Instead of editing the system-wide crontab, you should update your personal crontab. To do so, run:

```bash theme={null}
$ crontab -e
```

Before adding commands, always confirm you are using full paths. To locate the full path for the `touch` command:

```bash theme={null}
$ which touch
/usr/bin/touch
```

Now, to schedule the `touch` command to run daily at 6:35 A.M. and create a file named `test_passed`, include this line in your personal crontab (note that there is no username for user-specific crontabs):

```bash theme={null}
35 6 * * * /usr/bin/touch test_passed
```

Below are additional examples of cron entries:

```bash theme={null}
$ crontab -e
35 6 * * * /usr/bin/touch test_passed          # Daily at 6:35 AM
0 3 * * 0 /usr/bin/touch test_passed             # Every Sunday at 3:00 AM
0 3 * * 7 /usr/bin/touch test_passed             # Also every Sunday at 3:00 AM (alternate notation)
0 3 15 * * /usr/bin/touch test_passed            # On the 15th of every month at 3:00 AM
0 3 * * * /usr/bin/touch test_passed             # Every day at 3:00 AM
0 * * * * /usr/bin/touch test_passed             # At the start of every hour
```

To view your current crontab entries:

```bash theme={null}
$ crontab -l
35 6 * * * /usr/bin/touch aaron_test
```

For root user's crontab entries, prefix the command with `sudo`:

```bash theme={null}
$ sudo crontab -l
0 * * * * /usr/bin/touch root_test
```

To modify or delete another user's crontab (for example, user Jane), use the `-u` option combined with sudo:

```bash theme={null}
$ sudo crontab -e -u jane
$ sudo crontab -r -u jane
```

### Using Special Cron Directories

Cron also provides job scheduling using special directories:

* `/etc/cron.daily`
* `/etc/cron.hourly`
* `/etc/cron.weekly`
* `/etc/cron.monthly`

Any executable script placed into one of these directories will run at the associated interval.

For example, to schedule a shell script to run hourly:

1. Create the script:

   ```bash theme={null}
   $ touch shellscript
   ```

2. Copy it to the hourly directory with root privileges:

   ```bash theme={null}
   $ sudo cp shellscript /etc/cron.hourly/
   ```

3. Set the correct permissions for execution:

   ```bash theme={null}
   $ sudo chmod +rx /etc/cron.hourly/shellscript
   ```

4. To remove this scheduled job, simply delete the script:

   ```bash theme={null}
   $ sudo rm /etc/cron.hourly/shellscript
   ```

<Callout icon="lightbulb">
  Always use full paths in your cron jobs to prevent issues related to the environment's PATH variable.
</Callout>

***

## Anacron

Anacron is built for tasks that need to run on a daily, weekly, or monthly basis—even if the computer was off at the scheduled time. Unlike Cron, Anacron's smallest time unit is one day. This means if a scheduled job is missed (for example, if the computer was off at noon), it will execute as soon as possible after the system restarts.

To schedule a task with Anacron, you need to update the Anacrontab file. Open it with your favorite text editor:

```bash theme={null}
$ sudo vim /etc/anacrontab
#period in days  delay in minutes    job-identifier    command
1       5       cron.daily            nice run-parts
7       25      cron.weekly           nice run-parts
@monthly 45     cron.monthly          nice run-parts /etc/cron.monthly
```

Each entry consists of:

* The period (in days) between executions.
* The delay (in minutes) after the system starts before running the job.
* A unique identifier for the job.
* The exact command to run (always use full paths).

For instance, to schedule a job every 3 days with a 10-minute delay:

```bash theme={null}
$ sudo vim /etc/anacrontab
#period in days    delay in minutes    job-identifier    command
1                   5                   cron.daily        nice run-parts
7                   25                  cron.weekly       nice run-parts
@monthly            45                  cron.monthly      nice run-parts /etc/cron.monthly
3                   10                  test_job          /usr/bin/touch /root/anacron_created_this
```

<Callout icon="triangle-alert">
  If multiple jobs are due at the same time, assign different delays to prevent system overload.
</Callout>

You can also test your Anacrontab syntax with the `-T` option. A lack of error messages indicates a correct configuration.

***

## At

The At command is suited for one-off tasks that need to run at a specific time or after a given interval. When scheduling a job with At, always use the 24-hour format.

### Scheduling a Job with At

To schedule a job at a specific time, follow these steps:

1. Start by entering the at command:

   ```bash theme={null}
   $ at 15:00
   warning: commands will be executed using /bin/sh
   at>
   ```

2. Enter the command you want to execute (ensure you use the full path):

   ```bash theme={null}
   at> /usr/bin/touch file_created_by_at
   ```

3. Press Enter on an empty line and then press Control-D to save the job.

At can also schedule jobs for specific dates and relative times:

```bash theme={null}
$ at 'August 20 2022'
$ at '2:30 August 20 2022'
$ at 'now + 30 minutes'
$ at 'now + 3 hours'
$ at 'now + 3 days'
$ at 'now + 3 weeks'
$ at 'now + 3 months'
```

### Managing At Jobs

To review scheduled At jobs, use:

```bash theme={null}
$ atq
20      Wed Nov 17 08:30:00 2021 a aaron
```

The number (e.g., 20) is the job ID. To inspect the contents of a specific job:

```bash theme={null}
$ at -c 20
LESSOPEN=||/usr/bin/lesspipe.sh %s; export LESSOPEN
cd /home/aaron || {
        echo 'Execution directory inaccessible' >&2
        exit 1
}
${SHELL:-/bin/sh} << 'marcinDELIMITER1d46213b'
command1
command2
marcinDELIMITER1d46213b
```

To remove a scheduled job, use the job ID with the atrm command:

```bash theme={null}
$ atrm 20
```

***

This concludes our comprehensive guide on scheduling tasks in Linux using Cron, Anacron, and At. Apply these techniques to automate your system tasks and enhance your operational efficiency.

For further reading, check out these resources:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/736506db-a70d-463d-a061-74c768d309b0/lesson/56a5ebd4-db34-4acb-b679-89ac2b3de9b0" />
</CardGroup>


# Verify completion of scheduled jobs

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Deploy-Configure-and-Maintain-Systems/Verify-completion-of-scheduled-jobs/page

This guide explains how to verify the completion of scheduled jobs on CentOS Stream 8 using cron, anacron, and at commands.

Welcome to our detailed guide on verifying the completion of scheduled jobs on CentOS Stream 8. By default, this operating system logs all events generated by cron, anacron, and at. This guide will show you how to confirm that your scheduled jobs are executing correctly.

<Callout icon="lightbulb">
  CentOS Stream 8 logs provide detailed information including command output, which can be extremely useful for troubleshooting and ensuring that your tasks run as expected.
</Callout>

## Verifying Cron Jobs

Begin by reviewing your user-specific crontab. To open your crontab for editing, run:

```bash theme={null}
crontab -e
```

In this example, two commands have been added to the crontab, scheduled to run every minute:

```bash theme={null}
* * * * * /bin/echo "Just testing cron"
* * * * * /bin/echo "Just testing cron again"
```

These commands output their respective messages every minute. After adding these jobs, wait at least one minute before checking the logs. To view cron log entries, execute:

```bash theme={null}
sudo cat /var/log/cron
```

You should see log entries resembling the following:

```bash theme={null}
Mar 24 01:06:01 LFCS-CentOS CROND[9265]: (aaron) CMD (/bin/echo "Just testing cron again")
Mar 24 01:07:02 LFCS-CentOS CROND[9347]: (aaron) CMD (/bin/echo "Just testing cron again")
...
```

These log entries display the execution time, command details, and output. If you wish to view only executed command logs, filter the logs using:

```bash theme={null}
sudo grep CMD /var/log/cron
```

When you are finished testing or need to remove the current crontab settings, clear them with:

```bash theme={null}
crontab -r
```

## Reviewing the System-Wide Crontab

The system-wide crontab is a useful reference for understanding cron syntax and configuration. To view its content, run:

```bash theme={null}
cat /etc/crontab
```

You will see content similar to this:

```bash theme={null}
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root
