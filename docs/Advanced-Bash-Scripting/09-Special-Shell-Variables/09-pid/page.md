# pid

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Special-Shell-Variables/pid/page

This article explains the use of special shell variables `$$` and `$!` for managing process IDs in Bash and POSIX-compatible shells.

In Bash and other POSIX-compatible shells, special variables like `$$` and `$!` help you manage process IDs (PIDs) for debugging, automation, and scripting tasks. While they might not pop up every day, knowing how to use them can streamline background jobs, service management, and process monitoring.

Before diving into these variables, let’s clarify how TTYs, shells, and PIDs relate:

1. When you open a terminal, it’s assigned a TTY (teletype) name.
2. A shell (e.g., Bash) runs on that TTY and acts as the parent process.
3. Any command or script executed in that shell becomes a child process.
4. Every process—from parent shells to background jobs—has a PID and a lifecycle (start → run → exit).

***

## Table of Special PID Variables

| Variable | Description                                          | Typical Use Case                        |
| -------- | ---------------------------------------------------- | --------------------------------------- |
| `$!`     | PID of the most recently launched **background** job | Tracking & controlling background tasks |
| `$$`     | PID of the **current** shell or shell-script process | Self-awareness in scripts               |

***

## Using `$!` to Capture Background Job PIDs

The `$!` variable returns the PID of the last job you sent to the background.

```bash theme={null}
$ sleep 5 &
[1] 93506
$ echo $!
93506
```

Even if you run foreground commands afterward, `$!` holds the PID until you start another background job:

```bash theme={null}
$ echo "First background PID is $!"
First background PID is 93506

$ echo "Hello" &
[1] 93761
Hello
[1] + done echo "Hello"

$ echo $!
93761
```

### Storing `$!` in a Bash Script

A common pattern is launching a service in the background, capturing its PID, and later terminating it. For example, starting an Apache JMeter server:

```bash theme={null}
#!/usr/bin/env bash

jmeter_pid=""

start_jmeter() {
  echo "Starting JMeter server..."
  jmeter-server &
  jmeter_pid=$!
}

start_jmeter
