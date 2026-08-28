# Create the test file
touch suidfile

# Check default permissions
ls -l suidfile
# Output: -rw-rw-r--  1 jeremy jeremy 0 May 8 01:22 suidfile
```

To set the SUID bit, which is represented by a leading digit of 4 in the permission mode, execute:

```bash theme={null}
chmod 4664 suidfile
ls -l suidfile
```

Notice that the execute bit for the owner may be displayed as a capital "S" when it is not enabled. Including the execute permission (for example, using `4764`) will show a lowercase "s" instead.

## SGID (Set Group ID)

SGID works similarly to SUID but applies to the group ownership of an executable or directory. For executables, SGID allows any user running the file to do so with the file's group privileges. When applied to a directory, any new file or directory created inherits the group's ownership, which is invaluable for collaborative work environments.

For instance, if a reports application is associated with the reports group, both Emily and John can access executable files, and newly created files inside the directory will automatically inherit the reports group.

<Frame>
  ![The image illustrates the concept of SGID (Set Group ID) permissions, showing how it applies to both executables and directories, with two users accessing a file within a directory.](https://kodekloud.com/kk-media/image/upload/v1752881269/notes-assets/images/Linux-Foundation-Certified-System-Administrator-LFCS-SUID-SGID-and-Sticky-Bit/sgid-permissions-executables-directories.jpg)
</Frame>

### Demonstration of SGID

Follow these simple steps to set the SGID bit on a file:

```bash theme={null}
# Create the file
touch sgidfile

# Check the default file permissions
ls -l sgidfile
# Expected output: -rw-rw-r-- 1 jeremy jeremy 0 May 8 01:25 sgidfile
```

To set SGID without granting execute permissions for the group:

```bash theme={null}
chmod 2664 sgidfile
ls -l sgidfile
```

If the execute permission is also required (thus displaying a lowercase "s"), use:

```bash theme={null}
chmod 2674 sgidfile
ls -l sgidfile
```

## Combining SUID and SGID

Combining SUID and SGID on a single file is straightforward. Since SUID is represented by 4 and SGID by 2, the combined digit is 6. For example, to apply both on a file called `both`:

```bash theme={null}
touch both
chmod 6664 both
ls -l both
```

To efficiently locate files using these special permissions, use the `find` command:

```bash theme={null}
# Find files with the SUID bit set
find . -perm /4000

# Find files with the SGID bit set
find . -perm /2000

# Find files with either SUID or SGID (or both) set
find . -perm /6000
```

## Sticky Bit

The Sticky Bit is a special permission applied primarily to directories to control file deletion. When set, it restricts file deletion within the directory so that only the file owner, the directory owner, or the superuser can delete or rename files. This is especially beneficial for shared directories where multiple users have write access but should not be able to remove files created by others.

### Demonstration of the Sticky Bit

Creating a directory with a Sticky Bit is illustrated below:

```bash theme={null}
# Set the Sticky Bit using a shorthand command
chmod 1777 stickydir/
ls -ld stickydir/
# Expected output: drwxrwxrwt 2 jeremy jeremy 4096 May 8 01:29 stickydir/
```

In the permission output, a lowercase "t" signifies that the Sticky Bit is active along with the execute permission. If the execute permission is revoked (for example, by setting mode `1666`), the indicator changes to an uppercase "T":

```bash theme={null}
chmod 1666 stickydir/
ls -ld stickydir/
```

<Callout icon="lightbulb">
  A lowercase "t" denotes that the Sticky Bit is set and execute permission is enabled, while an uppercase "T" indicates that only the Sticky Bit is set.
</Callout>

## Conclusion

Understanding and properly configuring SUID, SGID, and the Sticky Bit is crucial for managing permissions in Unix/Linux environments. With SUID, programs can execute with the file owner's privileges; SGID facilitates group-controlled execution and inheritance; and the Sticky Bit secures shared directories against unauthorized file deletions.

By leveraging these permissions, system administrators can implement controlled privilege escalations while ensuring robust security. For further reading, check out the [Kubernetes Documentation](https://kubernetes.io/docs/) and explore how secure permissions integrate within broader system management practices.

Happy experimenting, and enjoy the power of controlled permission management!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-foundation-certified-system-administrator-lfcs/module/115b1db7-7970-4cc8-91d4-0ac4892fed9f/lesson/372c66a1-2a08-464f-b936-d3c0a13c3755" />
</CardGroup>


# Search File Using Grep

Source: https://notes.kodekloud.com/docs/Prep-Course-Linux-Foundation-Certified-System-Administrator-LFCS-Certification/Essential-Commands/Search-File-Using-Grep/page

Learn to use the grep utility for searching specific text within files, especially useful for large files.

In this lesson, you'll learn how to use the grep utility to search for specific text within files. Grep is particularly useful when working with large files containing thousands of lines, as it helps you quickly filter and locate the information you need.

## Basic grep Usage

The general syntax for the grep command is:

grep \[options] \[search pattern] \[file]

For example, to search for the term "password" inside the SSH daemon configuration file, run:

```bash theme={null}
$ grep 'password' /etc/ssh/sshd_config
#PermitRootLogin prohibit-password
