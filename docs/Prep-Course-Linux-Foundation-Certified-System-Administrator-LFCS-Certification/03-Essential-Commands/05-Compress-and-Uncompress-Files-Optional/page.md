# Compress and Uncompress Files Optional

Source: https://notes.kodekloud.com/docs/Prep-Course-Linux-Foundation-Certified-System-Administrator-LFCS-Certification/Essential-Commands/Compress-and-Uncompress-Files-Optional/page

Learn to compress and uncompress files in Linux using utilities like gzip, bzip2, xz, and zip for efficient file management.

In this article, you will learn how to compress and uncompress files in Linux. File compression reduces storage space and speeds up file transfers between systems. Most Linux distributions come with at least three built-in compression utilities: gzip, bzip2, and xz.

## Basic Compression with gzip and bzip2

Below is a simple example of compressing files with gzip and bzip2:

```bash theme={null}
$ gzip file1
$ bzip2 file2
```

When these commands are executed, each file is compressed into a new file (e.g., file1 becomes file1.gz and file2 becomes file2.bz2) and the original file is automatically deleted.

## Decompressing Files

To restore the original files, use the corresponding decompression commands for gzip, bzip2, and xz:

```bash theme={null}
$ gunzip file1.gz
$ bunzip2 file2.bz2
$ unxz file3.xz
```

## Retaining the Original File

Sometimes you may want to compress a file without deleting the original. Most Linux compression utilities offer an option to keep the original file. Use the `--help` flag to check available options:

```bash theme={null}
$ gzip --help
Usage: gzip [OPTION]... [FILE]...
Compress or uncompress FILEs (by default, compress FILES in-place).

Mandatory arguments to long options are mandatory for short options too.
  -c, --stdout       write on standard output, keep original files unchanged
  -d, --decompress   decompress
  -f, --force        force overwrite of output file and compress links
  -h, --help         give this help
  -k, --keep         keep (don't delete) input files
  -l, --list         list compressed file contents
  -L, --license      display software license
  -N, --no-name      do not save or restore the original name and timestamp
  -n, --name         save or restore the original name and timestamp
  -q, --quiet        suppress all warnings
  -r, --recursive    operate recursively on directories
  --rsyncable        make rsync-friendly archive
  -S, --suffix=SUF   use suffix SUF on compressed files
  --synchronous      synchronous output
  -t, --test         test compressed file integrity
  -v, --verbose      verbose mode
  -V, --version      display version number
```

> **lightbulb** Using the `--keep` (or `-k`) option retains the original file when compressing.

Here are examples of using the `--keep` option:

```bash theme={null}
$ gzip --keep file1
$ bzip2 --keep file2
$ xz --keep file3
```

## Inspecting Compressed File Contents

If you need to view the contents of a compressed file, you can use the `--list` option. For example:

```bash theme={null}
$ gzip --list file1
compressed        uncompressed      ratio   uncompressed_name
71                78               39.7%   file1
```

## Working with the zip Utility

While gzip, bzip2, and xz are popular for compressing individual files, the zip utility can compress an entire directory or multiple files into a single archive.

### Archiving a Single File with zip

```bash theme={null}
$ zip archive.zip file1
adding: file1 (deflated 40%)
```

### Compressing an Entire Directory

```bash theme={null}
$ zip -r archive.zip Pictures/
adding: Pictures/ (stored 0%)
adding: Pictures/family_dog.jpg (stored 0%)
```

To extract a zip archive, use the following command:

```bash theme={null}
$ unzip archive.zip
Archive:  archive.zip
replace file1? [y]es, [n]o, [A]ll, [N]one, [r]ename: N
```

## Using tar for Archiving and Compression

Unlike zip, utilities like gzip do not support compressing multiple files into a single archive. Instead, tar is commonly used to bundle files together before compression.

### Creating a Tar Archive and Compressing it

```bash theme={null}
$ tar --create --file archive.tar file1
$ gzip archive.tar
