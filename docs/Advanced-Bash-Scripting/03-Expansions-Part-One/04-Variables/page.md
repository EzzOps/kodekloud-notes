# Variables

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Expansions-Part-One/Variables/page

This article explains variable expansion in Bash, covering access, manipulation, and advanced features for effective scripting.

Variable expansion allows you to retrieve and manipulate the value stored in a Bash variable using the `$` syntax. This powerful feature is essential for automation, text processing, and script flexibility.

## Introduction

In shell scripting, variables can store filenames, paths, numbers, or strings. By applying parameter expansion, you can:

* Access variable contents
* Perform string operations
* Provide fallback values
* Calculate lengths and more

```bash theme={null}
filename="file.txt"
number=100
string="Hello World"
command_output=$(ls)

dir_path="/path/to/directory"
greeting="Hello"
name="User"
echo "$greeting, $name! Welcome to $dir_path"
```

## Basic Variable Expansion

Whenever the shell sees `$variable_name`, it replaces it with the variable’s value:

```bash theme={null}
name="John Doe"
echo $name
