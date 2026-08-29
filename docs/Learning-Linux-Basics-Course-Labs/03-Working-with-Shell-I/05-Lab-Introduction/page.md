# Home Directory = ~ (tilde)
[~]$
```

> **lightbulb** Always check your current directory by observing the prompt, and use the `pwd` command for confirmation.

## Executing Commands

Interacting with Linux is as simple as typing a command into the shell. Each command usually corresponds to a program that performs a particular task. For example, the `echo` command prints text to the screen. Running `echo` without an argument produces no output:

```bash theme={null}
[~]$ echo
[~]$
```

To see text output, provide an argument as shown here:

```bash theme={null}
[~]$ echo Hello
Hello
[~]$
```

### Arguments and Options

Many commands support additional input in the form of arguments or options to modify their behavior. For instance, to print "Hello" without a trailing newline, use the `-n` option with `echo`:

```bash theme={null}
[~]$ echo -n Hello
Hello[~]$
```

Another useful command is `uptime`, which displays how long the system has been running along with load information:

```bash theme={null}
[~]$ uptime
19:18:51 up 19:48,  2 users,  load average: 1.18, 0.49, 0.36
[~]$
```

> **lightbulb** If you are ever unsure about a command or its available options, refer to its help output (using `command --help`) or consult the man pages.

## Understanding Command Types

Linux commands are broadly categorized into two types:

1. **Internal (Built-in) Commands**\
   These commands are integrated into the shell. They include:
   * `cd` (change directory)
   * `export`
   * `mkdir` (make directory)
   * `pwd` (print working directory)

2. **External Commands**\
   These are separate binary programs or scripts residing on the system and may be installed by default or added later. A common example is the `mv` (move) command.

To verify whether a command is internal or external, use the `type` command. For example, executing `type echo` shows that `echo` is a built-in command.

## Conclusion

This lesson lays the groundwork for working with the Linux shell. As you continue, you will gain confidence in using commands, understanding options, and efficiently navigating the file system. Embrace the command line as your primary tool for effective system management and administration.

For further exploration, check out additional resources such as:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Linux Documentation](https://www.kernel.org/doc/html/latest/)
* [Bash Guide for Beginners](https://www.tldp.org/LDP/Bash-Beginners-Guide/html/)

Happy exploring!

- [Watch Video](https://learn.kodekloud.com/user/courses/learning-linux-basics-course-labs/module/267dec49-c3e9-4627-b7f8-9bf9aa834e53/lesson/a07b1843-0a6f-4cf5-91a5-d2ce9f2bf26c)


# Lab Introduction

Source: https://notes.kodekloud.com/docs/Learning-Linux-Basics-Course-Labs/Working-with-Shell-I/Lab-Introduction/page

This article provides an introductory tour of the Hands-on Labs available in this course.

This article provides an introductory tour of the Hands-on Labs available in this course. If you have never used KodeKloud Labs before, please review this guide before attempting any lab exercises.

The Hands-on Labs simulate a genuine Linux Command Line Interface where you execute commands using your keyboard. For the best experience, we recommend using a laptop or desktop computer. Each lab is specifically designed to reinforce the concepts covered in previous lecture sessions.

> **lightbulb** Before starting a lab, click the provided link to open the Hands-on Labs environment. Please allow a few minutes for the lab environment to load, as it simulates a real Linux setup running on Mumshad Mannambeth's laptop.

The lab interface is divided into two primary sections:

1. **Linux Terminal:** Located on the left-hand side where you’ll execute commands and perform tasks.
2. **Lab Portal:** Found on the right-hand side, displaying the questions and guidelines related to the lab exercises.

Below is a sample terminal prompt to help you get started:

```bash theme={null}
bob@caleston-lp10:~$
```

## Types of Lab Questions

There are two primary types of questions you may encounter during the labs:

### Multiple-Choice Questions

For multiple-choice questions, you will need to execute commands in the terminal to determine the correct answer. Once you have confirmed your result, click the corresponding button to proceed.

For example, to determine the path to Bob's home directory, execute the following command:

```bash theme={null}
bob@caleston-lp10:~$ echo $HOME
/home/bob
```

After selecting the correct answer, the next question will load automatically.

### Configuration Tests

Configuration tests require you to perform specific tasks in the terminal. For example, to create a directory named "birds" in Bob's home directory, use the following command:

```bash theme={null}
bob@caleston-lp10:~$ mkdir /home/bob/birds
```

If an error occurs—such as mistakenly creating a directory named "bird" instead of "birds"—the interface will indicate the mistake when you click the check button. For example:

```bash theme={null}
bob@caleston-lp10:~$ mkdir /home/bob/bird
```

To troubleshoot, click the provided icon for more details. Then, correct your command and validate the task again. The corrected command sequence appears as follows:

```bash theme={null}
bob@caleston-lp10:~$ mkdir /home/bob/bird
bob@caleston-lp10:~$ mkdir /home/bob/birds
```

If you ever feel uncertain about how to proceed, simply click the hint button to receive helpful guidance.

## Example Command Sequence

Below is an example sequence of commands you might encounter during a lab:

```bash theme={null}
bob@caleston-lp10:~$ echo $HOME
/home/bob
bob@caleston-lp10:~$ mkdir /home/bob/bird
bob@caleston-lp10:~$ mkdir /home/bob/birds
bob@caleston-lp10:~$
```

In some scenarios, you might also work with nested directories. For example, to create nested folders for "fish" and "salmon", run:

```bash theme={null}
mkdir -p /home/bob/fish/salmon
```

Good luck with your labs, and enjoy the hands-on learning experience!

## Additional Resources

* [KodeKloud Labs Documentation](/docs/klabs)
* [Linux Command Line Basics](https://linuxcommand.org/)

> **lightbulb** For optimal learning, practice these commands on your local terminal while following along with the lab instructions.

- [Watch Video](https://learn.kodekloud.com/user/courses/learning-linux-basics-course-labs/module/267dec49-c3e9-4627-b7f8-9bf9aa834e53/lesson/1b2b6aa8-4fa7-4708-abc0-ef91b537aa67)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/learning-linux-basics-course-labs/module/267dec49-c3e9-4627-b7f8-9bf9aa834e53/lesson/6d98e2f5-b982-4f21-add1-2ab4fb50826b)
