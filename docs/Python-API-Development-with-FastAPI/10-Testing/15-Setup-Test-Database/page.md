# SQLALCHEMY_DATABASE_URL
SQLALCHEMY_DATABASE_URL = (
    f'postgresql://{settings.database_username}:{settings.database_password}'
    f'@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
```

After moving the database configuration and fixtures into `database.py`, your test file (e.g., `test_users.py`) becomes more organized. It now only needs to import the necessary fixtures and define the test cases. For instance:

```python theme={null}
from app import schemas
from database import client, session

def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message") == "Hello World"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123"}
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201
```

After saving your changes, running your tests should confirm that both tests pass successfully. This organized setup not only cleans up your test files but also ensures that the database is properly configured and available during testing.

<Callout icon="triangle-alert">
  If you encounter warnings such as "is deprecated since Python 3.8, use 'async def' instead," review any legacy non-fixture code. Since table creation and session management are now fully handled within the fixtures, these warnings should no longer apply.
</Callout>

***

This concludes our lesson on setting up a test database with fixtures. By leveraging fixture dependency, we efficiently manage both the TestClient and the database session, simplifying testing and ensuring a reliable, isolated test environment.

For additional information and advanced testing strategies, please refer to the [FastAPI Testing Documentation](https://fastapi.tiangolo.com/tutorial/testing/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/eed445e5-68aa-46b3-9922-0fdf2a57b8f1/lesson/71e83dec-abb2-4491-86e9-baffe478b327" />
</CardGroup>


# Setup Test Database

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Testing/Setup-Test-Database/page

This article explains how to set up a separate test database in FastAPI to avoid interference with development data during testing.

Before proceeding, it's important to note that running tests against your development database is not ideal. Using your development, staging, or production databases for tests can cause interference and unexpected issues. To mitigate this, we will create and use a completely separate database specifically for testing.

Below is an example test for creating a user:

```python theme={null}
def test_create_user():
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123"}
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201
```

When you run the tests, you might see output similar to the following:

```plaintext theme={null}
tests/test_users.py::test_root Hello World
PASSED
tests/test_users.py::test_create_user PASSED
============================= 2 passed, 5 warnings in 0.87s =============================
```

Currently, the application imports the client from the main app. This causes the tests to use the existing development database (typically viewed in [PgAdmin](https://www.pgadmin.org)). Since the development database might contain pre-existing data, tests can unexpectedly fail. It is best to use a dedicated testing database.

Consider this test file snippet that includes the necessary changes to use a separate test database:

```python theme={null}
def test_root():
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message") == "Hello World"
    assert res.status_code == 200

def test_create_user():
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123"}
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201
```

The test outputs remain consistent:

```plaintext theme={null}
tests/test_users.py::test_root Hello World
PASSED
tests/test_users.py::test_create_user PASSED

========== 2 passed, 5 warnings in 0.87s ==========
```

One key advantage of our setup is the dependency injection configured in our `database.py` file. The original database configuration resembles the following:

```python theme={null}
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

This configuration creates a session dependency using a function like:

```python theme={null}
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Every SQLAlchemy query in your routes depends on this session object from `get_db`. To test in isolation, you can override this dependency with one that connects to your dedicated test database.

For example, a router file might include database dependency code similar to:

```python theme={null}
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

The dependency `get_db` is injected into the routes, making it easy to override for testing. To point tests to the dedicated database, create an override function (commonly named `override_get_db`) that returns a session connected to your test database. For example:

```python theme={null}
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
```

<Callout icon="lightbulb">
  This configuration ensures that whenever a route depends on `get_db`, FastAPI uses the testing session rather than the default development session.
</Callout>

Here’s an example demonstrating the testing of a user creation route using the dependency override:

```python theme={null}
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING """)
    new_post = cursor.fetchone()
```

After setting up the override, your tests run against the dedicated test database, yielding an output similar to:

```plaintext theme={null}
tests/test_users.py::test_root Hello World PASSED
tests/test_users.py::test_create_user PASSED
```

To complete the test setup, copy your database configuration into your tests and adjust the SQLAlchemy URL to point to your test database. One example is as follows:

```python theme={null}
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
