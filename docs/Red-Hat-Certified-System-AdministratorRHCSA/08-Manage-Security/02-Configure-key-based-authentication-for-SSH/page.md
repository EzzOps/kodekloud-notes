# Configure key based authentication for SSH

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Manage-Security/Configure-key-based-authentication-for-SSH/page

This guide covers configuring SSH servers and clients on Linux, focusing on enhancing security through key-based authentication.

Welcome to this comprehensive guide on configuring SSH servers and clients on Linux. In this tutorial, you will learn how to modify the settings for both the SSH daemon (server) and the SSH client with an emphasis on enhancing security using key-based authentication.

──────────────────────────────────────────────

## Configuring the SSH Server (sshd)

The main configuration file for the SSH server is located at `/etc/ssh/sshd_config`. Since the OpenSSH daemon runs by default, you can begin modifying its settings immediately.

### Editing the Configuration File

Start by opening the SSH server configuration file with Vim:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ sudo vim /etc/ssh/sshd_config
```

At the top of the file, you will find numerous comments that outline the default settings and parameters. For instance:

```bash theme={null}
