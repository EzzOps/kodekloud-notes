# Sql Relationship Basics

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Advanced-FastAPI/Sql-Relationship-Basics/page

This article explores establishing relationships in a relational database by connecting a users table with a posts table using foreign keys.

In this article, we explore how to establish relationships within a relational database to connect different tables—in our case, a "users" table and a "posts" table. In many applications, such as social media platforms, a post is always associated with its creator. However, our current setup lacks this connection: users and posts are managed independently without any inherent link between a post and the user account that created it.

When examining the posts table, you'll notice columns such as ID, title, content, published status, and a created\_at timestamp (not shown here). Yet, there is no column that indicates which user created a particular post.

## Establishing Relationships with Foreign Keys

Relational databases excel at forming connections between tables. To associate each post with a specific user, we need to add a new column—commonly called "user\_id"—to the posts table. This column will serve as a foreign key that references the ID column in the users table.

Below is an example SQL statement illustrating how to alter the posts table to add this relationship:

```sql theme={null}
ALTER TABLE posts
ADD COLUMN user_id INTEGER,
ADD CONSTRAINT fk_user
FOREIGN KEY (user_id)
REFERENCES users(id);
```

The foreign key constraint instructs SQL to link the "user\_id" column in the posts table with the "id" column in the users table. By embedding the ID of the user who created the post, the database maintains a clear association between the two tables. For example, if a post with the ID 621 has a user\_id of 212, you can look up the corresponding user in the users table and determine that "[Clay@gmail.com](mailto:Clay@gmail.com)" is the creator of the post.

<Callout icon="lightbulb">
  While the primary key (ID) is typically used as the foreign key target, some advanced database designs might involve referencing columns other than the primary key, tailored to specific business logic and relationship requirements.
</Callout>

## Visualizing the Relationship

The diagram below illustrates the one-to-many relationship between the "users" and "posts" tables. In this relationship, one user can create many posts, but each post is linked to only one user.

<Frame>
  ![The image illustrates a one-to-many relationship between two database tables: "User" and "Posts." The "User" table contains user IDs, emails, and passwords, while the "Posts" table includes post IDs, user IDs, titles, content, and publication status.](https://kodekloud.com/kk-media/image/upload/v1752883341/notes-assets/images/Python-API-Development-with-FastAPI-Sql-Relationship-Basics/user-posts-relationship-diagram.jpg)
</Frame>

When a new post is created, the creator’s user ID is embedded in the "user\_id" column. For example, if another post shows a user\_id of 378, referring to the users table will reveal that "[Mike@gmail.com](mailto:Mike@gmail.com)" created that post.

## Next Steps

In the following section, we will demonstrate how to connect to a PostgreSQL database, create the necessary additional column, enforce the foreign key constraint, and work with these relationships practically.

For further insights, check out:

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

Happy coding!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/ed782f8c-495c-4ff8-8703-c9ab0ab04a4d/lesson/4fd40e34-4fde-4e0d-b6ac-1de773b61953" />
</CardGroup>
