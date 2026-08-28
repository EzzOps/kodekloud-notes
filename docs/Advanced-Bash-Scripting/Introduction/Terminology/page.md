# In Bash
$ echo -n "Hello"; echo "END"
HelloEND

# In sh
$ sh -c 'echo -n "Hello"; echo "END"'
-n Hello
END
```

* Under **sh**, `-n` is treated as text and printed.
* Under **bash**, `-n` removes the newline as expected.

<Callout icon="triangle-alert">
  For portable scripts, avoid relying on `echo -n`. Use `printf` instead:

  ```bash theme={null}
  printf "Hello"; echo "END"
  ```
</Callout>

## Conclusion

* Refer to any interpreter as **shell scripting** when you don’t need to specify.
* Use **shell scripting with Bash** (or another shell) if you rely on that shell’s extensions.
* For maximum portability and advanced features, Bash is the de facto standard.

## Links and References

* [Bash Reference Manual](https://www.gnu.org/software/bash/manual/)
* [Zsh Manual](https://zsh.sourceforge.io/Doc/)
* [POSIX Shell Specification](https://pubs.opengroup.org/onlinepubs/9699919799/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/62d639a9-3779-4ae6-b8b2-1cc49f117f64/lesson/a1527056-e187-40bd-b475-de88e5d0973c" />
</CardGroup>


# Terminology

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/Introduction/Terminology/page

This article clarifies the terms shell, CLI, terminal, console, TTY, and POSIX compliance for Unix-like environments.

In this lesson, we’ll clarify the often-interchanged terms—**shell**, **CLI**, **terminal**, **console**, **TTY**, and **POSIX**—and explain what POSIX compliance means for your Unix-like environment. Having a consistent vocabulary will help you follow advanced Bash scripting techniques with confidence.

<Frame>
  ![The image shows a diagram with interconnected sections labeled with concepts: Shell, CLI, TTY, Terminal, Console, and POSIX. It is titled "Terminology."](https://kodekloud.com/kk-media/image/upload/v1752868583/notes-assets/images/Advanced-Bash-Scripting-Terminology/terminology-shell-cli-tty-diagram.jpg)
</Frame>

## Shell

A **shell** is a command interpreter: it reads your commands, executes them, and displays results. Different shells offer unique features, scripting syntax, and built-in utilities. Here are some of the most common:

| Shell      | Platform       | Description                             |
| ---------- | -------------- | --------------------------------------- |
| Bash       | Linux, macOS   | Bourne Again Shell; default on many     |
| Zsh        | macOS, Linux   | Z Shell with powerful customization     |
| KornShell  | Unix           | `ksh`; emphasizes scripting consistency |
| PowerShell | Windows, Linux | Object-oriented automation framework    |
| CMD        | Windows        | Legacy command-line interpreter         |

## CLI

A **Command Line Interface (CLI)** is the text-based interface that lets you type commands directly to a shell. While most shells share fundamental capabilities, each CLI might include:

* Unique prompts and themes
* Built-in command history and completion
* Custom scripting hooks

CLI tools often integrate with system components like SSH, Docker, or package managers.

## Terminal

A **terminal**, or terminal emulator, is the application window where your CLI session runs. It renders text, handles keyboard input, and manages multiple tabs or panes.

| Terminal Emulator | Platform | Key Features                     |
| ----------------- | -------- | -------------------------------- |
| GNOME Terminal    | Linux    | Profiles, tabs, custom theming   |
| xterm             | Cross-OS | Lightweight, highly configurable |
| Windows Terminal  | Windows  | Tabbed interface, PowerShell     |

<Callout icon="lightbulb">
  You can run the same shell (e.g., Bash) in different terminal emulators just as you might browse the same website in different web browsers.
</Callout>

## Console

Originally, a **console** was the physical keyboard-and-display unit directly wired into a machine via a dedicated port. Think of a video game console—hardware designed for one system. Modern usage sometimes treats “console” as synonymous with “terminal,” but the historical distinction remains.

<Frame>
  ![The image shows a section labeled "Consoles" with icons of a smartphone, laptop, and game controller, alongside a pixelated ghost and a clicking cursor.](https://kodekloud.com/kk-media/image/upload/v1752868584/notes-assets/images/Advanced-Bash-Scripting-Terminology/consoles-smartphone-laptop-game-controller.jpg)
</Frame>

## TTY

**TTY** stands for teletypewriter. Early terminals were electromechanical devices that functioned like remote printers. Today, Unix-like systems assign each terminal session (for example, a tab or SSH session) a pseudo-TTY number. You can inspect your current TTY with:

```bash theme={null}
tty
