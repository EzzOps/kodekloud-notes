# This group is read both by the client and the server
[client-server]
# include all files from the config directory
!includedir /etc/my.cnf.d
```

<Callout icon="lightbulb">
  If you need to change settings like the MySQL port or adjust other configurations, update this file as required. For this demo, default settings are maintained.
</Callout>

### Adding a Firewall Rule for MariaDB

Since MariaDB uses the default MySQL port (3306), add this port to firewalld permanently and then reload the service:

```bash theme={null}
sudo firewall-cmd --permanent --zone=public --add-port=3306/tcp
sudo firewall-cmd --reload
```

To confirm that the rule has been added, list the current firewall settings:

```bash theme={null}
sudo firewall-cmd --list-all
```

### Configuring the Database

Follow these steps to configure MariaDB for the e-commerce application:

1. Create the database.
2. Create a new user with appropriate privileges.
3. Load sample inventory data.

Log in to the MariaDB console:

```bash theme={null}
sudo mysql
```

Create the database and verify its creation:

```sql theme={null}
CREATE DATABASE ecomdb;
SHOW DATABASES;
```

You should see “ecomdb” listed alongside default databases like information\_schema, mysql, and performance\_schema.

Now, create a new user and grant it privileges:

```sql theme={null}
CREATE USER 'ecomuser'@'localhost' IDENTIFIED BY 'ecompassword';
GRANT ALL PRIVILEGES ON *.* TO 'ecomuser'@'localhost';
FLUSH PRIVILEGES;
```

### Loading Inventory Data

To populate the `ecomdb` database with sample data, create a SQL script (for example, named `db-load-script.sql`). You can either copy the script from the GitHub repository's assets or create it manually:

```bash theme={null}
cat > db-load-script.sql <<-EOF
USE ecomdb;
CREATE TABLE products (
    id mediumint(8) unsigned NOT NULL auto_increment,
    Name varchar(255) DEFAULT NULL,
    Price varchar(255) DEFAULT NULL,
    ImageUrl varchar(255) DEFAULT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT=1;

INSERT INTO products (Name, Price, ImageUrl) 
VALUES ("Laptop","100","c-1.png"),("Drone","200","c-2.png"),("VR","300","c-3.png"),("Tablet","50","c-5.png"),("Watch","90","c-6.png"),("Phone Covers","20","c-7.png"),("Phone","80","c-8.png");
EOF
```

Load the SQL script into MySQL with:

```bash theme={null}
mysql < db-load-script.sql
```

Verify that the inventory data has been imported by executing the following commands in the MariaDB console:

```sql theme={null}
USE ecomdb;
SELECT * FROM products;
```

***

## 3. Deploying and Configuring the Web Application

Now that your database is set up and configured, let's deploy the web application using Apache, PHP, and the required MySQL driver.

### Installing Required Packages

First, install Apache (httpd), PHP, and the PHP MySQL driver. Then add a firewall rule for HTTP (port 80):

```bash theme={null}
sudo yum install -y httpd php php-mysqlnd
sudo firewall-cmd --permanent --zone=public --add-port=80/tcp
sudo firewall-cmd --reload
```

### Configuring Apache

Modify Apache’s configuration to prioritize `index.php` over `index.html`. Use the following command to update the configuration:

```bash theme={null}
sudo sed -i 's/index.html/index.php/g' /etc/httpd/conf/httpd.conf
```

Start and enable the Apache service:

```bash theme={null}
sudo systemctl start httpd
sudo systemctl enable httpd
```

Verify that Apache is running:

```bash theme={null}
sudo systemctl status httpd
```

### Downloading the Application Code

Ensure Git is installed on your machine:

```bash theme={null}
yum install -y git
```

Clone the repository into the Apache document root:

```bash theme={null}
git clone https://github.com/kodekloudhub/learning-app-ecommerce.git /var/www/html
```

Since the sample code might have a hard-coded IP address for the MySQL database connection, update the `index.php` file to use `localhost`:

```bash theme={null}
sudo sed -i 's/172.20.1.101/localhost/g' /var/www/html/index.php
```

To verify the web application, open your browser and navigate to [http://localhost:80](http://localhost:80) or use curl:

```bash theme={null}
curl http://localhost
```

You should see the e-commerce application’s web page displaying the inventory data retrieved from the database.

### Verifying the Application’s Database Connection

Review the `index.php` file to ensure the MySQL credentials and host settings are correct. The relevant PHP section should resemble:

```php theme={null}
<?php
$link = mysqli_connect('localhost', 'ecomuser', 'ecompassword', 'ecomdb');

if ($link) {
    $res = mysqli_query($link, "SELECT * FROM products;");
    while ($row = mysqli_fetch_assoc($res)) { 
        ?>
        <div class="col-md-3 col-sm-6 business_content">
            <?php echo '<img src="'.$row["ImageUrl"] . '" alt="">' ?>
            <div class="media">
            </div>
            <div class="media-body">
                <a href="#"><?php echo $row['Name'] ?> at the lowest price <span><?php echo $row['Price'] ?></span></a>
            </div>
        </div>
        <?php 
    }
}
?>
```

After saving any changes, refresh your browser to see the updated product listing.

<Callout icon="lightbulb">
  By following these steps, you have successfully deployed and configured the KodeKloud e-commerce application on a CentOS machine. Both the database and web server are now running and properly connected.
</Callout>

Enjoy your fully functional e-commerce demo!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-pre-requisite-course/module/2608518c-d8a5-4ee7-8089-e53c93b30abc/lesson/df1329d7-5a2c-4085-ae66-a288160622d3" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/devops-pre-requisite-course/module/2608518c-d8a5-4ee7-8089-e53c93b30abc/lesson/11138573-95c5-456d-83ea-3877277c801a" />
</CardGroup>


# KodeKloud E Commerce Application

Source: https://notes.kodekloud.com/docs/DevOps-Pre-Requisite-Course/2-Tier-Applications/KodeKloud-E-Commerce-Application/page

This tutorial explains deploying the KodeKloud e-commerce website using a LAMP stack with detailed setup instructions and configurations.

This tutorial explains how to deploy the KodeKloud e-commerce website, a fictional online store for electronic devices, using a LAMP stack (Linux, Apache, MariaDB, PHP). For this lab, we use MariaDB—a community alternative to MySQL—with identical procedures whether you choose MariaDB or MySQL.

<Frame>
  ![The image shows a product list webpage featuring items like laptops, drones, VR devices, and phones, with prices and images for each product.](https://kodekloud.com/kk-media/image/upload/v1752873403/notes-assets/images/DevOps-Pre-Requisite-Course-KodeKloud-E-Commerce-Application/frame_10.jpg)
</Frame>

The sections below detail setting up the lab environment, installing required components, and configuring the system properly.

***

## Environment Setup and Task Overview

We start by preparing a CentOS machine to deploy the application. The overall procedure includes:

1. Installing and configuring the firewall.
2. Setting up the MariaDB database.
3. Installing and configuring the Apache HTTP Server and PHP.
4. Downloading and configuring the application code.
5. Verifying the deployment using tools like curl.

For an efficient process, start with the database configuration followed by the web server and PHP setup.

***

## Step 1: Firewall Configuration

Begin by installing and starting the firewalld service on your CentOS machine:

```bash theme={null}
sudo yum install firewalld
sudo service firewalld start
sudo systemctl enable firewalld
```

***

## Step 2: MariaDB Database Setup

Install the MariaDB server, adjust the configuration, and configure firewall rules for SQL access. Although the configuration file (/etc/my.cnf) is similar to that of MySQL, you can use the MySQL client to interact with MariaDB.

```bash theme={null}
sudo yum install mariadb-server
sudo vi /etc/my.cnf  # Configure the file with the correct port settings if needed
sudo service mariadb start
sudo systemctl enable mariadb

sudo firewall-cmd --permanent --zone=public --add-port=3306/tcp
sudo firewall-cmd --reload
```

After starting MariaDB, use the MySQL command-line interface to create the database, user, and load the inventory data:

```sql theme={null}
mysql
MariaDB > CREATE DATABASE ecomdb;
MariaDB > CREATE USER 'ecomuser'@'localhost' IDENTIFIED BY 'ecompassword';
MariaDB > GRANT ALL PRIVILEGES ON *.* TO 'ecomuser'@'localhost';
MariaDB > FLUSH PRIVILEGES;

mysql < db-load-script.sql
```

<Callout icon="lightbulb">
  Be sure to adjust port settings or other configuration parameters in `/etc/my.cnf` as needed for your environment.
</Callout>

***

## Step 3: Apache and PHP Setup

Install Apache, PHP, and Git. Then, configure Apache to serve PHP by prioritizing `index.php` over `index.html` and open port 80 for external traffic:

```bash theme={null}
sudo yum install -y httpd php php-mysql
sudo firewall-cmd --permanent --zone=public --add-port=80/tcp
sudo firewall-cmd --reload
sudo vi /etc/httpd/conf/httpd.conf  # Modify DirectoryIndex to prioritize index.php
sudo service httpd start
sudo systemctl enable httpd

sudo yum install -y git
git clone https://github.com/<application>.git /var/www/html/
