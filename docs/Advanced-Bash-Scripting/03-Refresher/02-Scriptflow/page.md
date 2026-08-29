# Invoke the function twice
echo_function
echo_function
```

Using functions improves readability, maintainability, and testability of your scripts.

## Error Handling and Exit Codes

Reliable scripts must report success or failure at each step. Imagine dropping off two kids at school: if one is absent due to illness, you must report that accurately to avoid confusion. The same principle applies in scripting—if a directory creation fails, your script should exit immediately rather than allowing downstream errors.

![The image shows a neon outline of a laptop with code brackets on the screen and an error message with a warning icon next to it.](https://kodekloud.com/kk-media/image/upload/v1752868599/notes-assets/images/Advanced-Bash-Scripting-Overview/neon-laptop-code-error-message.jpg)

Here are two common techniques:

* Use `set -e` at the top of your script to exit on any error.
* Check the exit status of critical commands explicitly:

  ```bash theme={null}
  mkdir /important/dir
  if [[ $? -ne 0 ]]; then
      echo "Failed to create /important/dir" >&2
      exit 1
  fi
  ```

> **triangle-alert** Always validate results of filesystem operations and external commands. Unhandled failures can cascade into bigger incidents.

***

With these principles—shebang usage, script lifecycle, imperative and functional structures, and robust error handling—you’re ready to write and maintain high-quality Bash scripts. See you in the next lesson!

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/397a2175-a186-4a6d-916e-d688c8def203/lesson/3416f32c-fca6-4a44-bd54-e2d1cf711c08)


# Scriptflow

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Refresher/Scriptflow/page

Mastering shell script execution flow using control constructs like conditionals, loops, sourcing files, and functions for reliable Bash scripting.

Understanding and controlling your shell script’s execution path is crucial for writing reliable Bash scripts. By default, a script runs sequentially, but you can alter this sequence using control constructs such as conditionals, loops, sourcing files, and functions. These tools allow you to:

* Run commands only if specific conditions are met
* Repeat commands multiple times with varying inputs

![The image shows a diagram labeled "Scriptflow" with lines of code on the left and two checkboxes on the right, indicating features for executing commands based on conditions and executing the same commands multiple times.](https://kodekloud.com/kk-media/image/upload/v1752868600/notes-assets/images/Advanced-Bash-Scripting-Scriptflow/scriptflow-diagram-code-checkboxes.jpg)

## A Real-World Analogy: Buying a Movie Ticket

Imagine you walk up to a theater ticket booth. If you hand over a valid ticket, you enter; if not, you’re turned away. This decision-making process mirrors how an `if` statement in Bash evaluates conditions and branches accordingly.

![The image depicts a flowchart with tickets leading to smiley faces, indicating approval or rejection, and then to a camera icon, suggesting a process related to film or video production.](https://kodekloud.com/kk-media/image/upload/v1752868602/notes-assets/images/Advanced-Bash-Scripting-Scriptflow/flowchart-tickets-smiley-camera.jpg)

## A Factory Analogy for Complex Workflows

Consider a widget factory where each item travels along a conveyor. At an inspection station, defective widgets are removed while good ones proceed to the next stage. This inspection step functions like a control construct in your script, deciding whether data moves forward or is handled differently.

![The image shows a dark interface with the word "Scriptflow" at the top and a graphic of a robotic arm above a conveyor belt with a green checkmark. It appears to be related to automation or workflow processes.](https://kodekloud.com/kk-media/image/upload/v1752868602/notes-assets/images/Advanced-Bash-Scripting-Scriptflow/scriptflow-robotic-arm-automation.jpg)

![The image shows a stylized illustration of a robotic arm over a conveyor belt with a wrench and screwdriver icon above it, set against a dark background. The word "Scriptflow" is displayed at the top.](https://kodekloud.com/kk-media/image/upload/v1752868604/notes-assets/images/Advanced-Bash-Scripting-Scriptflow/robotic-arm-conveyor-belt-scriptflow.jpg)

## Key Constructs That Alter Scriptflow

Shell scripts use these four core constructs to modify the default linear execution:

| Construct                      | Purpose                                       | Example Syntax                 |
| ------------------------------ | --------------------------------------------- | ------------------------------ |
| Conditional (`if`, `case`)     | Branch logic based on conditions              | `if [[ $x -gt 5 ]]; then … fi` |
| Loop (`for`, `while`, `until`) | Repeat code blocks until a condition changes  | `for i in {1..3}; do … done`   |
| Sourcing External Files        | Include and execute another script at runtime | `source config.sh`             |
| Function                       | Encapsulate and reuse code segments           | `my_func() { echo "Hi"; }`     |

![The image shows a diagram labeled "Scriptflow," featuring a block of multicolored lines resembling code, with arrows pointing to the right. It appears to represent a process or workflow related to scripting or programming.](https://kodekloud.com/kk-media/image/upload/v1752868605/notes-assets/images/Advanced-Bash-Scripting-Scriptflow/scriptflow-workflow-diagram.jpg)

***

## Conditional Statements

### `if` Statement

Bash’s `[[ … ]]` test command provides richer conditional checks than `[ … ]`:

```bash theme={null}
#!/usr/bin/env bash
