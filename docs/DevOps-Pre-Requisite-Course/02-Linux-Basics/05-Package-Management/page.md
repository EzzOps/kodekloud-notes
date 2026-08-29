# Package Management

Source: https://notes.kodekloud.com/docs/DevOps-Pre-Requisite-Course/Linux-Basics/Package-Management/page

This article explains Linux package management using RPM and Yum for software installation and dependency resolution.

Package managers in Linux simplify software installation by automating tasks that would otherwise be manually intensive. In many DevOps and Cloud scenarios, you may need to install components such as web servers, databases, and various DevOps tools. Linux distributions offer a range of package managers to manage this process efficiently.

## RPM-Based Package Management

CentOS, Red Hat Enterprise Linux, and Fedora use an RPM-based system. RPM stands for Red Hat Package Manager, and it distributes software in bundles with the .rpm extension. The basic usage of the RPM command includes:

* Installing a package:\
  Use the `-i` option along with the package name to install software from a specified location.
* Uninstalling a package:\
  Use the `-e` option to remove a package.
* Querying package details:\
  Use the `-q` option to retrieve information about an installed package.

> **lightbulb** RPM does not automatically resolve dependencies. For example, if you install Ansible—which requires Python and additional libraries—using RPM alone will not install missing dependencies.

Below is an example of common RPM commands:

```bash theme={null}
rpm -i telnet.rpm
rpm -e telnet
rpm -q telnet
```

## Dependency Management with Yum

To overcome RPM limitations regarding dependencies, Linux distributions use higher-level package managers like yum. Yum integrates with RPM while automating dependency resolution. When you run a simple command like:

```bash theme={null}
yum install ansible
```

yum searches its configured repositories, locates the specified package and its dependencies, and installs them in the correct order.

### Understanding Repositories

Yum retrieves packages from software repositories—collections of RPM packages stored locally or on remote servers. Repository configuration files are located in the `/etc/yum.repos.d/` directory. Most operating systems include a default set of repositories offering a wide range of software. In cases where the default repositories do not cover your requirements or if you need the latest versions, additional repositories can be configured by following the software’s documentation.

To list available repositories, use:

```bash theme={null}
yum repolist
```

This command displays all repositories available on your system, such as the base and extras repositories, along with any additional repositories like MongoDB or MySQL.

You can also list the configuration files that define these repositories:

```bash theme={null}
ls /etc/yum.repos.d/
```

An example output might be:

```plaintext theme={null}
CentOS-Base.repo           mysql-community.repo
CentOS-CR.repo             mysql-community-source.repo
CentOS-Debuginfo.repo      CentOS-Vault.repo
CentOS-fasttrack.repo      mongodb-org-4.2.repo
```

Opening any of these files will show a URL pointing to the repository location, where you can view the RPM files available for download.

## Upgrading to Newer Versions

Sometimes, default repositories may offer older package versions. For example, CentOS might provide Ansible version 2.4 by default, even though a later version like 2.9 is available. To install the latest version, refer to the Ansible documentation and configure an updated repository.

You can add an updated repository using commands such as:

```bash theme={null}
yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
```

## Managing Packages with Yum

Yum offers several commands to manage installed and available packages:

* **Listing installed or available packages:**\
  For instance, to check for Ansible:

  ```bash theme={null}
  yum list ansible
  ```

  The output might appear as follows:

  ```plaintext theme={null}
  Installed Packages
  ansible.noarch    2.9.6-1.el7      @epel
  ```

* **Removing an installed package:**

  ```bash theme={null}
  yum remove ansible
  ```

* **Listing all available package versions:**\
  Use the `--showduplicates` option to list all available versions.

  ```bash theme={null}
  yum --showduplicates list ansible
  ```

  This might return:

  ```plaintext theme={null}
  Available Packages
  ansible.noarch           2.4.2.0-2.el7
  ansible.noarch           2.9.6-1.el7
  ```

  This output indicates that different versions of Ansible are available, possibly from the extras and EPEL repositories. To install a specific version, include the version number in the install command:

  ```bash theme={null}
  yum install ansible-2.4.2.0
  ```

## Summary

Linux package managers, such as RPM and yum, streamline software installation and dependency management. Understanding how to leverage these tools is essential for efficiently managing packages in DevOps and Cloud environments.

> **lightbulb** Experiment with these commands in a controlled environment to deepen your understanding of Linux package management.

- [Watch Video](https://learn.kodekloud.com/user/courses/devops-pre-requisite-course/module/c990b480-a646-4321-89b4-a6fbc217f4e2/lesson/8e5d2994-425a-440d-9145-f742fa42f6b8)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/devops-pre-requisite-course/module/c990b480-a646-4321-89b4-a6fbc217f4e2/lesson/01522b99-c2dd-44b3-867c-b7fc66bf8a9f)
