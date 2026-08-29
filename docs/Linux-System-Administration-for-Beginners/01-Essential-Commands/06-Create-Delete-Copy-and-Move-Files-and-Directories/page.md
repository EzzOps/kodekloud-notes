# Compress
gzip   file1       # → file1.gz
bzip2  file2       # → file2.bz2
xz     file3       # → file3.xz

# Decompress
gunzip   file1.gz   # → file1
bunzip2  file2.bz2  # → file2
unxz     file3.xz   # → file3
```

Alternatively, use the long options for clarity:

```bash theme={null}
gzip  --decompress file1.gz
bzip2 --decompress file2.bz2
xz    --decompress file3.xz
```

> **triangle-alert** By default, `gzip`, `bzip2`, and `xz` delete the original file after (de)compression. Use `-k` or `--keep` to preserve input files.

***

## Preserving Original Files

To keep both the source and the compressed version, add the `-k` (keep) flag:

```bash theme={null}
gzip  --keep file1       # Keeping file1 and creating file1.gz
bzip2 --keep file2       # Keeping file2 and creating file2.bz2
xz    --keep file3       # Keeping file3 and creating file3.xz
```

You can confirm the flag via:

```bash theme={null}
gzip --help | grep -E '^-k, --keep'
#  -k, --keep   keep (don't delete) input files
```

***

## Inspecting Compressed Archives

To view metadata (compressed size, uncompressed size, compression ratio), use the `--list` (`-l`) option:

```bash theme={null}
gzip --list file1.gz
# compressed  uncompressed  ratio uncompressed_name
bzip2 --list file2.bz2
xz    --list file3.xz
```

***

## Working with ZIP Archives

Unlike `gzip`/`bzip2`/`xz`, the `zip` utility can bundle multiple files or directories into a single archive:

```bash theme={null}
# Create or update archive.zip with file1
zip archive.zip file1
# Recursively add a directory
zip -r archive.zip Pictures/
# adding: Pictures/ (stored 0%)
# adding: Pictures/family_dog.jpg (stored 0%)
```

To extract everything from a ZIP archive:

```bash theme={null}
unzip archive.zip
# Archive: archive.zip
#   inflating: file1
#   inflating: Pictures/family_dog.jpg
```

***

## Combining tar with Compression

Since `gzip`, `bzip2`, and `xz` operate on single files, `tar` is used to first archive multiple files/directories, then compress the archive.

### Two-Step Archiving

```bash theme={null}
# 1. Create an uncompressed tarball
tar --create --file archive.tar file1 file2 dir1/

# 2. Compress the tarball
gzip archive.tar         # → archive.tar.gz
# or
bzip2 archive.tar        # → archive.tar.bz2
# or
xz archive.tar           # → archive.tar.xz
```

### One-Step Archiving with Compression

Leverage `tar`’s built-in compression flags:

```bash theme={null}
tar --create --gzip   --file archive.tar.gz  file1 file2 dir1/
tar --create --bzip2  --file archive.tar.bz2 file1 file2 dir1/
tar --create --xz     --file archive.tar.xz  file1 file2 dir1/
```

Or use auto-compression (`-a`) to match the extension:

```bash theme={null}
tar --create --auto-compress --file archive.tar.gz file1
# shorthand
tar caf archive.tar.xz file1
```

### Extracting Compressed Tarballs

`tar` will detect compression automatically:

```bash theme={null}
tar --extract --file archive.tar.gz
tar xf archive.tar.bz2
tar xf archive.tar.xz
```

***

## References

* [GNU gzip Manual](https://www.gnu.org/software/gzip/manual/)
* [GNU bzip2 Manual](https://www.sourceware.org/bzip2/)
* [XZ Utils Documentation](https://tukaani.org/xz/)
* [tar — GNU tar Manual](https://www.gnu.org/software/tar/manual/)
* [zip & unzip – Info-ZIP](https://infozip.sourceforge.net/)

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/cc1949d1-8171-4c8c-b69f-86f96cad0bbe/lesson/bf4f9042-d38d-497a-9ed8-51fb7fee3fa8)


# Create Delete Copy and Move Files and Directories

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/Essential-Commands/Create-Delete-Copy-and-Move-Files-and-Directories/page

Learn to manage files and directories in Linux using commands like ls, touch, mkdir, cp, mv, and rm.

Managing files and directories is a foundational skill for any Linux user or administrator. In this guide, you’ll learn how to list, create, copy, move (or rename), and delete files and directories using core commands like `ls`, `touch`, `mkdir`, `cp`, `mv`, and `rm`.

## Listing Files and Directories with `ls`

The `ls` (list) command displays directory contents. By default, hidden files (those beginning with `.`) are not shown.

### Common `ls` Usage

| Flag   | Description                              | Example          |
| ------ | ---------------------------------------- | ---------------- |
| (none) | Show non-hidden items                    | `ls`             |
| `-a`   | Include all entries, including `.` files | `ls -a`          |
| `-l`   | Long format (permissions, owner, size)   | `ls -l /var/log` |
| `-h`   | Human-readable sizes (use with `-l`)     | `ls -lh`         |
| `-alh` | Combine all flags                        | `ls -alh`        |

#### Basic Listing

```bash theme={null}
$ ls
Desktop  Documents  Downloads  Music  Pictures  Videos
```

#### Including Hidden Files

```bash theme={null}
$ ls -a
.   ..   .bashrc   .ssh   Desktop   Documents   Downloads   Music   Pictures   Videos
```

#### Detailed, Human-Readable Output

```bash theme={null}
$ ls -alh
total 76K
drwx------. 16 aaron aaron 4.0K Nov  1 17:57 .
drwxr-xr-x.  7 root  root  4.0K Oct 26 16:54 ..
-rw-------   1 aaron aaron 5.0K Nov  1 17:56 .bash_history
...
```

## Understanding the Linux File System Tree

Linux files and directories form an inverted tree with `/` as the root. Every path you use is either absolute (from `/`) or relative (from your current directory).

* `/`
  * `/home`
    * `/home/aaron`
      * `/home/aaron/Documents`
      * `/home/aaron/Downloads`
  * `/var`
  * `/etc`

> **lightbulb** Absolute paths start with `/` and always refer to the same location.\
  Relative paths begin from your current directory (check with `pwd`).

### Absolute Path

```text theme={null}
/home/aaron/Documents/invoice.pdf
```

### Relative Path

```bash theme={null}
$ pwd
/home/aaron
