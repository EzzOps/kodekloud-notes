# 022 is the default value, but 027, or even 077, could be considered
HOME_MODE       0700
PASS_WARN_AGE   7

$ grep '7$' /etc/login.defs
PASS_WARN_AGE   7

$ grep 'mail$' /etc/login.defs
MAIL_DIR       /var/spool/mail
#MAIL_FILE     .mail
```

## 3. The Dot (`.`) — Any Single Character

A period in regex matches exactly one character. For instance, `c.t` matches `cat`, `cut`, or `c1t`, but not `ct`.

```bash theme={null}
$ grep -r 'c.t' /etc/
/etc/man_db.conf:# manpath. If no catpath string is used, the catpath will default to the
/etc/man_db.conf:# the database cache for any manpaths not mentioned below unless explicitly
...
```

To restrict matches to whole words, use the `-w` flag:

```bash theme={null}
$ grep -wr 'c.t' /etc/
/etc/brltty/Input/mn/all.txt:Left: append to existing cut buffer from selected character
...
```

### 3.1 Escaping the Dot

If your goal is to match a **literal** dot (`.`), escape it with a backslash:

```bash theme={null}
$ grep '\.' /etc/login.defs
```

## 4. The Asterisk (`*`) — Zero or More

The asterisk applies to the element immediately before it, allowing that element to repeat zero or more times. For example, `let*` matches `le`, `let`, `lett`, `letttt`, etc.:

```bash theme={null}
$ grep -r 'let*' /etc/
/etc/pnm2ppa.conf:#papersize letter    # this is the default
/etc/pnm2ppa.conf:#papersize legal
```

You can combine `.` and `*` to match any sequence of characters. For instance, extracting paths enclosed by slashes:

```bash theme={null}
$ grep -r '/.*/' /etc/
/etc/man_db.conf:# before /usr/man.
/etc/man_db.conf:MANDB_MAP /usr/man
...
```

## 5. The Plus (`+`) — One or More

In **basic** `grep`, the `+` is not treated specially unless escaped. Use `\+` to indicate “one or more” of the preceding item:

```bash theme={null}
$ grep -r '0*' /etc/
$ grep -r '0\+' /etc/
/etc/pnm2ppa.conf:#colorshear 0
/etc/pnm2ppa.conf:#blackshear 0
...
```

<Callout icon="lightbulb">
  Basic `grep` requires escaping `?`, `+`, `|`, `(`, and `)`. To leverage these metacharacters without backslashes, switch to **extended** regex mode using `grep -E` or the `egrep` command.
</Callout>

***

By combining these core operators, you can design precise search patterns to sift through logs, configuration files, or any text data on your Linux system.

## Further Reading and References

* [GNU grep Manual](https://www.gnu.org/software/grep/manual/grep.html)
* [Regular Expressions Tutorial](https://www.regular-expressions.info/)
* [Linux `grep` Command Tutorial](https://www.geeksforgeeks.org/grep-command-in-unixlinux/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/2490f961-886c-4531-be8c-915cccff60a9/lesson/a8082e94-5503-49f2-b9af-0c045e168085" />
</CardGroup>


# Search Text Files Using Regular Expressions Part 1 Understand the differences between basic and extended regular expressions

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/GNU-and-Unix-Commands/Search-Text-Files-Using-Regular-Expressions-Part-1-Understand-the-differences-between-basic-and-extended-regular-expressions/page

This article explains extended regular expressions in Linux, comparing them with basic regex and demonstrating their usage with various tools.

In this lesson, we’ll dive into **extended regular expressions** (ERE) on Linux, compare them with basic regex (BRE), and demonstrate how to leverage powerful metacharacters—without drowning in backslashes. You’ll learn to match repetitions, optional elements, alternation, ranges, sub-expressions, and negations using `grep`, `egrep`, `sed`, and other tools.

## Why Extended Regular Expressions?

Basic regular expressions require backslashes to enable special operators (`\+`, `\?`, `\|`). EREs simplify syntax and unlock built-in support for:

* `+`, `?`, `|`
* Range quantifiers `{m,n}`
* Grouping via `()`

This results in cleaner, more maintainable patterns.

## Enabling ERE in grep

Use `-E` with `grep` or call the `egrep` command directly:

```bash theme={null}
