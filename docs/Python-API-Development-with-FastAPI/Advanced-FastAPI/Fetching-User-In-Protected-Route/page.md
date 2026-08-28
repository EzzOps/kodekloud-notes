# Database connection handling
while True:
    try:
        conn = psycopg2.connect(
            host='localhost', 
            database='fastapi', 
            user='postgres',
            password='password123', 
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1}, 
    {"title": "favorite foods", "content": "I like pizza", "id": 2}
]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

# Include the router objects for user and post endpoints
app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Hello World"}
```

With these changes, FastAPI delegates request handling to the appropriate router based on the URL endpoints, keeping the code modular and manageable as the application grows.

## Testing the Application

Once refactored, test your application to confirm that all functionality operates as expected. Typical tests include:

* Fetching all posts
* Creating a new post
* Retrieving a single post by ID
* Deleting or updating posts
* Creating a new user and retrieving the user by ID

For instance, a successful post creation might respond with:

```json theme={null}
{
    "title": "this is the new title",
    "content": "this is the new content",
    "published": true,
    "id": 1,
    "created_at": "2021-08-22T01:35:58.101063-04:00"
}
```

And the server logs may display:

```plaintext theme={null}
INFO:     127.0.0.1:55409 - "POST /posts HTTP/1.1" 201 Created
INFO:     127.0.0.1:55409 - "GET /posts/2 HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55409 - "GET /posts/1 HTTP/1.1" 200 OK
INFO:     127.0.0.1:55409 - "DELETE /posts/3 HTTP/1.1" 204 No Content
INFO:     127.0.0.1:55409 - "POST /users HTTP/1.1" 201 Created
INFO:     127.0.0.1:55409 - "GET /users/1 HTTP/1.1" 200 OK
```

<Callout icon="lightbulb">
  Using routers helps keep your code clean and scalable. As your API grows, you can easily add new routers without cluttering the main application file.
</Callout>

Happy coding!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/ed782f8c-495c-4ff8-8703-c9ab0ab04a4d/lesson/dfef71ab-504b-4390-ad8d-7c8b45f0a3b4" />
</CardGroup>


# Fetching User In Protected Route

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Advanced-FastAPI/Fetching-User-In-Protected-Route/page

Learn to fetch the current user from your database using an access token in a FastAPI application.

In this lesson, you will learn how to leverage an access token to fetch the current user directly from your database. Initially, the implementation of the `get_current_user` function calls the `verify_access_token` function, which only extracts and returns the user ID from the token data. Enhancing this logic to automatically retrieve the full user record allows you to attach the complete user object to any path operation, enabling more complex business logic in your endpoints.

Below, you’ll find the initial implementation demonstrating the basic structure using the `verify_access_token` function and the `get_current_user` dependency.

***

```python theme={null}
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)
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

***

<Callout icon="lightbulb">
  In a production application, remember that the token data only contains the user ID. To work with the entire user object, you must extend this implementation to query your database.
</Callout>

## Extended Implementation: Retrieving the User Object from the Database

In a real-world scenario, after verifying the token, you will want to query your database to fetch the complete user record. The extended version below demonstrates how to import your database session dependency, query the user model, and return the full user object.

***

```python theme={null}
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import schemas, models, database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
