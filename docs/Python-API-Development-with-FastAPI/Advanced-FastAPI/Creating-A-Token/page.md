# Creating A Token

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Advanced-FastAPI/Creating-A-Token/page

Learn to create and manage JWT tokens for authentication in a FastAPI application, covering installation, configuration, token creation, and integration into a login endpoint.

In this guide, you'll learn how to create and manage JWT tokens for authentication in a FastAPI application. This implementation follows the [FastAPI documentation](https://fastapi.tiangolo.com/advanced/security/) for password-based authentication. The article covers installing the required library, configuring token settings, creating the token, and integrating it into a login endpoint.

────────────────────────────────────────

## Step 1. Installing the Required Library

First, install the library that handles signing and verification of JWT tokens. FastAPI uses the Python library python‑jose with a cryptography backend. Open your terminal and run the following command:

```bash theme={null}
pip install python-jose[cryptography]
```

After the installation, you should see output similar to:

```plaintext theme={null}
Installing collected packages: cryptography
Successfully installed cryptography-3.4.8 edcsa-0.15-python-jose cryptography
WARNING: You are using pip version 21.1.1; however, version 21.2.4 is available.
```

────────────────────────────────────────

## Step 2. Project Structure and File Setup

For handling authentication and JWT tokens, create a new file (for example, `oauth2.py`). Organize your project by including routers for posts, users, and authentication. A sample snippet might look like this:

```python theme={null}
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to the API"}
```

────────────────────────────────────────

## Step 3. Importing JWT Functions and Setting Up Token Configuration

Begin by importing JWT functionalities from python‑jose and setting up your token configuration. This includes defining a secret key, algorithm, and token expiration time. The secret key should be a long, randomly generated string.

<Callout icon="lightbulb">
  To generate a secure secret key, use the command: `openssl rand -hex 32`
</Callout>

Below is an example configuration:

```python theme={null}
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
