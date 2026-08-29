# Search by name under /usr/share for JPEG files
find /usr/share/ -name '*.jpg'

# Find files larger than 10 MB in /lib64
find /lib64/ -size +10M

# List files modified in the last minute under /dev
find /dev/ -mmin -1
```

## Specifying the Search Path First

Always place the directory to search **before** your search criteria.

Incorrect (no results under `/bin`):

```bash theme={null}
find -name file1.txt /bin
```

Correct:

```bash theme={null}
find /bin/ -name file1.txt
find -name file1.txt    # searches the current directory
```

## Name-Based Searches

* `-name`  : case-sensitive filename match
* `-iname` : case-insensitive filename match
* Wildcards (`*`) match any sequence of characters

```bash theme={null}
find -name felix
find -iname FELIX
find -name "f*"          # all files starting with 'f'
```

## Time-Based Searches

You can filter files based on modification or change times.

### Modified Time by Minutes (`-mmin`)

| Syntax | Description                 |
| ------ | --------------------------- |
| `n`    | exactly *n* minutes ago     |
| `-n`   | within the last *n* minutes |
| `+n`   | more than *n* minutes ago   |

```bash theme={null}
find -mmin 5    # exactly 5 minutes ago
find -mmin -5   # in the last 5 minutes
find -mmin +5   # more than 5 minutes ago
```

### Modified Time by Days (`-mtime`)

* `0`  : within the last 24 hours
* `1`  : between 24 and 48 hours ago
* `+n` : more than *n* days ago
* `-n` : less than *n* days ago

```bash theme={null}
find -mtime 0    # modified within the last day
find -mtime 1    # modified one to two days ago
```

### Change Time (`-ctime`)

Tracks **metadata** changes (permissions, ownership):

```bash theme={null}
find -ctime 1    # metadata changed one to two days ago
```

## Size-Based Searches

Filter files by size using the following suffixes:

| Suffix | Unit      |
| ------ | --------- |
| `c`    | bytes     |
| `k`    | kilobytes |
| `M`    | megabytes |
| `G`    | gigabytes |

| Syntax | Description         |
| ------ | ------------------- |
| `n`    | exactly *n* units   |
| `-n`   | less than *n* units |
| `+n`   | more than *n* units |

```bash theme={null}
find -size 512k    # exactly 512 KB
find -size -512k   # less than 512 KB
find -size +512k   # more than 512 KB
```

## Combining Expressions

By default, multiple expressions are combined with **AND**:

```bash theme={null}
# Files starting with 'f' AND exactly 512 KB in size
find -name "f*" -size 512k
```

### OR Operator

Use `-o` to OR expressions:

```bash theme={null}
# Files that start with 'f' OR are 512 KB in size
find -name "f*" -o -size 512k
```

### NOT Operator

Negate conditions with `-not` or an escaped `!`:

```bash theme={null}
# Exclude files starting with 'f'
find -not -name "f*"

# Equivalent using escaped '!'
find \! -name "f*"
```

## Permission-Based Searches

Search by file permission bits (octal notation):

| Mode Format | Description                 |
| ----------- | --------------------------- |
| `mode`      | exact match                 |
| `-mode`     | at least the bits in `mode` |
| `/mode`     | any of the bits in `mode`   |

Examples (mode `664` = `rw-rw-r--`):

```bash theme={null}
find -perm 664       # exactly 664
find -perm -664      # at least these bits
find -perm /664      # any of these bits
```

More permission filters:

```bash theme={null}
find -perm 600       # owner read/write only
find -perm -100      # owner has execute
find \! -perm -o=r   # not readable by others
find -perm /u=r,g=r,o=r  # readable by user OR group OR others
```

> **triangle-alert** Be careful to quote wildcard patterns (e.g., `"*.txt"`), especially when running in scripts or complex shells.

***

## Further Reading & References

* [GNU Findutils Manual](https://www.gnu.org/software/findutils/manual/find.html)
* [Linux `find` Command on tldr.sh](https://tldr.sh/)
* [Advanced `find` Examples](https://www.baeldung.com/linux/find-command)

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/cc1949d1-8171-4c8c-b69f-86f96cad0bbe/lesson/ed5aa87a-c660-4fd4-87f8-e5e4bc23327d)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/cc1949d1-8171-4c8c-b69f-86f96cad0bbe/lesson/6da024e0-2e3c-4504-beac-38ebf4e76563)


# Use input output redirection

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/Essential-Commands/Use-input-output-redirection/page

Guide to redirecting stdin, stdout, and stderr in Unix shells, covering redirection operators, pipes, here-documents, suppression, and common patterns for command-line workflows.

We'll cover how to redirect input and output in Linux — a foundational skill for shell scripting, automation, and command-line workflows.

<Frame>
  <img alt="A dark-themed presentation slide with the title &#x22;Redirecting Input and Output&#x22; on the left and a large empty rounded rectangle area on the right. The KodeKloud logo appears in the top-right corner." />
</Frame>

Why this matters: most Unix utilities read from stdin (standard input) and write to stdout (standard output). Redirecting these streams — and stderr (standard error) — lets you capture program output, suppress errors, chain commands, and feed files into programs that expect interactive input.

## Basic example (sort)

Many commands accept a filename argument, but they also work with stdin/stdout. For example, sort reads text and prints sorted lines:

```bash theme={null}
$ cat file.txt
6
5
1
3
4
2

$ sort file.txt
1
2
3
4
5
6
