# deploy_ECommerce_Application.sh
# This script deploys the ECommerce Application by installing and configuring
########################################
# Function: print_color
# Description: Print a message in a specified color.
# Usage: print_color "green" "Your message here"
########################################
function print_color(){
  NC='\033[0m'  # No Color
  case $1 in
    "green") COLOR='\033[0;32m' ;;
    "red")   COLOR='\033[0;31m' ;;
    *)       COLOR='\033[0m' ;;
  esac
  echo -e "${COLOR}$2${NC}"
}

########################################
# Function: check_service_status
# Description: Check if a service is active.
# Usage: check_service_status firewalld
########################################
function check_service_status(){
  service_name=$1
  is_active=$(systemctl is-active "$service_name")
  if [ "$is_active" = "active" ]; then
    print_color "green" "$service_name Service is active"
  else
    print_color "red" "$service_name Service is not active"
    exit 1
  fi
}

########################################
# Function: check_firewalld_port
# Description: Verify that a given port is configured in the public zone firewall.
# Usage: check_firewalld_port "3306"
########################################
function check_firewalld_port(){
  port=$1
  firewall_ports=$(sudo firewall-cmd --list-all --zone=public | grep ports)
  if [[ $firewall_ports == *"$port"* ]]; then
    print_color "green" "Port $port is configured in the firewall"
  else
    print_color "red" "Port $port is not configured in the firewall"
    exit 1
  fi
}

########################################
# Function: check_item
# Description: Check if a specific item appears in the web page content.
# Usage: check_item "$web_page_content" "Laptop"
########################################
function check_item(){
  web_page_content="$1"
  item="$2"
  if [[ "$web_page_content" == *"$item"* ]]; then
    print_color "green" "Item '$item' is present on the web page"
  else
    print_color "red" "Item '$item' is not present on the web page"
  fi
}

#############################
# Database and Service Setup
#############################

# Install and configure Firewalld
print_color "green" "Installing and starting firewalld..."
sudo yum install -y firewalld
sudo service firewalld start
sudo systemctl enable firewalld
check_service_status firewalld

# Install and configure MariaDB
print_color "green" "Installing and starting MariaDB..."
sudo yum install -y mariadb-server
sudo service mariadb start
sudo systemctl enable mariadb
check_service_status mariadb

# Configure firewall for MariaDB (port 3306)
print_color "green" "Adding firewall rule for MariaDB (port 3306)..."
sudo firewall-cmd --permanent --zone=public --add-port=3306/tcp
sudo firewall-cmd --reload
check_firewalld_port "3306"

# Configure the Database
print_color "green" "Configuring the database..."
cat > configure-db.sql <<EOF
CREATE DATABASE ecomdb;
CREATE USER 'ecomuser'@'localhost' IDENTIFIED BY 'ecompassword';
GRANT ALL PRIVILEGES ON *.* TO 'ecomuser'@'localhost';
FLUSH PRIVILEGES;
EOF
sudo mysql < configure-db.sql

# Load inventory data into the database
print_color "green" "Loading inventory data into the database..."
cat > db-load-script.sql <<EOF
USE ecomdb;
CREATE TABLE products (
  id mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  Name varchar(255) DEFAULT NULL,
  Price decimal(10,2) DEFAULT NULL,
  ImageUrl varchar(255) DEFAULT NULL,
  PRIMARY KEY (id)
);
INSERT INTO products (Name,Price,ImageUrl) VALUES 
  ("Laptop", "100", "c-1.png"),
  ("Drone", "200", "c-2.png"),
  ("VR", "300", "c-3.png"),
  ("Tablet", "5", "c-5.png"),
  ("Watch", "90", "c-6.png"),
  ("Phone", "80", "c-8.png"),
  ("Laptop", "150", "c-4.png");
EOF
sudo mysql < db-load-script.sql

#############################
# Web Server Configuration
#############################

print_color "green" "Installing Apache, PHP, and configuring the web server..."
sudo yum install -y httpd php php-mysql
sudo firewall-cmd --permanent --zone=public --add-port=80/tcp
sudo firewall-cmd --reload
sudo sed -i 's/index.html/index.php/g' /etc/httpd/conf/httpd.conf

sudo service httpd start
sudo systemctl enable httpd
check_service_status httpd

print_color "green" "Cloning application repository..."
sudo yum install -y git
sudo git clone https://github.com/kodekloudhub/learning-app-ecommerce.git /var/www/html/
sudo sed -i 's/172.20.1.101/localhost/g' /var/www/html/index.php

#############################
# Testing the Deployment
#############################

print_color "green" "Testing the web application..."
web_page=$(curl http://localhost)
for item in "Laptop" "Drone" "VR" "Watch" "Phone"
do
  check_item "$web_page" "$item"
done

print_color "green" "Deployment complete. The ECommerce Application is up and running."
```

### Explanation

1. **Functions for User-Friendly Output:**\
   The functions `print_color`, `check_service_status`, and `check_firewalld_port` offer colored output and validate that necessary services and firewall rules are active.

2. **Database Setup:**\
   SQL scripts (`configure-db.sql` and `db-load-script.sql`) configure the database and load inventory data. Executing these with `sudo mysql` ensures proper permission handling.

3. **Web Server Setup:**\
   Apache is installed and configured to use `index.php` via `sed`, and the application repository is cloned into `/var/www/html`. The script updates the IP address in `index.php` with `localhost`, standardizing the environment.

4. **Final Testing:**\
   The script uses `curl` to fetch the web content and verifies the presence of key items such as "Laptop", "Drone", etc.

***

## 6. Final Testing and Teardown

After executing the script, verify the deployment by visiting [http://localhost](http://localhost) in your browser to confirm that all products are listed. For further improvements, consider adding robust error checking and a teardown script to stop services, clean up changes, or restore your test VM to a clean snapshot.

Happy deploying!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/shell-scripts-for-beginners/module/0e75480e-85f7-470c-9aa4-fac3fef0ede7/lesson/d099f0fa-e998-45c4-9ba4-431cf012e932" />
</CardGroup>


# Exit Codes

Source: https://notes.kodekloud.com/docs/Shell-Scripts-for-Beginners/Shebang/Exit-Codes/page

This article explores exit codes in shell scripts, indicating command success or failure on Linux systems.

In this article, we explore the concept of exit codes in shell scripts and how they indicate whether a command executed successfully or encountered an error on Linux systems.

When you run a command, it either executes successfully or fails. For instance, listing the contents of the current directory with the command below executes successfully and returns an exit status of zero:

```bash theme={null}
$ ls
/home/root/tmp
```

Conversely, if you run a command that does not exist, an error is displayed and a non-zero exit code is returned:

```bash theme={null}
$ lss
Failed: command not found
```

When a command runs successfully, it returns an exit status of 0; when it fails, it returns a non-zero value. These exit codes are not shown in the command output but are stored in the built-in variable "\$?".

To view the exit code immediately after executing a command, use:

```bash theme={null}
$ ls
/home/root/tmp

$ echo $?
0

$ lss
Failed: command not found

$ echo $?
127
```

<Callout icon="lightbulb">
  It is considered best practice to use exit codes in your scripts to communicate the overall status to the caller or user.
</Callout>

Consider a scenario where you are launching a rocket mission. For a successful launch, the script should return an exit status of 0, and for any failure, it should explicitly return a non-zero value (commonly 1).

Below is a sample script that starts a rocket launch mission. In this naive version, even if the launch fails, the script returns an exit code of 0 because it only prints a failure message without setting a non-zero index:

```bash theme={null}
mkdir $mission_name
rocket-add $mission_name
rocket-start-power $mission_name
rocket-internal-power $mission_name
rocket-start-sequence $mission_name
rocket-start-engine $mission_name
rocket-lift-off $mission_name
rocket_status=$(rocket-status $mission_name)
while [ "$rocket_status" == "launching" ]
do
  sleep 2
  rocket_status=$(rocket-status $mission_name)
done
if [ "$rocket_status" = "failed" ]
then
  rocket-debug $mission_name
fi
```

If you run the script, the output might be:

```bash theme={null}
$ create-and-launch-rocket
failed
```

However, checking the exit code reveals that it remains 0:

```bash theme={null}
$ echo $?
0
```

To address this issue, update the script so that it returns a non-zero exit code (typically 1) when the launch fails. Here is the improved version of the script:

```bash theme={null}
mkdir $mission_name
rocket-add $mission_name
rocket-start-power $mission_name
rocket-internal-power $mission_name
rocket-start-sequence $mission_name
rocket-start-engine $mission_name
rocket-lift-off $mission_name
rocket_status=$(rocket-status $mission_name)
while [ "$rocket_status" == "launching" ]
do
    sleep 2
    rocket_status=$(rocket-status $mission_name)
done
if [ "$rocket_status" = "failed" ]
then
    rocket-debug $mission_name
    exit 1
fi
```

Now, if the rocket launch fails, the script will correctly exit with a status code of 1. This can be verified as follows:

```bash theme={null}
$ create-and-launch-rocket
failed
```

```bash theme={null}
$ echo $?
1
```

<Callout icon="lightbulb">
  Always ensure that your scripts return an appropriate exit code. Explicitly returning a non-zero code for failure conditions facilitates better integration with other systems and scripts.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/shell-scripts-for-beginners/module/2e5d4133-6bc2-421e-bc8f-0389e7f96490/lesson/6270f719-a1bc-4ab8-91d8-71786a2c60e8" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/shell-scripts-for-beginners/module/2e5d4133-6bc2-421e-bc8f-0389e7f96490/lesson/9cf43b24-3924-4d85-84db-519fa5eca391" />
</CardGroup>
