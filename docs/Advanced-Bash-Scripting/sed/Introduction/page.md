# (No command given; behavior depends on your sed version)
```

To print only matching lines, use `-n` (quiet mode) with the `p` command:

```bash theme={null}
sed -n '/Manager/p' employees.txt
```

* `-n`          : suppress automatic printing
* `/Manager/`   : search for “Manager”
* `p`           : print matching lines

```bash theme={null}
$ sed -n '/Manager/p' employees.txt
5|Feng|Lin|Sales|Sales Manager|feng.lin@company.com|90000
6|Andy|Luscomb|IT|IT Manager|andy.luscomb@company.com|95000
7|Mark|Crocker|HR|HR Manager|mark.crocker@company.com|85000
8|Jing|Ma|Engineering|Engineering Manager|jing.ma@company.com|100000
```

<Callout icon="lightbulb">
  By default, `sed` performs case-sensitive matches. Searching for `manager` (lowercase) yields no results:
</Callout>

```bash theme={null}
$ sed -n '/manager/p' employees.txt
# No match
```

## 2. Searching Substrings

Match partial strings by specifying only a fragment:

```bash theme={null}
$ sed -n '/Ma/p' employees.txt
4|Enrique|Rivera|Marketing|Marketing Specialist|enrique.rivera@company.com|65000
5|Feng|Lin|Sales|Sales Manager|feng.lin@company.com|90000
6|Andy|Luscomb|IT|IT Manager|andy.luscomb@company.com|95000
7|Mark|Crocker|HR|HR Manager|mark.crocker@company.com|85000
8|Jing|Ma|Engineering|Engineering Manager|jing.ma@company.com|100000
```

This matches “Marketing”, “Manager”, “Mark”, and the last name “Ma”.

## 3. Exact Word Matches with Word Boundaries

Use `\<` and `\>` to match whole words only:

```bash theme={null}
sed -n '/\<Ma\>/p' employees.txt
```

```bash theme={null}
$ sed -n '/\<Ma\>/p' employees.txt
8|Jing|Ma|Engineering|Engineering Manager|jing.ma@company.com|100000
```

**Command breakdown:**

* `sed`         : invoke stream editor
* `-n`          : suppress default output
* `/\<Ma\>/`    : match exact word “Ma”
* `p`           : print matching line

## 4. Combining Multiple Search Patterns

Chain multiple scripts with `-e` to search for more than one pattern:

```bash theme={null}
sed -n \
    -e '/\<Manager\>/p' \
    -e '/\<IT\>/p' \
    employees.txt
```

```bash theme={null}
$ sed -n -e '/\<Manager\>/p' -e '/\<IT\>/p' employees.txt
3|Debbie|Miller|IT|Software Developer|debbie.miller@company.com|80000
5|Feng|Lin|Sales|Sales Manager|feng.lin@company.com|90000
6|Andy|Luscomb|IT|IT Manager|andy.luscomb@company.com|95000
7|Mark|Crocker|HR|HR Manager|mark.crocker@company.com|85000
8|Jing|Ma|Engineering|Engineering Manager|jing.ma@company.com|100000
```

Lines matching either pattern appear once per script.

## 5. Deleting Matches

Swap `p` for `d` to remove matching lines:

Remove Enrique’s record:

```bash theme={null}
sed -e '/\<Enrique\>/d' employees.txt
```

Delete all lines containing “Ma” as a whole word:

```bash theme={null}
$ sed -e '/\<Ma\>/d' employees.txt
1|Kriti|Shreshtha|Finance|Financial Analyst|kriti.shreshtha@company.com|60000
2|Rajasekar|Vasudevan|Finance|Senior Accountant|rajasekar.vasudevan@company.com|75000
3|Debbie|Miller|IT|Software Developer|debbie.miller@company.com|80000
4|Enrique|Rivera|Marketing|Marketing Specialist|enrique.rivera@company.com|65000
5|Feng|Lin|Sales|Sales Manager|feng.lin@company.com|90000
6|Andy|Luscomb|IT|IT Manager|andy.luscomb@company.com|95000
7|Mark|Crocker|HR|HR Manager|mark.crocker@company.com|85000
```

## 6. Editing Files In-Place with `-i`

Apply deletions or substitutions directly using `-i`:

```bash theme={null}
$ sed -i \
    -e '/\<Manager\>/d' \
    -e '/\<IT\>/d' \
    employees.txt

$ cat employees.txt
1|Kriti|Shreshtha|Finance|Financial Analyst|kriti.shreshtha@company.com|60000
2|Rajasekar|Vasudevan|Finance|Senior Accountant|rajasekar.vasudevan@company.com|75000
4|Enrique|Rivera|Marketing|Marketing Specialist|enrique.rivera@company.com|65000
```

<Callout icon="triangle-alert">
  Using `-i` overwrites your source file. Always keep backups or use version control.
</Callout>

## 7. Quick Reference: sed Flags

| Option | Description                 | Example                        |
| ------ | --------------------------- | ------------------------------ |
| -n     | Suppress automatic printing | `sed -n '/pattern/p' file`     |
| -i     | Edit files in-place         | `sed -i 's/foo/bar/' file`     |
| -e     | Add multiple scripts        | `sed -e '/A/p' -e '/B/p' file` |

***

<Frame>
  ![The image is a checklist titled "sed search," highlighting topics such as using the search function with print and delete commands, expressing the dash e flag for multiple scripts, and revisiting the use of flags -n and -i.](https://kodekloud.com/kk-media/image/upload/v1752868669/notes-assets/images/Advanced-Bash-Scripting-Find/sed-search-checklist-flags.jpg)
</Frame>

## Links and References

* [GNU sed Manual](https://www.gnu.org/software/sed/manual/sed.html)
* [Regular Expressions Basics](https://www.regular-expressions.info/)
* [grep vs sed Comparison](https://www.baeldung.com/linux/grep-sed)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/2d48deee-c9f8-4d65-b92f-f164c06b545c/lesson/bb454e07-314d-446e-8aa2-40557903371e" />
</CardGroup>


# Introduction

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/sed/Introduction/page

Introduction to GNU sed for stream editing text from the command line, covering substitutions, line edits, flags, in-place editing, differences with BSD sed, and practical one-liners.

This lesson covers sed — the classic stream editor used for parsing, transforming, and editing text from the command line. sed is compact, fast, and ideal when you want to perform substitutions or line-based edits directly in shell pipelines or scripts.

Quick invocation:

```bash theme={null}
$ sed
```

To clarify when to reach for sed, here's a short comparison with two other common text tools: grep and awk.

| Tool | Primary purpose                            | When to use                                              | Example                         |                  |
| ---- | ------------------------------------------ | -------------------------------------------------------- | ------------------------------- | ---------------- |
| grep | Pattern matching                           | Quickly find lines that contain a pattern                | \`df -h                         | grep "root"\`    |
| awk  | Field/record processing language           | Extract or compute values from columns and rows          | \`df -h                         | awk 'NR == 2 '\` |
| sed  | Stream editing (substitutions, line edits) | Replace text, perform inline edits, or transform streams | `sed 's/sample/are/g' poem.txt` |                  |

Examples below illustrate typical use cases and show how sed compares to grep and awk in practice.

## grep: fast pattern search

grep is optimized for locating matches across large inputs. It doesn’t provide a simple oneliner for replacements (you'd pipe into sed or use other tools for that).

Example — list filesystems and filter for the root entry:

```bash theme={null}
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/root       7.7G  2.9G  4.9G  38% /
devtmpfs        486M     0  486M   0% /dev
tmpfs           490M     0  490M   0% /dev/shm
tmpfs            98M   828K   98M   1% /run
tmpfs           5.0M     0  5.0M   0% /run/lock
tmpfs           490M     0  490M   0% /sys/fs/cgroup

$ df -h | grep "root"
/dev/root       7.7G  2.9G  4.9G  38% /
```

## awk: field- and record-oriented processing

awk is a small but powerful programming language targeted at columns (fields) and rows (records). It’s ideal when you need conditional logic, arithmetic, or formatted output across fields.

Example — print the first non-header (second) line from df:

```bash theme={null}
$ df -h | awk 'NR == 2 { print }'
/dev/root       7.7G  2.9G  4.9G  38% /
```

## sed: stream editor for substitutions and line edits

sed excels at searching and transforming text in streams. Its syntax is compact and familiar to shell users. For many quick substitution tasks, sed is the simplest and most direct tool.

Example — replace every occurrence of "sample" with "are" in a file.

Contents of poem.txt:

```text theme={null}
Roses sample red,
Violets sample blue,
Sugar sample sweet,
And so sample you.
```

Run sed substitution:

```bash theme={null}
$ sed 's/sample/are/g' poem.txt
Roses are red,
Violets are blue,
Sugar are sweet,
And so are you.
```

Explanation of the sed substitution command:

* s — substitute command.
* First `/.../` — pattern to search for (sample).
* Second `/.../` — replacement string (are).
* g — global flag: replace all occurrences in each line. Without `g`, sed replaces only the first match on each line.

So:

```bash theme={null}
sed 's/sample/are/g' poem.txt
```

instructs sed to substitute all occurrences of "sample" with "are" for every line in poem.txt.

## What you'll learn in this section

We will progressively build sed knowledge:

* Basic commands: printing or deleting lines, simple substitutions.
* Flags and modifiers: `g`, address ranges, and regular-expression anchors.
* In-place edits: using `-i` and cross-platform gotchas.
* Advanced patterns: groups, backreferences, and multi-line techniques.
* Useful one-liners and examples for common editing tasks.

An important note: sed differs between platforms. The macOS version is based on BSD and differs in syntax/behavior from the GNU implementation commonly found on Linux.

<Frame>
  <img alt="A dark-themed slide titled &#x22;sed Introduction&#x22; showing two labeled boxes. On the left is a &#x22;MacOS&#x22; tag with &#x22;BSD Unix&#x22; and on the right a &#x22;Linux&#x22; tag with &#x22;GNU Project.&#x22;" />
</Frame>

<Callout icon="lightbulb">
  This lesson focuses on the GNU version of sed, which is more feature-rich and commonly available on Linux systems. If you're on macOS, be aware that some extended options may differ or be unavailable in the BSD sed.
</Callout>

<Callout icon="warning">
  Warning: In-place editing with sed (`-i`) and some extended expressions differ between GNU sed and BSD sed (macOS). When writing portable scripts, test sed commands on all target platforms or use POSIX-compatible constructs.
</Callout>

## Links and references

* [GNU sed Manual — GNU.org](https://www.gnu.org/software/sed/manual/sed.html)
* [sed one-liners collection](https://sed.sourceforge.net/sed1line.txt)
* [Differences between GNU sed and BSD sed (macOS)](https://stackoverflow.com/questions/2011852/portable-way-to-sed-i-in-place-editing)
* [Regular expressions (POSIX) reference](https://www.gnu.org/software/grep/manual/html_node/Regular-Expressions.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/2d48deee-c9f8-4d65-b92f-f164c06b545c/lesson/51198978-e470-402e-b26e-8fd512d8bbcb" />
</CardGroup>
