# This method is vulnerable to SQL injection and should be avoided.
cursor.execute(f"INSERT INTO posts (title, content, published) VALUES({post.title}, {post.content})")
```

Always use parameterized queries to ensure that values are treated strictly as data. This practice helps safeguard your database from possible SQL injection attacks.

<Callout icon="triangle-alert">
  Never interpolate user inputs directly into SQL queries. Always use parameterized queries to prevent malicious code execution.
</Callout>

***

## 4. Returning the Created Post

It is often useful to return the record that was just created. Many databases support a `RETURNING` clause that allows you to fetch the inserted data immediately. Ensure that the order of values in the tuple matches the order of placeholders. Here’s how you can modify your endpoint:

```python theme={null}
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    return {"data": new_post}
```

***

## 5. Committing the Transaction

After executing the INSERT statement, the changes remain staged until you commit the transaction. Without calling `commit()`, your changes will not be permanently saved in PostgreSQL. The final version of the endpoint includes not only the INSERT operation but also the commit to ensure the database is updated:

```python theme={null}
@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    conn.commit()  # Commit the transaction to save changes in the database.
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )
    return {"data": post}
```

The console outputs during server startup and requests might look similar to the following:

```plaintext theme={null}
INFO:     Started server process [23036]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:51977 - "POST /posts HTTP/1.1" 201 Created
```

***

## 6. Verifying the Insert in pgAdmin

After creating a new post, verify that the record is successfully inserted by running the following SQL query in your database client (e.g., pgAdmin):

```sql theme={null}
SELECT * FROM posts;
```

The results will display the details of the posts, including the newly inserted record.

<Frame>
  ![The image shows the pgAdmin interface connected to a PostgreSQL database, displaying the query editor and database schema details on the left panel.](https://kodekloud.com/kk-media/image/upload/v1752883384/notes-assets/images/Python-API-Development-with-FastAPI-Create-Posts-Sql/pgadmin-postgresql-query-editor-schema.jpg)
</Frame>

***

## 7. Committing via Visual Studio Code

When working within an integrated development environment such as Visual Studio Code, ensure that the transaction is committed by invoking `conn.commit()`. This results in visible output in the terminal confirming that the commit was successful.

<Frame>
  ![The image shows a Visual Studio Code interface with Python code for a FastAPI application. The code editor displays a function definition, and there's an autocomplete suggestion box visible.](https://kodekloud.com/kk-media/image/upload/v1752883385/notes-assets/images/Python-API-Development-with-FastAPI-Create-Posts-Sql/visual-studio-code-fastapi-python.jpg)
</Frame>

***

By following these best practices—using parameterized SQL queries, retrieving the inserted record with the RETURNING clause, and committing the transaction—you can ensure secure and reliable interactions between your FastAPI application and PostgreSQL database.

For further reading on best practices in SQL operations and FastAPI development, check out the [FastAPI documentation](https://fastapi.tiangolo.com/) and [PostgreSQL documentation](https://www.postgresql.org/docs/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/1c3ad280-5fee-4b8e-a891-42a61f9a2dd0/lesson/4382e166-c165-457e-8287-a7c43116e582" />
</CardGroup>


# Delete Posts Sql

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Databases-with-Python/Delete-Posts-Sql/page

Learn to safely delete a post from a database in a Python API using SQL with parameterized queries to prevent SQL injection.

In this lesson, you will learn how to safely delete a post from a database within a Python API using SQL. This process uses a DELETE statement with a parameterized query, ensuring that user input is properly handled to prevent SQL injection. The SQL statement also incorporates a RETURNING clause to retrieve the details of the post before it is deleted, which can be useful for validation and logging purposes.

<Callout icon="lightbulb">
  Converting the post ID to a string and including an extra comma in the parameter tuple is essential for preventing errors during query execution.
</Callout>

Below is the updated Python code for the DELETE endpoint:

```python theme={null}
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),)
    )
    deleted_post = cursor.fetchone()

    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist"
        )

    connection.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```

Once the DELETE operation executes successfully, you can verify the remaining posts in the database with a simple SQL query. For example:

```sql theme={null}
select * from posts;
```

Assume that before deletion, the database contains posts with IDs 1, 2, and 4. When the DELETE endpoint is called for the post with ID 4, the API will return a 204 No Content status, indicating a successful deletion.

Here is an example of the JSON response from a GET request that displays the details of the post with ID 4 before deletion:

```json theme={null}
{
    "post_detail": {
        "id": 4,
        "title": "hey this is my new post",
        "content": "something somethng beaches",
        "published": true,
        "created_at": "2021-08-21T23:34:18.169728-04:00"
    }
}
```

After the deletion operation, the console output confirms that the database connection was successful:

```plaintext theme={null}
Database connection was successful!
```

If you attempt to delete the post with ID 4 again, the API returns a 404 error with a message stating that the post does not exist. This precaution ensures that the client is informed of any attempts to delete non-existent resources, thereby maintaining the integrity of the application.

<Callout icon="lightbulb">
  Using clear, structured steps and code examples not only assists developers in understanding the process but also improves the page's SEO by including relevant keywords like "Python API", "SQL DELETE", and "safe database operations".
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/1c3ad280-5fee-4b8e-a891-42a61f9a2dd0/lesson/1bf3969e-7e12-4061-8817-e993a7b4c68a" />
</CardGroup>
