# Create mount unmount and use vfat file systems

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Create-and-Configure-File-Systems/Create-mount-unmount-and-use-vfat-file-systems/page

This guide covers creating, mounting, unmounting, and using VFAT file systems for cross-platform storage compatibility.

VFAT (Virtual File Allocation Table) is popular for its cross-platform compatibility, making it ideal for sharing storage between Windows, Linux, and other operating systems. This guide walks you through partitioning a storage device, creating a VFAT file system, mounting it, configuring automatic mounting at boot, and safely unmounting it.

## Step 1: Partitioning for VFAT

Begin by partitioning your storage device. When using the fdisk utility, change the partition type to designate it for W95 FAT32 (VFAT). Use the following steps:

```bash theme={null}
sudo fdisk /dev/vdb
