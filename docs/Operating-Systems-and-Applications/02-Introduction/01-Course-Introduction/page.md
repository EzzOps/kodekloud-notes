# create the script
echo 'echo "Hello, Kody!"' > script.sh

# try to run it (will likely fail if execute bit is not set)
./script.sh
# Example shell output:
# inspect permissions
ls -l script.sh
# Example output:
# add execute permission for the file owner (user)
chmod u+x script.sh

# verify the permission changed
ls -l script.sh
# Example output:
# run the script again
./script.sh
# Output:
# Hello, Kody!
```

Tip: `chmod u+x` adds execute permission only for the file owner (user). `chmod +x` (without a qualifier) adds execute permission for user, group, and other.

> **warning** Be careful when granting execute permission. Only mark trusted scripts or binaries as executable to avoid running untrusted code.

## Common commands summary

| Task                             | Command example      | What it does                                       |
| -------------------------------- | -------------------- | -------------------------------------------------- |
| List with permissions            | `ls -l filename`     | Shows file type and permission bits                |
| Add execute for owner            | `chmod u+x filename` | Adds execute permission for owner only             |
| Add execute for all              | `chmod +x filename`  | Adds execute permission for user, group, and other |
| Set specific permissions (octal) | `chmod 755 filename` | Set owner `rwx`, group `r-x`, other `r-x`          |

## Quick quiz

What does `chmod +x` do to a file?\
A) delete the file\
B) make the file executable\
C) change its name

Answer: B — it gives execute permission so the file can be run as a script or program.

## Recap

* Permission types are read (`r`), write (`w`), and execute (`x`).
* Permissions apply separately to user (owner), group, and other.
* The first character in `ls -l` shows file type; the next nine characters are the permission bits.
* Use `chmod` to change permission bits (for example, `chmod u+x` to add execute for the owner, or `chmod 755` to set octal permissions).

Next up: running another OS inside your current one — [Virtualization and Containers](https://learn.kodekloud.com/user/courses/virtualization-and-containers).

- [Watch Video](https://learn.kodekloud.com/user/courses/operating-systems-and-applications/module/edbf48fe-cad8-4a13-ad00-644b613f7867/lesson/d93d6fec-f61d-487d-9217-1916725bbfe0)


# Course Introduction

Source: https://notes.kodekloud.com/docs/Operating-Systems-and-Applications/Introduction/Course-Introduction/page

Introductory course covering operating system fundamentals including boot process, CPU scheduling, memory management, drivers, file systems, security, and user interfaces

Imagine this: Netflix streaming in your browser, a game running in a window, and Spotify DJing in the background — all on the same machine at once. They share the same physical resources, yet none of them starves the others. That balance is the job of an operating system (OS).

The OS is the coordinator between hardware and software. It schedules CPU time, allocates and protects memory, manages devices through drivers, organizes files, and enforces security policies. Without these responsibilities, your computer wouldn’t just slow down — it might stop working altogether.

<Frame>
  <img alt="A presenter stands to the right of a dark purple slide titled &#x22;Operating System&#x22; that shows colorful gear icons labeled CPU Handling, Memory Allocation, File Organization, Security, and User Interactions. The presenter wears a black shirt with a KodeKloud logo." />
</Frame>

This course gives you a practical, conceptual, and security-focused view of how modern operating systems work. Below is a quick overview of what we’ll cover and why it matters.

## What you'll learn

* How the OS initializes hardware and boots a system
* How the OS schedules CPU time and supports multitasking
* How memory management and virtual memory protect processes
* How device drivers and system calls connect software to hardware
* How file systems, permissions, and access control protect data
* How the OS integrates security tools and applies updates

## Core responsibilities of an operating system

| Responsibility                |                                                                  What it does | Real-world example                                                   |
| ----------------------------- | ----------------------------------------------------------------------------: | -------------------------------------------------------------------- |
| CPU scheduling & multitasking | Allocates CPU time across processes and threads to keep the system responsive | Prioritizing a video player while keeping background downloads alive |
| Memory management             |      Assigns memory regions, provides virtual memory, and enforces protection | Preventing one app from reading another app’s memory                 |
| Device and driver management  |       Loads drivers, initializes hardware, and provides interfaces to devices | Using network, storage, and USB devices without manual configuration |
| File systems & permissions    | Organizes data into files and directories and enforces ownership/access rules | Files with user/group permissions and journaling for integrity       |
| Security & updates            |  Enforces access control, applies patches, and integrates firewalls/antivirus | Sandboxing apps and installing OS security updates                   |
| User interfaces & APIs        |        Provides GUI/CLI and system calls for applications to request services | Launching apps from a desktop or running commands in a terminal      |

## How the OS coordinates hardware and software (the boot phase)

From power-on to a running desktop or server process, the OS performs several coordinated steps:

1. Firmware/bootloader initializes hardware and loads the kernel.
2. The kernel initializes device drivers and core services.
3. System services and daemons start, providing networking, storage, and user sessions.
4. User-space programs launch, using system calls and APIs to request resources.
5. When requested, the OS performs a graceful shutdown, stopping services and flushing storage.

Understanding these phases helps explain why some boot problems are hardware-related and others are configuration or driver issues.

## Security: protection, updates, and isolation

The OS is your first line of defense. It implements access control, isolates processes, and integrates tools like firewalls and antivirus to limit damage from malicious code. Patching the OS and applying security updates is essential to protect against known vulnerabilities.

<Frame>
  <img alt="A presenter wearing a KodeKloud t-shirt stands on the right. To the left is a slide titled &#x22;Security&#x22; with a purple-themed illustration of a laptop, folders and padlocks representing data protection." />
</Frame>

> **warning** Keep your system and applications updated. Many compromises exploit unpatched OS vulnerabilities or misconfigured permissions.

## User interfaces: GUIs and command lines

You interact with the OS through graphical user interfaces (GUIs) and command-line interfaces (CLIs). The OS handles input events, windowing, menus, and keyboard shortcuts for GUIs, while CLIs provide powerful scripting and automation via shell commands and APIs.

<Frame>
  <img alt="A presentation slide titled &#x22;User Interfaces&#x22; shows stylized purple illustrations of a laptop with UI windows, a game controller, mobile touch interaction, and code snippets. A presenter wearing a KodeKloud t-shirt stands at the right against a dark background." />
</Frame>

> **lightbulb** Pro tip: Learning to use the CLI and understanding basic system calls will make you a more effective administrator and developer. Start with commands for process listing, file permissions, and package management.

## Resource management and process isolation

An OS ensures multiple applications can run concurrently without interfering with each other by:

* Scheduling CPU time and handling interrupts
* Allocating and freeing memory safely
* Using virtual memory for isolation and swapping
* Managing device access through drivers and kernel interfaces

These mechanisms allow servers to host many services and consumer devices to run multiple apps smoothly.

## File systems and permissions

File systems organize data and provide durability and integrity features such as journaling. The OS enforces file ownership and permission bits (or ACLs), ensuring users and processes access only the resources they are allowed to.

## Community and continued learning

At KodeKloud, we encourage questions, discussions, and hands-on practice. Join our community to share problems, solutions, and real-world scenarios that deepen your understanding of operating system internals.

Further reading and references:

* [Kubernetes Documentation](https://kubernetes.io/docs/) — for containerized workloads and OS isolation concepts
* [Linux Kernel Documentation](https://www.kernel.org/doc/html/latest/) — kernel internals and driver development
* [Microsoft Docs — Windows OS](https://learn.microsoft.com/en-us/windows/) — Windows architecture and administration

If you're curious about what keeps your digital environment reliable and responsive, you're in the right place. Let's get started.

- [Watch Video](https://learn.kodekloud.com/user/courses/operating-systems-and-applications/module/a58b0c0b-ab99-487d-8373-0cef2163288e/lesson/05bc3753-622b-4816-a9d2-656bfb7c4142)
