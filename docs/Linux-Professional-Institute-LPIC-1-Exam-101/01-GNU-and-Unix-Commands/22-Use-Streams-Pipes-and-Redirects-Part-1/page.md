# Search recursively for one or more zeros in /etc
grep -Er '0+' /etc/
/usr/share/example.conf: option0
# Or equivalently:
egrep -r '0+' /etc/
```

Sample output:

```text theme={null}
/etc/pm2ppa.conf:#colorshear        0
/etc/pm2ppa.conf:#blackshear        0
/etc/pm2ppa.conf:#GammaR 1.0           # red enhancement
…
/etc/subuid--charles:23172:65536
```

## Quantifier Cheat Sheet

| Quantifier | Description                 | Example                               |
| ---------- | --------------------------- | ------------------------------------- |
| `?`        | 0 or 1 occurrence           | `colou?r` matches `color` or `colour` |
| `*`        | 0 or more occurrences       | `a*b` matches `b`, `ab`, `aaab`       |
| `+`        | 1 or more occurrences       | `0+` matches `0`, `00`, `000`         |
| `{n}`      | Exactly n times             | `A{3}` matches `AAA`                  |
| `{m,}`     | At least m times            | `0{3,}` matches `000` or more         |
| `{,n}`     | Up to n times (including 0) | `1{,3}` matches `1`, `11`, `111`      |
| `{m,n}`    | Between m and n times       | `a{2,4}` matches `aa`, `aaa`, `aaaa`  |

## Optional Elements with `?`

Make the preceding atom optional:

```bash theme={null}
# Match "disable" or "disabled"
egrep -r 'disabled?' /etc/
```

> **lightbulb** Because grep matches substrings by default, `disabled?` also finds `disables` unless you anchor (`^`, `$`) or use word boundaries (`\b`).

## Zero or More with `*`

`*` allows the element to repeat any number of times:

```bash theme={null}
# Matches "/dev/" plus any characters
egrep -r '/dev/.*' /etc/
```

> **triangle-alert** Unbounded `.*` is greedy and may overmatch. Constrain it with character classes or quantifiers whenever possible.

## Alternation with `|`

Select between multiple patterns:

```bash theme={null}
# Find "enabled" or "disabled"
egrep -r 'enabled|disabled' /etc/
```

Combine with `?` to catch both forms:

```bash theme={null}
egrep -ri 'enabled?|disabled?' /etc/
```

## Character Classes and Ranges

Define sets of allowed characters with `[]`. Hyphens indicate ranges:

```bash theme={null}
# Match "cat" or "cut"
egrep -r 'c[au]t' /etc/

# Any lowercase letter
egrep -r '[a-z]' /etc/

# Any digit
egrep -r '[0-9]' /etc/

# Specific characters
egrep -r '[ABZ954]' /etc/
```

## Building up a Device-Name Pattern

To match Linux device nodes under `/dev` while avoiding overmatching:

1. Letters only:
   ```bash theme={null}
   egrep -r '/dev/[a-z]*' /etc/
   ```
2. Append exactly one digit:
   ```bash theme={null}
   egrep -r '/dev/[a-z]*[0-9]' /etc/
   ```
3. Make the digit optional:
   ```bash theme={null}
   egrep -r '/dev/[a-z]*[0-9]?' /etc/
   ```
4. Repeat letter+digit segments (e.g., `tty0p0`):
   ```bash theme={null}
   egrep -r '/dev/([a-z]*[0-9]?)+' /etc/
   ```
5. Allow uppercase letters too:
   ```bash theme={null}
   egrep -r '/dev/(([a-z]|[A-Z])*[0-9]?)+' /etc/
   ```

Each refinement better aligns with real devices like `/dev/sda`, `/dev/ttyS0`, and `/dev/tty0p0`.

## Sub-Expressions (Grouping)

Group subpatterns with parentheses so quantifiers apply to the entire unit:

![The image shows a dark-themed interface with a command line on the left and a mathematical expression evaluation on the right, demonstrating the use of subexpressions with parentheses.](https://kodekloud.com/kk-media/image/upload/v1752881409/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Search-Text-Files-Using-Regular-Expressions-Part-1-Understand-the-differences-between-basic-and-extended-regular-expressions/dark-interface-command-line-math-evaluation.jpg)

```bash theme={null}
egrep -r '/dev/([a-z]*[0-9]?)+ ' /etc/
```

## Negated Character Classes

Start a class with `^` to invert it:

```bash theme={null}
# "http" not followed by "s"
egrep -r 'http[^s]' /etc/

# Slash not followed by a lowercase letter
egrep -r '/[^a-z]' /etc/
```

## Conclusion & Further Reading

Mastering EREs in `grep`, `egrep`, `sed`, and related tools empowers you to craft precise searches and avoid false positives. Practice your patterns interactively:

* [GNU grep Manual](https://www.gnu.org/software/grep/manual/)
* [Regexr – Online Regex Tester](https://regexr.com/)
* [POSIX Regular Expressions](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap09.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/2490f961-886c-4531-be8c-915cccff60a9/lesson/ce40bbd2-29eb-44ef-9c97-f378e9d0d4d8)


# Use Streams Pipes and Redirects Part 1

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/GNU-and-Unix-Commands/Use-Streams-Pipes-and-Redirects-Part-1/page

Learn to redirect input and output in Linux to enhance command-line workflows.

In this lesson, you’ll master how to redirect input and output in Linux, making your command-line workflows more powerful and flexible.

## Table of Contents

1. [Standard Streams Overview](#standard-streams-overview)
2. [Redirecting Output](#redirecting-output-)
3. [Appending Output](#appending-output)
4. [Discarding Output](#discarding-output-)
5. [Merging and Redirecting Both Streams](#merging-and-redirecting-both-streams)
6. [Redirecting Input](#redirecting-input-)
7. [Here Documents and Here Strings](#here-documents-and-here-strings)
8. [Pipes and Pipelines](#pipes-and-pipelines)
9. [Quick Reference](#quick-reference)
10. [Links and References](#links-and-references)

***

## Standard Streams Overview

Linux programs communicate using three standard streams:

| Descriptor | Stream Name              | Purpose                                |
| ---------- | ------------------------ | -------------------------------------- |
| 0          | stdin (standard input)   | Receives data (keyboard, files)        |
| 1          | stdout (standard output) | Sends regular output (terminal, files) |
| 2          | stderr (standard error)  | Sends error messages (terminal, files) |

![The image is a diagram illustrating the flow of standard input, output, and error in a command-line environment, showing how data from "file.txt" is processed by the "sort" command, with output directed to a terminal and errors to "errors.txt".](https://kodekloud.com/kk-media/image/upload/v1752881410/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Use-Streams-Pipes-and-Redirects-Part-1/command-line-input-output-diagram.jpg)

By default, both `stdout` and `stderr` appear on your terminal. You can redirect them separately:

```bash theme={null}
$ command 1>output.txt 2>errors.txt
```

## Redirecting Output (`>`)

To save a command’s output to a file (creating or overwriting it), use the `>` operator.

1. Create a file with unsorted numbers:

   ```bash theme={null}
   $ cat file.txt
   6
   5
   1
   3
   4
   2
   ```

2. Sort the file and write the result to `sortedfile.txt`:

   ```bash theme={null}
   $ sort file.txt > sortedfile.txt
   $ cat sortedfile.txt
   1
   2
   3
   4
   5
   6
   ```

> **triangle-alert** Using `>` always overwrites the target file. You will lose previous contents!

## Appending Output (`>>`)

To add output to the end of an existing file without erasing its contents, use `>>`:

```bash theme={null}
$ echo "First line"  >> file.txt
$ echo "Second line" >> file.txt
$ echo "Third line"  >> file.txt
$ cat file.txt
First line
Second line
Third line
```

## Discarding Output (`/dev/null`)

Send unwanted output or errors to `/dev/null`, the “black hole”:

```bash theme={null}
$ grep -r '^The' /etc/ 2>/dev/null
```

This filters matching lines while discarding all error messages.

## Merging and Redirecting Both Streams

* Redirect `stdout` and `stderr` to separate files:

  ```bash theme={null}
  $ grep -r '^The' /etc/ 1>output.txt 2>errors.txt
  ```

* Append both streams:

  ```bash theme={null}
  $ grep -r '^The' /etc/ 1>>output.txt 2>>errors.txt
  ```

* Merge `stderr` into `stdout` and write to one file:

  ```bash theme={null}
  $ grep -r '^The' /etc/ > all_output.txt 2>&1
  ```

> **lightbulb** Order matters: `> all_output.txt 2>&1` merges error output into the same file, while reversing redirects leaves errors on the console.

## Redirecting Input (`<`)

Some commands read from `stdin` instead of a file argument. Redirect a file into `stdin` like this:

```bash theme={null}
$ sendemail someone@example.com < email_content.txt
```

The contents of `email_content.txt` feed directly into `sendemail`.

## Here Documents and Here Strings

### Here Documents (`<<`)

Embed a block of text as input:

```bash theme={null}
$ sort <<EOF
6
3
2
5
1
4
EOF
1
2
3
4
5
6
```

`EOF` (or any marker you choose) encloses the input region.

### Here Strings (`<<<`)

For single-line input, here strings are concise:

```bash theme={null}
$ bc <<< "1+2+3+4"
10
```

## Pipes and Pipelines (`|`)

Pipelines let you chain commands by feeding one’s `stdout` into the next’s `stdin`. Example: filter, sort, and align columns from `/etc/login.defs`:

```bash theme={null}
$ grep -v '^#' /etc/login.defs \
| sort \
| column -t
```

Steps:

1. `grep -v '^#'` removes comments
2. `sort` orders lines
3. `column -t` aligns columns into a neat table

Example output:

```text theme={null}
CREATE_HOME         yes
ENCRYPT_METHOD      SHA512
GID_MAX             60000
GID_MIN             1000
HOME_MODE           0700
MAIL_DIR            /var/spool/mail
PASS_MAX_DAYS       99999
PASS_MIN_DAYS       0
PASS_MIN_LEN        5
PASS_WARN_AGE       7
SYS_GID_MAX         999
SYS_GID_MIN         201
SYS_UID_MAX         999
SYS_UID_MIN         201
UID_MAX             60000
UID_MIN             1000
UMASK               022
USERGROUPS_ENAB     yes
```

## Quick Reference

| Operator    | Description                     | Example                                                |         |             |
| ----------- | ------------------------------- | ------------------------------------------------------ | ------- | ----------- |
| `>`         | Redirect stdout, overwrite file | `sort file.txt > sortedfile.txt`                       |         |             |
| `>>`        | Redirect stdout, append to file | `echo hi >> greetings.txt`                             |         |             |
| `<`         | Redirect stdin from file        | `wc -l < file.txt`                                     |         |             |
| `2>`        | Redirect stderr, overwrite file | `grep foo bar 2>errors.log`                            |         |             |
| `/dev/null` | Discard stream                  | `cmd 2>/dev/null`                                      |         |             |
| `&>`        | Redirect both stdout and stderr | `cmd &> combined.log`                                  |         |             |
| \`          | \`                              | Pipe stdout into next stdin                            | \`ls -l | grep '^d'\` |
| `<<EOF`     | Here document (multiline input) | See [Here Documents](#here-documents-and-here-strings) |         |             |
| `<<<`       | Here string (single-line input) | `bc <<< "2+2"`                                         |         |             |

## Links and References

* [Bash Guide](https://www.gnu.org/software/bash/manual/bash.html)
* [Linux I/O Redirection](https://tldp.org/LDP/abs/html/io-redirection.html)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Terraform Registry](https://registry.terraform.io/)
* [Docker Hub](https://hub.docker.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/2490f961-886c-4531-be8c-915cccff60a9/lesson/ddde1c84-71a5-4d55-a5fe-a8d7f319a260)
