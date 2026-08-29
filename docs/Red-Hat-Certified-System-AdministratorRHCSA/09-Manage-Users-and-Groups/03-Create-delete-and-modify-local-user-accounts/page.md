# Expected output:
# john: john developers
```

There are situations where you might need to change a user's primary group. By default, Linux creates a primary group with the same name as the user account. However, you can change this using the usermod command with the -g option. For instance, to change John's primary group to Developers:

```bash theme={null}
sudo usermod -g developers john
```

> **lightbulb** A user can have only one primary group but can belong to multiple secondary groups. Avoid confusing the lowercase -g option (for the primary group) with the uppercase -G option (for secondary groups). To minimize errors, consider using the long option --gid:

  ```bash theme={null}
  sudo usermod --gid developers john
  ```

It is also important to note the difference in syntax between gpasswd and usermod. The gpasswd command expects the username before the group name, whereas usermod requires the group option immediately preceding the username.

If you need to rename an existing group, use the groupmod command with the --new-name option (or the short form -n). For example, to rename the developers group to programmers:

```bash theme={null}
sudo groupmod --new-name programmers developers
# Or equivalently:
sudo groupmod -n programmers developers
```

To delete a group, use the groupdel command. However, attempting to delete a group that is currently assigned as a user's primary group will result in an error:

```bash theme={null}
sudo groupdel programmers
# Output: groupdel: cannot remove the primary group of user 'john'
```

To successfully delete the group, change the user's primary group back to an appropriate group (e.g., the john group) before performing the deletion:

```bash theme={null}
sudo usermod --gid john john
sudo groupdel programmers
```

There is no need to manually remove a user from a secondary group before deleting it.

This concludes our lesson on managing local groups and group memberships. Be sure to practice these commands to solidify your understanding of Linux group management.

For further reading, consider exploring these resources:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/c2d7d0cc-a429-484c-b81b-674ff5fadc7e/lesson/f77d27d5-18e2-4b39-97dd-0ae9eb44809e)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/c2d7d0cc-a429-484c-b81b-674ff5fadc7e/lesson/6e4ef3b7-df0d-4912-a183-286c87ef5131)


# Create delete and modify local user accounts

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Manage-Users-and-Groups/Create-delete-and-modify-local-user-accounts/page

This article explains how to create, delete, and modify local user accounts in Linux for effective user management and system security.

In this article, we will explore how to efficiently create, delete, and modify local user accounts in Linux. Every individual who needs access to a Linux server should have a unique user account. This separation not only safeguards personal files with proper permissions but also allows users to customize their environment and enables administrators to limit privileges, reducing the risk of accidental or malicious errors.

<Frame>
  <img alt="The image shows a dark interface with a user icon and the text &#x22;Manage Local User Accounts&#x22; on the left side. The logo &#x22;KODEKLOUD&#x22; is in the top right corner." />
</Frame>

## Creating a New User Account

To create a new user, Linux provides the straightforward `useradd` command. The simplest usage creates a new user (for example, "john") and automatically assigns a primary group with the same name:

```bash theme={null}
$ sudo useradd john
```

When you execute this command, the following actions occur:

* A new user ("john") is added to the system.
* A new group ("john") is automatically created as the primary group.
* A home directory is established at `/home/john` for storing personal files, subdirectories, and program settings.
* The default shell is set to `/bin/bash`, ensuring John's session runs Bash upon login.
* All files from `/etc/skel` are copied into this new home directory. To inspect these default files, run:

  ```bash theme={null}
  $ ls -a /etc/skel
  .  ..  .bash_logout  .bash_profile  .bashrc
  ```

The operating system performs a set of default actions during account creation. You can review these default settings using:

```bash theme={null}
$ useradd --defaults
GROUP=100
HOME=/home
INACTIVE=-1
EXPIRE=
SHELL=/bin/bash
SKEL=/etc/skel
CREATE_MAIL_SPOOL=yes
```

These settings explain key aspects such as the home directory location, default shell, and group configuration.

> **lightbulb** Always review the default settings to ensure they align with your organization’s policies before creating user accounts.

## Setting a Password and Deleting an Account

After creating a new account, the user does not have a password by default. To set a password for John, use:

```bash theme={null}
$ sudo passwd john
Changing password for user john.
New password:
```

If you later decide that John's account is no longer needed, you can remove it using the `userdel` command. By default, this command removes only the user account (and its associated primary group, if auto-removed) while retaining the user's home directory:

```bash theme={null}
$ sudo userdel john
```

If you want to completely remove the account along with the home directory and mail spool, use the `--remove` option (or the shorthand `-r`):

```bash theme={null}
$ sudo userdel --remove john
