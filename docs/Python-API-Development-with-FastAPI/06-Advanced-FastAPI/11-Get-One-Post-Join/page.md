# Constants for token creation
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    """Creates a JWT access token with an expiration time."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    """Verifies the access token and retrieves the token data."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db)
):
    """
    Returns the current user based on the access token.
    This function first verifies the token, then queries the database
    to retrieve the user object.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"}
    )

    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if not user:
        raise credentials_exception
    return user
```

***

## Using the Current User Dependency in Route Operations

The following examples demonstrate how to integrate the `get_current_user` dependency within your route operations. Notice that the dependency now returns the full user object (referred to as `current_user`). This enhancement eliminates the need to repeatedly query the database in each endpoint.

***

```python theme={null}
from fastapi import APIRouter, Response, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
import schemas, models, database
from dependencies import get_current_user  # Adjust the import as per your project structure

router = APIRouter()

@router.get("/{id}", response_model=schemas.Post)
def get_post(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found"
        )
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist"
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist"
        )
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

@router.get("/", response_model=List[schemas.Post])
def get_posts(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    posts = db.query(models.Post).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Output the user's email for verification purposes.
    print(current_user.email)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
```

***

## Console Output Verification

When you run your application, you should see console output similar to the following:

INFO:     Started server process \[12328]\
INFO:     Application startup complete.\
[sanjeev@gmail.com](mailto:sanjeev@gmail.com)\
INFO:     127.0.0.1:59999 - "POST /posts HTTP/1.1" 201 Created

This output confirms that the `current_user` dependency correctly retrieves and prints the user’s email, ensuring that user-specific data is readily available for any subsequent business logic in your endpoints.

> **lightbulb** By returning the complete user object via the `get_current_user` dependency, your FastAPI application can efficiently access and utilize user-specific information throughout your route operations. This approach streamlines the management of authentication and user authorization in your API.

- [Watch Video](https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/ed782f8c-495c-4ff8-8703-c9ab0ab04a4d/lesson/7294905c-798f-46eb-b8a3-38f26f621a0a)


# Get One Post Join

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Advanced-FastAPI/Get-One-Post-Join/page

This article explains how to enhance an API endpoint to include vote counts when retrieving individual posts.

In this guide, we enhance our endpoint for retrieving an individual post by including the vote count in its JSON response. Previously, our endpoint for fetching multiple posts already used a join query to include votes, but the individual post retrieval did not incorporate this functionality.

## Creating a New Post

Below is the code snippet that demonstrates how a new post is created:

```python theme={null}
new_post = models.Post(owner_id=current_user.id, **post.dict())
db.add(new_post)
db.commit()
db.refresh(new_post)

return new_post
```

## Original Endpoint for Fetching a Single Post

The original implementation for retrieving a single post looked like this:

```python theme={null}
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id),))
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    return post
```

During testing, the console logs generated were similar to the following:

```plaintext theme={null}
WARNING:  WatchGodReload detected file change in '['C:\\Users\\sanje\\Documents\\Courses\\fastapi\\app\\routers\\post.py']'. Reloading...
INFO:     Started server process [10116]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:61470 - "GET /posts?limit=2 HTTP/1.1" 307 Temporary Redirect
INFO:     127.0.0.1:61470 - "GET /posts?limit=2 HTTP/1.1" 200 OK
```

## Integrating Vote Count with Join Queries

Since the JSON response did not include the vote count, we need to modify our query to join the votes table and count the votes. Here’s an example of the join query used for fetching multiple posts with their respective vote counts:

```python theme={null}
posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    models.Vote, models.Vote.post_id == models.Post.id, isouter=True
).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
return posts
```

## Updated Endpoint for a Single Post with Vote Count

Next, we update the individual post retrieval endpoint to include a join that fetches the vote count. The improved endpoint appears below:

```python theme={null}
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Fetch the post by its id
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    
    # Join posts with votes to count the number of votes for this post
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    return result
```

> **lightbulb** The updated endpoint now returns a JSON structure that includes both the main post data and the associated vote count. This enhancement provides a more comprehensive view of the post’s engagement.

During testing, the console output confirmed that the endpoint was working as expected:

```plaintext theme={null}
INFO:     127.0.0.1:61470 - "GET /posts/?limit=2 HTTP/1.1" 200 OK
INFO:     127.0.0.1:54833 - "GET /posts/10 HTTP/1.1" 200 OK
```

An example of a successful JSON response is:

```json theme={null}
{
  "Post": {
    "title": "asdf",
    "content": "sdfsf",
    "published": true,
    "id": 10,
    "created_at": "2021-08-28T21:49:28.150819-04:00",
    "owner_id": 23,
    "owner": {
      "id": 23,
      "email": "sanjeev@gmail.com",
      "created_at": "2021-08-28T21:03:56.927042-04:00"
    },
    "votes": 2
  }
}
```

> **triangle-alert** Ensure that all variables used in your queries are properly defined within the current scope. Errors like `NameError: name 'post' is not defined` may occur if variables are misspelled or referenced before initialization.

While you could extend this functionality to the post creation and update endpoints so that they also return the vote count, it is usually sufficient to include it only when fetching posts.

By implementing these changes, the get individual post endpoint now provides both the detailed post data and its vote count, resulting in an improved and more informative API response.

- [Watch Video](https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/ed782f8c-495c-4ff8-8703-c9ab0ab04a4d/lesson/1b21a16b-ee6e-4ee3-8da1-6be4c14b145b)
