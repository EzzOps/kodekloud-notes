# Search for files

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/Essential-Commands/Search-for-files/page

This guide explains how to use the `find` command in Linux to locate files based on various criteria.

In this guide, you’ll learn how to quickly locate files on a Linux system using the powerful `find` command. Whether you need to hunt down large log files, uncover recently modified documents, or filter by permissions, `find` provides flexible options to suit your needs.

By default, files on Linux are organized under standard directories:

* SSH daemon configurations: `/etc/ssh`
* System logs: `/var/log`

However, there are many scenarios where you must perform an arbitrary search:

* Locate all image files beneath your web directory
* Identify huge files when disk space is low
* List files modified or created within a specific timeframe

Below, we cover the most common use cases with examples.

## Basic Usage

The general syntax is:

```bash theme={null}
find [search_path] [expression]
```

If you omit `search_path`, `find` searches the **current directory**.

<Callout icon="lightbulb">
  Omitting the search path is equivalent to specifying `.` (the current directory).
</Callout>

### Examples

```bash theme={null}
