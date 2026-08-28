# Output:
# user1
# user2
# user3
# user4
# user5
# user6
```

To flip the order (last line first), pipe through `tac`:

```bash theme={null}
tac /home/users.txt
# Output:
# user6
# user5
# user4
# user3
# user2
# user1
```

### Inspecting the Start or End of Large Logs

Log files can grow huge. Quickly grab the first or last N lines:

* **Last 10 lines (default):**\
  `tail /var/log/dnf.log`

* **Last 20 lines:**\
  `tail -n 20 /var/log/dnf.log`

* **First 20 lines:**\
  `head -n 20 /var/log/dnf.log`

These let you preview recent errors or initial startup messages without opening the full file.

## Automating In-File Replacements with `sed`

The stream editor `sed` excels at find-and-replace tasks:

1. **Preview changes** (no file modified):
   ```bash theme={null}
   sed 's/canda/canada/g' userinfo.txt
   ```
2. **Apply in-place** (`-i`) substitutions:
   ```bash theme={null}
   sed -i 's/canda/canada/g' userinfo.txt
   cat userinfo.txt
   ```

* `s/pattern/replacement/g` replaces all occurrences on each line.
* The `-i` flag edits the file directly.

<Callout icon="triangle-alert">
  Always preview your `sed` commands without `-i` first. To keep a backup, use `-i.bak` (e.g., `sed -i.bak 's/old/new/g' file`).
</Callout>

## Extracting Fields with `cut`

When working with delimited data (spaces, commas, or tabs), `cut` slices out columns:

<Frame>
  ![The image shows a terminal interface with a command prompt on the left and a text file named "userinfo.txt" on the right, containing a list of names, cities, countries, and numbers.](https://kodekloud.com/kk-media/image/upload/v1752881405/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Process-Text-Streams-Using-Filters/terminal-command-prompt-userinfo-file.jpg)
</Frame>

* **By space delimiter:** extract the first field (name)
  ```bash theme={null}
  cut -d ' ' -f 1 userinfo.txt
  ```
* **By comma delimiter:** extract the third field (country) and save
  ```bash theme={null}
  cut -d ',' -f 3 userinfo.txt > countries.txt
  ```

## Listing Unique Entries with `sort` and `uniq`

The `uniq` filter only removes adjacent duplicates—sort first to catch all duplicates:

```bash theme={null}
sort countries.txt | uniq
```

<Callout icon="lightbulb">
  If your file isn’t sorted, `uniq` may leave non-adjacent duplicates. Always sort before `uniq` for a full cleanse.
</Callout>

## Comparing Files with `diff`

Spot differences between configuration files using:

* **Basic side-by-side:**
  ```bash theme={null}
  diff file1 file2
  ```
* **Unified context (`-c`):**
  ```bash theme={null}
  diff -c file1 file2
  ```
* **Two-column view (`-y`):**
  ```bash theme={null}
  diff -y file1 file2
  ```

This helps pinpoint changes before editing or deploying configurations.

## Quick Reference: Linux Text Filters

| Command | Purpose                                  | Basic Usage                     |
| ------- | ---------------------------------------- | ------------------------------- |
| `cat`   | Dump entire file                         | `cat file.txt`                  |
| `tac`   | Reverse file order                       | `tac file.txt`                  |
| `head`  | Show first N lines                       | `head -n 20 file.log`           |
| `tail`  | Show last N lines                        | `tail -n 20 file.log`           |
| `sed`   | Stream editor (find & replace)           | `sed -i 's/old/new/g' file.txt` |
| `cut`   | Extract columns from delimited streams   | `cut -d',' -f3 file.csv`        |
| `sort`  | Sort lines alphabetically or numerically | `sort file.txt`                 |
| `uniq`  | Remove adjacent duplicates               | `sort file.txt \| uniq`         |
| `diff`  | Compare files line by line               | `diff -y file1 file2`           |

## Links and References

* [GNU Coreutils Manual](https://www.gnu.org/software/coreutils/manual/)
* [sed – An Introduction and Tutorial](https://www.grymoire.com/Unix/Sed.html)
* [Linux `diff` Tutorial](https://www.gnu.org/software/diffutils/manual/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/2490f961-886c-4531-be8c-915cccff60a9/lesson/cfb18eb7-37ff-4763-ad32-3fd55c995d8b" />
</CardGroup>


# Work on the Command Line Part 1 Log into remote and graphical consoles demo

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/GNU-and-Unix-Commands/Work-on-the-Command-Line-Part-1-Log-into-remote-and-graphical-consoles-demo/page

This tutorial explains how to log into CentOS using local GUI, RDP, and SSH methods.

In this tutorial, you will learn how to:

* Perform a local graphical login on a CentOS VM
* Connect remotely via Remote Desktop Protocol (RDP)
* Access the shell in text mode using SSH

## Table of Contents

1. [Local Graphical Login on CentOS](#local-graphical-login-on-centos)
2. [Remote Graphical Login via RDP](#remote-graphical-login-via-rdp)
3. [Text-Mode Login via SSH](#text-mode-login-via-ssh)
4. [Summary and References](#summary-and-references)

***

## Local Graphical Login on CentOS

First, verify that your CentOS VM is set to boot into the graphical target with GNOME installed:

```bash theme={null}
sudo dnf groupinstall "Server with GUI"
sudo systemctl set-default graphical.target
sudo reboot
```

<Callout icon="lightbulb">
  If the VM defaults to text mode, start the graphical login with `sudo systemctl start gdm` or install the necessary GNOME packages.
</Callout>

Once the GNOME login screen appears:

1. Select your username.
2. Enter your password.
3. Click **Sign In**.

After GNOME loads, use the top-right menu to log out and prepare for the remote login demonstration.

***

## Remote Graphical Login via RDP

To enable RDP access on a CentOS server, install and configure the xrdp service:

```bash theme={null}
sudo dnf install xrdp
sudo systemctl enable --now xrdp
sudo firewall-cmd --add-service=rdp --permanent
sudo firewall-cmd --reload
```

<Callout icon="triangle-alert">
  Exposing RDP (port 3389) on public networks may introduce security vulnerabilities. Use a VPN or SSH tunnel when possible.
</Callout>

Next, open your preferred RDP client (e.g., Microsoft Remote Desktop) and enter the server’s IP address:

1. Launch the RDP client application.
2. Input the IP address (for example, `192.168.0.18`) and click **Connect**.
3. At the login prompt, the username field may auto-fill with `student`. Enter the password and proceed.

<Frame>
  ![The image shows a login screen for a remote desktop session with fields for session type, username, and password. The background is teal, and there's a logo with the text "Just connecting."](https://kodekloud.com/kk-media/image/upload/v1752881411/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Work-on-the-Command-Line-Part-1-Log-into-remote-and-graphical-consoles-demo/remote-desktop-login-screen-teal.jpg)
</Frame>

Once authenticated, verify the connection by checking the IP address in the RDP window’s title bar. Then, navigate to **Activities** → **GNOME Terminal** to open a terminal session.

<Frame>
  ![The image shows a computer desktop with a dark-themed terminal window open, set against a blue geometric patterned wallpaper.](https://kodekloud.com/kk-media/image/upload/v1752881412/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Work-on-the-Command-Line-Part-1-Log-into-remote-and-graphical-consoles-demo/dark-terminal-desktop-blue-wallpaper.jpg)
</Frame>

***

## Text-Mode Login via SSH

From the GNOME Terminal in the RDP session, initiate an SSH connection to your CentOS VM at `192.168.0.17` with the `aaron` account:

```bash theme={null}
[student@LFCS-CentOS2 ~]$ ssh aaron@192.168.0.17
aaron@192.168.0.17's password: 
Activate the web console with: systemctl enable --now cockpit.socket

Last login: Tue Oct 19 04:22:38 2021
[aaron@LFCS-CentOS ~]$ exit
logout
Connection to 192.168.0.17 closed.
[student@LFCS-CentOS2 ~]$
```

When finished, close the terminal emulator and end your RDP session.

***

## Summary and References

This lesson covered three login methods for CentOS:

| Login Method     | Description                     | How to Access                    |
| ---------------- | ------------------------------- | -------------------------------- |
| Local GUI        | GNOME desktop on local VM       | Select user → Enter password     |
| Remote GUI (RDP) | GNOME desktop via RDP client    | Use RDP client → Connect → Login |
| SSH Text Mode    | Command-line interface over SSH | `ssh user@host`                  |

Further reading:

* [GNOME Project][GNOME]
* [Microsoft RDP Documentation][RDP]
* [OpenSSH Manual][SSH]

[GNOME]: https://www.gnome.org/

[RDP]: https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/clients/remote-desktop-clients

[SSH]: https://www.openssh.com/manual.html

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/2490f961-886c-4531-be8c-915cccff60a9/lesson/e54c417e-f5fb-45d9-95e2-d52f34538a18" />
</CardGroup>
