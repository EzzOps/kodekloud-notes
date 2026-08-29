# Create the file
echo "Picture of Milo the dog" > ~/Pictures/family_dog.jpg

# Show metadata, including inode and link count
stat ~/Pictures/family_dog.jpg
```

Example output:

```text theme={null}
File: /home/aaron/Pictures/family_dog.jpg
Size: 24           Blocks: 8    IO Block: 4096   regular file
Device: fd00h/64768  Inode: 52946177    Links: 1
Access: (0640/-rw-r-----)  Uid: (1000/aaron)  Gid: (1005/family)
...
```

| Term  | Description                                                                    |
| ----- | ------------------------------------------------------------------------------ |
| Inode | Unique number with file metadata & data-block pointers                         |
| Links | Count of directory entries referencing this inode (starts at 1 for a new file) |
| Data  | Actual content blocks on disk                                                  |

<Callout icon="lightbulb">
  When you open or read a file, the kernel looks up its name, retrieves the inode (e.g., `52946177`), and accesses the data blocks. Hard links simply give you multiple names for the same inode.
</Callout>

## Sharing Files Without Duplication

Copying large directories wastes disk space:

```bash theme={null}
cp -r /home/aaron/Pictures/ /home/jane/Pictures/
```

Instead, Jane can create a hard link to Aaron’s photo:

```bash theme={null}
ln /home/aaron/Pictures/family_dog.jpg \
   /home/jane/Pictures/family_dog.jpg
```

* **Source**: `/home/aaron/Pictures/family_dog.jpg`
* **Link name**: `/home/jane/Pictures/family_dog.jpg`

Verify with `stat`:

```bash theme={null}
stat /home/jane/Pictures/family_dog.jpg
```

Now the link count is **2**:

```text theme={null}
Inode: 52946177    Links: 2
```

## Deletion Behavior

When Aaron removes his link, the data remains as long as one hard link exists:

```bash theme={null}
rm /home/aaron/Pictures/family_dog.jpg
stat /home/jane/Pictures/family_dog.jpg
```

* Link count drops to 1
* File content is still intact for Jane

Only when the last link is deleted does the filesystem free the inode and data:

```bash theme={null}
rm /home/jane/Pictures/family_dog.jpg
# inode 52946177 and its data blocks are now reclaimed
```

## Hard Link vs. Copy

| Operation | Disk Usage | Link Count | Independent Changes? |
| --------- | ---------- | ---------- | -------------------- |
| Copy      | +100%      | 1 each     | Yes                  |
| Hard Link | +0%        | >1         | No (shared inode)    |

<Callout icon="triangle-alert">
  * You cannot create hard links to directories (prevents filesystem loops).
  * Hard links must reside on the **same** filesystem—cross-device linking is not allowed.
</Callout>

## Managing Permissions for Shared Files

Since file permissions live in the inode, updating them on one hard link affects all links. To let both Aaron and Jane read/write:

1. Add both users to a common group (`family`):

   ```bash theme={null}
   sudo usermod -aG family aaron
   sudo usermod -aG family jane
   ```

2. Set group read/write permissions:

   ```bash theme={null}
   chmod 660 /home/aaron/Pictures/family_dog.jpg
   ```

Now both can modify the shared file seamlessly.

## Further Reading

* [stat(1) — Display File Status](https://man7.org/linux/man-pages/man1/stat.1.html)
* [ln(1) — Make Links](https://man7.org/linux/man-pages/man1/ln.1.html)
* [Understanding Linux Filesystems](https://www.kernel.org/doc/html/latest/filesystems/index.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/de71b96a-9dc0-4e92-987a-6c7055c44e8b/lesson/43f1c7d9-3aa0-4464-830d-6676106126a1" />
</CardGroup>


# Create and Change Soft Links

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/Devices-Linux-Filesystems-Filesystem-Hierarchy-Standard/Create-and-Change-Soft-Links/page

This article explains how to create, manage, and verify symbolic links in Linux, including their differences from hard links.

Symbolic links (or “soft links”) are pointers to files or directories, akin to Windows shortcuts. Unlike hard links, which reference the same inode on disk, a symlink stores the path to its target. When you access a symlink, the operating system follows that path and opens the real file or folder.

## Table: Hard Link vs. Symbolic Link

| Link Type     | Definition                                | Use Case                          | Limitation                        |
| ------------- | ----------------------------------------- | --------------------------------- | --------------------------------- |
| Hard Link     | Direct reference to the same inode        | Duplicate names for the same data | Cannot span filesystems           |
| Symbolic Link | Special file containing target’s pathname | Flexible alias or shortcut        | Broken if the target path changes |

## 1. Create a Symbolic Link

Use the `ln` utility with the `-s` (or `--symbolic`) flag:

```bash theme={null}
ln -s <path_to_target> <path_to_link>
