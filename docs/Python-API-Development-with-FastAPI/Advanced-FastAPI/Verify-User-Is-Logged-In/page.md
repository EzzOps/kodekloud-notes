# Verify User Is Logged In

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Advanced-FastAPI/Verify-User-Is-Logged-In/page

This article explains how to verify user authentication using access tokens and implement protected endpoints in FastAPI.

In this lesson, you'll learn how to verify that a user is logged in by using an access token. After authenticating a user by sending their username and password to the login endpoint, the API returns a JSON Web Token (JWT). This JWT must be included in the request payload every time the user needs to access a protected resource.

For example, after logging in, a user might receive a response like this:

```json theme={null}
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.[SECRET_REDACTED].WeZxYuAkAVEyb8-1A6LhwvpCyexRxQihWJ1IGDT0",
  "token_type": "bearer"
}
```

Whenever the client makes a request to an endpoint that requires authentication, the JWT from the access token is provided so the API can verify that it has not been tampered with or expired.

Below is another sample token payload:

```json theme={null}
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.[SECRET_REDACTED].6c7HaWhvpcYexRqQlhWJ1IGDT0",
  "token_type": "bearer"
}
```

> **Note: Token Structure**
>
> Before handling token verification, it is important to define a schema for the token. This ensures that both an access token and a token type, as strings, are received. You can also define an additional schema if more token data is required.

## Creating an Access Token

The following code snippet shows how to create an access token using the HS256 algorithm with a specified expiration time:

```python theme={null}
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

### Console Output Example

```plaintext theme={null}
[tapi/app/routers/auth.py]:: Reloading...
Database connection was successful!
INFO: Server process [3908]
INFO: Waiting for application startup.
INFO: Application startup complete.
127.0.0.1:58559 - "POST /login HTTP/1.1" 422 Unprocessable Entity
127.0.0.1:63605 - "POST /login HTTP/1.1" 200 OK
```

A user is expected to include the access token in subsequent requests. For instance:

```json theme={null}
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.[SECRET_REDACTED].K2RZLh0VgGldA2_P4FykoLUXf6CJc5H6-MFZagE-it4",
    "token_type": "bearer"
}
```

## Defining Token and User Schemas

To enforce the correct data structure, we define schemas for a user, their login credentials, and tokens as follows:

```python theme={null}
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
```

### Console Output Example

```plaintext theme={null}
[tapi/app/routers/auth.py]:: Reloading...
Database connection was successful!
INFO: Started server process [3980]
INFO: Waiting for application startup.
INFO: Application startup complete.
127.0.0.1:5859 - "POST /login HTTP/1.1" 422 Unprocessable Entity
127.0.0.1:63605 - "POST /login HTTP/1.1" 200 OK
```

## Token Verification

The data embedded into the access token, such as the user ID, is extracted using the following functions. Although embedding the user ID is optional, it is a good practice for validating the token:

```python theme={null}
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get("user_id")
```

### Console Output Example

```plaintext theme={null}
[tapi/app/routers/auth.py]:: Reloading...
Database connection was successfull!
Started server process [3980]
INFO: Waiting for application startup.
Application startup complete.
INFO: 127.0.0.1:58559 - "POST /login HTTP/1.1" 422 Unprocessable Entity
INFO: 127.0.0.1:63605 - "POST /login HTTP/1.1" 200 OK
```

If the token does not include a user ID, a credentials exception is raised. The token verification is wrapped in a try/except block to handle any JWT errors:

```python theme={null}
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_: str = payload.get("user_id")
        if id_ is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id_)
    except JWTError:
        raise credentials_exception

    return token_data
```

### Console Output Example

```plaintext theme={null}
[tapi/app/routers/auth.py]:: Reloading...
Database connection was successful!
INFO: Started server process [3980]
INFO: Waiting for application startup.
INFO: Application startup complete.
INFO: 127.0.0.1:5859 - "POST /login HTTP/1.1" 422 Unprocessable Entity
INFO: 127.0.0.1:63605 - "POST /login HTTP/1.1" 200 OK
```

## Protecting Endpoints with Authentication

Next, we define the function `get_current_user`. This function can be added as a dependency to any protected endpoint. FastAPI’s dependency injection, along with OAuth2, automatically extracts the token from the request:

```python theme={null}
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
