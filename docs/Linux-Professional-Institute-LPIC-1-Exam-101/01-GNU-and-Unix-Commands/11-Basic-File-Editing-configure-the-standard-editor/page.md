# Syntax: chgrp <group_name> <file_or_directory>
$ chgrp wheel family_dog.jpg
$ ls -l
-rw-r----- 1 aaron wheel 49 Oct 27 14:41 family_dog.jpg
```

Check your group memberships with:

```bash theme={null}
$ groups
aaron wheel family
```

> **lightbulb** You can only switch a file’s group to one you’re already a member of.

## Changing File Owner with chown

Only `root` can change file owners. Prefix with `sudo` if necessary:

```bash theme={null}
# Syntax: sudo chown <user>[:<group>] <file_or_directory>
$ sudo chown jane family_dog.jpg
$ ls -l
-rw-r----- 1 jane wheel 49 Oct 27 14:41 family_dog.jpg

# Change both owner and group in one go:
$ sudo chown aaron:family family_dog.jpg
$ ls -l
-rw-r----- 1 aaron family 49 Oct 27 14:41 family_dog.jpg
```

## Understanding Permission Bits

The permissions string (`-rwxrwxrwx`) breaks down as:

* First character: file type
  * `-` = regular file
  * `d` = directory
  * `l` = symbolic link
* Next nine: three triplets for **owner**, **group**, and **others**, each with `r` (read), `w` (write), and `x` (execute).

![The image illustrates file and directory permissions in a Unix-like system, showing the permission string "rwxrwxrwx" for owner, group, and others, along with a key explaining the meaning of each permission bit.](https://kodekloud.com/kk-media/image/upload/v1752881384/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Manage-File-Permissions-and-Ownership/unix-file-directory-permissions-diagram.jpg)

### Permission Effects

* **Files**
  * `r`: view contents
  * `w`: modify contents
  * `x`: execute (scripts or binaries)
* **Directories**
  * `r`: list entries (`ls`)
  * `w`: create/delete entries
  * `x`: enter directory (`cd`)

## Modifying Permissions with chmod

Use the symbolic syntax:

```bash theme={null}
chmod [ugoa][+-=][rwx] <file_or_directory>
```

| Reference | Meaning               |
| --------- | --------------------- |
| u         | owner (user)          |
| g         | group                 |
| o         | others                |
| a         | all (u, g, o)         |
| +         | add permissions       |
| -         | remove permissions    |
| =         | set exact permissions |

### Adding Permissions

Allow the owner to write:

```bash theme={null}
$ ls -l
-r--r----- 1 aaron family 49 Oct 27 14:41 family_dog.jpg

$ chmod u+w family_dog.jpg
$ ls -l
-rw-r----- 1 aaron family 49 Oct 27 14:41 family_dog.jpg
```

### Removing Permissions

Remove the read bit for others:

```bash theme={null}
$ chmod o-r family_dog.jpg
$ ls -l
-rw-r----- 1 aaron family 49 Oct 27 14:41 family_dog.jpg
```

![The image shows a guide on removing permissions in a command-line interface, with examples for users, groups, and others. It includes options like u-, g-, and o- with examples such as u-w, g-rw, and o-rwx.](https://kodekloud.com/kk-media/image/upload/v1752881385/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Manage-File-Permissions-and-Ownership/remove-permissions-command-line-guide.jpg)

### Setting Exact Permissions

Grant group read-only:

```bash theme={null}
$ chmod g=r family_dog.jpg
$ ls -l
-rw-r----- 1 aaron family 49 Oct 27 14:41 family_dog.jpg

$ chmod g=rw family_dog.jpg
$ ls -l
-rw-rw---- 1 aaron family 49 Oct 27 14:41 family_dog.jpg
```

### Combining References

You can comma-separate multiple adjustments:

```bash theme={null}
$ ls -l
-rw-r--r-- 1 appuser appuser 49 Oct 27 14:41 family.jpg

# Owner read/write, group read, others none
$ chmod u=rw,g=r,o= family.jpg
$ ls -l
-rw-r----- 1 appuser appuser 49 Oct 27 14:41 family.jpg

# Mix add/remove in one command
$ chmod u+rw,g-w family_dog.jpg
```

## Numeric (Octal) Notation

To inspect the octal value, use `stat`:

```bash theme={null}
$ stat family_dog.jpg
  Access: (0640/-rw-r-----)  Uid: ( 1000/aaron)   Gid: (   10/family)
```

Here **owner** has `rw-` (6), **group** has `r--` (4), **others** have `---` (0) → mode `640`.

![The image illustrates octal file permissions, showing the conversion between symbolic, binary, and decimal representations. It includes examples of permissions like "rw-r--r--" and "rwxr-xr-x" with their corresponding binary and decimal values.](https://kodekloud.com/kk-media/image/upload/v1752881386/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Manage-File-Permissions-and-Ownership/octal-file-permissions-symbolic-binary.jpg)

Alternatively, assign values: `r=4`, `w=2`, `x=1`:

* `rwx` = 4+2+1 = 7
* `r-x` = 4+0+1 = 5
* `r--` = 4+0+0 = 4

![The image explains octal permissions in a Unix-like system, showing how the permissions "rw-r-----" translate to the octal value "640". It also provides a key for permission values: read (r) is 4, write (w) is 2, and execute (x) is 1.](https://kodekloud.com/kk-media/image/upload/v1752881386/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Manage-File-Permissions-and-Ownership/octal-permissions-unix-diagram-640.jpg)

### Setting Numeric Permissions

```bash theme={null}
$ chmod 755 family_dog.jpg  # rwxr-xr-x
$ chmod 640 family_dog.jpg  # rw-r-----
```

## Further Reading

* [Linux File Permissions – Official Documentation](https://www.kernel.org/doc/html/latest/filesystems/permissions.html)
* [chmod Command Tutorial](https://linux.die.net/man/1/chmod)
* [chown and chgrp Usage](https://linux.die.net/man/1/chown)

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/de71b96a-9dc0-4e92-987a-6c7055c44e8b/lesson/f4992ea9-7155-41cd-a174-9fbebcdc4ccf)


# Basic File Editing configure the standard editor

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/GNU-and-Unix-Commands/Basic-File-Editing-configure-the-standard-editor/page

This article explains how to configure your shell's default text editor for improved efficiency when editing files.

Changing the shell’s default text editor lets you work faster when editing files like your crontab. By default, most UNIX-like systems use `vi` or `vim`. Bash determines which editor to launch by checking two environment variables:

| Variable | Purpose                       | Examples       |
| -------- | ----------------------------- | -------------- |
| VISUAL   | Full-screen, visual editors   | `vim`, `emacs` |
| EDITOR   | Simple, line-oriented editors | `nano`, `ed`   |

> **lightbulb** If both `VISUAL` and `EDITOR` are set, many programs will prefer `VISUAL`. To ensure consistency, consider exporting both variables.

## 1. Setting the Editor for the Current Session

To switch to `nano` for just the active shell session, export the `EDITOR` variable:

```bash theme={null}
export EDITOR=nano
```

After running this, any program in this session that relies on your default editor will open `nano` instead of `vi`.

> **triangle-alert** This change only applies to the current session. Close the terminal or start a new shell, and you’ll revert to the previous default.

## 2. Making the Change Permanent

To have `nano` (or another editor) as your default every time you open a new shell, add the export line to your Bash startup file. Most users place it in `~/.bash_profile`:

```bash theme={null}
vi ~/.bash_profile
```

Inside the file, append:

```bash theme={null}
export EDITOR=nano
```

Save and exit. From now on, all new Bash sessions for that user will launch `nano` as the standard editor.

## Links and References

* [GNU Bash Manual: Invoking Bash](https://www.gnu.org/software/bash/manual/html_node/Invoking-Bash.html)
* [Environment Variables in Linux](https://www.gnu.org/software/sh-utils/manual/html_node/Environmental-Variables.html)
* [Nano Editor Documentation](https://www.nano-editor.org/docs.php)

> **lightbulb** Check your understanding with the quiz.

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/2490f961-886c-4531-be8c-915cccff60a9/lesson/c52d877a-3522-4ac9-b7ee-0a6df6f95ae3)
