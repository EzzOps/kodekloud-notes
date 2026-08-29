# Duplicate for another mission:
mission_name=mars-mission
mkdir $mission_name
rocket-add $mission_name
rocket-start-power $mission_name
rocket-internal-power $mission_name
rocket-start-sequence $mission_name
rocket-start-engine $mission_name
rocket-lift-off $mission_name

rocket_status=$(rocket-status $mission_name)
# (Additional duplicated code would be here)
```

Duplicating code like this makes it difficult to maintain, as every instance must be updated individually if any change is needed.

## Modular Approach with Functions

A best practice is to encapsulate repeated code into a function. In shell scripting, a function is simply a block of code designed to perform a specific task and can be reused throughout your script. In the example below, the mission name is passed as an argument to the function and referenced within the function as `$1`.

Below is an improved and modular version of the rocket launch script using a function named `launch-rocket`:

```bash theme={null}
function launch-rocket() {
  mission_name=$1
  mkdir "$mission_name"

  rocket-add "$mission_name"
  rocket-start-power "$mission_name"
  rocket-internal-power "$mission_name"
  rocket-start-sequence "$mission_name"
  rocket-start-engine "$mission_name"
  rocket-lift-off "$mission_name"

  rocket_status=$(rocket-status "$mission_name")
  while [ "$rocket_status" = "launching" ]
  do
    sleep 2
    rocket_status=$(rocket-status "$mission_name")
  done

  if [ "$rocket_status" = "failed" ]
  then
    rocket-debug "$mission_name"
    return 1
  fi
}
```

In the code above, the function `launch-rocket` bundles the entire rocket launch process. This way, you only need to call the function with the desired mission name whenever required. For example, the main part of your script might look like this:

```bash theme={null}
launch-rocket lunar-mission
launch-rocket mars-mission
launch-rocket saturn-mission
launch-rocket mercury-mission
```

> **triangle-alert** Remember that functions must be defined before they are called in your script. Calling a function prior to its definition will result in an error because the shell interprets it as an undefined command.

Notice the difference between using `exit 1` and `return 1` in the function. In the initial version, `exit 1` would terminate the entire script if any individual mission failed. By using `return 1` instead, only the function call terminates with an error, which allows the main script to continue executing and manage subsequent missions. The exit status from each function can be captured with the special variable `$?` if needed.

## When to Use Functions

For large automation tasks—such as installing packages, adding users, configuring firewalls, or carrying out mathematical calculations—breaking down your script into functions is highly beneficial. Each specific task can be implemented as an independent function, which you call in the correct sequence. This strategy not only makes your code modular and easier to maintain but also minimizes duplication.

![The image explains when to use functions, listing tasks like installing packages, adding users, configuring firewalls, and performing mathematical calculations.](https://kodekloud.com/kk-media/image/upload/v1752884055/notes-assets/images/Shell-Scripts-for-Beginners-Functions/frame_240.jpg)

## Simple Function Example: Adding Two Numbers

Here is another straightforward example that demonstrates how to add two numbers using a shell function. In this case, the parameters `$1` and `$2` are passed to the function, which calculates and prints the sum. You can capture the function’s output using command substitution:

```bash theme={null}
function add() {
  echo $(( $1 + $2 ))
}

# Capture the result of the function call in the variable 'sum'
sum=$( add 3 5 )
echo "The sum is: $sum"
```

Keep in mind that anything printed within a function using `echo` becomes its output. While you can also use the return code to indicate success or failure, the `return` statement in shell functions only supports numeric exit statuses. Therefore, echoing the computed value and capturing it is the conventional method for returning results.

![The image lists best practices for coding: develop modular scripts, avoid duplicate code, and use arguments/parameters for variables.](https://kodekloud.com/kk-media/image/upload/v1752884056/notes-assets/images/Shell-Scripts-for-Beginners-Functions/frame_400.jpg)

## Final Thoughts

Modularizing your code with functions is a best practice in shell scripting, helping you avoid pitfalls associated with duplicate code blocks and making scripts more maintainable. Practice applying these techniques in your automation tasks and shell scripts to enhance your coding skills.

Happy scripting!

- [Watch Video](https://learn.kodekloud.com/user/courses/shell-scripts-for-beginners/module/2e5d4133-6bc2-421e-bc8f-0389e7f96490/lesson/c5fee3ab-67bc-4bc7-8705-2d07a75e3adc)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/shell-scripts-for-beginners/module/2e5d4133-6bc2-421e-bc8f-0389e7f96490/lesson/b0001b88-a483-4125-b093-afb0877a8cfa)


# Shebang

Source: https://notes.kodekloud.com/docs/Shell-Scripts-for-Beginners/Shebang/Shebang/page

This guide explores the shebangs role in shell scripts and differences between various shells affecting script execution.

In this guide, we explore the critical role of the shebang in shell scripts. We’ll also review Linux shell basics and highlight the differences between various shells like the Bourne shell, the Bourne Again shell (bash), Debian Almquist shell (dash), Korn shell, Z shell, and C shell. Although these shells share similarities, there are key differences that can affect your script’s execution.

For instance, consider the difference between the Bourne shell (ash, dash, or the Debian shell) and the Bourne Again shell (bash). The image below outlines a few common shell types:

![The image lists shell types: Bourne Shell (sh), Debian Almquist Shell (dash), and Bourne again Shell (bash), with a KodeKloud logo.](https://kodekloud.com/kk-media/image/upload/v1752884057/notes-assets/images/Shell-Scripts-for-Beginners-Shebang/frame_30.jpg)

Previously, we discussed a for loop in a shell script that generates a sequence from 0 to 10 using a bash-specific expression. The following script works as expected in bash:

```bash theme={null}
for mission in {0..10}
do
    create-and-launch-rocket $mission
done
```

When executed in bash, you will see the output:

```bash theme={null}
bash$ launch-rockets.sh
Launching mission 0
Launching mission 1
Launching mission 2
Launching mission 3
Launching mission 4
Launching mission 5
Launching mission 6
Launching mission 7
Launching mission 8
Launching mission 9
Launching mission 10
```

However, if you run this script using the Bourne shell (sh) or dash, the sequence expression `{0..10}` is not expanded, resulting in output like:

```bash theme={null}
sh$ launch-rockets.sh
Launching mission {0..10}
```

Even though many modern systems link the Bourne shell to bash, explicitly testing in shells like dash reveals these differences.

> **lightbulb** To ensure reliable behavior, always run scripts that depend on bash-specific features with the bash interpreter.

The solution is to include a shebang at the beginning of your script. The shebang is a special line that instructs the system which interpreter to use, as demonstrated here:

```bash theme={null}
#!/bin/bash
for mission in {0..10}
do
    create-and-launch-rocket $mission
done
```

With the shebang (`#!/bin/bash`) at the top, executing the script directly guarantees that bash is used regardless of the default shell environment. Consider the following examples:

* **Running the script directly in a non-bash shell:**

```bash theme={null}
sh$ launch-rockets.sh
Launching mission {0..10}
```

* **Running the script explicitly with bash:**

```bash theme={null}
sh$ bash launch-rockets.sh
Launching mission 0
Launching mission 1
Launching mission 2
Launching mission 3
Launching mission 4
Launching mission 5
Launching mission 6
Launching mission 7
Launching mission 8
Launching mission 9
Launching mission 10
```

The shebang assures that your shell script always runs under the intended interpreter, preventing issues associated with incompatible shell syntax.

> **triangle-alert** If your script relies on bash-specific features, **always** start with the appropriate shebang (`#!/bin/bash`) to avoid unexpected behavior when run in different shell environments.

![The image advises best practice in scripting: "Always start with a Shebang in your scripts," presented on a green and white background.](https://kodekloud.com/kk-media/image/upload/v1752884058/notes-assets/images/Shell-Scripts-for-Beginners-Shebang/frame_180.jpg)

That concludes our deep dive into the shebang in shell scripts. Happy scripting, and see you in the next article!

- [Watch Video](https://learn.kodekloud.com/user/courses/shell-scripts-for-beginners/module/2e5d4133-6bc2-421e-bc8f-0389e7f96490/lesson/ea1f0409-2d7e-474c-ab6d-c8ba4302b1a9)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/shell-scripts-for-beginners/module/2e5d4133-6bc2-421e-bc8f-0389e7f96490/lesson/69362b26-b485-45d0-81f0-bc1cf484fddc)
