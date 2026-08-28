# Manage Access to Root Account

Source: https://notes.kodekloud.com/docs/Prep-Course-Linux-Foundation-Certified-System-Administrator-LFCS-Certification/Users-and-Groups/Manage-Access-to-Root-Account/page

This guide explores methods for managing access to the root account in Linux, focusing on sudo and su commands for security and access control.

In this guide, we explore various methods for managing access to the root account in Linux. We will discuss two main approaches: using sudo for temporary root privileges and using su to log in as the root user. These techniques are essential for system administrators and users concerned with Linux security and effective access control.

## Using sudo for Temporary Root Privileges

For users with sudo privileges, you can execute commands as root without needing to log in directly as the root user. This method enhances security by using your user password instead of the root password.

For example, to list the contents of the /root directory, you can run:

```bash theme={null}
$ sudo ls /root/
anaconda-ks.cfg  initial-setup-ks.cfg
```

To start an interactive root shell, use the following command. Both `sudo -i` and `sudo --login` achieve the same result:

```bash theme={null}
$ sudo --login    # equivalent to: $ sudo -i
```

When your root session is complete, simply exit by typing:

```bash theme={null}
$ logout
```

<Callout icon="lightbulb">
  Using sudo for temporary privileges helps minimize the security risks associated with prolonged root sessions.
</Callout>

## Using su to Log In as Root

If your user does not have sudo privileges but you know the root password, you can switch to the root account using the `su` command. The following command is commonly used:

```bash theme={null}
$ su -       # equivalent to: $ su -l or $ su --login
```

Unlike sudo, which requests your current user's password, the su command requires the root user's password.

## Handling Locked Root Accounts

Some systems lock the root account by default to improve security. A locked root account disables password-based logins, but it does not prevent access to the root shell if you have sudo privileges.

### Enabling Password-Based Root Login

If you prefer to enable password-based logins for the root account, consider the following two scenarios:

• If the root account never had a password set, assign a new one.\
• If the root account had a password that was later locked, you can unlock it using one of these commands:

```bash theme={null}
$ sudo passwd root            # Set a new password for root
$ sudo passwd --unlock root   # Alternatively: $ sudo passwd -u root
```

Once the root password is set or unlocked, log in as the root user using:

```bash theme={null}
$ su -     # Then enter the newly set root password when prompted
```

<Callout icon="lightbulb">
  Enabling password-based logins can be useful for specific administrative tasks but consider the security implications carefully.
</Callout>

### Locking the Root Account

Conversely, if you decide that permitting password-based logins for the root account is too risky, you can lock the account by running:

```bash theme={null}
$ sudo passwd --lock root     # Alternatively: $ sudo passwd -l root
```

Before locking the root account, ensure that your current user has adequate sudo privileges. Losing both sudo access and root login may prevent you from performing essential system maintenance.

<Callout icon="triangle-alert">
  Make sure to verify that your user account has the necessary sudo privileges before locking the root account. Otherwise, you risk losing critical administrative access.
</Callout>

## Conclusion

This guide has provided comprehensive instructions on managing access to the root account in Linux using both the sudo and su commands. By understanding these methods, you can better secure your system while ensuring that you maintain adequate administrative access.

For further reading on Linux security and access management, check out the following reference:

* [Linux Security Fundamentals](https://www.linux.com/learn/)

By following these practices, you can effectively manage root access and maintain a secure Linux environment.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-foundation-certified-system-administrator-lfcs/module/b36d272b-24e2-44e1-82cb-20a5cfa93635/lesson/7978e813-053a-49bb-ad39-71bd3862c52e" />
</CardGroup>
