# Compress and Uncompress files

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Understand-and-Use-Essential-Tools/Compress-and-Uncompress-files/page

This guide explores methods to compress and decompress files on Linux, enhancing disk space management and file transfer speeds.

In this guide, we explore various methods to compress and decompress files on Linux. Compression not only saves disk space but also enhances file transfer speeds between systems.

Most Linux distributions come with several built-in compression utilities. The three most common are gzip, bzip2, and xz. Each of these tools offers a simple command-line interface.

<Callout icon="lightbulb">
  Using compression can significantly reduce file transfer times over slow networks.
</Callout>

## Basic Compression Techniques

For example, to compress a file using gzip, run:

```bash theme={null}
$ gzip file1
```

This command compresses `file1` and produces a new file named `file1.gz` while automatically deleting the original file. Similarly, you can compress other files with bzip2 or xz:

```bash theme={null}
$ bzip2 file2
$ xz file3
```

To decompress these files, you can use the corresponding utilities:

```bash theme={null}
$ gunzip file1.gz
$ bunzip2 file2.bz2
$ unxz file3.xz
```

<Callout icon="triangle-alert">
  By default, these commands delete the original uncompressed file. If you need to retain the source file, use the `-k` or `--keep` option.
</Callout>

## Preserving Original Files

To prevent the deletion of the original files after compression, use the `--keep` option. This option is available in gzip, bzip2, and xz. For example:

```bash theme={null}
$ gzip --keep file1
$ bzip2 --keep file2
$ xz --keep file3
```

You can view all the available options for a utility by running the `--help` command. For instance, to display gzip’s help information:

```plaintext theme={null}
$ gzip --help
Usage: gzip [OPTION]... [FILE]...
Compress or uncompress FILES (by default, compress FILES in-place).

  -c, --stdout         write on standard output, keep original files unchanged
  -d, --decompress     decompress
  -f, --force          force overwrite of output file and compress links
  -h, --help           give this help
  -k, --keep           keep (don't delete) input files
  -l, --list           list compressed file contents
  -L, --license        display software license
  -n, --no-name        do not save or restore the original name and timestamp
  -N, --name           save or restore the original name and timestamp
  -q, --quiet          suppress all warnings
  -r, --recursive      operate recursively on directories
  -S, --suffix=SUF     use suffix SUF on compressed files
  -s, --synchronous    synchronous output
  -t, --test           test compressed file integrity
  -v, --verbose        verbose mode
  -V, --version        display version number
```

Additionally, you can list information about a compressed file using the `--list` option with gzip:

```bash theme={null}
$ gzip --list file1.gz
         compressed        uncompressed  ratio uncompressed_name
               71                 78   39.7%    file1
```

## Archiving with ZIP and TAR

While gzip, bzip2, and xz are primarily focused on compressing a single file, the zip utility is capable of both archiving and compressing files. To create an archive containing `file1`, run:

```bash theme={null}
$ zip archive.zip file1
```

To compress an entire directory such as "Pictures" and include all subdirectories recursively, use the `-r` option:

```bash theme={null}
$ zip -r archive.zip Pictures/
```

It is important to note that gzip and similar utilities cannot archive multiple files into a single compressed file. In such cases, the tar utility is used to create an archive first, and then the archive is compressed with your chosen tool.

### Creating and Compressing Tar Archives

To create a simple tar archive containing `file1`:

```bash theme={null}
$ tar --create --file archive.tar file1
```

After creating the tar archive, you can compress it with gzip:

```bash theme={null}
$ gzip archive.tar
