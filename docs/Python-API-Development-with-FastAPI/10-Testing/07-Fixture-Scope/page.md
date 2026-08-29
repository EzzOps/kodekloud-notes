# Fixture Scope

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Testing/Fixture-Scope/page

This article explores fixture scopes and their impact on testing user creation and login in FastAPI applications.

In this lesson, we explore how fixture scopes affect tests for user creation and login in a FastAPI application. We will start with testing user creation, move on to login functionality, and then examine how different fixture scopes (function, module, and session) impact test behavior.

***

## Testing User Creation

The following test case demonstrates how to create a new user. We send a POST request to the "/users/" endpoint with an email and password. The response is then deserialized into a UserOut schema and validated:

```python theme={null}
def test_create_user(client):
    res = client.post(
        "/users/", 
        json={"email": "hello123@gmail.com", "password": "password123"}
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201
```

Earlier versions of this test might have only checked the status code:

```plaintext theme={null}
/users/ json={"email": "hello123@gmail.com", "password": "password123"}
