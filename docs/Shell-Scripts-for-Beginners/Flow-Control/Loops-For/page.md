# Command examples
$ rocket-status lunar-mission
launching    success     failed

$ rocket-debug lunar-mission
overheating

# Script snippet
mission_name=$1
rocket_status=$(rocket-status $mission_name)

if [ "$rocket_status" = "failed" ]; then
    rocket-debug $mission_name
elif [ "$rocket_status" = "success" ]; then
    echo "This is successful"
else
    echo "The state is not failed or success"
fi
```

In this snippet, the status is checked against predefined conditions. If `rocket_status` equals "failed," it triggers the debugging command. For a "success" status, it displays a confirmation message. Any other response results in a default message.

## String Comparisons and Conditional Operators

In shell scripts, string comparison uses the equals operator (`=`) for equality and the not-equals operator (`!=`) for inequality. Make sure the condition is placed inside square brackets with proper spacing.

<Frame>
  ![The image shows a table explaining conditional operators with examples and descriptions, including string and number comparisons for equality and inequality.](https://kodekloud.com/kk-media/image/upload/v1752884046/notes-assets/images/Shell-Scripts-for-Beginners-Conditional-Logic/frame_260.jpg)
</Frame>

## Numeric Comparisons

For numeric values, different operators are employed:

* Use `-eq` to check if two numbers are equal.
* Use `-ne` to verify that numbers are not equal.
* Use `-gt` for "greater than."
* Use `-lt` for "less than."

An extended version using double square brackets `[[ ]]` provides additional functionality such as pattern matching, which is a Bash extension and might not be available in all shells.

### Pattern Matching Example

To check if the string "ABC" contains the substring "BC", you can use pattern matching with asterisks (`*`) outside double quotes:

```bash theme={null}
[[ "ABC" == *BC* ]]
```

<Frame>
  ![The image explains conditional operators in Bash, showing examples and descriptions of string comparisons and pattern matching.](https://kodekloud.com/kk-media/image/upload/v1752884047/notes-assets/images/Shell-Scripts-for-Beginners-Conditional-Logic/frame_340.jpg)
</Frame>

## Sorting and Logical Operators

Alphabetical comparisons use sort order operators. For example, "ABC" comes before "BCD" when sorted alphabetically, and operators reflect that order during comparisons.

You can combine multiple conditions using logical operators:

* The AND operator (`&&`) ensures both conditions are true.

  ```bash theme={null}
  [ COND1 ] && [ COND2 ]
  ```

* The OR operator (`||`) checks if at least one condition is true.

  ```bash theme={null}
  [ COND1 ] || [ COND2 ]
  ```

When using double square brackets, you can include the entire condition with logical operators in one pair:

```bash theme={null}
[[ A -gt 4 && A -lt 10 ]]
[[ A -gt 4 || A -lt 10 ]]
```

## File-Level Conditional Operators

Shell scripts also allow file-level checks. Some common file operators are:

| Operator | Purpose                        | Example                     |
| -------- | ------------------------------ | --------------------------- |
| -e       | Check if a file exists         | `[ -e filename ]`           |
| -d       | Check if a path is a directory | `[ -d /path/to/directory ]` |
| -s       | Check if a file is not empty   | `[ -s filename ]`           |
| -x       | Check if a file is executable  | `[ -x filename ]`           |
| -w       | Check if a file is writable    | `[ -w filename ]`           |

<Frame>
  ![The image shows a table of conditional operators for files, detailing checks for existence, directory status, size, executability, and writability.](https://kodekloud.com/kk-media/image/upload/v1752884047/notes-assets/images/Shell-Scripts-for-Beginners-Conditional-Logic/frame_520.jpg)
</Frame>

<Callout icon="triangle-alert">
  Be cautious with file operators and always verify that the file or directory you are checking has the correct permissions to avoid unexpected behavior.
</Callout>

## Conclusion

By mastering conditional logic in shell scripts, you can effectively control the execution flow of your scripts based on dynamic conditions. Practice using these statements to further deepen your understanding of shell scripting and improve automation in your projects.

For additional learning, consider exploring resources like [Shell Scripting Fundamentals](https://www.shellscript.sh) and [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/shell-scripts-for-beginners/module/054d2eb5-f3b9-47d4-af5a-37b9f0d15f2c/lesson/312e6867-e630-4c8c-b9c7-93e54345ea52" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/shell-scripts-for-beginners/module/054d2eb5-f3b9-47d4-af5a-37b9f0d15f2c/lesson/262bb4c2-4f87-4601-b117-20e40198eae5" />
</CardGroup>


# Loops For

Source: https://notes.kodekloud.com/docs/Shell-Scripts-for-Beginners/Flow-Control/Loops-For/page

This article explores using for loops in shell scripts to automate repetitive tasks efficiently.

In this article, we explore how to use for loops in shell scripts to automate repetitive tasks. Imagine you built a script to launch a single rocket with one command. Now, if you need to launch hundreds of rockets for various missions—each requiring the same set of commands executed sequentially—a for loop becomes essential.

Initially, you might have executed commands like these:

```bash theme={null}
$ create-and-launch-rocket lunar-mission
$ create-and-launch-rocket jupiter-mission
$ create-and-launch-rocket saturn-mission
$ create-and-launch-rocket satellite-mission
$ create-and-launch-rocket lunar-mission-2
$ create-and-launch-rocket mars-mission
$ create-and-launch-rocket earth-mission
```

Instead of calling the `create-and-launch-rocket` script multiple times, you can consolidate these tasks into a new script (e.g., `launch_rockets.sh`) and use a for loop to handle each mission. For example, you could have written the commands manually as follows:

```bash theme={null}
create-and-launch-rocket lunar-mission
create-and-launch-rocket saturn-mission
create-and-launch-rocket solar-mission-20
create-and-launch-rocket lunar-mission
create-and-launch-rocket earth-mission
```

A for loop allows you to execute the `create-and-launch-rocket` command for every mission in a given list. A basic for loop in a shell script is structured like this:

```bash theme={null}
for mission in <list of missions>
do
    create-and-launch-rocket lunar-mission
done
```

In this structure, the keywords `do` and `done` define the block of commands executed during each loop iteration. The list of missions can be provided as space-separated names. However, keep in mind that using a hardcoded mission name inside the loop (e.g., always using `lunar-mission`) will result in launching the same mission each time:

```bash theme={null}
for mission in lunar-mission jupiter-mission saturn-mission satellite-mission lunar-mission-2
do
  create-and-launch-rocket lunar-mission
done
```

To correctly use the mission name for each iteration, replace the hardcoded mission name with the variable `mission`:

```bash theme={null}
for mission in lunar-mission jupiter-mission saturn-mission satellite-mission lunar-mission-2
do
  create-and-launch-rocket $mission
done
```

With this change, during each iteration the variable `mission` holds the value of the current mission in the list, and the script launches the corresponding rocket.

When you have a large number of missions, listing all mission names directly in the script becomes impractical. Instead, store the mission names in an external file (e.g., `mission-names.txt`) and read them into your loop:

```bash theme={null}
for mission in `cat mission-names.txt`
do
    create-and-launch-rocket $mission
done
```

Here, the command within the backticks (`cat mission-names.txt`) is executed first to retrieve the mission names, which are then iterated over by the loop. A best practice is to design your script so that inputs are either passed as command-line arguments or read from an external file, ensuring that the script requires no modifications for routine use.

<Callout icon="lightbulb">
  Avoid using backticks for command substitution; instead, use the more readable `$()` syntax, especially when embedding multiple commands.
</Callout>

There are two primary ways to supply values to a for loop:

1. Reading values from a file.
2. Specifying the items directly.

For example, to generate mission names from one to six, you might write:

```bash theme={null}
for mission in $(cat mission-names.txt)
do
    create-and-launch-rocket $mission
done

for mission in 1 2 3 4 5 6
do
    create-and-launch-rocket mission-$mission
done
```

If you need to run the loop over a specific range (such as 100 times), you can utilize brace expansion to generate the sequence:

```bash theme={null}
for mission in $(cat mission-names.txt)
do
  create-and-launch-rocket $mission
done

for mission in 1 2 3 4 5 6
do
  create-and-launch-rocket mission-$mission
done

for mission in {0..100}
do
  create-and-launch-rocket mission-$mission
done
```

For users familiar with programming languages like C, which combine initialization, condition, and increment in loops, note that shell scripts also support similar styles using double parentheses.

Typically, you would use a for loop to repeat tasks such as executing commands multiple times, iterating through files, parsing lines within a file, or processing command outputs. Consider the scenarios illustrated in the diagram below:

<Frame>
  ![The image lists scenarios for using a "For Loop": executing commands repeatedly, iterating through files, lines within a file, and command outputs.](https://kodekloud.com/kk-media/image/upload/v1752884049/notes-assets/images/Shell-Scripts-for-Beginners-Loops-For/frame_370.jpg)
</Frame>

Here are some practical examples of using for loops:

1. **Counting lines in files:** Iterate through a list of files from the output of the `ls` command and print the line count for each file.

   ```bash theme={null}
   for file in $(ls)
   do
     echo "Line count of $file is $(cat $file | wc -l)"
   done
   ```

2. **Installing packages:** Read a list of packages from a file and install them one by one.

   ```bash theme={null}
   for package in $(cat install-packages.txt)
   do
     sudo apt-get -y install $package
   done
   ```

3. **Checking server uptimes:** SSH into a list of servers (provided in a file) to check their uptimes. (Note: This approach requires passwordless SSH for a seamless experience.)

   ```bash theme={null}
   for server in $(cat servers.txt)
   do
     ssh $server "uptime"
   done
   ```

By incorporating these practices, you can create scripts that are both robust and maintainable, simplifying the task for users, even those with limited shell scripting experience.

Happy scripting!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/shell-scripts-for-beginners/module/054d2eb5-f3b9-47d4-af5a-37b9f0d15f2c/lesson/aafb5bad-118d-4486-9b24-c0dbb05b8cc9" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/shell-scripts-for-beginners/module/054d2eb5-f3b9-47d4-af5a-37b9f0d15f2c/lesson/2a701243-2952-4ba0-b1b4-218164117d87" />
</CardGroup>
