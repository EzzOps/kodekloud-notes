# Create a symbolic link to /home/aaron/Pictures/family_dog.jpg
$ ln -s /home/aaron/Pictures/family_dog.jpg family_dog_shortcut.jpg
```

After creating the link, you can verify its creation using the ls -l command. The output will display an "l" at the beginning of the permissions string, indicating that it is a soft link, along with the reference to the target path:

```bash theme={null}
$ ls -l
lrwxrwxrwx. 1 aaron aaron family_dog_shortcut.jpg -> /home/aaron/Pictures/family_dog.jpg
```

## Viewing the Complete Target Path

If the target path is too long, ls -l might truncate it. In such cases, the readlink command can be used to display the full target path:

```bash theme={null}
$ readlink family_dog_shortcut.jpg
/home/aaron/Pictures/family_dog.jpg
```

<Callout icon="lightbulb">
  The permission bits shown for soft links are generally set to read, write, and execute (RWX) for everyone. However, these permissions do not affect the target file. Writing to the link will adhere to the permissions of the actual destination file.
</Callout>

## Absolute vs. Relative Paths

Using an absolute path (as in /home/aaron/Pictures/family\_dog.jpg) ensures clarity but may lead to issues if the directory structure changes (for example, if the "aaron" directory is renamed). In such cases, the soft link will become broken and typically appear in red when using ls -l.

To mitigate this risk, you can create soft links using relative paths. This approach allows the system to interpret the path relative to the location of the soft link, preserving its functionality even if the absolute directory structure shifts. Consider the following examples:

```bash theme={null}
# Create a symbolic link using an absolute path
$ ln -s /home/aaron/Pictures/family_dog.jpg family_dog_shortcut.jpg
$ ls -l
lrwxrwxrwx. 1 aaron aaron family_dog_shortcut.jpg -> /home/aaron/Pictures/family_dog.jpg
$ readlink family_dog_shortcut.jpg
/home/aaron/Pictures/family_dog.jpg

# Attempt to write to a file via a soft link (will fail due to target file permissions)
$ echo "Test" >> fstab_shortcut
bash: fstab_shortcut: Permission denied

# Create a symbolic link using a relative path
$ ln -s Pictures/family_dog.jpg relative_picture_shortcut
```

<Callout icon="triangle-alert">
  When creating soft links with absolute paths, be aware that any changes in the directory structure can lead to broken links. Using relative paths can provide better resilience against such changes.
</Callout>

## Additional Considerations

Soft links are versatile. They can be used not only to reference files but also directories. Furthermore, unlike hard links, soft links can span across different file systems, making them particularly useful for various system management tasks.

<Frame>
  ![The image illustrates the concept of soft links, showing how they can link to files and folders, including across different filesystems.](https://kodekloud.com/kk-media/image/upload/v1752883618/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-Create-and-manage-soft-links/soft-links-files-folders-illustration.jpg)
</Frame>

That concludes our discussion on creating and managing soft links in Linux.

Let's move on to some hands-on labs.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/c3d8eded-b1dc-479c-a51a-c4f468ba6da3/lesson/74885f57-b142-430f-aa9f-1278868442e8" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/c3d8eded-b1dc-479c-a51a-c4f468ba6da3/lesson/7f9f8e43-8482-49be-955e-e34451ca7f38" />
</CardGroup>


# Create delete copy and move files and directories

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Understand-and-Use-Essential-Tools/Create-delete-copy-and-move-files-and-directories/page

This article covers essential Linux commands for creating, deleting, copying, and moving files and directories for effective file management.

In this lesson, we explore essential Linux commands to create, delete, copy, and move files and directories. Understanding these commands is crucial for effective file management in Linux. Before using these commands, ensure you are familiar with these fundamental concepts:

* What is a file system tree?
* What is an absolute path?
* What is a relative path?

## Listing Files and Directories

The `ls` command lists the files and directories in your current (or working) directory. The term `ls` is short for "list." Here are several common usages:

### Basic Listing

Running the simple `ls` command in a typical home directory might display:

```bash theme={null}
$ ls
Pictures    Desktop
Documents   Videos
Downloads   Music
```

Files and directories starting with a dot (such as `.ssh`) are hidden by default. To view hidden files, include the `-a` option:

```bash theme={null}
$ ls -a
.              ..
.ssh           .bash_logout   .bash_profile  .bashrc
Pictures       Desktop        Downloads       Documents   Music
```

### Listing Files in a Specific Location

To list files from another directory, provide the path to the `ls` command:

```bash theme={null}
$ ls /log
```

### Long Listing Format

For extended details like permissions, ownership, and modification times, use the `-l` option:

```bash theme={null}
$ ls -l /var/log/
total 4064
drwxr-xr-x. 2 root  root       4096 Oct 18 22:52 anaconda
drwx------. 2 root  root          23 Oct 18 22:53 audit
-rw-------. 1 root  root      19524 Nov  1 17:56 boot.log
-rw-rw----. 1 root  utmp          0 Nov  1 14:08 btmp
-rw-------. 1 root  utmp          0 Oct 18 22:38 btmp-20211101
drwxr-x---. 2 chrony chrony   6 Jun 24 09:21 chrony
...
```

### Combining Options for Detailed and Inclusive Listings

The `-a` and `-l` options can be combined, and their order is not important:

```bash theme={null}
$ ls -a -l
total 76
drwx------ 16 aaron aaron 4096 Nov  1 17:57 .
drwxr-xr-x  7 root  root    70 Oct 26 16:54 ..
-rw-------  1 aaron aaron 5085 Nov  1 17:56 .bash_history
-rw-r--r--  1 aaron aaron  141 Jul 27 09:21 .bash_logout
-rw-r--r--  1 aaron aaron  376 Jul 27 09:21 .bash_profile
-rw-r--r--  1 aaron aaron  141 Jul 27 09:21 .bashrc
drwxr-xr-x  2 aaron aaron    6 Oct 19 00:11 Desktop
drwxr-xr-x  3 aaron aaron   25 Oct 23 18:15 Documents
drwxr-xr-x  2 aaron aaron    6 Oct 19 00:11 Downloads
drwxr-xr-x  2 aaron aaron    6 Oct 19 00:11 Music
drwxr-xr-x  2 aaron aaron    2 Oct  6 19:37 Pictures
-rw-rw-r--  1 aaron aaron   36 Oct 28 20:06 testfile
```

To display file sizes in a human-friendly format (bytes, kilobytes, megabytes, etc.), combine the `-h` option:

```bash theme={null}
$ ls -ahl
total 76K
drwx------   16 aaron  aaron  4.0K Nov  1 17:57 .
drwxr-xr-x    7 root   root    70 Oct 26 16:54 ..
-rw-------    1 aaron  aaron  5.0K Nov  1 17:56 .bash_history
-rw-r--r--    1 aaron  aaron    18 Jul 27 09:21 .bash_logout
-rw-r--r--    1 aaron  aaron   141 Jul 27 09:21 .bash_profile
-rw-r--r--    1 aaron  aaron   376 Jul 27 09:21 .bashrc
drwxr-xr-x    2 aaron  aaron     6 Oct 19 00:11 Desktop
drwxr-xr-x    3 aaron  aaron    25 Oct 23 18:15 Documents
drwxr-xr-x    2 aaron  aaron     6 Oct 19 00:11 Downloads
drwxr-xr-x    2 aaron  aaron     6 Oct 19 00:11 Music
drwxr-xr-x    2 aaron  aaron     6 Oct 19 00:11 Pictures
-rw-rw-r--    1 aaron  aaron    36 Oct 28 20:06 testfile
```

## Understanding the File System Tree

Linux organizes all files and directories into a hierarchical structure known as the file system tree. Think of it like an inverted tree, where the root directory (`/`) sits at the top, and all subdirectories branch out from there.

### Paths Explained

#### Absolute Path

An absolute path starts from the root directory. For example:

```bash theme={null}
/home/aaron/Documents/Invoice.pdf
```

This path begins at the root (`/`), moves through the `home` directory, then `aaron`, followed by `Documents`, and finally accesses the file `Invoice.pdf`.

#### Relative Path

A relative path describes a location relative to the current working directory. To see your current working directory, use the `pwd` command:

```bash theme={null}
$ pwd
/root
```

If you're logged in as user Aaron with the starting directory `/home/aaron`, the path `Documents/Invoice.pdf` would reference `/home/aaron/Documents/Invoice.pdf`. Likewise, `Invoice.pdf` without any directory designation refers to a file in the current directory, while `../Invoice.pdf` navigates one level up.

Consider this structure: the root directory (/) branches into several subdirectories and further levels until it eventually leads to files like "Invoice.pdf".

<Frame>
  ![The image shows a filesystem tree diagram with directories and a file path, illustrating the hierarchy from the root directory to a specific file named "Invoice.pdf".](https://kodekloud.com/kk-media/image/upload/v1752883619/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-Create-delete-copy-and-move-files-and-directories/filesystem-tree-diagram-invoice-pdf.jpg)
</Frame>

<Callout icon="lightbulb">
  * Use `cd /var/log` to change to the `/var/log` directory using an absolute path.
  * Enter `cd ..` to move up one directory level (to the parent directory).
  * Simply type `cd` without arguments to return to your home directory.
  * Use `cd -` (or `cd --` in some shells) to switch back to your previous directory.
</Callout>

## Creating Files and Directories

Creating files and directories in Linux is simple with the following commands:

### Creating Files

The `touch` command creates a new, empty file. For example, to create a file named `Receipt.pdf` in the current directory:

```bash theme={null}
$ touch Receipt.pdf
```

To create a file in another location, specify the file path. Both absolute and relative paths work:

```bash theme={null}
$ touch /home/jane/Receipt.pdf
$ touch ../jane/Receipt.pdf
```

### Creating Directories

Use the `mkdir` command (short for "make directory") to create new directories. For instance:

```bash theme={null}
$ mkdir receipts
```

## Copying Files and Directories

The `cp` command copies files and directories with ease.

### Copy a File

To copy a file, provide its source path and destination path:

```bash theme={null}
$ cp Receipt.pdf receipts/
```

It is advisable to end directory paths with a slash (`/`) to indicate that the destination is a directory. You can also copy a file and rename it simultaneously:

```bash theme={null}
$ cp Receipt.pdf receipts/Receipt_copy.pdf
```

### Copy a Directory Recursively

To duplicate an entire directory and its contents, use the `-r` (recursive) flag:

```bash theme={null}
$ cp -r Receipts/ BackupOfReceipts/
```

<Callout icon="triangle-alert">
  Ensure the destination directory (e.g., `BackupOfReceipts/`) does not exist if you intend to create a new copy of the source directory.
</Callout>

## Moving and Renaming Files and Directories

The `mv` command is versatile—it moves files or folders and also renames them.

### Moving a File

To move a file to a different location:

```bash theme={null}
$ mv Receipt.pdf receipts/
```

### Renaming a File or Directory

To rename `Receipt.pdf` to `old_receipt.pdf`:

```bash theme={null}
$ mv Receipt.pdf old_receipt.pdf
```

When moving directories, `mv` automatically processes all contained files and subdirectories without needing a recursive flag.

## Deleting Files and Directories

Deleting files and directories is straightforward with the `rm` command.

### Deleting Files

To remove a file:

```bash theme={null}
$ rm Invoice.pdf
```

### Deleting Directories Recursively

To delete a directory and all its contents, use the `-r` option:

```bash theme={null}
$ rm -r Invoices/
```

<Callout icon="triangle-alert">
  Be cautious when using the `rm -r` command. Once executed, recovering a deleted directory and its contents can be difficult.
</Callout>

Visual aids, like command-line interfaces and directory structure diagrams, can help illustrate how paths reference files such as "Invoice.pdf". However, the commands function independently of any visual representations.

<Frame>
  ![The image shows a command-line interface on the left and a directory structure on the right, illustrating the path to a file named "Invoice.pdf" under the directories "/", "home", "aaron", and "Invoices".](https://kodekloud.com/kk-media/image/upload/v1752883620/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-Create-delete-copy-and-move-files-and-directories/command-line-directory-structure-invoice.jpg)
</Frame>

## Summary

In this lesson, you learned how to:

* List files and directories utilizing `ls` and its various options (`-a`, `-l`, `-h`).
* Understand the differences between absolute and relative paths.
* Create files with `touch` and directories with `mkdir`.
* Copy files and directories using `cp`, including the recursive copy option for entire directories.
* Move and rename files or directories with `mv`.
* Delete files using `rm` and remove directories recursively with `rm -r`.

Happy learning and efficient file management in Linux!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/c3d8eded-b1dc-479c-a51a-c4f468ba6da3/lesson/bd3e8383-e6e9-4548-adf3-4ffa6393808b" />
</CardGroup>
