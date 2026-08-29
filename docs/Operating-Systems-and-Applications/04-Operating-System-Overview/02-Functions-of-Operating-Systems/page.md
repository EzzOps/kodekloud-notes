# Functions of Operating Systems

Source: https://notes.kodekloud.com/docs/Operating-Systems-and-Applications/Operating-System-Overview/Functions-of-Operating-Systems/page

Overview of operating system functions, boot process, and core subsystems managing processes, memory, devices, filesystems, security, and system startup

This lesson breaks an operating system (OS) into its working parts and explains who does what. We’ll cover OS history, the typical boot sequence, core subsystems, and how the OS manages running applications.

Quick quiz — what major OS introduced time-sharing and heavily influenced modern OS design?\
A: MS‑DOS, B: UNIX, or C: Windows 95?

Correct answer: B, Unix. Unix (1970s) pioneered time-sharing, multi-user support, and concurrent program execution — features that shaped modern OS architecture.

<Frame>
  <img alt="A multiple-choice slide asks &#x22;What major OS introduced time-sharing and influenced modern design?&#x22; with answer options A: MS‑DOS, B: UNIX, and C: Windows 95. A presenter stands to the right wearing a KodeKloud t-shirt." />
</Frame>

MS‑DOS (1980s) was simple and single-tasking, while Windows 95 popularized consumer GUIs but still depended on DOS roots. Over time, OSes evolved from low-level hardware control and batch processing into multitasking systems with graphical interfaces, now powering phones, servers, embedded devices, and IoT appliances.

## What happens when an OS runs? (Boot and startup sequence)

1. Power-on and hardware checks
   * Firmware (BIOS or UEFI) runs POST (Power-On Self Test) to validate CPU, RAM, and connected devices.

2. Bootloader and kernel load
   * After POST, control transfers to a bootloader (MBR on legacy BIOS, EFI system partition on UEFI). The bootloader finds and loads the kernel into RAM.

3. Kernel takes charge
   * The kernel initializes hardware abstractions, mounts essential filesystems, and starts core services.

4. Authentication and user session
   * Login/auth systems verify credentials and create user sessions with the appropriate permissions.

5. Device drivers and interrupts
   * Drivers translate between hardware and OS. Hardware signals use interrupts so the kernel can react quickly (e.g., keyboard, network packets).

6. Process management (the juggler)
   * The process manager and scheduler create processes/threads and allocate CPU time so multiple programs run concurrently.

7. Memory management (the organizer)
   * Memory manager tracks memory pages, assigns virtual memory, and uses paging/swap when physical RAM is low.

8. File system (the librarian)
   * The file system organizes data on storage: allocation, naming, timestamps, permissions, and directory metadata.

These are OS subsystems that cooperate—often implemented inside the kernel (scheduling, interrupts, memory, drivers) with user-space services for higher-level tasks.

## Core OS roles at a glance

| Subsystem                   | Metaphor   | Primary responsibilities                                        |
| --------------------------- | ---------- | --------------------------------------------------------------- |
| Kernel                      | Boss       | Hardware abstraction, scheduling, memory control, core security |
| Process manager / Scheduler | Juggler    | Create/terminate processes, assign CPU time, manage threads     |
| Memory manager              | Organizer  | Virtual memory, paging, allocation, protecting address spaces   |
| File system                 | Librarian  | Store and retrieve files, enforce permissions and metadata      |
| Device drivers              | Translator | Interface with hardware, implement device-specific protocols    |
| Authentication & security   | Guard      | Validate identity, enforce access control and privileges        |

> **lightbulb** TIP: The kernel is the OS core, but many functions (like process scheduling and some services) appear as coordinated subsystems — sometimes implemented inside the kernel, sometimes in user space for safety and modularity.

To summarize key points:

* An operating system manages hardware and runs applications.
* It’s the bridge between users/apps and the machine.
* OS history moved from punch cards and batch jobs to multitasking, GUIs, mobile, and cloud computing — while the core goal remains making computers usable.
* Internally, an OS is a coordinated collection of subsystems (boss, guard, translator, juggler, organizer, librarian) that load from disk and run from RAM.

<Frame>
  <img alt="A purple presentation slide lists three key OS points: the OS is made of many parts working together; key roles include memory, processes, drivers, security and files; and it loads from disk but runs from RAM. A presenter stands on the right and a small cartoon cat graphic is on the left." />
</Frame>

## Which part manages running applications?

Quiz: Which part of the OS manages running applications?\
A: the file system, B: the kernel, or C: the process manager?

Correct answer: C, the process manager. While the kernel provides overall control and interfaces, the process manager (implemented via the kernel’s scheduler and process-management subsystems) is responsible for creating processes and allocating CPU time so applications can run concurrently.

> **warning** Warning: Don’t conflate the kernel with a single, monolithic program that directly performs all tasks. Modern OSes split responsibilities between kernel-space and user-space for reliability, security, and modularity.

## Zooming out

We defined the OS, traced its history from punch cards to modern systems, and examined the internal roles an OS performs: coordinating hardware, managing processes and memory, handling devices, enforcing security, and organizing storage. Rather than one large program, an operating system is a coordinated collection of parts that keep your machine running.

<Frame>
  <img alt="A presenter stands on the right wearing a KodeKloud t-shirt. On the left is a slide titled &#x22;Identify what's inside the OS&#x22; with a diagram of colored boxes around &#x22;OS&#x22; labeled Boss, Organizer, Librarian, Translator, Juggler, and Guard." />
</Frame>

Further reading and references:

* [Unix history and design principles](https://en.wikipedia.org/wiki/Unix)
* [UEFI specification overview](https://uefi.org/)
* [What is an operating system? (educational overview)](https://developer.ibm.com/articles/os-basics/)
* [Kernel vs user space explained](https://lwn.net/Kernel/Index/)

- [Watch Video](https://learn.kodekloud.com/user/courses/operating-systems-and-applications/module/8cc6f888-e958-4535-904e-22ffe290ae7d/lesson/e4eaba10-5c49-40a8-ba44-a0a17c1f2324)
