# Built in Commands

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Refresher/Built-in-Commands/page

This article discusses optimizing Bash script performance by using built-in commands to reduce latency and resource consumption.

Every time you invoke an external binary in a shell script, the shell forks a new process—adding latency and consuming CPU/memory. Bash and other modern shells mitigate this overhead by providing built-in commands that execute inside the shell process. Leveraging built-ins can dramatically speed up your scripts and reduce resource usage.

In this guide, we’ll cover:

* Command categories and types
* How to identify built-in commands
* Performance benefits and benchmarks
* Verifying process creation with `strace`
* Listing all built-in commands and keywords

![The image is a slide titled "Built-in" with a list of topics: command categories and types, how to identify built-in commands, and their performance benefits. It includes a checkmark icon next to each topic.](https://kodekloud.com/kk-media/image/upload/v1752868589/notes-assets/images/Advanced-Bash-Scripting-Built-in-Commands/built-in-commands-topics-checkmark.jpg)

## The Chef Analogy

Think of your shell as a chef in a kitchen. If the chef delegated every simple task—chopping vegetables, stirring soup, plating food—to sous-chefs, the overhead would be enormous. Instead, the chef handles routine tasks directly and only calls for help on specialized jobs. Built-in commands work the same way: the shell “chef” handles them instantly, while external binaries require spawning a separate “assistant” process.

## Command Categories and Types

Shell commands fall into two main categories:

| Category         | Description                                                           | Examples                  |
| ---------------- | --------------------------------------------------------------------- | ------------------------- |
| Built-in Command | Implemented inside the shell; runs without forking a new process.     | `cd`, `echo`, `true`      |
| External Binary  | Stored on disk; invoking them forks a new process then uses `execve`. | `/bin/ls`, `/usr/bin/cat` |

Example:

```bash theme={null}
$ ls
file1.txt  file2.txt

$ echo "Hello, world!"
Hello, world!
```

In the first case, `ls` is an external binary loaded from disk; `echo` is handled directly by the shell.

## Identifying Built-ins vs. External Binaries

Use the `type` built-in to check how a command is implemented:

```bash theme={null}
$ type echo
echo is a shell builtin

$ type cat
cat is /usr/bin/cat
```

> **lightbulb** You can also use `which` or `command -v`, but `type` gives the most accurate distinction between built-in, keyword, and function.

## Performance Benefits of Built-ins

### Benchmarks: `true` vs `/usr/bin/true`

The `true` command simply returns a zero exit status. Compare its built-in version to the external binary:

```bash theme={null}
$ time true
real    0m0.000s
user    0m0.000s
sys     0m0.000s

$ time /usr/bin/true
real    0m0.009s
user    0m0.001s
sys     0m0.005s
```

### Command Execution Times at a Glance

| Command | Built-in (real) | External `/usr/bin` (real) |
| ------- | --------------- | -------------------------- |
| `true`  | 0.000s          | 0.009s                     |
| `echo`  | 0.000s          | 0.324s                     |

Built-ins not only start faster but also complete quicker, especially when called repeatedly in loops.

## Verifying Process Creation with `strace`

To confirm built-ins don’t fork, trace `execve` system calls in your current shell:

1. **Find your shell’s PID**
   ```bash theme={null}
   $ pgrep -o bash
   56120
   ```
2. **Attach `strace` and filter for `execve`**
   ```bash theme={null}
   sudo strace -Tfp $(pgrep -o bash) 2>&1 | grep execve &
   ```
3. **In another terminal, run a built-in vs an external binary**
   ```bash theme={null}
   $ echo "Hello"
   Hello
   # No execve call appears for echo

   $ cat file.txt
   [pid 56147] execve("/usr/bin/cat", ["cat","file.txt"], 0x... ) = 0 <0.000186>
   Hello, world!
   ```

You’ll see `execve` only for `cat`, confirming `echo` runs inside the shell.

## External vs. Built-in Counterparts

Many built-ins have binary counterparts on disk:

```bash theme={null}
$ which echo
/bin/echo

$ type /bin/echo
/bin/echo is /bin/echo

$ type echo
echo is a shell builtin
```

Performance comparison:

```bash theme={null}
$ time /usr/bin/echo "Test"
$ time echo "Test"
