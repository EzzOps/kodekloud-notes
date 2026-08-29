# Testing Expired Token

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Advanced-FastAPI/Testing-Expired-Token/page

This guide demonstrates how to verify the JWT expiration mechanism and test access tokens with varying expiration times.

This guide demonstrates how to verify that the JWT expiration mechanism works as expected. A JSON Web Token (JWT) contains an expiration time that limits the validity of a user session. In our implementation, the default access token expires after 30 minutes. If a user attempts to access protected endpoints with the token beyond this duration, an error will be returned.

<Callout icon="lightbulb">
  The default token expiration is 30 minutes, ensuring enhanced security. However, for testing purposes, the expiration time is temporarily shortened.
</Callout>

## Creating an Access Token with a 30-Minute Expiration

Below is the Python code that creates an access token with a 30-minute expiration:

```python theme={null}
SECRET_KEY = "[SECRET_REDACTED]"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

During normal operation, your application logs may resemble the following:

```text theme={null}
INFO:     127.0.0.1:63400 - "DELETE /posts/ HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:65498 - "DELETE /posts/ HTTP/1.1" 204 No Content
INFO:     127.0.0.1:65830 - "PUT /posts/1 HTTP/1.1" 200 OK
INFO:     127.0.0.1:65415 - "PUT /posts/1 HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:65204 - "POST /posts/ HTTP/1.1" 307 Temporary Redirect
INFO:     127.0.0.1:62484 - "POST /posts/ HTTP/1.1" 201 Created
```

## Testing with a One-Minute Token Expiration

To expedite the testing process without waiting for 30 minutes, you can temporarily modify the token's expiration time to one minute. With this change, after one minute, the token will expire and any attempt to access protected endpoints will result in an "Unauthorized" error.

Here's the modified code for testing purposes:

```python theme={null}
SECRET_KEY = "[SECRET_REDACTED]"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1  # Set to one minute for testing

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

After updating the code, log in with a user so that the token is valid for one minute. To verify its functionality, you can retrieve some posts. For example, the following POST payload might be used when testing the "get posts" endpoint:

```json theme={null}
{
    "title": "top beaches in florida",
    "content": "something something beaches",
    "published": true,
    "id": 36,
    "created_at": "2021-08-28T01:40:44.626273-04:00"
}
```

Once you make a successful request, wait for a full minute. If you try accessing the posts again with the expired token, you should receive an error. A successful GET request might return a response similar to:

```json theme={null}
[
    {
        "title": "new sqlalchemy post",
        "content": "some random content",
        "published": true,
        "id": 4,
        "created_at": "2021-08-22T19:55:27.727572+00:00"
    },
    {
        "title": "welcome to funland",
        "content": "so much fun",
        "published": true
    }
]
```

And when the token has expired, the error response will be:

```json theme={null}
{
    "detail": "Could not validate credentials"
}
```

## Reverting to a Longer Expiration Time

After testing the token expiration, it is important to restore the intended expiration duration. For practical use, you might change the token's expiration to 60 minutes to minimize the need for frequent token refreshes. Below is the updated code reflecting this change:

```python theme={null}
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
