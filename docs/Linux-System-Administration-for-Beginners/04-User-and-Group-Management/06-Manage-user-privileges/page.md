# Manage user privileges

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/User-and-Group-Management/Manage-user-privileges/page

This guide explains how to manage `sudo` access and user privileges on Linux for improved system security.

Controlling who can perform administrative tasks is crucial for system security. In this guide, you’ll learn how to grant and restrict `sudo` access on Linux, manage entries in `/etc/sudoers`, and apply fine-grained policies for different users and groups.

## Using `sudo`

By default, only the **root** (superuser) can modify system-critical files and settings. Prefixing a command with `sudo` elevates it to root privileges:

```bash theme={null}
$ sudo apt update
```

> **lightbulb** When running `sudo` for the first time, you’ll be prompted for *your* password—not the root password.

## Granting `sudo` via the wheel group

Many Linux distributions allow members of the `wheel` group to use `sudo`:

```bash theme={null}
$ groups
aaron family wheel
```

To add a user (e.g., `trinity`) to `wheel`:

```bash theme={null}
$ sudo gpasswd -a trinity wheel
```

Now `trinity` can execute any command with `sudo`, which is easy but lacks fine control.

## Fine-grained control with `/etc/sudoers`

Instead of a broad group assignment, define precise policies in `/etc/sudoers`. **Never** edit that file directly! Always use `visudo`, which validates syntax.

```bash theme={null}
$ sudo visudo
```

Inside, you’ll find a line like:

```sudoers theme={null}
## Allows people in group wheel to run all commands
%wheel ALL=(ALL) ALL
```

> **triangle-alert** A malformed `/etc/sudoers` can lock out all sudo access. Always use `visudo` to edit safely.

### Breakdown of a sudoers entry

| Part       | Description                                                    | Example                      |
| ---------- | -------------------------------------------------------------- | ---------------------------- |
| User/Group | Rule applies to this user (e.g., `trinity`) or group (`%devs`) | `trinity`<br />`%developers` |
| Host       | Hosts where the rule is valid (`ALL` for every host)           | `ALL`                        |
| Run as     | User(s) the command may run as (in parentheses)                | `(ALL)`, `(aaron,john)`      |
| Commands   | Which commands are allowed                                     | `/bin/ls, /usr/bin/vim`      |

## Defining custom `sudoers` policies

Below are sample entries to append near the end of `/etc/sudoers` via `visudo`:

```sudoers theme={null}
