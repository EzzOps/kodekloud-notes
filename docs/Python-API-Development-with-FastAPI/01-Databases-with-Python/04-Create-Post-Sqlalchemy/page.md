# Create Post Sqlalchemy

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Databases-with-Python/Create-Post-Sqlalchemy/page

Learn to create a new post using SQLAlchemy with FastAPI, transitioning from raw SQL to a more maintainable ORM approach.

In this article, you will learn how to create a new post using SQLAlchemy—the powerful Python ORM that abstracts raw SQL commands into clean, maintainable code. This guide demonstrates how to migrate from raw SQL queries to a more standardized approach using FastAPI and SQLAlchemy.

## Initial Implementation with Raw SQL

Below is an initial implementation that uses raw SQL commands to create a new post:

```python theme={null}
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING 
                      (post.title, post.content, post.published))""")
    new_post = cursor.fetchone()
    
    conn.commit()
    
    return {"data": new_post}
```

During execution, you might observe errors and system logs similar to the following:

```text theme={null}
TypeError: 'title' is an invalid keyword argument for str()
WARNING: WatchGodReload detected file change in '[...].tmp'. Reloading...
Database connection was successful!
INFO:     Started server process [29432]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Transitioning to SQLAlchemy ORM

SQLAlchemy provides an abstraction layer that eliminates the need to write direct SQL queries. Instead, you can leverage ORM models to handle database operations smoothly. When working with FastAPI, it is important to include the database dependency in your path operations, which simplifies unit testing and centralizes database management through dependency injection.

Below is an updated example using FastAPI's `Depends` to pass the database session:

```python theme={null}
from fastapi import Depends
from sqlalchemy.orm import Session

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # The following raw SQL commands have been commented out:
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)
    # RETURNING """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    conn.commit()
    
    return {"data": new_post}
```

You might notice similar log messages when running this code:

```text theme={null}
TypeError: 'title' is an invalid keyword argument for str()
WARNING: WatchGodReload detected file change in 'C:\...\main.py'
Database connection was successful!
INFO:     Started server process [29432]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Defining the ORM Model

For the ORM approach, define models that represent your database tables. The example below shows how the `Post` model is structured:

```python theme={null}
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
```

When working with FastAPI, import and initialize your models as follows:

```python theme={null}
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)
```

After importing, you can access the model using `models.Post`.

## Creating a New Post Using SQLAlchemy

To create a new post, populate the SQLAlchemy model with attributes (title, content, published) provided by the request object. The following updated endpoint demonstrates how to create a new post using ORM:

```python theme={null}
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # The raw SQL command is commented out as we now use the ORM:
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    conn.commit()
    new_post = models.Post(
        title=post.title, content=post.content, published=post.published
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}
```

Once the post is saved, sending a request with the following JSON payload:

```json theme={null}
{
    "title": "welcome to funland",
    "content": "so much fun"
}
```

may result in a response like:

```json theme={null}
{
  "title": "welcome to funland",
  "content": "so much fun"
}
```

And your server logs might display messages similar to:

```text theme={null}
Application startup complete.
127.0.0.1:53845 - "POST /posts HTTP/1.1" 201 Created
```

However, if you query your PostgreSQL database with:

```sql theme={null}
select * from posts;
```

and do not see the newly created post, it indicates that changes were not properly committed. With SQLAlchemy, remember to add the new post to the session, commit the transaction, and refresh the instance to retrieve auto-generated fields such as `id` and `created_at`.

The corrected handler is shown below:

```python theme={null}
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(
        title=post.title, content=post.content, published=post.published
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}
```

## Simplifying with Dictionary Unpacking

Manually mapping each attribute from the Pydantic model to the SQLAlchemy model can be tedious as the number of fields increases. Since `post` is an instance of a Pydantic model, you can convert it to a dictionary using `post.dict()`. By leveraging Python's dictionary unpacking, you can simplify the creation of the ORM model instance:

```python theme={null}
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # Print the converted dictionary for debugging purposes.
    print(post.dict())
    
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}
```

Using `**post.dict()` automatically unpacks the dictionary into keyword arguments that match the fields defined in your `Post` model. This method is scalable and easier to maintain when additional fields are introduced.

> **lightbulb** Check that your model is defined accurately. The fields in your Pydantic model should directly correspond to the fields in your SQLAlchemy model for seamless data mapping.

## Final Endpoint Implementation

After consolidating the improvements, your cleaner and final endpoint implementation is as follows:

```python theme={null}
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}
```

This approach eliminates the need for manual attribute mapping, ensures that all changes are correctly committed to PostgreSQL, and makes your codebase more scalable and maintainable.

> **triangle-alert** Remember to always commit your database session after adding new entries. Missing a commit could result in data not being persisted in the database.

- [Watch Video](https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/1c3ad280-5fee-4b8e-a891-42a61f9a2dd0/lesson/91918418-00a1-42c0-b429-b57e69f3f6b1)
