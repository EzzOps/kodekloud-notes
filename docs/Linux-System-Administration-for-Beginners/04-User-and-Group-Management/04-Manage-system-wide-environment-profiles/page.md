# GROUP=100
# HOME=/home
# INACTIVE=-1
# EXPIRE=
# SHELL=/bin/bash
# SKEL=/etc/skel
# CREATE_MAIL_SPOOLS=yes
```

***

## 2. Setting a Password

After account creation, assign a strong password:

```bash theme={null}
sudo passwd john
# Changing password for user john.
# New password:
```

***

## 3. Deleting a User

Remove user accounts carefully:

| Task                                 | Command                                                  |
| ------------------------------------ | -------------------------------------------------------- |
| Delete account (keep home directory) | `sudo userdel john`                                      |
| Delete account + home + mail spool   | `sudo userdel --remove john`<br />`sudo userdel -r john` |

> **triangle-alert** Using `--remove` (or `-r`) will delete the user’s home directory and mail spool permanently.\
  Always back up important data before proceeding.

***

## 4. Customizing Account Creation

Pass flags to override defaults:

| Option                    | Description                                     | Example                                   |
| ------------------------- | ----------------------------------------------- | ----------------------------------------- |
| `-d, --home <dir>`        | Custom home directory                           | `sudo useradd -d /home/special_john john` |
| `-s, --shell <shell>`     | Specify login shell                             | `sudo useradd -s /bin/zsh john`           |
| `-u, --uid <UID>`         | Assign specific user ID                         | `sudo useradd -u 1100 smith`              |
| `-g, --gid <GID-or-name>` | Assign primary group (must exist or be created) | `sudo useradd -g 1100 smith`              |

***

## 5. Inspecting User Records

Account metadata resides in `/etc/passwd`:

```bash theme={null}
cat /etc/passwd | grep john
# john:x:1001:1001::/home/john:/bin/bash
```

* Field breakdown: `username:password:UID:GID:comment:home:shell`

View file ownership under `/home`:

```bash theme={null}
ls -l /home/
# drwxr-xr-x 2 john john 4096 Feb  5 10:00 john
```

Display numeric IDs:

```bash theme={null}
ls -ln /home/
```

***

## 6. Identifying the Current User

| Command  | Output                                                |
| -------- | ----------------------------------------------------- |
| `id`     | UID, GID, groups, and SELinux context (if applicable) |
| `whoami` | Current username                                      |

```bash theme={null}
id
whoami
# aaron
```

***

## 7. System Accounts

System accounts serve daemons and services. They typically have UIDs below 1000 and no home directory:

```bash theme={null}
sudo useradd --system sysacc
```

***

## 8. Modifying an Existing User

Use `usermod` to update user settings:

| Change                           | Command                                                      |
| -------------------------------- | ------------------------------------------------------------ |
| Move home directory              | `sudo usermod -d /home/newdir -m john`                       |
| Rename user                      | `sudo usermod -l jane john`                                  |
| Change login shell               | `sudo usermod -s /bin/zsh jane`                              |
| Lock account                     | `sudo usermod --lock jane` `<br />` `sudo usermod -L jane`   |
| Unlock account                   | `sudo usermod --unlock jane` `<br />` `sudo usermod -U jane` |
| Set expiration date (YYYY-MM-DD) | `sudo usermod -e 2022-01-01 jane`                            |
| Remove expiration date           | `sudo usermod -e "" jane`                                    |

***

## 9. Password Aging with `chage`

Control password policies using `chage`:

| Policy                       | Command                 |
| ---------------------------- | ----------------------- |
| Force change on next login   | `sudo chage -d 0 jane`  |
| Reset last password change   | `sudo chage -d -1 jane` |
| Set max days between changes | `sudo chage -M 30 jane` |
| Disable expiration           | `sudo chage -M -1 jane` |
| View aging info              | `sudo chage -l jane`    |

***

## 10. References

* [Linux User Management (The Linux Documentation Project)](https://tldp.org/LDP/sag/html/user-management.html)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [chage Manual](https://linux.die.net/man/1/chage)
* [passwd Manual](https://linux.die.net/man/1/passwd)

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/7e2b6f48-e58c-4d05-82e2-feb0f5f876f5/lesson/d5b36d54-e503-4378-9cb5-e18291372973)


# Manage system wide environment profiles

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/User-and-Group-Management/Manage-system-wide-environment-profiles/page

This guide explains how to configure and maintain system-wide environment variables and login scripts for all users on a Linux system.

In this guide, you’ll learn how to configure and maintain environment variables and login scripts that apply to all users on a Linux system. We’ll cover:

* Understanding and viewing environment variables
* Persisting system-wide variables via `/etc/environment`
* Executing commands at login with `/etc/profile.d/`

## Understanding Environment Variables

Environment variables are key–value pairs that shells and applications use to adjust behavior. You can list the current environment with either `env` or `printenv`.

| Command         | Description                                                  | Example Output          |
| --------------- | ------------------------------------------------------------ | ----------------------- |
| `env`           | Displays all environment variables                           | `PATH=/usr/local/bin:…` |
| `printenv HOME` | Shows the value of a specific variable (`HOME` in this case) | `/home/aaron`           |

```bash theme={null}
