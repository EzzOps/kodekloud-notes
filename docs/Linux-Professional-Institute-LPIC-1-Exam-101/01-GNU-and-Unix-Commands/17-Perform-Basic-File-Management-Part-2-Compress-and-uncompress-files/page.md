# Perform Basic File Management Part 2 Compress and uncompress files

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/GNU-and-Unix-Commands/Perform-Basic-File-Management-Part-2-Compress-and-uncompress-files/page

Learn to efficiently compress and decompress files on Linux using various tools to save storage space and speed up file transfers.

In this lesson, you’ll learn how to efficiently compress and decompress files on Linux using `gzip`, `bzip2`, `xz`, `zip`, and `tar`. Mastering these tools helps you save storage space and speed up file transfers across systems.

## Table of Contents

1. [Compression Utilities Overview](#compression-utilities-overview)
2. [Basic Compression with gzip, bzip2, and xz](#basic-compression-with-gzip-bzip2-and-xz)
3. [Keeping Original Files](#keeping-original-files)
4. [Creating and Extracting zip Archives](#creating-and-extracting-zip-archives)
5. [Combining tar with Compression](#combining-tar-with-compression)
6. [Links and References](#links-and-references)

***

## 1. Compression Utilities Overview

Most Linux distributions include three primary compression tools by default:

| Utility | File Extension | Compress Command | Decompress Command |
| ------- | -------------- | ---------------- | ------------------ |
| gzip    | .gz            | `gzip file`      | `gunzip file.gz`   |
| bzip2   | .bz2           | `bzip2 file`     | `bunzip2 file.bz2` |
| xz      | .xz            | `xz file`        | `unxz file.xz`     |

These utilities overwrite the original file with its compressed version unless you specify otherwise.

***

## 2. Basic Compression with gzip, bzip2, and xz

To compress a single file:

```bash theme={null}
$ gzip file1       # Creates file1.gz and deletes file1
$ bzip2 file2      # Creates file2.bz2 and deletes file2
$ xz file3         # Creates file3.xz and deletes file3
```

To decompress:

```bash theme={null}
$ gunzip file1.gz     # Restores file1 and deletes file1.gz
$ bunzip2 file2.bz2   # Restores file2 and deletes file2.bz2
$ unxz file3.xz       # Restores file3 and deletes file3.xz
```

You can also use the long-form `--decompress` (or `-d`) flag:

```bash theme={null}
$ gzip --decompress file1.gz
$ bzip2 --decompress file2.bz2
$ xz --decompress file3.xz
```

> **lightbulb** By default, these commands remove the original file after compressing or decompressing.

***

## 3. Keeping Original Files

To retain the input files alongside the compressed versions, add the `-k` (or `--keep`) flag:

```bash theme={null}
$ gzip --keep file1     # Leaves file1 and creates file1.gz
$ bzip2 --keep file2    # Leaves file2 and creates file2.bz2
$ xz --keep file3       # Leaves file3 and creates file3.xz
```

Check details of a compressed file using the `--list` (or `-l`) option:

```bash theme={null}
$ gzip --list file1.gz
   compressed     uncompressed  ratio  uncompressed_name
            71               78   39.7%  file1
```

***

## 4. Creating and Extracting zip Archives

The `zip` utility bundles and compresses files into a single archive. To compress individual files:

```bash theme={null}
$ zip archive.zip file1
  adding: file1 (deflated 40%)
```

Recursively compress a directory (e.g., `Pictures/`):

```bash theme={null}
$ zip -r archive.zip Pictures/
  adding: Pictures/ (stored 0%)
  adding: Pictures/family_dog.jpg (stored 0%)
```

Extract a `.zip` archive with `unzip`:

```bash theme={null}
$ unzip archive.zip
Archive:  archive.zip
  inflating: file1
  inflating: Pictures/family_dog.jpg
```

Unlike `gzip`, `bzip2`, and `xz`, the `zip` format natively supports multiple files and directories in one archive.

***

## 5. Combining tar with Compression

To package multiple files or directories and compress them in one step, use `tar` together with a compression option.

### 5.1 Creating a Tar Archive, Then Compressing

1. Create a tarball:
   ```bash theme={null}
   $ tar --create --file archive.tar file1 file2 dir/
   ```
2. Compress it:
   ```bash theme={null}
   $ gzip archive.tar        # → archive.tar.gz
   $ bzip2 archive.tar       # → archive.tar.bz2
   $ xz archive.tar          # → archive.tar.xz
   ```

### 5.2 One-Step Creation and Compression

Use the appropriate flag to combine creation and compression:

| Compressor | Short Option              | Command Example                       |
| ---------- | ------------------------- | ------------------------------------- |
| gzip       | `-z`                      | `tar -czf archive.tar.gz file1 dir/`  |
| bzip2      | `-j`                      | `tar -cjf archive.tar.bz2 file1 dir/` |
| xz         | `-J`                      | `tar -cJf archive.tar.xz file1 dir/`  |
| auto       | `--auto-compress` or `-a` | `tar -caf archive.tar.gz file1 dir/`  |

### 5.3 Extracting Compressed Tarballs

`tar` auto-detects compression, so extracting is straightforward:

```bash theme={null}
$ tar --extract --file archive.tar.gz    # or
$ tar xf archive.tar.xz
```

> **triangle-alert** Overwriting existing files when extracting archives can lead to data loss. Always verify the contents before extraction or use `--list` (`-t`) to preview:

  ```bash theme={null}
  $ tar -tf archive.tar.gz
  ```

***

## Links and References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [GNU tar Manual](https://www.gnu.org/software/tar/manual/)
* [Linux gzip Command](https://linux.die.net/man/1/gzip)
* [Linux zip Command](https://linux.die.net/man/1/zip)

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/2490f961-886c-4531-be8c-915cccff60a9/lesson/7c37d5c7-fcc9-4552-a8ff-c13e34dc01d8)
