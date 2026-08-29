# Add more contacts
email_addresses["Andy"]="andy@email.com"
email_addresses["Rajasekar"]="rajasekar@email.com"

echo "${email_addresses[@]}"
```

```bash theme={null}
$ ./email-3.sh
mark@email.com rajasekar@email.com ...
```

> **lightbulb** Associative arrays are **unordered**; iteration order can vary.

![The image is a slide about associative arrays, highlighting that they do not consider the order in which elements are stored.](https://kodekloud.com/kk-media/image/upload/v1752868544/notes-assets/images/Advanced-Bash-Scripting-Associative/associative-arrays-order-slide.jpg)

## Replacing a Value

Overwrite an existing key to update its value:

```bash theme={null}
#!/usr/bin/env bash
declare -A email_addresses=(
  ["Mark"]="mark@email.com"
  ["Kriti"]="kriti@email.com"
  ["Feng"]="feng@email.com"
  ["Rajasekar"]="rajasekar@email.com"
)

echo "Before: ${email_addresses[@]}"
email_addresses["Feng"]="feng2@email.com"
echo "After:  ${email_addresses[@]}"
```

```bash theme={null}
$ ./email-4.sh
Before: kriti@email.com ...
After:  kriti@email.com ... feng2@email.com
```

## Removing Elements

Use `unset` to delete by key or clear the entire array:

```bash theme={null}
#!/usr/bin/env bash
declare -A email_addresses=( ... )

# Remove one element
unset email_addresses["Kriti"]

# Remove all elements
unset email_addresses
```

## Listing Keys vs. Values

* **Keys:** `${!array[@]}`
* **Values:** `${array[@]}`

```bash theme={null}
#!/usr/bin/env bash
declare -A email_addresses=( ... )

echo "Keys:   ${!email_addresses[@]}"
echo "Values: ${email_addresses[@]}"
```

## Iterating with a `for` Loop

Loop through keys and access each value:

```bash theme={null}
#!/usr/bin/env bash
declare -A email_addresses=( ... )

for key in "${!email_addresses[@]}"; do
  echo "$key's email is ${email_addresses[$key]}"
done
```

```bash theme={null}
$ ./email-8.sh
Kriti's email is kriti@email.com
...
```

Enclose `"${!email_addresses[@]}"` in quotes to handle multi-word keys correctly.

***

## Links and References

* [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)
* [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/df27d5e6-23c2-4e4e-9163-4dd73f639282/lesson/3f0d2055-d115-442d-a39e-d064d0576cf2)


# Declare

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Arrays/Declare/page

This article explains the `declare` command in Bash for assigning variable attributes and data types, including arrays and type enforcement.

The `declare` (also known as `typeset`) built-in in Bash lets you assign attributes and data types to your variables. While Bash is dynamically typed, using `declare` can help enforce types (like integers), create read-only variables, and define arrays.

In this article, we'll cover:

* Data types in Bash
* Dynamically typed variables
* Enforcing integer types with `declare -i`
* Other useful `declare` flags
* Working with arrays using `declare -a`

![The image features a list of programming-related topics with checkmarks, including explaining data types, dynamically typed syntax, the declare command in Bash, and using declare for arrays. It also includes simple line drawings of a person and a lightbulb.](https://kodekloud.com/kk-media/image/upload/v1752868546/notes-assets/images/Advanced-Bash-Scripting-Declare/programming-topics-checklist-drawing.jpg)

## Data Types in Bash

Bash offers two fundamental data types:

1. **String**
2. **Integer**

![The image shows a split screen with "String" labeled as 1 on the left and "Integer" labeled as 2 on the right, under the title "arrays-declare."](https://kodekloud.com/kk-media/image/upload/v1752868547/notes-assets/images/Advanced-Bash-Scripting-Declare/arrays-declare-string-integer.jpg)

You can assign values using the typical syntax:

```bash theme={null}
