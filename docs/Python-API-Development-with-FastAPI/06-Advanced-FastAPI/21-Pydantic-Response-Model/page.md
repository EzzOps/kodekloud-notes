# Pydantic Response Model

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Advanced-FastAPI/Pydantic-Response-Model/page

This article explains how to define Pydantic schema models for shaping API responses in FastAPI, enhancing clarity and security by controlling exposed fields.

In this article, we explain how to define Pydantic schema models to shape API responses effectively when using FastAPI. Learn how to modify responses to include only the fields needed by the client, thereby excluding sensitive or unnecessary data like passwords or internal IDs. FastAPI’s seamless integration with SQLAlchemy and Pydantic helps you tailor responses for better clarity and security.

Below is our initial code for handling GET and POST requests for "posts" using SQLAlchemy. Notice the commented-out raw SQL queries alongside the ORM-based approach:

```python theme={null}
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)
    # RETURNING """ % (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
```

Console output indicates that the application started successfully:

```plaintext theme={null}
app\main.py']' Reloading...
Database connection was successful!
INFO:     Started server process [9144]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Currently, our endpoints return a dictionary with the key "data" wrapping the posts or a list of posts. However, this extra nesting might be unnecessary. To simplify responses, we can remove the "data" key and return the post or list of posts directly. For example:

```python theme={null}
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)
    #                 RETURNING * """,
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
```

The updated console output now resembles:

```plaintext theme={null}
[INFO]  Started server process [9144]
[INFO]  Waiting for application startup.
[INFO]  Application startup complete.
```

> **lightbulb** If you need to filter out sensitive attributes (e.g., a user's password) before sending data to the client, consider modifying your endpoint responses to return only the required fields.

## Defining the Response Schema with Pydantic

Next, we define the response schema using Pydantic models. Initially, Pydantic models define the schema for creating posts (data input from the user):

```python theme={null}
from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass
```

When FastAPI returns a response, you might want to include only selected fields (e.g., title, content, published) and optionally additional fields such as an ID or a creation timestamp that exists in your database. We create a new model for responses as shown below:

```python theme={null}
from pydantic import BaseModel
from datetime import datetime

class Post(BaseModel):
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True
```

Enabling ORM mode tells Pydantic to read attributes from an ORM object (such as a SQLAlchemy model) by treating them as a dictionary. This prevents errors like:

```plaintext theme={null}
pydantic.error_wrappers.ValidationError: 1 validation error for Post
response
  value is not a valid dict (type=type_error.dict)
```

### Using the Response Schema in the Create Endpoint

Once a post is created, the updated endpoint uses the response model:

```python theme={null}
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    #    """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)
    #       RETURNING * """, (post.title, post.content, post.published)
    # )
    # new_post = cursor.fetchone()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
```

A sample JSON response after creating a post:

```json theme={null}
{
  "title": "welcome to funlandasdfjasdlfkjasdf",
  "content": "so much fun",
  "published": true
}
```

Even though PostgreSQL stores additional fields like the ID and creation timestamp, you can control which fields are sent to the client by updating the Pydantic model. For example, to include the ID and creation timestamp in the response:

```python theme={null}
from pydantic import BaseModel
from datetime import datetime

class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    class Config:
        orm_mode = True
```

The API response will now include all defined fields:

```json theme={null}
{
    "id": 23,
    "title": "welcome to funlandsdfjasd1fkjasdf",
    "content": "so much fun",
    "published": true,
    "created_at": "2021-08-22T17:07:55.119164-04:00"
}
```

> **lightbulb** If certain fields (such as `created_at`) should not be exposed, remove them from the response schema.

### Leveraging Inheritance to Reduce Redundancy

You can streamline your code by leveraging inheritance. Since the fields for title, content, and published are already defined in PostBase, extend it in your response model to add only the new fields:

```python theme={null}
from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
```

## Updating Other Endpoints with the Response Model

### Root and Posts Endpoints

Here’s how you can update the endpoints to remove unnecessary nesting and to adopt the response model approach:

```python theme={null}
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)""")
    return post
```

Console logs confirm that GET and POST operations function as expected:

```plaintext theme={null}
INFO: Started server process [9144]
INFO: Waiting for application startup.
INFO: Application startup complete.
INFO: 127.0.0.1:5672 - "GET /posts HTTP/1.1" 200 OK
INFO: 127.0.0.1:5689 - "POST /posts HTTP/1.1" 201 Created
```

### Retrieving and Updating a Single Post

To retrieve a single post, ensure you specify the response model in your endpoint:

```python theme={null}
@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return post
```

Similarly, update the endpoint for modifying a post:

```python theme={null}
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    #    """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #    (updated_post.title, updated_post.content, updated_post.published, str(id))
    # )
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
```

### Handling a List of Posts

When returning a list of posts, update the response model to handle lists effectively by importing List from the typing module:

```python theme={null}
from typing import List

@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts
```

Console output confirms that the GET request returns a list of posts:

```plaintext theme={null}
INFO: 127.0.0.1:61645 - "GET /posts HTTP/1.1" 200 OK
```

## Summary

By explicitly defining your response schema using Pydantic models and enabling ORM mode, you achieve:

* Better control over the fields exposed in API responses.
* Reduced redundancy via inheritance and clearer API design.
* Improved performance and security by returning only necessary data.

Implementing these practices in your FastAPI projects ensures cleaner, more maintainable code and enhances the overall developer and client experience.

- [Watch Video](https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/ed782f8c-495c-4ff8-8703-c9ab0ab04a4d/lesson/8f4f74a8-3020-4e94-b1d2-8f0376a10618)
