# Hashing User Password

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Advanced-FastAPI/Hashing-User-Password/page

This article explains how to securely hash user passwords before storing them in a database to enhance application security.

Earlier, we outlined the process for creating a new user. However, storing passwords as plain text poses a significant security risk. Even if your database is secure now, a breach could expose these passwords to attackers. Instead, always store a hashed version of the password. Hashing is a one-way process that makes it practically impossible to retrieve the original password from its hash.

For instance, running the following SQL command:

```sql theme={null}
select * from users;
```

reveals that storing plain text passwords (as the query would show) is unsafe. Always hash passwords before saving them to your database.

> **lightbulb** FastAPI’s documentation provides an excellent guide on password hashing under the [OAuth2 with Password section](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/).

## Installing Required Libraries

To implement password hashing, you need two libraries: Passlib (which supports multiple hashing algorithms) and bcrypt (the algorithm we will use). Install them using pip:

```bash theme={null}
pip install passlib[bcrypt]
```

Alternatively, install both libraries directly:

```bash theme={null}
pip install passlib bcrypt
```

After installation, verify that both libraries are installed by running `pip freeze`.

## Application Models and Environment

Below is a snippet from our application models and configurations:

```python theme={null}
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
```

And a sample of our environment package list:

```plaintext theme={null}
colorama==0.4.4
dnspython==2.1.0
email-validator==1.1.3
fastapi==0.68.0
graphene==2.1.9
```

## Configuring the Password Hasher

In your main file, import `CryptContext` from Passlib to create a password context that utilizes bcrypt:

```python theme={null}
from fastapi.params import Body
from pydantic import BaseModel
from passlib.context import CryptContext
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from . import models, schemas
from .database import engine, get_db
