# Find all SUID files
find / -perm /4000

# Find all SGID files
find / -perm /2000

# Find files with either SUID or SGID (or both)
find / -perm /6000
```

***

## 4. Sticky Bit on Directories

The sticky bit ensures that only the file owner (or root) can delete or rename files within a shared directory.

### Step-by-Step

1. Create a directory and view its default permissions:
   ```bash theme={null}
   mkdir stickydir
   ls -ld stickydir
   # drwxrwxr-x. 2 aaron aaron 6 Apr 26 05:14 stickydir
   ```
2. Set the sticky bit with execute (octal `1777`):
   ```bash theme={null}
   chmod 1777 stickydir
   ls -ld stickydir
   # drwxrwxr-t. 2 aaron aaron 6 Apr 26 05:14 stickydir
   ```
   * The lowercase `t` shows both execute and sticky bits are set.
3. Demonstrate sticky without execute (octal `1666`):
   ```bash theme={null}
   chmod 1666 stickydir
   ls -ld stickydir
   # drw-rw-rwT. 2 aaron aaron 6 Apr 26 05:14 stickydir
   ```
   * Uppercase `T` indicates sticky is set but execute is not.

***

## Links and References

* [Linux File Permissions](https://www.kernel.org[AWS_SECRET_ACCESS_KEY].html)
* [chmod Manual Page](https://man7.org/linux/man-pages/man1/chmod.1.html)
* [Understanding Linux File System Permissions](https://www.redhat.com/en/topics/linux/what-is-linux-file-permissions)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/cc1949d1-8171-4c8c-b69f-86f96cad0bbe/lesson/6c86d57f-0864-4e96-b7cf-4a0bad7fba25" />
</CardGroup>


# Search file using Grep

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/Essential-Commands/Search-file-using-Grep/page

This article explains how to use the `grep` command on Linux for searching text patterns in files and directories.

Searching for text patterns across files and directories is a common task on Linux systems. The `grep` command lets you quickly locate lines that match a specified string or regular expression.

## Table of Common Options

| Option | Description                               | Example                              |
| ------ | ----------------------------------------- | ------------------------------------ |
| -i     | Ignore case (case-insensitive search)     | `grep -i 'error' logfile.txt`        |
| -r     | Recursive search in all subdirectories    | `grep -r 'TODO' /home/user/projects` |
| -v     | Invert match (show non-matching lines)    | `grep -v 'DEBUG' app.log`            |
| -w     | Match whole words only                    | `grep -w 'user' /etc/passwd`         |
| -o     | Show only the part of a line that matches | `grep -o '[0-9]\+' data.txt`         |

***

## General Syntax

```bash theme={null}
grep [OPTIONS] PATTERN [FILE...]
```

* **PATTERN**\
  The text or [regular expression](https://www.gnu.org/software/grep/manual/grep.html#Regular-Expressions) to search for.
* **FILE**\
  One or more files or directories to scan. If no file is given, `grep` reads from standard input.

<Callout icon="lightbulb">
  Always quote patterns that contain spaces or shell metacharacters:

  ```bash theme={null}
  grep -i 'error message' /var/log/syslog
  ```
</Callout>

***

## 1. Basic, Case-Sensitive Search

By default, `grep` performs a case-sensitive search. To find lines containing **CentOS** in `/etc/os-release`:

```bash theme={null}
$ grep 'CentOS' /etc/os-release
NAME="CentOS Stream 8"
PRETTY_NAME="CentOS Stream 8"
REDHAT_SUPPORT_PRODUCT_VERSION="CentOS Stream"
```

***

## 2. Case-Insensitive Search

Use `-i` to ignore case differences. This matches “centos”, “CentOS”, or “CENTOS” alike:

```bash theme={null}
$ grep -i 'centos' /etc/os-release
NAME="CentOS Stream 8"
ID="centos"
PRETTY_NAME="CentOS Stream 8"
CPE_NAME="cpe:/o:centos:centos:8"
HOME_URL="https://centos.org/"
REDHAT_SUPPORT_PRODUCT_VERSION="CentOS Stream"
```

***

## 3. Recursive Search in Directories

To search through all files in a directory and its subdirectories, combine `-r` with your pattern:

```bash theme={null}
$ grep -r 'CentOS' /etc/
/etc/centos-release:CentOS Stream release 8
/etc/yum.repos.d/CentOS-Stream-AppStream.repo:# CentOS-Stream-AppStream.repo
```

Combine `-r` and `-i` for a recursive, case-insensitive search:

```bash theme={null}
$ grep -ir 'centos' /etc/
/etc/centos-release:CentOS Stream release 8
/etc/krb5.conf.d/kcm_default_ccache:# On Fedora/RHEL/CentOS, this is /etc/krb5.conf.d/
…
```

<Callout icon="triangle-alert">
  You may encounter “Permission denied” messages when scanning protected directories. Use `sudo` if you need elevated privileges:

  ```bash theme={null}
  sudo grep -ir 'centos' /etc/
  ```
</Callout>

***

## 4. Invert Match

Show only the lines that **do not** contain the pattern. Use the `-v` option:

```bash theme={null}
$ grep -vi 'centos' /etc/os-release
VERSION="8"
ID_LIKE="rhel fedora"
VERSION_ID="8"
PLATFORM_ID="platform:el8"
ANSI_COLOR="0;31"
BUG_REPORT_URL="https://bugzilla.redhat.com/"
REDHAT_SUPPORT_PRODUCT="Red Hat Enterprise Linux 8"
```

***

## 5. Match Whole Words Only

To avoid matching substrings (e.g., “redhat” when you want “red”), add the `-w` flag:

```bash theme={null}
$ echo -e "red Red redhat RED" | grep -iw 'red'
red
Red
RED
```

***

## 6. Show Only the Matched Text

By default, `grep` prints the entire line containing the match. Use `-o` to display only the portion that matches:

```bash theme={null}
$ grep -oi 'centos' /etc/os-release
CentOS
centos
CENTOS
centos
```

***

You’ve now covered the essentials of `grep` for searching text in files. In upcoming lessons, we will explore more advanced text-processing tools like `awk` and `sed`.

## Links and References

* [GNU grep Manual](https://www.gnu.org/software/grep/manual/grep.html)
* [Linux Command Line Basics](https://linuxcommand.org/)
* [Regular Expressions Overview](https://www.regular-expressions.info/)
* [Bash Guide for Beginners](https://tldp.org/LDP/Bash-Beginners-Guide/html/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/cc1949d1-8171-4c8c-b69f-86f96cad0bbe/lesson/f38bcd9a-c4e3-4161-87c6-a75e4117c3d7" />
</CardGroup>
