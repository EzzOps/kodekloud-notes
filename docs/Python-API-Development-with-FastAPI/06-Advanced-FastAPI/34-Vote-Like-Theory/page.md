# SECRET_KEY, ALGORITHM and ACCESS_TOKEN_EXPIRE_MINUTES should be defined here
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

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

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return verify_access_token(token, credentials_exception)
```

### Console Output Example

```plaintext theme={null}
[tapi/app/routers/auth.py]:: Reloading...
Database connection was successful!
INFO: Started server process [3980]
INFO: Waiting for application startup.
INFO: Application startup complete.
INFO: 127.0.0.1:58595 - "POST /login HTTP/1.1" 422 Unprocessable Entity
INFO: 127.0.0.1:63605 - "POST /login HTTP/1.1" 200 OK
```

## Login Route Implementation

The login route in the authentication router utilizes the functions detailed above. Notice that the HTTP status code is set to 403 Forbidden when invalid credentials are provided. This accurately represents an error when a user supplies invalid credentials.

```python theme={null}
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, models, schemas, utils, oauth2

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    # Create a token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
```

### Console Output Example

```plaintext theme={null}
[tapi/app/routers/auth.py]:: Reloading...
Database connection was successful!
INFO: Started server process [3980]
INFO: Waiting for application startup.
INFO: Startup complete.
127.0.0.1:15859 - "POST /login HTTP/1.1" 422 Unprocessable Entity
127.0.0.1:163605 - "POST /login HTTP/1.1" 200 OK
```

## Securing Post Endpoints

When creating protected endpoints, such as those for creating new posts, add the dependency on `oauth2.get_current_user` to verify that the user is authenticated:

```python theme={null}
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.post("/", response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate, 
    db: Session = Depends(get_db), 
    get_current_user: int = Depends(oauth2.get_current_user)
):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
```

> **Note: Important Considerations**
>
> The dependency on `oauth2.get_current_user` ensures that the access token provided in the request is valid and that the user is authenticated before allowing actions such as creating posts.

## Summary of Key Corrections

* The JWT expiration time now leverages `datetime.utcnow()` to ensure UTC consistency.
* The JWT decode function now correctly passes the algorithm as a list (`algorithms=[ALGORITHM]`).
* Consistency in key names is maintained (using `"user_id"` instead of `"users_id"`).
* The proper HTTP status code (403) is utilized for invalid credentials.

This concludes the explanation on how to verify a user's token and how to protect endpoints using JWT and FastAPI.

- [Watch Video](https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/ed782f8c-495c-4ff8-8703-c9ab0ab04a4d/lesson/802a6fee-da8c-45b8-b77e-b8ce7e2cb422)


# Vote Like Theory

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Advanced-FastAPI/Vote-Like-Theory/page

This article explores implementing a basic like system for social media applications and discusses key design requirements and database structure.

In most social media applications, users interact with posts by voting or "liking" them. Platforms like [Facebook](https://www.facebook.com), [Instagram](https://www.instagram.com), and [Twitter](https://twitter.com) use likes, while [Reddit](https://www.reddit.com) employs a system of upvotes and downvotes. In this lesson, we’ll explore how to implement a basic like system and discuss the key requirements for its design.

## System Requirements

The primary requirements for our like system are as follows:

* A user should be able to like a post.
* Each user must only be allowed to like a given post once. Allowing multiple likes from the same user would artificially inflate the like count.
* When retrieving a post, the system should also return the total number of likes.

## Database Design for the Like System

Similar to how most applications separate concerns by using individual tables for users and posts, the like functionality should be implemented in its own table. The minimal columns essential for our likes table include:

| Column Name | Description                       |
| ----------- | --------------------------------- |
| Post ID     | ID of the post being liked        |
| User ID     | ID of the user who liked the post |

> **lightbulb** For systems with a more complex voting mechanism, like Reddit's upvote/downvote model, an additional column can be added to indicate the vote direction. However, in our simple like system, this extra detail is unnecessary.

The most critical aspect of designing our likes table is enforcing the uniqueness of each entry. While it is acceptable to have repeated post or user IDs individually, the combination of both (i.e., the composite pair) must be unique. For instance:

* A row indicating that post 12 is liked by user 4 is valid.
* Another valid row can indicate that post 28 is liked by user 9.
* However, if user 2 has already liked post 55, the system must reject any additional entries with the combination of (post 55, user 2).

## Enforcing Uniqueness with Composite Keys

In relational databases, a composite key is a primary key that is formed by combining two or more columns. Unlike a typical primary key that might consist of a single column (like an ID), the composite primary key in our likes table comprises both the post ID and the user ID. This approach guarantees that a user cannot like the same post more than once.

Consider the following scenarios:

* For post ID 12, if user 4 and user 9 both like it, there will be two distinct entries: (12, 4) and (12, 9).
* User 9 can like both post 28 and post 12, resulting in two unique pairs: (28, 9) and (12, 9).
* If there is an attempt to record a like with the combination (55, 2) when user 2 has already liked post 55, the database will reject this duplicate.

> **triangle-alert** Ensure that the composite key is properly indexed to enforce the uniqueness constraint. Failure to do so might lead to duplicate records, thereby compromising the integrity of the like count.

![The image explains composite keys in a database, showing a table with "Post\_id" and "User\_id" columns forming a primary key to ensure uniqueness.](https://kodekloud.com/kk-media/image/upload/v1752883343/notes-assets/images/Python-API-Development-with-FastAPI-Vote-Like-Theory/composite-keys-database-table.jpg)

By implementing a composite primary key, our database automatically guarantees that every record with a specific post ID and user ID pair is unique. This design effectively prevents users from liking the same post multiple times while still allowing a post to be liked by numerous users and a user to like multiple posts.

This concludes our discussion on the basic like system and the application of composite keys to maintain the uniqueness of likes in our application.

- [Watch Video](https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/ed782f8c-495c-4ff8-8703-c9ab0ab04a4d/lesson/3730c12c-6116-4109-81de-df951fe95a0d)
