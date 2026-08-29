# Underscore

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Special-Shell-Variables/Underscore/page

The special shell variable `$_` holds the last argument of the previous command, enhancing productivity in Bash sessions and scripts.

The special shell variable `$_` holds the last argument of the previous command. It’s especially handy in interactive Bash sessions and scripts when you want to avoid retyping long or dynamic arguments.

## Why Use `$_`?

* Boosts productivity by reducing repetitive typing
* Seamlessly reuses file names, directory paths, or any last argument
* Works in interactive shells **and** within scripts

<Callout icon="lightbulb">
  `$_` refers strictly to the last argument of the **previous** command. If that command had no arguments, `$_` will be empty.
</Callout>

***

## Interactive Shell Examples

### Listing and Copying a File

```bash theme={null}
$ ls -l file.conf
total 16
-rw-r--r-- 1 root root 896 Jun 18 2020 file.conf
$ cp $_ /tmp
```

Here, `$_` expands to `file.conf`, so you don’t have to type it twice.

### Chaining Commands

```bash theme={null}
$ ls -l file.conf; echo "Done"
total 16
-rw-r--r-- 1 root root 896 Jan 18 2020 file.conf
Done
$ echo $_
Done
```

Since the last command was `echo "Done"`, `$_` now contains `Done`.

***

## Using `$_` in Scripts

```bash theme={null}
#!/usr/bin/env bash
