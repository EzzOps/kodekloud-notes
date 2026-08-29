# | Alias                      | Name                                | Enabled | GPG Check | Refresh
--+----------------------------+-------------------------------------+---------+-----------+--------
1 | openSUSE-Leap-15.1-1       | openSUSE-Leap-15.1-1               | No      | ----      | ----
2 | repo-non-oss               | Non-OSS Repository                  | Yes     | (r) Yes   | Yes
3 | repo-oss                   | Main Repository                     | Yes     | (r) Yes   | Yes
4 | repo-source                | Source Repository                   | No      | ----      | ----
```

Enabled = **Yes** means active; **No** means disabled.

### Enabling, Disabling, and Auto-Refresh

| Command                             | Description                     |
| ----------------------------------- | ------------------------------- |
| `zypper modifyrepo -d <repo-alias>` | Disable a repository            |
| `zypper modifyrepo -e <repo-alias>` | Enable a repository             |
| `zypper modifyrepo -f <repo-alias>` | Enable auto-refresh for a repo  |
| `zypper modifyrepo -F <repo-alias>` | Disable auto-refresh for a repo |

Example:

```bash theme={null}
# Disable
sudo zypper modifyrepo -d repo-non-oss

# Enable
sudo zypper modifyrepo -e repo-non-oss

# Enable auto-refresh
sudo zypper modifyrepo -f repo-non-oss

# Disable auto-refresh
sudo zypper modifyrepo -F repo-non-oss
```

### Adding and Removing Repositories

* **Add a new repository**:

  ```bash theme={null}
  sudo zypper addrepo http://packman.inode.at/suse/openSUSE-Leap_15.1/packman packman
  ```

  Sample output:

  ```text theme={null}
  Adding repository 'packman' ...........................[done]
  Repository 'packman' successfully added
  URI         : http://packman.inode.at/suse/openSUSE-Leap_15.1/
  Enabled     : Yes
  GPG Check   : Yes
  Autorefresh : No
  Priority    : 99 (default)
  ```

* **Remove a repository**:

  ```bash theme={null}
  sudo zypper removerepo packman
  ```

  Sample output:

  ```text theme={null}
  Removing repository 'packman' ........................[done]
  Repository 'packman' has been removed.
  ```

***

## Links and References

* [Zypper User Guide](https://doc.opensuse.org/projects/libzypp/doc/zypper/)
* [openSUSE Documentation](https://en.opensuse.org/Portal:Zypper)
* [SUSE Linux Enterprise Server](https://www.suse.com/products/server/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/78ca0fa8-2083-408a-bf8a-2775b09fbf1d/lesson/ae5d58db-cf95-4eec-9da4-e879559d4af8" />
</CardGroup>


# Use RPM and YUM Package Management

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/Linux-Installation-and-Package-Management/Use-RPM-and-YUM-Package-Management/page

This guide covers using YUM and DNF for package management on RHEL, including system registration, repository configuration, and package installation.

Managing software on Red Hat Enterprise Linux (RHEL) relies on YUM (Yellowdog Updater, Modified) or its successor, `dnf`. In this guide, you’ll learn how to register your system, configure repositories, and install, update, or remove packages. Most `yum` commands work identically with `dnf`; just replace `yum` with `dnf` where desired.

<Callout icon="lightbulb">
  If you prefer `dnf` over `yum`, you can use it interchangeably, for example:

  ```bash theme={null}
  sudo dnf install httpd
  ```
</Callout>

***

## 1. Registering with Red Hat Subscription Management

Before accessing Red Hat repositories, register and attach your system to a subscription.

```bash theme={null}
sudo subscription-manager register \
  --username your-redhat-developer-username \
  --password your-redhat-password
```

Once registered, attach the system automatically:

```bash theme={null}
sudo subscription-manager attach --auto
```

<Callout icon="triangle-alert">
  Ensure your subscription is active; expired subscriptions will prevent you from installing or updating packages.
</Callout>

***

## 2. Listing and Inspecting Repositories

A repository (repo) is a storage location—online or on your network—containing RPM packages, metadata, and signing keys.

### 2.1 View Enabled Repositories

```bash theme={null}
sudo yum repolist
```

Sample output:

```text theme={null}
repo id                             repo name
rhel-8-for-x86_64-appstream-rpms    Red Hat Enterprise Linux 8 for x86_64 - AppStream (RPMs)
rhel-8-for-x86_64-baseos-rpms       Red Hat Enterprise Linux 8 for x86_64 - BaseOS (RPMs)
```

### 2.2 View Repository Details

Add `-v` for verbose details, including each repo’s URL and configuration file:

```bash theme={null}
sudo yum repolist -v
```

Key fields in the output:

* **Repo-baseurl**: URL where YUM fetches packages
* **Repo-filename**: Local file under `/etc/yum.repos.d/`

***

## 3. Enabling and Disabling Repositories

Some packages reside in optional or specialized repos.

### 3.1 List All Repositories

```bash theme={null}
sudo yum repolist --all
```

### 3.2 Using Subscription Manager

Enable or disable by repo ID:

```bash theme={null}
sudo subscription-manager repos --enable   rhel-8-for-x86_64-codeready-builder-rpms
sudo subscription-manager repos --disable  rhel-8-for-x86_64-codeready-builder-rpms
```

### 3.3 Using yum-config-manager

First, install `yum-utils`:

```bash theme={null}
sudo yum install yum-utils
```

Then enable or disable:

```bash theme={null}
sudo yum-config-manager --enable  some-repo-id
sudo yum-config-manager --disable some-repo-id
```

***

## 4. Adding a Custom Repository

To add a third-party or local repo:

```bash theme={null}
sudo yum install yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
