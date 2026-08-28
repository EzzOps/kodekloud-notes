# Variables

Source: https://notes.kodekloud.com/docs/Shell-Scripts-for-Beginners/Shell-Script-Introduction/Variables/page

This article explains the use of variables in shell scripts to enhance flexibility, reduce errors, and improve maintainability.

In shell scripting, variables enhance flexibility and reduce errors by enabling dynamic value assignment throughout your scripts. Instead of hardcoding values such as a mission name, using a variable (typically named "mission\_name") allows you to update the value in one place, ensuring consistency across all commands.

## Why Use Variables?

Hardcoding values like "lunar-mission" in every command can lead to issues:

* Inconsistencies: A single typo can disrupt the entire script.
* Maintenance Challenges: Adding or modifying steps requires updating every instance manually.
* Poor Reusability: Reusing the script for another mission (e.g., Mars mission) involves replacing each occurrence, increasing error risks.

By declaring a variable at the beginning, you can update its value once, and the change propagates throughout the script.

## Basic Variable Usage

When referencing a variable in a script, always prefix its name with a dollar sign (`$`). However, omit the dollar sign when assigning a value. Below is an improved example of how to set and use a variable in a shell script:

```bash theme={null}
#!/bin/bash
