# Built in Variables

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/awk/Built-in-Variables/page

This guide explains how to use awk's built-in variables for efficient text data parsing and manipulation.

In this guide, you’ll learn how to leverage **awk**’s built-in variables to parse and manipulate text data efficiently. We’ll cover:

* Positional variables (`$1`, `$2`, …)
* `NR` (Number of Records)
* `NF` (Number of Fields)
* `$NF` (Last Field in the Current Record)
* `FILENAME`

Throughout this article, we’ll use a sample file, **size.txt**, generated from `df -h`:

```bash theme={null}
df -h > size.txt
```

***

## 1. Positional Variables

By default, **awk** splits each input line on whitespace. You can print specific fields using `$1`, `$2`, `$3`, and so on:

```bash theme={null}
awk '{ print $1, $2, $3 }' abc.txt
```

* `$1` → first column
* `$2` → second column
* `$3` → third column

For example, given `abc.txt`:

```text theme={null}
abc def ghi
jkl mno pqr
stu vwx yz
```

```bash theme={null}
awk '{ print $1 }' abc.txt
