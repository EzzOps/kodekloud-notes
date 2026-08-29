# At least three zeros
$ egrep -r '0{3,}' /etc/

# One followed by up to three zeros (matches "1" as well)
$ egrep -r '10{,3}' /etc/

# Exactly three zeros
$ egrep -r '0{3}' /etc/
```

***

## `?` and `*` Quantifiers

* `x?` – *zero or one* `x`
* `x*` – *zero or more* `x`

To match both `disable` and `disabled`, make the final `d` optional:

```bash theme={null}
$ egrep -r 'disable(d)?' /etc/
```

***

## Character Classes and Ranges

Define a set or range of characters using square brackets:

* `[abc]` matches `a`, `b`, or `c`
* `[a-z]` matches any lowercase letter
* `[0-9]` matches any digit

<Frame>
  ![The image shows a dark-themed interface with a command line prompt and examples of character ranges or sets, such as \[a-z\] and \[0-9\]. The text "KodeKloud" is visible in the corner.](https://kodekloud.com/kk-media/image/upload/v1752881478/notes-assets/images/Linux-System-Administration-for-Beginners-Extended-Regular-Expressions/dark-theme-command-line-character-sets.jpg)
</Frame>

### Match `cat` or `cut`

```bash theme={null}
$ egrep -r 'c[au]t' /etc/
```

***

## Matching Device Files under `/dev`

A simple `'/dev/.*'` pattern is too greedy:

```bash theme={null}
$ egrep -r '/dev/.*' /etc/
```

To restrict matches to letters plus an optional digit:

```bash theme={null}
$ egrep -r '/dev/[a-z]+[0-9]?' /etc/
```

> **triangle-alert** If device names include uppercase letters or multiple segments (e.g., `/dev/tty0p0`), use grouping and repetition to cover all cases.

```bash theme={null}
$ egrep -r '/dev/([a-zA-Z]+[0-9]?)+'
```

***

## Sub-Expressions and Grouping

Parentheses `()` treat a group of tokens as a single unit. In arithmetic:

![The image shows a dark interface with a command line prompt on the left and a calculation on the right, demonstrating the expression "1+2\*3" which equals "7".](https://kodekloud.com/kk-media/image/upload/v1752881479/notes-assets/images/Linux-System-Administration-for-Beginners-Extended-Regular-Expressions/dark-interface-command-line-calculation.jpg)

* `1 + 2 * 3 = 1 + (2×3) = 7`
* `(1 + 2) * 3 = 3×3 = 9`

In regex:

```bash theme={null}
# Repeat a letter+digit group one or more times
$ egrep -r '/dev/([a-zA-Z]+[0-9]?)+'
```

***

## Alternation with `|`

Use `|` to match one pattern or another.

```bash theme={null}
# Match "enabled" or "disabled"
$ egrep -r 'enabled|disabled' /etc/

# Case-insensitive mix with optional "d"
$ egrep -ir 'enable(d)?|disable(d)?' /etc/
```

***

## Negated Character Classes

Prefix a class with `^` to invert it:

```bash theme={null}
# "http" not followed by "s"
$ egrep -r 'http[^s]' /etc/

# Slash not followed by a lowercase letter
$ egrep -r '/[^a-z]' /etc/
```

***

## Beyond grep: Other Regex Tools

Most Linux utilities support ERE or similar syntax:

| Tool         | Use Case                     |
| ------------ | ---------------------------- |
| `sed`        | Stream editing               |
| `awk`        | Field-based text processing  |
| Text editors | Interactive search & replace |

For interactive testing, try [Regexr](https://regexr.com).

## References

* [GNU grep Manual](https://www.gnu.org/software/grep/manual/)
* [Regular Expressions - MDN](https://developer.mozilla.org/docs/Web/JavaScript/Guide/Regular_Expressions)
* [Regexr Online Tester](https://regexr.com)

Happy pattern crafting!

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/cc1949d1-8171-4c8c-b69f-86f96cad0bbe/lesson/5805b6da-9cbc-49b5-b24b-4f2bcf80ac8d)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/cc1949d1-8171-4c8c-b69f-86f96cad0bbe/lesson/80dfb239-96f2-4fce-8a4b-3da0156e91c9)


# List set and change standard file permissions

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/Essential-Commands/List-set-and-change-standard-file-permissions/page

Learn to manage file permissions in Linux by viewing, changing ownership, and modifying permissions using symbolic and octal notation.

Managing file permissions is a core skill for any Linux administrator or user. In this guide, you’ll learn how to view ownership, adjust user and group assignments, interpret permission bits, and modify permissions using both symbolic and octal notation.

## Table of Contents

1. [Understanding Ownership](#understanding-ownership)
2. [Viewing Owner, Group, and Permissions](#viewing-owner-group-and-permissions)
3. [Changing Owner and Group](#changing-owner-and-group)
4. [File Types and Permission Bits](#file-types-and-permission-bits)
5. [Permission Evaluation Order](#permission-evaluation-order)
6. [Modifying Permissions with chmod](#modifying-permissions-with-chmod)
   * [Adding Permissions](#adding-permissions)
   * [Removing Permissions](#removing-permissions)
   * [Setting Exact Permissions](#setting-exact-permissions)
   * [Combining Multiple Changes](#combining-multiple-changes)
7. [Using Octal Notation with chmod](#using-octal-notation-with-chmod)
8. [Resources & References](#resources--references)

***

## Understanding Ownership

Every file or directory on Linux has:

* **User owner** (UID)
* **Group owner** (GID)

Only the file’s owner or `root` can change its permissions or ownership.

***

## Viewing Owner, Group, and Permissions

Run `ls -l` to display permissions, owner, group, size, and timestamp:

```bash theme={null}
$ ls -l
-rw-r----- 1 aaron family 49 Oct 27 14:41 family_dog.jpg
```

* `-rw-r-----`: File type and permission bits
* `aaron`   : User owner
* `family`   : Group owner

***

## Changing Owner and Group

### Change Group: `chgrp`

```bash theme={null}
$ chgrp wheel family_dog.jpg
```

Example:

```bash theme={null}
$ ls -l
-rw-r----- 1 aaron family 49 Oct 27 14:41 family_dog.jpg

$ chgrp wheel family_dog.jpg

$ ls -l
-rw-r----- 1 aaron wheel 49 Oct 27 14:41 family_dog.jpg
```

> **lightbulb** You can only switch to groups you belong to. Use `groups` to list them:

  ```bash theme={null}
  $ groups
  aaron wheel family
  ```

### Change Owner: `chown`

Only `root` (or via `sudo`) can change the user owner:

```bash theme={null}
$ sudo chown jane family_dog.jpg
```

Example:

```bash theme={null}
$ ls -l
-rw-r----- 1 aaron wheel 49 Oct 27 14:41 family_dog.jpg

$ sudo chown jane family_dog.jpg

$ ls -l
-rw-r----- 1 jane wheel 49 Oct 27 14:41 family_dog.jpg
```

You can change both user and group:

```bash theme={null}
$ sudo chown aaron:family family_dog.jpg

$ ls -l
-rw-r----- 1 aaron family 49 Oct 27 14:41 family_dog.jpg
```

***

## File Types and Permission Bits

The first character in `ls -l` indicates the file type:

| Symbol | Type          |
| ------ | ------------- |
| `-`    | Regular file  |
| `d`    | Directory     |
| `l`    | Symbolic link |

Permission bits follow in three sets (owner, group, others):

| Bit | Value | Meaning                |
| --- | ----- | ---------------------- |
| r   | 4     | Read                   |
| w   | 2     | Write                  |
| x   | 1     | Execute (or enter dir) |

> \[!note]
> For directories:
>
> * `r`: list contents
> * `w`: create/delete files
> * `x`: change into the directory

![The image illustrates file and directory permissions in a Unix-like system, showing "rwx" for owner, group, and others, with a key explaining the meaning of each permission bit.](https://kodekloud.com/kk-media/image/upload/v1752881480/notes-assets/images/Linux-System-Administration-for-Beginners-List-set-and-change-standard-file-permissions/unix-file-directory-permissions-diagram.jpg)

***

## Permission Evaluation Order

Linux checks permissions in this order:

1. Owner
2. Group
3. Others

Consider a file owned by `aaron:family` with permissions `-r--rw----`:

```bash theme={null}
$ ls -l
-r--rw---- 1 aaron family 49 Oct 27 14:41 family_dog.jpg
```

* As **aaron**: owner bits (`r--`) apply → no write
  ```bash theme={null}
  $ echo "Update" >> family_dog.jpg
  bash: family_dog.jpg: Permission denied
  ```
* As **jane** (in `family`): owner bits skipped, group bits (`rw-`) apply → can write
  ```bash theme={null}
  $ su jane
  $ echo "Add this content" >> family_dog.jpg
  $ cat family_dog.jpg
  Picture of Milo the dog
  ```
* Else: “others” bits determine access.

***

## Modifying Permissions with chmod

General syntax:

```bash theme={null}
chmod [who][+|-|=][perms] file
```

* **who**: `u` (owner), `g` (group), `o` (others), `a` (all)
* **+**: add permissions
* **-**: remove permissions
* **=**: set exact permissions

### Adding Permissions

Grant write to owner:

```bash theme={null}
$ ls -l
-r--rw---- 1 aaron family 49 Oct 27 14:41 family_dog.jpg

$ chmod u+w family_dog.jpg

$ ls -l
-rw-rw---- 1 aaron family 49 Oct 27 14:41 family_dog.jpg
```

### Removing Permissions

Use `-` to revoke bits. Common patterns:

> **lightbulb** * `u-w`: remove owner write
  * `g-rw`: remove group read/write
  * `o-rwx`: remove all for others

![The image shows a terminal interface with instructions on removing permissions for users, groups, and others, using options like "u-", "g-", and "o-". Examples include "u-w", "g-rw", and "o-rwx".](https://kodekloud.com/kk-media/image/upload/v1752881481/notes-assets/images/Linux-System-Administration-for-Beginners-List-set-and-change-standard-file-permissions/terminal-permissions-removal-instructions.jpg)

Remove read for others:

```bash theme={null}
$ ls -l
-r--rw-r-- 1 aaron family 49 Oct 27 14:41 family_dog.jpg

$ chmod o-r family_dog.jpg

$ ls -l
-r--rw---- 1 aaron family 49 Oct 27 14:41 family_dog.jpg
```

### Setting Exact Permissions

Overwrite existing bits with `=`:

```bash theme={null}
$ ls -l
-rw-rw---- 1 aaron family 49 Oct 27 14:41 family_dog.jpg

$ chmod g=r family_dog.jpg
$ ls -l
-rw-r----- 1 aaron family 49 Oct 27 14:41 family_dog.jpg

$ chmod g=rw family_dog.jpg
$ ls -l
-rw-rw---- 1 aaron family 49 Oct 27 14:41 family_dog.jpg

$ chmod g= family_dog.jpg
$ ls -l
-rw------- 1 aaron family 49 Oct 27 14:41 family_dog.jpg

$ chmod g=rwx family_dog.jpg
$ ls -l
-rw-rwx--- 1 aaron family 49 Oct 27 14:41 family_dog.jpg
```

### Combining Multiple Changes

Separate specs with commas:

```bash theme={null}
$ ls -l
-rw-rwxr-x 1 aaron family 49 Oct 27 14:41 family_dog.jpg
