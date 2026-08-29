# String assignment
name="John Doe"
echo "$name"   # John Doe

# Integer assignment
count=10
echo "$count"  # 10
```

### Dynamically Typed Variables

Bash determines the type at runtime, based on context:

```bash theme={null}
#!/usr/bin/env bash
var="10"
echo $(( var + 1 ))   # 11
```

You can even switch types on the fly:

```bash theme={null}
#!/usr/bin/env bash
i="42"
echo $(( i + 8 ))   # 50

i="hello"
echo "$i"           # hello
```

> **lightbulb** Bash’s dynamic typing means it tries to interpret values at runtime—no compile-time errors for type mismatches.

## Enforcing Integer Types with `declare -i`

To enforce integer semantics (mimicking static typing), use:

```bash theme={null}
#!/usr/bin/env bash
declare -i num=5
echo $(( num + 2 ))   # 7

num="not a number"
echo "$num"           # 0
```

Non-numeric assignments reset the variable to `0`.

## Other `declare` Flags

Here’s a quick reference for some common attributes:

| Flag | Description                | Example                             |
| ---- | -------------------------- | ----------------------------------- |
| -i   | Force integer              | `declare -i counter=100`            |
| -r   | Read-only variable         | `declare -r PI=3.1415`              |
| -u   | Convert value to uppercase | `declare -u animal="dog"` → `DOG`   |
| -l   | Convert value to lowercase | `declare -l word="HELLO"` → `hello` |

### Read-Only Variables (`-r`)

```bash theme={null}
#!/usr/bin/env bash
declare -r VERSION="1.0.0"
echo "$VERSION"
VERSION="2.0.0"  # Error: readonly variable
```

> **triangle-alert** Attempting to modify a `readonly` variable will terminate your script with an error.

### Case Conversion (`-u`, `-l`)

```bash theme={null}
#!/usr/bin/env bash
declare -u upper
declare -l lower

upper="Bash Rocks"
lower="Bash Rocks"

echo "$upper"  # BASH ROCKS
echo "$lower"  # bash rocks
```

## Arrays with `declare -a`

Bash supports both indexed and associative arrays:

```bash theme={null}
#!/usr/bin/env bash

# Indexed array
declare -a fruits=("apple" "banana" "cherry")
echo "${fruits[1]}"    # banana

# Associative array
declare -A colors
colors[sky]=blue
colors[rose]=red
echo "${colors[rose]}" # red
```

| Array Type        | Declaration      | Access          |
| ----------------- | ---------------- | --------------- |
| Indexed Array     | `declare -a arr` | `${arr[index]}` |
| Associative Array | `declare -A map` | `${map[key]}`   |

## Links and References

* [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)
* [KornShell `typeset` Documentation](https://www.kornshell.com/doc/sections/toc.html)
* [GNU Bash Features](https://www.gnu.org/software/bash/)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/df27d5e6-23c2-4e4e-9163-4dd73f639282/lesson/2f42b8d5-73da-4a1f-901e-08b6ca0ce20d)


# Insert

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Arrays/Insert/page

Learn to manage Bash arrays by adding, replacing, and inserting elements for more powerful and flexible scripts.

In this lesson, you’ll learn how to efficiently manage Bash arrays by adding, replacing, and inserting elements. Bash arrays allow you to store ordered lists of values, making scripts more powerful and flexible.

## Table of Contents

1. [Adding Elements Manually](#adding-elements-manually)
2. [Efficient Appending via Parameter Expansion](#efficient-appending-via-parameter-expansion)
3. [Replacing Elements at a Specific Index](#replacing-elements-at-a-specific-index)
4. [Inserting Elements in the Middle](#inserting-elements-in-the-middle)
5. [Method Comparison](#method-comparison)
6. [Links & References](#links--references)

***

## Adding Elements Manually

You can append items by specifying the next index directly. This approach works but requires you to know or calculate the current array length:

```bash theme={null}
#!/usr/bin/env bash

course_sections=("Introduction" "Coding Standards" "Refresher")
course_sections[3]="Streams"
echo "${course_sections[@]}"
```

```bash theme={null}
$ ./declare7.sh
Introduction Coding Standards Refresher Streams
```

Example with a `servers` array:

```bash theme={null}
#!/usr/bin/env bash

declare -a servers=("server1" "server2" "server3")
servers[3]="server4"
echo "${servers[@]}"
```

```bash theme={null}
$ ./adding.sh
server1 server2 server3 server4
```

> **lightbulb** Manually counting indices can lead to errors in larger scripts. Consider using parameter expansion to automate index calculation.

***

## Efficient Appending via Parameter Expansion

Bash provides `${#array[@]}` to retrieve the current number of elements. Since arrays are zero-indexed, this value equals the next available index:

```bash theme={null}
#!/usr/bin/env bash

declare -a servers=("server1" "server2" "server3")
