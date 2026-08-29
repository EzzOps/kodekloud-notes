# Interactive vs non interactive shell

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Introduction/Interactive-vs-non-interactive-shell/page

The article explains the differences between interactive and non-interactive shells in Bash scripting.

Understanding the distinction between **interactive** and **non-interactive** shells is fundamental when writing reliable Bash scripts. Interactive shells are designed for on-the-fly command entry, while non-interactive shells execute prewritten scripts without user intervention.

## Two Modes of Shell Operation

1. **Interactive Mode**\
   You type commands at a prompt and see immediate feedback.
2. **Non-Interactive Mode**\
   You place commands in a file (a script) and run them all at once.

<Callout icon="lightbulb">
  Interactive shells load initialization files like `~/.bashrc`, enabling features such as command history and prompt customization. Non-interactive shells skip most of these initializations.
</Callout>

## Invoking Interactive vs. Non-Interactive Shells

### Interactive Example

```bash theme={null}
$ ls
file1.txt  file2.txt
$ cd /tmp
$ pwd
/tmp
```

### Non-Interactive Example

1. Create a script `script.sh`:
   ```bash theme={null}
   #!/bin/bash
   ls
   cd /tmp
   pwd
   ```
2. Make it executable and run:
   ```bash theme={null}
   chmod +x script.sh
   ./script.sh
   # Output:
   # file1.txt  file2.txt
   # /tmp
   ```

## Comparing Shell Modes

| Feature                 | Interactive Shell             | Non-Interactive Shell             |
| ----------------------- | ----------------------------- | --------------------------------- |
| Invocation              | Direct terminal prompt        | `./script.sh` or `bash script.sh` |
| Input                   | Keyboard                      | Script file or piped commands     |
| Initialization files    | `~/.bashrc`, `PROMPT_COMMAND` | `/etc/profile`, `~/.bash_profile` |
| Common Use Cases        | Ad hoc tasks, debugging       | Automation, cron jobs, CI/CD      |
| Prompt Variable (`PS1`) | Typically set (`\u@\h:\w\$ `) | Usually unset                     |

## Why It Matters

Some environment variables and shell behaviors differ between modes:

### Inspecting `PS1`

**Interactive mode**:

```bash theme={null}
$ echo "$PS1"
\u@\h:\w\$ 
```

**Non-interactive script (`show_ps1.sh`)**:

```bash theme={null}
#!/bin/bash
echo "$PS1"
```

Running it produces no output because `PS1` is unset in non-interactive shells.

<Callout icon="triangle-alert">
  Don’t rely on interactive-only variables (like `PS1`) in scripts. Always initialize or provide defaults for any environment variable your script requires.
</Callout>

## Best Practices for Shell Scripts

* Start with a shebang `#!/usr/bin/env bash` for portability.
* Use `set -euo pipefail` to catch errors early.
* Double-quote variable expansions to prevent word splitting: `"$VAR"`.
* Explicitly source files when needed:
  ```bash theme={null}
  source ~/.bashrc
  ```
* Test scripts in both modes if they must run interactively and non-interactively.

## Further Reading

* [Bash Reference Manual](https://www.gnu.org/software/bash/manual/)
* [Bash Startup Files](https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html)
* [Learn Shell](https://linuxjourney.com/lesson/bash)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/62d639a9-3779-4ae6-b8b2-1cc49f117f64/lesson/ae390d87-135a-4421-a3c4-5552e124406f" />
</CardGroup>
