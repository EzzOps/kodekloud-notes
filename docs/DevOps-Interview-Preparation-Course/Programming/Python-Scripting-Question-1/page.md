# Python Scripting Question 1

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Preparation-Course/Programming/Python-Scripting-Question-1/page

This article discusses developing a Python monitoring script for an on-premises Linux server, focusing on using the psutil module for system metrics.

We have an on-premises Linux server that requires continuous monitoring. As a DevOps engineer with exclusive access, your goal is to develop a basic monitoring script using Python.

<Frame>
  ![The image contains a question about setting up a basic monitoring script on an on-premises Linux server, directed at a DevOps engineer.](https://kodekloud.com/kk-media/image/upload/v1752873398/notes-assets/images/DevOps-Interview-Preparation-Course-Python-Scripting-Question-1/monitoring-script-linux-server-devops.jpg)
</Frame>

In this article, you'll learn how to tackle this scenario by leveraging Python scripting, making it an ideal solution for rapid automation and real-world interview discussions.

## Understanding the Requirement

The task is to monitor a Linux server hosted on-premises instead of in the cloud. Python scripting is an essential skill for DevOps engineers because it allows you to quickly test solutions and automate server monitoring. This capability is particularly valuable during job interviews, where you may be asked to outline a step-by-step strategy for monitoring server health.

<Frame>
  ![The image contains text discussing the importance of scripting for DevOps engineers, emphasizing its role in quick testing, automation, and development, and mentions interview scenarios involving scripting and coding knowledge.](https://kodekloud.com/kk-media/image/upload/v1752873399/notes-assets/images/DevOps-Interview-Preparation-Course-Python-Scripting-Question-1/devops-scripting-importance-discussion.jpg)
</Frame>

<Callout icon="lightbulb">
  Make sure to practice explaining your script logically, focusing on how each system metric is monitored.
</Callout>

## The Python psutil Module

One of the most effective tools for system monitoring in Python is the psutil module. This module provides detailed access to system information such as CPU times, memory usage, disk usage, and temperature sensors. To install psutil, run the following command:

```bash theme={null}
pip install psutil
```

## Example Monitoring Script

Below is an example Python script that utilizes the psutil module to gather critical system metrics. The script captures details including CPU times, load averages, virtual memory, swap memory, disk usage, disk I/O counters, and temperature sensors, making it a robust solution for monitoring server performance:

```python theme={null}
import psutil
