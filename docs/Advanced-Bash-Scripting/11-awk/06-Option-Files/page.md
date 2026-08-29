# Option Files

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/awk/Option-Files/page

Explains running awk programs from files, contrasting pure awk scripts and Bash hybrid approaches, covering shebangs, quoting, variable passing, field separators, and portability considerations.

Although many awk programs are typed directly on the command line for quick tasks, storing awk programs in files is a better practice for larger or reusable scripts. Files make your awk code easier to read, test, version-control, and maintain.

Here are two equivalent ways to run a simple "Hello, World!" example.

Inline on the command line (single-quoted program literal):

```bash theme={null}
$ awk 'BEGIN { print "Hello, World!" }'
Hello, World!
```

From a file (hello.awk) using -f:

```awk theme={null}
BEGIN {
    print "Hello, World!"
}
```

Run it with:

```bash theme={null}
$ awk -f hello.awk
Hello, World!
```

<Frame>
  <img alt="A dark-themed presentation slide titled &#x22;awk Programs From Files&#x22; showing a teal checkmark icon next to the text &#x22;The importance of writing awk programs to a file.&#x22;" />
</Frame>

Key details when using awk programs from files

* Do not wrap the program contents in single quotes when it lives in a file. Single quotes are only used when passing an awk program as a single argument on the command line.
* You can make the file executable by adding a shebang that includes the `-f` flag so awk reads the program from the script file:

```bash theme={null}
#!/usr/bin/env awk -f

BEGIN {
    print "Hello, World!"
}
```

<Callout icon="warning">
  Using `#!/usr/bin/env awk -f` in a shebang can be unreliable on some systems because the shebang is passed as a single argument string and `env` may not split the interpreter from its option. Safer alternatives:

  * Use the explicit interpreter path (for example, `#!/usr/bin/awk -f`) when that path is known and consistent across target systems.
  * If your `/usr/bin/env` supports `-S` (GNU coreutils), use `#!/usr/bin/env -S awk -f` to allow argument splitting.

  For maximum portability, prefer an explicit awk interpreter path or invoke `awk -f script` from a shell wrapper.
</Callout>

<Callout icon="lightbulb">
  The `-f` flag tells awk to read the program from a file. When using an awk shebang, include `-f` so the interpreter treats the script file as an awk program.
</Callout>

Two common styles for file-based awk programs

There are two main patterns for organizing awk in files. Each has trade-offs in portability, readability, and access to shell features.

| Style             | Typical shebang / invocation                          | Pros                                                                                                     | Cons                                                                                                         | Best suited for                                           |
| ----------------- | ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------- |
| Pure awk script   | `#!/usr/bin/env awk -f` or `awk -f script.awk`        | Entire file is valid awk; portable within awk environments; idiomatic for larger awk-only programs       | No direct shell features (globbing, parameter expansion, pipelines) without invoking `system()` or `getline` | Standalone awk utilities and text-processing filters      |
| Bash + awk hybrid | `#!/usr/bin/env bash` and call `awk '...'` from shell | Full access to shell features (pipes, env vars, command substitution); easy integration with other tools | Awk code must be quoted inside shell; mixing languages can complicate quoting and maintenance                | Shell scripts that leverage awk for data processing steps |

1. Pure awk script (executable awk program)

* Create a file containing only valid awk syntax and include a shebang such as `#!/usr/bin/env awk -f` (or an explicit path).
* Pros: cleaner awk-only source, easier to share as an awk utility.
* Cons: less direct access to shell behavior.

Example (hello.awk):

```awk theme={null}
#!/usr/bin/env awk -f

BEGIN {
    print "Hello, World!"
}
```

Run with either:

```bash theme={null}
$ awk -f hello.awk
Hello, World!
