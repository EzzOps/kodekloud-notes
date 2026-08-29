# Demo KodeKloud E Commerce Application

Source: https://notes.kodekloud.com/docs/DevOps-Pre-Requisite-Course/2-Tier-Applications/Demo-KodeKloud-E-Commerce-Application/page

This guide explains how to deploy the KodeKloud e-commerce application on a CentOS machine, covering prerequisites, database setup, and web application deployment.

In this guide, you'll learn how to deploy the KodeKloud e-commerce application on a CentOS machine. The application code is hosted on GitHub under the repository “learning-app-ecommerce” at the KodeKloud hub. The repository includes all the necessary files along with a detailed README for further instructions.

Below is a step-by-step guide covering prerequisites installation, database and firewall configuration, and finally, the deployment of the web application.

***

## 1. Deploying Prerequisites

First, install and configure the firewall (firewalld) so that it automatically starts on system boot. This ensures that your system rules are applied correctly, aiding in troubleshooting any future issues.

### Install and Start Firewalld

Execute the following commands to install firewalld, start the service, enable it to run on reboot, and confirm its status:

```bash theme={null}
sudo yum install -y firewalld
sudo systemctl start firewalld
sudo systemctl enable firewalld
sudo systemctl status firewalld
```

To verify the current firewall rules, run:

```bash theme={null}
sudo firewall-cmd --list-all
```

> **lightbulb** Ensure that all expected firewall rules are active, confirming firewalld is running as intended.

***

## 2. Installing and Configuring the Database

The application uses MariaDB as its database server. The steps below demonstrate how to install, configure, and secure MariaDB.

### Installing MariaDB

Install MariaDB using the package manager and review the configuration file:

```bash theme={null}
sudo yum install -y mariadb-server
sudo vi /etc/my.cnf
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

The default configuration file (`/etc/my.cnf`) appears as follows:

```ini theme={null}
