# Use Debian Package Management Part 2

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/Linux-Installation-and-Package-Management/Use-Debian-Package-Management-Part-2/page

This guide explores advanced Debian package management using APT, covering installation, upgrades, removals, and repository configuration.

In this guide, we’ll dive deeper into Debian package management using APT (Advanced Package Tool). APT is a powerful front-end to `dpkg` that automates dependency resolution, offers advanced search capabilities, and simplifies package installation, upgrades, and removals. It works with software repositories—which can be remote servers, local mirrors, or even CD-ROMs. Official repositories are maintained by distributions like [Debian](https://www.debian.org/) and [Ubuntu](https://ubuntu.com/), and you can add third-party or custom repos as needed.

![The image is a slide describing the Advanced Package Tool (APT), highlighting its features such as advanced search, dependency resolution, and its role in working with software repositories.](https://kodekloud.com/kk-media/image/upload/v1752881445/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Use-Debian-Package-Management-Part-2/apt-advanced-features-search-dependency.jpg)

## APT Command-Line Utilities

| Command                    | Purpose                                          |
| -------------------------- | ------------------------------------------------ |
| `sudo apt-get [options]`   | Install, upgrade, or remove packages             |
| `sudo apt-cache [options]` | Search and display package information           |
| `sudo apt-file [options]`  | Search for files within packages (inst./uninst.) |
| `sudo apt [options]`       | Unified interface combining apt-get & apt-cache  |

> **triangle-alert** The `apt` command is more user-friendly, but it may not be installed on older systems. Always know how to use both `apt-get` and `apt-cache`.

***

## 1. Updating the Package Index

Before installing or upgrading any software, refresh your local package index:

```bash theme={null}
sudo apt-get update
```

This fetches the latest package lists from all configured repositories.

***

## 2. Installing and Upgrading Packages

To install a new package—or upgrade it if already present—use:

```bash theme={null}
sudo apt-get install xournal
```

Sample output:

```bash theme={null}
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following NEW packages will be installed:
  xournal
0 upgraded, 1 newly installed, 0 to remove and 75 not upgraded.
Need to get 285 kB of archives.
After this operation, 1041 kB of additional disk space will be used.
```

> **lightbulb** You can install multiple packages at once, for example:\
  `sudo apt-get install git curl vim`

***

## 3. Removing and Purging Packages

* **Remove (keep config files):**

  ```bash theme={null}
  sudo apt-get remove xournal
  ```

* **Purge (remove config files too):**

  ```bash theme={null}
  sudo apt-get purge p7zip
  # or equivalently:
  sudo apt-get remove --purge p7zip
  ```

APT will list affected packages and ask for confirmation before proceeding.

***

## 4. Fixing Broken Dependencies

When a manual `.deb` install triggers unmet dependencies:

```bash theme={null}
sudo dpkg -i --force openshot-qt_2.4.3+dfsg1-1_all.deb
