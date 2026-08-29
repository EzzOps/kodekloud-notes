# Conditional Logic

Source: https://notes.kodekloud.com/docs/Shell-Scripts-for-Beginners/Flow-Control/Conditional-Logic/page

Learn to implement conditional logic in shell scripts using practical examples to control script flow based on various conditions.

In this article, you'll learn how to implement conditional logic in shell scripts. Using a practical example, we simulate a scenario where a script checks a rocket’s status. The script handles three possible responses from a command:

* "launching" when the launch is in progress
* "success" when the launch completes successfully
* "failed" when the rocket crashes

If the rocket launch fails, the script automatically runs the debugging command. This tutorial will help you understand how to structure your conditional statements to control the script's flow based on various conditions.

## How Conditional Statements Work

Shell scripting utilizes the `if` statement similarly to natural language. The condition is placed inside square brackets, and if it evaluates to true, the subsequent commands are executed. The structure includes the `if` keyword, followed by a condition, the `then` statement, and finally the closing `fi` to mark the end of the conditional block.

Before entering the conditional block, the script captures the output of the rocket status command in the variable `rocket_status`. Based on its value, the script decides whether to trigger additional commands, such as running a debug command.

> **lightbulb** Ensure there is at least one space between the square brackets `[ ]` and the condition when using conditional statements.

## Example: Using if, elif, and else Blocks

Below is an example demonstrating how to implement conditional logic in a shell script:

```bash theme={null}
