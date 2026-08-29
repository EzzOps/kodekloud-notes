# Perform Basic File Management Part 2 Using find

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/GNU-and-Unix-Commands/Perform-Basic-File-Management-Part-2-Using-find/page

This lesson combines find with regular expressions in grep for advanced text analysis on Linux, focusing on extracting specific data from files.

In this lesson, we combine `find` with powerful regular expressions in `grep` to perform advanced text analysis on Linux. Previously, we used simple patterns like searching for “CentOS.” Now, we’ll tackle more complex tasks—such as extracting every IP address (e.g., 203.102.3.5) from multiple scattered files—by writing concise regex patterns that match exactly what you need.

Regular expressions let you define constraints, much like restricting a variable ( x ) in mathematics:

![The image shows a number line with conditions for an integer ( x ) where ( x > 3 ) and ( x \< 8 ). The numbers 3 and 8 are marked, with question marks in between.](https://kodekloud.com/kk-media/image/upload/v1752881400/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Perform-Basic-File-Management-Part-2-Using-find/number-line-conditions-integer-x.jpg)

By combining operators, you create a single pattern that matches only what you allow.

## Common Regular Expression Operators

Below is a quick reference to essential regex operators—mastering these accelerates file searches and log parsing:

| Operator                  | Description                           | Example    |
| ------------------------- | ------------------------------------- | ---------- |
| ^                         | Start of line                         | `^root`    |
| \$                        | End of line                           | `\.conf$`  |
| .                         | Any single character                  | `c.t`      |
| \*                        | Zero or more of the preceding element | `go*d`     |
| +                         | One or more of the preceding element  | `go+d`     |
| ?                         | Zero or one (optional)                | `colou?r`  |
| \[]                       | Character class                       | `[0-9]`    |
| Quantifier (exact, range) | `a{3}`, `b{2,4}`                      |            |
| ()                        | Grouping                              | `(abc)+`   |
| \|                        | Alternation (logical OR)              | `cat\|dog` |
| \[^]                      | Negated character class               | `[^a-z]`   |

<Frame>
  ![The image displays a set of regex operators, including symbols like ^, \$, ., \*, +, \{}, ?, |, \[\], (), and \[^\].](https://kodekloud.com/kk-media/image/upload/v1752881402/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Perform-Basic-File-Management-Part-2-Using-find/regex-operators-symbols-set.jpg)
</Frame>

## Anchors: Matching Line Boundaries

### `^` (Start of Line)

Restrict your search to the beginning of each line:

```bash theme={null}
$ cat names.txt
adam
adnan
basam
samad
samuel
sheela
ravi
mausami

$ grep '^sam' names.txt
samad
samuel
```

You can apply the same technique to system files. For instance, find lines in `/etc/login.defs` that start with `PASS`:

![The image shows a dark-themed command-line interface with the text "The line begins with" at the top. The prompt is ready for input, and "KodeKloud" is visible in the corner.](https://kodekloud.com/kk-media/image/upload/v1752881403/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Perform-Basic-File-Management-Part-2-Using-find/dark-command-line-interface-kodekloud.jpg)

```bash theme={null}
$ grep '^PASS' /etc/login.defs
PASS_WARN_AGE   7
PASS_MAX_DAYS   90
```

### `$` (End of Line)

Match patterns only at the end of lines:

```bash theme={null}
$ grep 'sam$' names.txt
basam

$ grep '7$' /etc/login.defs
PASS_WARN_AGE   7

$ grep 'mail$' /etc/login.defs
MAIL_DIR       /var/spool/mail
#MAIL_FILE     .mail
```

## Wildcard: The Dot `.`

The dot `.` matches exactly one character. To search for any three-letter word starting with ‘c’ and ending with ‘t’:

```bash theme={null}
$ grep -r 'c.t' /etc/
/etc/man_db.conf:#DEFINE cat cat
/etc/man_db.conf:# Range of terminal widths permitted when displaying cat pages.
/etc/nanorc:## double click), and execute shortcuts. The mouse will work in the X
...
```

To match whole words rather than substrings, add `-w`:

```bash theme={null}
$ grep -wr 'c.t' /etc/
/etc/brltty/Input/mn/all.txt:Left: append to existing cut buffer from selected character
/etc/brltty/Input/mn/all.txt:Up: start new cut buffer at selected character
...
```

## Escaping Metacharacters

If you need to match a literal metacharacter (e.g., a dot), escape it with a backslash:

```bash theme={null}
$ grep '\.' /etc/login.defs
