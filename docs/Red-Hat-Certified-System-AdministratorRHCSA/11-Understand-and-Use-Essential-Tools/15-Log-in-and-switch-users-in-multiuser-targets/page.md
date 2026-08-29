# Log in and switch users in multiuser targets

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Understand-and-Use-Essential-Tools/Log-in-and-switch-users-in-multiuser-targets/page

Introduction to Linux access control covering user and group management, file ownership and permissions, and safe privilege escalation using su and sudo with sudoers and visudo guidance.

In this lesson we'll cover Linux security basics focused on access control: user accounts, groups, file ownership and permissions, and privilege escalation. You'll learn how to create and manage users, inspect account details, and switch identities safely using su and sudo. Each topic includes commands and examples so you can practice these essential administrative skills.

<Frame>
  <img alt="A presentation slide titled &#x22;Security and File Permissions&#x22; with the KodeKloud logo. It shows topic boxes like &#x22;Basic Security and Identifying File Types,&#x22; &#x22;Creating Users and Groups,&#x22; &#x22;Managing file permission and ownership,&#x22; and highlighted lab items such as &#x22;Labs: Special Directories and Files.&#x22;" />
</Frame>

Security in Linux spans many layers:

* Authentication (who you are) — often handled via passwords, keys, and frameworks such as PAM (Pluggable Authentication Modules).
* Access control (what you can do) — user and group permissions, file modes, ACLs, and mandatory access controls such as SELinux.
* Network and service protection — firewalling (iptables, nftables, firewalld), SSH hardening, and service isolation.
* Audit and accountability — centralized logs, sudo logs, and system accounting.

This lesson focuses on the basics: user and group accounts, how user metadata is stored, and how to escalate or switch privileges safely.

For deeper reading:

* PAM: [https://www.linux-pam.org/](https://www.linux-pam.org/)
* SSH hardening: [https://www.openssh.com/](https://www.openssh.com/)
* SELinux: [https://selinuxproject.org/page/Main\_Page](https://selinuxproject.org/page/Main_Page)

<Frame>
  <img alt="A slide titled &#x22;Linux Accounts&#x22; showing a central &#x22;Linux Security&#x22; box connected to components like Access Controls, PAM, Network Security, SSH Hardening, SELinux, and &#x22;Many More.&#x22; The slide is branded with the KodeKloud logo." />
</Frame>

## What is a user account?

A Linux user account represents an identity that can authenticate and perform actions on the system. Each account stores metadata used by the kernel and system services to control access.

Typical account fields:

* username
* password placeholder (usually an `x` in /etc/passwd, with the hashed password in /etc/shadow)
* UID (user ID) — unique integer
* primary GID (group ID)
* optional comment / GECOS (human-readable info)
* home directory
* default login shell

Account and group data are stored in:

* /etc/passwd — account metadata and login shell/home
* /etc/shadow — encrypted password hashes (restricted)
* /etc/group — groups and group members

Example: two developers (bob and michael) can be members of the same group (e.g., developers) to share access to common files.

Example contents of /etc/passwd and /etc/group:

```bash theme={null}
$ cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
bob:x:1000:1000:Bob Kingsley,,,:/home/bob:/bin/bash
michael:x:1001:1001::/home/michael:/bin/sh
```

```bash theme={null}
$ cat /etc/group
ssh:x:118:
lpadmin:x:119:
scanner:x:120:saned
avahi:x:121:
saned:x:122:
colord:x:123:
geoclue:x:124:
pulse:x:125:
pulse-access:x:126:
gdm:x:127:
systemd-coredump:x:999:
bob:x:1000:
developers:x:1003:bob,michael
```

### Account field breakdown (quick reference)

| Field          | Description                                            | Example       |
| -------------- | ------------------------------------------------------ | ------------- |
| UID            | Unique numeric user identifier. `0` is root.           | 1001          |
| GID            | Primary numeric group identifier for the user.         | 1001          |
| Username       | Human-readable account name used to log in.            | michael       |
| Home directory | Default directory after login.                         | /home/michael |
| Login shell    | Default shell executed at login.                       | /bin/bash     |
| GECOS          | Optional comment: user’s full name, contact info, etc. | Bob Kingsley  |

Inspect a user's IDs and groups:

```bash theme={null}
$ id michael
uid=1001(michael) gid=1001(michael) groups=1001(michael),1003(developers)
```

Check a user’s home and shell by reading /etc/passwd (see example above).

## Account types

* User account — for a person who needs access.
* Superuser (root) — UID 0; unrestricted privileges.
* System accounts — created for OS services; often have low UIDs and no interactive shell.
* Service accounts — created for specific applications (e.g., nginx, mysql).

<Frame>
  <img alt="A presentation slide titled &#x22;Account Types&#x22; showing four colored boxes for User Account, Superuser Account (UID = 0), System Accounts (with UID ranges), and Service Accounts, plus example usernames (e.g., Bob, root, ssh, nginx). The slide includes the KodeKloud logo and illustrative icons." />
</Frame>

## Useful user-related commands

| Command | Purpose                                             | Example      |
| ------- | --------------------------------------------------- | ------------ |
| id      | Show UID, GID, and supplementary groups for a user. | `id michael` |
| who     | List users currently logged in.                     | `who`        |
| last    | Show login/logout history and reboots.              | `last`       |

Examples:

```bash theme={null}
$ id
uid=1000(michael) gid=1000(michael) groups=1000(michael)

$ who
bob      pts/2        Apr 28 06:48   (172.16.238.187)

$ last
michael  :1   :1        Tue May 12 20:00  still logged in
sarah    :1   :1        Tue May 12 12:00  still running
reboot   system boot 5.3.0-758-gen  Mon May 11 13:00 - 19:00 (06:00)
```

## Switching users: su vs sudo

There are multiple ways to run commands as another user. Choose the method that fits your operational and auditing requirements.

### su (substitute user)

* su starts a shell as another user and typically requires the target user’s password.
* `su -` opens a login shell, loading the target user’s environment.
* Useful for interactive sessions, but less auditable because commands aren’t centrally logged by sudo.

Examples:

```bash theme={null}
$ su -
Password:
root@host:~#

$ su -c "whoami"
Password:
root
```

### sudo (delegate privileges)

* sudo lets authorized users run commands as another user (commonly root) by authenticating with their own password.
* Sudo policies are configured in /etc/sudoers and in files under /etc/sudoers.d/.
* sudo provides better auditing and fine-grained privilege delegation.

Example usage:

```bash theme={null}
michael@ubuntu-server:~$ sudo apt-get install nginx
[sudo] password for michael:
```

Sample /etc/sudoers (simplified):

```bash theme={null}
