# Create Manage and Diagnose Advanced Filesystem Permissions

Source: https://notes.kodekloud.com/docs/Prep-Course-Linux-Foundation-Certified-System-Administrator-LFCS-Certification/Storage/Create-Manage-and-Diagnose-Advanced-Filesystem-Permissions/page

This article explores advanced filesystem permissions using Access Control Lists and file attributes for granular control beyond standard file permissions.

In this article, we explore how standard file permissions are represented, their limitations, and how to use Access Control Lists (ACLs) along with file attributes for more granular control. These advanced techniques allow system administrators and users to tailor permissions without disrupting existing ownership structures.

***

## Understanding Standard File Permissions

When you list files with the command `ls -l`, the output might look like this:

```bash theme={null}
jeremy@kodekloud:~$ ls -l
total 0
-rw-rw-r-- 1 alex  staff  0 May 23 05:56 file1
-rw-rw-r-- 1 alex  staff  0 May 23 05:56 file2
-rw-rw-r-- 1 alex  staff  0 May 23 05:56 file3
jeremy@kodekloud:~$
```

In the above output, each file is owned by the user `alex` and the group `staff`. The permission string is divided into three distinct parts:

1. The first three characters (`rw-`) indicate that the owner (Alex) can read and write the file.
2. The next three characters (`rw-`) show that users in the `staff` group can also read and write.
3. The final three characters (`r--`) mean that all other users have read-only access.

> **lightbulb** If you log in as another user (e.g., Jeremy Morgan) who is neither `alex` nor part of the `staff` group, only the last set of permissions (`r--`) applies.

Imagine Jeremy needs to edit only `file3` without being granted full access to all files owned by the group or changing file ownership. This is where ACLs become useful.

***

## Using ACLs for Granular Permission Control

Access Control Lists (ACLs) enable the definition of permissions for multiple users and groups beyond the standard owner-group-others model.

### Adding Content with Elevated Privileges

Suppose we want to add content to `file3` as the root user (since Jeremy is not the file owner):

```bash theme={null}
jeremy@kodekloud:~$ sudo sh -c 'echo "This is the file content" > file3'
[sudo] password for jeremy:
jeremy@kodekloud:~$ ls -l file3
-rw-rw-r-- 1 alex staff 25 May 23 06:18 file3
```

Even though you can view the content using `cat file3`, Jeremy is unable to overwrite it due to insufficient write permissions:

```bash theme={null}
jeremy@kodekloud:~$ echo "This is the NEW file content" > file3
-bash: file3: Permission denied
```

### Granting Specific Permissions via ACL

To grant Jeremy Morgan read and write access specifically on `file3`, set an ACL entry by running:

```bash theme={null}
sudo setfacl --modify user:jeremy:rw file3
```

After executing the above command, the permissions are adjusted. A plus sign (`+`) in the file listing indicates that additional ACL information is present:

```bash theme={null}
jeremy@kodekloud:~$ ls -l file3
-rw-rw-r--+ 1 alex staff 25 May 23 06:18 file3
```

To inspect the ACL entries on the file, use the `getfacl` command:

```bash theme={null}
getfacl file3
