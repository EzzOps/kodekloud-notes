# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$E2SxE1ZElStv1bvfx5v1kb6ZTb9v6Qoe6LruJ3vIPGmAmOQhnY4iK",
        "disabled": False,
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
```

For demonstration, a simple password string may suffice. However, for a production environment, always generate a secure secret key.

────────────────────────────────────────

## Step 4. Creating the Access Token

Define a function that creates an access token. The token payload includes the data you wish to expose (for example, the user ID) in addition to an expiration time. The expiration time is set by adding a defined time delta to the current timestamp.

Here’s the implementation:

```python theme={null}
def create_access_token(data: dict):
    to_encode = data.copy()  # Copy the data to prevent mutation
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # Add the expiration time to the payload
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

When this function is invoked, it generates a JWT token encoding both the provided data and the expiration time. The JWT library signs the token with the configured secret key and algorithm to ensure data integrity.

────────────────────────────────────────

## Step 5. Using the Token in a Login Endpoint

Integrate the token generation function into your FastAPI login endpoint. When a user supplies valid credentials, create an access token that includes the user ID. Return the token along with its type (in this case, "bearer") for use in the Authorization header of subsequent requests.

Below is an example of a login endpoint implementation:

```python theme={null}
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from .. import database, schemas, models, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.email
    ).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    # Create an access token using the user's id as payload.
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
```

Clients should include the token in the Authorization header like this:

```text theme={null}
Authorization: Bearer <JWT_TOKEN>
```

────────────────────────────────────────

## Step 6. Testing Your JWT Token

Once your FastAPI application is running, you can test the login endpoint with valid credentials. For example, send the following JSON payload:

```json theme={null}
{
    "email": "sanjeev@gmail.com",
    "password": "password123"
}
```

A successful response might look like this:

```json theme={null}
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNjMxMjM3Mzc5fQ.AKjP8cDhcdF0xB_BX6DYYh5LuPncVm8zl2nk_KRU",
    "token_type": "bearer"
}
```

To inspect the contents of your JWT token, visit [JWT.io](https://jwt.io/). Paste your token into the debugger to view the decoded header and payload. For example:

```plaintext theme={null}
Encoded
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjozNiwibmFtZSI6IkpvaG4ifQ.Q.4sWkRPbUhdcP0xB..._B6X6DYh1sUtnPcwMwZ1nk_KRU

Decoded
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "user": 36,
    "name": "John"
  },
  "Verify Signature": "HMACSHA256( base64UrlEncode(header) + \".\" + base64UrlEncode(payload), secret)"
}
```

This decoding lets you view the expiration time and other data contained in the token.

────────────────────────────────────────

## Understanding JWT Security

<Callout icon="lightbulb">
  JWTs are not encrypted. Their payload is simply base64 encoded, which means anyone who intercepts the token can read its content. However, thanks to the digital signature (using your secret key), any unauthorized modification to the token invalidates it. Additionally, an expiration time is added to the token to ensure that outdated tokens can no longer be used.
</Callout>

────────────────────────────────────────

## Conclusion

In this article, we've covered how to:

* Install python‑jose with its cryptography backend.
* Configure token settings including secret keys, algorithms, and expiration times.
* Create a JWT access token.
* Integrate the token into a FastAPI login endpoint.

This approach ensures your API can verify both the integrity and validity (through the expiration time) of the tokens provided by authenticated users.

Happy coding!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/ed782f8c-495c-4ff8-8703-c9ab0ab04a4d/lesson/d704faee-9ab1-45b0-a9e3-0b272a5608fa" />
</CardGroup>


# Creating User Table

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Advanced-FastAPI/Creating-User-Table/page

This article introduces user functionality in an application by creating a user table in PostgreSQL for registration, login, and post creation.

In this article, we introduce user functionality into our application. Users will be able to register, log in, and create posts linked to their accounts. The first step is to allow new users to register. To do this, we define our data model by creating a new table in our PostgreSQL database that stores user information.

Since we’re using SQLAlchemy, we will create an ORM model for users similar to the one used for posts. Below is the complete final version of our models, including the previously defined Post model:

```python theme={null}
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
```

After saving these changes, the application will automatically reload. You might see an output similar to the following in your console:

```plaintext theme={null}
app/models.py', 'C:\\Users\\sanje\\Documents\\Courses\\fastapi\\app\\models.py.915f4585d116cbdbbab21f73e5527481.tmp']. Reloading...
Database connection was successful!
INFO:     Started server process [18836]
INFO:     Waiting for application startup.
Application startup complete.
```

<Callout icon="lightbulb">
  In the User model:

  * The ID column serves as the primary key.
  * The email column is defined as a unique, non-nullable String to prevent duplicate registrations.
  * The password column is non-nullable.
  * The created\_at column automatically records when a record is added.
</Callout>

After the application restarts, open PgAdmin and refresh your tables to verify that the "users" table has been created with the necessary columns and constraints.

To verify the posts, run the following SQL query:

```sql theme={null}
SELECT * FROM public.posts
ORDER BY id ASC;
```

At this stage, the users table will be empty. To test user creation, right-click on the table in PgAdmin, select "View/Edit Data," and insert a new record. For example, add a user with the email "[john@gmail.com](mailto:john@gmail.com)" and any password. Upon saving, the generated ID and created timestamp should appear.

Next, test duplicate prevention by trying to insert another user with the same email. Execute the following SQL query to check the "users" table:

```sql theme={null}
SELECT * FROM public/users
ORDER BY id ASC;
```

If you attempt to insert a duplicate email, the database will throw a unique constraint error on the email field. To resolve this, change the email—for instance, to "[cindy@gmail.com](mailto:cindy@gmail.com)"—and save the record.

Use the following SQL query to view the current records in the "users" table:

```sql theme={null}
SELECT * FROM public/users
ORDER BY id ASC;
```

With the table and constraints now established, the first step is complete. The next phase will involve creating a new path operation in our API that enables users to register by submitting their email and password.

For more details on database design and managing SQL schemas, consider checking out the following resources: [PostgreSQL Documentation](https://www.postgresql.org/docs/) and [SQLAlchemy Documentation](https://docs.sqlalchemy.org/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/ed782f8c-495c-4ff8-8703-c9ab0ab04a4d/lesson/a5a7f26e-04b9-42e2-a3a2-012b09969d26" />
</CardGroup>
