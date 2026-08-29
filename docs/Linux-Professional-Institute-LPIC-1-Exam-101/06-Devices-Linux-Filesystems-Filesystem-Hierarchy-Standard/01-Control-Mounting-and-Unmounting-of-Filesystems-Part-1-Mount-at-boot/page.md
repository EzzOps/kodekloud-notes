# Control Mounting and Unmounting of Filesystems Part 1 Mount at boot

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/Devices-Linux-Filesystems-Filesystem-Hierarchy-Standard/Control-Mounting-and-Unmounting-of-Filesystems-Part-1-Mount-at-boot/page

Learn to manually mount filesystems, configure automatic mounts at boot, enable swap partitions, and use UUIDs for device identification in Linux.

Linux attaches storage devices to the directory tree by “mounting” them on existing folders. In this guide, you’ll learn how to:

* Manually mount and unmount filesystems
* Configure automatic mounts at boot using `/etc/fstab`
* Enable swap partitions at startup
* Use UUIDs for stable device identification

***

## 1. Manual Mounting and Unmounting

### 1.1 Verify an Empty Mount Point

A common temporary mount directory is `/mnt`. Confirm it’s empty:

```bash theme={null}
ls /mnt/
```

### 1.2 Mount an XFS Filesystem

Assuming you created an XFS filesystem on `/dev/vdb1`, mount it to `/mnt`:

```bash theme={null}
sudo mount /dev/vdb1 /mnt
```

Now `/mnt` is the root of that filesystem. Create a test file and verify:

```bash theme={null}
sudo touch /mnt/testfile
ls -l /mnt/
