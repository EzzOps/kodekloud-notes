# Create 5 note files with initial content
for i in {1..5}; do
  echo "TODO: Add content for note_$i" > "note_$i.txt"
done
```

Inside the terminal sits a shell: the program that reads your commands and asks the OS to run them. Common shells include:

* Windows: PowerShell — [https://learn.microsoft.com/powershell/](https://learn.microsoft.com/powershell/)
* Linux/macOS: Bash — [https://www.gnu.org/software/bash/](https://www.gnu.org/software/bash/)
* Many macOS users now use Z shell (zsh) — [https://www.zsh.org/](https://www.zsh.org/)

The CLI has deep roots. It evolved from teletypes (TTYs) and legacy terminals; that history explains the terminology you still see today.

```text theme={null}
user@hostname: $
```

Many people use both: GUI for day-to-day discoverability and CLI for scripted, repeatable work.

Table: quick comparison

| Interface Type | Best for                                             | Example                                              |
| -------------: | ---------------------------------------------------- | ---------------------------------------------------- |
|            GUI | Discoverability, casual users, touch-based workflows | Open a browser, drag files                           |
|            CLI | Automation, precision, bulk operations               | `for i in {1..5}; do echo "..." > note_$i.txt; done` |
|          Shell | Command interpretation and scripting                 | `bash`, `zsh`, `PowerShell`                          |

<Frame>
  <img alt="A presentation slide titled &#x22;CLI History Timeline&#x22; listing &#x22;01 Teletype,&#x22; &#x22;02 Green-Screen Terminal,&#x22; and &#x22;03 Modern Terminal Window&#x22; on the left. On the right is a presenter (wearing a KodeKloud t-shirt) standing in front of a large purple-toned image of a typewriter." />
</Frame>

Quick checkpoint: which best explains the difference between a GUI and a CLI?

A: CLI talks to hardware directly.
B: GUI is visual, CLI is typed, but both use the same OS.
C: CLI is only for developers.

<Frame>
  <img alt="A dark-themed quiz slide asking &#x22;Which best explains the difference between a GUI and a CLI?&#x22; with multiple-choice answers. A presenter wearing a KodeKloud shirt stands on the right." />
</Frame>

Correct answer: B — GUI and CLI are different ways to interact with the same operating system.

***

## Application lifecycle: install, launch, run, quit, and uninstall

The OS controls an app's lifecycle from installation to removal, managing resources and permissions along the way.

Installing apps

* Mobile (Android/iOS): typically via an app store.
* Desktop (Windows/macOS/Linux): download an installer, use a system store, or use a package manager such as Homebrew on macOS or Linux.

Example: install htop with Homebrew

```bash theme={null}
# Example: install htop with Homebrew on macOS or Linux
brew install htop
```

When you install, the OS places files, sets permissions, registers the app, and tracks metadata so it can update or remove the app later.

Launching apps

* Tap an icon, select from a menu, or run the app from a terminal.
* Open a file and the OS uses file associations to pick the right app.

Example: start htop from the terminal

```bash theme={null}
# Start htop (a terminal system monitor)
htop
```

Running apps

* The OS manages memory, CPU scheduling, and resource limits.
* Foreground apps usually get higher scheduling priority; background apps may be paused, limited, or throttled.
* Background services often continue running (downloads, syncs, music).

Example snapshot of a terminal-based system monitor (trimmed for clarity):

```text theme={null}
alan — ubuntu@ubuntu: ~ — htop — 80x17

CPU%                                     Mem[||||||||||||||||||||] 6.07G/8.00G
0  [||||||||||||||||||||||||||||||||||]   Load average: 2.49 3.87 4.57
Tasks: 564, Threads: 2510; Running: 2  Uptime: 6 days, 04:34:37

  PID  USER   PRI  NI  VIRT    RES    S  CPU%  %MEM   TIME+  Command
 683  alan    17   0  407G  29.7M  R   2.1   0.4   16:05.71  /System/Library/...
67829 alan    17   0  392G  44.4M  R   0.5   0.5    0:00.06  /usr/sbin/...
 640  alan    17   0  392G  57.6M  S   0.2   0.7    1:58.40  /System/Application/...
F1Help  F2Setup  F3Search  F4Filter  F5Tree  F6SortBy  F7Nice  F8Nice  F9Kill
```

Quitting vs. switching

* Completely quitting or swiping an app away typically frees memory and resources.
* Minimizing or switching away often just hides the UI; the OS decides whether to keep the process running or to pause/terminate it to reclaim resources.
* Mobile platforms often pause apps and resume them later; the OS handles lifecycle transitions and resource cleanup.

Uninstalling

* Mobile: press and hold an icon and select remove.
* Desktop: use an uninstaller, drag to Trash/Recycle Bin, or remove via a package manager.

<Frame>
  <img alt="A presenter wearing a KodeKloud shirt stands to the right of the frame next to screenshots of a smartphone home screen and a Mac Applications window. Overlaid purple text reads, &#x22;Removing apps looks different, but the OS always does the work.&#x22;" />
</Frame>

Swiping an app from the app switcher or choosing “Quit” will terminate it; simply minimizing or closing a window often only hides it. The OS continuously balances responsiveness and resource use by deciding what stays active, what is paused, and what is terminated.

<Frame>
  <img alt="A presenter stands on the right wearing a black KodeKloud t-shirt. On the left are three purple info panels (01–03) explaining app behavior — swiping up/quitting closes the app, switching/minimizing leaves it running, and the OS manages background memory." />
</Frame>

Recap

* GUI = visual, intuitive, and discoverable.
* CLI = typed, precise, and scriptable (great for automation).
* The OS is the intermediary: receiving input, running apps, managing resources, and enforcing security and accessibility.
* App lifecycle includes install → launch → run → quit → uninstall, and the OS orchestrates each step.

Further reading and references:

* Graphical User Interface concepts: [https://en.wikipedia.org/wiki/Graphical\_user\_interface](https://en.wikipedia.org/wiki/Graphical_user_interface)
* Command Line basics and shells: [https://en.wikipedia.org/wiki/Command-line\_interface](https://en.wikipedia.org/wiki/Command-line_interface)
* Homebrew package manager: [https://brew.sh](https://brew.sh)
* htop system monitor: [https://htop.dev](https://htop.dev)

<Callout icon="warning">
  Tip: Don’t assume swiping an app away always stops background activity. Many systems pause apps rather than fully quit them. Check your OS documentation for app lifecycle specifics and battery/resource implications.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/operating-systems-and-applications/module/cd9f643e-0d2b-462e-9db6-701cf653e03f/lesson/c0fb6ae9-fc86-4503-81a5-f13aae062514" />
</CardGroup>


# OS User Interface Part 2

Source: https://notes.kodekloud.com/docs/Operating-Systems-and-Applications/User-InterfacesUI/OS-User-Interface-Part-2/page

How operating systems mediate hardware access for applications via APIs, system calls, drivers, event normalization, and accessibility to ensure safety, simplicity, and stability

Applications never get unrestricted access to hardware. They can't write directly to disk, play audio through speakers, or draw pixels on the screen by themselves. The operating system is the gatekeeper that mediates every hardware request.

## How apps get things done

Apps request services through two related layers:

* A high-level API (application programming interface): the functions and conventions apps call (for example, "save this file" or "play this sound").
* A low-level kernel interface implemented as system calls: the controlled entry points the kernel exposes to perform hardware operations.

When an app calls an API function, that function typically ends up invoking one or more system calls. The kernel validates permissions, and then uses device drivers to talk to physical hardware. Device drivers usually run in kernel space (though some run in user space).

Example (typical flow):
app → API/library → system call → kernel → device driver → hardware

Simple C-style system call example:

```c theme={null}
int fd = open("file.txt", O_WRONLY | O_CREAT, 0644);
write(fd, "Hello\n", 6);
close(fd);
```

A higher-level function such as `fopen()` or `std::ofstream` may call `open()`/`write()` under the hood.

Quick practical check: you can observe system calls made by a utility with tools like `strace`:

```bash theme={null}
strace -e trace=open,write ls
```

Utilities like `ls` rely on system calls such as `getdents`, `stat`, and `write` to list directory contents and print output.

<Frame>
  <img alt="A presenter wearing a KodeKloud t-shirt stands on the right side of the image. On the left are three purple slide panels numbered 01–03 with text about apps asking for access, the OS acting as a gatekeeper, and protecting your data." />
</Frame>

## Why this design?

There are three primary goals behind this separation of concerns:

| Goal       | What it prevents or enables                                                                                     |
| ---------- | --------------------------------------------------------------------------------------------------------------- |
| Safety     | Prevents apps from performing arbitrary or malicious operations that could compromise the system or other apps. |
| Simplicity | Lets app developers rely on stable, well-documented APIs without needing to know hardware specifics.            |
| Stability  | Keeps the OS in control of resources, reducing crashes and data corruption when apps fail.                      |

Quick checkpoint:
Which of these best explains how apps interact with your device's hardware?

A. The app uses built-in drivers to manage hardware directly.\
B. The app requests services from the OS, which handles hardware access.\
C. The OS only gets involved if the app crashes or needs memory.

Correct answer: B — apps request services from the OS. The OS enforces permissions and carries out hardware access via system calls and drivers.

## Input and output: normalized events

Every user action — tapping, typing, clicking, or swiping — starts as raw input from device drivers. The OS interprets those raw events (for example, determining a touch position or a keypress) and dispatches standardized event objects to the focused application or to system subsystems.

Output is handled similarly: when an app wants to display text, render graphics, play audio, or trigger haptics, it requests those outcomes from the OS. The OS decides how to draw pixels, mix audio, or route haptics to the appropriate hardware.

<Frame>
  <img alt="A dark slide graphic on the left shows a flow diagram titled &#x22;App asks – The OS outputs&#x22; with icons for popup, sound, vibrates mapping to Screen, Speaker, and Haptics outputs. On the right a man in a black KodeKloud shirt is standing and gesturing as he presents." />
</Frame>

## Modern input modalities

Operating systems normalize many input types so apps can handle them consistently. Examples include:

| Input modality               | How the OS helps                                                                        |
| ---------------------------- | --------------------------------------------------------------------------------------- |
| Mouse / Touch / Keyboard     | Translated into pointer and keyboard events with coordinates, button/state information. |
| Voice                        | Converted to text or commands via speech recognition frameworks.                        |
| Stylus                       | Provides pressure, tilt, and precise coordinates through a common API.                  |
| Game controllers             | Exposed via standardized gamepad APIs with mapping for buttons/axes.                    |
| Eye tracking / Face tracking | Normalized gaze or face landmarks exposed as events or state objects.                   |

<Frame>
  <img alt="A slide shows a colorful OS graphic with icons and labels for Voice, Stylus, Gamepad, and Eye tracking. A presenter stands to the right wearing a black KodeKloud t-shirt and gesturing toward the slide." />
</Frame>

Because the OS exposes consistent event formats and APIs, application developers rarely have to write custom code for each hardware model. Instead, they handle canonical events and let the OS map device specifics to those events.

## Accessibility as a core feature

Accessibility features are integrated into every major OS, not bolted on as optional extras. Common accessibility capabilities include:

* High-contrast and large-text modes for low-vision users
* Screen readers and text-to-speech for blind users
* Closed captions and audio descriptions for hearing-impaired users
* Voice control and alternative input methods for motor impairments
* Speech-to-text and dictation for users with speech differences

Many accessibility features also benefit general users: dark mode, captions, dictation, and system-wide zoom are broadly useful beyond assistive scenarios.

## Recap

* Users interact with the OS through graphical and command-line interfaces.
* Apps are managed by the OS and request services via APIs that invoke system calls.
* The OS normalizes diverse inputs and routes outputs, providing a single, stable interface for apps.
* Accessibility is a first-class OS responsibility to make devices usable for more people.

<Callout icon="lightbulb">
  Key idea: Apps ask, the OS decides, and the kernel (via system calls and drivers) talks to the hardware. This separation provides safety, simplicity, and stability.
</Callout>

In the next lesson we'll examine how the OS schedules work, manages processes and threads, and allocates resources behind the scenes.

## Links and references

* [Kernel and system calls overview](https://en.wikipedia.org/wiki/System_call)
* [strace — trace system calls and signals](https://strace.io/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Accessibility in operating systems (concepts)](https://www.w3.org/WAI/standards-guidelines/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/operating-systems-and-applications/module/cd9f643e-0d2b-462e-9db6-701cf653e03f/lesson/ec9ce52a-ccd8-4111-9ddd-33e8eaad997d" />
</CardGroup>
