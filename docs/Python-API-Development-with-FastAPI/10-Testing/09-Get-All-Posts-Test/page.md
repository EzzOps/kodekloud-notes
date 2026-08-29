# Get All Posts Test

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Testing/Get-All-Posts-Test/page

This article demonstrates tests for user authentication and post-related operations in an API, focusing on clarity and maintainability through organized testing practices.

This article demonstrates various tests for user authentication and post-related operations in our API. We begin by testing user creation and login, then move on to verifying post-related endpoints. Throughout the guide, notice how fixtures are used to streamline authentication and how tests are organized to promote clarity and maintainability.

***

## User Authentication Tests

Below is a sample test for creating a user and logging in:

```python theme={null}
def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123"}
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

def test_login_user(test_user, client):
    res = client.post(
        "/login", data={"username": test_user["email"], "password": test_user["password"]}
    )
```

Result output:

```plaintext theme={null}
collected 7 items

tests/test_users.py::test_create_user PASSED
tests/test_users.py::test_login_user PASSED
tests/test_users.py::test_incorrect_login[wrongemail@gmail.com-password123-403] PASSED
tests/test_users.py::test_incorrect_login[sanjeev@gmail.com-wrongpassword-403] PASSED
tests/test_users.py::test_incorrect_login[None-password123-422] PASSED
tests/test_users.py::test_incorrect_login[sanjeev@gmail.com-None-422] PASSED

warnings summary =====================
```

<Callout icon="lightbulb">
  The example above shows the use of fixtures and assertions to validate user creation and login processes. This practice ensures each test runs independently with proper setup and teardown.
</Callout>

For clarity, here is the corrected version of the user test code that can be stored in a dedicated module:

```python theme={null}
def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123"}
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

def test_login_user(test_user, client):
    res = client.post(
        "/login", data={"username": test_user["email"], "password": test_user["password"]}
    )
```

Result output:

```plaintext theme={null}
collected 7 items

tests/test_users.py::test_create_user PASSED
tests/test_users.py::test_login_user PASSED
tests/test_users.py::test_incorrect_login[wrongemail@gmail.com-password123-403] PASSED
tests/test_users.py::test_incorrect_login[sanjeev@gmail.com-wrongpassword-403] PASSED
tests/test_users.py::test_incorrect_login[None-password123-422] PASSED
tests/test_users.py::test_incorrect_login[sanjeev@gmail.com-None-422] PASSED

warnings summary
```

***

## Post Endpoints Testing

When dealing with posts, note that every POST path operation requires authentication. For example, the posts retrieval endpoint is defined as follows:

```python theme={null}
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Any = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    # Implementation code here
```

Result output:

```plaintext theme={null}
collected 7 items
tests/test_users.py::test_create_user PASSED
tests/test_users.py::test_login_user PASSED
tests/test_users.py::test_incorrect_login[wrongemail@gmail.com-password123-403] PASSED
...
warnings summary
```

<Callout icon="lightbulb">
  For endpoints requiring authentication, using fixtures to simulate token generation is a more efficient approach than performing a full login request for every test.
</Callout>

Instead of making a full API call to log in and retrieve a token for every test, it is more efficient to import the token creation function directly from the OAuth2 module. This allows simulation of token generation without going through the complete login process. Consider the following implementation:

```python theme={null}
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    # Verification logic
    pass
```

Result output:

```plaintext theme={null}
collected 7 items
tests/test_users.py::test_create_user PASSED
...
warnings summary
```

***

## Configuring Fixtures with conftest.py

In our `conftest.py`, we set up a fixture to create a test user. This fixture sends a POST request to the user creation endpoint and returns the user data along with their password for further testing:

```python theme={null}
import pytest

@pytest.fixture
def test_user(client):
    user_data = {"email": "sanjeev@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user
```

Result output:

```plaintext theme={null}
collected 7 items
tests/test_users.py::test_create_user PASSED
...
warnings summary ==================================
```

Next, create a fixture that generates an access token for the test user using the imported function:

```python theme={null}
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})
```

Result output:

```plaintext theme={null}
collected 7 items
tests/test_users.py::test_create_user PASSED
...
```

Then, set up an `authorized_client` fixture that modifies the original client’s headers to include the access token for endpoints requiring authentication:

```python theme={null}
import pytest

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client
```

Result output:

```plaintext theme={null}
collected 7 items
tests/test_users.py::test_create_user PASSED
...
```

***

## Testing the Retrieval of Posts

Now that authentication is handled by our fixtures, we can write a test for retrieving posts using the authorized client. This test sends a GET request to the `/posts/` endpoint, prints the response data for inspection, and asserts that the response status code is 200:

```python theme={null}
def test_get_all_posts(authorized_client):
    res = authorized_client.get("/posts/")
    print(res.json())
    assert res.status_code == 200
```

Result output:

```plaintext theme={null}
collected 7 items
tests/test_posts.py::test_get_all_posts PASSED
```

<Callout icon="lightbulb">
  When running this test, the output may show an empty array if there are no posts in your test database. In that case, ensure you create test posts before executing this test to confirm data retrieval works correctly.
</Callout>

To run the tests, use a command similar to the following:

```bash theme={null}
(venv) C:\Users\sanje\Documents\Courses\fastapi>pytest tests\test_posts.py -v -s
```

Result output:

```plaintext theme={null}
platform win32 -- Python 3.9.5, pytest-6.2.5, ...
collected 1 item

tests/test_posts.py::test_get_all_posts [] PASSED

===================================================================== warnings summary =====================================================================
...
```

***

## Summary

This article demonstrated the following:

* Organizing tests for user authentication and post endpoints.
* Simulating authentication efficiently using fixtures.
* Verifying test results with proper assertions.

In the upcoming article, we will explore creating test posts and validating the retrieved data.

For more technical guides and best practices, be sure to check the [Kubernetes Documentation](https://kubernetes.io/docs/) and other [developer resources](https://docs.python.org/3/tutorial/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/eed445e5-68aa-46b3-9922-0fdf2a57b8f1/lesson/40db0443-f2c8-4557-8497-8b66b7909fd0" />
</CardGroup>
