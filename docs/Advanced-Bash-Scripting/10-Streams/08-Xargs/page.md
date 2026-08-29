# Xargs

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Streams/Xargs/page

This article explains how to use `xargs` to build dynamic command lines from standard input for more flexible shell scripting.

`xargs` is a powerful GNU utility that transforms piped data into arguments for another command. Instead of reading from stdin and writing to stdout like typical pipelines, `xargs` gathers items and appends them as parameters—enabling more flexible shell scripting and one-liners.

***

## Table of Contents

1. [Piping Basics](#piping-basics)
2. [How xargs Works](#how-xargs-works)
3. [Common Use Cases](#common-use-cases)
4. [Handling Special Characters](#handling-special-characters)
5. [Additional Resources](#additional-resources)

***

## Piping Basics

Most shell utilities can read from stdin or files. For example, to count words:

```bash theme={null}
echo "How many words are in this text?" | wc -w
