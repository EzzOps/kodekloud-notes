# If you had an ext4 partition, it might look like:
#/dev/vdb2          /mybackups  ext4    defaults  0 2
# After editing this file, run 'systemctl daemon-reload' to update systemd configuration.
```

After saving your changes, update systemd units generated from `/etc/fstab` without needing to reboot immediately:

```bash theme={null}
$ sudo systemctl daemon-reload
```

Verify that the `/mybackups` directory is empty before reboot:

```bash theme={null}
$ ls /mybackups/
```

After rebooting the system, you should find the test file in `/mybackups`, confirming that the file system was automatically mounted during boot. Check with:

```bash theme={null}
$ ls -l /mybackups/
-rw-rw-r-- 1 aaron aaron 30 Jan 31 14:30 testfile
```

You can also inspect mount points with:

```bash theme={null}
$ lsblk
NAME      MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
vda       8:0    0    20G  0 disk 
├─vda1    8:1    0     1G  0 part /boot
├─vda2    8:2    0    19G  0 part 
├─cs-root 253:0  0    17G  0 lvm  /
├─cs-swap 253:1  0     2G  0 lvm  [SWAP]
vdb       8:16   0    10G  0 disk 
├─vdb1    8:17   0     4G  0 part 
├─vdb2    8:18   0     4G  0 part /mybackups
└─vdb3    8:19   0     2G  0 part
```

To reboot the system, run:

```bash theme={null}
$ sudo systemctl reboot
```

─────────────────────────────────────────────

## 3. Configuring a Swap Partition to Mount Automatically

If you have created a swap partition (e.g., on `/dev/vdb3`), you can enable it to activate automatically at boot. To do this, edit the `/etc/fstab` file:

```bash theme={null}
$ sudo vim /etc/fstab
```

Locate a line similar to the following, which mounts swap space for another device:

```plaintext theme={null}
/dev/mapper/cs-swap   none   swap   defaults   0 0
```

Then add or modify the line for the swap partition on `/dev/vdb3`:

```plaintext theme={null}
/dev/vdb3   none   swap   defaults   0 0
```

Note that for swap, the second field is set to "none" because it does not attach to any directory. The file system type is "swap," and the last two fields are set to 0 since swap space is not backed up or checked during boot.

After saving the file, reboot your system and verify that the swap partition is active:

```bash theme={null}
$ swapon --show
```

> **lightbulb** Swap partitions do not mount to a directory. Instead, they enable virtual memory to improve system performance.

─────────────────────────────────────────────

## 4. Using UUIDs Instead of Device Names

Instead of specifying a block device file like `/dev/vda1`, you can use UUIDs (Universally Unique Identifiers). UUIDs are especially useful because device names may change if storage devices are connected in a different order.

A typical `/etc/fstab` line using a UUID looks like this:

```plaintext theme={null}
UUID=3b93b1ba-e44a-4f75-aa38-c93ed32e34e2   /boot   xfs   defaults   0 0
```

For comparison, the same mount point can be defined using the device name:

```plaintext theme={null}
/dev/vda1   /boot   xfs   defaults   0 0
```

To check the UUID of a block device, use the `blkid` command. For example, to view the UUID for `/dev/vdb1`:

```bash theme={null}
$ sudo blkid /dev/vdb1
/dev/vdb1: LABEL="FirstF5" UUID="9ab8cfa5-2813-4b70-ada0-7abd0ad9d289" BLOCK_SIZE="512" TYPE="xfs" PARTUUID="569a3fcc-f9eb-9147-888d-9e3ffe9ccdb0"
```

─────────────────────────────────────────────

## Conclusion

This guide has shown you how to mount file systems both manually and automatically using `/etc/fstab`, as well as how to configure a swap partition and use UUIDs for improved device management. Now it's time to put this knowledge into practice by mounting file systems and configuring the `/etc/fstab` file on your Linux system. Happy configuring!

- [Watch Video](https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/eb65d854-5137-4776-8ff8-73e274c43a0c/lesson/18d5741b-df3b-4515-b6be-d34704700203)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/eb65d854-5137-4776-8ff8-73e274c43a0c/lesson/4ac25e93-7156-4ed2-9300-4e3d2e45f43a)


# Create and configure file systems

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Create-and-Configure-File-Systems/Create-and-configure-file-systems/page

This article provides a guide on creating and configuring file systems in Linux, focusing on XFS and ext4 file systems.

Welcome to this detailed lesson on creating and configuring file systems in Linux. In this guide, we will walk through the process of formatting partitions, using XFS and ext4 file systems, and modifying file system properties with various utilities. This step-by-step explanation is designed to be both technical and SEO-friendly, ensuring an optimal learning experience.

Before storing files and directories on any partition, it is essential to create a file system on it. On CentOS, the default file system is XFS, but ext4 is also widely supported and commonly used.

## Formatting a Partition with XFS

To format a partition with the XFS file system using default settings, run the following command:

```bash theme={null}
sudo mkfs.xfs /dev/sdb1
```

If you choose to use the ext4 file system instead, the command is similar:

```bash theme={null}
sudo mkfs.ext4 /dev/sdb1
```

The `mkfs` command (short for "make file system") supports numerous settings to tailor the file system. The above examples use the default configuration, which is sufficient for most scenarios. However, if you need to customize parameters, refer to the manual pages for more details.

For example, to view the configurable options for constructing an XFS file system, check its manual page:

```bash theme={null}
man mkfs.xfs
```

One useful option when creating an XFS file system is the `-L` flag, which allows you to assign a label. Note that label names are limited to 12 characters. To label your XFS partition as "BackupVolume", use:

```bash theme={null}
sudo mkfs.xfs -L "BackupVolume" /dev/sdb1
```

Below is an excerpt from the manual page that highlights the `-L` flag and additional options:

![The image shows a terminal window displaying a manual page for the mkfs.xfs command, which is used to construct an XFS filesystem. It includes sections like NAME, SYNOPSIS, and DESCRIPTION.](https://kodekloud.com/kk-media/image/upload/v1752883572/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-Create-and-configure-file-systems/mkfs-xfs-manual-page-terminal.jpg)

Remember, when searching within the manual for specific options, you might need to escape characters like dashes. The manual confirms the label length restriction:

![The image shows a terminal window displaying a manual page for the mkfs.xfs command, detailing options and usage for setting filesystem labels and other parameters.](https://kodekloud.com/kk-media/image/upload/v1752883574/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-Create-and-configure-file-systems/mkfs-xfs-manual-terminal.jpg)

Additionally, you can configure the inode size to store extended file attributes. For instance, to format the partition with 512-byte inodes and label it "BackupVolume", execute:

```bash theme={null}
sudo mkfs.xfs -i size=512 -L "BackupVolume" /dev/sdb1
```

After entering your password, you should expect output similar to:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ sudo mkfs.xfs -i size=512 -L "BackupVolume" /dev/sdb1
[sudo] password for aaron:
meta-data              = /dev/sdb1
data                   =
name                   = version 2
log                    = internal log
realtime               = none
[aaron@LFCS-CentOS ~]$
```

> **lightbulb** If you encounter any unexpected errors while formatting, double-check your partition identifier and ensure your system supports the chosen file system.

## XFS Utilities and Modifying File System Attributes

Once the file system is created, you can explore a suite of XFS utilities by typing `xfs` and pressing the Tab key twice. This will display tools such as:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ xfs
xfs_admin         xfs_estimate       xfs_mkfile         
xfs_bmap          xfs_freeze         xfs_io            
xfs_copy          xfs_fsr            xfs_logprint       
xfs_db            xfs_growfs         xfs_mdrestore      
xfsdump           xfs_info           xfs_metadump      
                  xfs_ncheck         xfs_quota         
                  xfs_repair         xfsrestore        
[aaron@LFCS-CentOS ~]$
```

To display the current label (using a lowercase "l"), run:

```bash theme={null}
sudo xfs_admin -l /dev/sdb1
```

For instance, the output may show:

```bash theme={null}
label = "BackupVolume"
```

To change the label, use the uppercase `-L` option. For example, to update the label to "FistFS", run:

```bash theme={null}
sudo xfs_admin -L "FistFS" /dev/sdb1
```

A confirmation message such as the following indicates that the label has been successfully updated:

```bash theme={null}
writing all SBs
new label = "FistFS"
```

## Formatting a Partition with ext4

The ext4 file system is a popular choice on Linux systems. The process of creating an ext4 file system is handled by the `mke2fs` command, with `mkfs.ext4` serving as a convenient alias. To access its manual page, use:

```bash theme={null}
man mkfs.ext4
```

For ext4, the same `-L` flag is used to set a label, and the `-N` flag allows you to control the number of inodes. This is crucial if you anticipate handling a large volume of small files. If the default inode count is insufficient, you can specify an alternative number.

For instance, to create an ext4 file system on `/dev/sdb2` with a label "BackupVolume" and 500,000 inodes, execute:

```bash theme={null}
sudo mkfs.ext4 -L "BackupVolume" -N 500000 /dev/sdb2
```

The output should resemble:

```bash theme={null}
Creating filesystem with 1048576 4k blocks and 500224 inodes
Filesystem UUID: 903a4d4d-af29-4bf3-9fad-1dfdd0cd9f39
Superblock backups stored on blocks:
 32768, 98304, 163840, 229376, 294912, 819200, 884736
Allocating group tables: done
Writing inode tables: done
Creating journal (16384 blocks): done
Writing superblocks and filesystem accounting information: done
```

To modify properties of an existing ext4 file system, use the `tune2fs` utility. For example, to change the label of `/dev/sdb2` to "SecondFS", run:

```bash theme={null}
sudo tune2fs -L "SecondFS" /dev/sdb2
```

To verify that the label change has been applied, use:

```bash theme={null}
sudo tune2fs -l /dev/sdb2
```

The output will include an entry similar to:

```text theme={null}
Filesystem volume name:   SecondFS
...
```

> **triangle-alert** Ensure that you back up any critical data before modifying file system parameters. Changing labels or inode counts on active file systems without proper precautions can lead to data loss.

## Summary

In this lesson, you learned how to create and configure file systems on Linux using both XFS and ext4. We covered:

* Formatting partitions with XFS and ext4
* Customizing file system parameters such as labels and inode sizes
* Utilizing utilities like `xfs_admin`, `mkfs.ext4`, and `tune2fs` for managing file system attributes

For further details, consult the manual pages by running `man mkfs.xfs`, `man mkfs.ext4`, and `man tune2fs`. Experimenting with these tools will deepen your understanding and hone your Linux file system management skills.

Happy learning and exploring your Linux system configuration!

For additional resources, check out:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/eb65d854-5137-4776-8ff8-73e274c43a0c/lesson/daa33f27-f6d7-4097-9031-d12fe74deac9)
