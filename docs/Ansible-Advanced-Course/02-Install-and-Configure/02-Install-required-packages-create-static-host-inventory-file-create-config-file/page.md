# Install required packages create static host inventory file create config file

Source: https://notes.kodekloud.com/docs/Ansible-Advanced-Course/Install-and-Configure/Install-required-packages-create-static-host-inventory-file-create-config-file/page

Learn to install Ansible, create a static host inventory file, and configure Ansible with a custom configuration file.

In this lesson, you'll learn how to install the Ansible control machine, set up a static host inventory file, and configure Ansible using a custom configuration file. The control node hosts the core Ansible software and stores all your playbooks. Remember that Ansible must be installed on a Linux machine. Although you can run Ansible from a Linux VM on Windows, it cannot be installed directly on Windows. However, Windows machines can be managed as target nodes in your Ansible environment.

<Callout icon="lightbulb">
  Ansible can be installed using various methods. Use Linux package managers (yum, dnf, apt-get) for a quick setup, or use pip for the latest version and greater flexibility.
</Callout>

## Installing Ansible

You have two main options for installing Ansible: using your system’s package manager or the Python package manager pip.

### Using Package Managers

For systems based on different distributions, execute the following commands:

For Red Hat or CentOS:

```bash theme={null}
$ sudo yum install ansible
```

For Fedora:

```bash theme={null}
$ sudo dnf install ansible
```

For Ubuntu or Debian:

```bash theme={null}
$ sudo apt-get install ansible
```

### Using pip

If you already have Python installed, pip allows you to install or upgrade Ansible. On enterprise Linux, you may need to install the extra EPEL-release packages first:

```bash theme={null}
$ sudo yum install epel-release
$ sudo yum install python-pip
$ sudo pip install ansible
```

To upgrade Ansible:

```bash theme={null}
$ sudo pip install --upgrade ansible
```

To install a specific version, such as 2.4:

```bash theme={null}
$ sudo pip install ansible==2.4
```

## Creating an Inventory File

When Ansible is installed via a package manager, a default inventory file is created at `/etc/ansible/hosts`. If no other inventory file is specified, Ansible will use this file by default. However, you can create your own static inventory file anywhere, such as alongside your playbooks.

### Default Inventory File Example

```ini theme={null}
/etc/ansible/hosts
