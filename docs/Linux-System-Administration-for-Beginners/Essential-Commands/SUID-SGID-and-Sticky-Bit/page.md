# SUID SGID and Sticky Bit

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/Essential-Commands/SUID-SGID-and-Sticky-Bit/page

This article explains Linux special permissions SUID, SGID, and the sticky bit for secure system administration and access control.

In Linux, special permission bits—SUID, SGID, and the sticky bit—modify how executables and directories behave for different users and groups. Mastering these bits is essential for secure system administration and proper access control.

## What Are Special Permission Bits?

* **SUID (Set User ID)**\
  Runs an executable with the file owner’s user ID.
* **SGID (Set Group ID)**\
  Runs an executable with the owning group’s privileges.
* **Sticky Bit**\
  Restricts deletion of files in shared directories to the file owner or root.

| Octal Prefix | Permission Bit | Effect                             |
| -----------: | -------------: | ---------------------------------- |
|         4xxx |           SUID | Execute file as file owner         |
|         2xxx |           SGID | Execute file as file’s group owner |
|         1xxx |     Sticky Bit | Restrict deletion in directories   |

***

## 1. Set User ID (SUID)

When SUID is set on an executable, the process runs with the file owner’s privileges. Common use cases include `su`, `passwd`, and other administrative tools.

### Step-by-Step

1. Create a test file and view its default permissions:
   ```bash theme={null}
   touch suidfile
   ls -l suidfile
   # -rw-rw-r--. 1 aaron aaron 0 Apr 26 05:08 suidfile
   ```
2. Enable SUID without execute for the owner (octal `4664`):
   ```bash theme={null}
   chmod 4664 suidfile
   ls -l suidfile
   # -rwSrw-r--. 1 aaron aaron 0 Apr 26 05:08 suidfile
   ```

<Callout icon="lightbulb">
  The uppercase `S` indicates SUID is set but the owner’s execute bit is **not** enabled.
</Callout>

3. Grant both execute and SUID for the owner (octal `4764`):
   ```bash theme={null}
   chmod 4764 suidfile
   ls -l suidfile
   # -rwsrwxr--. 1 aaron aaron 0 Apr 26 05:08 suidfile
   ```
   The lowercase `s` shows both SUID and execute bits are active.

<Callout icon="triangle-alert">
  Carefully review which binaries receive the SUID bit. Misconfigured SUID files can introduce security vulnerabilities.
</Callout>

***

## 2. Set Group ID (SGID)

SGID works similarly to SUID but applies to group privileges.

### Step-by-Step

1. Create a test file and inspect permissions:
   ```bash theme={null}
   touch sgidfile
   ls -l sgidfile
   # -rw-rw-r--. 1 aaron aaron 0 Apr 26 05:11 sgidfile
   ```
2. Set SGID without group execute (octal `2664`):
   ```bash theme={null}
   chmod 2664 sgidfile
   ls -l sgidfile
   # -rw-rwSr--. 1 aaron aaron 0 Apr 26 05:11 sgidfile
   ```
   * Uppercase `S` in the group’s execute position shows SGID is set but no execute.
3. Add both group execute and SGID (octal `2764`):
   ```bash theme={null}
   chmod 2764 sgidfile
   ls -l sgidfile
   # -rw-rwsr--. 1 aaron aaron 0 Apr 26 05:11 sgidfile
   ```
   * Lowercase `s` indicates SGID and execute bits are set for the group.

***

## 3. Finding SUID/SGID Files

Quickly locate files with SUID or SGID bits:

```bash theme={null}
