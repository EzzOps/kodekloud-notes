# Mount definitions for /shares
mynetworkshare -fstype=auto    127.0.0.1:/etc
mynetworkshare -fstype=nfs4    127.0.0.1:/etc
mynetworkshare -fstype=auto,ro 127.0.0.1:/etc
myext4files    -fstype=auto    :/dev/vdb2
```

| Mount Name     | fstype Options | Source         | Description            |
| -------------- | -------------- | -------------- | ---------------------- |
| mynetworkshare | auto           | 127.0.0.1:/etc | Auto-detect filesystem |
| mynetworkshare | nfs4           | 127.0.0.1:/etc | Force NFSv4            |
| mynetworkshare | auto,ro        | 127.0.0.1:/etc | Read-only mount        |
| myext4files    | auto           | :/dev/vdb2     | Local ext4 partition   |

Reload AutoFS:

```bash theme={null}
sudo systemctl reload autofs.service
```

***

## 4. Test the On-Demand Mount

1. Verify that `/shares` is empty:
   ```bash theme={null}
   ls /shares
   # (no output; nothing is mounted yet)
   ```
2. Access the share to trigger the mount:
   ```bash theme={null}
   ls /shares/mynetworkshare/
   # mysharedfile1  mysharedfile2
   ```
3. After 5 minutes of inactivity, AutoFS will unmount the share automatically.

***

## 5. Direct Mount Points (No Common Parent)

If you prefer absolute mount paths instead of a shared parent:

1. Update **/etc/auto.master**:

   ```bash theme={null}
   sudo vim /etc/auto.master
   ```

   Replace the `/shares` entry with:

   ```text theme={null}
   /-  /etc/auto.shares  --timeout=400
   ```

2. Modify **/etc/auto.shares**:

   ```bash theme={null}
   sudo vim /etc/auto.shares
   ```

   ```text theme={null}
   /mynetworkshare         -fstype=auto    127.0.0.1:/etc
   /localfiles/myext4files -fstype=auto    :/dev/vdb2
   ```

3. Reload AutoFS:

   ```bash theme={null}
   sudo systemctl reload autofs.service
   ```

Now you can access directly:

```bash theme={null}
ls /mynetworkshare/
ls /localfiles/myext4files/
# mysharedfile3  mysharedfile4
```

***

## Next Steps

You’ve successfully configured on-demand mounting with AutoFS and NFS. In the next lesson, we’ll explore advanced unmounting controls and troubleshooting techniques.

***

## Links and References

* [AutoFS Manual Page](https://linux.die.net/man/5/auto.master)
* [NFS Documentation](https://nfs.sourceforge.io/)
* [Red Hat AutoFS Guide](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/managing_file_systems/assembly_managing-network-file-systems_managing-file-systems)

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/de71b96a-9dc0-4e92-987a-6c7055c44e8b/lesson/cb0c1447-f6ae-4243-90df-f44c5d9c1adf)


# Control Mounting and Unmounting of Filesystems Part 2

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/Devices-Linux-Filesystems-Filesystem-Hierarchy-Standard/Control-Mounting-and-Unmounting-of-Filesystems-Part-2/page

This guide explains how to allow non-root users to mount and unmount filesystems in Linux.

In this guide, you’ll learn how to grant non-root users the ability to mount and unmount filesystems on Linux. While root or sudo privileges have traditionally been required, desktop environments and modern distributions often auto-mount removable media such as CD-ROMs, USB flash drives, and external disks under a user’s home directory:

```bash theme={null}
/media/USER/LABEL
```

For example, if `john` plugs in a USB drive labeled `FlashDrive`, it appears at:

```bash theme={null}
/media/john/FlashDrive
```

## Allowing Non-Root Mounts via /etc/fstab

You can configure `/etc/fstab` to let normal users mount and unmount specific devices without sudo. Modify the mount options field to include one of the following:

| Option | Description                               | Default |
| ------ | ----------------------------------------- | ------- |
| user   | Allow any user to mount and unmount       | (no)    |
| nouser | Disallow non-root mounts                  | yes     |
| group  | Allow users belonging to the owning group | (no)    |
| owner  | Allow the device’s owning user            | (no)    |

Example: permitting all users to mount `/dev/sdb1` on `/mnt/userdrive`:

```fstab theme={null}
/dev/sdb1  /mnt/userdrive  ext4  defaults,user  0 0
```

> **lightbulb** After editing `/etc/fstab`, you can test the entry without rebooting:

  ```bash theme={null}
  mount /mnt/userdrive
  umount /mnt/userdrive
  ```

## Managing Mounts with systemd

systemd can manage both static mounts and on-demand automounts via unit files in `/etc/systemd/system/`. Units must be named after the mount point by replacing slashes with hyphens and appending `.mount` or `.automount`.

### Creating a Mount Unit

1. Create the file `/etc/systemd/system/mnt-external.mount`:

   ```bash theme={null}
   sudo vi /etc/systemd/system/mnt-external.mount
   ```

2. Populate it:

   ```ini theme={null}
   [Unit]
   Description=External data disk

   [Mount]
   What=/dev/disk/by-uuid/56C11DCC5D2E1334
   Where=/mnt/external
   Type=ntfs
   Options=defaults

   [Install]
   WantedBy=multi-user.target
   ```

| Field       | Purpose                                               |
| ----------- | ----------------------------------------------------- |
| Description | Brief description of the mount                        |
| What        | Device path or UUID (`/dev/disk/by-uuid/...`)         |
| Where       | Mount point directory (`/mnt/external`)               |
| Type        | Filesystem type (`ntfs`, `ext4`, etc.)                |
| Options     | Mount options (same as in `/etc/fstab`)               |
| WantedBy    | Target to activate the mount on (`multi-user.target`) |

> **triangle-alert** The filename `mnt-external.mount` **must** exactly match the `Where` path `/mnt/external` (slashes → hyphens).

3. Reload systemd and start the mount:

   ```bash theme={null}
   sudo systemctl daemon-reload
   sudo systemctl start mnt-external.mount
   ```

4. Check status:

   ```bash theme={null}
   sudo systemctl status mnt-external.mount
   ```

   Sample output:

   ```plain theme={null}
   ● mnt-external.mount — External data disk
        Loaded: loaded (/etc/systemd/system/mnt-external.mount; disabled; preset: enabled)
        Active: active (mounted) since Mon 2019-08-19 22:27:02 -03; 14s ago
         What: /dev/sdb1
         Where: /mnt/external
   ```

5. To auto-mount at boot:

   ```bash theme={null}
   sudo systemctl enable mnt-external.mount
   ```

### Creating an Automount Unit

An automount unit triggers the mount only when the directory is accessed. You’ll need both the `.mount` and a corresponding `.automount` file.

1. Create `/etc/systemd/system/mnt-external.automount`:

   ```bash theme={null}
   sudo vi /etc/systemd/system/mnt-external.automount
   ```

2. Add:

   ```ini theme={null}
   [Unit]
   Description=Automount External Data Disk

   [Automount]
   Where=/mnt/external

   [Install]
   WantedBy=multi-user.target
   ```

3. Reload, start, and enable:

   ```bash theme={null}
   sudo systemctl daemon-reload
   sudo systemctl start mnt-external.automount
   sudo systemctl enable mnt-external.automount
   ```

Now, whenever you `ls /mnt/external`, systemd will mount the disk automatically.

***

## Links and References

* [fstab(5) Manual](https://man7.org/linux/man-pages/man5/fstab.5.html)
* [systemd.mount Documentation](https://www.freedesktop.org/software/systemd/man/systemd.mount.html)
* [systemd.automount Documentation](https://www.freedesktop.org/software/systemd/man/systemd.automount.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/de71b96a-9dc0-4e92-987a-6c7055c44e8b/lesson/fc36f121-9775-4674-8a4a-ef92971fadb6)
