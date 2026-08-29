# Example output:
/Users/alan/Pictures

ls
# Example output:
Camera\ Roll  Photo\ Booth\ Library  kody.png  Photos\ Library.photoslibrary

ls -l kody.png
# Example output:
-rw-------@ 1 alan staff 1210528 Jan 14 15:22 kody.png
```

The `ls -l` output shows important metadata: owner, permissions, size, and timestamps. Behind the scenes, the OS stores this metadata in internal records (directory tables or metadata entries) that map file names to where their data blocks live on storage.

<Frame>
  <img alt="A presentation slide showing a &#x22;Directory Table&#x22; with rows for filenames, paths, types, sizes, creation dates and permissions. A person stands to the right of the slide, gesturing while speaking." />
</Frame>

You normally see one row of this table at a time (a filename and its details), but the OS consults the full table to locate and open file data.

Example (simplified directory-table rows):

```text theme={null}
File Name      | Path              | Type    | Size (bytes) | Created     | Permissions
---------------------------------------------------------------------------------------
filename.txt   | /home/user/...    | regular | 4096         | 2024-06-18  | rw-r--r--
dir1           | /home/user/...    | dir     | -            | 2024-06-12  | rwxr-xr-x
script.sh      | /home/user/...    | regular | 532          | 2024-06-10  | rwxr-x--
```

When you open a file, the OS looks up its directory entry, finds the disk blocks (or extents) that hold the file contents, and reads those blocks into memory for your application.

Quick quiz
What does a folder actually represent?

A) A separate storage location\
B) A physical container on the hard drive\
C) A label/entry in the directory table

Correct answer: C — folders are metadata the OS uses to organize files. The icons and colors you see in a file manager are visual aids; to the OS they are directory entries mapping names to storage locations.

<Frame>
  <img alt="A presenter stands beside a colorful quiz slide titled &#x22;What does a folder actually represent?&#x22; showing multiple-choice answers and a cartoon cat with a speech bubble about color‑coding folders. The presenter is wearing a KodeKloud shirt." />
</Frame>

## File systems: the rule books for storage

A file system defines the rules the OS uses to name files, place them on storage, and keep track of metadata (owner, permissions, timestamps). If your OS doesn’t understand the file system on a device, it can’t interpret the bits on that device — even when physically connected.

Common file systems differ in features, compatibility, and limits.

<Frame>
  <img alt="A presenter stands on the right in front of a dark infographic showing USB-related icons (USB stick, phone, external drive, camera) and folders, with the heading “Same connection. Different outcomes.”" />
</Frame>

### Major file systems: FAT32, ExFAT, ext4, NTFS

Below is a quick reference comparison to help choose the right file system for common tasks.

| File System | Typical use case                                     | Pros                                                          | Cons                                                                                    |
| ----------- | ---------------------------------------------------- | ------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| FAT32       | USB sticks, SD cards for maximum compatibility       | Very widely supported across devices and OSes                 | Max file size \~4 GB; limited partition sizes; no journaling or rich permissions        |
| ExFAT       | Large files on removable media (videos, disk images) | Supports files >4 GB; broad modern OS/device support          | No journaling or rich permissions; slightly less ubiquitous than FAT32 on older devices |
| ext4        | Linux internal disks and servers                     | Journaling, speed, reliability, Linux-native features         | Not natively supported on Windows/macOS without drivers                                 |
| NTFS        | Windows internal drives and advanced features        | Permissions, encryption, journaling, resilient metadata (MFT) | macOS mounts read-only by default; incomplete support on other OSes without drivers     |

FAT32 (File Allocation Table)

* Breaks storage into clusters. Files may be stored in clusters that are not contiguous.
* Directory entries point to the starting cluster, and the FAT (a linked list table) is followed to find subsequent clusters (e.g., 17 → 23 → 45 → END).
* Simple and broadly compatible, but limited to \~4 GB per file.

<Frame>
  <img alt="A presenter stands to the right of a slide showing a diagram of FAT32 file allocation with a grid of storage clusters and PNG file parts, with &#x22;Clusters&#x22; and &#x22;Storage&#x22; labels and a KodeKloud logo on the speaker's shirt." />
</Frame>

FAT32 follows a cluster chain:

<Frame>
  <img alt="A presentation slide showing a FAT32 cluster chain diagram (blocks 17 → 23 → 45 → END) and a &#x22;choose your own adventure&#x22; book icon on a black background. A man in a black KodeKloud t‑shirt stands to the right, appearing to present." />
</Frame>

ExFAT

* Designed to overcome FAT32’s file-size limit while remaining cross-platform.
* Ideal for large media files on removable drives.
* Does not provide the richer metadata features (permissions, journaling) found in modern internal filesystems.

ext4 (common on Linux)

* Uses inodes: each inode stores metadata and pointers to data blocks (with indirect pointers for large files).
* Supports journaling to reduce corruption risk after crashes.
* Performs well on Linux but requires additional tools or drivers to access natively on Windows/macOS.

<Frame>
  <img alt="A presentation slide showing a FAT32 file allocation table (table of filenames, paths, types, sizes, creation dates and permissions). The presenter is wearing a &#x22;KodeKloud&#x22; shirt and is gesturing while explaining." />
</Frame>

NTFS (Windows default)

* Uses a Master File Table (MFT): a centralized index where each file’s name, metadata, and storage pointers are recorded.
* Provides advanced features: ACL-based permissions, encryption, compression, and journaling.
* Best for Windows system drives; other OSes may need extra drivers to write reliably.

<Frame>
  <img alt="A presentation slide about the NTFS file system showing a file icon labeled &#x22;Report.txt&#x22; with timestamps, permissions, and extents listed, alongside a stylized master file table graphic. A man wearing a KodeKloud shirt stands to the right speaking." />
</Frame>

<Frame>
  <img alt="A presenter stands to the right of a slide titled &#x22;Choose the right tool for the job&#x22; that compares filesystem types (FAT32, exFAT, ext4, NTFS) and their features. The speaker is wearing a KodeKloud shirt." />
</Frame>

### A short note on journaling

> **lightbulb** Journaling records pending filesystem operations (a short transaction log). After a crash, the OS replays or rolls back those journal entries to restore consistency, greatly reducing the chance of corruption and improving recovery time.

## Mounting: attaching a device into the directory tree

Even when the OS understands a file system, a device must be mounted to make its files part of the system’s directory tree. Until mounted, a device may only charge or show as an unrecognized format.

Typical mount points by OS:

* Linux/macOS example mount points:

```text theme={null}
/mnt/usb
/Volumes/USB
```

* Windows:

```text theme={null}
D:\
```

Mounting connects the device’s root into the OS directory tree so you can navigate it with the normal path hierarchy.

> **warning** Formatting a disk erases its data. Always back up important files before reformatting or changing the filesystem on removable or internal drives.

## Quick decision guides

* Need to move a 10 GB video between macOS and Windows? Use `ExFAT`.
* Need rich permissions and journaling for a Linux server disk? Use `ext4`.
* Sharing tiny files with older cameras or very old devices? `FAT32` might still be required.
* Windows system drive or heavy use of ACLs/encryption? `NTFS`.

Final quiz
You're on a Mac and need to format a USB drive to hold a 10 GB video. Which file system should you choose?

A) FAT32\
B) ExFAT\
C) NTFS

Correct answer: B — ExFAT. FAT32 has a \~4 GB file-size limit. NTFS is typically read-only by default on macOS without extra drivers.

## Recap

* Files are blocks of data; folders are directory entries (metadata) used to organize them.
* Paths (absolute and relative) locate files within the directory tree.
* The OS maps filenames to storage locations using directory tables, inodes, or an MFT depending on the filesystem.
* Common filesystems (FAT32, ExFAT, ext4, NTFS) trade compatibility, maximum file size, permissions, and journaling differently — pick the right one for the job.
* Journaling improves crash recovery; mounting integrates a device’s filesystem into your directory tree so it’s accessible.

- [Watch Video](https://learn.kodekloud.com/user/courses/operating-systems-and-applications/module/edbf48fe-cad8-4a13-ad00-644b613f7867/lesson/f3bb4db3-f4b5-4ea4-9904-4957ca32fab2)


# File Management Part 2

Source: https://notes.kodekloud.com/docs/Operating-Systems-and-Applications/File-Management/File-Management-Part-2/page

Overview of Unix-like file permissions including roles, read write execute types, inspecting and changing permissions with ls and chmod, plus examples and summaries

Every file and folder on your system has permissions — rules that control who can access them and what actions they can perform. This article explains file permission roles and types on Unix-like systems, demonstrates how to inspect and change permissions, and summarizes the key concepts for quick reference.

## Who controls a file?

Earlier we covered different user account types: administrators (who can use elevated privileges), standard users (day-to-day accounts), and guests (limited access). The OS maps those accounts to roles for each file:

* user — the file's owner
* group — a set of users that share access
* other — everyone else on the system

<Frame>
  <img alt="A presenter stands to the right of a slide showing a stylized folder with documents and three gradient boxes labeled &#x22;User,&#x22; &#x22;Group,&#x22; and &#x22;Other.&#x22; The slide is explaining file roles (how the OS handles the file)." />
</Frame>

On Windows, permissions are typically handled with Access Control Lists (ACLs), which provide more granular control over individual accounts and groups. Across platforms, the general pattern holds: regular users control their own files, guests are restricted, and administrators (or root) can override restrictions when using elevated privileges (for example, using `sudo` on Unix-like systems).

## What types of permissions exist?

There are three basic permission types:

* Read (`r`): view the file contents
* Write (`w`): modify or delete the file
* Execute (`x`): run the file as a program or script

These three permissions apply separately to the three roles (user, group, other), producing nine permission bits in total. The common textual representation you see from `ls -l` is a ten-character string: the first character indicates file type and the next nine are the permission bits.

> **lightbulb** The first character in the `ls -l` string indicates the file type (for example, `-` for a regular file, `d` for a directory, `l` for a symlink). The following nine characters appear as three groups of `rwx` corresponding to user, group, and other.

Example permission string:

```text theme={null}
-rwxr-xr--
```

Breakdown:

* Characters 2–4 (`rwx`) — owner's permissions: read, write, execute
* Characters 5–7 (`r-x`) — group's permissions: read and execute (no write)
* Characters 8–10 (`r--`) — others' permissions: read only

If a permission is missing, it is shown as a dash (`-`).

## Permission letters and their numeric (octal) equivalents

Here's a quick mapping between the `rwx` letters and the octal values commonly used with `chmod`.

| Permission letters | Octal value | Description                        |
| ------------------ | ----------- | ---------------------------------- |
| `rwx`              | `7`         | read (4) + write (2) + execute (1) |
| `rw-`              | `6`         | read (4) + write (2)               |
| `r-x`              | `5`         | read (4) + execute (1)             |
| `r--`              | `4`         | read (4) only                      |
| `---`              | `0`         | no permissions                     |

You can set permissions with octal notation, for example `chmod 755 file` sets owner to `7` (`rwx`) and group/other to `5` (`r-x`).

## Quick demo — create a script and set execute permission

Follow this short demo to see permission behavior and how to add execute permission.

```bash theme={null}
