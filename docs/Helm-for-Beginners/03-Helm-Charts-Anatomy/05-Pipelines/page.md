# Pipelines

Source: https://notes.kodekloud.com/docs/Helm-for-Beginners/Helm-Charts-Anatomy/Pipelines/page

This article explores how pipelines streamline command operations and templating in Helm, enhancing readability and flexibility in code.

In this lesson, we will explore how pipelines work and how they can streamline command operations and templating in Helm.

When working in a Linux environment, the output of the echo command simply prints the provided string. However, there are situations where you may want to take this output and process it with another command. This is where pipes (or pipelines) come into play.

For example, consider the following commands:

```shell theme={null}
$ echo "abcd"
abcd
$ echo "abcd" | tr a-z A-Z
ABCD
```

In the first command, the string "abcd" is printed as is. In the second command, the output of `echo "abcd"` is piped into the `tr` command, which translates all lowercase letters (a–z) to uppercase, resulting in "ABCD".

## Pipelines in Helm Templating

Helm templating allows you to efficiently manipulate variables using functions. Typically, functions are written with the function name preceding the variable names. For instance:

```helm theme={null}
{{ upper .Values.image.repository }}
