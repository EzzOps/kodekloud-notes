# Pydantic Models Deep Dive

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Advanced-FastAPI/Pydantic-Models-Deep-Dive/page

Explains extracting and reusing Pydantic schemas in a separate module, using inheritance and response models with orm_mode to produce consistent, documented FastAPI request and response shapes.

This article demonstrates how to extract Pydantic schemas into their own module, reuse fields via inheritance, and define response schemas so FastAPI returns consistent, documented API shapes.

Why separate schemas into their own file?

* Keeps `main.py` focused on routing and app wiring.
* Promotes reuse of schema classes across endpoints (create, update, responses).
* Simplifies tests, documentation, and OpenAPI generation.

## Quick example: inline schema (before extraction)

This works for tiny examples but becomes hard to maintain as your API grows.

```python theme={null}
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
```

Move related schemas into a dedicated `schemas.py` so you can clearly separate request shapes (what clients send) and response shapes (what your API returns).

## Create schemas.py

* Define base fields once and reuse them with inheritance.
* Create distinct classes for create/update requests if input requirements differ.
* Add `orm_mode = True` on response schemas to allow Pydantic to read SQLAlchemy ORM objects.

Example `schemas.py`:

```python theme={null}
from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    """Used for POST /posts — all fields required unless defaulted in Base."""
    pass

class PostUpdate(PostBase):
    """Use this for PUT/PATCH when update semantics differ (e.g., optional fields)."""
    # For partial updates you might prefer all fields optional:
    # title: Optional[str] = None
    # content: Optional[str] = None
    # published: Optional[bool] = None
    pass

class PostOut(PostBase):
    id: int

    class Config:
        orm_mode = True
```

Table: Schema classes and common use cases

| Schema class | Use case                             | Notes                                                          |
| ------------ | ------------------------------------ | -------------------------------------------------------------- |
| `PostBase`   | Shared fields for requests/responses | Base for inheritance to avoid repetition                       |
| `PostCreate` | Request body when creating a post    | Use for `POST /posts`                                          |
| `PostUpdate` | Request body when updating           | Use for `PUT/PATCH` — can be made optional for partial updates |
| `PostOut`    | Response model returned by endpoints | Set `orm_mode = True` so Pydantic accepts SQLAlchemy models    |

## Using the schemas in main.py

Import the `schemas` module and reference specific classes in endpoint signatures. Using `response_model` enforces the output shape and adds it to the generated OpenAPI docs.

App setup (assumes `models.py` and `database.py` exist):

```python theme={null}
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
```

GET all posts (returns a list of `PostOut`):

```python theme={null}
@app.get("/posts", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts
```

GET a single post by id:

```python theme={null}
@app.get("/posts/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    return post
```

Create a post (request uses `PostCreate`; response uses `PostOut`):

```python theme={null}
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
```

Update a post:

```python theme={null}
@app.put("/posts/{id}", response_model=schemas.PostOut)
def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    # Use exclude_unset=True for partial updates so defaults don't overwrite existing data.
    post_query.update(updated_post.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return post_query.first()
```

Delete a post:

```python theme={null}
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```

> **lightbulb** When you use `response_model` with SQLAlchemy ORM objects, set `orm_mode = True` on the response Pydantic model (as shown in `PostOut`). This tells Pydantic to read attributes from ORM instances instead of expecting plain dicts.

## When to create multiple request schemas

Create separate request schemas when permissions or allowed fields differ between operations:

* POST: full creation input (e.g., `PostCreate`).
* PUT/PATCH: partial updates or restricted updates (e.g., `PostUpdate` with optional fields).
* Separate schemas also make validation rules explicit and reduce accidental field overwrite.

Diagram: Schema models overview
Schemas/Pydantic models define both request and response shapes, enforce required fields, and help maintain a stable API contract between clients and your FastAPI backend.

<Frame>
  <img alt="A presentation slide titled &#x22;Schema Models&#x22; explaining that Schema/Pydantic models define the structure of requests and responses and enforce required fields like &#x22;title&#x22; and &#x22;content.&#x22; A diagram shows a browser (Chrome logo) sending a request through a schema/pydantic model to a FastAPI server and receiving a response back through a schema model." />
</Frame>

## Links and references

* [FastAPI — Pydantic models](https://fastapi.tiangolo.com/tutorial/schema/)
* [OpenAPI Specification](https://www.openapis.org/)
* [SQLAlchemy ORM documentation](https://docs.sqlalchemy.org/en/14/orm/)

Use these practices to keep your code modular, validation explicit, and responses predictable — improving developer experience and API reliability.

- [Watch Video](https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/ed782f8c-495c-4ff8-8703-c9ab0ab04a4d/lesson/8fab93e9-8c4a-4c46-a5e3-bcc5bca0afd6)
