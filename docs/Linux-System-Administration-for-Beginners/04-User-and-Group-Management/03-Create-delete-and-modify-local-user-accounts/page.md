# Add John to developers
sudo gpasswd --add john developers
# or short form
sudo gpasswd -a john developers

# Verify John's groups
groups john
# Remove John from developers
sudo gpasswd --delete john developers
# or short form
sudo gpasswd -d john developers
```

## Changing a User’s Primary Group

To switch John’s primary group to `developers`, use `usermod` with the `--gid` option:

```bash theme={null}
sudo usermod --gid developers john

# Verify change
groups john
# Output: john : developers
```

> **lightbulb** `gpasswd` syntax is `gpasswd [--add|--delete] username group`\
  `usermod` syntax is `usermod --gid group username`

## Renaming and Deleting Groups

Rename a group from `developers` to `programmers`:

```bash theme={null}
sudo groupmod --new-name programmers developers
# or short form
sudo groupmod -n programmers developers
```

Delete a group when it’s no longer needed:

```bash theme={null}
sudo groupdel programmers
```

> **triangle-alert** If the group is the primary group for any user, `groupdel` will fail with:

  ```bash theme={null}
  groupdel: cannot remove the primary group of user 'john'
  ```

  Change the user’s primary group first:

  ```bash theme={null}
  sudo usermod --gid john john
  ```

  Then run:

  ```bash theme={null}
  sudo groupdel programmers
  ```

## Quick Reference Table

| Command                             | Description                          |
| ----------------------------------- | ------------------------------------ |
| `sudo useradd <user>`               | Create a new user                    |
| `sudo groupadd <group>`             | Create a new group                   |
| `sudo gpasswd -a <user> <group>`    | Add a user to a secondary group      |
| `sudo gpasswd -d <user> <group>`    | Remove a user from a secondary group |
| `sudo usermod --gid <group> <user>` | Change a user’s primary group        |
| `sudo groupmod -n <new> <old>`      | Rename a group                       |
| `sudo groupdel <group>`             | Delete a group                       |
| `groups <user>`                     | List all groups for a user           |

## Links and References

* [Linux User and Group Management](https://www.linux.com/training-tutorials/user-and-group-management/)
* [gpasswd Manual](https://man7.org/linux/man-pages/man1/gpasswd.1.html)
* [usermod Manual](https://man7.org/linux/man-pages/man8/usermod.8.html)
* [groupmod Manual](https://man7.org/linux/man-pages/man8/groupmod.8.html)
* [Kubernetes Documentation](https://kubernetes.io/docs/)

Practice these commands on a test environment to master Linux group administration!

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/7e2b6f48-e58c-4d05-82e2-feb0f5f876f5/lesson/1dc2201d-4c56-41c7-9d80-35239a84607c)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/7e2b6f48-e58c-4d05-82e2-feb0f5f876f5/lesson/33d61eed-41fe-4e58-9e6d-7f78b08a9d8c)


# Create delete and modify local user accounts

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/User-and-Group-Management/Create-delete-and-modify-local-user-accounts/page

Managing local user accounts on Linux for security, privacy, and streamlined administration.

Managing local user accounts on Linux is essential for security, privacy, and streamlined administration. Each user should have a dedicated account so they:

* Keep personal files and directories protected by proper permissions
* Configure their own environment and tool settings
* Operate with the least privilege, reducing accidental damage and attack surface

![The image shows a dark interface with the text "Manage Local User Accounts" on the left and a user icon in the center. The word "KodeKloud" is in the top right corner.](https://kodekloud.com/kk-media/image/upload/v1752881493/notes-assets/images/Linux-System-Administration-for-Beginners-Create-delete-and-modify-local-user-accounts/manage-local-user-accounts-interface.jpg)

***

## 1. Creating a New User

Use `useradd` to provision a fresh account.

```bash theme={null}
sudo useradd john
```

By default, this performs:

| Action                | Description                                                          |
| --------------------- | -------------------------------------------------------------------- |
| Create user and group | A new user named `john` and a primary group `john` with matching GID |
| Home directory        | `/home/john` is created and populated from `/etc/skel`               |
| Default shell         | `/bin/bash`                                                          |
| Account expiration    | No expiration date (unlimited)                                       |
| Password              | Unset (must be initialized with `passwd`)                            |

> **lightbulb** Skeleton files define initial user config.

  ```bash theme={null}
  ls -a /etc/skel
  # .  ..  .bash_logout  .bash_profile  .bashrc
  ```

You can also review default parameters:

```bash theme={null}
useradd --defaults
