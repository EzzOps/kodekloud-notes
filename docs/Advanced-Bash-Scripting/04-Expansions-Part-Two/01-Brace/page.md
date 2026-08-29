# Output:
# John Doe
```

Using braces helps delimit variable names clearly:

```bash theme={null}
name="John Doe"
echo "Hello, ${name}"
# Output:
# Hello, John Doe
```

Variable names are case-sensitive and may contain letters, digits, and underscores:

```bash theme={null}
# Invalid:
# Valid:
name_user="John Doe"
```

## Using Curly Braces

Curly braces `{}` not only disambiguate names but also unlock advanced parameter expansion features.

### Avoiding Ambiguity

Without braces, attached text can be misinterpreted:

```bash theme={null}
#!/usr/bin/env bash
height=170

# Wrong: shell looks for 'heightcm'
echo "Your height is: $heightcm"

# Correct: braces isolate 'height'
echo "Your height is: ${height}cm"
# Output:
# Your height is: 170cm
```

### Default Values

Provide a fallback when a variable is unset or empty:

<Callout icon="lightbulb">
  Use `${var:-default}` to safely reference a variable that may not exist.
</Callout>

```bash theme={null}
#!/usr/bin/env bash
echo "Hello, ${name:-Unknown}"
# If 'name' is unset:
# Output:
# Hello, Unknown
```

## Parameter Expansion Operators

| Expansion Type       | Syntax                 | Description                                      |
| -------------------- | ---------------------- | ------------------------------------------------ |
| Default Value        | `${var:-default}`      | Use `default` if `var` is unset or null          |
| Substring Extraction | `${var:offset:length}` | Extract a substring starting at `offset`         |
| String Replacement   | `${var/pattern/repl}`  | Replace the first match of `pattern` with `repl` |
| Length               | `${#var}`              | Return the length of `var`’s value               |

## String Manipulation

### Substring Extraction

Pull out part of a string using an offset and length:

```bash theme={null}
#!/usr/bin/env bash
name="John Doe"
echo "Hello, ${name:0:4}"
# Output:
# Hello, John
```

### Substring Replacement

Replace the first occurrence of a pattern:

```bash theme={null}
#!/usr/bin/env bash
path="/home/user/file.txt"
echo "${path/file/data}"
# Output:
# /home/user/data.txt
```

## Length of a Variable

Determine the number of characters in a variable’s value:

```bash theme={null}
#!/usr/bin/env bash
name="John Doe"
echo "${#name}"
# Output:
# 8
```

## Quoting and Word Splitting

By default, unquoted expansions undergo word splitting. To preserve spaces, quote your variables. If you want to iterate over words, leave them unquoted:

```bash theme={null}
#!/usr/bin/env bash
readonly SERVERS="server1 server2 server3"

# Iterate over each hostname:
for server in $SERVERS; do
  echo "${server}.kodekloud.com"
done
# Output:
# server1.kodekloud.com
# server2.kodekloud.com
# As a single string when quoted:
for server in "$SERVERS"; do
  echo "${server}.kodekloud.com"
done
# Output:
# server1 server2 server3.kodekloud.com
```

<Callout icon="triangle-alert">
  Always quote expansions containing spaces unless you explicitly need word splitting.
</Callout>

## Additional Resources

* [GNU Bash Manual – Shell Parameter Expansion](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html)
* [Bash Reference Manual](https://www.gnu.org/software/bash/manual/)
* [Understanding Quoting in Bash](https://tldp.org/LDP/abs/html/quotingvar.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/0e090d75-12b5-4e0f-ace8-519f11d7b5d2/lesson/504de133-a0ad-437b-9cb1-d2fc50a5a4aa" />
</CardGroup>


# Brace

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Expansions-Part-Two/Brace/page

This article explains brace expansion in Bash, a feature for generating strings or arguments using curly braces.

Brace expansion is a powerful shell feature that generates arbitrary strings or arguments by evaluating expressions within curly braces `{}`. Unlike globs, which match existing filenames, brace expansions create new text before any other expansion (such as pathname or parameter expansion) takes place.

<Callout icon="lightbulb">
  Brace expansions are always processed **before** globs and parameter expansions. This lets you quickly generate lists of filenames, parameters, or other strings in a single command.
</Callout>

## Table of Content

1. [Basic Range Expansion](#1-basic-range-expansion)
2. [Department Usernames Example](#2-department-usernames-example)
3. [Comma-Separated List Expansion](#3-comma-separated-list-expansion)
4. [Numeric Range Expansion](#4-numeric-range-expansion)
5. [Nested Brace Expansions](#5-nested-brace-expansions)
6. [Step-Based Range Expansion (Bash 4.0+)](#6-step-based-range-expansion-bash-40)
7. [Prefix and Suffix with Brace Expansion](#7-prefix-and-suffix-with-brace-expansion)
8. [Integrating Brace Expansion in Scripts](#8-integrating-brace-expansion-in-scripts)
9. [Summary & Best Practices](#9-summary--best-practices)
10. [Links and References](#10-links-and-references)

***

## 1. Basic Range Expansion

Alphabetic and numeric ranges let you generate sequences with minimal syntax.

```bash theme={null}
