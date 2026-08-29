# 1. Allow trinity to run any command as any user (including root)
trinity ALL=(ALL) ALL

# 2. Grant all members of 'developers' the same privilege
%developers ALL=(ALL) ALL

# 3. Permit trinity to run any command, but only as aaron or john
trinity ALL=(aaron,john) ALL

# 4. Shortcut: run as root (default) without specifying run-as list
trinity ALL=ALL

# 5. Restrict trinity to only run /bin/ls and /bin/stat as root
trinity ALL=(ALL) /bin/ls, /bin/stat

# 6. Same as above, omitting the run-as list (defaults to root)
trinity ALL= /bin/ls, /bin/stat
```

## Running commands as another user

Beyond root, you can invoke commands as any user:

```bash theme={null}
$ sudo -u trinity ls /home/trinity
Desktop  Documents  Downloads  Music  Pictures
```

## Handling “Permission denied” errors

If a user invokes a disallowed command, sudo reports:

```bash theme={null}
$ sudo echo "Test passed?"
Sorry, user trinity is not allowed to execute '/bin/echo Test passed?' as root on server01.
```

## Disabling the password prompt

To let a user run commands without entering their password, add `NOPASSWD:`:

```sudoers theme={null}
# Allow trinity to run any command without a password
trinity ALL=(ALL) NOPASSWD: ALL
```

> **lightbulb** Use `NOPASSWD:` sparingly; it increases convenience but may reduce auditability.

***

## Links and References

* [sudo Manual (sudoers)](https://www.sudo.ws/man/1.8.13/sudoers.man.html)
* [visudo Documentation](https://www.sudo.ws/man/1.8.13/visudo.man.html)
* [Linux User Management](https://www.linux.com/training-tutorials/introduction-linux-user-accounts/)

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/7e2b6f48-e58c-4d05-82e2-feb0f5f876f5/lesson/46d7c494-6c04-4bb9-bac0-cfec84e594c6)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/7e2b6f48-e58c-4d05-82e2-feb0f5f876f5/lesson/3dcaca87-ddaf-4de8-b0d9-7a82f102fe4d)


# Creating a Chatbot for a Restaurant

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Building-an-Interactive-Chatbot/Creating-a-Chatbot-for-a-Restaurant/page

This tutorial guides you in building an interactive chatbot for a fast-food restaurant using OpenAI and Panel in Python.

In this tutorial, you’ll build an interactive chatbot for **Burger Bliss**, a fast-food restaurant. We’ll cover:

1. Imports and API key configuration
2. Implementing the chat completion function
3. Collecting messages and updating the UI
4. Crafting the system prompt with menu details
5. Building the Panel-based UI
6. Running an example conversation and inspecting the message history

***

## 1. Imports and API Key Configuration

First, install and import the required libraries:

```bash theme={null}
pip install openai panel
```

```python theme={null}
import os
import openai
import panel as pn
