# date -s '19 APR 2012 22:00:00'
date: cannot set date: Operation not permitted
```

You can inspect the container’s process status by reading `/proc/1/status`. The Seccomp field should indicate a value of 2, meaning a filtered Seccomp profile is in use.

### Seccomp Modes

Seccomp operates in three distinct modes:

* **Mode 0:** Seccomp is disabled.
* **Mode 1:** Strict mode, permitting only four syscalls: read, write, exit, and sigreturn.
* **Mode 2:** Filter mode, allowing a defined subset of syscalls based on a filtering profile. Our container example uses Mode 2.

The diagram below summarizes these modes:

<Frame>
  ![The image outlines three syscall restriction modes: Mode 0 (DISABLED), Mode 1 (STRICT), and Mode 2 (FILTERED).](https://kodekloud.com/kk-media/image/upload/v1752871751/notes-assets/images/Certified-Kubernetes-Security-Specialist-CKS-Restrict-syscalls-using-seccomp/frame_220.jpg)
</Frame>

<Callout icon="lightbulb">
  Docker automatically applies a default Seccomp filter if your host supports Seccomp. This default filter is defined via a JSON document that whitelists approximately 60 syscalls.
</Callout>

## Default Docker Seccomp Profile

The default Docker profile is designed to block dangerous syscalls such as ptrace, which was exploited in the Dirty COW vulnerability. Here is an example snippet of a default Seccomp JSON profile used by Docker:

```json theme={null}
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": [
    "SCMP_ARCH_X86_64",
    "SCMP_ARCH_X86",
    "SCMP_ARCH_X32"
  ],
  "syscalls": [
    {
      "names": [
        "arch_prctl",
        "brk",
        "capget",
        "capset",
        "mkdir",
        "close",
        "execve",
        "...",
        "clone"
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

The key elements of any Seccomp JSON profile are:

1. **Architectures** – Defines the supported CPU architectures (e.g., x86\_64, x86, x32).
2. **Syscalls** – An array listing syscall names and their permitted actions.
3. **Default Action** – Determines how to handle syscalls not explicitly listed. Whitelist profiles typically deny undeclared syscalls.

A **whitelist profile** explicitly allows certain syscalls while denying all others:

```json theme={null}
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": [
    "SCMP_ARCH_X86_64",
    "SCMP_ARCH_X86",
    "SCMP_ARCH_X32"
  ],
  "syscalls": [
    {
      "names": [
        "<syscall-1>",
        "<syscall-2>",
        "<syscall-3>"
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

In contrast, a **blacklist profile** allows all syscalls by default and only denies those specifically listed:

```json theme={null}
{
  "defaultAction": "SCMP_ACT_ALLOW",
  "architectures": [
    "SCMP_ARCH_X86_64",
    "SCMP_ARCH_X86",
    "SCMP_ARCH_X32"
  ],
  "syscalls": [
    {
      "names": [
        "<syscall-1>",
        "<syscall-2>",
        "<syscall-3>"
      ],
      "action": "SCMP_ACT_ERRNO"
    }
  ]
}
```

<Callout icon="triangle-alert">
  While blacklist profiles are easier to implement, they are inherently less secure compared to whitelist profiles due to the possibility of overlooking dangerous syscalls.
</Callout>

The default Docker Seccomp profile on x86 blocks around 60 syscalls related to functions such as system time adjustments, file system mounts, and kernel module loading. This is why changing the system time in our earlier container failed:

```bash theme={null}
docker run -it --rm docker/whalesay /bin/sh
#
# date -s '19 APR 2012 22:00:00'
date: cannot set date: Operation not permitted
```

For a complete list of blocked syscalls, refer to the [Docker documentation](https://docs.docker.com/engine/security/seccomp/).

## Custom Seccomp Profiles

Although Docker’s default profile enhances security by restricting many dangerous syscalls, you can further harden your container by using a custom Seccomp profile. For example, to block the mkdir syscall, you might modify the default filter and save it as custom.json:

```json theme={null}
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": [
    "SCMP_ARCH_X86_64",
    "SCMP_ARCH_X86",
    "SCMP_ARCH_X32"
  ],
  "syscalls": [
    {
      "names": [
        "arch_prctl",
        "brk",
        "capget",
        "capset",
        "close",
        "execve",
        "clone"
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

Start a container using your custom profile with the --security-opt flag:

```bash theme={null}
docker run -it --rm --security-opt seccomp=/root/custom.json docker/whalesay /bin/sh
```

Within this container, attempting to create a directory using mkdir will result in an error:

```bash theme={null}
/ #
/ # mkdir test
mkdir: can't create directory 'test': Operation not permitted
```

It is also possible to disable Seccomp entirely using the "unconfined" flag, though this is strongly discouraged:

```bash theme={null}
docker run -it --rm --security-opt seccomp=unconfined docker/whalesay /bin/sh
#
```

Even without a Seccomp profile, certain syscalls (like those used to change the system time) may remain blocked by additional Docker security measures:

```bash theme={null}
docker run -it --rm --security-opt seccomp=unconfined docker/whalesay /bin/sh
# date -s '19 APR 2012 22:00:00'
date: cannot set date: Operation not permitted
```

Additional security layers are discussed in further lessons.

***

For more guidance on Docker security and related topics, please refer to the [Docker Documentation](https://docs.docker.com/engine/security/seccomp/) and other linked resources.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-security-specialist-cks/module/d67be5ee-871d-4435-a187-382610cb6a1f/lesson/5e9b6232-59d3-44b3-8716-a5dfe51a2411" />
</CardGroup>


# SSH Hardening

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Security-Specialist-CKS/System-Hardening/SSH-Hardening/page

Learn to enhance the security of SSH on Linux servers through key-based authentication and configuration modifications.

SSH is a critical service used to log into remote Linux servers and execute commands securely. In this lesson, you'll learn how to harden SSH to enhance the security of your nodes.

## Overview

Connecting to a remote server typically involves using the ssh command with the server’s IP address or hostname. You can specify the remote user by either prepending the username followed by an @ symbol (e.g., user\@hostname) or by using the -l flag. Remember, the remote server must have the SSH service running and allow connections through port 22.

Also, valid authentication credentials are required to access the server. These credentials can be either a username and password combination or an SSH key pair for a passwordless login. In the following sections, we first explore basic SSH usage and then move on to setting up SSH key pairs.

## Basic SSH Connection

To connect from your laptop to a Linux host named node01, simply run:

```bash theme={null}
ssh node01
```

If no username is specified, SSH will use your local username (for example, mark). When connected, you will be prompted to enter the password for that user on the remote system. In this scenario, your laptop acts as the client while node01 functions as the server running the SSH service.

<Callout icon="lightbulb">
  If you encounter connection issues, ensure that the SSH service is active on the remote server and that port 22 is open.
</Callout>

## Using SSH Key Pairs for Authentication

A more secure authentication method involves using a cryptographic key pair—composed of a private key on the client and a public key installed on the remote server. With this setup, you can log in without repeatedly entering a password.

### Generating an SSH Key Pair

Generate the key pair on your client (e.g., your laptop) using the ssh-keygen command:

```bash theme={null}
ssh-keygen -t rsa
```

During generation, you will be prompted to enter a passphrase. Although optional, adding a passphrase increases security in case your private key is compromised. Note that using a passphrase will require you to enter it each time the key is used. The keys are stored in a hidden directory within your home folder (.ssh), with the public key typically named id\_rsa.pub and the private key as id\_rsa.

Example output:

```bash theme={null}
ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/home/mark/.ssh/id_rsa): 
/home/mark/.ssh/id_rsa already exists.
Overwrite (y/n)? y
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/mark/.ssh/id_rsa.
Your public key has been saved in /home/mark/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:[SECRET_REDACTED] mark@localhost
The key's randomart image is:
+---[RSA 2048]----+
|      .o=oo+    |
|       +E=++    |
|      o * o=. o |
|       = o*.o.   |
|      S o + .    |
|       . . oo+   |
|          .. o+..|
|         .o=..oo+|
|          ..o.o+.|
+----[SHA256]-----+
```

The public key (id\_rsa.pub) is shared with remote systems, while the private key (id\_rsa) stays secure on your client system.

### Copying the Public Key to the Remote Server

To enable passwordless login, copy the public key to the remote server using the ssh-copy-id command. For example, if your username is mark and the remote server is node01, run:

```bash theme={null}
ssh-copy-id mark@node01
```

After providing your password for the remote system, the public key is appended to the `authorized_keys` file inside the `.ssh` directory of your remote home folder. You can verify its content with:

```bash theme={null}
cat /home/mark/.ssh/authorized_keys
```

This confirms that the public key has been successfully installed. Going forward, you should be able to connect without entering your password each time.

## Hardening the SSH Configuration

Once key-based authentication is set up, you can further secure your server by modifying the SSH configuration.

### Disabling Root Login

Disabling remote logins for the root account is a best security practice. This prevents unauthorized direct root access. Instead, use standard user accounts with privilege escalation tools like sudo for administrative tasks.

Edit the SSH configuration file as the root user:

```bash theme={null}
vi /etc/ssh/sshd_config
```

Locate the line for PermitRootLogin and change it to:

```bash theme={null}
PermitRootLogin no
```

### Disabling Password-Based Authentication

Since key-based authentication is now in place, you can disable password-based authentication to further protect your server. In the same configuration file (`/etc/ssh/sshd_config`), find the PasswordAuthentication directive and update it as follows:

```bash theme={null}
PasswordAuthentication no
```

After making these changes, save the file and restart the SSH service:

```bash theme={null}
systemctl restart sshd
```

<Callout icon="lightbulb">
  After restarting the SSH service, ensure you can log in with your SSH key. It is advised to keep an active session until you confirm that key-based authentication works properly, to avoid locking yourself out.
</Callout>

## Summary

In this lesson, you learned how to secure your Linux nodes by hardening the SSH service. We covered:

* Basic SSH connection commands
* Generating and using SSH key pairs for enhanced security
* Copying your public key to the remote server
* Securing the SSH configuration by disabling root login and password-based authentication

For more detailed security guidance, consider exploring established best practices for SSH hardening.

Happy securing!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-security-specialist-cks/module/d67be5ee-871d-4435-a187-382610cb6a1f/lesson/ca52732f-2d65-4d47-8eca-1f42459c01f2" />
</CardGroup>
