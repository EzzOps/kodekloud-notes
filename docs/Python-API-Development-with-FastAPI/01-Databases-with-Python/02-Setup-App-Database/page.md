# Establish a connection to the PostgreSQL database
conn = psycopg2.connect("dbname=test user=postgres")
cur = conn.cursor()

# Create a table, insert data, and fetch it
cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))
cur.execute("SELECT * FROM test;")
print(cur.fetchall())

# Commit the transaction and close connections
conn.commit()
cur.close()
conn.close()
```

The workflow illustrated above includes:

1. Importing the psycopg2 library.
2. Establishing a connection using specific connection parameters.
3. Creating a cursor for executing SQL commands.
4. Executing SQL commands such as creating a table, inserting data, and selecting data.
5. Committing the transaction and closing the connection.

## Integrating with FastAPI

When developing an API with a framework like FastAPI, managing database connections effectively becomes essential. The snippet below illustrates how to integrate psycopg2 with FastAPI while leveraging Pydantic models for data validation:

```python theme={null}
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Body
from pydantic import BaseModel
from random import randrange
import psycopg2

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# Dummy data for posts
my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1}, 
    {"title": "favorite foods", "content": "I like pizza", "id": 2}
]
```

## Setting Up a Robust Database Connection

Proper error handling is critical when connecting to the database. In this section, we configure the connection to return query results as dictionaries using the `RealDictCursor`. This makes it easier to work with query results. Additionally, the code demonstrates the use of a try/except block to capture and handle connection errors:

```python theme={null}
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

try:
    # Connect to the 'fastapi' database on localhost with given user credentials
    conn = psycopg2.connect(
        host='localhost',
        database='fastapi',
        user='postgres',
        password='password123',
        cursor_factory=RealDictCursor
    )
    cursor = conn.cursor()
    print("Database connection was successful!")
except Exception as error:
    print("Connecting to database failed")
    print("Error:", error)

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite foods", "content": "I like pizza", "id": 2}
]
```

> **lightbulb** For enhanced readability and maintainability, consider using environment variables to store sensitive database credentials instead of hard-coding them.

## Handling Connection Failures with a Retry Mechanism

Database connection attempts may fail temporarily—for example, if the database service has not fully started. In these cases, implementing a retry mechanism can be especially useful. The code below demonstrates a looping construct that continuously attempts to connect until successful, with a 2-second delay between each attempt.

```python theme={null}
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# Continuously attempt to connect to the database until successful
while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password='password123',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successful!")
        break  # Exit loop on successful connection
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)  # Wait 2 seconds before retrying

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite foods", "content": "I like pizza", "id": 2}
]
```

> **lightbulb** Implementing a retry mechanism not only ensures your application waits for a stable connection but also provides resilience against transient network or service issues.

## Important Note on Hard-Coded Credentials

Hard-coding database credentials (such as host, database name, user, and password) is considered a security risk. This approach:

* Exposes sensitive information if committed to version control.
* Makes it challenging to switch between development and production environments where credentials differ.

For production-level applications, use environment variables or a configuration manager to handle sensitive information securely. This practice enhances both security and flexibility.

***

With a robust database connection and proper error handling in place, you can now extend your application by executing more SQL commands and building API endpoints that interact seamlessly with your PostgreSQL database.

- [Watch Video](https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/1c3ad280-5fee-4b8e-a891-42a61f9a2dd0/lesson/77bf956d-7bb1-4492-b535-2274e8a998af)


# Setup App Database

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Databases-with-Python/Setup-App-Database/page

This guide integrates a PostgreSQL database with a Python/FastAPI application, focusing on setting up a "posts" table for a social media application.

In this guide, we integrate our PostgreSQL database with a Python/FastAPI application. Previously, we built a strong foundation in PostgreSQL by querying, inserting, updating, and deleting rows. Now, let's combine these skills and set up a new table for our social media application.

Before diving into the application code, perform a quick cleanup. In earlier demonstrations, we worked with a "products" table. If this table is no longer needed, you can remove it by right-clicking the table in your database management tool and selecting "Delete" or "Drop." Otherwise, you may leave it intact—it won’t affect the FastAPI database integration.

> **lightbulb** Ensure you are working with the designated FastAPI database. If you have multiple databases on your machine, ignore any unrelated entries and focus solely on your FastAPI-specific instance.

## Schema Design for the Posts Table

For our social media application, we will create a new table called "posts." The table will have the following columns:

1. **ID Column**
   * Type: `SERIAL` (auto-incrementing integer primary key)

2. **Title Column**
   * Type: `VARCHAR` (or character varying)
   * Constraint: `NOT NULL` (each post must have a title)

3. **Content Column**
   * Type: `VARCHAR`
   * Constraint: `NOT NULL`

4. **Published Column**
   * Type: `BOOLEAN`
   * Constraint: `NOT NULL`
   * Default Value: `TRUE` (defaults to true if not provided)

5. **Created\_at Column**
   * Type: `TIMESTAMP WITH TIME ZONE`
   * Constraint: `NOT NULL`
   * Default Value: the current timestamp at the time of insertion

Once you have configured these columns in your database management tool, name the table "posts" and save your changes. Afterward, you can right-click on the table and select "View/Edit Data" to confirm that the table is empty and ready to store your posts.

## FastAPI Application Code

Below is a snippet of our FastAPI application that defines a post schema using Pydantic and includes some sample posts:

```python theme={null}
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite foods", "content": "I like pizza", "id": 2}
]
```

Below is a sample of the application log showcasing the server startup and a successful GET request to the posts endpoint:

```console theme={null}
INFO:     Started server process [26448]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:53763 - "GET /posts HTTP/1.1" 200 OK
```

## Creating the Posts Table

With the schema in mind, create the "posts" table in your FastAPI database using your preferred SQL tool or user interface. For initial testing, you can insert data directly. For example, to verify the contents of the posts table, run:

```sql theme={null}
SELECT * FROM public.posts
ORDER BY "id" ASC;
```

After inserting data, you should see two entries in your database, confirming that the table is ready for further development.

> **lightbulb** You can use your SQL management tool to insert sample data into the posts table, ensuring that the correct structure and constraints are applied.

## Revisiting Previous SQL Operations

Earlier, we demonstrated basic SQL operations. For reference, here is a corrected SQL command that updated records in the products table (used previously for demonstration purposes):

```sql theme={null}
UPDATE products SET is_sale = true WHERE id > 15 RETURNING *;
```

Now that our focus is on the posts table for our social media application, we can continue to develop and integrate this table into our FastAPI application.

The database is now set up and ready to be used by your application. Moving forward, you can build upon this integration to create robust CRUD operations for your FastAPI-powered social media application.

For more information on PostgreSQL and FastAPI integration, consider exploring additional resources such as [FastAPI Documentation](https://fastapi.tiangolo.com/) and the [PostgreSQL Official Documentation](https://www.postgresql.org/docs/).

- [Watch Video](https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/1c3ad280-5fee-4b8e-a891-42a61f9a2dd0/lesson/b5f0588b-0aff-4a64-a7d6-8049bfcf98bd)
