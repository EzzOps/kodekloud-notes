# Arrays demo

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Arrays/Arrays-demo/page

This tutorial explains how to create a Bash script that randomly selects a lunch spot from a list without repeats.

In this tutorial, we’ll build a Bash script that picks a random lunch spot from a list—without repeats—by combining indexed arrays and simple file-based persistence. This pattern is perfect for one-time draws, rotating duties, or any scenario where you want to consume items until the list is exhausted.

Imagine a team of 20 colleagues who vote on their favorite restaurants each Friday. Everyone adds their go-to spot to an array. The script then:

* Reads the list into memory
* Selects a random entry
* Displays it
* Removes it from both memory and disk
* Exits with an error if the list is missing or empty

## Why In-Memory vs Persistent Storage?

1. Manipulating data in memory means changes disappear once the script ends.

![The image is a slide titled "Arrays demo" that explains "manipulating data in-memory," referring to initializing or modifying values directly in variables within a script or program.](../../../../images/kodekloud.com/kk-media/image/upload/v1752868537/notes-assets/images/Advanced-Bash-Scripting-Arrays-demo/arrays-demo-manipulating-data.jpg)

2. Persistent storage (files, databases) retains data between runs.

![The image is a diagram titled "Arrays demo" that explains the concept of a persistent storage method, which retains data after restarting an application or rebooting a machine, with icons representing databases and files.](../../../../images/kodekloud.com/kk-media/image/upload/v1752868538/notes-assets/images/Advanced-Bash-Scripting-Arrays-demo/arrays-demo-persistent-storage-diagram.jpg)

> **lightbulb** This script uses Bash 4.0+ for the `mapfile` builtin.

## Key Bash Features

* **mapfile -t**: Loads lines from a file (or stdin) into an array.

![The image is a slide titled "Arrays demo" that describes the shell built-in command "mapfile," which reads input data and stores it in an array format, available from bash 4.0 onwards.](../../../../images/kodekloud.com/kk-media/image/upload/v1752868539/notes-assets/images/Advanced-Bash-Scripting-Arrays-demo/arrays-demo-mapfile-bash-command.jpg)

* **\$RANDOM**: Yields a pseudo-random integer between 0 and 32767.

![The image is a slide from an "Arrays demo" presentation, describing a special shell variable "RANDOM" that generates a random integer between 0 and 32767.](../../../../images/kodekloud.com/kk-media/image/upload/v1752868540/notes-assets/images/Advanced-Bash-Scripting-Arrays-demo/arrays-demo-random-variable.jpg)

### Exit Code Reference

| Exit Code               | Condition                              |
| ----------------------- | -------------------------------------- |
| 150 (`FILE_NOT_FOUND`)  | `food_places.txt` is missing           |
| 180 (`NO_OPTIONS_LEFT`) | No entries remain in `food_places.txt` |

***

## 1. Prepare the Data File

Create `food_places.txt` with initial entries:

```bash theme={null}
cat <<EOF > food_places.txt
Ramen
Sushi
Tacos
Dal makhani
EOF
```

***

## 2. Initialize the Script

Create `lunch_selector.sh`:

```bash theme={null}
#!/usr/bin/env bash
declare -a lunch_options
