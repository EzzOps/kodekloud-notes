# Update Posts

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Databases-with-Python/Update-Posts/page

This guide explains how to update a post resource by adding a new path operation that supports modifying posts.

In this guide, we explain how to update a post resource by adding a new path operation that supports modifying posts. First, we introduce a basic update function that changes a post in an in-memory posts list.

> **lightbulb** Ensure that each code block is tested properly before deploying changes to production.

## Basic Update Function

The following code shows a simple update function that finds a post by its ID and modifies it if it exists:

```python theme={null}
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
```

## Updating the Database

Next, we update our database by grabbing the cursor object and executing an SQL query to update post attributes with the values provided by the user. To mitigate risk due to unpredictable user input, placeholders are used in the query for safely injecting data.

Below is an updated code block that executes an SQL update query. Notice that the `RETURNING` clause in the SQL statement immediately returns the updated record:

```python theme={null}
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s RETURNING""",
        (post.title, post.content, post.published)
    )
    index = find_index_post(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
```

## Fetching the Updated Record

To retrieve the updated post, we need to call `cursor.fetchone()`. The following code snippet demonstrates this operation:

```python theme={null}
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s RETURNING *""",
        (post.title, post.content, post.published)
    )

    index = find_index_post(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_dict = post.dict()
    post_dict['id'] = id
```

After the update, the query result is stored in a variable named `updated_post`. To ensure a successful update, we check if the result is `None` and return a 404 error if no post was updated.

```python theme={null}
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s RETURNING *""",
        (post.title, post.content, post.published)
    )
    updated_post = cursor.fetchall()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
```

At this point, our previous implementation becomes obsolete as we now rely on the updated record returned directly from the database query. If the update operation returns `None`, it indicates that no post with the given ID exists and a 404 error is triggered.

## Finalizing the Update Endpoint

The final version of our update endpoint fetches the updated post directly using `cursor.fetchone()` and returns it. For example, if the database initially contains a post with ID 1 and you run:

```sql theme={null}
select * from posts;
```

You might see output similar to:

```plaintext theme={null}
 id |     title      |         content         | published |        created_at         
----+----------------+-------------------------+-----------+---------------------------
  1 | first post     | some interesting stuff  | true      | 2021-08-21 23:08:39.63312-04
  2 | second post    | yadaydayda              | true      | 2021-08-21 23:08:39.63312-04
```

If you update the post with this JSON payload:

```json theme={null}
{
    "title": "updated title",
    "content": "THIS is the new content"
}
```

The endpoint should return:

```json theme={null}
{
    "data": {
        "id": 1,
        "title": "updated title",
        "content": "THIS is the new content",
        "published": true,
        "created_at": "2021-08-21T23:08:39.631320-04:00"
    }
}
```

After checking the database, you will find that the post has been updated correctly.

> **triangle-alert** The initial update query did not include a WHERE clause, inadvertently updating every post. Always verify that your SQL queries update only the intended record.

To address this bug, add a WHERE condition to target the post with the specified ID. The updated SQL query is as follows:

```python theme={null}
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, str(id))
    )
    updated_post = cursor.fetchone()
    conn.commit()
    
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    return {"data": updated_post}
```

After updating the post, running the following command:

```sql theme={null}
select * from posts;
```

will show that only the specified post is updated, though its position in the result set may change due to the modification. When testing with a non-existent post ID (for example, ID 23), the endpoint correctly returns a 404 error.

## Final Update Endpoint Implementation

Below is the complete and corrected version of the update endpoint:

```python theme={null}
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, str(id))
    )
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    return {"data": updated_post}
```

When testing, you might see log entries similar to:

```plaintext theme={null}
INFO:     Started server process [22924]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
127.0.0.1:52880 - "PUT /posts/1 HTTP/1.1" 200 OK
INFO:     127.0.0.1:53994 - "PUT /posts/23 HTTP/1.1" 200 OK
```

Make sure that existing posts are updated as expected and that non-existent posts return the appropriate 404 error.

## Additional Resources

* [FastAPI Documentation](https://fastapi.tiangolo.com/)
* [PostgreSQL SQL Command Reference](https://www.postgresql.org/docs/current/sql-update.html/)
* [Python DB-API Documentation](https://www.python.org/dev/peps/pep-0249/)

- [Watch Video](https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/1c3ad280-5fee-4b8e-a891-42a61f9a2dd0/lesson/44f218a9-b18f-4837-a97e-259767549c44)
