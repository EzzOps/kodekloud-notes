# Determine script directory
work_dir=$(dirname "$(readlink -f "${0}")")
food_places="${work_dir}/food_places.txt"

# Exit codes
readonly FILE_NOT_FOUND=150
readonly NO_OPTIONS_LEFT=180

terminate() {
  local msg="$1"
  local code="${2:-$FILE_NOT_FOUND}"
  echo "$msg" >&2
  exit "$code"
}

# Guard clause
if [[ ! -f "$food_places" ]]; then
  terminate "Error: food_places.txt file doesn't exist" "$FILE_NOT_FOUND"
fi
```

***

## 3. Load and Validate the Array

Populate `lunch_options` and ensure it’s not empty:

```bash theme={null}
fillout_array() {
  mapfile -t lunch_options < "$food_places"
  if [[ ${#lunch_options[@]} -eq 0 ]]; then
    terminate "Error: No food options left. Please add options to food_places.txt" "$NO_OPTIONS_LEFT"
  fi
}

fillout_array
```

***

## 4. Select and Display a Random Option

Choose a random index, echo it, and remove from the in-memory list:

```bash theme={null}
index=$(( RANDOM % ${#lunch_options[@]} ))
chosen="${lunch_options[$index]}"
echo "$chosen"

# Remove the selected element
unset 'lunch_options[index]'
```

***

## 5. Persist the Updated List

Write the remaining entries back to `food_places.txt`:

```bash theme={null}
update_options() {
  if [[ ${#lunch_options[@]} -eq 0 ]]; then
    # Empty the file when no items remain
    : > "$food_places"
  else
    printf "%s\n" "${lunch_options[@]}" > "$food_places"
  fi
}

update_options
```

***

## 6. Complete Script

Here’s the full `lunch_selector.sh`. Don’t forget to make it executable:

```bash theme={null}
#!/usr/bin/env bash
declare -a lunch_options

work_dir=$(dirname "$(readlink -f "${0}")")
food_places="${work_dir}/food_places.txt"
readonly FILE_NOT_FOUND=150
readonly NO_OPTIONS_LEFT=180

terminate() {
  local msg="$1"
  local code="${2:-$FILE_NOT_FOUND}"
  echo "$msg" >&2
  exit "$code"
}

if [[ ! -f "$food_places" ]]; then
  terminate "Error: food_places.txt file doesn't exist" "$FILE_NOT_FOUND"
fi

fillout_array() {
  mapfile -t lunch_options < "$food_places"
  if [[ ${#lunch_options[@]} -eq 0 ]]; then
    terminate "Error: No food options left. Please add options to food_places.txt" "$NO_OPTIONS_LEFT"
  fi
}

fillout_array

index=$(( RANDOM % ${#lunch_options[@]} ))
chosen="${lunch_options[$index]}"
echo "$chosen"
unset 'lunch_options[index]'

update_options() {
  if [[ ${#lunch_options[@]} -eq 0 ]]; then
    : > "$food_places"
  else
    printf "%s\n" "${lunch_options[@]}" > "$food_places"
  fi
}

update_options
```

Make it executable and run:

```bash theme={null}
chmod +x lunch_selector.sh
./lunch_selector.sh
```

Each run prints a random, non-repeating lunch spot until the list is empty.

***

## References

* [GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/)
* [Bash FAQ](https://tiswww.case.edu/php/chet/bash/FAQ)
* [Using `mapfile` in Bash (StackOverflow)](https://stackoverflow.com/questions/tagged/bash)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/df27d5e6-23c2-4e4e-9163-4dd73f639282/lesson/4750796e-0747-49d0-bdae-20bf2fcf4374)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/df27d5e6-23c2-4e4e-9163-4dd73f639282/lesson/2a6a85bf-c161-4efb-ae2e-8bfe8fb63f61)


# Arrays

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Arrays/Arrays/page

This article explains how to declare, access, and effectively use arrays in Bash scripting.

Arrays in Bash empower you to store multiple values in an indexed collection, offering direct access to any element—first, middle, or last—by its index. This is analogous to reaching into a specific drawer when you know exactly where your socks are kept, rather than inspecting each one sequentially.

![The image illustrates the concept of arrays using a drawer analogy, showing three drawers labeled 1, 2, and 3 on the left, and an array with indices 0, 1, and 2 on the right.](https://kodekloud.com/kk-media/image/upload/v1752868541/notes-assets/images/Advanced-Bash-Scripting-Arrays/arrays-drawer-analogy-diagram.jpg)

> **lightbulb** Bash arrays are **zero-indexed**: the first element is at index `0`, the second at `1`, and so on.

## Why Use Arrays?

* **Direct element access** reduces loops and conditional checks.
* **Cleaner scripts** when handling lists of servers, filenames, or configurations.
* **Improved performance** versus string-based lists requiring manual parsing.

Compare a string-based iteration:

```bash theme={null}
#!/usr/bin/env bash

servers="server1 server2 server3"
for server in ${servers}; do
  if [[ "$server" == "server2" ]]; then
    server="${server}.kodekloud.com"
  fi
  echo "$server"
done
```

Output:

```bash theme={null}
server1
server2.kodekloud.com
server3
```

This checks every item, akin to opening each drawer until you find your socks. Arrays eliminate that overhead.

***

## Declaring Arrays

### 1. Assigning by Index

```bash theme={null}
#!/usr/bin/env bash

course_sections[0]="Introduction"
course_sections[1]="Coding Standards"
course_sections[2]="Refresher"

echo "${course_sections[0]}"   # Introduction
echo "${course_sections[1]}"   # Coding Standards
echo "${course_sections[2]}"   # Refresher
```

<Frame>
  ![The image illustrates an array with three indexed elements (0, 1, 2), highlighting the second element (index 1) as "server\[1\]".](https://kodekloud.com/kk-media/image/upload/v1752868542/notes-assets/images/Advanced-Bash-Scripting-Arrays/array-indexed-elements-server1.jpg)
</Frame>

### 2. Inline Initialization

```bash theme={null}
#!/usr/bin/env bash

declare -a course_sections=("Introduction" "Coding Standards" "Refresher")
echo "${course_sections[@]}"   # Introduction Coding Standards Refresher
```

You can also omit `declare -a`:

```bash theme={null}
course_sections=("Intro" "Middle" "End")
```

***

## Accessing Array Elements

| Operation          | Syntax                     | Example Output                             |
| ------------------ | -------------------------- | ------------------------------------------ |
| Single element     | `${array[index]}`          | `${course_sections[1]}` → Coding Standards |
| All elements       | `${array[@]}`              | `${course_sections[@]}` → all items        |
| Number of elements | `${#array[@]}`             | count of items                             |
| All indices (keys) | `${!array[@]}`             | list of valid indices                      |
| Slice              | `${array[@]:start:length}` | subset of elements                         |

### Get All Elements

```bash theme={null}
#!/usr/bin/env bash

sections=("Intro" "Body" "Conclusion")
echo "${sections[@]}"  # Intro Body Conclusion
```

***

## Quoting Arrays: Preserve Whitespace

Unquoted expansions split on spaces:

```bash theme={null}
#!/usr/bin/env bash

sections=("Coding Standards" "Best Practices")
