# Install and update software packages from Red Hat Network a remote repository or from the local file system

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Deploy-Configure-and-Maintain-Systems/Install-and-update-software-packages-from-Red-Hat-Network-a-remote-repository-or-from-the-local-file-system/page

This guide explains how to install and update software packages on a RHEL system using YUM and DNF.

In this guide, we explain how to install and update software packages on a RHEL system using YUM. While many RHEL installations still rely on YUM, newer systems may use DNF; in most cases, simply replace “yum” with “dnf” in the commands below.

RHEL systems use the Red Hat Subscription Manager (subscription-manager) to manage subscriptions and access updates. When you first set up your RHEL system, you must register it with a valid Red Hat subscription to receive the latest packages and security updates. Otherwise, you might encounter an error message from YUM indicating that the system isn’t registered to Red Hat Subscription Management.

> **lightbulb** If you are using DNF instead of YUM, almost all commands described here will work similarly by replacing `yum` with `dnf`.

## Registering with Red Hat Subscription Management

Before accessing software repositories, register your system using your Red Hat Developer account credentials:

```bash theme={null}
sudo subscription-manager register --username your-redhat-developer-username --password your-redhat-password
```

After successful registration, attach your system to an available subscription automatically:

```bash theme={null}
sudo subscription-manager attach --auto
```

## Software Repositories

Software repositories contain packages, configuration files, and libraries. These repositories are usually hosted on the internet, though enterprises can host private repositories on a local network.

### Viewing Enabled Repositories

To list the repositories currently enabled on your system, run:

```bash theme={null}
sudo yum repolist
```

The command output will appear similar to:

```bash theme={null}
repo id                           repo name
rhel-8-for-x86_64-appstream-rpms  Red Hat Enterprise Linux 8 for x86_64 - AppStream (RPMs)
rhel-8-for-x86_64-baseos-rpms     Red Hat Enterprise Linux 8 for x86_64 - BaseOS (RPMs)
```

For more detailed information, including the repository URL addresses, use the verbose flag:

```bash theme={null}
sudo yum repolist -v
```

Expected output excerpt:

```bash theme={null}
Repo-baseurl     : https://cdn.redhat.com/content/dist/rhel8/8/x86_64/appstream/os
Repo-filename    : /etc/yum.repos.d/redhat.repo
```

Here, `Repo-baseurl` indicates the repository URL, and `Repo-filename` shows the path to the configuration file on your system.

### Enabling Optional Repositories

If the default repositories do not include the package you need, you can enable optional repositories such as the CodeReady Builder RPMs. First, list all available repositories:

```bash theme={null}
sudo yum repolist --all
```

The output may include entries like:

```bash theme={null}
repo id
codeready-builder-for-rhel-8-x86_64-debug-rpms
codeready-builder-for-rhel-8-x86_64-eus-debug-rpms
codeready-builder-for-rhel-8-x86_64-eus-rpms
codeready-builder-for-rhel-8-x86_64-source-rpms
codeready-builder-for-rhel-8-x86_64-rpms
repo name
Red Hat CodeReady Linux Builder for RHEL 8 x86_64 (Debug RPMs)
Red Hat CodeReady Linux Builder for RHEL 8 x86_64 - Extended Update Support (Debug RPMs)
Red Hat CodeReady Linux Builder for RHEL 8 x86_64 - Extended Update Support (RPMs)
Red Hat CodeReady Linux Builder for RHEL 8 x86_64 - Extended Update Support (Source RPMs)
Red Hat CodeReady Linux Builder for RHEL 8 x86_64 (RPMs)
status
disabled
disabled
disabled
disabled
disabled
```

To enable an optional repository, use its repo ID:

```bash theme={null}
sudo subscription-manager repos --enable codeready-builder-for-rhel-8-x86_64-rpms
```

To disable the repository, replace `--enable` with `--disable`:

```bash theme={null}
sudo subscription-manager repos --disable codeready-builder-for-rhel-8-x86_64-rpms
```

Alternatively, use yum-utils with the yum-config-manager tool:

```bash theme={null}
sudo yum-config-manager --enable codeready-builder-for-rhel-8-x86_64-rpms
```

Verify changes by listing all repositories again:

```bash theme={null}
sudo yum repolist --all
```

## Adding Custom Repositories

There are times when you need to add external repositories from a specific URL or a local network. First, ensure that the yum-utils package is installed to access the yum-config-manager:

```bash theme={null}
sudo yum install yum-utils
```

Next, add a repository. For example, to add an internet-based repository:

```bash theme={null}
sudo yum-config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
```

For a repository hosted on a local network:

```bash theme={null}
sudo yum-config-manager --add-repo 192.168.1.220/BaseOS.repo
```

After adding, verify the repository configuration:

```bash theme={null}
sudo yum repolist -v
```

You should see an excerpt like the following in the output:

```bash theme={null}
Repo-filename    : /etc/yum.repos.d/docker-ce.repo
```

### Examining a Custom Repository File

Let’s review the Docker repository file that you added. Open the file using an editor such as Vim:

```bash theme={null}
sudo vi /etc/yum.repos.d/docker-ce.repo
```

The initial lines of the file might look like this:

```bash theme={null}
[docker-ce-stable]
name=Docker CE Stable - $basearch
baseurl=https://download.docker.com/linux/rhel/$releasever/$basearch/stable
enabled=1
gpgcheck=1
gpgkey=https://download.docker.com/linux/rhel/gpg
```

Each element of the repository file serves a purpose:

1. **Repository ID** (e.g., `[docker-ce-stable]`)\
   A unique identifier required for the repository.

2. **Name** (`name=Docker CE Stable - $basearch`)\
   A descriptive label displayed in repository lists.

3. **Base URL** (`baseurl=https://download.docker.com/linux/rhel/$releasever/$basearch/stable`)\
   The URL location for the repository.

4. **Enabled Flag** (`enabled=1`)\
   Indicates active status. Changing to 0 disables the repository.

5. **GPG Check** (`gpgcheck=1`)\
   Enables verification of package integrity using GPG signatures.

6. **GPG Key Location** (`gpgkey=https://download.docker.com/linux/rhel/gpg`)\
   Specifies the URL for the GPG key used in verification.

This format provides a blueprint for creating or modifying repository files for troubleshooting and custom configurations. To remove a custom repository, simply delete its configuration file from `/etc/yum.repos.d/`.

## Managing Packages with YUM

YUM is a powerful tool for installing, updating, reinstalling, and removing packages from both repositories and local RPM files.

### Searching for Packages

If you are unsure of a package name, use the search feature. For instance, to search for packages related to web servers:

```bash theme={null}
sudo yum search web server
```

This command searches for any package containing either "web" or "server" in its description:

```bash theme={null}
cockpit.x86_64 : Web Console for Linux servers
```

For exact phrase matching, enclose the search term in single quotes:

```bash theme={null}
sudo yum search 'web server'
```

This refined search might return:

```bash theme={null}
nginx.x86_64 : A high performance web server and reverse proxy server
```

Once you identify the package (e.g., Nginx), obtain more details by running:

```bash theme={null}
sudo yum info nginx
```

You should see output similar to:

```text theme={null}
Description : Nginx is a web server and a reverse proxy server for HTTP, SMTP, POP3, and IMAP protocols,
              with a strong focus on high concurrency, performance, and low memory usage.
```

### Installing, Reinstalling, and Removing Packages

To install a package like Nginx:

```bash theme={null}
sudo yum install nginx
```

If you need to reinstall a package (for example, if a configuration file was accidentally deleted), use:

```bash theme={null}
sudo yum reinstall nginx
```

To remove a package:

```bash theme={null}
sudo yum remove package_name
```

Sometimes, removing a package leaves behind dependencies. You can clean up these unnecessary dependencies with:

```bash theme={null}
sudo yum autoremove
```

### Installing Software from an RPM File

YUM can also install packages directly from local RPM files. For example, to install the NoMachine package:

1. Download the package:

   ```bash theme={null}
   sudo wget https://download.nomachine.com/download/7.7/Linux/nomachine_7.7.4_1_x86_64.rpm
   ```

2. Install the downloaded RPM file:

   ```bash theme={null}
   sudo yum install ./nomachine_7.7.4_1_x86_64.rpm
   ```

To uninstall software installed via an RPM file, remove it by package name:

```bash theme={null}
sudo yum remove nomachine
```

Then, clean up any remaining dependencies:

```bash theme={null}
sudo yum autoremove
```

## Managing Package Groups

YUM supports package groups, which allow you to manage related collections of packages together.

### Listing Available Groups

List all available package groups with:

```bash theme={null}
sudo yum group list
```

To view a comprehensive list, including hidden groups, run:

```bash theme={null}
sudo yum group list --hidden
```

For example, you might see a group labeled "Server with GUI."

### Installing and Removing Group Packages

To install the "Server with GUI" package group:

```bash theme={null}
sudo yum group install 'Server with GUI'
```

To remove the group:

```bash theme={null}
sudo yum group remove 'Server with GUI'
```

## Updating and Upgrading Packages

Keeping your system up to date is crucial. Begin by checking for available package upgrades:

```bash theme={null}
sudo yum check-upgrade
```

To update all installed packages to their latest versions, run:

```bash theme={null}
sudo yum update
```

> **lightbulb** After upgrading critical components such as the kernel, it is advisable to reboot your system to ensure all changes take effect properly.

***

By following the steps in this guide, you can effectively manage software packages and repositories on your RHEL system using YUM. For more detailed information, consider visiting [Red Hat's official documentation](https://access.redhat.com/documentation).

Happy managing!

- [Watch Video](https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/736506db-a70d-463d-a061-74c768d309b0/lesson/031be5f4-5cee-42bf-9310-f2329aace49a)
