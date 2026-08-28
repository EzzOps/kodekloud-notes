# Create a new directory
mkdir project_build

# Change into the new directory using $_
cd $_

# Show current path
pwd
```

Here, `$_` saves you from typing `project_build` again.

***

## Common Use Cases

| Scenario            | Last Command                      | `$_` Value              |
| ------------------- | --------------------------------- | ----------------------- |
| Copying a file      | `cp large_archive.tar.gz /backup` | `/backup`               |
| Editing a file      | `vim /etc/nginx/nginx.conf`       | `/etc/nginx/nginx.conf` |
| Moving a directory  | `mv logs_old logs_archive`        | `logs_archive`          |
| Pipelining commands | `grep ERROR logfile.log`          | `logfile.log`           |

***

## Advanced Examples

```bash theme={null}
# Remove a file, then verify its removal
rm temp_data.csv
echo "Removed" $_

# Using in a pipeline
find . -name '*.log' | xargs gzip
echo "Compressed" $_
```

***

## Further Reading

* [Bash Reference Manual](https://www.gnu.org/software/bash/manual/)
* [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)

<Callout icon="triangle-alert">
  If you chain multiple commands with `;` or `&&`, `$_` always reflects the **very last argument** of the last executed command.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/7ff1ccc1-5a14-41fc-817c-c0ec4a100231/lesson/ff4a84c5-46bc-4f66-9d70-4aa06539d2f7" />
</CardGroup>


# Zero

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Special-Shell-Variables/Zero/page

This article explains the use of the `$0` special shell variable in Bash scripting for script name retrieval and directory resolution.

In Bash scripting, the special parameter `$0` holds the name (and path) used to invoke the script. Understanding and manipulating `$0` lets you:

1. Retrieve the script’s invoked name or full path
2. Derive the absolute directory where the script resides

Below, we explore each technique with practical examples and patterns for robust, user-friendly scripts.

***

## Table of Contents

1. [Getting the Invoked Script Name](#1-getting-the-invoked-script-name)
2. [Extracting Only the Basename](#2-extracting-only-the-basename)
3. [Dynamic Usage Messages with `SCRIPT_NAME`](#3-dynamic-usage-messages-with-script_name)
4. [Graceful Exits via a `terminate` Helper](#4-graceful-exits-via-a-terminate-helper)
5. [Resolving the Script’s Directory (`WORK_DIR`)](#5-resolving-the-scripts-directory-work_dir)
6. [Quick Reference Table](#6-quick-reference-table)
7. [Links and References](#7-links-and-references)

***

## 1. Getting the Invoked Script Name

By default, `$0` prints exactly how the script was called:

```bash theme={null}
#!/usr/bin/env bash
echo "$0"
```

Save this as `show-zero.sh` and run:

```bash theme={null}
$ ./show-zero.sh
./show-zero.sh

$ # If on your PATH:
$ show-zero.sh
/usr/local/bin/show-zero.sh
```

***

## 2. Extracting Only the Basename

To obtain just the filename (dropping any leading directories), use shell parameter expansion:

```bash theme={null}
#!/usr/bin/env bash
readonly SCRIPT_NAME=${0##*/}
echo "${SCRIPT_NAME}"
```

Running:

```bash theme={null}
$ ./show-zero.sh
show-zero.sh
```

Here `${0##*/}` strips everything up to the last slash.

***

## 3. Dynamic Usage Messages with `SCRIPT_NAME`

Embedding the script’s basename in help text ensures accuracy, even if the file is renamed:

```bash theme={null}
#!/usr/bin/env bash
readonly SCRIPT_NAME=${0##*/}

usage() {
  cat <<USAGE
Usage: ${SCRIPT_NAME} <name>

Greet a user by name.

Arguments:
  name       The name to greet.

Options:
  -h, --help Show this help message and exit.
USAGE
}
