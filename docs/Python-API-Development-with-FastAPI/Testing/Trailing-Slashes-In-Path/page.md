# Trailing Slashes In Path

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Testing/Trailing-Slashes-In-Path/page

This article explains the impact of trailing slashes in FastAPI endpoint paths on application behavior and testing outcomes.

Before moving forward, it's essential to understand how trailing slashes in endpoint paths can affect your FastAPI application, especially during testing. An endpoint defined with a trailing slash, such as `/users/`, requires that all requests strictly match this pattern. Sending a request to `/users` (without the trailing slash) will trigger FastAPI's built-in behavior: it issues a 307 Temporary Redirect to the correct URL (`/users/`). While this redirect is helpful in production, it can lead to unexpected results during testing.

## Example: Testing the "Create User" Endpoint

Consider the following code, which tests the "create user" endpoint:

```python theme={null}
from app import schemas
from .database import client, session

def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hello World'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "password123"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201
```

In this snippet, the endpoint is defined as `/users/`, so the request URL must include the trailing slash. If a request is made to `/users` without the trailing slash, FastAPI first sends a 307 redirect before processing it.

## Impact of Omitting the Trailing Slash

When testing, if the request URL omits the trailing slash, the following behavior occurs:

1. FastAPI issues a 307 Temporary Redirect.
2. The test might capture this redirect response (307) instead of the expected 201 Created response.

For example, consider the test code below where schema validation is commented out to focus solely on the status code:

```python theme={null}
def test_create_user(client):
    res = client.post(
        "/users", json={"email": "hello123@gmail.com", "password": "password123"}
    )
    # new_user = schemas.UserOut(**res.json())
    # assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201
```

The output from this scenario might show:

```Python theme={null}
"/users", json={"email": "hello123@gmail.com", "password": "password123"})
