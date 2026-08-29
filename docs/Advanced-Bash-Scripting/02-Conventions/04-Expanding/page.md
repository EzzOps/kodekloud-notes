# Append three more elements
array+=("Four" "Five" "Six")
echo "After appending: ${array[@]}"
```

Save this as `example2.sh` and run:

```bash theme={null}
$ chmod +x example2.sh
$ ./example2.sh
Original array: One Two Three
After appending: One Two Three Four Five Six
```

## 2. Sorting an Array with `printf` & `sort`

Bash doesn’t have a built-in array sort, but you can leverage the Unix `sort` command. Since `sort` expects one item per line, use `printf` to split space-separated elements:

> **lightbulb** Do not enclose each item in quotes (e.g., `"a"` `"b"`), or `printf` will treat them as single arguments and won't split them into lines.

```bash theme={null}
# Example: sorting letters
printf "%s\n" d a g h i f | sort
```

Output:

```plain theme={null}
a
d
f
g
h
i
```

You can apply the same method to numeric arrays:

```bash theme={null}
#!/usr/bin/env bash
declare -a nums=(4 2 0 6 8 1)

# Print each element on its own line and pipe to sort
printf "%s\n" "${nums[@]}" | sort
```

Running `sort_numbers.sh`:

```bash theme={null}
$ chmod +x sort_numbers.sh
$ ./sort_numbers.sh
0
1
2
4
6
8
```

## 3. Displaying Unsorted and Sorted Arrays

To compare the original and sorted array side by side, capture the sorted output in a new array via command substitution:

```bash theme={null}
#!/usr/bin/env bash
declare -a nums=(4 2 0 6 8 1)

# Display the unsorted array
echo "Unsorted array: ${nums[@]}"

# Sort and capture in a new array
sorted_nums=($(printf "%s\n" "${nums[@]}" | sort))

# Display the sorted array
echo "Sorted array: ${sorted_nums[@]}"
```

Running `sort_ex2.sh` produces:

```bash theme={null}
$ chmod +x sort_ex2.sh
$ ./sort_ex2.sh
Unsorted array: 4 2 0 6 8 1
Sorted array: 0 1 2 4 6 8
```

![The image shows a comparison between an unsorted array (4, 2, 0, 6, 8, 1) and its sorted version (0, 1, 2, 4, 6, 8) with a lightbulb icon above.](https://kodekloud.com/kk-media/image/upload/v1752868551/notes-assets/images/Advanced-Bash-Scripting-Sort/array-sorting-comparison-lightbulb.jpg)

## Summary

| Task                  | Command Example                                     |
| --------------------- | --------------------------------------------------- |
| Append elements       | `array+=("item1" "item2")`                          |
| Sort an array         | `printf "%s\n" "${array[@]}" \| sort`               |
| Capture sorted output | `sorted=( $(printf "%s\n" "${array[@]}" \| sort) )` |

## Links and References

* [Bash Arrays (GNU Bash Manual)](https://www.gnu.org/software/bash/manual/html_node/Arrays.html)
* [sort — Unix manual page](https://man7.org/linux/man-pages/man1/sort.1.html)
* [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/df27d5e6-23c2-4e4e-9163-4dd73f639282/lesson/59f7d166-3e53-489f-b821-c37ec3de7898)


# Expanding

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Conventions/Expanding/page

This article explains variable expansion in shell scripting, including usage of braces, quoting, and best practices for handling variables.

In shell scripting, variable expansion uses the dollar sign (`$`) to tell the shell to replace the variable name with its stored value.

```bash theme={null}
#!/bin/bash
var="value of var"
echo ${var}
```

Running this script:

```bash theme={null}
$ ./var-sample.sh
value of var
```

## Braces vs No Braces

You can reference variables with or without braces. Braces become essential when you append characters immediately after the variable name.

### With Braces

```bash theme={null}
#!/bin/bash
var="value of var"
echo ${var}
```

### Without Braces

```bash theme={null}
#!/bin/bash
var="value of var"
echo $var
```

Both scripts output:

```bash theme={null}
$ ./var-sample.sh
value of var
```

### Delimiting Variable Names

Without braces, the shell cannot determine where the variable name ends:

```bash theme={null}
#!/bin/bash
height=170
