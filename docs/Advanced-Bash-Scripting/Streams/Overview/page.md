# Overview

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Streams/Overview/page

This lesson covers Linux streams, their manipulation in shell scripting, and techniques for redirecting and chaining commands.

In this lesson, we’ll dive into Linux streams and learn how to manipulate them in shell scripting. Linux streams are the flow of data between processes—much like water flowing through a pipe. Just as you can redirect a river with gates, you can reroute streams in the shell using redirection operators and pipes.

<Frame>
  ![The image is a "Streams Overview" diagram comparing general streams, represented by wavy lines and gates or valves, to Linux streams, represented by code symbols and redirection operators or programming constructs.](https://kodekloud.com/kk-media/image/upload/v1752868642/notes-assets/images/Advanced-Bash-Scripting-Overview/streams-overview-diagram-linux-comparison.jpg)
</Frame>

Understanding streams is essential for robust shell scripts. You’ll see how to capture command output, handle errors, and chain commands with pipes to build powerful one-liners.

***

## Standard Streams in Linux

Every Linux process is born with three standard file descriptors:

| File Descriptor | Stream Name | Description                              | Default Source / Destination |
| --------------- | ----------- | ---------------------------------------- | ---------------------------- |
| 0               | stdin       | Reads input (keyboard or another stream) | Keyboard or pipe             |
| 1               | stdout      | Writes normal output                     | Terminal or redirected file  |
| 2               | stderr      | Writes error messages and diagnostics    | Terminal or redirected file  |

* Standard input (fd 0) typically reads from your keyboard

<Frame>
  ![The image is a "Streams Overview" slide showing "0: Stdin" with an icon of a keyboard, indicating standard input.](https://kodekloud.com/kk-media/image/upload/v1752868643/notes-assets/images/Advanced-Bash-Scripting-Overview/streams-overview-stdin-keyboard.jpg)
</Frame>

* Standard output (fd 1) displays command results

* Standard error (fd 2) sends error messages

<Frame>
  ![The image is a slide titled "Streams Overview" showing "2: Stderr" with an icon of a window and an exclamation mark, indicating standard error output.](https://kodekloud.com/kk-media/image/upload/v1752868644/notes-assets/images/Advanced-Bash-Scripting-Overview/streams-overview-stderr-icon.jpg)
</Frame>

<Callout icon="lightbulb">
  `stdout` and `stderr` both default to your terminal. Redirecting one does not affect the other unless you explicitly combine them.
</Callout>

***

## Redirecting Streams

You can reroute streams using `<`, `>`, and pipes (`|`). This allows you to save output to files, read input from files, or chain commands together.

<Frame>
  ![The image is a "Streams Overview" slide showing three concepts: output redirection, input redirection, and pipes, each represented by a symbol.](https://kodekloud.com/kk-media/image/upload/v1752868645/notes-assets/images/Advanced-Bash-Scripting-Overview/streams-overview-redirection-pipes.jpg)
</Frame>

```bash theme={null}
