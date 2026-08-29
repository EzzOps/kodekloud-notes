# Resolve a name to an IP
dig +short www.calicatnip.com

# Test reachability to an IP (Linux/macOS)
ping -c 4 203.0.113.42
```

- [Watch Video](https://learn.kodekloud.com/user/courses/networks-and-communications/module/f96c3ffe-8569-4a9d-99c2-2fe528af47cb/lesson/f076f33d-2d0d-4544-9004-a956913553cf)


# File Management Part 1

Source: https://notes.kodekloud.com/docs/Operating-Systems-and-Applications/File-Management/File-Management-Part-1/page

Explains files, folders, paths, mounting and common filesystems including FAT32, ExFAT, ext4, NTFS and journaling

We save files all the time — photos, screenshots, essays. But where do these files actually live? And what decides whether you or someone else can open them later?

This lesson explains two core concepts: files and file management. You'll learn where data is stored, how it's organized, and how the operating system (OS) enforces access. We'll cover:

* What a file and folder (directory) actually are
* Paths: absolute vs relative
* How the OS maps names to data (directory tables / metadata)
* Common file systems (FAT32, ExFAT, ext4, NTFS) and their tradeoffs
* Journaling, mounting, and practical choices for formatting drives

Think of the OS as a librarian: it doesn't just dump items on shelves — it catalogs them, places them in the right drawer, and controls who can read or write them.

<Frame>
  <img alt="A presenter wearing a KodeKloud t-shirt gestures on the right side of the image. To the left is a black-background diagram with a laptop icon, file and folder icons arranged in a hierarchical tree, and the word &#x22;macOS&#x22; next to a Windows-style logo." />
</Frame>

## Basics: files, folders, and paths

A file is a block of digital data — an image, document, executable, etc. Folders (directories) are entries in the OS’s directory table that group files into a hierarchical structure. At the very top is the root directory:

* Windows root example: `C:\`
* macOS / Linux root: `/`

From the root the OS builds a directory tree. A full (absolute) path shows exactly where a file lives. For example, a photo file:

* Absolute path:

```text theme={null}
/Users/alan/Pictures/kody.png
```

* Relative path (from `/Users/alan`):

```text theme={null}
Pictures/kody.png
```

Command-line examples (macOS / Linux style) demonstrate how you inspect the current location and list files:

```bash theme={null}
cd ~/Pictures
pwd
