# no output, exit code 0
```

<Callout icon="triangle-alert">
  Don’t confuse `:` with the external `true` command—`:` is built into the shell and more efficient.
</Callout>

## References and Further Reading

* [Ansible CLI Options](https://docs.ansible.com/ansible/latest/cli/ansible-playbook.html#cmdoption-ansible-playbook-check)
* [kubectl dry-run Documentation](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#apply)
* [Puppet noop Mode](https://puppet.com/docs/puppet/latest/applying_catalogs.html#noop)

For more on advanced Bash scripting patterns and best practices, visit the [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/48c76c43-0257-44a4-b95d-36a8cceaff66/lesson/a8104f85-10c5-467a-a12e-8e5b8e367186" />
</CardGroup>


# Course Introduction

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Introduction/Course-Introduction/page

Learn advanced techniques and best practices to enhance your Bash scripting skills through interactive labs and hands-on exercises.

Welcome to the **Advanced Bash Scripting** course on KodeKloud. I’m Juan Carlos Martinez, and I’ll guide you through the techniques and best practices that will elevate your Bash scripting skills.

## What You’ll Learn

| Module                             | Description                                                                                  |
| ---------------------------------- | -------------------------------------------------------------------------------------------- |
| Shell Environments                 | Understand **interactive vs non-interactive** shells and when each is used.                  |
| Script Style & Conventions         | Learn naming, formatting, and commenting standards for maintainable scripts.                 |
| Core Bash Constructs               | Revisit control structures, command types, the shebang line, and I/O redirection.            |
| Advanced Expansions & Globbing     | Master parameter, command, and arithmetic expansions as well as pattern matching (globbing). |
| Special Shell Variables            | Explore variables like `$?`, `$$`, and `$#` for status, process IDs, and parameter counts.   |
| Arrays and Complex Data Handling   | Work with indexed and associative arrays for structured data management.                     |
| Powerful Text Processing Tools     | Leverage **awk**, **sed**, and other command-line utilities for robust text manipulation.    |
| Interactive Labs & Code Challenges | Apply each concept in hands-on exercises to reinforce your learning.                         |

## Why Practice Matters

<Callout icon="lightbulb">
  “Practice is the hardest part of learning, and training is the essence of transformation.”\
  – Ann Boscum
</Callout>

Typing and running each example yourself is the best way to internalize these concepts.

## Key Concepts Overview

1. **Interactive vs Non-Interactive Shells**\
   How shells behave when reading from a terminal versus a script.

2. **Shebang Line (`#!`)**\
   Ensuring your script runs with the intended shell interpreter.

3. **Streams & Redirection**\
   Redirecting standard output (`stdout`) and standard error (`stderr`) to files or other commands.

4. **Control Structures**\
   Using `if`, `case`, `for`, `while`, and `until` for flow control.

5. **Expansions**
   * Parameter expansion
   * Command substitution
   * Arithmetic expansion

6. **Globbing & Pattern Matching**\
   Matching file names with wildcards (`*`, `?`, `[]`).

7. **Special Variables**\
   Exploring shell-provided variables like `$?`, `$$`, and `$#` for status codes, process IDs, and argument counts.

8. **Arrays**\
   Indexed and associative arrays for storing lists and key/value pairs.

9. **Text Processing with awk & sed**\
   Powerful one-liners and scripts for parsing and transforming text.

## Interactive Labs and Challenges

Throughout the course, you’ll encounter scenarios where you must:

* Write scripts that validate user input.
* Process log files with **awk** and **sed**.
* Automate system checks and reporting.

<Callout icon="triangle-alert">
  Always test your scripts in a safe environment before deploying them in production!
</Callout>

## Further Reading & References

* [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)
* [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)
* [KodeKloud Labs](https://kodekloud.com/labs/)

Thank you for choosing this course. Let’s get started on your journey to mastering Advanced Bash Scripting!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/62d639a9-3779-4ae6-b8b2-1cc49f117f64/lesson/7638aa37-bddb-447d-8e1a-f843f2af5acd" />
</CardGroup>
