# For SQLite (commented out PostgreSQL):
# SQLALCHEMY_DATABASE_URL = "sqlite:///sql_app.db"
# For PostgreSQL:
# Format: postgresql://<username>:<password>@<ip-address>/<database_name>
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password123@localhost/fastapi"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Only required for SQLite.
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Ensure you update the connection string appropriately, and avoid hardcoding sensitive credentials in production code.

***

## Defining Models

In an ORM, database tables are represented as Python classes. Create a file named `models.py` to store your models. Each model corresponds to a table in your database. Below is an example model for a posts table demonstrating four columns: `id`, `title`, `content`, and `published`.

```python theme={null}
from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
```

This model generates the corresponding table in PostgreSQL automatically as the application starts.

***

## Initializing the Database in the Main Application

Within your main FastAPI application file (commonly `main.py`), import your models and create the database tables. Additionally, set up a dependency to manage database sessions for API endpoints.

Below is an example implementation:

```python theme={null}
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .database import engine, get_db

# Automatically create tables on application startup.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db_user := crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
```

The above snippet uses `models.Base.metadata.create_all(bind=engine)` to create the necessary database tables if they do not exist. The `get_db` function is a dependency that ensures every request gets its own session and that the session is properly closed afterward.

***

## Testing the Database Connection

To verify that your database is properly connected, add a simple endpoint that queries the posts table. This example demonstrates the usage of the SQLAlchemy session dependency:

```python theme={null}
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    # Implement your query logic here using SQLAlchemy session methods.
    return {"status": "success"}
```

If you prefer using a raw SQL query (assuming your driver supports the necessary configurations), ensure that you modify the code to obtain a cursor from your database connection.

***

## Creating and Managing the Posts Table

Each time the application starts, SQLAlchemy checks for the existence of the `posts` table in the database. If the table is missing, it will be automatically created based on the definition in `models.py`. You can inspect the table structure using tools like PgAdmin.

<Frame>
  ![The image shows a pgAdmin interface displaying the structure of a PostgreSQL database table named "posts," with columns such as "id," "title," "content," "published," and "created\_at." The data types and constraints for each column are also visible.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883395/notes-assets/images/Python-API-Development-with-FastAPI-Sqlalchemy-Setup/pgadmin-postgresql-posts-table-structure.jpg)
</Frame>

This automated table management ensures consistency between your Python models and the actual database schema.

***

## Cleaning Up the Main Application

To keep your main application file concise, consider migrating the database dependency function (`get_db`) to the `database.py` file. You can then import `get_db` in your `main.py` as shown below:

```python theme={null}
from .database import engine, get_db
```

This organization maintains a clean separation of concerns by keeping your database configuration centralized.

***

## Final Remarks

Your FastAPI application is now configured with SQLAlchemy for managing database connections via a session dependency. The posts table is automatically created based on the model in `models.py`, and you can further develop endpoints to execute more complex queries and operations.

<Callout icon="lightbulb">
  With this setup, you now have a robust foundation for database operations in your FastAPI project. In future articles, we will explore adding additional columns (like timestamps) and handling more advanced database interactions.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/1c3ad280-5fee-4b8e-a891-42a61f9a2dd0/lesson/3b6e099c-5e15-43f3-944b-0df6aa5f215c" />
</CardGroup>


# Sqlalchemy Update Posts

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Databases-with-Python/Sqlalchemy-Update-Posts/page

This guide demonstrates updating posts using SQLAlchemy in a FastAPI application, covering querying, validation, updating, and returning results.

In this guide, we will demonstrate how to update posts using SQLAlchemy in a FastAPI application. The update operation follows a familiar pattern similar to deleting or retrieving a post by its ID. We will cover how to query the database, validate that the post exists, perform the update, and return the updated result.

***

## 1. Original PostgreSQL-based Update (for reference)

Initially, a raw PostgreSQL update query might have been used:

```python theme={null}
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s
    RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    return {"data": updated_post}
```

```plaintext theme={null}
INFO:     Application startup complete.
INFO:     127.0.0.1:53042 - "DELETE /posts/6 HTTP/1.1" 204 No Content
INFO:     127.0.0.1:60950 - "DELETE /posts/444 HTTP/1.1" 404 Not Found
```

***

## 2. Deleting a Post with SQLAlchemy

Before diving into the update, it is useful to review the deletion process using SQLAlchemy. This example ensures that database dependency configurations are set up correctly:

```python theme={null}
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()
```

```plaintext theme={null}
INFO:     127.0.0.1:53042 - "DELETE /posts/6 HTTP/1.1" 204 No Content
INFO:     127.0.0.1:60950 - "DELETE /posts/444 HTTP/1.1" 404 Not Found
```

***

## 3. Update Operation Using SQLAlchemy

The update process with SQLAlchemy follows these steps:

* Query the database for the post with the given ID.
* Validate if the post exists.
* Update the post using the values provided in the request.
* Commit the changes and return the updated post.

<Callout icon="lightbulb">
  Be sure to handle naming collisions between the input schema and the SQLAlchemy model instance. In our example, we use the name `existing_post` for the fetched instance.
</Callout>

### Step 3.1: Preparing the Query and Validating the Post

```python theme={null}
@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # Query the database for the post matching the id
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()
    
    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
```

### Step 3.2: Updating the Post

You can either use hardcoded updated values or dynamically update with the incoming Pydantic model. Typically in production, you would use the provided data:

```python theme={null}
    # Update the post using the data from the request body
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
```

### Step 3.3: Returning the Updated Post

After committing the update, re-query the database for the latest data to return:

```python theme={null}
    updated_post = post_query.first()
    return {"data": updated_post}
```

***

## 4. Complete Updated Endpoint

Below is the final consolidated code for the update endpoint:

```python theme={null}
@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # Query for the existing post by ID
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()
    
    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    
    # Update the post using the dictionary from the Pydantic model
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    # Retrieve and return the updated post
    updated_post = post_query.first()
    return {"data": updated_post}
```

***

## 5. Testing the Update

To test the endpoint, send an update request with JSON data. For instance, using the following JSON payload:

```json theme={null}
{
    "title": "updated title",
    "content": "This is the new content"
}
```

The server logs might then reflect:

```plaintext theme={null}
INFO:  Application startup complete.
INFO:  127.0.0.1:60884 - "PUT /posts/1 HTTP/1.1" 200 OK
```

You can verify that the post has been updated in your database by running a query such as:

```sql theme={null}
select * from posts;
```

***

## 6. Important Considerations

* Ensure that the dependency `db: Session = Depends(get_db)` is correctly configured in your application.
* Avoid naming conflicts between the input schema (`post`) and the SQLAlchemy model instance by using a distinct variable name (e.g., `existing_post`).
* Utilize the `post.dict()` method to convert the Pydantic model to a dictionary before applying the update with SQLAlchemy.
* The `synchronize_session=False` flag is applied for performance optimization during updates.

Happy coding!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/1c3ad280-5fee-4b8e-a891-42a61f9a2dd0/lesson/d40e0421-b3aa-455d-bf51-834692d08d10" />
</CardGroup>
