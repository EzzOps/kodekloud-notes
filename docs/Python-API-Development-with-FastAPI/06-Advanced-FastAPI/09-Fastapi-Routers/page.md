# SECRET_KEY, ALGORITHM, and ACCESS_TOKEN_EXPIRE_MINUTES are hardcoded here
SECRET_KEY = "[SECRET_REDACTED]"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

Hardcoding secret keys makes it difficult to manage configurations across different environments, increasing security risks and maintenance overhead.

***

## Leveraging Environment Variables

Environment variables allow you to externalize sensitive configuration details. By setting these values at the operating system level, your application can automatically retrieve the correct configuration for the current environment.

### Accessing Environment Variables in Python

Create a simple file (e.g., `example.py`) to demonstrate accessing an environment variable:

```python theme={null}
import os

# Retrieve the PATH environment variable (note: variable names are case-sensitive on non-Windows systems)
path = os.getenv("Path")
print(path)
```

Execute the script with:

```shell theme={null}
py example.py
```

This command prints the value of the PATH variable, illustrating how environment variables can be accessed in Python.

***

## Configuring Environment Variables

### On Windows

1. Open **Advanced System Settings** and click **Environment Variables**.
2. Create a new user variable (e.g., `MY_DB_URL`) with a value like `localhost:5432`.
3. Open a new command prompt, then verify by running:

   ```shell theme={null}
   echo %MY_DB_URL%
   ```

*Note: If you update environment variables, close and reopen your terminal or VS Code to see the changes.*

### On macOS/Linux

Set an environment variable in the terminal:

```bash theme={null}
export MY_DB_URL="localhost:5432"
printenv | grep MY_DB_URL
```

Or verify using:

```bash theme={null}
echo $MY_DB_URL
```

***

## Managing Multiple Variables with .env Files

For projects with numerous environment variables, managing them manually can be tedious. A common solution during development is to use an environment file (commonly named `.env`).

### Using Pydantic BaseSettings for Validation

[Pydantic](https://pydantic-docs.helpmanual.io/) offers a robust solution for managing and validating environment variables through the `BaseSettings` class. This method ensures that all required settings are present and automatically handles type conversions.

Create a configuration file (e.g., `config.py`):

```python theme={null}
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        # Load variables from the .env file
        env_file = ".env"

settings = Settings()
```

Pydantic reads and validates the environment variables at runtime. If a required variable is missing or a conversion fails, it raises a descriptive error.

### Creating the .env File

In your project root, add a `.env` file:

```text theme={null}
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=password123
DATABASE_NAME=fastapi
DATABASE_USERNAME=postgres
SECRET_KEY[SECRET_REDACTED]
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

<Callout icon="lightbulb">
  Avoid committing your `.env` file to version control. Add `.env` to your `.gitignore` to protect your sensitive data.
</Callout>

***

## Integrating Environment Variables into Your Application

After centralizing your configuration using environment variables, update your codebase to reference these settings.

### Database Connection Setup

In `database.py`, adjust your database connection configuration to use environment variables:

```python theme={null}
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from config import settings  # Import validated settings

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:"
    f"{settings.database_password}@"
    f"{settings.database_hostname}:"
    f"{settings.database_port}/"
    f"{settings.database_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### OAuth2 Token Configuration

Similarly, update your OAuth2 settings to reference configuration variables:

```python theme={null}
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Use environment variables for sensitive settings
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

By centralizing configuration in `config.py`, your application automatically adapts to different environments without modifying the code.

***

## Summary

* **Avoid Hardcoding:** Embed sensitive information as environment variables rather than hardcoding.
* **Environment Variables:** Utilize OS-level variables to manage configurations dynamically.
* **Pydantic Validation:** Employ Pydantic’s `BaseSettings` to validate and manage environment settings.
* **.env File Usage:** During development, use a `.env` file to simplify configuration management, but exclude it from version control.
* **Dynamic Application Configuration:** Update your application to utilize environment variables, ensuring secure and flexible deployments across various environments.

By following these practices, you improve your application’s security, scalability, and maintainability while reducing the risk of exposing sensitive information.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/ed782f8c-495c-4ff8-8703-c9ab0ab04a4d/lesson/ecc2161d-d790-4ab6-8454-baae59b225e7" />
</CardGroup>


# Fastapi Routers

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Advanced-FastAPI/Fastapi-Routers/page

This article explains how to refactor a FastAPI application by organizing endpoints into separate router files for better modularity and maintainability.

In this article, we refactor our FastAPI application by separating user and post path operations (CRUD operations) into distinct files. Initially, our main.py file contains all endpoints, which can lead to clutter as the application grows.

## Current Main.py Structure

Initially, our main.py file includes endpoints such as:

```python theme={null}
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
```

During execution, you might observe logs like these:

```sql theme={null}
[SQL: INSERT INTO users (email, password) VALUES (%(email)s, %(password)s) RETURNING users.id]
[parameters: {'email': 'mark1123@email.com', 
              'password': '$2b$12$mvtoneBzuKAA0HgrBTDeRfJaf10F1W3oz'}]
(Background on this error at: https://sqlalche.me/e/14/gkpj)
WARNING: WatchGodReload detected file change in '[C:\Users\sanje\Documents\Courses\fastapi\app\main.py]'. Reloading...
Database connection was successful!
INFO:     Started server process [7824]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

In addition to posts, main.py also handles user operations, such as creating a new user or retrieving a user by ID:

```python theme={null}
@app.get('/users/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
```

Managing all endpoints in one file can become unwieldy as your application grows.

<Callout icon="lightbulb">
  Splitting your endpoints into separate files makes your code more modular and maintainable.
</Callout>

## Organizing Code with Routers

To streamline our application structure, we create a new directory named `routers` and add two files inside it: `post.py` and `user.py`. This allows us to move all post-related operations to `post.py` and user-related operations to `user.py`.

### User Router Example

In the `user.py` file, the code for handling user-related endpoints looks like this:

```python theme={null}
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password for security
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    return user
```

Later, once this code is moved from main.py, you can safely remove the user-related endpoints from it.

### Post Router Example

Likewise, in the `post.py` file, the post-related endpoints are refactored as follows:

```python theme={null}
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # Fetching posts using ORM
    posts = db.query(models.Post).all()
    return posts

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # Create a new post using ORM
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
```

Replace the usage of the FastAPI instance (`app`) with the router object (`router`) in each file. This makes the routes modular and easier to manage.

## Integrating Routers in main.py

After splitting the routes into separate files, update your main.py to include the routers from the `routers` directory:

```python theme={null}
from fastapi import FastAPI
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user
import psycopg2
from psycopg2.extras import RealDictCursor
import time

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
