# ... dpkg: dependency problems prevent configuration of openshot-qt: ...
```

Restore consistency by installing missing dependencies:

```bash theme={null}
sudo apt-get install -f
```

This will automatically fetch and install the required packages.

***

## 5. Upgrading All Packages

1. Refresh your index:

   ```bash theme={null}
   sudo apt-get update
   ```

2. Upgrade upgradable packages:

   ```bash theme={null}
   sudo apt-get upgrade
   ```

Example summary:

```bash theme={null}
Reading package lists... Done
Building dependency tree       
Reading state information... Done
Calculating upgrade... Done
The following packages have been kept back:
  gnome-control-center
The following packages will be upgraded:
  cups cups-bsd cups-client cups-common cups-core-drivers cups-daemon ...
74 upgraded, 0 newly installed, 0 to remove and 1 not upgraded.
Need to get 243 MB of archives.
After this operation, 30.7 kB of additional disk space will be used.
Do you want to continue? [Y/n]
```

> **lightbulb** To upgrade one package without affecting others, use:

  ```bash theme={null}
  sudo apt-get install --only-upgrade unrar
  ```

***

## 6. Cleaning the Package Cache

APT caches downloaded `.deb` files in `/var/cache/apt/archives`. Free up disk space by running:

```bash theme={null}
sudo apt-get clean
```

***

## 7. Searching Packages with `apt-cache`

* **Search by keyword:**

  ```bash theme={null}
  sudo apt-cache search p7zip
  ```

  Sample output:

  ```bash theme={null}
  liblzma-dev     - XZ-format compression library - development files
  liblzma5        - XZ-format compression library
  forensics-extra - Forensics Environment - extra console components (metapackage)
  p7zip           - 7zr file archiver with high compression ratio
  p7zip-full      - 7z and 7za file archivers with high compression ratio
  p7zip-rar       - non-free rar module for p7zip
  ```

* **Show package details:**

  ```bash theme={null}
  sudo apt-cache show liblzma5
  ```

  Key fields:

  ```text theme={null}
  Package: liblzma5
  Version: 5.2.4-1
  Depends: libc6 (>= 2.17)
  Description-en: XZ-formatted compression library
   LZMA is the successor to the Lempel-Ziv-Markov-chain Algorithm...
  ```

***

## 8. Configuring Software Repositories

Repository entries reside in `/etc/apt/sources.list` or under `/etc/apt/sources.list.d/`. Each line follows:

```text theme={null}
<type> <URL> <distribution> <components>
```

Example (Ubuntu “disco”):

```bash theme={null}
deb http://us.archive.ubuntu.com/ubuntu/ disco main restricted universe multiverse
```

| Component  | Description                                                     |
| ---------- | --------------------------------------------------------------- |
| main       | Officially supported open-source packages                       |
| restricted | Supported closed-source software (e.g., proprietary drivers)    |
| universe   | Community-maintained open-source packages                       |
| multiverse | Unsupported closed-source or patented software                  |
| contrib    | DFSG-compliant packages depending on non-main components        |
| non-free   | Packages not compliant with the Debian Free Software Guidelines |
| security   | Security updates                                                |
| backports  | Newer versions backported from testing or unstable branches     |

After editing or adding a `.list` file, always run:

```bash theme={null}
sudo apt-get update
```

### Example: Adding Debian Buster Backports

```bash theme={null}
sudo vi /etc/apt/sources.list.d/buster-backports.list
```

Append:

```text theme={null}
deb     http://deb.debian.org/debian buster-backports main contrib non-free
deb-src http://deb.debian.org/debian buster-backports main contrib non-free
```

***

## 9. Using `apt-file`

The `apt-file` tool lets you search for individual files within packages, even if they aren’t installed.

1. Install and initialize:

   ```bash theme={null}
   sudo apt-get install apt-file
   sudo apt-file update
   ```

2. List package contents:

   ```bash theme={null}
   sudo apt-file list unrar
   # unrar: /usr/bin/unrar-nonfree
   # unrar: /usr/share/doc/unrar/changelog.Debian.gz
   ```

3. Search for a specific file:

   ```bash theme={null}
   sudo apt-file search libsdl2.so
   ```

Unlike `dpkg-query`, `apt-file` can search across all available (but not yet installed) packages.

***

Test your knowledge with the included quiz!

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/78ca0fa8-2083-408a-bf8a-2775b09fbf1d/lesson/d6b848b0-fee5-4327-bbcb-19ada81eb134)


# Use RPM and YUM Package Management Zypper

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/Linux-Installation-and-Package-Management/Use-RPM-and-YUM-Package-Management-Zypper/page

This article explains how to use Zypper for package management in SUSE Linux and openSUSE, covering installation, removal, and repository management.

Zypper is the powerful command-line package manager for SUSE Linux and openSUSE, providing functionality similar to YUM and APT. It enables you to install, update, and remove packages, automatically resolving dependencies. Because Zypper relies on up-to-date repository metadata, it’s best practice to refresh before performing searches or installations.

> **lightbulb** You need `sudo` privileges to run Zypper commands that modify the system.\
  Always refresh metadata to ensure you get the latest package versions.

***

## Refreshing Package Metadata

Before you search or install packages, update metadata from all enabled repositories:

```bash theme={null}
sudo zypper refresh
```

This fetches the latest repository data so Zypper can see available package versions.

***

## Searching for Packages

Use the `se` (search) command to find packages by name or keyword:

```bash theme={null}
sudo zypper se gnumeric
```

Sample output:

```text theme={null}
Loading repository data...
Reading installed packages...
S | Name           | Summary                         | Type
--+----------------+---------------------------------+--------
  | gnumeric       | Spreadsheet application         | package
  | gnumeric-devel | Development files for Gnumeric  | package
  | gnumeric-doc   | Documentation for Gnumeric      | package
  | gnumeric-lang  | Translations for Gnumeric       | package
```

***

## Listing Installed Packages

To list **all** installed packages:

```bash theme={null}
sudo zypper se -i
```

To check if a specific package (e.g., `firefox`) is installed:

```bash theme={null}
sudo zypper se -i firefox
```

Example when Firefox is installed:

```text theme={null}
Loading repository data...
Reading installed packages...
S | Name                           | Summary                     | Type
--+--------------------------------+-----------------------------+--------
i | MozillaFirefox                 | Mozilla Firefox Web Browser | package
  | MozillaFirefox-branding-openSUSE | Branding files for openSUSE | package
  | MozillaFirefox-translations-common | Common translations     | package
```

***

## Installing Packages

### From Repositories

Install a package from enabled repositories with the `in` (install) command:

```bash theme={null}
sudo zypper in unrar
```

Interactive example:

```text theme={null}
Resolving package dependencies...
The following NEW package is going to be installed:
  unrar

1 new package to install.
Overall download size: 141.2 KiB. After the operation, additional 301.6 KiB will be used.
Continue? [y/n/v/...? shows all options] (y): y
Retrieving package unrar-5.7.5-lp151.1.1.x86_64 ...................................[done]
(1/1) Installing: unrar-5.7.5-lp151.1.1.x86_64 ..........................................[done]
```

### From a Local RPM

To install an RPM file stored on your machine:

```bash theme={null}
sudo zypper in /path/to/package.rpm
```

Zypper will attempt to resolve dependencies against your enabled repositories.

***

## Removing Packages

Use the `rm` (remove) command to uninstall a package and any packages that depend on it:

```bash theme={null}
sudo zypper rm unrar
```

Example:

```text theme={null}
Resolving package dependencies...
The following package is going to be REMOVED:
  unrar

1 package to remove.
After the operation, 301.6 KiB will be freed.
Continue? [y/n/v/...? shows all options] (y): y
(1/1) Removing unrar-5.7.5-lp151.1.1.x86_64 ..........................................[done]
```

> **triangle-alert** Removing packages may also uninstall dependencies required by other applications. Double-check the list before confirming.

***

## Managing Software Repositories

### Listing Repositories

Display all configured repositories and their status:

```bash theme={null}
sudo zypper repos
```

Sample output:

```text theme={null}
