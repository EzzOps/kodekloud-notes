# Create Posts Sql

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Databases-with-Python/Create-Posts-Sql/page

Learn to create a new post using FastAPI and PostgreSQL while ensuring SQL parameterization and preventing SQL injection.

In this lesson, you will learn how to create a new post using FastAPI along with PostgreSQL, while following best practices for SQL parameterization. We will cover how to insert a post into the database, prevent SQL injection, retrieve the newly created record, and commit the transaction to persist the changes. The code examples and console outputs provided will help you understand the workflow in a clear, step-by-step manner.

***

## 1. Initial Endpoint Setup

We start by defining endpoints to retrieve all posts, create a new post, and fetch a specific post by its ID. Previously, posts were stored in an in-memory list and a Pydantic model was used to parse the request body. For instance:

```python theme={null}
@app.get("/posts/")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    ...
```

This initial version works for basic illustration purposes; however, it doesn't interact with a SQL database.

***

## 2. Inserting Data with SQL

To insert a new post into the PostgreSQL database, we use the cursor's `execute` method with a parameterized SQL `INSERT` statement. Consider the following SQL command that shows the structure of the `posts` table:

```sql theme={null}
SELECT * FROM public.posts
ORDER BY "id" ASC;
```

The table includes three critical fields: `title`, `content`, and `published`. An ID and creation timestamp are automatically generated. To insert values into these columns, we use placeholders (`%s`) in our query and provide a tuple of values. For example:

```python theme={null}
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)""",
        (post.title, post.content, post.published)
    )
    return {"data": "created post"}
```

> **lightbulb** Using parameterized queries not only simplifies the code but also protects the database by ensuring that inputs are sanitized.

***

## 3. Preventing SQL Injection

Using f-strings to insert values directly into SQL statements can lead to vulnerabilities such as SQL injection. For example, avoid using:

```python theme={null}
