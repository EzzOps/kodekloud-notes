# Project Demo

Source: https://notes.kodekloud.com/docs/Ansible-Advanced-Course/Ansible-Modules/Project-Demo/page

This article demonstrates manual deployment of the KodeKloud ecommerce application on a CentOS machine without automation tools.

In this article, we demonstrate how to deploy the KodeKloud ecommerce application manually on a CentOS machine—without using automation tools like Ansible. You can use any available CentOS machine or quickly access a CentOS playground online.

The application's source code is hosted on GitHub in the **learning-app-ecommerce** repository maintained by the KodeKloud organization. The repository includes all necessary deployment files along with a detailed README file divided into three sections:

• Deploying prerequisites\
• Deploying and configuring the database\
• Deploying and configuring the web server

Follow the steps below sequentially to complete the manual deployment.

***

## 1. Deploying Prerequisites

### Installing and Configuring firewalld

Begin by installing firewalld, then start and enable the service to run on system boot:

```bash theme={null}
sudo yum install -y firewalld
sudo systemctl start firewalld
sudo systemctl enable firewalld
```

If you need to troubleshoot, verify the service status with:

```bash theme={null}
sudo systemctl status firewalld
```

When adding firewall rules later in the process, you can list all active rules with:

```bash theme={null}
sudo firewall-cmd --list-all
```

A sample troubleshooting session might resemble:

```bash theme={null}
[root@eb29eab4499 ~]# sudo systemctl start firewalld
Redirecting to /bin/systemctl start firewalld.service
[root@eb29eab4499 ~]# sudo systemctl enable firewalld
Created symlink from /etc/systemd/system/dbus-org.fedoraproject.FirewallD1.service
    to /usr/lib/systemd/system/firewalld.service.
Created symlink from /etc/systemd/system/multi-user.target.wants/firewalld.service
    to /usr/lib/systemd/system/firewalld.service.
```

***

## 2. Deploying and Configuring the Database

### Installing MariaDB Server

Install the MariaDB server package using the following command:

```bash theme={null}
sudo yum install -y mariadb-server
```

After installation, you can review or modify default settings in the configuration file `/etc/my.cnf`. Below is an example configuration; unless you need to change the default port or other settings, the provided configuration remains suitable:

```ini theme={null}
[mysqld]
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
