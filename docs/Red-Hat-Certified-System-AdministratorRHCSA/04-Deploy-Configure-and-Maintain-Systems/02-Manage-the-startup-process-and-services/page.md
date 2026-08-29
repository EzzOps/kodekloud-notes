# Manage the startup process and services

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Deploy-Configure-and-Maintain-Systems/Manage-the-startup-process-and-services/page

Learn to manage Linux startup processes and services using systemd, including handling service dependencies, restarts, and configurations.

In this article, you'll learn how to manage Linux startup processes and services effectively. We will discuss how systemd—the init system—handles the startup sequence, restarts failed applications, and orchestrates service dependencies.

When Linux boots, several critical applications launch automatically in a defined order. For instance, if "app2" depends on "app1", then app1 starts before app2. This ordered process happens seamlessly behind the scenes. Furthermore, if a vital application crashes, systemd automatically restarts it to maintain system reliability.

## Understanding the Init System and Service Units

The core mechanism responsible for this operation is the init system (short for initialization system). It reads configuration files called "units" that provide detailed instructions on how to:

* Start the system and individual services.
* Handle unexpected crashes.
* Reload configurations or restart services.

Service units—files ending with a `.service` extension—specifically define how to manage applications. A typical service unit describes:
• The command to launch an application.
• The behavior when a program crashes.
• Commands to reload configurations or restart the service.

To explore all available options for a service unit, run:

```bash theme={null}
$ man systemd.service
```

This command opens the manual page that explains the configuration options for service units:

```text theme={null}
SYSTEMD.SERVICE(5)                          systemd.service                          SYSTEMD.SERVICE(5)

NAME
       systemd.service - Service unit configuration

SYNOPSIS
       service.service

DESCRIPTION
       A unit configuration file whose name ends in ".service" encodes
       information about a process controlled and supervised by systemd.

       This man page lists the configuration options specific to this unit
       type. See systemd.unit(5) for the common options of all unit
       configuration files. The common configuration items are configured in
       the generic "[Unit]" and "[Install]" sections. The service specific
       configuration options are configured in the "[Service]" section.
```

## Example: Managing the SSH Daemon

For many servers, the SSH daemon is essential for remote connectivity. The SSH service unit guides systemd on how to start and maintain the daemon. To inspect this service file, use the command:

```bash theme={null}
$ systemctl cat sshd.service
```

You might see output similar to this:

```plaintext theme={null}
