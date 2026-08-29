# Manage the startup process and services In Services Configuration

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/Operation-of-Running-Systems/Manage-the-startup-process-and-services-In-Services-Configuration/page

This guide teaches how to inspect, configure, and control services on a Linux system using systemd.

In this guide, you’ll learn how to inspect, configure, and control services on a Linux system using **systemd**—the modern init system. We cover unit files, service management commands, and best practices for maintaining your server’s services.

***

## Table of Contents

1. [Introduction to systemd](#introduction-to-systemd)
2. [Unit File Types](#unit-file-types)
3. [Service Unit Structure](#service-unit-structure)
4. [Inspecting the SSH Daemon Service](#inspecting-the-ssh-daemon-service)
5. [Editing and Reverting a Unit](#editing-and-reverting-a-unit)
6. [Monitoring Service Status](#monitoring-service-status)
7. [Managing Service Lifecycle](#managing-service-lifecycle)
8. [Enabling and Disabling at Boot](#enabling-and-disabling-at-boot)
9. [Masking and Unmasking Services](#masking-and-unmasking-services)
10. [Listing All Service Units](#listing-all-service-units)
11. [Further Reading](#further-reading)

***

## Introduction to systemd

When Linux boots, **systemd** orchestrates service startup in parallel while respecting dependencies. If a critical service fails, systemd can restart it automatically, ensuring high availability. All behavior is defined by **unit files**—plain-text configurations that tell systemd how to manage resources.

<Callout icon="lightbulb">
  Learn more about systemd on the [Official Freedesktop Wiki](https://www.freedesktop.org/wiki/Software/systemd/).
</Callout>

***

## Unit File Types

Unit files end in `.service`, `.socket`, `.device`, `.timer`, and more. Here’s a quick overview:

| Unit Type | Description                                      |
| --------- | ------------------------------------------------ |
| service   | Defines how to start, stop, and manage a service |
| socket    | Configures socket activation                     |
| target    | Groups units and handles synchronization         |
| timer     | Schedules tasks similar to cron                  |

***

## Service Unit Structure

Service units reside in `/etc/systemd/system/` or `/usr/lib/systemd/system/`. They have three main sections:

```ini theme={null}
[Unit]
Description=Human-readable description
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/myapp
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Key directives:

* **ExecStart**: Command to launch the service
* **ExecReload**: How to reload without a full restart
* **Restart**: Policy (`no`, `on-failure`, `always`)

Consult the manual for all options:

```bash theme={null}
man systemd.service
```

***

## Inspecting the SSH Daemon Service

Most servers run the OpenSSH daemon (`sshd`) as a systemd service. View its complete unit file:

```bash theme={null}
$ systemctl cat sshd.service
