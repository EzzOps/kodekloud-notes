# Demo Vagrant

Source: https://notes.kodekloud.com/docs/DevOps-Pre-Requisite-Course/Lab-Setup/Demo-Vagrant/page

This guide teaches how to deploy a virtual machine using Vagrant, covering installation, configuration, resource management, and troubleshooting.

In this guide, you will learn how to deploy a virtual machine (VM) using Vagrant. We will cover installing Vagrant, initializing and configuring a Vagrant box (using CentOS 7 as an example), managing resources, and troubleshooting common boot timeout issues.

## Prerequisites

Before you begin, ensure that you have the following:

* Vagrant installed on your system. Download it from [Vagrantup.com](https://www.vagrantup.com) by selecting the appropriate version for your operating system.
* A virtual machine provider installed, such as VirtualBox, VMware Workstation, or Fusion. If you are using a provider other than VirtualBox, remember to specify it using the `--provider` option when running the `vagrant up` command.

> **lightbulb** Make sure the Vagrant command is available on your system after installation.

## Setting Up Your Project Directory

Start by opening your terminal and creating a directory for your Vagrant configurations. Navigate to your desired folder. For example:

```bash theme={null}
host> ls
Applications
Desktop
Documents
Downloads
Google Drive
Google Drive File Stream
Library
Movies

host> cd Documents
host> ls
```

## Finding and Initializing a Vagrant Box

Vagrant boxes are available on [Vagrant Cloud](https://app.vagrantup.com/boxes/search). By browsing through the available options, you can choose a box that fits your needs. In this example, we will use the CentOS 7 box.

To initialize a Vagrantfile with the CentOS 7 box, run:

```bash theme={null}
vagrant init centos/7
```

This command creates a Vagrantfile with a basic configuration where the active line is:

```ruby theme={null}
config.vm.box = "centos/7"
```

The generated Vagrantfile provides additional configuration examples as commented lines, such as settings for box update checking and port forwarding. Below is an excerpt from the file:

```ruby theme={null}
