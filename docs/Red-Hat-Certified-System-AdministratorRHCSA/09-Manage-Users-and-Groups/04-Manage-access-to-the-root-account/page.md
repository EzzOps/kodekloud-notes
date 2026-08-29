# or equivalently
$ sudo userdel -r john
```

## Customizing User Account Settings

You can modify default settings, such as the shell or home directory, when creating or updating an account. For example, to change a user's home directory immediately after creation, run:

```bash theme={null}
$ sudo usermod --home /home/otherdirectory --move-home john
# or using short options:
$ sudo usermod -d /home/otherdirectory -m john
```

The `--move-home` (or `-m`) option ensures that the contents of the old home directory are moved to the new location.

User account details—comprising usernames, user IDs, group IDs, home directories, and login shells—are stored in the `/etc/passwd` file. You can view this information by running:

```bash theme={null}
$ cat /etc/passwd
john:x:1001:1001::/home/otherdirectory/:/bin/othershell
```

In the output above:

* The first numeric value (1001) represents John's user ID.
* The second numeric value (1001) is his primary group ID.
* The home directory and the default shell are also listed.

By default, `useradd` assigns the next available numeric ID by incrementing the previous value. For manual assignment of a specific user ID, use:

```bash theme={null}
$ sudo useradd --uid 1100 smith
```

This command creates a user "smith" with a user ID of 1100 and automatically creates a primary group "smith" with the same numeric ID. To verify file ownership by username or numeric ID, you can use the `ls -l` command and include the numeric option `-n` if needed.

You can also review the current user's details, including group memberships, with commands like:

```bash theme={null}
$ id
uid=1000(aaron) gid=1000(aaron) groups=1000(aaron),10(wheel),1005(family) context=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023

$ whoami
aaron
```

## System Accounts

Linux also accommodates system accounts designed for programs and daemons. These accounts typically have numeric IDs less than 1000 and do not require a home directory. For example, to create a system account named "sysacc", run:

```bash theme={null}
$ sudo useradd --system sysacc
```

System accounts are ideal for running background services such as database servers or web servers that do not need interactive logins.

## Removing Multiple Users

If you need to remove multiple users along with their personal files, the process can be streamlined. For instance:

```bash theme={null}
$ sudo userdel -r john
$ sudo userdel -r smith
```

<Callout icon="lightbulb">
  Use the `useradd --help` option if you ever need a quick reminder of the available options for managing user accounts.
</Callout>

## Modifying User Accounts

To update user account details after creation—such as modifying the home directory, username, or login shell—the `usermod` command is invaluable. For example, to change John's home directory, run:

```bash theme={null}
$ sudo usermod --home /home/otherdirectory --move-home john
# or
$ sudo usermod -d /home/otherdirectory -m john
```

To change the username from "john" to "jane", use:

```bash theme={null}
$ sudo usermod --login jane john
# or using the shorthand option:
$ sudo usermod -l jane john
```

You can also change a user's login shell by providing the appropriate option with `usermod`.

Locking an account is another common action to disable password-based logins without deleting the account:

```bash theme={null}
$ sudo usermod --lock jane
```

To re-enable the account, issue:

```bash theme={null}
$ sudo usermod --unlock jane
```

Additionally, setting an account expiration date can control when a user’s account becomes inactive. For example:

```bash theme={null}
$ sudo usermod --expiredate 2021-12-10 jane
```

Note that setting an expiration date in the past will immediately disable the account. To remove an expiration date, provide an empty value (i.e., two quotes with nothing between).

Password expiration, which forces a user to change their password upon the next login, is handled separately by the `chage` command. To expire a password immediately, run:

```bash theme={null}
$ sudo chage --lastday 0 jane
# or using the short option:
$ sudo chage -d 0 jane
```

The next time Jane logs in, she will be required to choose a new password. To cancel this requirement, set the expiration parameter to `-1`. Additionally, you can enforce password change policies—such as prompting a change every 30 days—with:

```bash theme={null}
$ sudo chage --maxdays 30 jane
```

To ensure a password never expires, set the maximum days to `-1`. To review a user's password expiration settings, use:

```bash theme={null}
$ sudo chage --list jane
```

## Conclusion

In this article, we have covered the fundamental processes for creating, modifying, and deleting Linux local user accounts. We explored the default settings applied to new accounts, how to set and manage passwords, and the nuances of modifying account details with `usermod` and `chage`. These tools empower system administrators to efficiently manage user access and maintain system security.

Happy system managing, and see you in the next article!

For further reading on managing Linux systems, check out [Linux System Administration Basics](https://www.linux.com/learn/linux-basics/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/c2d7d0cc-a429-484c-b81b-674ff5fadc7e/lesson/4f1c0991-c9ae-4777-9238-ea6af9ee6d48" />
</CardGroup>


# Manage access to the root account

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Manage-Users-and-Groups/Manage-access-to-the-root-account/page

This article explores methods to manage root account access in Linux, including using sudo, handling locked accounts, and best practices for security.

In this article, we explore various methods to manage root account access in Linux. We cover temporary administrative privileges using sudo, full root logins, and how to handle scenarios with locked root accounts. This guide will help you understand the best practices for safely granting and restricting root access.

## Using sudo for Temporary Root Access

One common practice is to use sudo to execute individual commands with root privileges. When you prefix a command with sudo, it runs as if the command were executed by the root user.

For example, to list files in the /root directory:

```bash theme={null}
$ sudo ls /root/
anaconda-ks.cfg  initial-setup-ks.cfg
```

You can also initiate a full root session using:

```bash theme={null}
$ sudo --login    # Same as: $ sudo -i
```

Once the root session is active, you remain logged in as root until you type `logout`.

## Switching to a Full Root Shell

If your account lacks sudo privileges but you know the root password, you can log in directly as the root user. Use any of the following commands to start a full root shell:

* `su -`
* `su -l`
* `su --login` (long form)

All the above commands achieve the same result by switching the session to the root user.

## Handling Locked Root Accounts

In some Linux systems, the root account may be locked by default. When the root account is locked, you cannot log in using a password; however, you can still obtain root privileges via sudo.

<Callout icon="lightbulb">
  When the root account is locked, attempting to log in with `su -` will fail because it requires a valid root password. Always verify that your user account retains sudo privileges before making changes.
</Callout>

## Setting or Unlocking the Root Password

If you want to enable password-based logins for the root account, you have two options:

* Assign a new password if the root account never had one set.
* Unlock the account using the password unlock command if it was previously locked.

Follow these commands to set or unlock the root password:

```bash theme={null}
$ sudo --login
$ su -
$ sudo passwd root
$ sudo passwd --unlock root
```

After setting or unlocking the password, you can switch to the root account using `su -` and enter the new password.

## Locking the Root Account for Added Security

If you decide that direct root logins pose a security risk, you can disable them by locking the root account. Locking the account prevents password-based logins without affecting alternative login methods such as SSH keys.

<Callout icon="triangle-alert">
  Before locking the root account, ensure that your user account has sudo privileges. Losing this access could prevent you from making essential system changes.
</Callout>

To lock or unlock the root account, use the following commands:

```bash theme={null}
$ sudo --login
$ su -
$ sudo passwd root
$ sudo passwd --unlock root   # Equivalent to: $ sudo passwd -u root
$ su -
$ su -
$ sudo passwd --lock root     # Equivalent to: $ sudo passwd -l root
```

## Conclusion

By understanding and applying these methods, you can effectively manage access to the root account in your Linux environment. Use sudo for quick administrative tasks and carefully manage the root account’s password settings for full root access when necessary. In our next lesson, we will delve into more advanced topics to further enhance your system management skills.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/c2d7d0cc-a429-484c-b81b-674ff5fadc7e/lesson/863ec305-3bf5-4071-82c6-9651cde8dd25" />
</CardGroup>
