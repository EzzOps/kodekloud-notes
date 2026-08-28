# Save sorted output to a new file
$ sort file.txt > sortedfile.txt
$ cat sortedfile.txt
1
2
3
4
5
6
```

## Redirecting stdout: overwrite vs append

* > overwrites (creates the file if it doesn't exist).
* > > appends to the file.

Example — overwrite (only the last run remains):

```bash theme={null}
$ date > file.txt
$ date > file.txt
$ cat file.txt
Mon Nov  8 18:50:30 CST 2021
```

Example — append (each timestamp preserved):

```bash theme={null}
$ date >> file.txt
$ date >> file.txt
$ cat file.txt
Mon Nov  8 18:50:30 CST 2021
Mon Nov  8 18:50:31 CST 2021
```

Quick comparison:

| Operator | Behavior         | Creates file if missing |
| -------: | ---------------- | :---------------------: |
|        > | Overwrite stdout |           Yes           |
|       >> | Append stdout    |           Yes           |

## File descriptors and common redirections

Programs use three standard streams:

| Descriptor | Name   | Purpose                                            |
| ---------: | ------ | -------------------------------------------------- |
|          0 | stdin  | Input to the process (keyboard or redirected file) |
|          1 | stdout | Normal program output                              |
|          2 | stderr | Error messages and diagnostics                     |

Common redirection operators:

| Syntax                      | Meaning                                   |
| --------------------------- | ----------------------------------------- |
| \< file.txt                 | Redirect stdin from file.txt              |
| > file.txt or 1> file.txt   | Redirect stdout to file.txt (overwrite)   |
| >> file.txt or 1>> file.txt | Append stdout to file.txt                 |
| 2> errors.txt               | Redirect stderr to errors.txt (overwrite) |
| 2>> errors.txt              | Append stderr to errors.txt               |

<Callout icon="lightbulb">
  File descriptors: 0 = stdin, 1 = stdout, 2 = stderr. Use 2> to redirect error messages separately from normal output.
</Callout>

## Discard unwanted output: /dev/null

Send output you don't want to see to /dev/null — a special sink that discards everything.

Example: hide permission-denied messages from a recursive grep:

```bash theme={null}
# Without suppression: stderr clutter
$ grep -r '^The' /etc/
grep: /etc/cups/ssl: Permission denied
...

# Suppress stderr by redirecting it to /dev/null
$ grep -r '^The' /etc/ 2>/dev/null
/etc/brltty/Input/tn/all.txt:The two keys at the left rear (2 columns, 1 row):
...
```

## Redirect stdout and stderr separately

Capture normal output and errors in different files:

```bash theme={null}
# Overwrite files
$ grep -r '^The' /etc/ 1>output.txt 2>errors.txt

# Append to files
$ grep -r '^The' /etc/ 1>>output.txt 2>>errors.txt
```

## Redirect both stdout and stderr to the same file

To collect both streams into one file, redirect stdout first, then redirect stderr to stdout with 2>&1. The order matters:

```bash theme={null}
# Correct: both streams go into all_output.txt
$ grep -r '^The' /etc/ > all_output.txt 2>&1

# Equivalent with explicit descriptor
$ grep -r '^The' /etc/ 1>all_output.txt 2>&1
```

Why order matters:

* 1>all\_output.txt sets stdout to the file.
* 2>&1 then points stderr to wherever stdout is currently going (the file).
  If you reverse the order (2>&1 1>file), stderr is redirected to the original stdout (the terminal) before stdout is redirected, so errors still appear on-screen.

## Input redirection (\<) and feeding commands

Some programs read from stdin instead of accepting a filename. Use \< to provide a file as stdin:

```bash theme={null}
# Example: feed an email body from a file to a sendemail utility that reads stdin
$ sendemail someone@example.com < emailcontent.txt
```

## Here-documents and here-strings

Use here-documents (heredocs) for multi-line inline input. Terminate with the chosen delimiter (EOF is common):

```bash theme={null}
$ sort <<EOF
6
3
2
5
1
4
EOF
1
2
3
4
5
6
```

Here-strings pass a single string to stdin using \<\<\<:

```bash theme={null}
$ bc <<< "1+2+3+4"
10
```

## Piping: chain small tools

Pipes (|) send the stdout of one command into the stdin of the next. This enables powerful one-line workflows:

Example — remove commented lines, sort, and column-format the file:

```bash theme={null}
# Show non-comment lines
$ grep -v '^#' /etc/login.defs

# Pipe into sort
$ grep -v '^#' /etc/login.defs | sort

# Pipe into column for neat alignment
$ grep -v '^#' /etc/login.defs | sort | column -t
CREATE_HOME        yes
ENCRYPT_METHOD     SHA512
GID_MAX            60000
...
```

Pipes are essential for combining simple Unix tools into effective data-processing chains — searching, sorting, formatting, counting, and more.

## Quick reference: common patterns

| Goal                       | Example                |      |      |
| -------------------------- | ---------------------- | ---- | ---- |
| Overwrite stdout to file   | command > file.txt     |      |      |
| Append stdout to file      | command >> file.txt    |      |      |
| Redirect stderr to file    | command 2> errors.txt  |      |      |
| Append stderr to file      | command 2>> errors.txt |      |      |
| Redirect both to same file | command > all.txt 2>&1 |      |      |
| Suppress stderr            | command 2>/dev/null    |      |      |
| Read stdin from file       | command \< input.txt   |      |      |
| Pipeline multiple commands | cmd1                   | cmd2 | cmd3 |

## Further reading and references

* Bash manual — Redirections: [https://www.gnu.org/software/bash/manual/html\_node/Redirections.html](https://www.gnu.org/software/bash/manual/html_node/Redirections.html)
* Unix I/O and file descriptors overview: [https://en.wikipedia.org/wiki/Standard\_streams](https://en.wikipedia.org/wiki/Standard_streams)
* Advanced shell scripting techniques (pipes, heredocs): [https://tldp.org/LDP/abs/html/](https://tldp.org/LDP/abs/html/)

That’s all for this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/cc1949d1-8171-4c8c-b69f-86f96cad0bbe/lesson/7295b13d-8b26-4d1e-b5a2-6ef87502a7d9" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/cc1949d1-8171-4c8c-b69f-86f96cad0bbe/lesson/9a83d820-3004-4b8c-916c-75249ac75581" />
</CardGroup>


# Introduction

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-[AWS_SECRET_ACCESS_KEY]

This course teaches essential Linux skills through hands-on labs and interactive articles for beginners in system administration.

Welcome to **Linux System Administration for Beginners**! In this course, Aaron Lockhart guides you through essential Linux skills:

<Frame>
  ![The image shows a list of topics related to system administration skills, such as logging into systems, managing files, and user accounts, alongside a person speaking.](https://kodekloud.com/kk-media/image/upload/v1752881487/notes-assets/images/Linux-System-Administration-for-Beginners-Introduction/system-administration-skills-topics-list.jpg)
</Frame>

* Local and remote host login
* Reading and using system documentation
* Working with files and directories
* Creating and managing hard and soft symlinks
* Listing, setting, and changing file permissions
* Searching files with `grep` and using regular expressions
* Managing user accounts and privileges
* Controlling access to the root account

By the end of this course, you'll have a high-level understanding of Linux and hands-on experience through interactive, browser-based labs—no environment setup required. Switch from reading to practicing in under 30 seconds!

***

## What You’ll Learn

| Topic                      | Description                                     | Hands-On Practice                         |
| -------------------------- | ----------------------------------------------- | ----------------------------------------- |
| User & Group Management    | Create, modify, and delete accounts             | User management labs                      |
| File System Navigation     | Traverse directories and manipulate files       | Directory structure exercises             |
| Permissions & Ownership    | Set and change file modes and ownership         | `chmod` & `chown` challenges              |
| Symbolic & Hard Links      | Link files for flexible references              | Symlink creation tasks                    |
| SSH Server Configuration   | Secure remote access via SSH                    | `sshd_config` editing                     |
| System Resource Monitoring | Inspect and manage processes, memory, and disks | `top`, `free`, `lsblk` hands-on scenarios |
| Advanced Text Processing   | Search and analyze text with `grep` and regex   | Pattern matching exercises                |

***

## Interactive Labs

Each concept includes a challenge-based lab with instant feedback. Try to solve each exercise yourself; hints and full solutions are available if you get stuck.

<Callout icon="lightbulb">
  Practice labs open directly in your browser—no installation needed. You can retry as many times as necessary before moving on.
</Callout>

To get the most out of this course, minimize distractions—turn off mobile and desktop notifications—and dedicate focused time to follow the curriculum and complete labs in sequence.

***

## Course Format

Hello! I’m Aaron Lockhart, your instructor for KodeKloud’s Linux tutorial. According to [Stack Overflow’s Developer Survey](https://insights.stackoverflow.com/survey), Linux is the most loved platform among developers.

This course is hands-on, featuring:

* Interactive articles with clear illustrations and animations
* Live demonstration videos for complex tasks
* Browser-based labs for real-world practice

### Live Demonstrations

In video demos, I’ll walk you through commands and utilities, showing real-world examples and best practices.

***

## Links and References

* [OpenSSH Manual: sshd\_config(5)](https://man.openbsd.org/sshd_config.5)
* [Linux Documentation Project](http://tldp.org/)
* [Stack Overflow Insights](https://insights.stackoverflow.com/survey)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/c73f5dce-79a1-407b-9924-dc437f02821a/lesson/42c65198-d27c-440f-9e1d-f7c3b357fc83" />
</CardGroup>
