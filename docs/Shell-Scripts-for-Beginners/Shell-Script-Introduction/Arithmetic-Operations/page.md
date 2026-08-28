# Or
$ yum install shellcheck
```

For additional installation instructions and platform-specific details, please refer to the [ShellCheck GitHub repository](https://github.com/koalaman/shellcheck).

Once installed, run ShellCheck on your script with:

```bash theme={null}
$ shellcheck menu.sh
```

This command inspects your script and provides warnings along with helpful suggestions. For instance, you might see output like:

```bash theme={null}
In menu.sh line 9:
read -r -p "Enter your choice: " choice
     ^--^ SC2162: read without -r will mangle backslashes.

In menu.sh line 11:
if [ "$choice" -eq 1 ]
   ^-----^ SC2086: Double quote to prevent globbing and word splitting.
Did you mean:
if [ "$choice" -eq 1 ]

In menu.sh line 14:
elif [ "$choice" -eq 2 ]
     ^-----^ SC2086: Double quote to prevent globbing and word splitting.
Did you mean:
elif [ "$choice" -eq 2 ]
```

With ShellCheck, you ensure that your script adheres to industry best practices and minimizes potential errors.

## Using an Integrated Development Environment (IDE)

For users who prefer a visual interface, many free and open-source IDEs support shell scripting. One notable option is the [JetBrains PyCharm Community Edition IDE](https://www.jetbrains.com/pycharm/download/#section=windows), which, via plugins, offers syntax highlighting and real-time recommendations that help improve your scripts.

<Frame>
  ![The image shows a webpage for downloading PyCharm, offering Professional and Community editions for Windows, Mac, and Linux, with version details and download links.](https://kodekloud.com/kk-media/image/upload/v1752884059/notes-assets/images/Shell-Scripts-for-Beginners-Tips-amp-Tricks-ShellCheck-amp-IDE/frame_90.jpg)
</Frame>

Other popular IDEs include [Microsoft Visual Studio](https://visualstudio.microsoft.com/) and [Atom](https://atom.io/), both of which provide environments tailored to writing and debugging shell scripts. For a comprehensive look at industry best practices, consider reviewing [Google’s shell scripting style guide](https://google.github.io/styleguide/shellguide.html).

<Frame>
  ![The image compares Visual Studio Code and Atom, showcasing download options for macOS, with a focus on editing and debugging features.](https://kodekloud.com/kk-media/image/upload/v1752884060/notes-assets/images/Shell-Scripts-for-Beginners-Tips-amp-Tricks-ShellCheck-amp-IDE/frame_110.jpg)
</Frame>

<Frame>
  ![The image shows a Shell Style Guide table of contents, covering topics like environment, comments, formatting, and naming conventions, with a link to the full guide.](https://kodekloud.com/kk-media/image/upload/v1752884062/notes-assets/images/Shell-Scripts-for-Beginners-Tips-amp-Tricks-ShellCheck-amp-IDE/frame_120.jpg)
</Frame>

<Callout icon="lightbulb">
  Integrating IDE plugins for shell scripting can help catch potential issues before runtime, streamlining your development process.
</Callout>

By incorporating these tools and methodologies into your workflow, you can significantly enhance the quality and reliability of your shell scripts. Happy scripting and enjoy exploring these practical techniques!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/shell-scripts-for-beginners/module/2e5d4133-6bc2-421e-bc8f-0389e7f96490/lesson/dcc9872e-95d3-464f-b73e-33ff0fb0ac1f" />
</CardGroup>


# Arithmetic Operations

Source: https://notes.kodekloud.com/docs/Shell-Scripts-for-Beginners/Shell-Script-Introduction/Arithmetic-Operations/page

This guide explores methods for performing arithmetic operations in shell scripts using expr, double parentheses, and the bc utility for floating point calculations.

In this guide, we explore various methods to perform arithmetic operations in shell scripts. We'll cover different techniques such as using the expr command, double parentheses for arithmetic expansion, and the bc utility for floating point calculations.

## Using the expr Command

The `expr` command is a traditional way to perform arithmetic operations in shell scripts. To use it, simply provide an arithmetic expression as input, and it will output the result. For example, the following command adds two numbers:

```bash theme={null}
$ expr 6 + 3
9
```

<Callout icon="lightbulb">
  Ensure that operators and operands are strictly separated by spaces. When multiplying using `expr`, the star symbol (\*) must be escaped with a backslash because `*` is interpreted as a reserved regex character.
</Callout>

The `expr` command supports other arithmetic operations like subtraction, division, and multiplication. You can also incorporate variable substitution. Consider the following examples:

```bash theme={null}
$ expr 6 + 3
9
$ expr 6 - 3
3
$ expr 6 / 3
2
$ expr 6 \* 3
18

$ A=6
$ B=3
$ expr $A + $B
9
$ expr $A - $B
3
$ expr $A / $B
2
$ expr $A \* $B
18
```

## Using Double Parentheses

Bash also offers a more concise method for arithmetic evaluation using double parentheses `(( ))`. This C-like syntax automatically handles variable expansion (no need to prefix variables with `$`) and doesn’t require spaces between operators and operands. Escaping the multiplication operator is also unnecessary.

For example, the following commands perform arithmetic operations:

```bash theme={null}
$ A=6
$ B=3
$ echo $(( A + B ))
9
$ echo $(( A - B ))
3
$ echo $(( A / B ))
2
$ echo $(( A * B ))
18
```

Using double parentheses also allows C-style variable manipulation with operators such as pre-increment (`++A`), pre-decrement (`--A`), post-increment (`A++`), and post-decrement (`A--`). Observe the following:

```bash theme={null}
$ echo $(( ++A ))
7
$ echo $(( --A ))
6
$ echo $(( A++ ))
6
$ echo $(( A-- ))
7
```

<Callout icon="triangle-alert">
  Always use `echo` or store the result in a variable when using arithmetic expansion. Failing to do so might cause the shell to misinterpret the output as a command, leading to errors.
</Callout>

## Performing Floating Point Arithmetic with bc

Both `expr` and double parentheses support only integer arithmetic. To handle floating point calculations, use the `bc` utility. The `bc` tool acts as a basic calculator and is ideal for more precise computations.

For instance, dividing 10 by 3 using integer arithmetic returns an integer result:

```bash theme={null}
$ A=10
$ B=3
$ expr $A / $B
3
$ echo $(( A / B ))
3
```

To obtain a floating point result, use the `-l` flag with `bc`:

```bash theme={null}
$ echo "$A / $B" | bc -l
3.333333
```

The `-l` flag loads the standard math library, enabling accurate floating point calculations. You can interact with `bc` in a script or use piping for one-off operations.

## Summary

By utilizing the methods discussed above, you can effectively perform both integer and floating point arithmetic in your shell scripts. Whether you choose the traditional `expr` command, the modern double parentheses expansion, or the versatile `bc` utility for precision arithmetic, these techniques are essential for automating numerical operations in your scripts.

Happy scripting!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/shell-scripts-for-beginners/module/2709b373-3a6f-4b31-9aff-fe8a553898fa/lesson/60ae59e7-fbc1-4954-bcdc-0b574f259399" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/shell-scripts-for-beginners/module/2709b373-3a6f-4b31-9aff-fe8a553898fa/lesson/3cb2b8e2-e29c-4525-8fc7-0c999dda4f9b" />
</CardGroup>
