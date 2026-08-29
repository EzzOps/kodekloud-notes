# File Compression and Archival

Source: https://notes.kodekloud.com/docs/Learning-Linux-Basics-Course-Labs/Working-with-Shell-II/File-Compression-and-Archival/page

This lesson explores file compression and archival techniques in Linux, covering tools, commands, and interactive labs for practical learning.

In this lesson, we continue our journey into the Linux shell by exploring file compression and archival techniques. You'll learn about several tools for compressing and archiving files, methods for searching files and directories, and basic pattern matching in Linux. In addition, there is an interactive lab that allows you to experiment with the VI Editor.

![The image lists Linux Core Concepts, including file compression, data extraction, and text editors, with associated labs for practical learning.](https://kodekloud.com/kk-media/image/upload/v1752881160/notes-assets/images/Learning-Linux-Basics-Course-Labs-File-Compression-and-Archival/frame_20.jpg)

Before diving into file compression and archival commands, let's start by checking the size of a file in Linux. The `du` command (short for disk usage) is widely used to determine file sizes.

:::note Viewing File Sizes
To display a file size in kilobytes, use the following command:
:::

```bash theme={null}
[~]$ du -sk test.img
100000
```

For a more user-friendly, human-readable format:

```bash theme={null}
[~]$ du -sh test.img
98M     test.img
```

Alternatively, you can use the `ls -lh` command to view file sizes in a human-readable format:

```bash theme={null}
[~]$ ls -lh test.img
```

## Using tar for Archival

The `tar` command is one of the most common utilities used to group multiple files or directories into a single archive file (tarball). This is particularly useful for data backup, transfer, and archiving.

To create a tar archive, use the `-c` option to create the archive and the `-f` option to specify the file name:

```bash theme={null}
[~]$ tar -cf test.tar file1 file2 file3
[~]$ ls -ltr test.tar
-rw-rw-r--  1 1281054720 Mar 13 19:48 test.tar
```

You can list the contents of a tarball using:

```bash theme={null}
[~]$ tar -tf test.tar
./file1
./file2
./file3
```

To extract files from a tar archive, use the `-x` option:

```bash theme={null}
[~]$ tar -xf test.tar
```

Additionally, to compress the tarball and reduce its file size, include the `-z` option:

```bash theme={null}
[~]$ tar -zcf test.tar file1 file2 file3
```

## Compression Commands in Linux

Linux offers several commands for compressing files. The choice of command depends on the type of data and required compression level. Below are examples using `bzip2`, `gzip`, and `xz`:

| Compression Utility | Command Example                                     | Compressed File Extension |
| ------------------- | --------------------------------------------------- | ------------------------- |
| bzip2               | \[\~]$ bzip2 test.img<br />[~]$ du -sh test.img.bz2 | .bz2                      |
| gzip                | \[\~]$ gzip test1.img<br />[~]$ du -sh test1.img.gz | .gz                       |
| xz                  | \[\~]$ xz test2.img<br />[~]$ du -sh test2.img.xz   | .xz                       |

Each command appends a specific file extension indicating the compression format: `.bz2` for `bzip2`, `.gz` for `gzip`, and `.xz` for `xz`.

:::note Decompressing Files
To uncompress these files, use the following commands:

* For bzip2: `bunzip2`
* For gzip: `gunzip`
* For xz: `unxz`
  :::

For example, here is how you decompress each file type:

```bash theme={null}
