# You can also override PATH; by default, newer versions inherit it.
# Example of job definition:
# ----------- minute (0 - 59)
# ----------- hour (0 - 23)
# ----------- day of month (1 - 31)
# ----------- month (1 - 12) OR jan,feb,mar,apr ...
# ----------- day of week (0 - 6) (Sunday=0 or 7) OR
#               sun,mon,tue,wed,thu,fri,sat
# * * * * * user-name command to be executed
35 6 * * * root /bin/some_command --some_options
```

<Callout icon="lightbulb">
  When modifying the system-wide cron file, be aware that package updates may overwrite your changes. It is generally safer to add cron jobs using the user's personal cron table.
</Callout>

To edit your personal cron table, run:

```bash theme={null}
$ crontab -e
```

In your personal cron table, the username is not required because the job inherits your current privileges. For example, if you want to create a file named `test_path` every day at 6:35 AM using the `touch` command, first determine its full path:

```bash theme={null}
$ which touch
/usr/bin/touch
```

Then, add the following line using `crontab -e`:

```bash theme={null}
35 6 * * * /usr/bin/touch test_path
```

Save and exit the editor to schedule the job.

Below are additional examples for scheduling tasks:

```bash theme={null}
$ which touch
/usr/bin/touch

$ crontab -e
35 6 * * * /usr/bin/touch test_passed            # Every day at 6:35 AM
0 3 * * 0 /usr/bin/touch test_passed              # Every Sunday at 3:00 AM
0 3 * * 7 /usr/bin/touch test_passed              # Alternative notation for Sunday
0 3 15 * * /usr/bin/touch test_passed             # On the 15th of every month at 3:00 AM
```

To run a command every day at 3:00 AM or at the top of every hour (when the minute is 00), adjust the timing fields as needed.

For further testing of your cron expressions, visit [crontab.guru](http://www.crontab.guru).

To list your current cron jobs, use:

```bash theme={null}
$ crontab -l
35 6 * * * /usr/bin/touch aaron_test
```

To view or edit other users' cron jobs (e.g., root or another user), use `sudo`:

```bash theme={null}
$ sudo crontab -l
0 * * * * /usr/bin/touch root_test

$ sudo crontab -e -u jane
30 * * * * /usr/bin/touch jane_test
```

If you need to remove a user's cron jobs entirely, use the `-r` option:

```bash theme={null}
$ crontab -r
$ sudo crontab -r -u jane
```

An alternative to adding jobs to the cron table directly is by placing scripts into specific directories, such as `/etc/cron.daily`, `/etc/cron.hourly`, `/etc/cron.weekly`, or `/etc/cron.monthly`. For instance, to schedule a shell script named `shellscript` to run hourly:

```bash theme={null}
$ touch shellscript
$ sudo cp shellscript /etc/cron.hourly/
```

Make sure the script is both readable and executable. To remove it, simply delete the file from the directory.

***

## Anacron

Anacron is designed for tasks that need to run periodically (daily, weekly, monthly) on systems that are not continuously powered on. If a scheduled cron task is missed because the system is off, anacron will run the task once the system is available.

On many systems, anacron is pre-installed. If not, install it with:

```bash theme={null}
$ sudo apt install anacron
```

Anacron's configuration is in the `/etc/anacrontab` file, which includes helpful comments and examples. Here’s an excerpt:

```bash theme={null}
$ sudo vim /etc/anacrontab
# See anacron(8) and anacrontab(5) for details.
# These entries replace cron's job entries.
1       5       cron.daily      run-parts --report /etc/cron.daily
7       10      cron.weekly     run-parts --report /etc/cron.weekly
@monthly 15      cron.monthly    run-parts --report /etc/cron.monthly
```

The syntax in the anacrontab file consists of four fields:

1. The period in days (e.g., 1 for daily, 7 for weekly).
2. A delay (in minutes) after system startup.
3. A unique job identifier.
4. The command to execute.

For example, to run a job every three days with a 10-minute delay:

```bash theme={null}
3 10 test_job /usr/bin/touch /root/anacron_created_this
```

Other examples include:

```crontab theme={null}
7 10 test_job /usr/bin/touch /root/anacron_created_this
@monthly 10 test_job /usr/bin/touch /root/anacron_created_this
```

After editing, verify your anacrontab syntax with:

```bash theme={null}
$ anacron -T
anacron: /etc/anacrontab: Unknown named period on line 13, skipping
```

If no errors are reported, your anacron entries are correctly formatted.

<Callout icon="lightbulb">
  For more detailed information on anacron, refer to the man pages by running:

  ```bash theme={null}
  $ man 5 anacrontab
  ```
</Callout>

***

## At Utility

The at utility is ideal for one-time task scheduling, rather than recurring jobs. If at is not already installed on your Ubuntu system, install it with:

```bash theme={null}
$ sudo apt install at
```

To schedule a job with at, specify the desired run time. For example, to run a job at 3:00 PM:

```bash theme={null}
$ at '15:00'
warning: commands will be executed using /bin/sh
at> /usr/bin/touch file_created_by_at
at> <CTRL-D>
```

You can also schedule jobs for specific dates or relative times. Some examples include:

```bash theme={null}
$ at 'August 20 2024'
$ at '2:30 August 20 2024'
$ at 'now + 30 minutes'
$ at 'now + 3 hours'
$ at 'now + 3 days'
$ at 'now + 3 weeks'
$ at 'now + 3 months'
```

To view scheduled at jobs, use:

```bash theme={null}
$ atq
1 Wed Mar  6 15:00:00 2024 a aaron
```

Here, the first number is the job ID. To inspect a job's details, use the `-c` option, similar to using `cat`. To remove a job, execute:

```bash theme={null}
$ atrm 1
```

<Callout icon="lightbulb">
  For more information on the at utility, refer to the [at documentation](https://linux.die.net/man/1/at).
</Callout>

***

Each of these tools—cron, anacron, and at—has its unique strengths. Cron excels for regular, recurring tasks; anacron ensures tasks are completed even if scheduled times are missed due to system downtime; and at is perfect for one-off commands.

By mastering these scheduling utilities, you can automate and manage tasks efficiently on your Linux system, ensuring a more resilient and well-maintained environment.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-foundation-certified-system-administrator-lfcs/module/cb813f7f-73bd-40ee-a088-d31ba20c51de/lesson/949118d4-a6f4-4db0-a22f-3ba4610fd59d" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/linux-foundation-certified-system-administrator-lfcs/module/cb813f7f-73bd-40ee-a088-d31ba20c51de/lesson/742878c9-6670-4182-9615-47af709f2218" />
</CardGroup>


# Use Scripting to Automate System Maintenance Tasks

Source: https://notes.kodekloud.com/docs/Prep-Course-Linux-Foundation-Certified-System-Administrator-LFCS-Certification/Operations-Deployment/Use-Scripting-to-Automate-System-Maintenance-Tasks/page

This article explores leveraging scripting to automate essential system maintenance tasks on Linux using bash scripting.

In this article, we explore how to leverage scripting to automate essential system maintenance tasks on Linux. By utilizing bash scripting, you can log system information, archive important data, and streamline routine maintenance operations.

When you log into a Linux system, you are immediately presented with a command-line interface. After a successful login, the bash shell starts, providing a text-based environment. Bash interprets every command you type, which is why it is also known as a command interpreter or shell.

An interactive bash session typically looks like this:

```bash theme={null}
[aaron@kodekcloud]$ date
Mon Dec  6 16:28:09 CST 2021
```

In interactive mode, you type commands, press Enter, and view the results instantly. However, bash can also execute scripts—files containing multiple commands that are executed sequentially.

──────────────────────────────

## Creating a Simple Script

Let's start by creating a basic script called script.sh. Although the ".sh" extension is optional, it helps identify the file as a script when browsing directories.

First, create and open the file for editing:

```bash theme={null}
$ touch script.sh
$ vim script.sh
```

Begin your script with the shebang line, which must be the very first line in the file without any leading spaces:

```bash theme={null}
#!/bin/bash
```

The shebang (#! followed by the interpreter's full path) specifies that bash should be used to execute the script.

Next, add a comment to document the purpose of the script. Comments start with a "#" and are ignored during execution:

```bash theme={null}
#!/bin/bash
