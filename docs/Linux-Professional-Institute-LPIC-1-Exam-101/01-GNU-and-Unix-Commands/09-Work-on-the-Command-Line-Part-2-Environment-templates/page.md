# Work on the Command Line Part 2 Environment templates

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/GNU-and-Unix-Commands/Work-on-the-Command-Line-Part-2-Environment-templates/page

Configuring `/etc/skel` defines default files and settings for new user accounts, streamlining onboarding and enforcing policies.

Configuring the `/etc/skel` directory allows you to define default files and environment settings for every new user account. When you create a user with the `-m` flag, all contents of `/etc/skel` are copied into the new home directory—making it easy to enforce policies, defaults, and customizations.

## Table of Common Skeleton Files

| File            | Purpose                              | Description                                                                   |
| --------------- | ------------------------------------ | ----------------------------------------------------------------------------- |
| `.bashrc`       | Shell configuration                  | Defines aliases, functions, and environment variables for interactive shells. |
| `.bash_profile` | Login shell startup                  | Exports user-specific environment variables and initializes the login shell.  |
| `README`        | Onboarding notice or policy document | Displays a default message or policy for every new user.                      |

## 1. Adding a Default README for All New Users

To inform new users about your site policy or housekeeping rules, place a `README` file in `/etc/skel`:

```bash theme={null}
sudo vim /etc/skel/README
```

Add your message, for example:

```text theme={null}
Please don’t run CPU-intensive processes between 8 am and 10 pm.
```

Save and exit. Every future user will see this notice in their home directory.

> **lightbulb** Files in `/etc/skel` are only applied when a home directory is created (e.g., via `useradd -m`). Existing users are unaffected.

## 2. Testing with a New User

Create a new user named **trinity** and verify that the `README` was copied:

```bash theme={null}
sudo useradd -m trinity
ls -a /home/trinity
