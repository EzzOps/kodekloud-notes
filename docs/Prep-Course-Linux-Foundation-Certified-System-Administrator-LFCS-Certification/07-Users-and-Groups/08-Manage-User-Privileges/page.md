# Manage User Privileges

Source: https://notes.kodekloud.com/docs/Prep-Course-Linux-Foundation-Certified-System-Administrator-LFCS-Certification/Users-and-Groups/Manage-User-Privileges/page

This article explores managing user privileges on Linux systems using sudo and user groups for effective access control.

In this article, we explore how to manage user privileges on Linux systems. By understanding how sudo works and how user groups are associated with administrative rights, you can effectively grant and fine-tune access on your server.

## Using Sudo and User Groups

For critical system changes, you typically prepend your commands with sudo. Since only the root user is allowed to modify sensitive parts of the system, sudo temporarily elevates privileges to execute commands as the superuser.

A user is permitted to use sudo if they belong to the sudo group. To verify your group memberships, run:

```bash theme={null}
$ groups
aaron family sudo
```

Since Aaron is a member of the sudo group, he can execute administrative tasks using sudo. To grant another user sudo privileges (for example, to add Trinity), execute the following:

```bash theme={null}
$ groups
aaron family sudo
$ sudo gpasswd -a trinity sudo
```

At this point, the user Trinity will have administrator privileges, meaning she can execute any command using sudo. However, granting full sudo rights enables complete control over the system, which might not always be desirable.

## Fine-Tuning Sudo Privileges

For more granular control over user privileges, you can define specific sudo policies using the sudoers file located at `/etc/sudoers`. It is important not to edit this file directly; instead, always use the `visudo` utility. Visudo opens the file in an editor, checks for syntax errors before saving, and thus prevents misconfigurations.

Before proceeding with customization, remove Trinity from the sudo group to avoid granting her full sudo privileges:

```bash theme={null}
$ sudo gpasswd -d trinity sudo
$ sudo visudo
```

When you open the file with visudo, you might encounter a section like this:

```bash theme={null}
