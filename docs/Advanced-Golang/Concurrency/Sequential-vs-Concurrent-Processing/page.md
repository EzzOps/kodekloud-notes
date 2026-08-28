# Sequential vs Concurrent Processing

Source: https://notes.kodekloud.com/docs/Advanced-Golang/Concurrency/Sequential-vs-Concurrent-Processing/page

This article explores the key differences between sequential and concurrent programming, essential for understanding concurrency in Golang and modern programming languages.

In this article, we explore the key differences between sequential and concurrent programming. Understanding these concepts is crucial for grasping how concurrency works in Golang and other modern programming languages.

## Sequential Programming

Sequential programming executes instructions one after another in a strict linear order. Each operation must finish before the next one begins. For instance, consider a simple program that calculates the sum of two numbers. The program might follow these steps:

1. Request the first number from the user.
2. Request the second number from the user.
3. Compute the sum of the two numbers.
4. Return the result.

This fixed, step-by-step order is typical for basic, independent operations.

<Frame>
  ![The image illustrates a sequential processing flow on a CPU core, showing steps to get two numbers, calculate their sum, and return the result.](https://kodekloud.com/kk-media/image/upload/v1752868714/notes-assets/images/Advanced-Golang-Sequential-vs-Concurrent-Processing/cpu-sequential-processing-flow.jpg)
</Frame>

## Multitasking

Modern CPUs enhance sequential execution by employing multitasking. Even on a single-core processor, the CPU rapidly switches between multiple tasks using small time intervals, which gives the illusion of performing several tasks simultaneously.

<Frame>
  ![The image illustrates concurrent processing on a CPU core, showing a sequence of tasks (Task 1, Task 2, Task 3, Task 1, Task 3, Task 1, Task 2, Task 4) being executed in an interleaved manner.](https://kodekloud.com/kk-media/image/upload/v1752868715/notes-assets/images/Advanced-Golang-Sequential-vs-Concurrent-Processing/concurrent-processing-cpu-tasks.jpg)
</Frame>

## Understanding Concurrency

Concurrency refers to the ability to have multiple tasks or processes in progress at the same time. This is primarily achieved through multitasking, where tasks are interleaved on a processor. Note that concurrency is about managing multiple tasks, not necessarily executing them simultaneously.

<Callout icon="lightbulb">
  Concurrency enables more responsive applications by efficiently managing several tasks at once, even if they do not run in parallel.
</Callout>

<Frame>
  ![The image explains "Concurrent Processing," defining concurrency as the notion of multiple things happening simultaneously, with the potential for multiple processes to be in progress at the same time.](https://kodekloud.com/kk-media/image/upload/v1752868716/notes-assets/images/Advanced-Golang-Sequential-vs-Concurrent-Processing/concurrent-processing-definition-diagram.jpg)
</Frame>

### Concurrency in Multicore CPUs

In multicore systems, the benefits of concurrency are amplified. For example, in a system with two cores and two tasks, each core can manage both tasks by switching between them, thereby maximizing the overall processing power. This approach, which leverages multiple cores to handle tasks concurrently, is known as multiprocessing.

<Frame>
  ![The image illustrates concurrent processing with two CPU cores, each alternating between Task 1 and Task 2.](https://kodekloud.com/kk-media/image/upload/v1752868717/notes-assets/images/Advanced-Golang-Sequential-vs-Concurrent-Processing/concurrent-processing-cpu-cores-tasks.jpg)
</Frame>

## Concurrency vs. Parallelism

It's important to distinguish between concurrency and parallelism:

* **Concurrency** involves managing multiple tasks at once, often through rapid task switching. An example is a text editor that lets you type and save a file simultaneously.
* **Parallelism** uses multiple processing units to execute tasks simultaneously. A distributed data processing system that divides tasks across multiple clusters is a typical example of parallel processing.

<Frame>
  ![The image provides examples of concurrent and parallel processing, with concurrent processing related to user-interactive programs and parallel processing related to distributed data processing.](https://kodekloud.com/kk-media/image/upload/v1752868717/notes-assets/images/Advanced-Golang-Sequential-vs-Concurrent-Processing/concurrent-parallel-processing-examples.jpg)
</Frame>

<Callout icon="lightbulb">
  While concurrency improves the efficiency and responsiveness of applications, parallelism takes advantage of hardware by executing tasks simultaneously across multiple cores or processors.
</Callout>

That concludes our discussion on sequential versus concurrent processing. Thank you for reading and happy coding!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-golang/module/5a3833bd-1030-4e53-a886-007bd0b9fbf3/lesson/66b300a4-271e-4adc-8bcd-11445ecf028b" />
</CardGroup>
