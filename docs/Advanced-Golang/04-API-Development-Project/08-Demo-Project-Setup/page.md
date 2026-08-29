# Demo Project Setup

Source: https://notes.kodekloud.com/docs/Advanced-Golang/API-Development-Project/Demo-Project-Setup/page

This article guides the creation of a Golang application that connects to a MySQL database, covering setup, data insertion, and HTTP routing.

In this lesson, we'll create a simple project that connects to a MySQL database using [Golang](https://learn.kodekloud.com/user/courses/golang). You will learn how to create a database, set up a table, insert sample data, and build a [Golang](https://learn.kodekloud.com/user/courses/golang) application that connects to the database and registers HTTP routes.

─────────────────────────────

## Step 1: Initial Golang File Overview

Begin by creating a basic Golang file. The snippet below includes the necessary imports and a placeholder function for error checking:

```go theme={null}
package main

import (
    "database/sql"
    "fmt"
    _ "github.com/go-sql-driver/mysql"
    "log"
)

func checkError(e error) {
    // Implement error handling as needed
}
```

```plaintext theme={null}
Desktop/kodekloud/learn via 🐹 v1.19.3
```

─────────────────────────────

## Step 2: Database Setup in MySQL

First, create a database named **Inventory**. Follow these steps:

1. Log in to MySQL:

   ```bash theme={null}
   mysql -u root -p
   ```

2. In the MySQL shell, create the database:

   ```sql theme={null}
   create database inventory;
   -- Query OK, 1 row affected (0.01 sec)
   ```

3. Switch to the new database and create a table named **Products** with the following columns:

   * **id**: An integer, not null and auto-incremented.
   * **name**: A non-null varchar field.
   * **quantity**: An integer.
   * **price**: A float with precision.

   Execute the following SQL commands:

   ```sql theme={null}
   mysql> use inventory;
   Database changed

   mysql> create table products(
       ->   id int NOT NULL AUTO_INCREMENT,
       ->   name varchar(255) NOT NULL,
       ->   quantity int,
       ->   price float(10,7),
       ->   PRIMARY KEY(id)
       -> );
   Query OK, 0 rows affected, 1 warning (0.01 sec)

   mysql> insert into products values(1, "chair", 100, 200.00);
   Query OK, 1 row affected (0.00 sec)

   mysql> insert into products values(2, "desk", 800, 600.00);
   Query OK, 1 row affected (0.00 sec)

   mysql> select * from products;
   +----+-------+----------+---------------+
   | id | name  | quantity | price         |
   +----+-------+----------+---------------+
   |  1 | chair |      100 | 200.0000000   |
   |  2 | desk  |      800 | 600.0000000   |
   +----+-------+----------+---------------+
   2 rows in set (0.00 sec)
   ```

─────────────────────────────

## Step 3: Project Directory and Module Initialization

Set up your workspace by creating a new project directory called **my-inventory**. Then, initialize a new Go module and create the main application file.

```bash theme={null}
cd ..
~/Desktop/kodekloud
mkdir my-inventory
cd my-inventory
```

Initialize the module and create the app file:

```bash theme={null}
go mod init example.com/my-inventory
