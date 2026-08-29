# Privilege Escalation in Linux

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Security-Specialist-CKS/System-Hardening/Privilege-Escalation-in-Linux/page

This article explores privilege escalation in Linux, focusing on the use of sudo for executing commands with elevated privileges securely.

In this lesson, we explore how privilege escalation works in Linux and why it is critical from a security perspective. Previously, we disabled root user login via SSH because using the root account for routine tasks poses significant security risks. However, performing administrative tasks—such as installing software or conducting system maintenance—still requires elevated privileges.

One of the most effective methods to execute commands with root privileges is through the sudo command. Using sudo enables trusted users to run administrative commands by providing their own password, which not only strengthens security but also creates an audit trail of actions performed.

<Callout icon="lightbulb">
  For enhanced security, always use sudo rather than logging in directly as root.
</Callout>

## Using Sudo Versus Direct Commands

If you attempt to install a package without sudo privileges, you will encounter a permission error:

```bash theme={null}
apt install nginx
E: Could not open lock file /var/lib/dpkg/lock-frontend - open (13: Permission denied)
E: Unable to acquire the dpkg frontend lock (/var/lib/dpkg/lock-frontend), are you root?
```

When you prepend the command with sudo, the system will prompt you for your password, allowing you to proceed with administrative tasks:

```bash theme={null}
sudo apt install nginx
[sudo] password for michael:
```

## Understanding the /etc/sudoers File

The default configuration for sudo is maintained in the `/etc/sudoers` file. This file governs policies for executing commands with elevated privileges and can only be modified by users who have been explicitly granted access. Only users listed in the `/etc/sudoers` file can use sudo, thereby preventing unauthorized root logins.

Below is an excerpt from the `/etc/sudoers` file that demonstrates a granular assignment of privileges:

```bash theme={null}
cat /etc/sudoers
User privilege specification
root    ALL=(ALL:ALL) ALL
