# Append at the next free index
servers[${#servers[@]}]="server4"
echo "${servers[@]}"
```

```bash theme={null}
$ ./sample2.sh
server1 server2 server3 server4
```

![The image shows a sequence of labeled items, "index0" to "index3" and "server1" to "server4," with a focus on inserting "index2" and "server3" into the sequence.](https://kodekloud.com/kk-media/image/upload/v1752868548/notes-assets/images/Advanced-Bash-Scripting-Insert/index-sequence-insertion-server3.jpg)

This method automatically calculates the correct index to append, preventing accidental overwrites.

***

## Replacing Elements at a Specific Index

To overwrite an existing element, assign a new value to that index:

![The image explains that inserting an element into an existing index of an array replaces the current value at that index.](https://kodekloud.com/kk-media/image/upload/v1752868548/notes-assets/images/Advanced-Bash-Scripting-Insert/array-insert-replace-index-explanation.jpg)

```bash theme={null}
#!/usr/bin/env bash

declare -a servers=("server1" "server2" "server3")
servers[1]="serverx"
echo "${servers[@]}"
```

```bash theme={null}
$ ./array-manipulation3.sh
server1 serverx server3
```

### Warning: Scalar vs Array Assignment

If you omit the index brackets, Bash treats the assignment as a scalar, modifying index 0:

```bash theme={null}
#!/usr/bin/env bash

declare -a servers=("server1" "server2" "server3")
servers="replaced value"
echo "${servers[@]}"
```

```bash theme={null}
$ ./array-manipulation4.sh
replaced value server2 server3
```

***

## Inserting Elements in the Middle

To insert an element at a specific position and automatically shift the rest, use array slicing:

```bash theme={null}
#!/usr/bin/env bash

declare -a servers=("server1" "server2" "server3")

# Insert "server1.5" at index 1
servers=(
  "${servers[@]:0:1}"
  "server1.5"
  "${servers[@]:1}"
)

echo "${servers[@]}"
```

```bash theme={null}
$ ./array-manipulation2.sh
server1 server1.5 server2 server3
```

Slicing breakdown:

* `${servers[@]:0:1}` → elements up to (but not including) the insertion point
* `"server1.5"` → new element
* `${servers[@]:1}` → remaining elements from index 1 onward

***

## Method Comparison

| Method                  | Description                               | Example                                                   |
| ----------------------- | ----------------------------------------- | --------------------------------------------------------- |
| Manual Indexing         | Explicit index assignment; error-prone    | `servers[3]="server4"`                                    |
| Parameter Expansion     | Append at next free index                 | `servers[${#servers[@]}]="server4"`                       |
| Array Slicing           | Insert at arbitrary position              | `servers=( "${servers[@]:0:i}" "new" "${servers[@]:i}" )` |
| Direct Variable Assign. | Scalar assignment to index 0 (unexpected) | `servers="replaced value"`                                |

***

## Links & References

* [Bash Reference Manual](https://www.gnu.org/software/bash/manual/)
* [Bash Scripting Best Practices](https://tldp.org/LDP/abs/html/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) (for scripting in cloud-native environments)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/df27d5e6-23c2-4e4e-9163-4dd73f639282/lesson/0cb3ab22-b9d5-44a4-aaaa-d9084a9dd8cf)


# Remove

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Arrays/Remove/page

Learn to manage Bash arrays by removing specific elements and clearing all elements in one command.

In this lesson, you’ll learn two key operations for managing Bash arrays:

1. Removing a specific element by its index
2. Clearing all elements in one command

![The image is a slide titled "Arrays remove," showing two checked items: "How to remove a specific element from an array" and "How to remove all of the elements from an array in one shot."](https://kodekloud.com/kk-media/image/upload/v1752868550/notes-assets/images/Advanced-Bash-Scripting-Remove/arrays-remove-element-diagram.jpg)

## Removing a Specific Element by Index

To delete a single entry in a Bash array, use `unset` with the array name and the target index:

```bash theme={null}
#!/usr/bin/env bash
declare -a servers=("server1" "server2" "server3")
unset 'servers[1]'
echo "Remaining elements: ${servers[@]}"
```

Running this script produces:

```bash theme={null}
$ ./removing.sh
server1 server3
```

> **lightbulb** Bash does not reindex arrays after removal. The original indices remain, leaving gaps in the sequence.

To view both values and their indices after deletion:

```bash theme={null}
#!/usr/bin/env bash
declare -a servers=("server1" "server2" "server3")
unset 'servers[1]'
echo "Values : ${servers[@]}"
echo "Indices: ${!servers[@]}"
```

```bash theme={null}
$ ./removing_indices.sh
Values : server1 server3
Indices: 0 2
```

## Clearing All Elements

If you need to empty an array completely, omit the brackets when using `unset`:

```bash theme={null}
#!/usr/bin/env bash
declare -a servers=("server1" "server2" "server3")
unset servers
echo "After clearing: ${servers[@]}"
```

```bash theme={null}
$ ./removing_all.sh
```

No output appears because the array has been removed.

> **triangle-alert** Using `unset array` deletes the entire variable. You must redeclare it before adding new elements.

## Summary of Removal Operations

| Operation          | Command Usage          | Result                                |
| ------------------ | ---------------------- | ------------------------------------- |
| Remove by index    | `unset 'array[index]'` | Deletes the specified element only    |
| Clear entire array | `unset array`          | Removes all elements and the variable |

## Links and References

* [Bash Array Basics](https://www.gnu.org/software/bash/manual/html_node/Arrays.html)
* [Shell Parameter Expansion](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html)
* [Bash Scripting Guide](https://tldp.org/LDP/abs/html/)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/df27d5e6-23c2-4e4e-9163-4dd73f639282/lesson/9a3bfc72-8ba1-41bc-9011-fe3f2980b4c4)
