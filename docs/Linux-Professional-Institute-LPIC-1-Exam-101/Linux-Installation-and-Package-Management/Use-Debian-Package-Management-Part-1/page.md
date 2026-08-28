# libfuse.so.2 (libc6,x86-64) => /lib/x86_64-linux-gnu/libfuse.so.2
```

Inspect the symlink:

```bash theme={null}
ls -l /lib/x86_64-linux-gnu/libfuse.so.2
# lrwxrwxrwx 1 root root 16 Aug 21 2018 /lib/x86_64-linux-gnu/libfuse.so.2 -> libfuse.so.2.9.7
```

## 6. LD\_LIBRARY\_PATH Environment Variable

`LD_LIBRARY_PATH` is a colon-separated list of directories the dynamic linker checks before standard paths.

```bash theme={null}
export LD_LIBRARY_PATH=/usr/local/mylib:$LD_LIBRARY_PATH
echo $LD_LIBRARY_PATH
# /usr/local/mylib:...
```

To remove it:

```bash theme={null}
unset LD_LIBRARY_PATH
```

<Callout icon="triangle-alert">
  Overusing `LD_LIBRARY_PATH` can cause version conflicts and security issues. Prefer updating `/etc/ld.so.conf.d/` and running `ldconfig` for persistent changes.
</Callout>

For permanent updates, add the `export` line to `~/.bashrc` or `/etc/profile`.

## 7. Inspecting Dependencies with ldd

Use `ldd` to list shared libraries an executable depends on:

```bash theme={null}
ldd /usr/bin/git
```

Example output:

```text theme={null}
linux-vdso.so.1 =>  (0x00007ffcbb310000)
libpcre.so.3 => /lib/x86_64-linux-gnu/libpcre.so.3 (0x00007f18241eb000)
libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007f1823fd1000)
libresolv.so.2 => /lib/x86_64-linux-gnu/libresolv.so.2 (0x00007f1823db6000)
libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007f1823b99000)
librt.so.1 => /lib/x86_64-linux-gnu/librt.so.1 (0x00007f1823991000)
libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f18235c7000)
/lib64/ld-linux-x86-64.so.2 (0x00007f182445b000)
```

To list unused direct dependencies:

```bash theme={null}
ldd -u /usr/bin/git
```

Example:

```text theme={null}
Unused direct dependencies:
    /lib/x86_64-linux-gnu/libz.so.1
    /lib/x86_64-linux-gnu/libpthread.so.0
    /lib/x86_64-linux-gnu/librt.so.1
```

Unused entries often result from linker options during the build process.

***

## References

* [GNU ldconfig Manual](https://man7.org/linux/man-pages/man8/ldconfig.8.html)
* [Linux Shared Libraries HOWTO](https://tldp.org/HOWTO/Program-Library-HOWTO/shared-libraries.html)
* [ld.so.conf Configuration](https://man7.org/linux/man-pages/man5/ld.so.conf.5.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/78ca0fa8-2083-408a-bf8a-2775b09fbf1d/lesson/fd8ddef4-51d5-41b5-83cd-b388e3ef653f" />
</CardGroup>


# Use Debian Package Management Part 1

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/Linux-Installation-and-Package-Management/Use-Debian-Package-Management-Part-1/page

This article covers the fundamentals of using dpkg for managing Debian packages, including installation, removal, dependency handling, and package inspection.

Debian’s native package manager, `dpkg`, handles the installation, upgrade, and removal of `.deb` packages on Debian‐based systems. In the early days of Linux, software was distributed as source archives (`.tar.gz`) requiring manual compilation. As distributions matured, package managers automated dependency resolution, file tracking, and version control. This article covers the fundamentals of using `dpkg` to:

* Install and upgrade packages
* Handle dependencies
* Remove or purge packages
* Force operations (with caution)
* Inspect package contents and metadata
* Reconfigure installed packages

Whether you’re a sysadmin automating deployments or a developer packaging your own software, understanding `dpkg` is essential for reliable Debian system management.

## 1. Installing and Upgrading Packages

To install a new `.deb` file or upgrade an existing one:

```bash theme={null}
sudo dpkg -i mypackage.deb
```

* If no version is installed, `dpkg` adds a fresh copy.
* If an older version exists, it upgrades in place.

<Callout icon="lightbulb">
  For automated dependency resolution, consider using [`apt`](https://wiki.debian.org/Teams/Apt) or `apt-get` instead.\
  `sudo apt install ./mypackage.deb` will fetch missing dependencies automatically.
</Callout>

### Handling Dependency Errors

When dependencies are missing, `dpkg` aborts and lists unmet requirements:

```bash theme={null}
sudo dpkg -i openshot-qt_2.4.3+dfsg1-1_all.deb
```

Sample output:

```text theme={null}
dpkg: dependency problems prevent configuration of openshot-qt:
 openshot-qt depends on fonts-cantarell; however:
  Package fonts-cantarell is not installed.
 ...
dpkg: error processing package openshot-qt (--install):
 dependency problems - leaving unconfigured
```

You must install each required `.deb` manually or switch to `apt` for automatic resolution.

***

## 2. Removing and Purging Packages

### 2.1 Remove (keep configuration files)

```bash theme={null}
sudo dpkg -r unrar
```

`dpkg` checks reverse dependencies and refuses removal if other packages rely on it:

```bash theme={null}
sudo dpkg -r p7zip
```

```text theme={null}
dpkg: dependency problems prevent removal of p7zip:
 winetricks depends on p7zip; however:
  Package p7zip is to be removed.
 ...
```

To remove multiple packages at once:

```bash theme={null}
sudo dpkg -r unrar p7zip
```

### 2.2 Purge (remove package and configuration)

```bash theme={null}
sudo dpkg -P unrar p7zip
```

Purging deletes all configuration files, freeing up disk space and resetting system state.

***

## 3. Forcing Operations

You can bypass dependency and safety checks—but this can break your system!

```bash theme={null}
sudo dpkg -i --force-depends openshot-qt_2.4.3+dfsg1-1_all.deb
```

Use `--force-all` to override nearly all safeguards. Only force when you understand the implications.

<Callout icon="triangle-alert">
  Forcing package operations may lead to an inconsistent system state. Always have backups and test in a sandbox before using on production.
</Callout>

***

## 4. Inspecting Packages

Here’s a quick reference for common `dpkg` inspection commands:

| Command                         | Description                               |
| ------------------------------- | ----------------------------------------- |
| `dpkg -I mypackage.deb`         | Show metadata (version, maintainer, deps) |
| `dpkg --get-selections`         | List all installed packages               |
| `dpkg -L unrar`                 | List files installed by a package         |
| `dpkg-query -S /usr/bin/unrar*` | Find which package owns a given file      |

### 4.1 View Package Metadata

```bash theme={null}
dpkg -I mypackage.deb
```

### 4.2 List Files in a Package

```bash theme={null}
sudo dpkg -L unrar
```

Sample output:

```text theme={null}
/usr/bin/unrar-nonfree
/usr/share/doc/unrar/changelog.Debian.gz
/usr/share/man/man1/unrar-nonfree.1.gz
```

### 4.3 Identify Owning Package of a File

```bash theme={null}
dpkg-query -S /usr/bin/unrar-nonfree
```

Output:

```text theme={null}
unrar: /usr/bin/unrar-nonfree
```

***

## 5. Reconfiguring Packages

Sometimes you need to rerun a package’s configuration scripts—useful after restoring defaults or changing `debconf` answers:

```bash theme={null}
sudo dpkg-reconfigure tzdata
```

This command re-executes maintainer scripts, prompting you to confirm or update settings as needed.

***

## References

* [dpkg Manual](https://manpages.debian.org/unstable/dpkg/dpkg.1.en.html)
* [Apt User’s Guide](https://wiki.debian.org/Teams/Apt)
* [Debian Package Management](https://www.debian.org/doc/manuals/debian-faq/pkg-basics.en.html)
* [Debian Policy Manual](https://www.debian.org/doc/debian-policy/)

Future installments will cover advanced package building, repository management, and best practices for Debian package maintenance.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/78ca0fa8-2083-408a-bf8a-2775b09fbf1d/lesson/7f4a465c-2c3b-45a6-ada8-6ae201480062" />
</CardGroup>
