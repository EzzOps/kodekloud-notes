# Demo KodeKloud e commerce application

Source: https://notes.kodekloud.com/docs/Shell-Scripts-for-Beginners/Project-E-Commerce-Application/Demo-KodeKloud-e-commerce-application/page

This guide explains how to deploy the KodeKloud ECommerce Application on a CentOS machine, covering prerequisites, database configuration, and web server setup.

In this guide, we will walk you through deploying the KodeKloud ECommerce Application on a CentOS machine. The application code is hosted on GitHub in the "learning-app-ecommerce" repository at KodeKloud Hub. The repository contains all the required files plus a README that explains how to deploy prerequisites, configure the database, and set up the web server.

Below is a detailed, step‑by‑step walkthrough.

***

## 1. Deploying Prerequisites

### a. Installing and Configuring Firewalld

Begin by installing the firewalld package, starting the service, and enabling it to automatically run on system reboot:

```bash theme={null}
sudo yum install firewalld
sudo service firewalld start
sudo systemctl enable firewalld
```

Verify that firewalld is running by checking its status:

```bash theme={null}
sudo service firewalld status
```

A sample output might appear as follows:

```plaintext theme={null}
[root@eb29eab4d499 ~]# service firewalld status
Redirecting to /bin/systemctl status firewalld.service
● firewalld.service - firewalld - dynamic firewall daemon
   Loaded: loaded (/usr/lib/systemd/system/firewalld.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2019-10-11 10:53:21 UTC; 19s ago
     Docs: man:firewalld(1)
 Main PID: 1540 (firewalld)
   CGroup: /system.slice/firewalld.service
           └─1540 /usr/bin/python2 -Es /usr/sbin/firewalld --nofork --nopid

Oct 11 10:53:21 eb29eab4d499 systemd[1]: Starting firewalld - dynamic firewall....
Oct 11 10:53:21 eb29eab4d499 systemd[1]: Started firewalld - dynamic firewall.
Hint: Some lines were ellipsized, use -l to show in full.
[root@eb29eab4d499 ~]#
[root@eb29eab4d499 ~]# clear
```

### b. Installing and Configuring MariaDB

Install the MariaDB server and, if necessary, modify its configuration file. Then start and enable the MariaDB service:

```bash theme={null}
sudo yum install mariadb-server
sudo vi /etc/my.cnf
sudo service mariadb start
sudo systemctl enable mariadb
```

Next, update the firewall to allow connections on port 3306 (MySQL's default port):

```bash theme={null}
sudo firewall-cmd --permanent --zone=public --add-port=3306/tcp
sudo firewall-cmd --reload
```

To verify that MariaDB is running correctly, check its status:

```bash theme={null}
sudo service mariadb status
```

Sample output:

```plaintext theme={null}
[root@eb29eab4d499 ~]# sudo service mariadb status
Redirecting to /bin/systemctl status mariadb.service
● mariadb.service - MariaDB database server
   Loaded: loaded (/usr/lib/systemd/system/mariadb.service; enabled; vendor preset: disabled)
   Active: active (running) since Fri 2019-10-11 10:55:08 UTC; 13s ago
 Main PID: 1842 (mysqld_safe)
   CGroup: /system.slice/mariadb.service
           └─1842 /bin/sh /usr/bin/mysqld_safe --basedir=/usr
             └─2004 /usr/libexec/mysqld --basedir=/usr --datadir=/var/lib/mysql --...
```

The MariaDB configuration file (`/etc/my.cnf`) may have settings similar to:

```ini theme={null}
[mysqld]
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
