# Show usage
usage
```

Example output:

```bash theme={null}
$ ./show-zero.sh
Usage: show-zero.sh <name>

Greet a user by name.

Arguments:
  name       The name to greet.

Options:
  -h, --help Show this help message and exit.
```

***

## 4. Graceful Exits via a `terminate` Helper

Centralize error reporting and custom exit codes:

```bash theme={null}
#!/usr/bin/env bash
readonly SCRIPT_NAME=${0##*/}
readonly ERR_MISSING_ARG=155

usage() {
  cat <<USAGE
Usage: ${SCRIPT_NAME} <name>

Greet a user by name.

Options:
  -h, --help Show this help message and exit.
USAGE
}

terminate() {
  echo "Error: ${1}" >&2
  exit "${2:-1}"
}

# Argument count check
if [[ $# -ne 1 ]]; then
  usage
  terminate "Missing argument" "$ERR_MISSING_ARG"
fi

# Help flag
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  usage
  exit 0
fi

name="$1"
echo "Hello, ${name}! Welcome!"
exit 0
```

Example runs:

```bash theme={null}
$ ./greet.sh
Usage: greet.sh <name>
Error: Missing argument
$ echo $?
155

$ ./greet.sh --help
Usage: greet.sh <name>
$ echo $?
0
```

<Callout icon="lightbulb">
  For more advanced flag parsing, consider using `getopts` to handle short and long options.
</Callout>

***

## 5. Resolving the Script’s Directory (`WORK_DIR`)

Hard-coding relative paths can break when you run scripts from different locations. Instead, compute the script’s own directory:

```bash theme={null}
#!/usr/bin/env bash
readonly WORK_DIR=$(dirname "$(readlink -f "$0")")
```

* `readlink -f "$0"` returns the script’s canonical absolute path (following symlinks).
* `dirname` extracts the parent directory.

Now you can reliably reference files relative to the script’s location:

```bash theme={null}
cd "${WORK_DIR}/../assets"
cd "${WORK_DIR}/subdir"
# ...other tasks
```

<Callout icon="triangle-alert">
  On macOS, `readlink -f` may not be available. Use `brew install coreutils` or alternative methods (`realpath`).
</Callout>

***

## 6. Quick Reference Table

| Feature                        | Purpose                                        | Example                                      |
| ------------------------------ | ---------------------------------------------- | -------------------------------------------- |
| `$0`                           | How the script was invoked                     | `echo "$0"`                                  |
| `${0##*/}`                     | Basename of the script                         | `SCRIPT_NAME=${0##*/}`                       |
| Dynamic heredoc usage messages | Embed `SCRIPT_NAME` in help text               | `cat <<USAGE…`                               |
| `terminate()`                  | Standardize error output and exit codes        | `terminate "message" 42`                     |
| `readlink -f` + `dirname`      | Compute absolute script directory (`WORK_DIR`) | `WORK_DIR=$(dirname "$(readlink -f "$0")")"` |

***

## 7. Links and References

* [Bash Parameter Expansion](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html)
* [readlink (Linux) Manual](https://man7.org/linux/man-pages/man1/readlink.1.html)
* [getopts Bash Built-in](https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html)

These patterns make your Bash scripts more predictable, portable, and user-friendly—leveraging `$0` effectively is a key skill for any shell scripter.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/7ff1ccc1-5a14-41fc-817c-c0ec4a100231/lesson/8b30db1e-0226-435a-9ceb-b074e91c10a3" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/7ff1ccc1-5a14-41fc-817c-c0ec4a100231/lesson/7d0d01f5-9b2a-432a-b9ea-0479e538d920" />
</CardGroup>


# ifs

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Special-Shell-Variables/ifs/page

The article explains the Internal Field Separator (IFS) in Bash, its default behavior, customization, and implications for string manipulation in shell scripting.

The Internal Field Separator (`IFS`) is a special shell variable that defines how Bash—and other POSIX-compatible shells—split strings into fields. While environment variables provide static, system-wide settings, shell variables like `IFS` are dynamic and scoped to your shell session. Properly managing `IFS` enhances portability by ensuring your scripts behave consistently across different systems.

<Frame>
  ![The image features a magnifying glass with the text "IFS Environment variables" and a thumbs-up icon, set against a dark background.](https://kodekloud.com/kk-media/image/upload/v1752868625/notes-assets/images/Advanced-Bash-Scripting-ifs/ifs-environment-variables-magnifying-glass.jpg)
</Frame>

By default, `IFS` includes space, tab, and newline. This default behavior impacts many common tasks, such as iterating over lists of filenames or parsing command output.

## Table of Default IFS Separators

| Separator | Escape Sequence | Description        |
| --------- | --------------- | ------------------ |
| Space     | `<space>`       | Splits on spaces   |
| Tab       | `\t`            | Splits on tabs     |
| Newline   | `\n`            | Splits on newlines |

## Default IFS in Action

Consider a simple Bash script that iterates over a space-separated list:

```bash theme={null}
#!/usr/bin/env bash
elements="alpha beta gamma"
for element in ${elements}; do
  echo "${element} is now separated from the elements list"
done
```

Running this script yields:

```text theme={null}
alpha is now separated from the elements list
beta is now separated from the elements list
gamma is now separated from the elements list
```

Because `elements` splits on spaces by default, each word becomes its own iteration.

## Customizing IFS with ANSI-C Quoting

To explicitly redefine `IFS` to include space, tab, and newline, use ANSI-C quoting:

```bash theme={null}
IFS=$' \t\n'
```

<Callout icon="lightbulb">
  The `$'…'` syntax tells Bash to process backslash escapes within single quotes, ensuring you include the exact characters you need.
</Callout>

<Frame>
  ![The image is a slide titled "ANSI-C Quoting" and explains that it starts with a dollar sign.](https://kodekloud.com/kk-media/image/upload/v1752868626/notes-assets/images/Advanced-Bash-Scripting-ifs/ansi-c-quoting-dollar-sign.jpg)
</Frame>

## Changing the Field Separator

If your data uses a different delimiter—such as a colon (`:`)—override `IFS` before expanding variables. Without overriding, the string remains intact:

```bash theme={null}
#!/usr/bin/env bash
elements="one:two:three"
for element in ${elements}; do
  echo "${element} is now separated from the elements list"
done
```

Output:

```text theme={null}
one:two:three is now separated from the elements list
```

Now set `IFS` to a colon:

```bash theme={null}
#!/usr/bin/env bash
IFS=":"
elements="one:two:three"
for element in ${elements}; do
  echo "${element} is now separated from the elements list"
done
```

Output:

```text theme={null}
one is now separated from the elements list
two is now separated from the elements list
three is now separated from the elements list
```

<Callout icon="triangle-alert">
  Changing `IFS` globally can affect subsequent commands and scripts. Always restore it to its default value after making temporary adjustments.
</Callout>

## IFS and Literal Strings

`IFS` only applies when expanding variables. Looping over a quoted literal string bypasses field splitting:

```bash theme={null}
#!/usr/bin/env bash
IFS=":"
for element in "one:two:three"; do
  echo "${element} is a value"
done
```

Output:

```text theme={null}
one:two:three is a value
```

Because there’s no variable expansion, `IFS` has no effect.

## Interactive IFS Changes

You can also reassign `IFS` directly in your interactive shell session:

```bash theme={null}
$ IFS=","
$ val="apple,banana,cherry"
$ set -- ${val}
$ echo $1
apple
$ echo $2
banana
$ echo $3
cherry
```

Here, `set -- ${val}` replaces the shell’s positional parameters with the split values of `val`.

## Restoring IFS and Handling Empty Strings

<Frame>
  ![The image contains two questions about IFS: "How to restore IFS to default?" and "What happens if IFS is assigned to an empty string or a null value?" It also features speech bubble icons with question marks.](https://kodekloud.com/kk-media/image/upload/v1752868627/notes-assets/images/Advanced-Bash-Scripting-ifs/ifs-questions-speech-bubbles.jpg)
</Frame>

1. **Restore IFS to default**
   ```bash theme={null}
   IFS=$' \t\n'
   ```
   This command works in Bash, Zsh, and KornShell. Older shells might require specialized syntax.

2. **Set IFS to an empty string**
   ```bash theme={null}
   IFS=''
   ```
   When `IFS` is empty, no field splitting occurs—every expansion remains as a single, unsplit string.

## References

* [Bash Manual: Special Parameters](https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html#Special-Parameters)
* [POSIX Shell Syntax](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
* [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/7ff1ccc1-5a14-41fc-817c-c0ec4a100231/lesson/f295e8ce-bbc4-4717-b5e4-42e67f188b01" />
</CardGroup>
