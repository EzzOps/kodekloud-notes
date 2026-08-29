# Create Posts

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/FastAPI-Basics/Create-Posts/page

This article discusses refactoring FastAPI code to align with RESTful principles and standardizing API endpoint naming conventions.

In previous examples, we discussed best practices and naming conventions for building APIs. In this updated guide, our FastAPI code is refactored to align with RESTful principles and industry standards.

## Initial Implementation

Initially, our application defined GET and POST endpoints as follows:

```python theme={null}
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}

@app.post("/createposts")
def create_posts(post: Post):
    print(post)
    print(post.dict())
    return {"data": post}
```

Notice that the POST endpoint is defined with the path `/createposts`, which is inconsistent with RESTful naming standards. Our goal is to standardize all endpoints, so we update the POST endpoint to use `/posts`.

## Improved Endpoint Definition

By changing the POST endpoint to `/posts`, our API maintains a consistent naming scheme. The updated endpoint is shown below:

```python theme={null}
@app.post("/posts")
def create_posts(post: Post):
    print(post)
    print(post.dict())
    return {"data": post}
```

After updating the endpoint, be sure to adjust your testing tools—such as [Postman](https://www.postman.com)—with the new endpoint URL. For example, sending the following JSON in a POST request:

```json theme={null}
{
  "title": "top beaches in florida",
  "content": "something something beaches",
  "rating": 4
}
```

will now target the `/posts` endpoint. When tested, this endpoint responds as expected.

<Callout icon="lightbulb">
  Keep in mind that this example only prints and returns the submitted post; it does not persist data in a database.
</Callout>

## Simulating Data Persistence

Since this simple example does not use a database, we simulate data persistence by storing posts in an in-memory list. In a production setting, these posts would be saved to a database where ID creation is handled automatically. Here, we assign a unique ID to each post using a random integer.

Below is the consolidated version of our FastAPI application:

```python theme={null}
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
