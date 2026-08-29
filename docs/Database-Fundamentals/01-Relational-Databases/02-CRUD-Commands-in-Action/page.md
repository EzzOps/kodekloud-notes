# CRUD Commands in Action

Source: https://notes.kodekloud.com/docs/Database-Fundamentals/Relational-Databases/CRUD-Commands-in-Action/page

Introduction to CRUD operations and creating MySQL users and videos tables with primary and foreign keys, data types, and example SQL for creating reading updating and deleting records

Earlier we designed an Entity Relationship Diagram (ERD) for Cody's cat video club. We split her messy spreadsheet into two normalized tables—`users` and `videos`—and added primary keys, foreign keys, data types and relationships.

Now we'll convert that spreadsheet into a relational database using MySQL. In this lesson you'll learn what CRUD means, create a new database, and run basic SQL to Create, Read, Update and Delete records.

What is CRUD?

* CRUD stands for Create, Read, Update, Delete. These are the four fundamental operations any application or service performs on persistent data.
* SQL (Structured Query Language) is the standard language you use to perform CRUD operations in a relational DBMS like MySQL.

<Frame>
  <img alt="The image is about SQL (Structured Query Language), showing a database graphic with glasses and a question mark, highlighting tasks like adding data, finding data, fixing mistakes, and clearing old entries, alongside a person from KodeKloud explaining it." />
</Frame>

Getting started with MySQL

* We'll use MySQL in the KodeKloud Playground (or your local MySQL instance). The playground provides login details and an interactive MySQL shell.
* If you need help in the MySQL client, use the built-in `HELP` command or consult the official MySQL documentation.

Example: connect and run a simple SELECT in the MySQL client

```sql theme={null}
mysql> SELECT * FROM my_table;
+----+------------+-----------+-------------------------+
| id | first_name | last_name | email                   |
+----+------------+-----------+-------------------------+
|  1 | John       | Smith     | johnsmith@newemail.com  |
+----+------------+-----------+-------------------------+
1 row in set (0.00 sec)
