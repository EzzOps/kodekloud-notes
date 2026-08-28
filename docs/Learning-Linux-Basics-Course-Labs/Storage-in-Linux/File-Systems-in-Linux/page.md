# File Systems in Linux

Source: https://notes.kodekloud.com/docs/Learning-Linux-Basics-Course-Labs/Storage-in-Linux/File-Systems-in-Linux/page

This article explains creating and managing file systems in Linux, focusing on ext2, ext3, and ext4 file systems.

This article explains how to make a disk usable in Linux by creating file systems. After partitioning divides a disk into segments of usable space, the Linux kernel still treats these partitions as raw disk areas. To read and write data, you must create a file system that defines the storage structure and then mount that file system to a directory.

In this guide, we focus on the extended file system family: ext2, ext3, and ext4.

## Comparing ext2, ext3, and ext4

Both ext2 and ext3 file systems support a maximum file size of 2 TB and a maximum volume size of 4 TB. While they efficiently store data, ext2 may experience long boot times after an unclean shutdown (for example, due to a power outage). In contrast, ext3 adds journaling features that enable a faster system startup following such events. Ext4 further enhances these capabilities and is one of the most popular general-purpose file systems today—it supports files up to 16 TB and volumes as large as 1 exabyte. Additionally, ext4 (as well as ext3) offers backward compatibility: a file system created with ext4 can be mounted as ext3 or ext2, and an ext3 file system can be mounted as ext2.

<Frame>
  ![The image compares Linux filesystems EXT2, EXT3, and EXT4, highlighting file size, volume size, features like journaling, compression, and compatibility.](https://kodekloud.com/kk-media/image/upload/v1752881151/notes-assets/images/Learning-Linux-Basics-Course-Labs-File-Systems-in-Linux/frame_100.jpg)
</Frame>

## Creating and Mounting an ext4 File System

Follow these steps to create an ext4 file system on the device /dev/sdb1:

1. Use the `mkfs.ext4` command to format the device.
2. Create a mount point directory.
3. Mount the file system.

```bash theme={null}
[~]$ mkfs.ext4 /dev/sdb1
Allocating group tables: done
Writing inode tables: done
Creating journal (32768 blocks): done
Writing superblocks and filesystem accounting information: done

[~]$ mkdir /mnt/ext4
[~]$ mount /dev/sdb1 /mnt/ext4
```

### Verifying the Mounted File System

You can confirm that the file system is mounted correctly by using the `mount` command combined with `grep`:

```bash theme={null}
[~]$ mount | grep /dev/sdb1
/dev/sdb1 on /mnt/ext4 type ext4 (rw,relatime,data=ordered)
```

## Configuring Automatic Mounting at Boot

To automatically mount the file system during system boot, add an entry to the `/etc/fstab` file. This enables persistent mounting and ensures the file system is available after a reboot. For example:

```fstab theme={null}
