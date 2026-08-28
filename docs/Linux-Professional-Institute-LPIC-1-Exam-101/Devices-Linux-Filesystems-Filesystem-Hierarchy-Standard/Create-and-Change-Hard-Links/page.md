# -rw-rw-r-- 1 carol carol 118K Jul 11 16:36 Twitter_Down_20190711.jpg
# -rw-rw-r-- 1 carol carol 324K Jul  2 15:22 Xiaomi_Mimoji.png
```

### 4.3 Read-Only Snapshots

Immutable snapshots prevent accidental writes:

```bash theme={null}
sudo btrfs subvolume snapshot -r /mnt/disk /mnt/disk/snap-ro
```

## 5. Transparent Compression

Enable compression at mount time to reduce disk usage without manual compression commands.

```bash theme={null}
sudo mount -o compression=zstd /dev/sdb1 /mnt/disk
```

| Algorithm | Speed    | Compression Ratio |
| --------- | -------- | ----------------- |
| zlib      | Moderate | Good (default)    |
| lzo       | Fast     | Lower             |
| zstd      | Fastest  | Similar to zlib   |

<Frame>
  ![The image lists three compression algorithms: ZLIB (default), LZO (faster but lower compression ratio), and ZSTD (faster with a similar compression ratio to ZLIB).](https://kodekloud.com/kk-media/image/upload/v1752881380/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Create-Partitions-and-Filesystems-btrfs/compression-algorithms-zlib-lzo-zstd.jpg)
</Frame>

## Additional Resources

* [Btrfs Wiki](https://btrfs.wiki.kernel.org/)
* [Kernel Documentation – Btrfs](https://www.kernel.org/doc/html/latest/filesystems/btrfs.html)
* [Linux Man Pages – btrfs](https://man7.org/linux/man-pages/man5/btrfs.5.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/de71b96a-9dc0-4e92-987a-6c7055c44e8b/lesson/894c1fe4-148d-4b21-90cc-51def300423a" />
</CardGroup>


# Create and Change Hard Links

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/Devices-Linux-Filesystems-Filesystem-Hierarchy-Standard/Create-and-Change-Hard-Links/page

Learn how to create and manage hard links in Linux to share files efficiently without duplicating data.

In this lesson, you’ll learn how Linux uses inodes and hard links to share files efficiently—without duplicating data. We’ll cover:

* What inodes and links are
* Creating hard links
* Deletion behavior
* Common limitations
* Permission management

## What Are Inodes and Hard Links?

Every file on a Linux filesystem is represented by an **inode**, which stores metadata (permissions, timestamps, disk block locations). A **hard link** is simply another directory entry that points to the same inode.

Consider Aaron’s photo of his dog Milo, saved as:

```bash theme={null}
/home/aaron/Pictures/family_dog.jpg
```

Create this sample file and inspect its inode:

```bash theme={null}
