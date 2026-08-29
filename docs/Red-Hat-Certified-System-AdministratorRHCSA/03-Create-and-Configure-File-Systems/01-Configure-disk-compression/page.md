# Log the date and time the script was last executed
date >> /tmp/script.log
cat /proc/version >> /tmp/script.log
```

### Setting Permissions and Running Your Script

To create and edit the script using the command line:

```bash theme={null}
$ touch script.sh
$ vim script.sh
```

After saving your file, make it executable by setting the proper permissions. For instance:

```bash theme={null}
$ chmod u+x script.sh
```

Alternatively, to allow anyone to execute the script:

```bash theme={null}
$ chmod +x script.sh
```

You can run the script by either specifying its full path:

```bash theme={null}
$ /home/aaron/script.sh
```

or running it from its directory:

```bash theme={null}
$ ./script.sh
```

After execution, check the contents of `/tmp/script.log`:

```bash theme={null}
$ cat /tmp/script.log
Mon Dec  6 17:06:16 CST 2021
Linux version 4.18.0-348.2.1.el8_5.x86_64
(mockbuild@kbuilder.bsys.centos.org) (gcc version 8.5.0 20210514 (Red Hat 8.5.0-4) (GCC)) #1 SMP Tue Nov 16 14:42:35 UTC 2021
```

This log can be useful for diagnosing issues by correlating system behavior with specific kernel versions.

## Enhancing Your Script with Bash Built-ins

Bash built-ins can add powerful logic to your scripts. To view available built-ins, type:

```bash theme={null}
$ help
```

Two fundamental built-ins are `if` and `test`. In the next example, we archive the contents of the `/etc/dnf` directory and later use conditional logic to manage backups.

### Archiving a Directory

Create a script called "archive-dnf.sh". Use your favorite editor:

```bash theme={null}
$ vim archive-dnf.sh
```

Add the following content with the shebang and a command using `tar` to archive the contents:

```bash theme={null}
#!/bin/bash
tar acf /tmp/archive.tar.gz /etc/dnf
```

Save the file, make it executable, and run it:

```bash theme={null}
$ chmod +x archive-dnf.sh
$ ./archive-dnf.sh
```

Verify that the archive exists:

```bash theme={null}
$ ls /tmp
archive.tar.gz
```

## Improving the Backup with Conditional Logic

Imagine a scenario where files in `/etc/dnf` are accidentally deleted. Running the backup script again would overwrite the existing (and potentially good) backup. To prevent this, modify your script to check if an archive exists. If it does, rename it to `/tmp/archive.tar.gz.OLD` before creating a new archive.

Create a new script named "archive-dnf-2.sh":

```bash theme={null}
$ vim archive-dnf-2.sh
```

Enter the following content:

```bash theme={null}
#!/bin/bash
if test -f /tmp/archive.tar.gz; then
    mv /tmp/archive.tar.gz /tmp/archive.tar.gz.OLD
    tar acf /tmp/archive.tar.gz /etc/dnf/
else
    tar acf /tmp/archive.tar.gz /etc/dnf/
fi
```

> **lightbulb** The `if test -f` construct checks whether the archive file exists as a regular file. If it does, the old archive is renamed before creating a new one.

Make the script executable and run it:

```bash theme={null}
$ chmod +x archive-dnf-2.sh
$ ./archive-dnf-2.sh
```

List the `/tmp` directory to confirm that both the new archive and its backup exist:

```bash theme={null}
$ ls /tmp
archive.tar.gz
archive.tar.gz.OLD
script.log
```

## Using Exit Status in Conditional Statements

Each command returns an exit status code after execution, where `0` indicates success and any non-zero value signals an error. For example, `grep` returns `0` if it finds a match, and `1` if it does not.

Consider the following script that checks if the file `/etc/default/grub` contains the number `5`:

```bash theme={null}
#!/bin/bash
if grep -q '5' /etc/default/grub; then
    echo 'Grub has timeout of 5 seconds.'
else
    echo 'Grub DOES NOT have a timeout of 5 seconds.'
fi
```

Here, the `-q` flag makes `grep` run quietly. Save this script as "check-grub-timeout.sh", make it executable, and run it:

```bash theme={null}
$ vim check-grub-timeout.sh
$ chmod +x check-grub-timeout.sh
$ ./check-grub-timeout.sh
Grub has a timeout of 5 seconds.
```

## Additional Scripting Concepts

These examples illustrate basic Bash scripting techniques using built-in commands. As you progress, you can integrate more advanced features such as loops (`for`, `while`), functions, and variable handling to create more robust scripts.

For a quick scripting refresher, consider reviewing the contents of the `/etc/cron.d/hourly/0anacron` file. This file serves as a practical cheat sheet covering essential scripting conventions, including the shebang and conditional syntax:

```sh theme={null}
#!/bin/sh
# Check whether @anacron was run today already
if test -r /var/spool/anacron/cron.daily; then
    day=`cat /var/spool/anacron/cron.daily`
fi
if [ `date +%Y%m%d` = "$day" ]; then
    exit 0
fi

# Do not run jobs when on battery power
online=1
for psupply in AC ADP0 ; do
    sysfile="/sys/class/power_supply/$psupply/online"
    if [ -f $sysfile ] ; then
        if [ `cat $sysfile 2>/dev/null` = 1 ]; then
            online=1
            break
        else
            online=0
        fi
    fi
done
if [ $online = 0 ]; then
    exit 0
fi
```

For more detailed tutorials and hands-on practice, explore the [Shell Scripts for Beginners](https://learn.kodekloud.com/user/courses/shell-scripts-for-beginners) course on KodeKloud.

![The image is an advertisement for a "Shell Scripts for Beginners" course by KodeKloud, featuring a rocket and penguins on a digital platform, alongside a list of course contents.](https://kodekloud.com/kk-media/image/upload/v1752883566/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-Use-scripting-to-automate-system-maintenance-tasks/shell-scripts-beginners-advertisement.jpg)

This article is now complete. When you are ready for the next lesson, we look forward to seeing you there.

- [Watch Video](https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/9225d80c-3f9d-4e8e-9135-febe7ca37af2/lesson/fd57ea10-0853-41be-aa77-d02578c7f8e1)


# Configure disk compression

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Create-and-Configure-File-Systems/Configure-disk-compression/page

This tutorial explains how to configure disk compression using Virtual Data Optimizer in Linux for effective storage management.

In this tutorial, you'll learn how to configure disk compression using Virtual Data Optimizer (VDO) in Linux. Although storage has become increasingly abundant and affordable, effective storage management remains crucial. VDO optimizes storage use through three key techniques: zero-block filtering, deduplication, and compression. Below, we explain each concept and provide step-by-step instructions to configure VDO on your system.

> **lightbulb** VDO enhances storage performance by filtering out unnecessary data, eliminating redundant blocks, and compressing data in real time.

## Zero-Block Filtering

VDO begins by scanning the storage device for blocks filled only with zeros—data that does not contribute meaningfully to the stored information. This process is similar to draining water from pasta using a colander: the water (empty data) flows away while the pasta (useful data) is retained.

![The image illustrates a "Virtual Data Optimizer (VDO)" process, highlighting "Zero-Block Filtering" with a visual representation of data blocks containing binary numbers.](https://kodekloud.com/kk-media/image/upload/v1752883568/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-Configure-disk-compression/virtual-data-optimizer-zero-block-filtering.jpg)

![The image illustrates a concept of "Zero-Block Filtering" in a "Virtual Data Optimizer (VDO)" with a visual metaphor of a fork and colander with noodles. It also mentions "Deduplication" and "Compression" as part of the process.](https://kodekloud.com/kk-media/image/upload/v1752883569/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-Configure-disk-compression/zero-block-filtering-vdo-fork-colander.jpg)

## Deduplication

Once zero blocks are filtered out, VDO moves on to deduplication. In this step, VDO checks if a block of data is already present elsewhere on the storage device. If a duplicate is found, instead of rewriting the data, VDO updates its metadata to reference the existing block. This method reduces redundant data storage and conserves disk space.

![The image illustrates the Virtual Data Optimizer (VDO) process, highlighting zero-block filtering, deduplication, and compression with a visual representation of data blocks.](https://kodekloud.com/kk-media/image/upload/v1752883571/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-Configure-disk-compression/vdo-process-zero-blocks-deduplication.jpg)

## Compression

The final step in the VDO process is data compression. As data blocks are written to disk, VDO compresses them and packs several compressed blocks into one physical block. This not only saves space but can also improve read performance by reducing the amount of data transferred.

## Installing and Enabling VDO

If VDO is not already installed, you can add it using YUM. Once installed, enable and start the VDO service with systemctl:

```bash theme={null}
sudo yum install vdo
sudo systemctl enable --now vdo.service
```

## Creating a VDO Device

To begin using VDO, you must have a storage device. In this example, we use an unpartitioned device `/dev/vdb` (5 GB in size) and create a VDO device with a logical size of 10 GB:

```bash theme={null}
sudo vdo create --name=vdo_storage --device=/dev/vdb --vdoLogicalSize=10G
```

Explanation of the command options:

* `vdo create`: Initiates the creation of a new VDO-managed device.
* `--name=vdo_storage`: Assigns a name to the new VDO device.
* `--device=/dev/vdb`: Specifies the physical storage device to use.
* `--vdoLogicalSize=10G`: Sets the logical volume size that users will see (10 GB logical, despite a 5 GB physical size).

After creating the VDO device, check its status with:

```bash theme={null}
sudo vdostats --human-readable
```

Expected output:

```bash theme={null}
Device                     Size   Used Available Use% Space saving%
/dev/mapper/vdo_storage    5.0G  3.0G      2.0G 60% N/A
```

Here, the "Size" column reflects the physical capacity while "Use%" indicates current usage. The "Space saving%" field displays N/A until data is written.

## Creating a Filesystem on the VDO Device

Next, create an XFS filesystem on the VDO device. The `-K` option prevents XFS from sending discard requests, which accelerates filesystem creation on an all-zero VDO device:

```bash theme={null}
sudo mkfs.xfs -K /dev/mapper/vdo_storage
sudo udevadm settle
```

After filesystem creation and letting udev settle, check the VDO statistics again:

```bash theme={null}
sudo vdostats --human-readable
```

The updated output should reflect a significant space-saving percentage:

```text theme={null}
Device                     Size   Used Available Use% Space saving%
/dev/mapper/vdo_storage    5.0G  3.0G      2.0G 60% 99%
```

## Mounting the VDO Device

Before mounting the VDO device, create a mount point (e.g., `/mnt/myvdo`) and add an entry to `/etc/fstab` with the necessary options to ensure the VDO service is active before mounting:

```plaintext theme={null}
/dev/mapper/vdo_storage /mnt/myvdo xfs _netdev,x-systemd.device-timeout=0,x-systemd.requires=VDO.service 0 0
```

Then, create the mount point and mount the filesystem:

```bash theme={null}
sudo mkdir /mnt/myvdo
sudo vi /etc/fstab
sudo mount -a
df -h /mnt/myvdo
```

Expected output:

```text theme={null}
Filesystem              Size  Used Avail Use% Mounted on
/dev/mapper/vdo_storage  10G  104M  9.9G  2% /mnt/myvdo
```

Note that the physical size is 5 GB, but the logical size presented to users is 10 GB.

## Demonstrating Deduplication

To observe how VDO conserves disk space via deduplication, follow these steps:

1. Create a 50 MB file with random data:

   ```bash theme={null}
   head -c 50MB /dev/urandom > mydata.txt
   ```

2. Create 10 directories on the VDO mount point:

   ```bash theme={null}
   mkdir /mnt/myvdo/dir{1..10}
   ```

3. Copy the file into each directory using a loop:

   ```bash theme={null}
   for i in $(seq 1 10); do sudo cp /home/aaron/mydata.txt /mnt/myvdo/dir$i; done
   ```

4. Verify the mount point’s usage:

   ```bash theme={null}
   df -h /mnt/myvdo
   ```

   Expected result:

   ```text theme={null}
   Filesystem              Size  Used Avail Use% Mounted on
   /dev/mapper/vdo_storage  10G  581M  9.5G   6% /mnt/myvdo
   ```

5. Check the VDO statistics:

   ```bash theme={null}
   sudo vdostats --human-readable
   ```

   Expected output:

   ```text theme={null}
   Device                      Size  Used Available Use% Space saving%
   /dev/mapper/vdo_storage     5.0G  3.0G      2.0G 60%          94%
   ```

Next, copy another file with a different name into each directory:

```bash theme={null}
sudo cp /home/aaron/mydata.txt /home/aaron/moredata.txt
for i in $(seq 1 10); do sudo cp /home/aaron/moredata.txt /mnt/myvdo/dir$i; done
```

Then verify the filesystem usage and VDO statistics again:

```bash theme={null}
df -h /mnt/myvdo
sudo vdostats --human-readable
```

Expected output for filesystem usage:

```text theme={null}
Filesystem              Size  Used Avail Use% Mounted on
/dev/mapper/vdo_storage  10G  1.1G  9.0G 11% /mnt/myvdo
```

And VDO stats might show:

```text theme={null}
Device                      Size  Used Available Use% Space saving%
/dev/mapper/vdo_storage     5.0G  3.1G  1.9G   61% 95%
```

As you add more identical copies, you will notice an increase in the space-saving percentage, demonstrating VDO's effective deduplication—even when file names differ.

## VDO in RHEL 9 with LVM Integration

In RHEL 9, VDO is integrated with LVM, and the standalone Python-based VDO tools are no longer used. To create a new VDO volume using LVM, proceed with the following steps:

1. Create a physical volume on `/dev/vdb`:

   ```bash theme={null}
   sudo pvcreate /dev/vdb
   ```

2. Create a volume group named `vdo_volume`:

   ```bash theme={null}
   sudo vgcreate vdo_volume /dev/vdb
   ```

3. Create a logical volume with VDO options:

   ```bash theme={null}
   sudo lvcreate --type vdo -n vdo_storage -L 100%FREE -V 10G vdo_volume/vdo_pool1
   ```

4. Create an XFS filesystem on the new VDO volume:

   ```bash theme={null}
   sudo mkfs.xfs -K /dev/vdo_volume/vdo_storage
   ```

   Alternatively, to use an ext4 filesystem:

   ```bash theme={null}
   sudo mkfs.ext4 -E nodiscard /dev/vdo_volume/vdo_storage
   ```

One clear advantage of the LVM-integrated approach in RHEL 9 is that it simplifies mounting by eliminating the complex options required in previous versions.

## Mounting the LVM-Based VDO Device

First, create a mount point:

```bash theme={null}
sudo mkdir /mnt/myvdo
```

Edit the `/etc/fstab` file with your preferred text editor (e.g., vi) and add the following line:

```plaintext theme={null}
/dev/vdo_volume/vdo_storage /mnt/myvdo xfs defaults 0 0
```

Then, mount the filesystem and verify the mount:

```bash theme={null}
sudo mount -a
df -h /mnt/myvdo
```

Expected output:

```text theme={null}
Filesystem                  Size  Used Avail Use% Mounted on
/dev/vdo_volume/vdo_storage  10G  104M  9.9G  2% /mnt/myvdo
```

This confirms that the VDO volume has a logical size of 10 GB and is correctly mounted.

For more details on LVM-based VDO options, refer to the manual pages:

```bash theme={null}
man lvm vdo
```

This concludes our comprehensive guide on configuring disk compression with VDO. Enjoy the benefits of optimized storage and improved performance in your Linux environment!

- [Watch Video](https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/eb65d854-5137-4776-8ff8-73e274c43a0c/lesson/b456ae40-1ac9-40e2-83cd-1eeb52f36c0e)
