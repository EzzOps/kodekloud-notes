# From /home/aaron, this goes to invoice.pdf inside Documents
$ cd Documents
$ ls invoice.pdf
```

To move up one level:

```bash theme={null}
$ cd ..
```

Jump to your home directory:

```bash theme={null}
$ cd
$ pwd
/home/aaron
```

![The image shows a directory structure with a command line interface on the left. The directory tree includes folders like "home," "var," and "root," with a file named "Invoice.pdf" under "aaron/Documents."](https://kodekloud.com/kk-media/image/upload/v1752881468/notes-assets/images/Linux-System-Administration-for-Beginners-Create-Delete-Copy-and-Move-Files-and-Directories/directory-structure-command-line-invoice.jpg)

## Creating Files and Directories

* Create an empty file:
  ```bash theme={null}
  $ touch receipt.pdf
  ```
* Create a directory:
  ```bash theme={null}
  $ mkdir receipts
  ```

Both commands accept absolute or relative paths:

```bash theme={null}
$ mkdir /home/aaron/new_folder
```

## Copying Files and Directories with `cp`

Use `cp` to duplicate files and directories.

### Copying a Single File

```bash theme={null}
$ cp receipt.pdf receipts/
```

To copy and rename at the same time:

```bash theme={null}
$ cp receipt.pdf receipts/receipt_backup.pdf
```

![The image shows a file directory structure with a command line interface on the left. The directory path includes folders named "home," "aaron," and "Receipts," leading to a file named "Receipt.pdf."](https://kodekloud.com/kk-media/image/upload/v1752881469/notes-assets/images/Linux-System-Administration-for-Beginners-Create-Delete-Copy-and-Move-Files-and-Directories/file-directory-structure-command-line.jpg)

### Copying Directories Recursively

```bash theme={null}
$ cp -r Receipts/ BackupOfReceipts/
```

This duplicates the entire `Receipts` folder and its contents into `BackupOfReceipts`. Ensure the destination name does not already exist to avoid nesting.

## Moving and Renaming with `mv`

The `mv` command handles both moving and renaming:

* Move a file:
  ```bash theme={null}
  $ mv receipt.pdf receipts/
  ```
* Rename a file:
  ```bash theme={null}
  $ mv receipt.pdf old_receipt.pdf
  ```
* Rename or move a directory:
  ```bash theme={null}
  $ mv receipts/ old_receipts/
  ```

No recursive flag is needed for directories; `mv` automatically moves contents.

## Deleting Files and Directories with `rm`

Use caution when removing files and directories:

* Remove a file:
  ```bash theme={null}
  $ rm invoice.pdf
  ```
* Remove a non-empty directory:
  ```bash theme={null}
  $ rm -r invoices/
  ```

> **triangle-alert** The `rm -r` command permanently deletes directories and their contents. Always double-check the path before pressing Enter!

***

## References

* [Linux Man Pages](https://www.kernel.org/doc/man-pages/)
* [GNU coreutils Documentation](https://www.gnu.org/software/coreutils/)
* [Introduction to Linux File System](https://en.wikipedia.org/wiki/File_system#Unix_and_Unix-like_systems)

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/cc1949d1-8171-4c8c-b69f-86f96cad0bbe/lesson/8ab7329a-f096-4f27-99a5-e7d94c813bce)


# Create and manage hard links

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/Essential-Commands/Create-and-manage-hard-links/page

This article explains how to create, manage, and understand hard links in Linux file systems.

Learn how Linux file systems use hard links to let multiple directory entries point to the same underlying data. You’ll see how to create, inspect, and remove hard links without wasting disk space.

## Files, Inodes, and Link Counts

Every file on a Linux filesystem (ext4, XFS, etc.) is represented by an inode. The inode stores metadata—permissions, timestamps, and pointers to data blocks on disk. The “Links” count in the `stat` output shows how many directory entries (hard links) reference that inode.

Let’s simulate Aaron saving a photo of his dog:

```bash theme={null}
mkdir -p /home/aaron/Pictures
echo "Picture of Milo the dog" > /home/aaron/Pictures/family_dog.jpg
stat /home/aaron/Pictures/family_dog.jpg
```

Example output:

```text theme={null}
File: /home/aaron/Pictures/family_dog.jpg
Size: 24         Blocks: 8          IO Block: 4096   regular file
Device: fd00h/64768d Inode: 52946177    Links: 1
Access: (0640/-rw-r-----)  Uid: (1000/aaron)   Gid: (1005/family)
...
```

Each new file has one link by default.

## Why Use Hard Links?

Copying files duplicates data and consumes extra space:

```bash theme={null}
cp /home/aaron/Pictures/family_dog.jpg /home/jane/Pictures/
```

Hard links solve this by pointing two filenames to the same inode:

```bash theme={null}
ln /home/aaron/Pictures/family_dog.jpg /home/jane/Pictures/family_dog.jpg
```

Now both entries share one set of data blocks.

| Comparison        | Copy (`cp`)         | Hard Link (`ln`)                   |
| ----------------- | ------------------- | ---------------------------------- |
| Disk Usage        | Duplicated per copy | Single copy on disk                |
| Data Consistency  | Separate files      | Always the same content            |
| Link Count Effect | Independent inodes  | Inode “Links” count increases by 1 |

> **lightbulb** Hard links only work on regular files within the same filesystem. See limitations below.

## Inspecting Link Counts

After creating the hard link, check the link count again:

```bash theme={null}
stat /home/jane/Pictures/family_dog.jpg
```

```text theme={null}
File: /home/jane/Pictures/family_dog.jpg
...
Inode: 52946177    Links: 2
...
```

Now `Links: 2` confirms two directory entries point to the same inode.

## Removing Hard Links

* If Aaron removes his entry:

  ```bash theme={null}
  rm /home/aaron/Pictures/family_dog.jpg
  stat /home/jane/Pictures/family_dog.jpg
  # Links: 1
  ```

* Only when *all* links are removed does the filesystem reclaim the inode and free the data blocks:

  ```bash theme={null}
  rm /home/jane/Pictures/family_dog.jpg
  ```

## Limitations of Hard Links

You **cannot**:

* Link directories (to prevent cycles in the filesystem tree).
* Cross filesystem boundaries (e.g., SSD → external drive).

![The image illustrates limitations and considerations of hardlinking, showing that hardlinks can only be created for files, not folders, and must be on the same filesystem.](https://kodekloud.com/kk-media/image/upload/v1752881470/notes-assets/images/Linux-System-Administration-for-Beginners-Create-and-manage-hard-links/hardlinking-limitations-filesystem-considerations.jpg)

> **triangle-alert** Attempting to `ln` a file across different mounts will fail silently or return an error:

  ```bash theme={null}
  ln: failed to create hard link ... Invalid cross-device link
  ```

## Permissions and Hard Links

Permissions and ownership are stored in the inode itself. Changing them via any hard link affects all links:

```bash theme={null}
chmod g+rw /home/aaron/Pictures/family_dog.jpg
