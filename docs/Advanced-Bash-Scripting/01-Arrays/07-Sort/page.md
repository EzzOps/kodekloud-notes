# Sort

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Arrays/Sort/page

Learn to append elements to a Bash array and sort it using Unix utilities.

In this lesson, you’ll learn how to append elements to a Bash array and then sort that array using standard Unix utilities. We’ll cover:

* Appending items with the `+=` notation
* Sorting array elements by printing each one on a new line
* Capturing sorted output in a new array for easy comparison

## 1. Appending Elements with `+=`

Bash arrays support the `+=` operator to add one or more items at the end of an existing array. Here’s an example:

```bash theme={null}
#!/usr/bin/env bash
declare -a array=("One" "Two" "Three")
echo "Original array: ${array[@]}"
