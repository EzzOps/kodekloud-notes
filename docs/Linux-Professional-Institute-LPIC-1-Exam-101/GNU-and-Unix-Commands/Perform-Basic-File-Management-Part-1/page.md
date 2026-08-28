# Perform Basic File Management – Part 1

## Simple and Advanced Wildcard Specifications in Commands

In this lesson, you’ll master wildcard (glob) patterns in Linux to search, copy, move, or delete files efficiently. Wildcards are symbols that stand for one or more characters in file names or paths. We’ll cover three primary types:

* Asterisk (`*`)
* Question mark (`?`)
* Bracketed expressions (`[ ]`)

<Frame>
  ![The image explains types of wildcards: asterisk (\*) for zero or more occurrences, question mark (?) for a single occurrence, and brackets (\[\]) for specific character occurrences, with an example of \[0-9\] matching all digits.](https://kodekloud.com/kk-media/image/upload/v1752881396/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Perform-Basic-File-Management-Part-1-Simple-and-advanced-wildcard-specifications-in-commands/wildcards-asterisk-question-brackets-example.jpg)
</Frame>

***

## Wildcard Reference Table

| Wildcard | Matches                             | Example Pattern | Matches                               |
| -------- | ----------------------------------- | --------------- | ------------------------------------- |
| `*`      | Zero or more characters             | `*.log`         | `kern.log`, `sys.log`, `apperror.log` |
| `?`      | Exactly one character               | `?.conf`        | `a.conf`, `b.conf`, *not* `ab.conf`   |
| `[ ]`    | Any one character in a set or range | `[0-9].txt`     | `1.txt`, `5.txt`, `9.txt`             |

***

## 1. Asterisk (`*`)

The asterisk is the most flexible wildcard—it matches any string of characters (even an empty string).

```bash theme={null}
# Find all .png images in /home and its subdirectories
find /home -name "*.png"

# List all text files beginning with "lpic-"
ls lpic-*.txt

# Copy all contents under 'animal/' into 'forest/' recursively
cp -r animal/* forest/

# Delete any file whose name contains "ate"
rm *ate*
```

<Callout icon="lightbulb">
  In interactive shells, wrap `*` patterns in quotes (e.g., `"*.png"`) to prevent premature expansion by your shell.
</Callout>

You can use multiple asterisks in a single pattern, at any position:

```bash theme={null}
# Matches names like 'backup-2021-01-*.tar.gz'
ls backup-*-*.tar.gz
```

***

## 2. Question Mark (`?`)

The question mark matches exactly one character. It’s ideal for pinpointing files that differ by a single letter or digit.

```bash theme={null}
# Directory listing
ls
# Match any single char between 'l' and 'st.txt'
ls l?st.txt
# Two ? characters allow any two-character prefix
ls ??st.txt
# Output: last.txt  lest.txt  list.txt  past.txt
```

***

## 3. Bracketed Characters (`[ ]`)

Square brackets let you match one character from a specified set or range.

```bash theme={null}
# Only 'last.txt' or 'lest.txt'
ls l[aef]st.txt

# Any lowercase letter between 'a' and 'z'
ls l[a-z]st.txt
```

Combine multiple bracket sets for more control:

```bash theme={null}
ls
# Match student-<digit><uppercase>.txt
ls student-[0-9][A-Z].txt
# Output: student-1A.txt  student-2A.txt
```

***

## 4. Combining Wildcards

For advanced file matching, mix wildcards in a single pattern:

```bash theme={null}
ls
# [plf] = p, l, or f ; ? = one char ; * = zero or more chars
ls [plf]?st*
# Output: last.txt  lest.txt  list.txt  past.txt
```

Another practical example:

```bash theme={null}
ls
# f* = names starting with 'f'; [0-9] ensures one digit before .txt
ls f*[0-9].txt
# Output: file1.txt  file23.txt  fom23.txt
```

<Callout icon="triangle-alert">
  Be cautious when using wildcards with destructive commands like `rm`. Always double-check your pattern with `ls` before deletion.
</Callout>

***

## Links and References

* [Bash Manual – Pattern Matching](https://www.gnu.org/software/bash/manual/bash.html#Pattern-Matching)
* [Linux Glob How-To](https://tldp.org/LDP/abs/html/globbingref.html)
* [Kubernetes Documentation](https://kubernetes.io/docs/)

That concludes Part 1 of wildcard specifications. In the next lesson, we’ll dive deeper into escape sequences and advanced glob qualifiers.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/2490f961-886c-4531-be8c-915cccff60a9/lesson/f6a282c3-a525-46e1-b479-9455f24b31d2" />
</CardGroup>


# Perform Basic File Management Part 1

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/GNU-and-Unix-Commands/Perform-Basic-File-Management-Part-1/page

This guide covers essential Linux file operations to streamline your workflow on any Unix-like system.

In this guide, you’ll master essential Linux file operations—listing, creating, copying, moving, and deleting files and directories—to streamline your workflow on any Unix-like system.

## Table of Contents

1. [Key Concepts](#key-concepts)
2. [Listing Files and Directories](#listing-files-and-directories)
3. [Filesystem Structure](#filesystem-structure)
4. [Creating Files and Directories](#creating-files-and-directories)
5. [Copying Files and Directories](#copying-files-and-directories)
6. [Moving and Renaming](#moving-and-renaming)
7. [Deleting Files and Directories](#deleting-files-and-directories)
8. [Summary of Commands](#summary-of-commands)
9. [References](#references)

## Key Concepts

Before you begin, make sure you understand:

* The Linux filesystem tree and hierarchy
* The difference between **absolute paths** and **relative paths**
* How to navigate directories with `cd` and identify your location with `pwd`

<Callout icon="lightbulb">
  Absolute paths start at the root directory `/` while relative paths are based on your current working directory.
</Callout>

## Listing Files and Directories

Use the `ls` command to display directory contents:

```bash theme={null}
$ ls
Documents  Desktop  Downloads  Music  Pictures  Videos
```

Show hidden files (those starting with a dot) with `-a`:

```bash theme={null}
$ ls -a
.  ..  .bashrc  .profile  Documents  Desktop  Downloads  Music  Pictures  Videos
```

For a detailed (long) listing including permissions, ownership, size, and timestamp, add `-l`:

```bash theme={null}
$ ls -l /var/log
total 4064
drwxr-xr-x 2 root root    4096 Oct 18 22:52 anaconda
drw------- 2 root root    4096 Oct 18 22:53 audit
-rw------- 1 root root   19524 Nov  1 17:56 boot.log
...
```

Combine options to save time:

```bash theme={null}
$ ls -al        # same as ls -a -l
$ ls -ahl       # human-readable sizes with -h
```

## Filesystem Structure

Linux organizes files in an inverted tree structure:

* Root directory: `/`
* Standard subdirectories: `/home`, `/var`, `/etc`, `/usr`, etc.
* Each folder can contain files and more subdirectories

### Absolute Paths

Absolute paths always begin at `/`.\
Example:

```text theme={null}
/home/aaron/documents/invoice.pdf
```

### Relative Paths

Relative paths depend on your current directory. Check it with:

```bash theme={null}
$ pwd
/home/aaron
```

Change directories using `cd`:

```bash theme={null}
$ cd /var/log           # absolute path
$ cd /home/aaron        # absolute path
$ cd ..                 # up one level
$ cd documents          # down into current dir’s "documents"
```

<Frame>
  ![The image shows a directory structure with a command line interface on the left. The directory tree includes folders like "home," "var," and "root," with a file named "Invoice.pdf" under "aaron/Documents."](https://kodekloud.com/kk-media/image/upload/v1752881397/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Perform-Basic-File-Management-Part-1/directory-structure-command-line-invoice.jpg)
</Frame>

From `/home/aaron`, these relative paths resolve to:

* `documents/invoice.pdf` → `/home/aaron/documents/invoice.pdf`
* `invoice.pdf` → `/home/aaron/invoice.pdf`
* `../invoice.pdf` → `/home/invoice.pdf`
* `../../invoice.pdf` → `/invoice.pdf`

Additional `cd` shortcuts:

```bash theme={null}
$ cd /      # go to root
$ cd       # go to your home directory
$ cd -     # switch to previous directory
```

## Creating Files and Directories

* Create an empty file:

  ```bash theme={null}
  $ touch receipt.pdf
  ```

* Create a new directory:

  ```bash theme={null}
  $ mkdir receipts
  ```

## Copying Files and Directories

Use `cp [source] [destination]`:

* Copy a file into a directory:

  ```bash theme={null}
  $ cp receipt.pdf receipts/
  ```

* Copy and rename:

  ```bash theme={null}
  $ cp receipt.pdf receipts/receipt_copy.pdf
  ```

* Copy a directory recursively:

  ```bash theme={null}
  $ cp -r receipts/ backup_of_receipts/
  ```

  Ensure `backup_of_receipts` does not already contain a `receipts` subdirectory.

## Moving and Renaming

Use `mv [source] [destination]` to move or rename:

```bash theme={null}
$ mv receipt.pdf receipts/                      
$ mv receipts/receipt.pdf receipts/old_receipt.pdf  
$ mv receipts/ old_receipts/                    
```

`mv` works seamlessly on both files and directories.

## Deleting Files and Directories

<Callout icon="triangle-alert">
  `rm -r` permanently deletes directories and their contents. Use with caution to avoid data loss.
</Callout>

* Remove a file:

  ```bash theme={null}
  $ rm invoice.pdf
  ```

* Remove a directory recursively:

  ```bash theme={null}
  $ rm -r invoices/
  ```

Always include `-r` when deleting directories.

## Summary of Commands

| Command | Description                          | Example                    |
| ------- | ------------------------------------ | -------------------------- |
| ls      | List directory contents              | `ls -ahl /var/log`         |
| pwd     | Print working directory              | `pwd`                      |
| cd      | Change directory                     | `cd /home/aaron/documents` |
| touch   | Create an empty file                 | `touch newfile.txt`        |
| mkdir   | Create a new directory               | `mkdir project`            |
| cp      | Copy files or directories            | `cp -r src/ dest/`         |
| mv      | Move or rename files and directories | `mv oldname newname`       |
| rm      | Remove files or directories          | `rm -r obsolete_folder/`   |

## References

* [GNU Coreutils Manual](https://www.gnu.org/software/coreutils/manual/coreutils.html)
* [Linux File System Basics](https://www.tldp.org/LDP/intro-linux/html/sect_03_01.html)
* [Bash Reference Manual](https://www.gnu.org/software/bash/manual/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/2490f961-886c-4531-be8c-915cccff60a9/lesson/bc254632-a371-4fc5-9ad5-3d95cf332d4f" />
</CardGroup>
