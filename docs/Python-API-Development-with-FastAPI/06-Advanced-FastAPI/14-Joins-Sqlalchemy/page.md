# Configure Passlib to use bcrypt for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

while True:
    # Your database connection logic goes here
    break
```

This configuration sets up the CryptContext to use the bcrypt algorithm for secure password hashing.

## Updating the User Registration Endpoint

To ensure passwords are securely stored, update the registration endpoint to hash the password before saving it to the database:

```python theme={null}
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the user's password before storing it in the database
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
```

A similar version of this endpoint appears as follows:

```python theme={null}
@app.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password using Passlib's CryptContext
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
```

After creating a user, you can confirm that the password has been hashed by running:

```sql theme={null}
select * from users;
```

Since hashing is a one-way process, retrieving the original password from the hash is not feasible.

## Extracting the Hashing Logic for Maintainability

To improve code maintainability, extract the password hashing logic into a separate utility function. Create a new file named `utils.py` with the following content:

```python theme={null}
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str) -> str:
    return pwd_context.hash(password)
```

Then, modify your `main.py` to import and use this new utility function:

```python theme={null}
from sqlalchemy.sql.functions import mode
from . import models, schemas, utils
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

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
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)
```

Update the user registration endpoint to use the utility function for hashing:

```python theme={null}
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the user's password using the utility function from utils.py
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
```

After testing the endpoint—by creating a new user (e.g., email "[mark@gmail.com](mailto:mark@gmail.com)" with password "password123")—query the users table:

```sql theme={null}
select * from users;
```

This query will confirm that the application stores only the hashed password, significantly reducing security risks in the event of a data breach.

<Callout icon="lightbulb">
  By following these steps, you enhance your application's security by ensuring user passwords are hashed rather than stored in plain text. This practice is essential for maintaining user data integrity.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/ed782f8c-495c-4ff8-8703-c9ab0ab04a4d/lesson/08fbff1f-121f-4210-ad9a-e600223963d0" />
</CardGroup>


# Joins Sqlalchemy

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Advanced-FastAPI/Joins-Sqlalchemy/page

Explains building SQLAlchemy joins in FastAPI to fetch posts with vote counts, handle aggregation, pagination, and resolve Pydantic response model mismatches.

This guide demonstrates how to combine data from two tables using SQLAlchemy joins within a FastAPI posts router. We'll build the query incrementally: start from a basic posts query, add a join to the votes table, aggregate (count) votes per post, and then apply filters, limit, and offset. Finally, we'll cover response-model mismatches and two strategies to resolve them.

Why this matters

* Efficiently fetch posts with vote counts in a single query.
* Avoid N+1 query problems by leveraging SQL joins and aggregation.
* Ensure FastAPI/Pydantic response models match the returned data shape.

Table of contents

* Basic posts query
* Adding a JOIN
* Counting votes and grouping
* Complete query with filters, limit, and offset
* Response model mismatches and solutions
* Final router implementation
* Alternative: flattening results
* Summary and references

## Basic posts query (fetch posts only)

This is the starting `get_posts` implementation that retrieves posts only:

```python theme={null}
from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    posts = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return posts
```

Note: the core of the query is `db.query(models.Post)` — this returns mapped Post model instances (one per row). If you remove `.all()` you get a SQLAlchemy Query object; inspect it with `str(query)` or `query.statement` to view the generated SQL for debugging.

## Adding a JOIN

To include vote information, add a `join(...)` to the query. This demonstrates joining the `votes` table on the foreign key:

```python theme={null}
results = db.query(models.Post).join(
    models.Vote, models.Vote.post_id == models.Post.id
)
```

<Callout icon="lightbulb">
  By default SQLAlchemy produces an inner join. Use `isouter=True` to create a
  LEFT OUTER JOIN so posts with zero votes are included.
</Callout>

If you want to include posts without any votes (i.e., zero votes), use a left outer join:

```python theme={null}
results = db.query(models.Post).join(
    models.Vote, models.Vote.post_id == models.Post.id, isouter=True
)
```

## Counting votes and grouping

To compute vote counts per post, import SQLAlchemy's `func` and apply `func.count(...)` along with `.group_by(...)`. Use `.label(...)` to name the aggregated column:

```python theme={null}
from sqlalchemy import func

results = (
    db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
    .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
    .group_by(models.Post.id)
)
```

The generated SQL is equivalent to:

SELECT posts.\*, count(votes.post\_id) AS votes\
FROM posts LEFT OUTER JOIN votes ON votes.post\_id = posts.id\
GROUP BY posts.id;

Naming the label (we used "votes") makes it easy to read the results and include the count in the API response.

## Complete query with filters, limit, and offset

Re-apply filtering, pagination, and execute the query:

```python theme={null}
results = (
    db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
    .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
    .group_by(models.Post.id)
    .filter(models.Post.title.contains(search))
    .limit(limit)
    .offset(skip)
    .all()
)
```

This returns a list where each row contains two elements (commonly as a tuple): `(PostInstance, votes_count)`.

## Pydantic response model mismatch and solution

When your endpoint's `response_model` is `List[schemas.Post]` but you return `(PostInstance, votes_count)` rows, FastAPI/Pydantic will raise validation errors because the returned structure doesn't match the expected schema shape.

Two approaches to fix this:

1. Create a response schema that matches the returned tuple/nested shape.
2. Flatten/transform each row into a dict matching an existing schema.

Below is an example response schema approach.

Example schemas to match the returned structure

```python theme={null}
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post   # capital "Post" matches how the query result may be serialized
    votes: int

    class Config:
        orm_mode = True
```

Important: If your query serialization nests the Post under a capitalized `Post` key, your Pydantic model must match that key exactly. Otherwise set a different returned shape or adjust your schema accordingly.

<Callout icon="warning">
  If your response model does not match the exact shape (keys, nesting,
  capitalization) of the returned data, FastAPI/Pydantic will raise validation
  errors. Update the returned data shape or the response model to match.
</Callout>

## Final router implementation (response model matches joined results)

Set the endpoint's `response_model` to `List[schemas.PostOut]` and return the query results directly:

```python theme={null}
from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return results
```

Returned JSON shape (example):

```json theme={null}
[
  {
    "Post": {
      "title": "something something beaches hello",
      "content": "something something beaches",
      "published": true,
      "id": 19,
      "created_at": "2021-08-28T22:38:44.511524-04:00",
      "owner_id": 21,
      "owner": {
        "id": 21,
        "email": "sanjeev1@gmail.com",
        "created_at": "2021-08-28T21:09:08.032365-04:00"
      }
    },
    "votes": 0
  }
]
```

## Alternative: flattening results into a single dict per post

If you prefer a top-level post object that includes `votes` (no nested `Post` key), transform the query rows before returning:

```python theme={null}
rows = (
    db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
    .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
    .group_by(models.Post.id)
    .filter(models.Post.title.contains(search))
    .limit(limit)
    .offset(skip)
    .all()
)

flattened = []
for post, votes in rows:
    post_dict = dict(post.__dict__)
    # remove SQLAlchemy protected attribute
    post_dict.pop("_sa_instance_state", None)
    post_dict["votes"] = votes
    flattened.append(post_dict)
