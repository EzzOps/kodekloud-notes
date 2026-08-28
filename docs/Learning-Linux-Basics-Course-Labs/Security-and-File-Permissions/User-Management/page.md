# User Management

Source: https://notes.kodekloud.com/docs/Learning-Linux-Basics-Course-Labs/Security-and-File-Permissions/User-Management/page

This guide covers essential commands for creating and managing user accounts on Linux, including user addition, account customization, and group management.

In this guide, you'll learn essential commands for creating and managing user accounts on Linux. This tutorial covers adding users, customizing account settings, and managing groups, ensuring you understand both the basics and some advanced options.

## Creating a New User

The primary command to add a new local user is `useradd`. System administrators typically use this command to add new users. For example, to create a new user named Bob, execute:

```bash theme={null}
[~]$ useradd bob
```

This command creates Bob with a system-generated UID and GID. By default, Bob's home directory is set to `/home/bob` (based on the system's default configuration) and his login shell is set to `/bin/sh`.

To set a password for Bob's account, use the `passwd` command:

```bash theme={null}
[~]$ passwd bob
```

<Callout icon="triangle-alert">
  Both `useradd` and `passwd` commands must be executed with root privileges.
</Callout>

After logging in, a user can confirm their current username by running the `whoami` command. Additionally, users can change their password at any time by simply running `passwd` without any additional arguments.

## Using Options with useradd

The `useradd` command supports several options that allow you to customize the user creation process. Here are some commonly used options:

* **-u:** Specify a custom UID.
* **-g:** Specify the primary group via a custom GID.
* **-d:** Define a custom home directory path.
* **-s:** Set the default login shell.
* **-c:** Add a comment (often used for a user description).
* **-e:** Set the account expiration date.
* **-G:** Add the new user to additional (secondary) groups.

For example, to create Bob with a custom UID, GID, home directory, shell, and an account comment, use:

```bash theme={null}
[~]$ useradd -u 1009 -g 1009 -d /home/robert -s /bin/bash -c "Mercury Project member" bob
```

This command assigns Bob a UID and a primary GID of 1009, sets his home directory to `/home/robert`, selects `/bin/bash` as his login shell, and includes the comment "Mercury Project member" in his account information.

You can validate Bob's settings with the `id` command:

```bash theme={null}
[~]$ id bob
uid=1009(bob) gid=1009(avenger) groups=1009(avenger)
```

Additionally, inspect the `/etc/passwd` file to verify the custom comment and other account details:

```bash theme={null}
[~]$ grep -i bob /etc/passwd
bob:x:1009:1009:Mercury Project member:/home/robert:/bin/bash
```

## User Deletion and Group Management

To delete a user account, use the `userdel` command followed by the username:

```bash theme={null}
[~]$ userdel bob
```

Managing groups is equally essential. Below are commands for adding and deleting groups:

* **Adding a New Group:** Use the `groupadd` command. The **-g** option lets you specify a custom GID.

  ```bash theme={null}
  [~]$ groupadd -g 1010 newgroup
  ```

* **Deleting a Group:** Use the `groupdel` command along with the group name.

  ```bash theme={null}
  [~]$ groupdel newgroup
  ```

## Hands-On Practice

<Callout icon="lightbulb">
  We recommend practicing these Linux user account management commands on your local system to reinforce your skills in system administration.
</Callout>

Happy learning!

## Additional Resources

* [Linux Documentation](https://www.kernel.org/doc/html/latest/)
* [User Management Best Practices](https://www.linux.com/training-tutorials/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/learning-linux-basics-course-labs/module/6c7e1a9b-9ecc-43c5-9dce-8031ab5d3fe2/lesson/9822d51e-160e-4b91-a5d7-76be53e20635" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/learning-linux-basics-course-labs/module/6c7e1a9b-9ecc-43c5-9dce-8031ab5d3fe2/lesson/d441ffb6-31e6-4194-abbc-3875324cecea" />
</CardGroup>
