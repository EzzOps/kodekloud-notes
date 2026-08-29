# List set and change standard ugorwx permissions

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Understand-and-Use-Essential-Tools/List-set-and-change-standard-ugorwx-permissions/page

Learn to list, set, and change standard file permissions in Linux for effective access management.

In this article, you will learn how to list, set, and change standard file permissions in Linux. Mastering file and directory ownership along with permission settings is essential for effective access management on any Linux system.

## Viewing File Ownership and Permissions

Every file and directory has an associated owner. To view detailed information—including owner details and permission settings—use the following command:

```bash theme={null}
$ ls -l
-rw-r-----  aaron family 49 Oct 27 14:41 family_dog.jpg
```

In the example above, the file "family\_dog.jpg" is owned by the user "aaron". Only the owner (or a root user) can modify the file’s permissions.

The second field in the output indicates the file’s group; here, it is the "family" group.

## Changing File Group

To change the group of a file or directory, use the `chgrp` command. The syntax is:

```bash theme={null}
