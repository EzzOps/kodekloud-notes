# Delete

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/sed/Delete/page

This guide explores how to delete lines from input files using the `sed` command, covering various deletion methods and in-place updates.

Stream Editor (`sed`) is a powerful command-line utility for transforming text in a pipeline. In this guide, we’ll explore how to delete lines from input files using the `d` command, covering non-destructive edits, specific-line removals, range deletions, and in-place updates.

## Table of Contents

1. [Overview of the `d` Command](#overview-of-the-d-command)
2. [Non-Destructive Deletion](#non-destructive-deletion)
3. [Deleting a Specific Line](#deleting-a-specific-line)
4. [Deleting a Range of Lines](#deleting-a-range-of-lines)
5. [In-Place Deletion with `-i`](#in-place-deletion-with--i)
6. [Quick Reference](#quick-reference)
7. [Links & References](#links--references)

***

## Overview of the `d` Command

The simplest way to remove lines in `sed` is with the delete script `d`:

```bash theme={null}
sed 'd' employees.txt
```

This command reads every line and deletes it, producing no output.

Under the hood, `sed` follows this syntax:

```text theme={null}
sed [OPTIONS] SCRIPT [INPUT-FILE...]
```

* **SCRIPT**: A quoted set of editing commands (here, `'d'`).
* **INPUT-FILE**: One or more files to process (defaults to standard input).

<Callout icon="lightbulb">
  Wrap your script in single quotes (e.g., `'d'`) so the shell interprets it literally.
</Callout>

***

## Non-Destructive Deletion

By default, `sed` writes the transformed text to **standard output** and leaves the original file unchanged. To delete line 2 from `employees.txt`:

```bash theme={null}
sed '2d' employees.txt
```

Output:

```text theme={null}
1|Kriti|Shreshtha|Finance|Financial Analyst|kriti.shreshtha@company.com|60000
3|Debbie|Miller|IT|Software Developer|debbie.miller@company.com|80000
4|Enrique|Rivera|Marketing|Marketing Specialist|enrique.rivera@company.com|65000
5|Feng|Lin|Sales|Sales Manager|feng.lin@company.com|90000
6|Andy|Luscomb|IT|IT Manager|andy.luscomb@company.com|95000
7|Mark|Crocker|HR|HR Manager|mark.crocker@company.com|85000
8|Jing|Ma|Engineering|Engineering Manager|jing.ma@company.com|100000
```

Your source file remains intact:

```bash theme={null}
cat employees.txt
```

***

## Deleting a Specific Line

To drop only the sixth line:

```bash theme={null}
sed '6d' employees.txt
```

This command filters out line 6 from the output stream, leaving all others.

***

## Deleting a Range of Lines

Use a comma-separated address pair to remove a block of lines:

```bash theme={null}
sed '3,5d' employees.txt
```

This deletes lines 3 through 5.

<Callout icon="triangle-alert">
  Address ranges must ascend (e.g., `3,5d`). Specifying `5,3d` is invalid and will have no effect.
</Callout>

***

## In-Place Deletion with `-i`

To modify the file directly, add the `-i` (in-place) option:

```bash theme={null}
