# (enter Insert mode, make edits, then Esc)
:wq
[aaron@LFCS-CentOS ~]$ cat testfile
no
yes
no
no
no
no
no
yes
new changes
[aaron@LFCS-CentOS ~]$
```

***

## Additional Resources

* [Vim Documentation](https://vimhelp.org/)
* [GNU less Manual](https://www.gnu.org/software/less/manual/)
* [Linux Command-Line Navigation](https://linuxcommand.org/)

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/cc1949d1-8171-4c8c-b69f-86f96cad0bbe/lesson/23449ef2-bfb1-4049-9f2c-092fd9fd492d)


# Extended Regular Expressions

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/Essential-Commands/Extended-Regular-Expressions/page

This guide explains using Extended Regular Expressions in Linux for crafting powerful searches with tools like grep.

Extended Regular Expressions (ERE) let you write more expressive patterns without backslash escapes for common operators. In this guide, you’ll learn how to use quantifiers, character classes, grouping, alternation, and negation with GNU grep (and similar tools) to craft powerful searches.

## Using grep -E vs egrep

Both `grep -E` and `egrep` enable ERE syntax, so you don’t need to escape `+`, `?`, `{}`, or `|`:

| Command               | Description                                        |
| --------------------- | -------------------------------------------------- |
| `grep -Er '0+' /etc/` | Recursively search for one or more `0` in `/etc/`. |
| `egrep -r '0+' /etc/` | Same as above using `egrep`.                       |

```bash theme={null}
$ grep -Er '0+' /etc/
$ egrep -r '0+' /etc/
```

> **lightbulb** Under the hood, `egrep` is equivalent to `grep -E`. Future versions of GNU grep may deprecate `egrep`.

***

## Curly-Brace Quantifiers

Curly braces let you specify exact or range-based repetition counts:

| Syntax  | Meaning                         |
| ------- | ------------------------------- |
| `{n}`   | Exactly *n* occurrences         |
| `{n,}`  | At least *n* occurrences        |
| `{,m}`  | At most *m* occurrences         |
| `{n,m}` | Between *n* and *m* occurrences |

### Examples

```bash theme={null}
