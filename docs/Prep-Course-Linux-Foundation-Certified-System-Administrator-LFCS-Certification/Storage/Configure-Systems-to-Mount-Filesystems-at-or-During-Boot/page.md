# of inodes with ind/dind/tind blocks: 0/0/0
Extent depth histogram: 3
36942 blocks used (3.52%, out of 1048576)
0 bad blocks
1 large file

0 regular files
2 directories
0 character device files
0 block device files
0 fifos
0 links
0 symbolic links (0 fast symbolic links)
0 sockets
__________
2 files
```

<Callout icon="lightbulb">
  Using the "-p" option with fsck.ext4 is especially useful when the file system has many errors, as it automates the repair process.
</Callout>

─────────────────────────────────────────────

## Verifying Key Processes and Services

Ensuring that critical services are running is vital for system stability. The following command displays systemd unit dependencies in a tree-like structure, helping you visualize service relationships.

```bash theme={null}
$ systemctl list-dependencies
default.target
└─ apport.service
   ├─ display-manager.service
   ├─ systemd-update-utmp-runlevel.service
   ├─ udisks2.service
   └─ multi-user.target
       └─ anacron.service
```

In the dependency tree, a green (active) circle indicates the service is running, while a white (inactive) circle means it isn’t. Some services only run briefly at boot (and then exit), but others—like ssh.service, cron.service, and atd.service—should remain active.

To simulate an issue, let’s terminate the atd daemon:

```bash theme={null}
$ sudo pkill atd
```

After terminating, check the dependencies to see that the atd service is now inactive:

```bash theme={null}
$ systemctl list-dependencies
multi-user.target
├─ atd.service
├─ console-setup.service
├─ cron.service
└─ dbus.service
```

View the status of the terminated service for more details:

```bash theme={null}
$ systemctl status atd.service
○ atd.service - Deferred execution scheduler
   Loaded: loaded (/lib/systemd/system/atd.service; enabled; vendor preset: enabled)
   Active: inactive (dead) since Fri 2024-03-08 03:18:09 EET; 4min 10s ago
Mar 08 03:45:30 kodekloud systemd[1]: atd.service: Deactivated successfully.
```

Since atd is configured to start on boot, restarting it should resolve the issue:

```bash theme={null}
$ sudo systemctl start atd.service
```

If "systemctl status" logs do not clearly explain the issue, review the service logs with journalctl:

```bash theme={null}
$ journalctl -u atd.service
```

This command helps you pinpoint the root cause if the service is failing to start.

─────────────────────────────────────────────

## Summary

By using tools such as df, du, free, uptime, and file system check utilities like xfs\_repair and fsck.ext4, alongside service monitoring commands like systemctl and journalctl, you can proactively verify the integrity and availability of your server’s resources and processes. This systematic monitoring helps ensure your systems run smoothly and alerts you early to potential issues.

Happy monitoring!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-foundation-certified-system-administrator-lfcs/module/cb813f7f-73bd-40ee-a088-d31ba20c51de/lesson/9cda6cb2-2337-41e7-a671-2866f65ca44a" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/linux-foundation-certified-system-administrator-lfcs/module/cb813f7f-73bd-40ee-a088-d31ba20c51de/lesson/975feb92-bf2c-4ced-945e-fc04b1814fac" />
</CardGroup>


# Configure Systems to Mount Filesystems at or During Boot

Source: https://notes.kodekloud.com/docs/Prep-Course-Linux-Foundation-Certified-System-Administrator-LFCS-Certification/Storage/Configure-Systems-to-Mount-Filesystems-at-or-During-Boot/page

This guide explains how to mount filesystems manually and automatically during boot using fstab.

This guide explains how to mount filesystems both manually and automatically during boot. Previously, you learned how to create filesystems, but even after creation, a filesystem remains inaccessible until it is mounted. Mounting attaches a filesystem to a directory, allowing you to create and manage files on it. The sections below detail the step-by-step process of mounting filesystems and automating these operations using fstab.

## Mounting a Filesystem Manually

First, consider a temporary mount directory. In this example, we will mount an XFS filesystem (created in a previous lesson) located on `/dev/vdb1` at the directory `/mnt`.

<Callout icon="lightbulb">
  Ensure that the directory exists and is empty before mounting the filesystem.
</Callout>

Run the following commands to mount the device, create a test file, and verify the mount:

```bash theme={null}
$ ls /mnt/
$ sudo mount /dev/vdb1 /mnt/
$ sudo touch /mnt/testfile
$ ls -l /mnt/
-rw-r--r--. 1 root root 0 Apr 8 09:03 testfile
```

You can confirm that the new file resides on the mounted filesystem using the `lsblk` command:

```bash theme={null}
$ lsblk
NAME                             MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
vda                              252:0    0   20G  0 disk 
├─vda1                           252:1    0    1M  0 part 
├─vda2                           252:2    0  1.8G  0 part /boot
├─vda3                           252:3    0 18.2G  0 part 
│ └─ubuntu--vg-ubuntu--lv       253:0    0   10G  0 lvm  /
vdb                              252:16   0   10G  0 disk 
├─vdb1                           252:17   0    4G  0 part 
├─vdb2                           252:18   0    4G  0 part 
└─vdb3                           252:19   0    2G  0 part
```

When finished, unmount the filesystem using the `umount` command (note the spelling without the “n”):

```bash theme={null}
$ sudo umount /mnt/
```

After unmounting, running `lsblk` will show that `/mnt` is empty.

## Automatic Mounting with fstab

Some filesystems mount automatically at boot time. For instance, `/dev/vda2` is typically mounted to `/boot` based on system configuration. To automate the mounting of additional filesystems such as the XFS filesystem on `/dev/vdb1`, you need to add an entry to the `/etc/fstab` file.

### Understanding the fstab File Format

The `/etc/fstab` file uses six fields for each filesystem entry:

1. **Block Device**: The partition (e.g., `/dev/vdb1`).
2. **Mount Point**: The directory to attach the filesystem (e.g., `/mybackups`).
3. **Filesystem Type**: The type of filesystem (e.g., `xfs` or `ext4`).
4. **Mount Options**: Commonly set to `defaults` but can be customized.
5. **Dump**: Typically set to `0` to disable dump backups.
6. **Pass**: Determines the order for filesystem checks at boot (usually `1` for the root and `2` for others; `0` disables checks).

<Callout icon="lightbulb">
  Use a text editor like Vim to modify the `/etc/fstab` file. Always back up this file before making changes.
</Callout>

For example, to set up your XFS filesystem to mount at `/mybackups`, follow these steps:

1. Create the mount point directory:

   ```bash theme={null}
   $ sudo mkdir -p /mybackups
   ```

2. Edit the `/etc/fstab` file:

   ```bash theme={null}
   $ sudo vim /etc/fstab
   ```

3. Add the following lines to the file:

   ```fstab theme={null}
   /dev/vda2   /boot      ext4    defaults    0 1
   /dev/vdb1   /mybackups xfs     defaults    0 2
   /dev/vdb2   /mybackups ext4    defaults    0 2
   ```

After saving the file, if a reboot is not performed immediately, notify Systemd of your changes so that they are applied at the next boot. On reboot, the filesystem on `/dev/vdb1` will be mounted automatically, and previously created files (for example, `testfile`) will become visible:

```bash theme={null}
$ sudo systemctl reboot

$ ls -l /mybackups/
-rw-r--r-- 1 root root 0 Apr 8 09:03 testfile

$ lsblk
NAME          MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
vda           252:0    0    20G  0 disk 
├─vda1        252:1    0     1M  0 part 
├─vda2        252:2    0   1.8G  0 part /boot
├─vda3        252:3    0  18.2G  0 part 
└─ubuntu--vg-ubuntu--lv
              253:0    0    10G  0 lvm  /
vdb           252:16   0    10G  0 disk 
└─vdb1        252:17   0     4G  0 part /mybackups
  ├─vdb2      252:18   0     4G  0 part 
  └─vdb3      252:19   0     2G  0 part
```

The above output confirms that the filesystem is mounted as expected.

## Configuring a Swap Partition

In a previous lesson, you created a swap partition at `/dev/vdb3`. To enable the swap partition automatically at boot, add the following line to the `/etc/fstab` file:

```bash theme={null}
$ sudo vim /etc/fstab
/dev/vdb3   none    swap    defaults    0 0
```

Key differences in the fstab fields for swap space include:

* The second field is set to `none` since swap space does not require a mount point.
* The third field specifies the type as `swap`.
* Both the dump and pass fields are set to `0` because swap space is not backed up or checked during boot.

A system reboot will ensure the swap partition is enabled automatically.

## Using UUIDs for Reliable Mounting

Sometimes, `/etc/fstab` entries reference devices by their UUID (Universally Unique Identifier) rather than device names. For example, instead of using `/dev/vda2`, an entry might use a UUID from `/dev/disk/by-uuid/`. The major advantage of using UUIDs is that they remain constant even if the device names change (for instance, due to varying connection orders).

To check the UUID of a block device, execute:

```bash theme={null}
$ sudo blkid /dev/vdb1
/dev/vdb1: LABEL="FirstFS" UUID="a51d7731-b033-4c07-b171-628ae951ea01" BLOCK_SIZE="512" TYPE="xfs" PARTUUID="21b2fb38-0cb9-104b-bd17-a60362e5aacd"
```

You can then update your fstab entry to use the UUID format, ensuring consistent device identification. To view all UUID assignments, run:

```bash theme={null}
$ ls -l /dev/disk/by-uuid/
```

Using UUIDs in your fstab file improves reliability, especially in complex storage environments.

## Final Thoughts

By following these guidelines, you can ensure that your filesystems and swap space are automatically mounted and enabled at boot, even when underlying device names change. For more detailed information on fstab and mounting options, refer to the manual page:

```bash theme={null}
man fstab
```

This concludes our guide on configuring systems to mount filesystems at boot. Happy computing!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-foundation-certified-system-administrator-lfcs/module/cfd9ce0f-72d4-40ec-97cd-875899512ff2/lesson/e3d35648-d593-42c6-95fd-6bcaed170c5c" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/linux-foundation-certified-system-administrator-lfcs/module/cfd9ce0f-72d4-40ec-97cd-875899512ff2/lesson/b950ad75-7bb1-4a62-86ec-17ece0693a3d" />
</CardGroup>
