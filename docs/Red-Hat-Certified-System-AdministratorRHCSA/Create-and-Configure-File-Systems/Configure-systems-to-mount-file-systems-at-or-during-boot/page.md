# Configure systems to mount file systems at or during boot

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Create-and-Configure-File-Systems/Configure-systems-to-mount-file-systems-at-or-during-boot/page

Learn to configure Linux systems for automatic file system mounting during boot using manual methods and the /etc/fstab file.

In this article, you will learn how to configure Linux systems to mount file systems automatically during boot. Mounting a file system means attaching it to a directory within your existing directory hierarchy, allowing you to access and create files on it. Previously, file systems may have been created but not mounted, which prevents access to their directories and files.

Below is a step-by-step guide that demonstrates how to mount a file system manually and configure permanent mounts in the /etc/fstab file.

─────────────────────────────────────────────

## 1. Mounting a File System Manually

First, inspect the directory used for temporary mounts. The `/mnt` directory is conventionally used for this purpose:

```bash theme={null}
$ ls /mnt/
```

This directory should be empty initially.

Assume you want to mount an XFS file system that has already been created on the partition `/dev/vdb1`. To mount it, use the following command:

```bash theme={null}
$ sudo mount /dev/vdb1 /mnt/
```

After mounting, you can create files on the file system. For example, create a test file and list the directory contents:

```bash theme={null}
$ ls /mnt/
$ sudo touch /mnt/testfile
$ ls -l /mnt/
-rw-rw-r--. 1 aaron aaron 30 Jan 31 14:30 testfile
```

To confirm the file system is mounted, use the `lsblk` command:

```bash theme={null}
$ lsblk
NAME       MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
vda        8:0    0   20G  0 disk 
├─vda1     8:1    0    1G  0 part /boot
├─vda2     8:2    0   19G  0 part 
├─cs-root 253:0   0   17G  0 lvm  /
└─cs-swap 253:1   0    2G  0 lvm  [SWAP]
```

Once you are finished with work on the file system, unmount it using the `umount` command (note that the command is spelled without an "n"):

```bash theme={null}
$ sudo umount /mnt/
```

You can verify that the `/mnt` directory is empty again:

```bash theme={null}
$ ls /mnt/
```

<Callout icon="lightbulb">
  When Linux boots, certain file systems (like `/dev/vda1` mounted on `/boot`) are automatically mounted according to the instructions provided in configuration files.
</Callout>

For example, the following output from `lsblk` shows various mount points:

```bash theme={null}
$ lsblk
NAME        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
vda         8:0    0   20G  0 disk 
├─vda1      8:1    0    1G  0 part /boot
├─vda2      8:2    0   19G  0 part 
│ ├─cs-root 253:0   0   17G  0 lvm  /
│ └─cs-swap 253:1   0    2G  0 lvm  [SWAP]
vdb         8:16   0  100G  0 disk 
├─vdb1      8:17   0    4G  0 part 
├─vdb2      8:18   0    4G  0 part 
└─vdb3      8:19   0    2G  0 part
```

─────────────────────────────────────────────

## 2. Configuring Automatic Mounting with /etc/fstab

When booting, a Linux system mounts file systems according to the configurations specified in the `/etc/fstab` file. To automatically mount our XFS file system on `/dev/vdb1`, follow these steps:

1. Create a directory that will serve as the mount point. In this example, we create `/mybackups`:

   ```bash theme={null}
   $ sudo mkdir /mybackups
   ```

2. Edit the `/etc/fstab` file using your preferred text editor. In this example, we use Vim:

   ```bash theme={null}
   $ sudo vim /etc/fstab
   ```

The `/etc/fstab` file contains six fields per line:

* **Field 1:** The block device file (e.g., `/dev/vdb1`), indicating the partition or storage resource.
* **Field 2:** The mount point (e.g., `/mybackups`), where the file system will be attached.
* **Field 3:** The file system type (e.g., `xfs`). If using another file system type like `ext4`, adjust this accordingly.
* **Field 4:** Mount options (commonly set to `defaults`).
* **Field 5:** Dump utility flag (commonly `0` since dump is rarely used).
* **Field 6:** File system check order at boot (use `0` to disable, `1` for the root partition, and `2` for other partitions).

A sample line to mount the XFS file system on `/dev/vdb1` to `/mybackups` would be:

```plaintext theme={null}
/dev/vdb1    /mybackups  xfs  defaults  0 2
```

For context, a typical `/etc/fstab` file might look like this:

```plaintext theme={null}
/dev/mapper/cs-root  /         xfs     defaults  0 0
/dev/vdb1           /mybackups  xfs     defaults  0 2
