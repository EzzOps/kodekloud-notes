# Resource Limits Memory

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine-Security/Resource-Limits-Memory/page

This guide explains how to apply memory constraints to Docker containers and manage Linux memory for improved stability and resource predictability.

In this guide, you’ll learn how to apply memory constraints to Docker containers and understand how Linux handles memory under the hood. Properly limiting container memory prevents individual workloads from exhausting host resources, improving stability and predictability.

## Table of Contents

1. [Linux Memory Allocation](#linux-memory-allocation)
2. [Docker’s Default Memory Behavior](#dockers-default-memory-behavior)
3. [Setting a Hard RAM Limit with `--memory`](#setting-a-hard-ram-limit-with--memory)
4. [Controlling Swap with `--memory-swap`](#controlling-swap-with--memory-swap)
5. [Memory Flags Comparison](#memory-flags-comparison)
6. [Best Practices](#best-practices)
7. [References](#references)

***

## Linux Memory Allocation

A typical Linux host provides:

* **Physical RAM** (e.g., 2 GB, 4 GB, 8 GB)
* **Swap space**: disk-backed extension of RAM

By default, processes may consume all available RAM. Once RAM is exhausted, the kernel resorts to swap. If both RAM and swap fill up, an Out-Of-Memory (OOM) event is triggered, and the kernel terminates processes to free memory.

## Docker’s Default Memory Behavior

Without explicit flags, Docker containers can use all host memory (RAM + swap). This can lead to a single container consuming all resources and destabilizing the host.

> **lightbulb** Always set memory limits in production to avoid unexpected OOM kills on the host.

## Setting a Hard RAM Limit with `--memory`

Use `--memory` (or `-m`) to cap a container’s physical RAM usage. Specify a value with a suffix:

* B (bytes)
* K (kilobytes)
* M (megabytes)
* G (gigabytes)

Example: Limit RAM to 512 MB

```bash theme={null}
docker run --memory=512m my-webapp
```

If the container exceeds this limit, Docker immediately kills the process with an OOM error. Unlike CPU, memory is not throttled—it’s enforced as a hard cap.

> **triangle-alert** Exceeding the `--memory` limit results in an immediate container termination. Monitor your application’s memory usage with tools like [`docker stats`](https://docs.docker.com/engine/reference/commandline/stats/).

## Controlling Swap with `--memory-swap`

By default, setting only `--memory` allows unlimited swap usage (up to the host’s swap). To enforce a combined RAM+swap limit, use `--memory-swap`. The value you provide is the total memory budget:

* Total limit = `--memory` + (`--memory-swap` − `--memory`)

### Common Swap Configurations

1. **Disable swap entirely**\
   Set both flags to the same value:

   ```bash theme={null}
   docker run \
     --memory=512m \
     --memory-swap=512m \
     my-webapp
   ```

   Here, swap available = 512 MB − 512 MB = 0 MB.

2. **Allocate specific swap**\
   Allow 256 MB swap on top of 512 MB RAM:

   ```bash theme={null}
   docker run \
     --memory=512m \
     --memory-swap=768m \
     my-webapp
   ```

   Here, swap available = 768 MB − 512 MB = 256 MB.

## Memory Flags Comparison

| Flag                  | Purpose                                       | Example                            |
| --------------------- | --------------------------------------------- | ---------------------------------- |
| `--memory`            | Hard cap on container’s physical RAM          | `--memory=512m`                    |
| `--memory-swap`       | Total RAM + swap limit (must be ≥ `--memory`) | `--memory=512m --memory-swap=768m` |
| `--memory-swappiness` | Kernel swap tendency (0–100)                  | `--memory-swappiness=10`           |

## Best Practices

* Always set both `--memory` and `--memory-swap` in production.
* Use monitoring (e.g., [`cAdvisor`](https://github.com/google/cadvisor), Prometheus) to track container memory.
* Tune `--memory-swappiness` to control how aggressively a container uses swap.
* Test under load to identify realistic memory requirements.

## References

* [Docker Run Reference](https://docs.docker.com/engine/reference/commandline/run/)
* [Managing Docker Resources](https://docs.docker.com/config/containers/resource_constraints/)
* [Linux Memory Management](https://www.kernel.org/doc/html/latest/admin-guide/mm/index.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/59a97752-06d2-4cac-a4d0-ad4240730912/lesson/7e321934-19ba-4f0c-8178-e0b2104ea403)
