# /etc/fstab: static file system information.
#
# Use 'blkid' to print the universally unique identifier for a
# device; this may be used with UUID= as a more robust way to name devices
# that works even if disks are added and removed. See fstab(5).
/dev/sda1  /  ext4  defaults,relatime,errors=panic  0  1
```

<Callout icon="lightbulb">
  In the fstab entry:

  * The first field indicates the device or filesystem.
  * The second field specifies the directory where the file system is mounted.
  * The third field designates the type of file system, here ext4.
  * The fourth field lists mount options. A commonly used option is `rw`, which mounts the file system in read-write mode.
  * The fifth field (often set to zero) indicates whether a dump backup is scheduled.
  * The sixth field determines the order in which file systems are checked during boot-up; a `0` means the check is skipped, while `1` is typically reserved for the root filesystem.
</Callout>

## Hands-On Lab

Now it's your turn to experiment further with Linux file systems. Try creating, mounting, and configuring automatic mounting for an ext4 file system on your Linux environment to reinforce your learning.

Explore more Linux fundamentals with other guides and practical labs to deepen your understanding of modern file system management.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/learning-linux-basics-course-labs/module/e0021af2-9983-4bde-97a2-29255d3ea1da/lesson/6888ecca-2804-4606-8127-a5f1b0f1d651" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/learning-linux-basics-course-labs/module/e0021af2-9983-4bde-97a2-29255d3ea1da/lesson/9b574ed0-5a82-4c32-abf6-b4fe00c9459f" />
</CardGroup>


# LVM

Source: https://notes.kodekloud.com/docs/Learning-Linux-Basics-Course-Labs/Storage-in-Linux/LVM/page

This article provides an overview of Logical Volume Manager (LVM) and guides users through its setup and management.

In this lesson, we explore the Logical Volume Manager (LVM), a powerful tool that enables you to group multiple physical volumes (disks or partitions) into a single volume group (VG). From the volume group, you can then allocate one or more logical volumes (LVs). While our example uses three partitions, LVM is flexible enough to work with a single disk, multiple disks, or even an unlimited number of partitions grouped under a single VG.

<Callout icon="lightbulb">
  One of LVM’s most significant advantages is its ability to resize logical volumes dynamically, provided there is sufficient free space in the volume group. This feature is especially useful for systems with changing storage requirements.
</Callout>

## Prerequisites

Before you begin, ensure that the LVM2 package is installed on your system. Use the command below to install LVM2:

```bash theme={null}
apt-get install lvm2
```

## Step 1: Create a Physical Volume

The initial step in configuring LVM is to identify available disks or partitions and create physical volumes (PVs) from them. A physical volume represents the disk or partition in LVM.

For example, to create a physical volume on the device path `/dev/sdb`, execute:

```bash theme={null}
pvcreate /dev/sdb
```

Expected output:

```text theme={null}
Physical volume "/dev/sdb" successfully created
```

## Step 2: Create a Volume Group

Once the physical volume is established, create a volume group (VG) that will host your logical volumes. In this example, the VG is named `caleston_vg` and includes `/dev/sdb`:

```bash theme={null}
vgcreate caleston_vg /dev/sdb
```

Expected output:

```text theme={null}
Volume group "caleston_vg" successfully created
```

To display details about the physical volume, run:

```bash theme={null}
pvdisplay
```

Sample output:

```text theme={null}
--- Physical volume ---
PV Name               /dev/sdb
VG Name               caleston_vg
PV Size               20.00 GiB / not usable 3.00 MiB
Allocatable           yes
PE Size               4.00 MiB
Total PE              5119
Free PE               5119
Allocated PE          0
PV UUID               iDCXIN-En2h-5IlJ-Yjqv-GcsR-gDfV-zaf66E
```

For further information about the volume group, use:

```bash theme={null}
vgdisplay
```

Sample output:

```text theme={null}
--- Volume group ---
VG Name               caleston_vg
System ID             LVM2-XXXXXX
Format                lvm2
Metadata Areas        1
Metadata Sequence No  1
VG Access             read/write
VG Status             resizable
MAX LV                0
Cur LV                0
Open LV               0
Max PV                0
Cur PV                1
Act PV                1
VG Size               20.00 GiB
PE Size               4.00 MiB
Total PE              5119
Alloc PE / Size       0 / 0
Free PE / Size        5119 / 20.00 GiB
VG UUID               VzmIAn-9cEl5bA-lVtm-wHKX-KQaObR
```

## Step 3: Create a Logical Volume

After establishing the volume group, create a logical volume (LV). In this example, we create a 1GB LV named `vol1` within the `caleston_vg` volume group:

```bash theme={null}
lvcreate -L 1G -n vol1 caleston_vg
```

Expected output:

```text theme={null}
Logical volume "vol1" created.
```

To verify that the LV was created successfully, list all logical volumes:

```bash theme={null}
lvs
```

Sample output:

```text theme={null}
LV      VG          Attr       LSize   Pool
vol1    caleston_vg -wi-a----- 1.00g
```

## Step 4: Create and Mount a Filesystem

With your logical volume in place, the next step is to create a filesystem on it. In this example, we create an ext4 filesystem on `/dev/caleston_vg/vol1`:

```bash theme={null}
mkfs.ext4 /dev/caleston_vg/vol1
```

After the filesystem is created, mount it to a directory (e.g., `/mnt/vol1`) to make it accessible:

```bash theme={null}
mount -t ext4 /dev/caleston_vg/vol1 /mnt/vol1
```

## Step 5: Resize the Logical Volume and Filesystem

Sometimes you may need to expand the logical volume while it remains mounted. Begin by verifying that there is sufficient free space in the volume group:

```bash theme={null}
vgs
```

Sample output:

```text theme={null}
 VG           #PV #LV #SN Attr   VSize  VFree
 caleston_vg   1  1   1   0 wz--n- 20.00g 19.00g
```

If there is enough free space, extend the logical volume by an additional 1GB:

```bash theme={null}
lvresize -L +1G /dev/caleston_vg/vol1
```

Expected output:

```text theme={null}
Logical volume vol1 successfully resized.
```

<Callout icon="triangle-alert">
  At this stage, even after resizing the logical volume, the filesystem will still report its original size (1GB) when using the `df` command because only the LV has been extended. It is essential to also resize the filesystem with the `resize2fs` command.
</Callout>

Resize the filesystem using:

```bash theme={null}
resize2fs /dev/caleston_vg/vol1
```

The output will indicate that the filesystem has been resized. Finally, verify the new filesystem size:

```bash theme={null}
df -hP /mnt/vol1
```

Sample output:

```text theme={null}
Filesystem                      Size  Used Avail Use% Mounted on
/dev/mapper/caleston_vg-vol1     2.0G  1.6M  1.9G   1% /mnt/vol1
```

## Access Paths for the Logical Volume

It’s important to note that the logical volume can be accessed through two different paths:

* /dev/caleston\_vg/vol1
* /dev/mapper/caleston\_vg-vol1

Both paths refer to the same logical volume, so you can use either interchangeably in your commands and configurations.

## Conclusion

This lesson has walked you through the fundamental steps of setting up and managing LVM—from creating physical volumes and volume groups to creating, mounting, and resizing logical volumes and filesystems. Regular practice of these operations will help solidify your understanding of LVM's flexibility and scalability.

For further reading and advanced concepts, consider exploring additional resources:

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/learning-linux-basics-course-labs/module/e0021af2-9983-4bde-97a2-29255d3ea1da/lesson/f6fac38a-495f-42a6-b4a1-3fcc2f8375ac" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/learning-linux-basics-course-labs/module/e0021af2-9983-4bde-97a2-29255d3ea1da/lesson/edd2515f-a32d-41b2-9299-eedfa62eb676" />
</CardGroup>
