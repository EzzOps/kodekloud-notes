# Design Hard Disk Layout LVM

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/Linux-Installation-and-Package-Management/Design-Hard-Disk-Layout-LVM/page

This article provides a comprehensive guide on configuring and managing LVM storage in Linux, covering installation, volume creation, resizing, and filesystem formatting.

Welcome to our in-depth guide on configuring and managing LVM (Logical Volume Manager) storage in Linux. LVM provides dynamic volume resizing, flexible disk pooling, and snapshot capabilities, making it a powerful tool for system administrators.

## What You’ll Learn

* Installing LVM utilities
* Key LVM components: PV, VG, LV, PE
* Creating Physical Volumes (PV)
* Building and extending Volume Groups (VG)
* Allocating and resizing Logical Volumes (LV)
* Formatting and resizing filesystems
* Common commands and handy tips

## Prerequisites

We’ve attached three new 5 GiB virtual disks to our CentOS VM. If you haven’t installed the LVM tools yet, run:

```bash theme={null}
sudo dnf install lvm2
```

<Callout icon="lightbulb">
  Most LVM operations require root privileges. Prepend `sudo` or switch to the root user before proceeding.
</Callout>

***

## LVM Abbreviations

| Resource             | Description                          | Command Prefix |
| -------------------- | ------------------------------------ | -------------- |
| Physical Volume (PV) | A disk or partition managed by LVM   | `pv*`          |
| Volume Group (VG)    | A pool of one or more PVs            | `vg*`          |
| Logical Volume (LV)  | A virtual partition carved from a VG | `lv*`          |
| Physical Extent (PE) | The smallest allocation unit in LVM  | n/a            |

***

## 1. Creating Physical Volumes (PV)

Physical Volumes are the foundation of LVM. You can use entire disks or partitions.

1. Scan for available disks and existing PVs:
   ```bash theme={null}
   sudo lvmdiskscan
   ```
   Sample output:
   ```text theme={null}
   /dev/sda1  [   1.00 GiB]
   /dev/sda2  [ <19.00 GiB] LVM physical volume
   /dev/sdb1  [   4.00 GiB]
   /dev/sdc   [   5.00 GiB]
   /dev/sdd   [   5.00 GiB]
   /dev/sde   [   5.00 GiB]
   3 disks
   1 LVM physical volume
   ```

2. Initialize `/dev/sdc` and `/dev/sdd` as new PVs:
   ```bash theme={null}
   sudo pvcreate /dev/sdc /dev/sdd
   ```

3. Verify all PVs:
   ```bash theme={null}
   sudo pvs
   ```
   ```text theme={null}
     PV         VG         Fmt  Attr PSize   PFree
     /dev/sda2  cs         lvm2 a--  <19.00g    0
     /dev/sdc   lvm2 ---   5.00g  5.00g
     /dev/sdd   lvm2 ---   5.00g  5.00g
   ```

`PFree` indicates unallocated space ready for LVs.

***

## 2. Building a Volume Group (VG)

Volume Groups aggregate one or more PVs into a single storage pool.

1. Create a VG named **my\_volume**:
   ```bash theme={null}
   sudo vgcreate my_volume /dev/sdc /dev/sdd
   ```
   ```text theme={null}
   Volume group "my_volume" successfully created
   ```

2. To extend the VG later, initialize another PV:
   ```bash theme={null}
   sudo pvcreate /dev/sde
   ```

3. Add it to **my\_volume**:
   ```bash theme={null}
   sudo vgextend my_volume /dev/sde
   ```

4. List all VGs:
   ```bash theme={null}
   sudo vgs
   ```
   ```text theme={null}
     VG          #PV #LV #SN Attr   VSize   VFree
     cs           1   2   0 wz--n  <19.00g    0
     my_volume    3   0   0 wz--n  14.99g 14.99g
   ```

### Removing a PV from a VG

1. Detach `/dev/sde`:
   ```bash theme={null}
   sudo vgreduce my_volume /dev/sde
   ```
2. Wipe its metadata:
   ```bash theme={null}
   sudo pvremove /dev/sde
   ```

***

## 3. Allocating Logical Volumes (LV)

Logical Volumes are like partitions within a VG.

1. Create a 2 GiB LV called **partition1**:
   ```bash theme={null}
   sudo lvcreate --size 2G --name partition1 my_volume
   ```
2. Create a 6 GiB LV called **partition2**:
   ```bash theme={null}
   sudo lvcreate --size 6G --name partition2 my_volume
   ```
3. View all LVs:
   ```bash theme={null}
   sudo lvs
   ```
   ```text theme={null}
     LV         VG         Attr       LSize
     partition1 my_volume -wi-a----- 2.00g
     partition2 my_volume -wi-a----- 6.00g
   ```
4. Check remaining VG space:
   ```bash theme={null}
   sudo vgs
   ```
   ```text theme={null}
     VG         #PV #LV #SN Attr   VSize   VFree
     my_volume   2   2   0 wz--n-  9.99g  1.99g
   ```

***

## 4. Resizing Logical Volumes

LVM data is allocated in Physical Extents (PE). You can grow or shrink LVs by adjusting their extents.

### Grow to Fill Free Space

Expand **partition1** to consume all free extents:

```bash theme={null}
sudo lvresize --extents +100%FREE /dev/my_volume/partition1
```

### Shrink Back

Reduce **partition1** back to 2 GiB:

```bash theme={null}
sudo lvresize --size 2G /dev/my_volume/partition1
```

<Callout icon="triangle-alert">
  Shrinking a filesystem without shrinking the filesystem itself first can lead to data loss. Always unmount, run a filesystem check, and resize the filesystem before reducing an LV.
</Callout>

***

## 5. Formatting the Filesystem

Before storing data, format your LV. For example, to use XFS:

```bash theme={null}
sudo mkfs.xfs /dev/my_volume/partition1
```

***

## 6. Resizing with an Existing Filesystem

To grow both the LV and its filesystem in one command:

```bash theme={null}
sudo lvresize --resizefs --size 3G /dev/my_volume/partition1
```

> Note: Not all filesystems support online shrinking. Check your filesystem’s documentation.

***

## 7. Handy Tips & Resources

* Browse the full LVM manual:
  ```bash theme={null}
  man lvm
  ```
* Use tab-completion to explore subcommands:
  ```bash theme={null}
  vg↹↹
  ```
* Always back up critical data before performing volume operations.

***

## Links and References

* [LVM Documentation](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/logical_volume_manager_administration/)
* [mkfs.xfs Man Page](https://linux.die.net/man/8/mkfs.xfs)
* [KVM Virtual Disks](https://www.linux-kvm.org/page/Storage)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/78ca0fa8-2083-408a-bf8a-2775b09fbf1d/lesson/4350fea4-2189-46b2-9859-6e9d25cc902c" />
</CardGroup>
