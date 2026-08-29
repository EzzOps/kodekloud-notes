# file: examplefile
# owner: adm
# group: ftp
user::rw-
user:aaron:rw-
group::rw-
mask::rw-
other::r--
[aaron@LFCS-CentOS attributes]$
```

The mask setting defines the maximum permissions available to users and groups affected by ACLs. This means that even if an ACL grants extended permissions, the effective permissions will be restricted by the mask. To enforce read-only access despite broader ACL entries, set the mask to `r--`:

```bash theme={null}
sudo setfacl --modify mask:r-- examplefile
getfacl examplefile
```

## Modifying ACLs for Groups and Removing ACL Entries

ACLs can also apply to groups. To grant the "wheel" group read and write access, execute:

```bash theme={null}
sudo setfacl --modify group:wheel:rw examplefile
```

If you need to restrict a user’s permissions completely (for example, to deny Aaron Lockhart any access), set his permissions to none:

```bash theme={null}
sudo setfacl --modify user:aaron:--- examplefile
```

Should you wish to remove a specific ACL entry entirely, use the `--remove` option:

```bash theme={null}
sudo setfacl --remove user:aaron examplefile
```

Similarly, to remove a group ACL entry:

```bash theme={null}
sudo setfacl --remove group:wheel examplefile
```

## Applying ACLs Recursively

In cases where you need to update ACLs for an entire directory and its contents, utilize the recursive flag (`--recursive` or `-R`). For example, to grant Aaron full permissions on all files within directory `dir1`:

```bash theme={null}
mkdir dir1
sudo setfacl --recursive -m user:aaron:rwx dir1/
```

To remove an ACL entry recursively from a directory:

```bash theme={null}
sudo setfacl --recursive --remove user:aaron dir1/
```

## Managing File and Directory Attributes

Beyond ACLs, Linux file systems support attributes that serve as on/off switches to control file behavior. Two frequently used attributes are append-only and immutable.

### Append-Only Attribute

First, create a new file with initial content:

```bash theme={null}
echo "This is old content" > newfile
```

To enable the append-only attribute, use `chattr` with the `+a` flag. With this attribute active, you can append data but cannot overwrite the file's existing contents:

```bash theme={null}
sudo chattr +a newfile
```

Verifying the content:

```bash theme={null}
cat newfile
```

Attempting to overwrite the file:

```bash theme={null}
echo "Replace with this content" > newfile
# Output: bash: newfile: Operation not permitted
```

Appending new content is allowed:

```bash theme={null}
echo "Replace with this content" >> newfile
cat newfile
```

To remove the append-only attribute, use:

```bash theme={null}
sudo chattr -a newfile
```

### Immutable Attribute

When a file is marked as immutable (indicated by the letter `i`), it becomes completely unmodifiable—even root cannot delete or alter the file. To set the immutable attribute:

```bash theme={null}
sudo chattr +i newfile
```

Any attempt to remove the file, even with elevated privileges, will result in an error:

```bash theme={null}
sudo rm newfile
# Output: rm: cannot remove 'newfile': Operation not permitted
```

To view file attributes, run:

```bash theme={null}
lsattr newfile
```

Expected output:

```bash theme={null}
[aaron@LFCS-CentOS attributes]$ lsattr newfile
----i------------ newfile
[aaron@LFCS-CentOS attributes]$
```

Remove the immutable attribute with:

```bash theme={null}
sudo chattr -i newfile
```

For further information on available attributes beyond append-only and immutable, refer to the manual page for `chattr`. Note that some attributes may have no effect, depending on your file system type. For instance, the `c` attribute for compression does not work on file systems such as ext4 that do not support on-the-fly compression.

![The image shows a terminal window displaying a manual page for the chattr command, detailing file attributes like 'C', 'd', and 'D'.](https://kodekloud.com/kk-media/image/upload/v1752883549/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-Create-manage-and-diagnose-advanced-file-system-permissions/chattr-command-manual-terminal.jpg)

> **lightbulb** Always verify your file system's support for specific attributes to avoid unexpected behavior. Explore `man chattr` for a detailed list.

## Conclusion

This tutorial provided an in-depth look at managing advanced file system permissions and attributes in Linux. You learned how to work with standard file permissions, leverage ACLs to grant specific user and group privileges, and handle additional file attributes like append-only and immutable. Continue practicing these commands in your lab exercises to enhance your proficiency in Linux system management.

For more detailed information, consider exploring additional resources:

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

Happy learning!

- [Watch Video](https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/207496ef-0e82-42c8-aa9d-7996cfb968a6/lesson/933069b6-15b3-4dd4-9898-59f54ba83874)


# List create delete and modify physical storage partitions

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Configure-Local-Storage/List-create-delete-and-modify-physical-storage-partitions/page

This guide covers essential commands and utilities for managing physical storage partitions in Linux, including listing, creating, deleting, and modifying disk partitions.

Welcome to our comprehensive guide on managing physical storage partitions in Linux. This lesson covers essential commands and interactive utilities to list, create, delete, and modify disk partitions. Whether you’re setting up a dual-boot system or reorganizing storage, this guide will help you understand and implement proper partition management.

## Understanding Disk Partitions

Disk partitions divide a physical storage device into discrete sections to isolate different file systems. For example, if you have a 2TB solid-state drive intended for both Windows and Linux, you cannot mix the NTFS file system (used by Windows) with Linux file systems like ext4 on a single continuous volume. Instead, you’d allocate separate partitions—for instance, 1TB for Windows and 1TB for Linux—so each operating system uses its dedicated partition.

## Viewing Partitions with lsblk

The `lsblk` command lists block devices and their partitions. In the output, look for entries with "part" under the TYPE column to identify actual partitions. Consider the following example:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda    8:0    0   20G  0 disk
├─sda1 8:1    0    1G  0 part /boot
├─sda2 8:2    0   19G  0 part
├─cs-root 253:0 0   17G  0 lvm  /
└─cs-swap 253:1 0    2G  0 lvm  [SWAP]
sdb    8:16   0   10G  0 disk
sr0   11:0    1 1024M  0 rom
[aaron@LFCS-CentOS ~]$
```

Here, the primary disk `sda` includes partitions (`sda1` and `sda2`) along with LVM volumes (`cs-root` and `cs-swap`). Disk names might vary in virtual environments (e.g., starting with "v"), so always refer to the TYPE column to distinguish between entire devices and their partitions.

> **lightbulb** Remember: `/dev/sda1` specifically accesses the first partition on `/dev/sda`, while `/dev/sda` refers to the whole disk.

You can verify device file usage with this repeated `lsblk` command:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ lsblk
NAME        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda           8:0    0   20G  0 disk 
├─sda1        8:1    0    1G  0 part /boot
├─sda2        8:2    0   19G  0 part 
├─cs-root   253:0    0   17G  0 lvm  /
└─cs-swap   253:1    0    2G  0 lvm  [SWAP]
sdb           8:16   0   10G  0 disk 
sr0          11:0    1 1024M  0 rom  
[aaron@LFCS-CentOS ~]$
```

## Examining Partitions with fdisk

The `fdisk` utility is a powerful tool for displaying and altering disk partition tables. To list the partitions on a specific device (for example `/dev/sda`), run:

```bash theme={null}
sudo fdisk --list /dev/sda
```

The output includes detailed information such as sector size. If your output shows a 512-byte sector size and the first partition starts at sector 2048, the calculation (2048 × 512) confirms a 1,048,576-byte (1MB) offset reserved for a bootloader. For disks with a sector size of 4,096 bytes, the calculation adjusts accordingly.

> **triangle-alert** Modifying partition tables requires elevated privileges. Double-check the device names and calculations to prevent data loss.

## Interactive Partitioning using cfdisk

For a more intuitive management experience, `cfdisk` provides an interactive text-based interface. In this example, an additional storage device (`/dev/sdb`) is attached to a virtual machine. Start by running:

```bash theme={null}
sudo cfdisk /dev/sdb
```

Depending on your setup, the additional disk might be represented as `/dev/sdb` or `/dev/vdb`. In our guide, we assume `/dev/sdb`.

### Choosing a Partition Table: MBR vs. GPT

When beginning with `cfdisk`, you are prompted to choose a partition table type. Historically, the Master Boot Record (MBR) was common, but modern setups typically favor the GUID Partition Table (GPT) due to its support for more partitions and larger drives.

![The image shows a terminal window on a CentOS system prompting the user to select a partition label type, with options like GPT, DOS, SGI, and SUN.](https://kodekloud.com/kk-media/image/upload/v1752883550/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-List-create-delete-and-modify-physical-storage-partitions/centos-terminal-partition-labels.jpg)

### Creating and Adjusting Partitions with cfdisk

Imagine partitioning a 10GB drive into two sections:

* 8GB for a new operating system.
* 2GB dedicated to swap space.

Follow these steps in `cfdisk`:

1. Navigate to the free space using the arrow keys and select “New.”
2. Specify an 8G partition size (using a capital “G” to denote gigabytes) and press Enter.
3. Navigate to the remaining free space to create a 2G partition.

At this point, you have established two partitions: SDB1 (8GB) and SDB2 (2GB). Later, if you decide to create a third partition, you can resize an existing partition. For example, reducing the 8GB partition to 4GB frees additional space, allowing the creation of three partitions:

* SDB1 as 4GB
* SDB2 as 2GB
* SDB3 as 4GB

Note that partition numbers are assigned based on creation order rather than physical disk locations.

![The image shows a terminal window displaying disk partition information for /dev/sdb, listing three partitions with their sizes and types. The interface includes options for managing the partitions, such as delete, resize, and quit.](https://kodekloud.com/kk-media/image/upload/v1752883552/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-List-create-delete-and-modify-physical-storage-partitions/disk-partition-info-dev-sdb.jpg)

To reorder partitions according to their physical position, select the “Sort” option. After sorting, SDB1 remains 4GB, SDB2 becomes 4GB, and SDB3 (now at the end of the disk) functions as a 2GB swap partition. You may also delete and recreate partitions at any time using the “Delete” and “New” options, noting that these changes remain tentative until committed.

### Changing a Partition’s Type

Before committing the changes, you might need to adjust a partition’s type. For example, to designate SDB3 (the 2GB partition) as swap space, navigate to it and press the “Type” button. Then select “Linux swap” from the menu and confirm by pressing Enter.

![The image shows a terminal window on a CentOS system with a menu for selecting a partition type, highlighting "Linux swap."](https://kodekloud.com/kk-media/image/upload/v1752883553/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-List-create-delete-and-modify-physical-storage-partitions/centos-terminal-partition-linux-swap.jpg)

By default, partitions are created with a standard Linux file system type suitable for data storage. Changing the partition type is particularly useful when setting up swap areas or specific boot partitions (like EFI system partitions).

### Committing Your Partition Changes

All modifications you make in `cfdisk` are provisional until you commit them. This feature allows you to review your changes and cancel if necessary. When ready, press the “Write” button (or similar) to apply the modifications. The tool will prompt for confirmation—type “Yes” and press Enter to proceed.

![The image shows a terminal window displaying disk partition information for /dev/sdb, including details about three partitions with their sizes and types. It prompts the user to confirm writing the partition table to disk.](https://kodekloud.com/kk-media/image/upload/v1752883554/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-List-create-delete-and-modify-physical-storage-partitions/disk-partition-info-dev-sdb-2.jpg)

Once the partition table is committed, exit `cfdisk` by selecting “Quit.” Running the `lsblk` command again should display the updated partition layout similar to the following:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda      8:0    0   20G  0 disk 
├─sda1   8:1    0    1G  0 part /boot
├─sda2   8:2    0   19G  0 part 
├─cs-root 253:0  0   17G  0 lvm  /
└─cs-swap 253:1  0    2G  0 lvm  [SWAP]
sdb      8:16   0   10G  0 disk 
├─sdb1   8:17   0    4G  0 part 
├─sdb2   8:18   0    4G  0 part 
└─sdb3   8:19   0    2G  0 part 
sr0     11:0    1 1024M  0 rom  
[aaron@LFCS-CentOS ~]$
```

## Summary

In this guide, you learned how to:

* Use `lsblk` to view existing disk partitions and understand device naming.
* Employ `fdisk` to examine detailed partition information and perform calculations related to sector sizes.
* Utilize `cfdisk` for an interactive approach to creating, deleting, resizing, and modifying partitions.
* Choose between MBR and GPT partition tables based on your system’s requirements.
* Commit changes safely after reviewing your planned partition layout.

> **lightbulb** Properly managing disk partitions is crucial for maintaining system stability and data integrity. Always back up any critical data before making significant changes to your disk structure.

Thank you for following this guide. Continue to explore additional lectures and labs to deepen your understanding of Linux storage management.

- [Watch Video](https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/207496ef-0e82-42c8-aa9d-7996cfb968a6/lesson/e6047763-d2b7-49a3-b096-ff36647fdf02)
