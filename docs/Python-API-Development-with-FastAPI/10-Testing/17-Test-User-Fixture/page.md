# Test User Fixture

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Testing/Test-User-Fixture/page

This article explains how to create a test user fixture to decouple login tests from external states, improving test modularity and reducing code duplication.

In this lesson, we demonstrate how to decouple the login user test from other tests by ensuring the test does not rely on external states. The solution is to create a fixture that sets up a test user before executing the login test.

Below is the original login test code, which creates a user and then performs a login:

```python theme={null}
res = client.post(
    "/users/", json={"email": "hello123@gmail.com", "password": "password123"}
)

new_user = schemas.UserOut(**res.json())
assert new_user.email == "hello123@gmail.com"
assert res.status_code == 201

def test_login_user(client):
    res = client.post(
        "/login", data={"username": "hello123@gmail.com", "password": "password123"}
    )
    print(res.json())
    assert res.status_code == 200
```

When running these tests, you might encounter an error similar to:

```plaintext theme={null}
venv\lib\site-packages\aiofiles\os.py:10: DeprecationWarning: "@coroutine" decorator is deprecated since Python 3.8, use "async def" instead
-- Docs: https://docs.pytest.org/en/stable/warnings.html
FAILED tests/test_users.py::test_login_user -> assert 403 == 200
```

This error occurs because the login test expects a user to exist before running. The underlying issue is the need for a consistent fixture order or scope. Our goal is to centralize the user creation logic in a fixture, avoiding code repetition across multiple tests.

Previously, the following snippet was repeated for creating a user and testing login:

```python theme={null}
res = client.post(
    "/users/", json={"email": "hello123@gmail.com", "password": "password123"}
)

new_user = schemas.UserOut(**res.json())
assert new_user.email == "hello123@gmail.com"
assert res.status_code == 201

def test_login_user(client):
    res = client.post(
        "/login", data={"username": "hello123@gmail.com", "password": "password123"}
    )
    print(res.json())
    assert res.status_code == 200
```

with output:

```plaintext theme={null}
venv\lib\site-packages\aiofiles\os.py:10
c:\users\sanje\documents\courses\fastapi\venv\lib\site-packages\aiofiles\os.py:10: DeprecationWarning: "@coroutine" decorator is deprecated since Python 3.8, use "async def" instead
def run(*args, loop=None, executor=None, **kwargs):
-- Docs: https://docs.pytest.org/en/stable/warnings.html
FAILED tests/test_users.py::test_login_user - assert 403 == 200
```

<Callout icon="lightbulb">
  Centralizing the user creation logic in a fixture makes our tests modular and avoids code duplication.
</Callout>

## Setting Up the User Fixture

First, remove or comment out any redundant tests at the top of your test file. Then, import pytest along with other required modules:

```python theme={null}
import pytest
from app import schemas
from database import client, session
```

Now, define a fixture that posts to the user creation endpoint. This fixture asserts successful user creation and returns the user data, including the password for subsequent login:

```python theme={null}
@pytest.fixture
def test_user(client):
    user_data = {"email": "sanjeev@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    # Include the password in the returned data for later authentication
    new_user["password"] = user_data["password"]
    return new_user
```

## Updating the Login Test

With the test user fixture in place, modify the login test to depend on both the client and the test\_user fixture. This ensures that any changes in user creation details automatically propagate to the login test:

```python theme={null}
def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username": test_user["email"], "password": test_user["password"]}
    )
    print(res.json())
    assert res.status_code == 200
```

## Dependencies: Session and Client Fixtures

The client fixture depends on a session fixture. An example session fixture (typically defined elsewhere) might look like:

```python theme={null}
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

@pytest.fixture(scope="module")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Similarly, the client fixture may override the dependency to use our test database session:

```python theme={null}
@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            pass
    # The following setup is an example if you're using FastAPI:
    # app.dependency_overrides[get_db] = override_get_db
    # yield TestClient(app)
```

## Example Test Output

When running the tests, you might initially see output similar to:

```plaintext theme={null}
cachedir: .pytest_cache
rootdir: C:\Users\sanjeev\Documents\Courses\fastapi
plugins: cov-2.12.1
collected 2 items

tests/test_users.py::test_create_user PASSED
tests/test_users.py::test_login_user {'id': 1, 'email': 'sanjeev@gmail.com', 'created_at': '2021-09-12T22:33:05.149462-04:00'}
{'detail': 'Invalid Credentials'}
FAILED
```

After properly linking the fixture and ensuring that the login test sends the correct credentials from the test user, the final output should be:

```plaintext theme={null}
cachedir: .pytest_cache
rootdir: C:\Users\sanjeev\Documents\Courses\fastapi
plugins: cov-2.12.1
collected 2 items

tests/test_users.py::test_create_user PASSED
tests/test_users.py::test_login_user PASSED
```

<Callout icon="lightbulb">
  By refactoring our tests in this way, any changes to user credentials in the fixture will automatically reflect in the login test. This modular approach improves the maintainability and reliability of your test suite.
</Callout>

Happy testing!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/eed445e5-68aa-46b3-9922-0fdf2a57b8f1/lesson/01fc22c9-7488-4c06-a0ac-96a719d3e5bd" />
</CardGroup>
