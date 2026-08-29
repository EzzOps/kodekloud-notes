# Use a separate test database by appending '_test' to the database name.
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

Then, define the testing dependency:

```python theme={null}
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Finally, override the dependency in your FastAPI app:

```python theme={null}
from app.database import get_db

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
```

> **triangle-alert** If your test database is new, you might encounter errors due to missing tables. Make sure to create all the necessary tables before running your tests.

One common strategy is to have SQLAlchemy create all tables from your models before the tests execute:

```python theme={null}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.database import engine
from app.routers import post, user, auth, vote
from app.config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

With this setup, the test database (e.g., `fastapi_test`) is automatically created and populated with the necessary tables when the tests run. You can verify the existence of tables by executing a query like:

```sql theme={null}
SELECT * FROM public.users
ORDER BY "id" ASC;
```

After running your test suite, you should see output confirming that tests passed, and you can view the new table entries in your test database via your favorite database tool (such as [PgAdmin](https://www.pgadmin.org)):

```plaintext theme={null}
tests/test_users.py::test_root Hello World PASSED
tests/test_users.py::test_create_user PASSED
=================================== 2 passed, 5 warnings in 1.00s ===================================
```

Below is the final summary snippet showing the test database setup:

```python theme={null}
from app.database import get_db, Base
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configure the test database URL by appending '_test' to the existing name.
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
```

FastAPI’s dependency override functionality allows you to easily swap out dependencies, such as the database session, during testing. This separation ensures that your tests run in an isolated environment, protecting your development data. Moreover, the test database can be hosted on your local machine, in a Docker container, or on a remote server—simply adjust your connection details accordingly.

![The image shows a webpage from the FastAPI documentation, specifically a section on testing a database. It includes a table of contents and instructions for adding tests for an SQL app.](https://kodekloud.com/kk-media/image/upload/v1752883472/notes-assets/images/Python-API-Development-with-FastAPI-Setup-Test-Database/fastapi-testing-database-docs.jpg)

Before running tests against your dedicated testing database (e.g., `fastapi_test`), make sure that the database exists. In [PgAdmin](https://www.pgadmin.org), you can create the database by executing:

```sql theme={null}
SELECT * FROM public.users
ORDER BY id ASC;
```

If you need to drop or create databases for testing purposes, tools like [PgAdmin](https://www.pgadmin.org) offer a graphical interface. For example, you might see a confirmation dialog when dropping a database:

![The image shows a pgAdmin interface with a confirmation dialog asking if the user wants to drop the database "fastapi\_test." The background displays a list of databases and a data output table.](https://kodekloud.com/kk-media/image/upload/v1752883473/notes-assets/images/Python-API-Development-with-FastAPI-Setup-Test-Database/pgadmin-drop-database-confirmation.jpg)

After setting up the test database and overriding the dependency, you can run your tests. A final example of the configuration is as follows:

```python theme={null}
# Configure test database connection.
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
```

When you run the tests:

```plaintext theme={null}
tests/test_users.py::test_root Hello World PASSED
tests/test_users.py::test_create_user PASSED
```

you can verify, using your database tool, that all necessary tables (such as the users table) have been created and populated appropriately.

This concludes our guide on setting up a separate test database in FastAPI. By leveraging dependency overrides, you can ensure that tests run in a fully isolated environment without affecting your development data.

- [Watch Video](https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/eed445e5-68aa-46b3-9922-0fdf2a57b8f1/lesson/2a793148-83cc-41c6-acaa-1196dc2c1139)


# Test Create Post

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Testing/Test-Create-Post/page

This article reviews tests for post endpoints, ensuring proper access control, post creation, and default values.

In this article, we review a comprehensive suite of tests for our post endpoints. These tests ensure that unauthorized users cannot access posts, non-existent posts return appropriate status codes, posts are successfully created via the API, and that the default published value is correctly applied when not provided.

The sections below group the tests logically to improve readability and SEO. Each section includes detailed explanations and corresponding code blocks.

***

## Unauthorized Access and Retrieve Post Tests

The tests in this section verify that:

* Unauthorized users cannot retrieve posts.
* Requests for non-existing posts return a 404 status code.
* Authorized users can successfully retrieve an existing post with matching attributes.

```python theme={null}
def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.id == test_posts[0].id
    assert post.title == test_posts[0].title
    assert post.content == test_posts[0].content
```

***

## Create Post Tests

This section tests the post creation functionality using parameterization. It verifies that:

* The correct HTTP status code (201) is returned.
* The post content matches the input.
* The owner ID of the post is correctly assigned.

```python theme={null}
import pytest

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={
        "title": title,
        "content": content,
        "published": published
    })
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']
```

***

## Default Published Value Test

> **lightbulb** In the PostBase model, the "published" field defaults to True. This test confirms that when the "published" field is omitted, the system sets it to True by default.

```python theme={null}
def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={
        "title": "arbitrary title",
        "content": "aasdfjasdf"
    })
    
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "aasdfjasdf"
    assert created_post.published is True
    assert created_post.owner_id == test_user['id']
```

***

## Unauthorized Post Creation Test

This test confirms that only authorized users can create posts. Any attempt by an unauthorized user to access the post route will result in a 401 status code.

```python theme={null}
def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401
```

***

## Pydantic Schemas for Posts and Users

The following Pydantic schemas define the structure for posts and users used in the tests. Notice that the "published" attribute in the PostBase model defaults to True.

```python theme={null}
from pydantic import BaseModel, EmailStr
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

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
```

***

## Conclusion

At this stage, all tests related to post creation have been implemented and verified, including:

* Validating unauthorized access attempts.
* Handling requests for non-existent posts.
* Confirming the correct creation of posts.
* Ensuring default values are set appropriately when omitted.

In the next article, we will explore tests for updating or deleting a post.

> **triangle-alert** Note: Additional console warnings regarding external library deprecations, such as the `@coroutine` decorator warning from aiofiles, do not affect the test outcomes.

Additional console warnings may include:

```plaintext theme={null}
=================================================================
warnings summary
=================================================================
/venv/lib/site-packages/aiofiles/os.py:10: DeprecationWarning: "@coroutine" decorator
  ...
```

This concludes our lesson on testing post creation functionality. For more details, refer to our [API Testing Documentation](#).

- [Watch Video](https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/eed445e5-68aa-46b3-9922-0fdf2a57b8f1/lesson/22be8076-4c5d-4338-b638-4ea314230005)
