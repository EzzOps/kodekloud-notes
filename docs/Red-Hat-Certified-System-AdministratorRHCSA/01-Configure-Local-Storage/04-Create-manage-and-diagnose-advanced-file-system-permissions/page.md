# Create manage and diagnose advanced file system permissions

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Configure-Local-Storage/Create-manage-and-diagnose-advanced-file-system-permissions/page

This comprehensive guide covers creating, managing, and diagnosing advanced file system permissions in Linux using standard permissions, ACLs, and additional file attributes.

Welcome to this comprehensive guide on advanced file system permissions in Linux. In this tutorial, we cover how to create, manage, and diagnose file permissions using standard permissions as well as Access Control Lists (ACLs) and additional file attributes.

Imagine issuing the command:

```bash theme={null}
ls -l
```

This command lists files along with their permissions. In our example, files are owned by the user "adm" and belong to the "ftp" group. The permission sets are broken down as follows:

* The first three bits (`rw-`) indicate that the owner ("adm") can read and write.
* The next three bits (`rw-`) allow members of the "ftp" group to also read and write.
* The final three bits (`r--`) provide read-only access for other users.

Below is a sample output of the `ls -l` command:

```bash theme={null}
[aaron@LFCS-CentOS attributes]$ ls -l
total 0
-rw-rw-r--. 1 adm ftp 0 Mar 24 17:55 file1
-rw-rw-r--. 1 adm ftp 0 Mar 24 17:55 file2
-rw-rw-r--. 1 adm ftp 0 Mar 24 17:55 file3
[aaron@LFCS-CentOS attributes]$
```

> **lightbulb** Notice how the permissions allow the group and others different levels of access. For a user like Aaron Lockhart, who is not in the "ftp" group, only the read permission from the third set is applicable.

If we need to grant specific users additional access—such as providing Aaron Lockhart with write access to "file3" without altering his permissions for "file1" and "file2"—reassigning file ownership is not ideal, as it would remove write access from the regular owner ("adm"). Instead, Access Control Lists (ACLs) offer a more granular approach.

## Creating a File with Standard Permissions

Let's start by creating a new file called `examplefile` and setting its content to "This is the file content". We then change the file's ownership to user "adm" and group "ftp":

```bash theme={null}
echo "This is the file content" > examplefile
sudo chown adm:ftp examplefile
ls -l examplefile
```

Since the current user is neither "adm" nor a member of the "ftp" group, attempts to overwrite the file will result in a permission error. For example:

```bash theme={null}
echo "This is the NEW file content" > examplefile
```

This command will yield an error such as "Permission denied". However, reading the file with:

```bash theme={null}
cat examplefile
```

will correctly display its content:

```bash theme={null}
[aaron@LFCS-CentOS attributes]$ cat examplefile
This is the file content
[aaron@LFCS-CentOS attributes]$
```

Standard file permissions work well in most cases, but when finer control is necessary, ACLs can be used to grant specific permissions to additional users.

## Granting Specific Permissions Using ACLs

To allow Aaron Lockhart to both read and modify `examplefile`, apply the following ACL command. If the file is not owned by the user, prepend the command with `sudo`:

```bash theme={null}
sudo setfacl --modify user:aaron:rw examplefile
```

With this ACL in place, Aaron can now overwrite the file:

```bash theme={null}
echo "This is the NEW file content" > examplefile
cat examplefile
```

After modifying the file, the presence of ACLs is indicated by a plus sign (`+`) in the permission listing:

```bash theme={null}
[aaron@LFCS-CentOS attributes]$ ls -l
total 4
-rw-rw-r--+ 1 adm ftp 29 Mar 24 18:04 examplefile
...
```

To inspect detailed ACL settings, use the `getfacl` command:

```bash theme={null}
getfacl examplefile
```

Example output:

```bash theme={null}
[aaron@LFCS-CentOS attributes]$ getfacl examplefile
