# label = "BackupVolume"
```

To update the label:

```bash theme={null}
sudo xfs_admin -L "FirstFS" /dev/sdb1
# writing all SBs
# new label = "FirstFS"
```

***

## Formatting with ext4

ext4 is widely supported and offers robust data integrity features.

<Callout icon="lightbulb">
  `mkfs.ext4` is a convenient alias for `mke2fs -t ext4`. You can use either command interchangeably.
</Callout>

### 1. Create an ext4 Filesystem

Format `/dev/sdb2` with default ext4 options:

```bash theme={null}
sudo mkfs.ext4 /dev/sdb2
```

### 2. Read the Manual

Inspect available flags like `-L` (label) and `-N` (inode count):

```bash theme={null}
man mkfs.ext4
```

### 3. Set a Custom Label and Inode Count

If your workload involves many small files, increase the inode count:

```bash theme={null}
sudo mkfs.ext4 -L "BackupVolume" -N 500000 /dev/sdb2
```

Sample output:

```text theme={null}
mke2fs 1.45.6 (20-Mar-2020)
Creating filesystem with 1048576 4k blocks and 500224 inodes
Filesystem UUID: 903a4d4d-af29-4bf3-9fad-1dfdd0cd9f39
Superblock backups stored on blocks:
    32768, 98304, 163840, 229376, 294912, 819200, 884736
Allocating group tables: done
Writing inode tables: done
Creating journal (16384 blocks): done
Writing superblocks and filesystem accounting information: done
```

### 4. Examine and Tune ext4

List parameters and check the label:

```bash theme={null}
sudo tune2fs -l /dev/sdb2
sudo tune2fs -l /dev/sdb2 | grep 'Filesystem volume name'
# Filesystem volume name:   BackupVolume
```

To change the label:

```bash theme={null}
sudo tune2fs -L "SecondFS" /dev/sdb2
```

Verify:

```bash theme={null}
sudo tune2fs -l /dev/sdb2 | grep 'Filesystem volume name'
# Filesystem volume name:   SecondFS
```

***

## References

* [XFS Filesystem How-To](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/managing_file_systems/assembly_xfs-file-system-managing-file-systems)
* [ext4 on Kernel.org](https://www.kernel.org/doc/html/latest/filesystems/ext4/index.html)
* [tune2fs Manual Page](https://linux.die.net/man/8/tune2fs)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/de71b96a-9dc0-4e92-987a-6c7055c44e8b/lesson/848cb6cb-8ee4-4e9e-adb6-ad26632d9cab" />
</CardGroup>


# Create Partitions and Filesystems btrfs

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/Devices-Linux-Filesystems-Filesystem-Hierarchy-Standard/Create-Partitions-and-Filesystems-btrfs/page

This guide teaches how to create, manage, and optimize Btrfs volumes on Linux, covering single-device setups to multi-disk RAID configurations.

In this comprehensive guide, you’ll learn how to build, manage, and optimize Btrfs (B-tree file system) volumes on Linux. We cover everything from one-device setups to multi-disk RAID configurations, subvolumes, snapshots, and transparent compression.

## Btrfs Overview

Btrfs is a modern copy-on-write (COW) filesystem designed for Linux environments with large storage needs, multiple disks, or advanced snapshot requirements. Its core capabilities include:

| Feature                        | Description                                                                      |
| ------------------------------ | -------------------------------------------------------------------------------- |
| Multi-device support           | RAID-like layouts: `single`, `dup`, `raid0`, `raid1`, `raid5`, `raid6`, `raid10` |
| Transparent compression        | ZLIB, LZO, ZSTD algorithms for on-the-fly data reduction                         |
| SSD optimizations              | TRIM support, reduced fragmentation                                              |
| Snapshots & incremental backup | Create point-in-time subvolume copies for quick rollback and backup              |
| Online defragmentation         | Defragment without unmounting                                                    |
| Subvolumes with quotas         | Isolate datasets, enforce per-subvolume space limits                             |
| Deduplication                  | Post-process or realtime block dedupe                                            |

<Callout icon="lightbulb">
  When modifying data, COW filesystems write new data to free space, update metadata, then discard the old blocks. This preserves data integrity across crashes.
</Callout>

<Frame>
  ![The image explains the difference between traditional filesystems and copy-on-write filesystems, highlighting how new data is written and managed. Traditional filesystems overwrite old data directly, while copy-on-write filesystems write new data to free space and update metadata before removing old data.](../../../../images/kodekloud.com/kk-media/image/upload/v1752881380/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Create-Partitions-and-Filesystems-btrfs/filesystems-traditional-vs-copy-on-write.jpg)
</Frame>

## 1. Creating a Btrfs Filesystem

### 1.1 Single-Device Setup

Initialize a simple Btrfs volume on `/dev/sdb1`:

```bash theme={null}
sudo mkfs.btrfs /dev/sdb1
```

Add a human-readable label:

```bash theme={null}
sudo mkfs.btrfs -L "New Disk" /dev/sdb1
```

<Callout icon="triangle-alert">
  Changing labels on a mounted filesystem can cause mount failures. Always unmount before relabeling.
</Callout>

### 1.2 Multi-Device & RAID Profiles

Expand a Btrfs pool across `/dev/sdb` and `/dev/sdc`:

```bash theme={null}
sudo mkfs.btrfs \
  -d raid1 \
  -m raid1 \
  -L "MirrorPool" \
  /dev/sdb /dev/sdc
```

| Profile | Data Layout   | Use Case                          |
| ------- | ------------- | --------------------------------- |
| single  | No redundancy | Tests, single-disk volumes        |
| dup     | Metadata only | Protect metadata on single device |
| raid0   | Striping      | Max performance, no redundancy    |
| raid1   | Mirroring     | Redundancy, small pools           |
| raid5/6 | Parity        | Large pools, high capacity        |
| raid10  | Stripe+Mirror | Performance + redundancy          |

## 2. Subvolumes

Subvolumes are independent namespaces within a Btrfs filesystem—each with its own snapshots and quotas.

1. Mount the main volume:

   ```bash theme={null}
   sudo mount /dev/sdb1 /mnt/disk
   ```

2. Create a subvolume named `BKP`:

   ```bash theme={null}
   sudo btrfs subvolume create /mnt/disk/BKP
   ```

3. Verify the listing:

   ```bash theme={null}
   ls -lh /mnt/disk/
   # drwxr-xr-x 1 root root   0 Jul 13 17:35 BKP
   # drwxrwxr-x 1 carol carol 988 Jul 13 17:30 Images
   ```

4. Inspect subvolume metadata:

   ```bash theme={null}
   sudo btrfs subvolume show /mnt/disk/BKP
   # Name:               BKP
   # UUID:               e90a14fe-69fa-da4f-9764-3384f66fa32e
   # Subvolume ID:       260
   # Creation time:      2019-07-13 17:35:40 -0300
   ```

## 3. Mounting a Specific Subvolume

To mount `BKP` directly:

```bash theme={null}
sudo mount -t btrfs \
  -o subvol=BKP \
  /dev/sdb1 /mnt/BKP
```

## 4. Snapshots

Snapshots capture a subvolume’s state at a specific point in time. They are instant, space-efficient, and independent from ongoing changes.

### 4.1 Create a Read-Write Snapshot

```bash theme={null}
sudo btrfs subvolume snapshot /mnt/disk /mnt/disk/snap
```

### 4.2 Verify & Test

Remove some files from the live subvolume:

```bash theme={null}
rm /mnt/disk/LG-G8S-ThinQ-*
```

Original data remains intact in the snapshot:

```bash theme={null}
ls -lh /mnt/disk/snap/
