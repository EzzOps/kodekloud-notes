# Output: /home/user/data
```

In this lesson, we’ll focus on pattern matching and how to remove prefixes and suffixes from strings using Bash parameter expansion.

## Patterns in Bash

A *pattern* is a sequence of characters recognized by the shell for matching or substitution. You’ll find patterns in file globbing (e.g., `*.txt`), text processing, and data validation. In Bash, patterns power parameter expansion, letting you transform variable content without external tools.

## Variable Expansion vs. Parameter Expansion

By default, `${var}` simply expands to its value:

```bash theme={null}
name="John Doe"
echo "Hello, ${name}"
# Hello, John Doe
```

When you include operators like `#` or `%` inside the braces, Bash invokes parameter expansion, applying pattern-based modifications to the variable’s value.

<Callout icon="lightbulb">
  Always enclose the expression in double quotes (`"${...}"`) to preserve spaces and prevent word splitting.
</Callout>

## Removing Prefixes and Suffixes

Bash supports removing the *shortest* matching prefix or suffix from a string with `${var#pattern}` and `${var%pattern}`.

### Understanding Prefix and Suffix

Consider these job titles in an IT company:

<Frame>
  ![The image lists different engineering job titles: Mid DevOps Engineer, Jr. Software Engineer, Sr. DevOps Engineer, and Associate DevOps Engineer, alongside an icon of a briefcase with a magnifying glass.](https://kodekloud.com/kk-media/image/upload/v1752868556/notes-assets/images/Advanced-Bash-Scripting-Parameter-Part-One/engineering-job-titles-briefcase-icon.jpg)
</Frame>

* Prefixes (associate, senior, junior, mid) indicate tenure or level.
* The suffix (`Engineer`) indicates the job field.

### Prefix Removal with

The `#` operator deletes the shortest matching pattern from the *start* of the string:

<Frame>
  ![The image illustrates the concept of "Parameter Expansions" with a focus on removing a prefix, represented by a hashtag symbol and scissors icon.](https://kodekloud.com/kk-media/image/upload/v1752868557/notes-assets/images/Advanced-Bash-Scripting-Parameter-Part-One/parameter-expansions-remove-prefix.jpg)
</Frame>

Example 1: Remove the leading `H`:

```bash theme={null}
greetings="Hello World"
echo "${greetings#H}"
# Output: ello World
```

If the pattern isn't found at the beginning, the value remains unchanged:

```bash theme={null}
echo "${greetings#e}"
# Output: Hello World
```

Example 2: Remove the word “Hello ” (including the space):

```bash theme={null}
echo "${greetings#Hello }"
# Output: World
```

Patterns are case-sensitive: `"h"` won’t match `"H"`.

```bash theme={null}
echo "${greetings#h}"
# Output: Hello World
```

### Suffix Removal with %

The `%` operator removes the shortest matching pattern from the *end* of the string:

Example 1: Drop the trailing `d`:

```bash theme={null}
echo "${greetings%d}"
# Output: Hello Worl
```

Example 2: Remove “rld” at the end:

```bash theme={null}
echo "${greetings%rld}"
# Output: Hello Wo
```

If the suffix doesn't match exactly, the string stays the same:

```bash theme={null}
echo "${greetings%world}"
# Output: Hello World
```

<Callout icon="triangle-alert">
  Pattern matching in Bash is case-sensitive. Ensure your pattern matches the exact case of the prefix or suffix.
</Callout>

## Quick Reference Table

| Operator         | Action                       | Example                         |
| ---------------- | ---------------------------- | ------------------------------- |
| `${var#pattern}` | Remove shortest prefix match | `${greetings#Hello }` → `World` |
| `${var%pattern}` | Remove shortest suffix match | `${greetings%rld}` → `Hello Wo` |

<Frame>
  ![The image illustrates parameter expansions, showing a blue circle with a hash symbol for "Prefix" and a red circle with a percent symbol for "Suffix."](https://kodekloud.com/kk-media/image/upload/v1752868558/notes-assets/images/Advanced-Bash-Scripting-Parameter-Part-One/parameter-expansions-prefix-suffix.jpg)
</Frame>

## Next Steps

In the next lesson, we'll explore *longest*-match removals using `##` and `%%` to strip more complex patterns.

## References

* [Bash Reference Manual: Shell Parameter Expansion](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html)
* [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/0e090d75-12b5-4e0f-ace8-519f11d7b5d2/lesson/6ce8bd94-0ac6-4398-9814-e925337bf0f0" />
</CardGroup>


# Parameter Part Two

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Expansions-Part-One/Parameter-Part-Two/page

Explores advanced parameter expansion techniques using wildcards for flexible string manipulation in Linux, focusing on file paths and extensions.

In Part One, we covered basic parameter‐expansion techniques for stripping fixed prefixes or suffixes. Here, we’ll explore more flexible patterns using wildcards to handle arbitrary extensions, path segments, or words in a string.

## Removing Fixed Prefixes and Suffixes

Often in Linux you work with file paths and extensions:

| Component | Example 1            | Example 2            | Example 3   |
| --------- | -------------------- | -------------------- | ----------- |
| Prefix    | `/home/my_username/` | `/home/my_username/` | `/usr/bin/` |
| Name      | `text_file`          | `text_file2`         | `app.py`    |
| Suffix    | `.txt`               | `.txt`               | `.py`       |

A fixed‐suffix removal like `${var%.txt}` only matches when the filename actually ends in `.txt`:

```bash theme={null}
$ var="/home/my_username/text_file.txt"
$ echo "${var%.txt}"
/home/my_username/text_file

$ var="/home/my_username/text_file2.txt"
$ echo "${var%.txt}"
/home/my_username/text_file2

$ var="/usr/bin/app.py"
$ echo "${var%.txt}"
/usr/bin/app.py
```

<Callout icon="lightbulb">
  Using `${var%.txt}` leaves `.py` files untouched. For arbitrary extensions or dynamic patterns, you’ll need wildcards.
</Callout>

***

## Using Wildcards for General Cases

By introducing `*` in the pattern, you can remove everything up to or after a delimiter (space, slash, dot, etc.).

### Strip the First Word

For a space-separated string, `${var#* }` removes the shortest match from the front (everything up to the first space):

```bash theme={null}
export position1="Senior Cloud Architect"
export position2="Senior DevOps Engineer"
export position3="Associate Frontend Engineer"
export position4="Junior Software Developer"

echo "${position1#* }"   # Cloud Architect
echo "${position2#* }"   # DevOps Engineer
echo "${position3#* }"   # Frontend Engineer
echo "${position4#* }"   # Software Developer
```

### Strip the Last Word

Using `${var% *}` removes the shortest match from the end (from the last space onward):

```bash theme={null}
echo "${position1% *}"   # Senior Cloud
echo "${position2% *}"   # Senior DevOps
echo "${position3% *}"   # Associate Frontend
echo "${position4% *}"   # Junior Software
```

<Callout icon="triangle-alert">
  Always pair `*` with a literal character (e.g., space or slash). A pattern like `${var%*}` matches the entire string, returning an empty result.
</Callout>

***

## Handling Unix‐Style Filenames

Consider two variables:

```bash theme={null}
my_text_file="/home/my_username/text_file.txt"
my_python_file="/usr/bin/app.py"
```

* **Prefix**: directory path
* **Name**: file name
* **Suffix**: extension

### Remove All Directory Components

* `${var#*/}` strips up to the *first* slash
* `${var##*/}` strips up to the *last* slash (longest‐prefix removal)

```bash theme={null}
echo "${my_text_file#*/}"    # home/my_username/text_file.txt
echo "${my_python_file#*/}"  # usr/bin/app.py

echo "${my_text_file##*/}"   # text_file.txt
echo "${my_python_file##*/}" # app.py
```

### Strip File Extension

Use shortest‐suffix (`%`) or longest‐suffix (`%%`). With a single dot, both behave identically:

```bash theme={null}
echo "${my_text_file%.*}"   # /home/my_username/text_file
echo "${my_text_file%%.*}"  # /home/my_username/text_file

echo "${my_python_file%.*}"   # /usr/bin/app
echo "${my_python_file%%.*}"  # /usr/bin/app
```

***

## Choosing the Right Operator

| Operator    | Description                  | Example                          |
| ----------- | ---------------------------- | -------------------------------- |
| `${var#…}`  | Remove shortest prefix match | Strip up to first delimiter      |
| `${var##…}` | Remove longest prefix match  | Strip up to last delimiter       |
| `${var%…}`  | Remove shortest suffix match | Remove first occurrence from end |
| `${var%%…}` | Remove longest suffix match  | Remove all occurrences from end  |

* Use **shortest‐suffix** (`%`) for extensions.
* Use **longest‐prefix** (`##`) for directory paths.

With these four operators, you can tailor string manipulations to filenames, paths, or any delimited data.

***

## Links and References

* [Bash Parameter Expansion](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Docker Hub](https://hub.docker.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/0e090d75-12b5-4e0f-ace8-519f11d7b5d2/lesson/9e19ee01-6dbe-4e13-85cc-4f2da2a4f5c6" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/0e090d75-12b5-4e0f-ace8-519f11d7b5d2/lesson/72bafe84-69d6-464b-9023-9c04224b9ae1" />
</CardGroup>
