# Hard only
trinity    hard    nproc    30

# Soft only
trinity    soft    nproc    10

# Both soft & hard
trinity    -       nproc    20
```

### 2.3 Item

Resource items you can limit:

| Item      | Description                                                                     | Example |
| --------- | ------------------------------------------------------------------------------- | ------- |
| nproc     | Max processes per user session                                                  | 10      |
| fsize     | Max file size (KB)                                                              | 1024    |
| cpu       | CPU time (minutes)                                                              | 1       |
| core      | Core dump file size (KB)                                                        | 0       |
| rss       | Resident set size (KB)                                                          | 10000   |
| maxlogins | Max concurrent logins per user                                                  | 4       |
| …         | See [man limits.conf](https://man7.org/linux/man-pages/man5/limits.conf.5.html) | –       |

Example: file-size and CPU restrictions for `trinity`:

```ini theme={null}
trinity    hard    fsize    1024   # 1 MB max file size
trinity    hard    cpu      1      # 1 minute CPU time
```

***

## 3. Exercise: Enforce a 3-Process Limit for “trinity”

1. Add the following (uncommented) line to `/etc/security/limits.conf`:

   ```ini theme={null}
   trinity    -    nproc    3
   ```

2. Save and exit.

### 3.1 Verify the Limit

```bash theme={null}
# Switch to trinity
sudo -iu trinity

# Attempt to list processes
ps | less
# Try spawning a fourth
ls -a | grep bash | less
logout
```

### 3.2 Check with ulimit

```bash theme={null}
ulimit -a
# ...
# max user processes        (-u)    3
```

You can adjust soft limits on the fly:

```bash theme={null}
# Raise soft limit up to hard (if below hard)
ulimit -u 5000
```

> **lightbulb** Changes take effect on new sessions. Log out and back in to apply updates.\
  Use `ulimit -a` to inspect all current limits.

***

## 4. References and Further Reading

* [PAM Limits Module (limits.conf)](https://www.linux-pam.org/Linux-PAM-html/sag-pam_limits.html)
* [Linux Manual: limits.conf(5)](https://man7.org/linux/man-pages/man5/limits.conf.5.html)
* [ulimit Builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/7e2b6f48-e58c-4d05-82e2-feb0f5f876f5/lesson/62174b1a-cb2b-488e-adb3-47b9a339efc1)


# Create delete and modify local groups and group memberships

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/User-and-Group-Management/Create-delete-and-modify-local-groups-and-group-memberships/page

This guide covers creating, deleting, and modifying local groups in Linux, managing memberships, and adjusting group assignments for user permissions.

Keeping your Linux server secure and organized often involves managing groups and assigning users the appropriate permissions. In this guide, you'll learn how to create, delete, and modify local groups, manage memberships, and adjust primary versus secondary group assignments.

## Why Use Groups?

Groups let you grant permissions to multiple users at once. For example, imagine a shared directory for your development team:

* Team members: John, Jack, Jane
* Directory: `/srv/dev-project`
* Required access: read/write

Instead of adjusting permissions per user, you can:

1. Create a **developers** group
2. Add John, Jack, and Jane to **developers**
3. Change the directory’s group ownership to **developers**
4. Grant the group read/write rights

![The image shows a diagram of a "Developers" group with members named John, Jack, and Jane, alongside a folder icon labeled "Permission."](https://kodekloud.com/kk-media/image/upload/v1752881493/notes-assets/images/Linux-System-Administration-for-Beginners-Create-delete-and-modify-local-groups-and-group-memberships/developers-group-john-jack-jane-permission.jpg)

Now any member of **developers** automatically has the correct permissions. Remove a user from the group to revoke access, or add new members to grant permissions instantly.

Beyond file access, group membership controls special privileges:

* **wheel** or **sudo** group → run commands as root
* **docker** group → manage [Docker containers](https://docs.docker.com/get-started/)

> **lightbulb** Each user has one **primary** group (used when creating files or running processes) and zero or more **secondary** groups.

## Creating a User and a Group

First, ensure you have a user (`john`) and create the `developers` group:

```bash theme={null}
sudo useradd john
sudo groupadd developers
```

## Managing Group Memberships

Use the `gpasswd` tool to add or remove users from secondary groups:

```bash theme={null}
