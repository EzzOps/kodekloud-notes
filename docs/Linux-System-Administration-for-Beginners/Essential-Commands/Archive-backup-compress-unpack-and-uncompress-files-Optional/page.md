# 022 is the default value, but 027, or even 077, could be considered
HOME_MODE         0700
PASS_WARN_AGE     7
```

To list only those ending in `7`:

```bash theme={null}
$ grep '7$' /etc/login.defs
PASS_WARN_AGE     7
```

And lines ending with `mail`:

```bash theme={null}
$ grep 'mail$' /etc/login.defs
MAIL_DIR          /var/spool/mail
#MAIL_FILE        .mail
```

## The Dot (.) – Match Any Single Character

A dot (`.`) matches exactly one character. For example, `c.t` will match `cat`, `cut`, `c1t`, and even parts of longer strings:

```bash theme={null}
$ grep -r 'c.t' /etc/
/etc/man_db.conf:# manpath. If no catpath string is used, the catpath will default to the
/etc/man_db.conf:# the database cache for any manpaths not mentioned below unless explicitly
...
```

To restrict matches to whole words, use the `-w` option:

```bash theme={null}
$ grep -wr 'c.t' /etc/
/etc/brltty/Input/mn/all.txt:Left: append to existing cut buffer from selected character
...
```

## Escaping Special Characters

To match a literal dot instead of using `.` as a wildcard, escape it with a backslash:

```bash theme={null}
$ grep '\.' /etc/login.defs
HOME_MODE         0700
PASS_WARN_AGE     7
```

## The Asterisk (\*) – Zero or More Occurrences

The asterisk (`*`) applies to the preceding element, allowing zero or more matches. For instance, `let*` matches `le`, `let`, `lett`, `letttt`, etc.:

```bash theme={null}
$ grep -r 'let*' /etc/
/etc/pm2ppa.conf:# configuration  file (/etc/pm2ppa.conf), and not from configuration files
/etc/pm2ppa.conf:#leftmargin  10
...
```

To match any path segment between slashes:

```bash theme={null}
$ grep -r '/.*/' /etc/
/etc/man_db.conf:# before /usr/man.
/etc/man_db.conf:MANDB_MAP              /usr/man
...
```

## The Plus (+) – One or More Occurrences

The plus operator requires at least one occurrence of the preceding element.

<Callout icon="lightbulb">
  Use `\+` in basic `grep` to enable the plus operator, or switch to extended regex with `grep -E`.
</Callout>

```bash theme={null}
$ grep -r '0\+' /etc/
/etc/pnm2ppa.conf:#colorshear      0
/etc/pnm2ppa.conf:#blackshear      0
...
```

If you omit the backslash (e.g., `grep -r '0+' /etc/`), `+` is treated literally, not as a quantifier.

## Extended Regular Expressions

To avoid escaping metacharacters like `+`, use extended regex with `grep -E` or `egrep`:

```bash theme={null}
$ grep -Er '0+' /etc/
```

With this foundation, you can harness regex patterns in Linux to perform precise text analysis and filtering.

## References

* [GNU grep Manual](https://www.gnu.org/software/grep/manual/grep.html)
* [Regular Expressions Tutorial](https://www.regular-expressions.info/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/cc1949d1-8171-4c8c-b69f-86f96cad0bbe/lesson/73d4bc39-7b48-48ad-b06f-146366279c6c" />
</CardGroup>


# Archive backup compress unpack and uncompress files Optional

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/Essential-Commands/Archive-backup-compress-unpack-and-uncompress-files-Optional/page

This lesson covers archiving, compressing, and preparing files for remote backups in Linux using tar.

In this lesson, we’ll cover how to archive files in Linux using `tar`, compress those archives, and prepare them for remote backups. This workflow is essential for system administrators and DevOps engineers who need reliable, space-efficient backups.

Typical backup workflow:

1. **Archive**: Pack multiple files and directories into one file (e.g., `backup.tar`).
2. **Compress**: Shrink the archive size (e.g., `backup.tar.gz`).
3. **Transfer**: Copy the compressed archive to a remote server, shared drive, or cloud storage.

<Frame>
  ![The image illustrates a process for archiving, compressing, and backing up files, showing steps from creating a "backup.tar" archive to compressing it into "backup.tar.gz" and then backing it up.](https://kodekloud.com/kk-media/image/upload/v1752881465/notes-assets/images/Linux-System-Administration-for-Beginners-Archive-backup-compress-unpack-and-uncompress-files-Optional/file-archiving-compressing-backing-up.jpg)
</Frame>

We’ll focus first on archiving with **tar**, then move on to compression and remote backups.

## Why Use tar?

Tar (tape archive) was originally designed for magnetic tapes but remains the de facto tool for:

* Bundling multiple files or directories into a single tarball (`.tar`).
* Preserving file metadata: permissions, timestamps, and ownership.

## Common tar Commands at a Glance

| Action    | Long Option | Short Option | Example                       |
| --------- | ----------- | ------------ | ----------------------------- |
| List      | --list      | -t           | `tar -tf archive.tar`         |
| Create    | --create    | -c           | `tar -cf archive.tar file1`   |
| Append    | --append    | -r           | `tar -rf archive.tar file2`   |
| Extract   | --extract   | -x           | `tar -xf archive.tar`         |
| Directory | --directory | -C           | `tar -xf archive.tar -C /tmp` |

## Listing Contents of an Existing Archive

To preview what’s inside `archive.tar`:

```bash theme={null}
tar --list --file archive.tar    # Long form
tar -tf archive.tar              # Short form
```

This displays:

```text theme={null}
file1
file2
file3
```

<Callout icon="lightbulb">
  Always put the `--file` (or `-f`) option at the end of your option list, immediately followed by the archive name.
</Callout>

## Creating and Appending to a Tarball

### Create a New Archive

```bash theme={null}
