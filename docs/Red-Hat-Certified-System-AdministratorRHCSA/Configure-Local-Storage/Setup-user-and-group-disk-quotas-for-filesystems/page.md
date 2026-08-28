# open                 0
LV Size                2.00 GiB
Current LE             512
Segments               1
Allocation             inherit
Read ahead sectors     auto (currently set to 8192)
Block device           253:2
```

This LV path (/dev/my\_volume/partition1) works in a similar way to standard device files like `/dev/vda`.

<Frame>
  ![The image shows a terminal window displaying information about a logical volume in a CentOS system, including details like path, name, size, and status.](https://kodekloud.com/kk-media/image/upload/v1752883555/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-Manage-and-configure-LVM-storage/centos-logical-volume-terminal-info.jpg)
</Frame>

## Additional LVM Commands and Tips

If you ever need help or a quick refresher on any LVM command, refer to the manual pages by running:

```bash theme={null}
man lvm
```

While navigating the manual, you can use tab-completion in the terminal. For example, type "vg" and press Tab twice to see available VG options such as:

* vgcreate
* vgdisplay
* vgexport
* vgchange
* vgck
* vgextend
* vgimport
* vgmerge
* vgimportdevices
* vgcfgrestore
* vgmknodes
* vgreduce
* vgs
* vgsplit

This concludes our guide on managing and configuring LVM storage in Linux. Armed with these commands and tips, you are now ready to explore further lab exercises and enhance your Linux storage management skills.

<Frame>
  ![The image shows a terminal window displaying a list of Linux Logical Volume Manager (LVM) commands and related utilities. The text is part of a manual page, as indicated by the footer.](https://kodekloud.com/kk-media/image/upload/v1752883556/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-Manage-and-configure-LVM-storage/linux-lvm-commands-terminal.jpg)
</Frame>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/207496ef-0e82-42c8-aa9d-7996cfb968a6/lesson/ffca6cd1-f450-491b-a7b9-609f2752674c" />
</CardGroup>


# Setup user and group disk quotas for filesystems

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Configure-Local-Storage/Setup-user-and-group-disk-quotas-for-filesystems/page

This guide explains how to set up user and group disk quotas on Linux filesystems to ensure fair storage resource distribution.

In this guide, you'll learn how to set up user and group disk quotas for file systems in Linux. Disk quotas prevent any user or group from monopolizing storage resources, ensuring fair distribution among all system users. For instance, on a 100-terabyte server, instead of one user consuming 80 terabytes and leaving only 20 terabytes for 99 users, you can enforce quotas—such as allowing each user 1 terabyte of storage.

<Callout icon="lightbulb">
  Enforcing disk quotas helps maintain balanced resource usage on shared storage systems, preventing individual users or groups from overwhelming the system capacity.
</Callout>

## Prerequisites

Before proceeding, ensure the necessary quota management tools are available. On many distributions like CentOS, these tools come preinstalled. If not, install them using DNF:

```bash theme={null}
$ sudo dnf install quota
```

## Enabling Disk Quotas on a Filesystem

### Updating /etc/fstab

To begin, decide which file system will have quotas enabled. For example, to enforce quotas on the backup partition, open the `/etc/fstab` file with your preferred text editor (e.g., Vim) and modify the corresponding line to include user and group quota options.

If the original entry is:

```fstab theme={null}
/dev/vdb1 /mybackups xfs ro,noexec 0 2
```

Update it to:

```fstab theme={null}
/dev/vdb1 /mybackups xfs defaults,usrquota,grqquota 0 2
```

Here, `usrquota` activates user quotas and `grqquota` activates group quotas.

<Callout icon="triangle-alert">
  Before modifying /etc/fstab, ensure you have a backup of the file. A misconfiguration could render your system unbootable.
</Callout>

### Applying Changes

After editing `/etc/fstab`, save the file and reboot the machine to apply the changes:

```bash theme={null}
$ sudo vim /etc/fstab
$ sudo systemctl reboot
```

## Configuring Quotas on Different Filesystems

### XFS Filesystem

On an XFS filesystem, quota monitoring is managed internally. Once the quota options are enabled in `/etc/fstab`, the system will automatically track usage and enforce limits without additional configuration.

### ext4 Filesystem

For ext4 filesystems, quotas are not tracked internally. To set up quota tracking on a partition (e.g., `/dev/vdb2` mounted at `/mnt`), create the necessary quota files (`aquota.user` and `aquota.group`) by running:

```bash theme={null}
$ sudo quotacheck --create-files --user --group /dev/vdb2
```

Note: Run the `quotacheck` command only once per filesystem to avoid redundancy.

## Creating a Test Environment on an XFS Filesystem

To demonstrate quota management, we will use the XFS filesystem mounted at `/mybackups`.

### Step 1: Set Up a User Directory

Create a directory for a user named Aaron, change its ownership, and generate a 100-megabyte file using the `fallocate` command:

```bash theme={null}
$ sudo mkdir /mybackups/aaron/
$ sudo chown aaron:aaron /mybackups/aaron
$ fallocate --length 100M /mybackups/aaron/100Mfile
```

### Step 2: Adjust User Quotas

Use the `edquota` command to adjust quotas for the user Aaron:

```bash theme={null}
$ sudo edquota --user aaron
Disk quotas for user aaron (uid 1000):
```

When the editor launches, you will see current block usage (where one block is typically one kilobyte). For example, 102,400 blocks correspond to 100 megabytes. You can easily set soft and hard limits using the suffixes “M” (megabytes), “G” (gigabytes), or “T” (terabytes). In this scenario, you might set a soft limit of 150M and a hard limit of 200M:

```bash theme={null}
$ sudo edquota --user aaron
Disk quotas for user aaron (uid 1000):
Filesystem           blocks   soft    hard   inodes   soft   hard
/dev/vdb1            102400   150M    200M     2       0      0
```

### Step 3: Testing Quota Enforcement

Create an additional 60-megabyte file to increase Aaron's disk usage:

```bash theme={null}
$ fallocate --length 60M /mybackups/aaron/60Mfile
```

At this point, Aaron's total disk usage is 160 megabytes—exceeding the soft limit of 150M but still below the hard limit of 200M. The system marks the soft limit breach with an asterisk and initiates a grace period (typically six days), during which Aaron can reduce disk usage below the soft limit:

```bash theme={null}
$ sudo quota --user aaron
Disk quotas for user aaron (uid 1000):
    Filesystem   blocks   quota   limit   grace   files   quota   limit   grace
    /dev/vdb1    163840*  153600  204800  6days   3       0       0
```

If storage usage is not reduced during the grace period, the system will enforce the soft limit strictly.

### Step 4: Exceeding the Hard Limit

Attempting to create a file that pushes usage beyond the hard limit will result in an error. For example, creating a 40-megabyte file would exceed the 200-megabyte hard limit:

```bash theme={null}
$ fallocate --length 40M /mybackups/aaron/40Mfile
fallocate: fallocate failed: Disk quota exceeded
```

## Managing Inode Quotas

Disk quotas can also limit the number of files and directories via inode quotas. Each file or directory consumes one inode. For example, the quota editor might display:

```bash theme={null}
$ sudo edquota --user aaron
Disk quotas for user aaron (uid 1000):
    Filesystem      blocks   soft   hard    inodes   soft   hard
    /dev/vdb1       102400    0      0       4       0      5
```

Aaron is using 4 inodes with a hard limit of 5. Creating another file or directory would exceed the inode limit, blocking further file creations.

## Adjusting Grace Periods

You can modify the grace periods (the time before soft limits are enforced) using the `edquota` command with the corresponding edit period option. This allows you to set separate grace periods for blocks (storage) and inodes (file count).

## Managing Group Quotas

Managing group quotas follows a process nearly identical to that for user quotas. The primary difference is using the group flag (e.g., -g) with the `edquota` command. To verify group quotas, include the group option with the `quota` command.

## Conclusion

By following these steps, you can efficiently set up and manage disk quotas for both users and groups on Linux systems. This ensures balanced resource utilization and prevents excessive disk usage by any single user or group.

Now, it's time to get some hands-on lab practice and deepen your understanding of disk quota management!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/207496ef-0e82-42c8-aa9d-7996cfb968a6/lesson/d2e9ecaa-ee35-43f8-bac7-4ac64eceefd9" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/207496ef-0e82-42c8-aa9d-7996cfb968a6/lesson/cf7eac38-499b-477b-bad7-ae5c9505a76a" />
</CardGroup>
