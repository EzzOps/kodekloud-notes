# Default: sizes in 1K blocks
df
```

For human-readable output (MB, GB, …), add the `-h` flag:

```bash theme={null}
df -h
Filesystem                  Size  Used Avail Use% Mounted on
/dev/mapper/cs-root          17G  7.9G   9.2G  47% /
/dev/vda1                   1014M  435M  580M  43% /boot
tmpfs                       1.9G     0  1.9G   1% /dev/shm
...
```

<Callout icon="lightbulb">
  Ignore `tmpfs` entries—they represent in-memory filesystems, not physical disks.
</Callout>

## Directory Usage

To measure the size of a specific directory, run `du` with summarization and human-readable flags:

```bash theme={null}
du -sh /var/log
# e.g., 512M    /var/log
```

<Callout icon="triangle-alert">
  Running `du` on very large or deeply nested directories can take time and generate high I/O.
</Callout>

## Memory Utilization

Display RAM and swap usage with `free`:

```bash theme={null}
free -h
              total        used        free      shared  buff/cache   available
Mem:          3.6Gi       1.0Gi       1.5Gi        15Mi       1.1Gi       2.4Gi
Swap:         2.0Gi          0B       2.0Gi
```

Focus on the **available** column—it indicates memory ready for new applications.

## CPU Load and Hardware Details

### Load Averages

Use `uptime` to view load averages over 1, 5, and 15 minutes:

```bash theme={null}
uptime
# 17:24:55 up 32 min,  1 user,  load average: 0.05, 0.05, 0.01
```

* On a single-core system, load of **1.00** equates to 100% utilization.
* On an 8-core system, a load of **6.00** means six cores were fully busy.

### CPU Architecture

```bash theme={null}
lscpu
```

Key fields:\
• Architecture\
• CPU(s)\
• Thread(s) per core\
• Model name\
• Cache sizes

### PCI Devices

```bash theme={null}
lspci
```

Lists all PCI devices, including network adapters, GPUs, and host bridges.

## File System Integrity

### Repairing an XFS File System

1. **Unmount** the partition:\
   `sudo umount /dev/vdb1`
2. **Repair** with verbose output:
   ```bash theme={null}
   sudo xfs_repair -v /dev/vdb1
   ```
3. **Remount** after completion:\
   `sudo mount /dev/vdb1 /mnt`

<Callout icon="lightbulb">
  Always unmount the XFS volume before running `xfs_repair` to avoid data corruption.
</Callout>

### Checking and Repairing an ext4 File System

Run `fsck.ext4` with verbose, forced check, and preen (auto-fix simple issues):

```bash theme={null}
sudo fsck.ext4 -v -f -p /dev/vdb2
```

* `-v`: verbose output
* `-f`: force check even if clean
* `-p`: preen mode for unattended fixes

<Callout icon="triangle-alert">
  Do **not** run `fsck` on a mounted ext4 partition, especially the root (`/`), as it may cause data loss.
</Callout>

## Monitoring Key Processes

List all service dependencies and their statuses with `systemctl`:

```bash theme={null}
systemctl list-dependencies
# default.target
# ● └─accounts-daemon.service
# ● └─gdm.service
# ○ └─chronyd.service
```

* `●` = running
* `○` = stopped

Example: simulate stopping NTP service, verify, then restart:

```bash theme={null}
# Stop chronyd
sudo pkill chronyd

# Recheck dependencies
systemctl list-dependencies

# Inspect why it stopped
systemctl status chronyd.service

# Restart the service
sudo systemctl start chronyd.service
```

## Command Summary

| Command                     | Description                            | Key Flags               |
| --------------------------- | -------------------------------------- | ----------------------- |
| df                          | Show filesystem disk usage             | -h (human readable)     |
| du                          | Estimate directory space usage         | -sh (summarize + human) |
| free                        | Display memory and swap usage          | -h                      |
| uptime                      | Show system uptime and load averages   | —                       |
| lscpu                       | Display CPU architecture and features  | —                       |
| lspci                       | List PCI devices                       | —                       |
| xfs\_repair                 | Repair XFS file systems                | -v (verbose)            |
| fsck.ext4                   | Check and repair ext4 partitions       | -v, -f, -p              |
| systemctl list-dependencies | List service dependencies and statuses | —                       |

## Links and References

* [df(1) Manual Page](https://man7.org/linux/man-pages/man1/df.1.html)
* [du(1) Manual Page](https://man7.org/linux/man-pages/man1/du.1.html)
* [free(1) Manual Page](https://man7.org/linux/man-pages/man1/free.1.html)
* [xfs\_repair(8) Manual Page](https://man7.org/linux/man-pages/man8/xfs_repair.8.html)
* [fsck.ext4(8) Manual Page](https://man7.org/linux/man-pages/man8/fsck.ext4.8.html)
* [systemctl(1) Manual Page](https://man7.org/linux/man-pages/man1/systemctl.1.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/ca5e9d7c-9dac-4ecc-9e21-dafef5ef2641/lesson/587e0638-9eed-4b9e-886b-ff478341d263" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/ca5e9d7c-9dac-4ecc-9e21-dafef5ef2641/lesson/fc948c4e-a60f-4e77-a297-8ab6661bc64d" />
</CardGroup>


# Configure user resource limits

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/User-and-Group-Management/Configure-user-resource-limits/page

This guide explains how to configure user resource limits in Linux to prevent resource monopolization.

Managing resource usage per user prevents any single account from monopolizing CPU, memory, or processes. In this guide, you’ll learn how to configure limits via `/etc/security/limits.conf`, verify them, and understand each directive.

## Prerequisites

* A Linux distribution with PAM-enabled login (most modern distros).
* `sudo` privileges to edit `/etc/security/limits.conf`.

## 1. Back Up and Open limits.conf

<Callout icon="triangle-alert">
  Always back up system configuration files before editing.

  ```bash theme={null}
  sudo cp /etc/security/limits.conf{,.bak}
  ```
</Callout>

Open the file for editing:

```bash theme={null}
sudo vim /etc/security/limits.conf
```

You’ll see a template like:

```ini theme={null}
#<domain>    <type>  <item>      <value>
#*           soft    core       0
#*           hard    rss        10000
#@student    hard    nproc      20
#@faculty    soft    nproc      20
#@faculty    hard    nproc      50
#ftp         hard    nproc      0
#@student    -       maxlogins  4
```

***

## 2. Understanding limits.conf Fields

limits.conf uses four fields per line:

| Field  | Description                                                                  |
| ------ | ---------------------------------------------------------------------------- |
| domain | User (`trinity`), group (`@developers`), or `*` for all users.               |
| type   | `soft` (initial limit), `hard` (maximum ceiling), or `-` (both soft & hard). |
| item   | Resource type (e.g., `nproc`, `fsize`, `cpu`).                               |
| value  | Numeric limit (units vary per item).                                         |

### 2.1 Domain

* `username` (e.g., `trinity`)
* Group with `@` prefix (e.g., `@developers`)
* `*` for every user not otherwise matched

Example: limit user `trinity` to 10 processes:

```ini theme={null}
trinity    hard    nproc    10
```

### 2.2 Type

* `hard` — absolute maximum (cannot be exceeded).
* `soft` — initial/session limit (can increase up to hard).
* `-` — sets both `soft` and `hard`.

```ini theme={null}
