# Log the date and time when the script was executed
date >> /tmp/script.log
```

In this snippet, the date command appends the current date and time to /tmp/script.log. This technique can be extended to redirect other outputs and errors.

Now, include another command to log the Linux kernel version from the /proc/version file:

```bash theme={null}
#!/bin/bash
# Log the date and time when the script was executed
date >> /tmp/script.log
# Append the current Linux kernel version to the log
cat /proc/version >> /tmp/script.log
```

After saving your changes (for example, by typing :wq in vim), make the script executable:

```bash theme={null}
$ chmod +x script.sh
```

To run the script from the current directory, execute:

```bash theme={null}
$ ./script.sh
```

Verify the output by checking the log file:

```bash theme={null}
$ cat /tmp/script.log
Linux version 5.15.0-94-generic (buildd@lcy02-amd64-096) (gcc …)
```

This script now logs both the date/time and the kernel version, which can be very helpful for maintaining system records. Later, you might consider scheduling this script to run automatically at regular intervals.

──────────────────────────────

## Enhancing Scripts with Bash Built-ins

Bash includes a variety of built-in commands that can make your scripts more intelligent and efficient—these include conditional statements, loops, and more. To see a list of available built-in commands, simply execute:

```plaintext theme={null}
$ help
```

This command displays built-ins such as if, test, alias, and others.

──────────────────────────────

## Archiving Application Data

Next, let’s create a script that archives the contents of the /etc/apt directory. Even if the file does not exist, your editor (like vim) will create it once you save.

Open a new file for editing:

```bash theme={null}
$ vim archive-apt.sh
```

Enter the following content to create a tar archive:

```bash theme={null}
#!/bin/bash
tar acf /tmp/archive.tar.gz /etc/apt/
```

This script uses tar to create an archive at /tmp/archive.tar.gz that contains the entire /etc/apt directory. After making the script executable and running it, you can inspect the archive contents using:

```bash theme={null}
tar -tf /tmp/archive.tar.gz
```

<Callout icon="lightbulb">
  Re-running this script will overwrite the existing archive. Adding backup logic can preserve previous archives.
</Callout>

──────────────────────────────

## Archive Script with Backup Rotation

To avoid unintended data loss, create a script that implements backup rotation for the archive file:

```bash theme={null}
$ vim archive-apt-2.sh
```

Add the following content:

```bash theme={null}
#!/bin/bash
if test -f /tmp/archive.tar.gz; then
    mv /tmp/archive.tar.gz /tmp/archive.tar.gz.OLD
    tar acf /tmp/archive.tar.gz /etc/apt/
else
    tar acf /tmp/archive.tar.gz /etc/apt/
fi
```

This script checks if the file /tmp/archive.tar.gz exists. If it does, the script renames it to /tmp/archive.tar.gz.OLD before creating a new archive. Otherwise, it simply creates the archive.

Make the script executable and run it:

```bash theme={null}
$ chmod +x archive-apt-2.sh
$ ./archive-apt-2.sh
$ ls /tmp
archive.tar.gz
archive.tar.gz.OLD
script.log
```

Now you have both the new archive and a backup available for reference.

──────────────────────────────

## Understanding Exit Status Codes and Conditional Execution

In bash, every command returns an exit status. A zero value usually indicates success, while a non-zero value signals an error or a condition that was not met. For example, the grep command returns zero if a match is found and one if no match is found.

Consider the following script, which checks if the file /etc/default/grub contains the digit '5':

```bash theme={null}
#!/bin/bash
if grep -q '5' /etc/default/grub; then
    echo 'Grub has a timeout of 5 seconds.'
else
    echo 'Grub DOES NOT have a timeout of 5 seconds.'
fi
```

Here, the -q option makes grep work in quiet mode, suppressing output and relying solely on its exit status for the conditional check.

──────────────────────────────

## Reviewing Common Script Structures

Many essential system scripts are located in directories such as /etc, /cron.daily, /cron.weekly, and /cron.monthly. These scripts typically follow common conventions: starting with the shebang, using descriptive comments, and employing structured if/else statements.

Below is an example shell script that checks whether anacron was run today and confirms if the system is running on battery power:

```sh theme={null}
#!/bin/sh
# Check whether anacron was run today already
if test -r /var/spool/anacron/cron.daily; then
    day=`cat /var/spool/anacron/cron.daily`
fi
if [ `date +%Y%m%d` = "$day" ]; then
    exit 0
fi

# Do not run jobs when on battery power
online=1
for psupply in AC ADP0 ; do
    sysfile="/sys/class/power_supply/$psupply/online"
    if [ -f $sysfile ] ; then
        if [ `cat $sysfile 2>/dev/null` = 1 ]; then
            online=1
            break
        else
            online=0
        fi
    fi
done
if [ $online = 0 ] ; then
    exit 0
fi
```

This script exemplifies standard practices in shell scripting, including proper use of the shebang, commenting, and managing conditionals with if/else statements and loops.

──────────────────────────────

## Further Learning

To further enhance your bash scripting skills, consider exploring advanced courses. The [Shell Scripts for Beginners](https://learn.kodekloud.com/user/courses/shell-scripts-for-beginners) course on KodeKloud is an excellent resource that provides hands-on labs and practical exercises along with clear theoretical explanations.

<Frame>
  ![The image is an advertisement for a "Shell Scripts for Beginners" course by KodeKloud, featuring a 3D illustration of a rocket and penguins on a circuit board, alongside a list of course contents.](https://kodekloud.com/kk-media/image/upload/v1752881354/notes-assets/images/Linux-Foundation-Certified-System-Administrator-LFCS-Use-Scripting-to-Automate-System-Maintenance-Tasks/shell-scripts-beginners-advertisement.jpg)
</Frame>

This concludes our guide on using scripting to automate system maintenance tasks. By mastering these techniques, you can ensure efficient system performance and streamline routine administrative operations.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-foundation-certified-system-administrator-lfcs/module/cb813f7f-73bd-40ee-a088-d31ba20c51de/lesson/c72b7e37-8a66-4afc-b9c3-36119965215b" />
</CardGroup>


# Verify Integrity and Availability of Resources and Processes

Source: https://notes.kodekloud.com/docs/Prep-Course-Linux-Foundation-Certified-System-Administrator-LFCS-Certification/Operations-Deployment/Verify-Integrity-and-Availability-of-Resources-and-Processes/page

This article explains how to verify the integrity and availability of system resources and processes through various monitoring tools and commands.

In this lesson, we explain how to verify the integrity and availability of key system resources and processes. Over time, servers tend to use more resources—storage space may fill up as databases grow or users store more files. In cloud environments, adding storage devices is relatively straightforward, but knowing when your storage is near capacity is essential.

Below, we provide detailed steps to monitor disk space, RAM, CPU load, file system integrity, and essential services.

─────────────────────────────────────────────

## Checking Disk Space with df

The "df" (disk free) utility reports on disk usage. By default, sizes are shown in 1-kilobyte blocks, which can be difficult to interpret. Use the "-h" option to display sizes in a human-readable format (MB, GB, TB).

Example output of "df":

```bash theme={null}
$ df
Filesystem                                   1K-blocks      Used Available Use% Mounted on
tmpfs                                         400588      1112    399476   1% /run
/dev/mapper/ubuntu--vg-ubuntu--lv         10218772   4070292   5607808  43% /
tmpfs                                        2002940         0   2002940   0% /dev/shm
tmpfs                                          5120         0      5120   0% /run/lock
/dev/vda2                                   1790136    256868   1424068  16% /boot
tmpfs                                         400588         4    400584   1% /run/user/1000
```

Using the human-readable option:

```bash theme={null}
$ df -h
Filesystem                                   Size  Used Avail Use% Mounted on
tmpfs                                        392M  1.1M  391M   1% /run
/dev/mapper/ubuntu--vg-ubuntu--lv             9.8G  3.9G  5.4G  43% /
tmpfs                                        2.0G  0.0G  2.0G   0% /dev/shm
tmpfs                                        5.0M  0.5M  0.5M   0% /run/lock
/dev/vda2                                    1.8G  251M  1.4G  16% /boot
tmpfs                                        392M  4.0K  392M   1% /run/user/1000
```

In the output above, filesystems labeled as "tmpfs" are virtual filesystems that only reside in memory. In this case, only two actual filesystems are in use: the root filesystem (mounted on "/") where the Linux operating system is installed, and the smaller "/boot" filesystem that holds boot files.

To view the disk space used by a specific directory, use the "du" (disk usage) utility. By default, "du" lists the space used by the directory and all of its subdirectories. The "-s" (summarize) option provides output for the specified directory only, while "-h" displays sizes in a human-friendly format.

```bash theme={null}
$ du -sh /usr/
3.0G    /usr/
```

─────────────────────────────────────────────

## Checking Memory Usage with free

Monitoring RAM is as important as disk monitoring. The "free" command displays how much RAM is used and available, while the "-h" option renders sizes in a human-readable format (using mebibytes and gibibytes).

```bash theme={null}
$ free -h
              total        used        free      shared  buff/cache   available
Mem:          3.6Gi       1.0Gi       1.5Gi        15Mi       1.1Gi       2.4Gi
Swap:         2.0Gi          0B       2.0Gi
```

In this example, the "used" value might appear high, but the "available" column indicates that 2.4 GiB of memory can still be reclaimed if necessary. Temporary memory used for caching large files does not prevent the memory from being available to applications.

<Callout icon="lightbulb">
  Use the "free -h" command as a quick reference to ensure your system has adequate memory, especially when running high-load applications.
</Callout>

─────────────────────────────────────────────

## Analyzing CPU Load with uptime

The "uptime" command provides key data about system load and uptime. The output shows three load average numbers representing the average system load over the last 1, 5, and 15 minutes.

```bash theme={null}
$ uptime
17:24:55 up 32 min,  1 user,  load average: 0.05, 0.05, 0.01
```

A load average of 1.0 over the last minute indicates that one CPU core has been fully utilized on average. For systems with multiple cores, a load average higher than the number of cores suggests some processes are waiting for CPU time. Consistently high load averages may signal the need to upgrade hardware or optimize running processes.

─────────────────────────────────────────────

## Checking File System Integrity

Before checking a file system for errors, ensure it is unmounted. File system checks differ depending on whether your system uses XFS or ext4. For more detailed information on file systems, partitions, mounting, and unmounting, refer to our upcoming storage sections.

<Frame>
  ![The image provides information on file system integrity, noting that file systems must be unmounted to check for errors. It mentions that Redhat OS uses xfs as the default file system, while Ubuntu OS uses ext4.](https://kodekloud.com/kk-media/image/upload/v1752881355/notes-assets/images/Linux-Foundation-Certified-System-Administrator-LFCS-Verify-Integrity-and-Availability-of-Resources-and-Processes/file-system-integrity-checks-redhat-ubuntu.jpg)
</Frame>

<Callout icon="lightbulb">
  Operating systems in the Red Hat family typically use the XFS file system by default, while Ubuntu systems use ext4.
</Callout>

To verify an XFS file system, run:

```bash theme={null}
$ sudo xfs_repair -v /dev/vdb1
Phase 1 - find and verify superblock...
        - block cache size set to 175968 entries
Phase 2 - using internal log
        zero log...
zero_log: head block 103 tail block 103
        scan filesystem freespac and inode maps...
        found root inode chunk
Phase 3 - for each AG...
        scan and clear agi unlinked lists...
        process known inodes and perform inode discovery...
        agno = 0
        agno = 1
        agno = 2
        agno = 3
Phase 4 - check for duplicate blocks...
        setting up duplicate extent list...
        check for inodes claiming duplicate blocks...
        agno = 0
        agno = 1
        agno = 2
        agno = 3
Phase 5 - rebuild AG headers and trees...
        agno = 0
        agno = 1
        agno = 2
        agno = 3
Phase 6 - check inode connectivity...
        resetting contents of realtime bitmap and summary inodes
        traversing filesystem
        agno = 0
        agno = 1
        agno = 2
        agno = 3
Phase 7 - scan finished ...
        moving disconnected inodes to lost+found ...
done
```

Here, "/dev/vdb1" is the partition containing the file system. Depending on your configuration, the device name might differ (for example, "/dev/vda2" or "/dev/sdc3").

For an ext4 file system, use the fsck utility with ext4 options. The "-v" flag increases verbosity, "-f" forces a check even on healthy filesystems, and "-p" (preen mode) fixes simple issues automatically.

```bash theme={null}
$ sudo fsck.ext4 -v -f -p /dev/vdb2
11 inodes used (0.00%, out of 262144)
0 non-contiguous files (0.0%)
0 non-contiguous directories (0.0%)
