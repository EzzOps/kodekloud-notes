# Sqlalchemy Setup

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Databases-with-Python/Sqlalchemy-Setup/page

Integrating SQLAlchemy into a FastAPI project for database connection, model creation, and session utilization.

In this article, we will integrate SQLAlchemy into a FastAPI project. You will learn how to establish a database connection, create models, and utilize sessions for database operations.

Below is an overview of the SQLAlchemy documentation with pointers to the sections relevant to our setup.

![The image shows a webpage from the FastAPI documentation, specifically focusing on SQL (Relational) Databases and how to use them with SQLAlchemy. It includes a list of supported databases and a table of contents on the right.](https://kodekloud.com/kk-media/image/upload/v1752883391/notes-assets/images/Python-API-Development-with-FastAPI-Sqlalchemy-Setup/fastapi-sqlalchemy-database-docs.jpg)

Begin by visiting the SQL page.

![The image shows the SQLAlchemy 1.4 documentation webpage, featuring sections on getting started, tutorials, and reference documentation for SQLAlchemy ORM and Core.](https://kodekloud.com/kk-media/image/upload/v1752883392/notes-assets/images/Python-API-Development-with-FastAPI-Sqlalchemy-Setup/sqlalchemy-1-4-documentation-webpage.jpg)

Search for "SQL" to navigate to the main page, and under "Library" select "References" for version 1.4 (the version used in this course). Although version 2.0 may be released in the future, please install version 1.4 if you are following this article.

For additional details, click the link below:

![The image shows a webpage from the SQLAlchemy documentation, featuring navigation menus and information about the Python SQL toolkit.](https://kodekloud.com/kk-media/image/upload/v1752883393/notes-assets/images/Python-API-Development-with-FastAPI-Sqlalchemy-Setup/sqlalchemy-documentation-webpage.jpg)

A comprehensive tutorial and reference documentation on setting up the ORM (including session usage) are available. The FastAPI documentation offers further guidelines for configuring SQLAlchemy with SQL relational databases.

***

## Installing SQLAlchemy

First, install SQLAlchemy using pip:

```bash theme={null}
pip install sqlalchemy
```

You might see output similar to the following:

```bash theme={null}
Downloading greenlet-1.1.1-cp39-cp39-win_amd64.whl (96 kB)
Installing collected packages: greenlet, sqlalchemy
Successfully installed greenlet-1.1.1 sqlalchemy-1.4.23
WARNING: You are using pip version 21.1.1; however, version 21.2.4 is available.
You should consider upgrading via the 'c:\users\sanje\documents\courses\fastapi\venv\scripts\python.exe -m pip install --upgrade pip' command.
```

> **lightbulb** Keep in mind that SQLAlchemy does not communicate directly with a database; it requires a database driver (for instance, `psycopg2` for PostgreSQL or an equivalent driver for MySQL, SQLite, etc.). If you're using PostgreSQL and have the driver installed, there is no need to reinstall it.

***

## Creating the Database Connection File

Create a file named `database.py` in your project. This file manages the database connection while setting up the SQLAlchemy engine, session, and base model. Below is a sample configuration. Note that for SQLite, you must include the `connect_args` parameter; for PostgreSQL or other databases, it is not necessary.

```python theme={null}
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
