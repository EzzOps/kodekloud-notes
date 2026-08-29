# Setup Test Database With Fixtures

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Testing/Setup-Test-Database-With-Fixtures/page

This article explains how to set up a test database using fixtures and manage dependencies for efficient testing.

In this lesson, we will learn how to set up a test database using fixtures and configure one fixture to depend on another. This approach enables you to create a fixture that returns a database session (or database object) and then pass that session fixture to another fixture that provides a configured TestClient. Dependency chaining like this simplifies database manipulation and client usage in your tests.

<Callout icon="lightbulb">
  Using fixture dependency helps separate concerns by allowing one fixture to manage the database session while another focuses on providing an HTTP client. This setup ensures that tests run against a freshly configured database, improving test reliability.
</Callout>

***

## Overriding the Database Dependency with a Client Fixture

Below is an initial example where we override the dependency for the database connection using a fixture that returns a TestClient:

```python theme={null}
@app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)

def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message") == "Hello World"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@email.com", "password": "password123"})
```

In this example, the fixture returns our client. However, if you need direct access to the database object, you can separate the responsibilities by creating a dedicated fixture (named `session`) to set up the database and return a database session. Then, pass this `session` fixture to the TestClient fixture.

***

## Creating a Session Fixture and Chaining Dependencies

Below is an updated version where we define the `session` fixture for managing database setup (dropping and creating tables) and then configure the TestClient fixture to use this session:

```python theme={null}
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
def client():
    yield TestClient(app)

def test_test_root(client):
    # This test uses the client fixture which initializes the database session
    res = client.get("/")
```

At this point, the test framework ensures that whenever the `client` fixture is used, the `session` fixture runs first. This guarantees a fresh database setup and an available session before tests execute. You can also access the session directly in your tests if necessary.

Here’s an enhanced version that demonstrates passing the `session` fixture into the TestClient fixture and using it in a test:

```python theme={null}
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
    yield TestClient(app)

def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message") == "Hello World"
```

***

## Overriding the Database Dependency Properly

Next, modify the `client` fixture to override the database dependency correctly. Instead of yielding a hard-coded database object, define an inner function `override_get_db` that yields the `session` fixture. Apply this override before returning the TestClient:

```python theme={null}
@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message") == "Hello World"
    assert res.status_code == 200
```

With this setup, every time a test uses the `client` fixture, the `session` fixture is invoked first. This guarantees that the TestClient has access to a fresh database session, allowing direct database queries such as `session.query(models.Post)` when required.

For example, to access the database session separately from the client, include the `session` fixture in your test parameters:

```python theme={null}
@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

def test_root(client, session):
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message") == "Hello World"
    assert res.status_code == 200
```

The `client` fixture now ensures that the `session` fixture executes beforehand, and the database dependency override is applied accordingly.

***

## Organizing Database Configuration into a Separate File

After verifying that your tests work as expected (for example, running `pytest tests/test_calculations.py` in the terminal), consider cleaning up your test files by moving database-specific code and fixtures into a separate file (such as `database.py`) within your test directory.

An example of what the `database.py` file might look like:

```python theme={null}
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db, Base
from alembic import command
