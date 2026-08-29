# Stopping and Removing a Container

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine/Stopping-and-Removing-a-Container/page

This guide covers managing Docker containers, including stopping, pausing, resuming, and removing them, along with Linux signal mappings and cleanup best practices.

In this guide, we’ll explore how to manage Docker containers by stopping, pausing, resuming, and removing them. You’ll also learn how Linux signals map to Docker commands, plus best practices for cleaning up containers to reclaim resources.

***

## 1. Linux Signals Refresher

Linux processes respond to signals for control and shutdown. Below is a quick overview:

| Signal  | Action            | Description                                |
| ------- | ----------------- | ------------------------------------------ |
| SIGSTOP | Pause             | Suspends the process, cannot be caught.    |
| SIGCONT | Resume            | Continues a paused process.                |
| SIGTERM | Graceful shutdown | Allows process cleanup before exit.        |
| SIGKILL | Forceful kill     | Immediately terminates; cannot be trapped. |

```bash theme={null}
