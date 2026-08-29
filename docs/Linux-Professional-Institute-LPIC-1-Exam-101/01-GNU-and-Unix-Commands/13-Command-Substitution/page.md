# Command Substitution

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/GNU-and-Unix-Commands/Command-Substitution/page

Learn to capture command output in Bash and create powerful pipelines using xargs for efficient file processing.

Learn how to capture command output in Bash and build powerful pipelines using `xargs`. This guide covers:

* Command substitution with backquotes and `$(...)`
* Storing outputs in variables
* Processing file lists with `xargs`
* Handling special characters and custom argument placement

***

## Table of Contents

1. [Command Substitution](#command-substitution)\
   1.1 [Using Backquotes](#using-backquotes)\
   1.2 [Using `$(...)` Syntax](#using-...)\
   1.3 [Assigning Output to a Variable](#assigning-output-to-a-variable)
2. [Processing Input with xargs](#processing-input-with-xargs)\
   2.1 [Basic xargs Example](#basic-xargs-example)\
   2.2 [Limiting Arguments per Invocation](#limiting-arguments-per-invocation)\
   2.3 [Handling Filenames with Spaces](#handling-filenames-with-spaces)\
   2.4 [Placing Arguments at a Specific Position](#placing-arguments-at-a-specific-position)
3. [Common xargs Options](#common-xargs-options)
4. [Links and References](#links-and-references)

***

## Command Substitution

Command substitution allows you to embed the output of one command into another or assign it to a variable. Bash supports two forms:

* Backquotes: `` `…` ``
* Dollar parentheses: `$(…)`

### Using Backquotes

```bash theme={null}
mkdir `date +%Y-%m-%d`
ls
