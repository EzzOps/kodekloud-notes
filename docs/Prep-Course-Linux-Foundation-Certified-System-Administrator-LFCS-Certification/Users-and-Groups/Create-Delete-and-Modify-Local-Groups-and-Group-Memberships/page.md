# The user and group nslcd should run as.
uid nslcd
gid nslcd

# The location at which the LDAP server(s) should be reachable.
uri ldap://10.0.142.218/

# The search base that will be used for all queries.
base dc=kodekloud,dc=com

# The LDAP protocol version to use.
#ldap_version 3

# The DN to bind with for normal lookups.
#binddn cn=anonymous,dc=example,dc=net
#bindpw secret

# The DN used for password modifications by root.
#rootpwmoddn cn=admin,dc=example,dc=com

# SSL options
#ssl off
#tls_reqcert never
tls_cacertfile /etc/ssl/certs/ca-certificates.crt

# The search scope.
#scope sub
```

You may update the LDAP server IP or base here if necessary.

***

## Testing LDAP Integration

Initially, local test commands confirmed that the accounts for John and Jane were absent:

```bash theme={null}
jeremy@kodekloud:~$ id john
id: ‘john’: no such user
jeremy@kodekloud:~$ id jane
id: ‘jane’: no such user
jeremy@kodekloud:~$
```

After configuring LDAP, re-run the commands to verify that these users are now recognized:

```bash theme={null}
jeremy@kodekloud:~$ id john
uid=10000(john) gid=10000(ldapusers) groups=10000(ldapusers)
jeremy@kodekloud:~$ id jane
uid=10001(jane) gid=10000(ldapusers) groups=10000(ldapusers)
jeremy@kodekloud:~$
```

The output indicates that John and Jane are LDAP users who belong to the "ldapusers" group. To view all user entries (both local and LDAP), use the following command:

```bash theme={null}
jeremy@kodekloud:~$ getent passwd
```

To filter specifically for LDAP-based entries:

```bash theme={null}
jeremy@kodekloud:~$ getent passwd --service ldap
john:x:10000:10000:John Smith:/home/john:/bin/bash
jane:x:10001:10000:Jane Smith:/home/jane:/bin/bash
```

Similarly, to display LDAP-based group information:

```bash theme={null}
jeremy@kodekloud:~$ getent group --service ldap
ldapusers:*:10000:
```

Notice that although the LDAP entries for John and Jane specify home directories (/home/john and /home/jane), these directories have not yet been created:

```bash theme={null}
jeremy@kodekloud:~$ ls /home
jeremy
jeremy@kodekloud:~$
```

***

## Automating Home Directory Creation with PAM

Manually creating home directories for every LDAP user is not scalable, especially across many servers. Instead, Pluggable Authentication Modules (PAM) can automatically create a user's home directory upon login if it does not exist.

To enable this automation, update your PAM configuration by executing:

```bash theme={null}
sudo pam-auth-update
```

When the configuration screen appears, select the option labeled "Create home directory on login" and press Enter to save your changes.

Below is an image of the PAM configuration interface (do not modify the image link or its description):

<Frame>
  ![The image shows a configuration screen for Pluggable Authentication Modules (PAM), allowing the user to select various authentication and session management options, such as Unix authentication and LDAP Authentication.](https://kodekloud.com/kk-media/image/upload/v1752881372/notes-assets/images/Linux-Foundation-Certified-System-Administrator-LFCS-Configure-the-System-to-Use-LDAP-User-and-Group-Accounts/pam-configuration-authentication-options.jpg)
</Frame>

Now, test the home directory creation by logging in as John using his LDAP credentials (password is "password"). Upon a successful login, PAM automatically creates the /home/john directory, if it is missing.

After logging in as John, verify the home directory exists:

```bash theme={null}
john@kodekloud:~$ ls /home
jeremy  john
john@kodekloud:~$
```

***

## Summary

By configuring your Linux system to leverage an LDAP server for user and group accounts, you centralize account management. This setup automatically retrieves and updates user data—including creating home directories on first login via PAM—thereby eliminating the need to manage accounts across every individual server.

This guide demonstrated how to:

* Set up and start an LDAP server in an LXC container
* Install and configure libnss-ldapd to integrate LDAP lookups
* Verify that user and group information is correctly fetched from LDAP
* Use PAM to automatically create home directories on user login

For more information, refer to the following resources:

* [LDAP Introduction](https://ldap.com/)
* [Pluggable Authentication Modules (PAM) Overview](https://www.linux.com/tutorials/introduction-pluggable-authentication-modules-pam/)

Happy learning, and see you in the next lesson!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-foundation-certified-system-administrator-lfcs/module/b36d272b-24e2-44e1-82cb-20a5cfa93635/lesson/5550800c-0757-4339-8828-7816fadee16c" />
</CardGroup>


# Create Delete and Modify Local Groups and Group Memberships

Source: https://notes.kodekloud.com/docs/Prep-Course-Linux-Foundation-Certified-System-Administrator-LFCS-Certification/Users-and-Groups/Create-Delete-and-Modify-Local-Groups-and-Group-Memberships/page

Managing local groups in Linux simplifies file permission and system privilege administration by efficiently controlling access to project files or critical system functions.

Managing local groups in Linux simplifies file permission and system privilege administration. By grouping users—such as developers, administrators, or container managers—you can efficiently control access to project files or critical system functions.

Imagine you have a directory containing files that developers need to work on. For instance, by creating a group called Developers and assigning appropriate read/write permissions, you can ensure that users like John, Jack, and later Jane have proper access to edit files. If a developer’s role changes or they leave the team, simply adding or removing them from the Developers group updates their permissions automatically.

Certain groups provide special privileges on the system. Consider the following examples:

| Group      | Privilege Description                                      |
| ---------- | ---------------------------------------------------------- |
| wheel/sudo | Execute any command with root privileges                   |
| Docker     | Manage Docker containers without requiring root privileges |

Remember that each user has a primary (login) group and may belong to several secondary (supplementary) groups. The primary group is set at login and influences file creation permissions, as files are automatically associated with both the user account and the primary group.

Before proceeding with these exercises, ensure that a user named John exists on your system.

***

## Creating a New Group and Adding a User

To start, ensure that the user John is created and then create the Developers group:

```bash theme={null}
$ sudo adduser john
$ sudo groupadd developers
```

The easiest way to add John to the Developers group is by using the `gpasswd` command. Despite its name originating from "group password," it is primarily used to manage group memberships. To add John to the Developers group, run:

```bash theme={null}
$ sudo gpasswd --add john developers
```

You can verify John's group memberships with:

```bash theme={null}
$ groups john
```

The output will list his primary group first, followed by any secondary groups, for example:

```text theme={null}
john: john developers
```

If you need to remove John from a secondary group, use:

```bash theme={null}
$ sudo gpasswd --delete john developers
```

Or equivalently:

```bash theme={null}
$ sudo gpasswd -d john developers
```

***

## Changing a User’s Primary Login Group

Sometimes you may need to change John’s primary login group. Use the `usermod` command with caution, ensuring that you do not confuse the option for modifying secondary groups. The `-g` (or `--gid`) option specifically changes the primary group.

<Callout icon="triangle-alert">
  Be sure that you correctly distinguish between the primary group and secondary groups. An incorrect adjustment may lead to unintended permission issues.
</Callout>

Execute the following command to change John’s primary group to Developers:

```bash theme={null}
$ sudo usermod --gid developers john
```

After executing the command, verify the change by running:

```bash theme={null}
$ groups john
```

The expected output should be:

```text theme={null}
john: developers
```

*Note: The `gpasswd` command expects the username first and then the group name, whereas `usermod` requires the group name before the username.*

***

## Renaming and Deleting a Group

To rename the "developers" group to "programmers," use the `groupmod` command. You can choose between the long option or its short alternative:

```bash theme={null}
$ sudo groupmod --new-name programmers developers
```

Or equivalently:

```bash theme={null}
$ sudo groupmod -n programmers developers
```

If you later decide to delete the programmers group, use the `groupdel` command. However, if any user, such as John, is still using that group as their primary group, you will encounter an error:

```bash theme={null}
$ sudo groupdel programmers
groupdel: cannot remove the primary group of user 'john'
```

<Callout icon="lightbulb">
  Before deleting a group, make sure that no user has it set as their primary group. In cases where the group is primary for any user, change that user's primary group (for example, back to "john") before deletion.
</Callout>

Deleting a secondary group will work seamlessly provided it is not set as a user's primary group.

***

This concludes our guide on managing local groups and group memberships in Linux. By leveraging these commands, administrators can simplify the management of file permissions and user roles across the system. For more detailed information on Linux user and group management, consider reviewing the [Linux Documentation](https://www.kernel.org/doc/) or related [user management tutorials](https://www.linux.com/topic/desktop/how-manage-users-and-groups-linux/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-foundation-certified-system-administrator-lfcs/module/b36d272b-24e2-44e1-82cb-20a5cfa93635/lesson/81bc6d77-7ed1-4db0-a080-391b6135e605" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/linux-foundation-certified-system-administrator-lfcs/module/b36d272b-24e2-44e1-82cb-20a5cfa93635/lesson/4cd8ffe1-601d-4a31-9655-f6b31b697bac" />
</CardGroup>
