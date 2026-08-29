# For details see man 4 crontabs
# Example of job definition:
# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12) OR jan,feb,mar,apr ...
# │ │ │ │ ┌───────────── day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# │ │ │ │ │
# * * * * * user-name  command to be executed
```

Notice the `MAILTO` setting, which directs the output of cron jobs to the specified user (in this example, root). This ensures that the results of cron jobs are mailed, providing an additional layer of monitoring.

## Verifying Anacron Jobs

Anacron is designed to schedule jobs on daily, weekly, or monthly intervals and ensures that they are executed even if the system was off at the scheduled time. Inspect the anacrontab configuration with:

```bash theme={null}
sudo vi /etc/anacrontab
```

You should see content similar to:

```bash theme={null}
# /etc/anacrontab: configuration file for anacron
# See anacron(8) and anacrontab(5) for details.
SHELL=/bin/sh
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root
# the maximal random delay added to the base delay of the jobs
RANDOM_DELAY=45
# the jobs will be started during the following hours only
START_HOURS_RANGE=3-22

# period in days    delay in minutes    job-identifier    command
1                5                      cron.daily        nice run-parts /etc/cron.daily
7                25                     cron.weekly       nice run-parts /etc/cron.weekly
@monthly        45                     cron.monthly      nice run-parts /etc/cron.monthly
1                10                     test_job         /bin/echo "Testing anacron"
```

The `MAILTO` directive ensures that the output for each job, such as `test_job`, is sent to the specified email recipient. Since waiting a full day for testing isn’t practical, you can manually trigger anacron jobs with:

```bash theme={null}
sudo anacron -n
```

To focus on anacron-specific log messages, filter the cron log with:

```bash theme={null}
sudo grep anacron /var/log/cron
```

For example, you'll see log entries like:

```bash theme={null}
Mar 24 01:15:27 LFCS-CentOS anacron[8903]: Job `test_job` started
Mar 24 01:15:27 LFCS-CentOS anacron[8903]: Job `test_job` terminated (produced output)
```

If you need logs exclusively for `test_job`, further filter by:

```bash theme={null}
sudo grep test_job /var/log/cron
```

### Enhancing Test Job Logging for Anacron

To capture command output from an anacron job more clearly, modify the job command to pipe its output to `systemd-cat` with a custom identifier. Edit `/etc/anacrontab`:

```bash theme={null}
sudo vi /etc/anacrontab
```

Update the `test_job` line as follows:

```bash theme={null}
1       10          test_job         /bin/echo "Testing anacron" | systemd-cat --identifier=test_job
```

After saving your changes, force anacron to run all jobs irrespective of their previous status using:

```bash theme={null}
sudo anacron -n -f
```

Then, view the system log to find the output:

```bash theme={null}
journalctl -e
```

You should see entries similar to:

```text theme={null}
Mar 24 01:19:38 LFCS-CentOS anacron[9869]: Job `test_job' started
Mar 24 01:19:38 LFCS-CentOS test_job[9887]: Testing anacron
Mar 24 01:19:38 LFCS-CentOS anacron[9869]: Job `test_job' terminated
```

Once you finish testing, remember to remove or comment out the modified logging command if it is no longer required.

## Verifying at Jobs

The `at` command schedules one-time jobs. To schedule a job to run in one minute, enter:

```bash theme={null}
at 'now + 1 minute'
```

After this command, you will be prompted to enter the command you wish to run. For example:

```bash theme={null}
echo "My at job produced this output"
```

Press Control-D (Ctrl+D) to signal the end of input. The system will display a message like:

```text theme={null}
job 4 at Thu Mar 24 01:22:00 2022
```

To view the at job log entries:

```bash theme={null}
sudo grep atd /var/log/cron
```

You should see log lines indicating the start of the job, for example:

```text theme={null}
Mar 24 01:04:00 LFCS-CentOS atd[9079]: Starting job 2 (a0000201a3224c) for user 'aaron' (1000)
Mar 24 01:07:00 LFCS-CentOS atd[9319]: Starting job 3 (a0000301a3224f) for user 'aaron' (1000)
```

Keep in mind that the default logging for at jobs does not capture the command output. To log the output, schedule an at job by piping its output to `systemd-cat`:

```bash theme={null}
at 'now + 1 minute'
```

Then, when prompted, enter:

```bash theme={null}
echo "My at job produced this output" | systemd-cat --identifier=at_scheduled_backup
```

Once the job executes, review the log output with:

```bash theme={null}
journalctl | grep at_scheduled_backup
```

Depending on your system settings, you might also find relevant messages in `/var/log/messages` or `/var/log/syslog`.

## Conclusion

This guide has detailed how to verify the successful execution of scheduled jobs using cron, anacron, and at on CentOS Stream 8. By examining log files and, when necessary, modifying your job commands to capture their output, you can ensure that your scheduled processes are running correctly and troubleshoot issues as they arise.

For further queries and comprehensive documentation on cron, anacron, or at scheduling, you might want to visit the [CentOS Documentation](https://www.centos.org/docs/).

Thank you for reading, and please proceed to the next section for additional demonstrations and related topics.

- [Watch Video](https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/736506db-a70d-463d-a061-74c768d309b0/lesson/932ac452-6ea8-4fe9-8416-6e1a3903265f)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/736506db-a70d-463d-a061-74c768d309b0/lesson/f2c537b4-1787-4f9e-9f03-578aa7f0b98e)


# Work with package module streams

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Deploy-Configure-and-Maintain-Systems/Work-with-package-module-streams/page

Learn to manage packaged module streams in RHEL 8 for greater software version flexibility and compatibility.

In this lesson, you'll learn how to manage packaged module streams in RHEL 8. Application streams (or app streams) allow you to select from multiple versions of software packages grouped as modules, offering greater flexibility and compatibility for your environment.

A module is a collection of packages that are typically installed together, while a profile is a subset of that module tailored for a specific purpose—for example, server configuration, client setup, or development environment. Module streams can be active (enabled) or inactive (disabled), and only one version of a module stream can be active at any given time. This setup ensures that only the designated version of a package and its dependencies are installed, with the YUM package manager handling all dependencies automatically.

> **lightbulb** If you ever need to verify which modules are available or currently active, the YUM package manager provides commands to list module streams and their profiles.

## Viewing Available Modules

To display all available module streams, run the following command:

```bash theme={null}
sudo yum module list
```

The output will look similar to this:

```text theme={null}
Extra Packages for Enterprise Linux Modular 8 - x86_64
Name    Stream    Profiles        Summary
nginx   mainline  common          [ nginx webserver]
nginx   1.20     common          [ nginx webserver]
nodejs  13       default,        Javascript runtime
                develop
                minimal
nodejs  16-epel default,        Javascript runtime
                develop
                minimal
```

## Detailed Module Information and Installation

For more detailed information about a specific module, you can search within its listings. For instance, the Node.js module may list several versions (such as 10, 12, 14, and 16). By default, installing Node.js without specifying a version will install version 10 with the common profile.

To install a specific version with a designated profile—for example, Node.js version 14 using the development profile—execute:

```bash theme={null}
sudo yum module install nodejs:14/development
```

After installation, you can confirm the active module stream and its profiles by running:

```bash theme={null}
sudo yum module list --installed nodejs
```

The output should indicate that Node.js version 14 is active, similar to the following:

```text theme={null}
Name              Stream      Profiles                       Summary
nodejs            14 [e]     common [d], development [i], minimal, s2i
Hint: [d]efault, [e]nabled, [x]disabled, [i]ninstalled
```

## Resetting Module Streams

If you need to revert to the default module settings—for example, to switch back to Node.js version 10 with the common profile—you can use the reset command:

```bash theme={null}
sudo yum module reset nodejs
```

Once reset, you can install a different version (such as version 16 with the development profile) if needed. This modular approach simplifies the process of switching between different package versions to suit your current requirements.

> **lightbulb** This lesson covered how to view available modules, install a specific module stream with a chosen profile, and reset module streams in RHEL 8 using the YUM package manager.

- [Watch Video](https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/736506db-a70d-463d-a061-74c768d309b0/lesson/6a7fcbd3-681c-41a6-8d4c-2465a85141b4)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/736506db-a70d-463d-a061-74c768d309b0/lesson/2d44ca62-2a64-4588-8755-8a8ebcb91421)
