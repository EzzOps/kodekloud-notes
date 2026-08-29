# Comments

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Good-Practices-applied/Comments/page

Clear, concise comments make your shell scripts easier to maintain, understand, and extend while following best practices for documentation.

Clear, concise comments make your shell scripts easier to maintain, understand, and extend. Follow these best practices to ensure your scripts are well-documented and self-explanatory.

## Header Comment Structure

A standardized header typically includes:

| Field      | Purpose                                               |
| ---------- | ----------------------------------------------------- |
| Shebang    | Defines the interpreter (`#!/usr/bin/env bash`)       |
| Summary    | One-line description of the script’s functionality    |
| Usage      | How to invoke the script, including any flags/options |
| Exit Codes | List of possible exit codes and their meanings        |
| Author     | Name and contact information                          |

<Callout icon="lightbulb">
  With modern version control systems like [Git](https://git-scm.com/), embedding a change history in comments is usually redundant.
</Callout>

## Example Header

```bash theme={null}
#!/usr/bin/env bash
#
