# Log the date and time of execution
date >> /tmp/script.log
# Capture the current kernel version
cat /proc/version >> /tmp/script.log
```

<Callout icon="lightbulb">
  The first line (`#!/bin/bash`) is the **shebang**, telling the system which interpreter to use.
</Callout>

* Lines beginning with `#` are comments.
* `>>` appends output rather than overwriting.

### 3. Make the Script Executable

```bash theme={null}
$ chmod u+x script.sh
# or allow everyone:
$ chmod +x script.sh
```

### 4. Run and Verify

```bash theme={null}
$ ./script.sh
$ cat /tmp/script.log
Mon Dec  6 17:06:16 CST 2021
Linux version 4.18.0-348.2.1.el8_5.x86_64 ...
```

***

## Automating Backups

Backup scripts are ideal for automating directory archiving. Below are two approaches: a simple archive and one that retains the previous generation.

### Archiving a Directory

Create `archive-dnf.sh`:

```bash theme={null}
#!/bin/bash
tar acf /tmp/archive.tar.gz /etc/dnf
```

```bash theme={null}
$ chmod +x archive-dnf.sh
$ ./archive-dnf.sh
$ ls /tmp
archive.tar.gz
```

You can inspect the archive with:

```bash theme={null}
tar tf /tmp/archive.tar.gz
```

***

### Keeping Two Generations of Backups

To avoid overwriting a good backup, rename the old archive before creating a new one.

1. Save this as `archive-dnf-2.sh`:

   ```bash theme={null}
   #!/bin/bash
   if test -f /tmp/archive.tar.gz; then
       mv /tmp/archive.tar.gz /tmp/archive.tar.gz.OLD
       tar acf /tmp/archive.tar.gz /etc/dnf
   else
       tar acf /tmp/archive.tar.gz /etc/dnf
   fi
   ```

2. Make it executable and run:

   ```bash theme={null}
   $ chmod +x archive-dnf-2.sh
   $ ./archive-dnf-2.sh
   $ ls /tmp
   archive.tar.gz
   archive.tar.gz.OLD
   ```

<Callout icon="triangle-alert">
  Moving or deleting files in `/tmp` can remove critical data if misused. Always verify paths and filenames before executing backup scripts.
</Callout>

***

## Using Exit Status in Conditions

Every command returns an **exit status**: `0` (success) or nonzero (failure). You can leverage this in `if` statements:

```bash theme={null}
#!/bin/bash
if grep -q '5' /etc/default/grub; then
    echo 'Grub has timeout of 5 seconds.'
else
    echo 'Grub DOES NOT have a timeout of 5 seconds.'
fi
```

* `grep -q` runs quietly (`-q`) and sets exit status accordingly.
* Save as `check-grub-timeout.sh`, make it executable, then:

```bash theme={null}
$ chmod +x check-grub-timeout.sh
$ ./check-grub-timeout.sh
Grub has timeout of 5 seconds.
```

***

## Real-World Example: Anacron

Inspect `/etc/cron.hourly/0anacron` to see conditionals, loops, and file checks in action:

```sh theme={null}
#!/bin/sh
# Check whether @anacron ran today
if test -r /var/spool/anacron/cron.daily; then
    day=$(cat /var/spool/anacron/cron.daily)
fi
if [ "$(date +%Y%m%d)" = "$day" ]; then
    exit 0
fi

# Skip jobs when on battery power
online=1
for psupply in AC AD0*; do
    sysfile="/sys/class/power_supply/$psupply/online"
    if [ -f "$sysfile" ]; then
        if [ "$(cat "$sysfile" 2>/dev/null)" = 1 ]; then
            online=1
            break
        else
            online=0
        fi
    fi
done
if [ "$online" = 0 ]; then
    exit 0
fi
# …rest of the script…
```

***

## Quick Reference: Shell Constructs

| Construct   | Use Case                   | Example                                    |   |                |
| ----------- | -------------------------- | ------------------------------------------ | - | -------------- |
| shebang     | Select interpreter         | `#!/bin/bash`                              |   |                |
| if … then   | Conditional execution      | `if grep -q 'foo' file; then echo yes; fi` |   |                |
| for … do    | Iterate over lists         | `for file in *.log; do gzip "$file"; done` |   |                |
| `>>`        | Append redirection         | `date >> /tmp/script.log`                  |   |                |
| `test -f`   | Check file existence       | `if test -f /path/to/file; then …`         |   |                |
| exit status | Check command success/fail | \`command && echo success                  |   | echo failure\` |

***

## Further Resources

* [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)
* [Linux `tar` Documentation](https://www.gnu.org/software/tar/manual/)
* [Anacron on CentOS Wiki](https://wiki.centos.org/HowTos/Anacron)

Make sure to explore bash built-ins (`help`) and system scripts under `/etc/cron.*` for more real-world patterns and advanced techniques.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/ca5e9d7c-9dac-4ecc-9e21-dafef5ef2641/lesson/1dc5ee08-21f3-4716-8495-459735938e6b" />
</CardGroup>


# Verify completion of scheduled jobs

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/Operation-of-Running-Systems/Verify-completion-of-scheduled-jobs/page

Explains how to verify and capture output of cron, anacron, and at scheduled jobs on CentOS Stream 8 using system logs, journalctl, and systemd-cat.

Hello, and welcome to this lesson on verifying the completion of scheduled jobs on CentOS Stream 8 (and similar Linux systems). By default, cron, anacron, and at write activity to the system logging facility. That makes it straightforward to confirm whether scheduled jobs ran and, when needed, to capture their output.

<Frame>
  <img alt="A dark presentation slide showing the heading &#x22;Demo&#x22; and the text &#x22;Verify Completion of Scheduled Jobs&#x22; on the left. The right side has a large video placeholder with a small film camera icon and a KodeKloud logo in the top-right." />
</Frame>

## Why this matters

System administrators frequently need to verify that scheduled tasks completed successfully or produced the expected output. Knowing where and how cron/anacron/at log their activity helps you troubleshoot failures, capture output, and set up notifications.

## Cron — per-user crontab

To demonstrate, add two simple per-user cron jobs that run every minute. Edit the crontab with crontab -e and add these lines:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ crontab -e
