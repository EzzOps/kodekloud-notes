# Generates A, B, C
echo {A,B,C}

# Generates numbers 1 through 5
echo {1..5}
```

> **lightbulb** Brace expansions must not be quoted for the shell to recognize them. For example, `echo "{A,B}"` will literally output `{A,B}`.

***

## 2. Parameter Expansion

Parameter expansion lets you inspect or transform variable values without invoking external commands.

### Basic Variable Expansion

```bash theme={null}
USER_HOME=$HOME
echo "Your home directory is: $USER_HOME"
```

### Removing Directory Components

To strip the longest matching prefix (e.g., remove everything up to the last slash), use `##*/`:

```bash theme={null}
#!/usr/bin/env bash

some_script="/usr/bin/my_script.sh"
# Remove the longest match of '*/' from the front
echo "${some_script##*/}"
```

Output:

```bash theme={null}
$ ./expansions.sh
my_script.sh
```

> **triangle-alert** Always quote your expansions (e.g., `"${var}"`) to prevent word splitting and globbing in unexpected ways.

***

## 3. Command Substitution

Command substitution captures the stdout of a command and embeds it in another command’s arguments:

```bash theme={null}
current_date=$(date +%Y-%m-%d)
echo "Today is $current_date"
```

***

## 4. Filename Generation (Globbing)

Globbing uses wildcard patterns to match filenames:

```bash theme={null}
# List all .log files
ls *.log

# Recursive match in subdirectories (with Bash extglob)
shopt -s globstar
echo **/*.md
```

***

## Next Steps

Now that you’ve seen the major shell expansions, try combining them to simplify your scripts—generate file lists, parse log entries, or batch-rename files with a single command.

For more examples and edge cases, consult the [GNU Bash Reference Manual][bash-expansion].

```markdown theme={null}

<Card title="Watch Video" icon="video" cta="Learn more" href="https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/0e090d75-12b5-4e0f-ace8-519f11d7b5d2/lesson/017ed46b-54db-44fc-a839-6627eec48490"/>
```


# Parameter Part One

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Expansions-Part-One/Parameter-Part-One/page

This article explains Bash parameter expansion for transforming variable values, focusing on removing prefixes and suffixes from strings.

In Bash scripting, parameter expansion lets you transform variable values using patterns inside `${}`. Previously, we replaced “file.txt” with “data” in a path:

```bash theme={null}
#!/usr/bin/env bash
path="/home/user/file.txt"
echo "${path/file.txt/data}"
