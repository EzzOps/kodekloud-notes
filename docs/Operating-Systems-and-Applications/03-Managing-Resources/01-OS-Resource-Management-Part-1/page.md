# OS Resource Management Part 1

Source: https://notes.kodekloud.com/docs/Operating-Systems-and-Applications/Managing-Resources/OS-Resource-Management-Part-1/page

Explains how operating systems schedule CPU time, context switching, and different policies like round-robin, priority and FCFS to enable multitasking on single and multi-core systems.

Imagine your computer running a single app — for example, a calculator. The CPU focuses entirely on that one task, RAM holds only that program, and there’s no sharing or switching. This is basic computing: one core, one process, no interruptions. Early computers and many microcontrollers still operate like this.

Modern desktops and laptops are different. When you open a browser, play music, and run a terminal at the same time, many tasks compete for the same CPU core. The operating system (OS) must juggle them while keeping the system responsive.

In this article we build the picture step by step:

* Start with one core and one task.
* Add more tasks and see how the OS decides who gets the CPU next.
* Learn how the system switches between tasks (context switching).
* Inspect how a process can contain multiple threads.
* Scale up to multiple cores and explain true parallelism.
* Finally, examine interrupts and how the OS responds instantly to events like key presses or device plugs.

## Single-core, multiple tasks: concurrency through time slicing

Each running program is a process. The scheduler — part of the OS kernel — decides which process runs, how long it runs, and in what order. Because a single core can execute only one instruction stream at a time, the OS shares CPU time by giving each process short bursts of CPU time called a time slice or quantum. The kernel switches between processes, creating concurrency: many tasks making progress by taking turns.

Here’s a concrete example. Suppose:

* P1 needs 5 ms to complete.
* P2 needs 3 ms.
* P3 needs 2 ms.
  All arrive at time 0. The OS can schedule them in many ways; three common policies are round-robin, priority, and first-come, first-served (FCFS).

With round-robin scheduling, each process gets an equal time slice, for example 2 ms. The CPU rotates: P1 → P2 → P3 → P1 → P2 → P1, and processes finish when they've accumulated their required CPU time. Round-robin is fair and predictable, but short tasks can be delayed waiting for the rotation.

<Frame>
  <img alt="A slide explaining Round Robin CPU scheduling with Gantt and timeline charts showing colored bars for processes P1, P2, and P3 and a table of arrival/process times. A presenter stands at the right wearing a KodeKloud shirt." />
</Frame>

Priority scheduling executes the highest-priority task first. If P2 has the highest priority, it runs immediately and finishes in 3 ms, then the scheduler runs P1 (5 ms), then P3 (2 ms). Priority scheduling is ideal for time-sensitive tasks (audio playback, interrupts), but it can starve low-priority tasks unless the scheduler implements aging or other anti-starvation techniques.

<Frame>
  <img alt="A presenter wearing a black KodeKloud t-shirt gestures on the right side of the image. The slide on the left shows Gantt and timeline charts and a table titled &#x22;Priority Scheduling: Urgent tasks jump the queue.&#x22;" />
</Frame>

FCFS runs processes in arrival order. If P1 arrives first, the OS runs it to completion, then runs P2, then P3. FCFS is simple, but a long job arriving first can delay everything else — the so-called “convoy effect.”

<Frame>
  <img alt="A slide showing Gantt and timeline charts illustrating First-Come First-Serve CPU scheduling with a table of process arrival and run times. A presenter stands to the right wearing a black T‑shirt with a &#x22;KodeKloud&#x22; logo." />
</Frame>

### Scheduling policy comparison

| Policy      | How it works                                      | Pros                                            | Cons                                                       |
| ----------- | ------------------------------------------------- | ----------------------------------------------- | ---------------------------------------------------------- |
| Round-robin | Each process gets a fixed time slice; CPU rotates | Fair, predictable latency for interactive tasks | Short tasks may wait for rotation; context-switch overhead |
| Priority    | Run highest-priority task first                   | Low-latency for critical tasks                  | Can starve low-priority jobs without mitigations           |
| FCFS        | Run in arrival order, to completion               | Simple, easy to implement                       | Long jobs block others (convoy effect)                     |

Quick quiz:

Which of these best explains how a single-core system handles multiple processes?

A. Each process runs in full before the next starts.\
B. Processes run at the same time using multitasking.\
C. The OS gives each process a short turn, switching rapidly between them.

Correct answer: C. On one core only one thing runs at a time. The OS switches rapidly between processes so each makes progress — this is concurrency.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; shows three numbered boxes explaining OS scheduling, concurrency, and tweaking scheduling order. An instructor wearing a KodeKloud T‑shirt stands to the right." />
</Frame>

## Context switching: how the kernel switches tasks

When P1 is running and its time slice ends, the OS performs a context switch. The kernel saves P1’s context — CPU registers, program counter (instruction pointer), stack pointer, and other architecture-specific state — effectively a bookmark that lets P1 resume later. The OS then loads P2’s saved context and resumes execution where P2 left off. On busy systems this happens thousands of times per second.

Context switches are necessary for concurrency, but they have overhead:

* Saving and restoring processor state consumes CPU cycles.
* Switching can flush CPU caches and translation lookaside buffers (TLBs), hurting performance.
* Switching between threads in the same process is usually cheaper than switching between processes because threads share address space and many kernel structures.

The scheduler balances trade-offs: responsiveness, throughput, and fairness. Different kernels and configurations implement variations such as preemptive vs. cooperative scheduling, multi-level feedback queues, and real-time classes to meet workload and latency requirements.

<Frame>
  <img alt="A presenter stands on the right next to a graphic of a balance scale comparing &#x22;Speed&#x22; (represented by a rocket) and &#x22;Fairness&#x22; (represented by a ribbon with gender symbols). Text below says &#x22;The OS balances performance and fairness.&#x22;" />
</Frame>

Quick pop quiz:

Why does context switching come with a performance cost?

A. The OS has to restart the entire process each time.\
B. The OS duplicates memory between processes.\
C. The OS has to save and restore CPU state for each switch.

Correct answer: C. During a switch the OS checkpoints and restores the CPU and execution state. That work takes time and can flush useful cached state.

<Frame>
  <img alt="A dark presentation slide asks &#x22;Why does context switching come with a performance cost?&#x22; with three multiple-choice answers listed. A presenter stands to the right wearing a black KodeKloud t-shirt." />
</Frame>

## Summary

* A single core can only run one instruction stream at a time. The OS scheduler divides CPU time into quanta and switches rapidly between processes to create concurrency.
* Scheduling policies (round-robin, priority, FCFS, and many variants) trade off fairness, latency, and throughput.
* Context switches save and restore execution state. They enable multitasking but impose overhead that affects performance.
* Switching between threads of the same process is usually cheaper than switching between processes because threads share virtual memory and kernel resources.

<Frame>
  <img alt="A dark presentation slide titled &#x22;Summary&#x22; shows two purple info boxes about the OS saving/restoring process state and that switching takes time. A man in a black KodeKloud t-shirt stands on the right, gesturing as he speaks." />
</Frame>

> **lightbulb** Note: Scheduling and context switching are kernel-level activities. Modern kernels implement variations (preemptive vs. cooperative scheduling, multi-level queues, real-time classes) to meet different workload and latency requirements.

## Links and references

* [Linux scheduler overview](https://www.kernel.org/doc/html/latest/scheduler/index.html)
* [Operating system concepts — scheduling (Wikipedia)](https://en.wikipedia.org/wiki/Scheduling_\(computing\))
* Tanenbaum, A. S., & Bos, H. (Modern Operating Systems) — for deeper study of scheduling algorithms and context switching principles.

- [Watch Video](https://learn.kodekloud.com/user/courses/operating-systems-and-applications/module/f1c2dfb7-7917-4c97-be15-ba6300068f41/lesson/1d5fb24a-5e68-428c-8679-3419097d38c7)
