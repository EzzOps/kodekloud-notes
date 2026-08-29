# Decompress using bzip2
[~]$ bunzip2 test.img.bz2
[~]$ du -sh test.img
99M     test.img

# Decompress using gzip
[~]$ gunzip test1.img.gz
[~]$ du -sh test1.img
99M     test1.img

# Decompress using xz
[~]$ unxz test2.img.xz
[~]$ du -sh test2.img
99M     test2.img
```

It is important to note that you do not always need to fully uncompress a file to view its content. Tools like `zcat`, `bzcat`, and `xzcat` allow you to read compressed files without manual decompression.

## Conclusion

This lesson has provided an overview of file compression and archival in Linux. Mastering these techniques will enhance your file management and storage efficiency. Additionally, exploring interactive labs with the VI Editor serves as a practical complement to these technical skills.

For further learning, consider exploring additional documentation on Linux file management and archival strategies.

- [Watch Video](https://learn.kodekloud.com/user/courses/learning-linux-basics-course-labs/module/8587333b-3a93-4eb5-8d3f-13c4a3435d1b/lesson/6c4f9780-6be1-4c2f-b2e1-0b6992ee3c5a)


# IO Redirection

Source: https://notes.kodekloud.com/docs/Learning-Linux-Basics-Course-Labs/Working-with-Shell-II/IO-Redirection/page

This article explains IO redirection in Linux, covering standard streams, redirection techniques, pipes, and the `tee` command for managing command outputs and errors.

In this article, we delve into IO redirection in Linux and explain the concept of standard streams. Every Linux command you run is automatically associated with three primary data streams:

1. **STDIN**: The standard input stream that accepts text input.
2. **STDOUT**: The standard output stream that displays text output on your screen.
3. **STDERR**: The standard error stream that shows error messages.

Below is an example of displaying the content of a file using the `cat` command:

```bash theme={null}
[~]$ cat sample_text.txt
This is the file contents
```

If you attempt to access a file that does not exist, the error message is directed to STDERR:

```bash theme={null}
[~]$ cat sample_text.txt
This is the file contents
cat: sample_text.txt: No such file or directory
```

## Redirecting Standard Output and Error

To redirect the standard output to a file instead of the screen, use the forward arrow symbol (`>`). This operator will overwrite the file with the new output. If you prefer appending the output to an existing file, use the double forward arrow symbol (`>>`). For instance, to save your shell information and then append a descriptive message, execute the following commands:

```bash theme={null}
[~]$ echo $SHELL > shell.txt
[~]$ cat shell.txt
/bin/bash

[~]$ echo "This is the Bash shell" >> shell.txt
[~]$ cat shell.txt
/bin/bash
This is the Bash shell
```

Similarly, to redirect only error messages to a file, prefix the redirection operator with the number 2. This tells the shell to redirect STDERR:

```bash theme={null}
[~]$ cat missing_file 2> error.txt
[~]$ cat error.txt
cat: missing_file: No such file or directory
```

To append error messages instead of overwriting them, use `2>>`:

```bash theme={null}
[~]$ cat missing_file 2>> error.txt
```

> **lightbulb** If you want to run a command without displaying error messages on the screen, you can redirect STDERR to `/dev/null`. This special file discards any input provided to it.

## Using Pipes to Link Commands

Often, you might want to pass the output of one command directly to another without creating an intermediary file—that’s where piping comes into play. The pipe operator (`|`) transfers the standard output from the command on its left to the standard input of the command on its right. For example:

```bash theme={null}
command1 | command2
```

Consider a file named `sample.txt` with the following contents:

```bash theme={null}
[~]$ cat sample.txt
hello there!
Nice to see you here!
```

If you search within `sample.txt` using `grep` and redirect the output to a file, you will experience:

```bash theme={null}
[~]$ grep Hello sample.txt > file.txt
[~]$ less file.txt
```

However, you can use a pipe to send the output directly to `less` for quick viewing:

```bash theme={null}
[~]$ grep Hello sample.txt | less
Hello there!
(END)
```

For comparison, you can view the entire file by simply calling:

```bash theme={null}
[~]$ less sample.txt
hello there!
Nice to see you here!
sample.txt (END)
```

The pipe mechanism allows you to chain multiple commands together, enhancing efficiency and flexibility.

## The tee Command

Another valuable tool for managing IO redirection is the `tee` command. Unlike the redirection operator that sends the output exclusively to a file, `tee` duplicates the output by writing it both to a file and to the screen simultaneously. For example, instead of redirecting the output to a file, you can use:

```bash theme={null}
[~]$ echo $SHELL | tee shell.txt
/bin/bash
[~]$ cat shell.txt
/bin/bash
```

To append the output to the file rather than replacing its content, use the `-a` option with `tee`:

```bash theme={null}
[~]$ echo $SHELL | tee -a shell.txt
```

This technique is especially useful when you need to monitor the output in real time while also saving it for later review.

By mastering these IO redirection techniques, you can efficiently manage command outputs and errors in Linux. Whether saving output to files, suppressing error messages, or chaining commands with pipes, these methods are essential for streamlining your workflow and enhancing your command-line proficiency.

## Quick Reference Table

| Technique           | Purpose                                            | Example Command                                               |
| ------------------- | -------------------------------------------------- | ------------------------------------------------------------- |
| Redirect STDOUT     | Send command output to a file                      | echo \$SHELL > shell.txt                                      |
| Append STDOUT       | Append command output to an existing file          | echo \$SHELL >> shell.txt                                     |
| Redirect STDERR     | Send error messages to a file                      | cat missing\_file 2> error.txt                                |
| Append STDERR       | Append error messages to an existing file          | cat missing\_file 2>> error.txt                               |
| Use Pipes           | Pass output from one command as input to another   | grep Hello sample.txt \| less                                 |
| Utilize tee Command | Duplicate output to file and screen simultaneously | echo $SHELL \| tee shell.txt; echo $SHELL \| tee -a shell.txt |

Happy learning and efficient command chaining!

- [Watch Video](https://learn.kodekloud.com/user/courses/learning-linux-basics-course-labs/module/8587333b-3a93-4eb5-8d3f-13c4a3435d1b/lesson/ca237928-cb81-470a-b923-878e62149490)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/learning-linux-basics-course-labs/module/8587333b-3a93-4eb5-8d3f-13c4a3435d1b/lesson/f22851fc-6994-4895-972b-0b34e29e1b37)
