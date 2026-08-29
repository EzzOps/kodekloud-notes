# Privilege Escalation

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Kubernetes-Threat-Model/Privilege-Escalation/page

This article explains how to use sudo for privilege escalation on Linux, enhancing security by allowing controlled access to superuser commands.

Privilege escalation allows a non-root user to perform tasks requiring superuser rights. Instead of enabling direct root logins—which poses security risks—you can delegate specific commands to trusted users via `sudo`. This approach enforces the [principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege) and keeps your system secure.

## Why Use sudo?

* Grants temporary elevated rights without sharing the root password
* Provides an audit trail of executed commands
* Limits users to only the commands they need

### Attempting a Restricted Operation

Without `sudo`, installing packages fails:

```bash theme={null}
$ apt install nginx
E: Could not open lock file /var/lib/dpkg/lock-frontend - open (13: Permission denied)
E: Unable to acquire the dpkg frontend lock (/var/lib/dpkg/lock-frontend), are you root?
```

### Elevate with sudo

Prepend `sudo`, authenticate with your own password, and the command succeeds:

```bash theme={null}
$ sudo apt install nginx
[sudo] password for michael: 
```

<Callout icon="lightbulb">
  If you see `User michael is not in the sudoers file`, add your user to the `sudo` group or update `/etc/sudoers` accordingly.
</Callout>

## Configuring sudo: /etc/sudoers

All `sudo` policies live in `/etc/sudoers` and included files under `/etc/sudoers.d/`. Always edit with `visudo` to prevent syntax errors:

```bash theme={null}
sudo visudo
```

Here’s a sample excerpt:

```bash theme={null}
