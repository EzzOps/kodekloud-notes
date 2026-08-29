# Script usage: Brief summary of the script’s purpose and how to invoke it.
# Exit codes: 0 = Success, 1 = General error, 2 = Missing arguments
# Author: Your Name <your.email@example.com>
```

## Tips for Effective Comments

* Keep lines under 80 characters for readability.
* Write comments in complete sentences where clarity is needed.
* Update comments whenever you modify related code blocks.
* Avoid over-commenting trivial code—focus on intent, not implementation.

## References

* [Git Documentation](https://git-scm.com/doc)
* [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/48c76c43-0257-44a4-b95d-36a8cceaff66/lesson/ce43002c-6c71-46ef-9896-db036ba84e67)


# Logging

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Good-Practices-applied/Logging/page

Track events with ISO 8601 timestamps by wrapping date calls in functions for consistent, machine-friendly logs across environments.

Track events with ISO 8601 timestamps by wrapping `date` calls in functions. This ensures consistent, machine-friendly logs across environments.

## Why Use Timestamped Logs

Timestamped entries help you:

* Debug sequences in real time
* Audit events in containerized workflows
* Reconstruct failures across distributed systems

## Quick Demo: Inline Timestamp

Use `echo` with command substitution to append UTC time:

```bash theme={null}
echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") : Script event happening"
```

Output:

```text theme={null}
2023-05-20T03:51:03Z : Script event happening
```

## Reusable `log` Function

Instead of repeating timestamp logic, encapsulate it:

```bash theme={null}
#!/usr/bin/env bash
log() {
    echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") ${*}" >&2
}

log "Hello World!"
```

Running `./log.sh` produces:

```text theme={null}
2023-06-01T05:42:45Z Hello World!
```

> **lightbulb** Sending log messages to standard error (`>&2`) separates them from regular output and integrates better with redirection.

![The image features a diagram with a clock icon and connected nodes, accompanied by the text "Enabling us to track the flow and sequence of events," under the heading "Logging."](https://kodekloud.com/kk-media/image/upload/v1752868574/notes-assets/images/Advanced-Bash-Scripting-Logging/logging-clock-icon-diagram.jpg)

## ISO 8601 Date Format

Using `YYYY-MM-DDThh:mm:ssZ` guarantees consistency across locales. Common `date` specifiers:

| Specifier | Meaning               |
| --------- | --------------------- |
| %Y        | Year (4 digits)       |
| %m        | Month (01–12)         |
| %d        | Day of month (01–31)  |
| %H        | Hour (00–23)          |
| %M        | Minute (00–59)        |
| %S        | Second (00–59)        |
| %Z        | Time zone (e.g., UTC) |

Test formats:

```bash theme={null}
date
date -u +"%Y-%m-%dT%H:%M:%SZ"
