# Manage File Permissions and Ownership

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/Devices-Linux-Filesystems-Filesystem-Hierarchy-Standard/Manage-File-Permissions-and-Ownership/page

This article explains how to view and modify file permissions and ownership on a Linux system.

In this lesson, we’ll explore how to view and modify file permissions and ownership on a Linux system. You’ll learn to inspect permission bits, change owners and groups, and apply both symbolic and numeric modes with `chmod`, `chown`, and `chgrp`.

## Inspect Current Ownership and Permissions

Run `ls -l` to display the owner, group, and permission bits for files and directories:

```bash theme={null}
$ ls -l
-rw-r----- 1 aaron family 49 Oct 27 14:41 family_dog.jpg
```

* **Owner**: `aaron`
* **Group**: `family`
* **Permissions**: `-rw-r-----`

Only the file owner or the superuser (`root`) can change these settings.

## Viewing and Changing Group Ownership

Use `chgrp` to assign a file or directory to a different group you belong to:

```bash theme={null}
