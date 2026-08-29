# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0
# Settings user and group are ignored when systemd is used.
# If you need to run mysqld under a different user or group,
# customize your systemd unit file for mariadb according to the
[mysqld_safe]
log-error=/var/log/mariadb/mariadb.log
pid-file=/var/run/mariadb/mariadb.pid
#
# include all files from the config directory
#
!includedir /etc/my.cnf.d
```

Start and enable MariaDB:

```bash theme={null}
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

A sample session to verify these steps:

```bash theme={null}
[root@eb29eab44d99 ~]# vi /etc/my.cnf
[root@eb29eab44d99 ~]# sudo systemctl start mariadb
Redirecting to /bin/systemctl start mariadb.service
[root@eb29eab44d99 ~]# sudo systemctl enable mariadb
Created symlink from /etc/systemd/system/multi-user.target.wants/mariadb.service
    to /usr/lib/systemd/system/mariadb.service.
```

### Adding the Firewall Rule for MariaDB

Open port 3306 (the default MySQL port) by executing:

```bash theme={null}
sudo firewall-cmd --permanent --zone=public --add-port=3306/tcp
sudo firewall-cmd --reload
```

Confirm that the new rule is active:

```bash theme={null}
sudo firewall-cmd --list-all
```

### Configuring the Database

Access the MariaDB monitor to create the database, add a new user, and grant the necessary privileges.

:::note Database Setup
In this example, we create a database named **ecomdb** and a user **ecomuser** with the password **ecompassword**.
:::

1. **Create the Database:**

   ```sql theme={null}
   MariaDB [(none)]> CREATE DATABASE ecomdb;
   Query OK, 1 row affected (0.00 sec)
   ```

2. **Verify the Database:**

   If a typo occurs, such as `show database;`, correct it using:

   ```sql theme={null}
   MariaDB [(none)]> SHOW DATABASES;
   +--------------------+
   | Database           |
   +--------------------+
   | information_schema |
   | ecomdb             |
   | mysql              |
   | performance_schema |
   | test               |
   +--------------------+
   5 rows in set (0.00 sec)
   ```

3. **Create a Database User and Grant Privileges:**

   ```sql theme={null}
   MariaDB [(none)]> CREATE USER 'ecomuser'@'localhost' IDENTIFIED BY 'ecompassword';
   Query OK, 0 rows affected (0.00 sec)

   MariaDB [(none)]> GRANT ALL PRIVILEGES ON *.* TO 'ecomuser'@'localhost';
   Query OK, 0 rows affected (0.00 sec)

   MariaDB [(none)]> FLUSH PRIVILEGES;
   ```

### Loading Inventory Data

The GitHub repository includes a SQL script (`DB-load-script.sql` in the assets directory) that creates a **products** table with sample data.

1. **Create the SQL Script File:**

   Run the command below to create the file and paste the content:

   ```bash theme={null}
   cat > db-load-script.sql
   ```

2. **Sample Contents of db-load-script.sql:**

   ```sql theme={null}
   USE ecomdb;
   CREATE TABLE products (
     id mediumint(8) unsigned NOT NULL auto_increment,
     Name varchar(255) DEFAULT NULL,
     Price varchar(255) DEFAULT NULL,
     ImageUrl varchar(255) DEFAULT NULL,
     PRIMARY KEY (id) AUTO_INCREMENT=1
   );

   INSERT INTO products (Name, Price, ImageUrl) VALUES
     ("Laptop", "100", "c-1.png"),
     ("Drone", "20", "c-2.png"),
     ("VR", "300", "c-3.png"),
     ("Tablet", "50", "c-5.png"),
     ("Watch", "90", "c-6.png"),
     ("Phone Covers", "20", "c-7.png"),
     ("Phone", "80", "c-8.png"),
     ("Laptop", "150", "c-4.png");
   ```

3. **Load the Data:**

   Execute the script with:

   ```bash theme={null}
   mysql < db-load-script.sql
   ```

4. **Verification:**

   Log in to the MariaDB monitor and switch to the **ecomdb** database to confirm the data was loaded:

   ```bash theme={null}
   mysql
   Welcome to the MariaDB monitor.  Commands end with ; or \g.
   Your MariaDB connection id is 4
   Server version: 5.5.64-MariaDB MariaDB Server

   MariaDB [(none)]> USE ecomdb;
   Database changed
   MariaDB [ecomdb]> SELECT * FROM products;
   +----+---------------+-------+----------+
   | id | Name          | Price | ImageUrl |
   +----+---------------+-------+----------+
   |  1 | Laptop        | 100   | c-1.png  |
   |  2 | Drone         | 20    | c-2.png  |
   |  3 | VR            | 300   | c-3.png  |
   |  4 | Tablet        | 50    | c-5.png  |
   |  5 | Watch         | 90    | c-6.png  |
   |  6 | Phone Covers  | 20    | c-7.png  |
   |  7 | Phone         | 80    | c-8.png  |
   |  8 | Laptop        | 150   | c-4.png  |
   +----+---------------+-------+----------+
   8 rows in set (0.00 sec)
   ```

At this point, the database is configured and pre-populated with sample data.

***

## 3. Deploying and Configuring the Web Application

### Installing HTTPD, PHP, and MySQL Extensions

Install the required web server packages along with PHP and its MySQL extension:

```bash theme={null}
sudo yum install -y httpd php php-mysql
```

Add the firewall rule for HTTP (port 80) and reload firewalld:

```bash theme={null}
sudo firewall-cmd --permanent --zone=public --add-port=80/tcp
sudo firewall-cmd --reload
```

### Configuring HTTPD

To configure Apache, open the configuration file and modify the DirectoryIndex if needed. For example, change the default file to **index.php** by editing the file:

```bash theme={null}
sudo vi /etc/httpd/conf/httpd.conf
```

Locate and adjust the DirectoryIndex section from:

```apacheconf theme={null}
<IfModule dir_module>
    DirectoryIndex index.html
</IfModule>
```

to:

```apacheconf theme={null}
<IfModule dir_module>
    DirectoryIndex index.php
</IfModule>
```

After saving the changes, restart HTTPD:

```bash theme={null}
sudo systemctl start httpd
sudo systemctl enable httpd
sudo systemctl restart httpd
```

### Downloading the Application Code

Ensure Git is installed, then clone the ecommerce repository into the web server’s document root:

```bash theme={null}
sudo yum install -y git
git clone https://github.com/kodekloudhub/learning-app-ecommerce.git /var/www/html/
```

Verify the files were cloned successfully:

```bash theme={null}
ls /var/www/html/
# Expected output: assets  css  fonts  img  index.php  js  README.md  scss  vendors
```

### Updating Database Connection Settings

By default, the application’s **index.php** file is configured to connect to an IP address (e.g., 172.20.1.101). Since this is an all-in-one setup, update the database connection details to use **localhost**. Open **index.php** and locate the `mysqli_connect` call.

Change the connection parameters from:

```php theme={null}
$link = mysqli_connect('172.20.1.101', 'ecommerce', 'password', 'ecommerce');
```

to:

```php theme={null}
$link = mysqli_connect('localhost', 'ecomuser', 'ecompassword', 'ecomdb');
```

Save the file and refresh your web page. You can also test the server response with:

```bash theme={null}
curl http://localhost
```

If the connection is correctly configured, you will see a list of products fetched from the database.

### Troubleshooting Default Page Issues

If an **index.html** file exists alongside **index.php**, Apache might serve **index.html** by default. Ensure that the DirectoryIndex configuration in `/etc/httpd/conf/httpd.conf` prioritizes **index.php**. If necessary, remove or rename the default **index.html**. For example, to create a temporary index file:

```bash theme={null}
cat > index.html
Hello there! This is a sample index file.
^C
```

After adjusting the DirectoryIndex value, restart HTTPD:

```bash theme={null}
sudo systemctl restart httpd
```

Now, accessing your site should display the ecommerce application (i.e., **index.php**) rather than the sample **index.html**.

***

## Conclusion

Following these steps, you have successfully deployed the KodeKloud ecommerce application manually on a CentOS machine. The process included:

• Installing and configuring **firewalld** and **MariaDB**\
• Setting up the database by creating the database, adding a user, and loading sample data\
• Installing and configuring **HTTPD**, PHP, and cloning the application code\
• Updating the database connection settings in **index.php**

This demonstration highlights how all components work together in a manual deployment scenario. Enjoy exploring the KodeKloud ecommerce application and refer to the [KodeKloud GitHub repository](https://github.com/kodekloudhub/learning-app-ecommerce) for further information and updates.

- [Watch Video](https://learn.kodekloud.com/user/courses/ansible-advanced-course/module/c47e8f27-3b16-4603-966c-b440295e5b75/lesson/e393d63d-8bdb-4732-845c-4450529dfad6)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/ansible-advanced-course/module/c47e8f27-3b16-4603-966c-b440295e5b75/lesson/97c6cfcd-3fc3-492d-b672-b62831a1d331)


# Project Introduction

Source: https://notes.kodekloud.com/docs/Ansible-Advanced-Course/Ansible-Modules/Project-Introduction/page

This article introduces a project to develop Ansible playbooks for deploying a fictional ecommerce website using a LAMP stack architecture.

In this article, we introduce the project that you will work on throughout this course. You will develop Ansible playbooks to deploy the KodeKloud ecommerce website—a fictional online store selling electronic devices. This project is divided into stages, starting with setting up a lab environment and creating simple playbooks, and then progressing to advanced best practices using includes and roles.

The KodeKloud ecommerce website uses a LAMP stack architecture:

* **Linux** as the operating system
* **Apache HTTP Server** for web services
* **MariaDB** as the database (a community fork of MySQL)
* **PHP** for server-side scripting

> **lightbulb** The focus of this project is on automating the deployment process with Ansible, rather than making changes to the application code itself.

Before you automate the deployment, it is important to be familiar with the manual configuration steps for setting up each component. This lesson reviews these essential tasks so you understand how each piece fits into the overall process.

The tasks include:

1. Choosing the deployment system (we use a CentOS Linux machine).
2. Installing and configuring the Apache HTTP server, then enabling and starting the service.
3. Installing and configuring the MariaDB database, then enabling and starting the service.
4. Installing and configuring PHP.
5. Downloading and setting up the application code such that it correctly connects to Apache and PHP.
6. Configuring the system further by setting up the firewall and creating the necessary rules.

For better logical flow, the guide begins by setting up and configuring the database before moving on to Apache and PHP.

***

## Step 1: Setting Up the Firewall

First, install firewalld on your CentOS system. Run the following commands to install, start, and enable the firewall service:

```bash theme={null}
sudo yum install firewalld
sudo service firewalld start
sudo systemctl enable firewalld
```

***

## Step 2: Configuring the MariaDB Database

Begin by installing the MariaDB server. Next, update the `/etc/my.cnf` file to change port settings if needed (remember that although the file is named `my.cnf`, it is also used by MariaDB). Then, start and enable the MariaDB service.

```bash theme={null}
sudo yum install mariadb-server
sudo vi /etc/my.cnf  # Adjust port settings as required
sudo service mariadb start
sudo systemctl enable mariadb
```

After starting the database service, add the necessary firewall rules to allow external access on port 3306:

```bash theme={null}
sudo firewall-cmd --permanent --zone=public --add-port=3306/tcp
sudo firewall-cmd --reload
```

Next, access the database with the MySQL client to create the database, user, and assign privileges. Use the following SQL commands:

```sql theme={null}
MariaDB > CREATE DATABASE ecomdb;
MariaDB > CREATE USER 'ecomuser'@'localhost' IDENTIFIED BY 'ecompassword';
MariaDB > GRANT ALL PRIVILEGES ON *.* TO 'ecomuser'@'localhost';
MariaDB > FLUSH PRIVILEGES;
```

Finally, load the inventory data for the products with the provided database load script.

> **lightbulb** Make sure the database credentials and port settings in your configuration match those specified in your Ansible playbooks.

***

## Step 3: Configuring the Web Server

This step involves installing Apache, PHP, and PHP-MySQL to enable database connectivity. Then, update the firewall rules to allow HTTP traffic and modify Apache’s configuration to use `index.php` as the default file.

Install the necessary packages:

```bash theme={null}
sudo yum install -y httpd php php-mysql
```

Configure the firewall for HTTP traffic:

```bash theme={null}
sudo firewall-cmd --permanent --zone=public --add-port=80/tcp
sudo firewall-cmd --reload
```

Edit the Apache configuration file to prioritize `index.php`:

```bash theme={null}
sudo vi /etc/httpd/conf/httpd.conf  # Set DirectoryIndex to use index.php instead of index.html
```

After saving the changes, start and enable the Apache service:

```bash theme={null}
sudo service httpd start
sudo systemctl enable httpd
```

***

## Step 4: Deploying the Application Code

Clone the repository containing the KodeKloud ecommerce application code. If Git isn't installed, install it first:

```bash theme={null}
sudo yum install -y git
git clone https://github.com/<application>.git /var/www/html/
```

Before testing, update the `index.php` file with the correct database details (address, name, user ID, and password). Finally, verify the deployment with a simple test:

```bash theme={null}
curl http://localhost
```

This setup demonstrates how to deploy the LAMP stack on a single node where the database, Apache, and PHP all reside on the same system.

In a multi-node configuration, the components are distributed on separate systems. Although the steps remain similar, connectivity details must be adjusted:

* Update `index.php` on the web server with the database server's IP address.
* In the database server, specify the web server's IP address when configuring user access. This ensures that only the authorized web server can connect.

For example, on the database server, use the following configuration:

```sql theme={null}
MariaDB > CREATE DATABASE ecomdb;
MariaDB > CREATE USER 'ecomuser'@'172.20.1.102' IDENTIFIED BY 'ecompassword';
MariaDB > GRANT ALL PRIVILEGES ON *.* TO 'ecomuser'@'172.20.1.102';
MariaDB > FLUSH PRIVILEGES;
```

And, update the PHP connection code on the web server accordingly:

```php theme={null}
$link = mysqli_connect('172.20.1.101', 'ecomuser', 'ecompassword');
if ($link) {
    $res = mysqli_query($link, "SELECT * FROM products;");
    while ($row = mysqli_fetch_assoc($res)) {
        // Process each row
    }
}
```

> **triangle-alert** Always ensure that your database user permissions and firewall settings are secured in both single and multi-node setups to prevent unauthorized access.

***

## Step 5: Reviewing the PHP Connection in the Application

The primary file to focus on within the application is `index.php`, which contains the database connection details. The critical line in the file is:

```php theme={null}
$link = mysqli_connect('172.20.1.101', 'ecomuser', 'ecompassword', 'ecomdb');
```

This line specifies the IP address of the database server, the database name, the user ID, and the password. You will modify this connection string as needed throughout the project.

***

## Demo and Next Steps

After reviewing this demo:

* Set up your project environment.
* Create Ansible playbooks to automate the deployment.
* Practice deploying the KodeKloud ecommerce application following the steps provided.

For further reading on Kubernetes concepts and container orchestration (if relevant to your deployment automation), visit the [Kubernetes Documentation](https://kubernetes.io/docs/).

Happy automating!

- [Watch Video](https://learn.kodekloud.com/user/courses/ansible-advanced-course/module/c47e8f27-3b16-4603-966c-b440295e5b75/lesson/d4153d2d-a162-4aa3-9590-1ebaa5ff4fab)
