# Dash

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Special-Shell-Variables/Dash/page

This article explains the `$-` special shell variable in Bash, detailing its flags and differences between interactive and non-interactive modes.

The `$-` variable in Bash shows the current shell’s option flags. These flags differ when you run commands interactively versus inside a script. In this guide, we’ll:

* Inspect `$-` interactively
* Compare interactive vs. non-interactive outputs
* Demonstrate how `set -e` affects `$-`
* Review common `$-` flags in a summary table

***

## Checking `$-` Interactively

Run the following command in your terminal to see which flags are active in your interactive shell:

```bash theme={null}
echo $-
```

Example output:

```bash theme={null}
himBHs
```

Each letter (such as `h`, `i`, `m`, `B`, `H`, `s`) represents a specific shell option. These may vary between systems and user configurations.

> **lightbulb** The exact set of flags depends on your Bash version and how you’ve configured your environment (e.g., via `.bashrc` or `.bash_profile`).

***

## Comparing with a Non‐Interactive Script

Create a file named `special-dash.sh`:

```bash theme={null}
#!/usr/bin/env bash
echo $-
```

Make it executable and run it:

```bash theme={null}
chmod +x special-dash.sh
./special-dash.sh
```

Typical output:

```bash theme={null}
hB
```

You’ll notice the `i` flag (interactive mode) is missing because scripts run non-interactively by default.

***

## Enabling “Exit on Error” with `set -e`

The `set -e` option causes Bash to exit immediately if any command returns a non-zero status. Let’s enable it in our script:

```bash theme={null}
#!/usr/bin/env bash
set -e
echo $-
```

Run the updated script:

```bash theme={null}
./special-dash.sh
```

Now you should see:

```bash theme={null}
ehB
```

The leading `e` indicates that “exit on error” is active.

> **triangle-alert** Using `set -e` can make debugging harder if you’re not careful. Always test scripts thoroughly or combine with `set -u` and `set -o pipefail` for stricter error checking.

***

## Common `$-` Flags

| Flag | Description                                        |
| ---- | -------------------------------------------------- |
| i    | Shell is running in interactive mode               |
| e    | Exit immediately if a command exits with failure   |
| u    | Treat unset variables as an error                  |
| x    | Print commands and their arguments as they execute |

***

## Further Reading

* [Bash Reference Manual – Invocations](https://www.gnu.org/software/bash/manual/html_node/Invocations.html)
* [Bash Scripting Guide](https://tldp.org/LDP/Bash-Beginners-Guide/html/)

***

By understanding and inspecting the `$-` variable, you can better control your shell’s behavior in both interactive sessions and automated scripts.

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/7ff1ccc1-5a14-41fc-817c-c0ec4a100231/lesson/2ea36ac0-a04e-4a85-84eb-e2978e3dd9ac)
