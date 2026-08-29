# Creating Votes Table Pgadmin

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Advanced-FastAPI/Creating-Votes-Table-Pgadmin/page

Learn to create a votes table in pgAdmin using PostgreSQL commands and SQLAlchemy, including defining foreign key constraints for referential integrity.

In this lesson, you'll learn how to create a new votes table in pgAdmin using standard PostgreSQL commands and later through SQLAlchemy. We'll also cover defining foreign key constraints to enforce referential integrity.

***

## Step 1: Verifying the Existing Posts Table

Before adding the votes table, verify the contents of the existing posts table by executing the following query:

```sql theme={null}
SELECT * FROM posts;
```

***

## Step 2: Creating the Votes Table

Within the tables section of pgAdmin, create a new table called "votes." Define the following columns:

* **post\_id**: Stores the associated post's ID.
* **user\_id**: Stores the ID of the user casting the vote.

Both columns should be of integer type. Configure these columns as a composite primary key to ensure that each combination of post\_id and user\_id remains unique.

***

## Step 3: Defining Foreign Key Constraints

Establish foreign key constraints to maintain proper relationships among tables.

### Adding the Foreign Key for post\_id

Set a foreign key constraint on the post\_id column so it references the ID column in the posts table. Be sure to apply the "ON DELETE CASCADE" rule, which ensures that deleting a post will also remove its associated votes.

<Frame>
  ![The image shows a pgAdmin interface where a table is being created with columns for "post\_id" and "user\_id," both set as integers and primary keys. The interface includes a database schema with tables and other database objects visible on the left.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883319/notes-assets/images/Python-API-Development-with-FastAPI-Creating-Votes-Table-Pgadmin/pgadmin-table-creation-post-user-id.jpg)
</Frame>

During configuration, select the local column (post\_id) in the votes table and reference it to the ID column in the posts table. If an error occurs stating that the columns for the foreign key need specification, double-check that you have correctly selected the referencing column.

<Frame>
  ![The image shows a pgAdmin interface where a user is attempting to create a foreign key constraint in a PostgreSQL database table. An error message indicates that columns for the foreign key need to be specified.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883322/notes-assets/images/Python-API-Development-with-FastAPI-Creating-Votes-Table-Pgadmin/pgadmin-foreign-key-error-postgresql.jpg)
</Frame>

### Adding the Foreign Key for user\_id

Next, add a foreign key constraint for the user\_id column, setting it to reference the ID column in the users table. Again, configure the "ON DELETE CASCADE" rule to ensure that deleting a user also removes the associated votes.

<Frame>
  ![The image shows a pgAdmin interface with a table creation window open, focusing on setting a foreign key constraint for a database table. The left panel displays a database schema with tables and other database objects.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883325/notes-assets/images/Python-API-Development-with-FastAPI-Creating-Votes-Table-Pgadmin/pgadmin-table-creation-foreign-key.jpg)
</Frame>

After configuring both foreign keys, save your changes.

***

## Step 4: Verifying and Testing the Votes Table

To review the data in the votes table, right-click on the table in pgAdmin and select "View/Edit Data." You can also open a new query window and execute the following SQL command to display the votes ordered by post\_id and user\_id:

```sql theme={null}
SELECT * FROM public.votes
ORDER BY post_id ASC, user_id ASC;
```

Additionally, re-run these queries to check the contents of the posts and users tables:

```sql theme={null}
SELECT * FROM posts;

SELECT * FROM users;
```

<Callout icon="lightbulb">
  When testing, try inserting a vote using valid post and user IDs (for example, post ID 10 and user ID 21) to ensure that the entry is successful. Conversely, attempt an insertion with an invalid post or user ID to confirm that the foreign key constraints properly prevent the entry. Leaving any foreign key field blank should trigger an error.
</Callout>

If you experience any issues while editing data (such as input bugs within pgAdmin), use the "View/Edit Data" feature for a smoother experience.

***

## Next Steps

After confirming that the votes table functions correctly, you can remove it if it was created solely for testing purposes. In the next lesson, you will learn how to define your model in SQLAlchemy so that the framework can automatically generate the table as part of your application development.

Happy coding!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/ed782f8c-495c-4ff8-8703-c9ab0ab04a4d/lesson/c52cec63-de1e-4078-b109-bc9026e494fc" />
</CardGroup>
