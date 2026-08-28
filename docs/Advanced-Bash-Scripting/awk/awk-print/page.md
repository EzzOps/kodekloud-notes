# Verify Awk installation
$ awk --version
# Step 1: Print the 3rd field for each line
$ awk '{ print $3 }' minimovies.txt
c
n
n
n
y

# Step 2: Only line 2
$ awk 'NR == 2 { print $3 }' minimovies.txt
n
```

<Callout icon="lightbulb">
  `NR` is a built-in Awk variable representing the current record (line) number.\
  Fields are referenced as `$1`, `$2`, etc.
</Callout>

## Awk as a Domain-Specific Language

Awk is more than a simple filter—it’s a small programming language tailored for text. It provides:

* Pattern-action statements
* Built-in variables (`NR`, `NF`, `FS`, `OFS`)
* Control structures (`if`, `while`, `for`)

<Frame>
  ![The image is a slide titled "Introduction to awk," explaining that a Domain-Specific Language is a programming language designed for a specific subject area.](https://kodekloud.com/kk-media/image/upload/v1752868664/notes-assets/images/Advanced-Bash-Scripting-Introduction-to-awk/introduction-to-awk-dsl-slide.jpg)
</Frame>

<Callout icon="lightbulb">
  Awk treats any sequence of spaces and tabs as the default field separator (`FS` = `[ \t]+`).
</Callout>

## Handling Irregular Spacing

Even if your data has inconsistent spacing, Awk splits fields correctly:

<Frame>
  ![The image is an introduction to "awk," highlighting its ability to create powerful programs or one-liner scripts for parsing large and complex text data easily.](https://kodekloud.com/kk-media/image/upload/v1752868665/notes-assets/images/Advanced-Bash-Scripting-Introduction-to-awk/awk-introduction-text-parsing.jpg)
</Frame>

```bash theme={null}
$ awk 'NR == 2 { print $3 }' minimovies.txt
n
```

## Integrating Awk with Unix Pipelines

Combine Awk with other commands to filter and format on the fly:

```bash theme={null}
$ cat minimovies.txt | awk '$1 == "2" { print $4 }'
n
```

### Common Use Cases

| Command | Purpose              | Example                                  |
| ------- | -------------------- | ---------------------------------------- |
| top     | System runtime stats | `top \| awk '{ print $2 }' \| head -5`   |
| ps      | Process listing      | `ps aux \| awk '$3 > 50 {print $1, $3}'` |
| df -h   | Disk usage report    | `df -h \| awk '$5 > "80%"'`              |

```bash theme={null}
$ top | awk '{ print $2 }' | head -n 5
702
Avg:
996838
353T
41224173/79G
```

```bash theme={null}
$ df -h
Filesystem            Size  Used Avail Use% Mounted on
C:/Program Files/Git   459G  182G  277G  40% /
G:                     15G     0   15G   0% /g
```

## Writing Full Awk Scripts

Instead of one-liners, you can write complete Awk programs:

```awk theme={null}
#!/usr/bin/awk -f
BEGIN {
    print "Hello, World!"
}
```

Make it executable and run directly:

```bash theme={null}
$ chmod +x hello.awk
$ ./hello.awk
Hello, World!
```

<Callout icon="triangle-alert">
  Ensure the shebang path (`/usr/bin/awk`) matches your system’s Awk installation.
</Callout>

Awk transforms text processing into an intuitive workflow by combining pattern matching, field manipulation, and a minimal scripting language. Whether you need quick one-liners or full scripts, Awk has you covered.

## Links and References

* [GNU Awk User’s Guide](https://www.gnu.org/software/gawk/manual/gawk.html)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/0cddb337-89d3-4068-a878-37a0a342c22f/lesson/a72d19f2-bcef-45f0-9cc7-6eb02446b558" />
</CardGroup>


# awk print

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/awk/awk-print/page

This guide covers awk's syntax, pattern-action structure, and the print statement for data extraction and formatting.

Awk is a powerful, domain-specific language built for efficient text processing. In this guide, we'll cover its core syntax, the pattern-action structure, and how to use the `print` statement to extract and format data.

## Awk Usage Overview

```bash theme={null}
awk [options] [program] [file...]
```

| Option         | Description                                                    |
| -------------- | -------------------------------------------------------------- |
| `-F fs`        | Set the input field separator to `fs`                          |
| `-v var=value` | Assign a value to an awk variable before program execution     |
| `-f file`      | Read the awk program from the specified `file`                 |
| `program`      | Provide the awk program directly as a quoted string            |
| `file...`      | One or more input files; if omitted, reads from standard input |

<Callout icon="lightbulb">
  Always quote your `program` (single or double quotes) so the shell passes it verbatim to awk.
</Callout>

For full details, see the [GNU Awk Manual](https://www.gnu.org/software/gawk/manual/gawk.html).

## Pattern-Action Structure

An awk program is a sequence of *pattern-action* pairs:

```text theme={null}
pattern { action }
```

* If **pattern** is omitted, **action** runs on every input line.
* The `{ … }` block is the **action block**, containing commands like `print`, loops, and conditionals.

Example: Start an interactive session that does nothing with your input.

```bash theme={null}
awk '{}'
```

Type lines, then press **Ctrl-D** to end input:

```bash theme={null}
$ awk '{}'
hello world
^D
$
```

<Callout icon="triangle-alert">
  Without quotes around `{}`, many shells will interpret braces or special characters—always quote your action blocks!
</Callout>

## The `print` Statement

Inside the action block, `print` sends its arguments (fields, string literals, variables) to standard output.

### Accessing Fields

By default, awk splits each line on whitespace into fields named `$1`, `$2`, ..., `$NF`.

```bash theme={null}
$ awk '{ print $2 }'
abc def ghi
jkl mno pqr
^D
def
mno
```

### Processing Files

Place the filename after the program to read from a file instead of interactively:

Given `abc.txt`:

```text theme={null}
abc def ghi
jkl mno pqr
xy yz uv
```

Run:

```bash theme={null}
awk '{ print $3 }' abc.txt
```

Output:

```text theme={null}
ghi
pqr
uv
```

### Printing String Literals

You can mix fields and literal strings in a single `print`:

```bash theme={null}
awk '{ print "Line:", $1, "->", $NF }' abc.txt
```

Output:

```text theme={null}
Line: abc -> ghi
Line: jkl -> pqr
Line: xy -> uv
```

### Multiple Expressions

Separate expressions by commas; awk joins them with the **output field separator** (`OFS`, default is a space):

```bash theme={null}
awk '{ print "Hello", "World" }' abc.txt
```

## Redirecting and Piping Input

Awk accepts input from:

* Files:
  ```bash theme={null}
  awk '{ print $0 }' data.txt
  ```
* Standard input via redirection:
  ```bash theme={null}
  awk '{ print $0 }' < data.txt
  ```
* Piping from other commands:
  ```bash theme={null}
  cat data.txt | awk '{ print $1 }'
  ```

## Summary

* **Command structure**: `awk [options] [pattern-action] [file...]`
* **Pattern-action**: `pattern { action }`
* **Fields**: `$1`, `$2`, … `$NF`
* **String literals**: printed as-is within quotes
* **Separators**: input (`FS`) and output (`OFS`)
* **Interactive mode**: omit files; end with **Ctrl-D**, cancel with **Ctrl-C**

## Links and References

* [GNU Awk Manual](https://www.gnu.org/software/gawk/manual/gawk.html)
* [Kurt Werner’s Awk Tutorial](https://www.grymoire.com/Unix/Awk.html)
* [Awk on TLDP](https://tldp.org/LDP/abs/html/awk.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/0cddb337-89d3-4068-a878-37a0a342c22f/lesson/3a318cf3-36c2-44f2-8a85-5fba886c2225" />
</CardGroup>
