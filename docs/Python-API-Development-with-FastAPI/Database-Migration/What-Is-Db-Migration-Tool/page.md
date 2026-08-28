# revision identifiers, used by Alembic.
revision = '01b2584928a5'
down_revision = 'ccfc4fd02d18'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass

def downgrade():
    op.drop_column('posts', 'content')
    pass
```

When you run the upgrade, the log output might look like this:

```plaintext theme={null}
INFO [alembic.runtime.migration] Will assume transactional DDL.
INFO [alembic.runtime.migration] Running upgrade -> ccfc4fd02d18, create posts table
Generating C:\Users\sanje\Documents\Courses\fastapi\alembic\versions\01b2584928a5_add_content_column_to_p
done
```

## Verifying the Applied Migration

To ensure the migration has been applied successfully, you can check the current revision using:

```bash theme={null}
(venv) C:\Users\sanje\Documents\Courses\fastapi>alembic current
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
cfcc4fd02d18
```

To view the latest (head) migration, run:

```bash theme={null}
(venv) C:\Users\sanje\Documents\Courses\fastapi>alembic heads
01b2584928a5 (head)
```

Since the latest migration is referred to as the head, upgrade to it by specifying the revision number or simply using "head":

```bash theme={null}
(venv) C:\Users\sanje\Documents\Courses\fastapi>alembic upgrade head
```

After upgrading successfully, verify PostgreSQL table properties using a query like:

```sql theme={null}
SELECT * FROM public.alembic_version
ORDER BY version_num ASC;
```

## Rolling Back a Migration

If you decide that the "content" column is no longer needed, you can revert the change using the downgrade function defined in the migration script. To roll back the changes, run:

```bash theme={null}
(venv) C:\Users\sanje\Documents\Courses\fastapi>alembic downgrade cfcc4fd0218
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
```

Alternatively, you can perform a relative downgrade by moving one revision back:

```bash theme={null}
(venv) C:\Users\sanje\Documents\Courses\fastapi>alembic downgrade -1
```

After downgrading, refresh your database client to verify that the "content" column has been removed.

<Callout icon="triangle-alert">
  Before executing a downgrade in a production environment, ensure that you have backed up your database to prevent any accidental data loss.
</Callout>

## Summary

Alembic offers a streamlined way to manage your database schema:

* Create new tables or modify existing ones by writing migrations.
* Apply changes via `alembic upgrade` and roll them back with `alembic downgrade`.

This process provides excellent version control for your database, ensuring that any changes can be easily reversed if necessary.

For further reading, check out these helpful resources:

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/a6a7b30d-5ca7-4d69-a323-c508340e9931/lesson/ee4ed733-0132-42d5-94e7-9abbcb3dcf50" />
</CardGroup>


# What Is Db Migration Tool

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Database-Migration/What-Is-Db-Migration-Tool/page

This article explores SQLAlchemys limitations in evolving database schemas and introduces Alembic as a tool for automating and streamlining schema updates.

In this article, we explore the limitations of SQLAlchemy when evolving database schemas and introduce Alembic—a powerful database migration tool that automates and streamlines schema updates.

***

## SQLAlchemy Model Definitions and Their Limitations

Consider the following SQLAlchemy models:

```python theme={null}
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
```

When your application starts, SQLAlchemy uses these definitions to create the corresponding tables in the PostgreSQL database if they do not already exist. Below is a sample console output indicating a successful startup:

```plaintext theme={null}
INFO: Application startup complete.
WARNING: WatchGodReload detected file change in 'C:\Users\sanje\Documents\Courses\fastapi\app\models.py': 915f4585d116cdbbab211f73e5527481.tmp'. Reloading...
INFO: Started server process [26152]
INFO: Waiting for application startup.
INFO: Application startup complete.
```

However, SQLAlchemy does not accommodate modifications to the schema after the tables are created. For instance, if you update your model definitions by adding new columns, deleting columns, or altering constraints, SQLAlchemy will not modify the existing tables. Even if the models are updated with the same definitions:

```python theme={null}
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
```

... the logs will still simply show that the application was successfully started:

```plaintext theme={null}
INFO: Application startup complete.
WARNING: WatchGodReload detected file change in 'C:\...\models.py': 915f485d116cbdbaab217f3e5527481.tmp'. Reloading...
INFO: Started server process [26152]
INFO: Waiting for application startup.
INFO: Application startup complete.
```

SQLAlchemy checks for the existence of a table by name, and if it already exists, it does not push any updates. Thus, if you modify your models, the changes will not reflect in the production database unless you manually drop the tables and restart your application.

<Callout icon="triangle-alert">
  Manually dropping tables in a production environment is not a viable strategy for managing schema updates.
</Callout>

***

## Demonstrating the Schema Limitation

Suppose you add a new column to the **User** model for demonstration purposes:

```python theme={null}
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number = Column(String)

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
```

Even after saving and reloading the application, SQLAlchemy will not update the PostgreSQL table to include the new `phone_number` column. When inspecting the **users** table in pgAdmin, the new column is missing:

<Frame>
  ![The image shows a pgAdmin interface with a table structure for "users," displaying columns for id, email, password, and created\_at, along with their data types and constraints. The left panel shows a database schema with various tables and functions.](https://kodekloud.com/kk-media/image/upload/v1752883382/notes-assets/images/Python-API-Development-with-FastAPI-What-Is-Db-Migration-Tool/pgadmin-users-table-structure.jpg)
</Frame>

***

## Introducing Alembic: A Database Migration Tool

To overcome these limitations, Alembic automates database migrations by updating your database schema in line with your SQLAlchemy models. With Alembic you can:

* Automatically update columns based on model changes.
* Track incremental changes to your schema over time.
* Roll back changes to any previous state with simple commands.

For example, when you update the **User** model to include the `phone_number` column, Alembic can generate and execute the necessary migration scripts to update your PostgreSQL database. Here is the updated model:

```python theme={null}
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number = Column(String)

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
```

After incorporating Alembic, you might see console output similar to the following, indicating the detection of changes and the application of migrations:

```plaintext theme={null}
INFO: Application startup complete.
WARNING: WatchGodReload detected file change in 'C:\Users\sanje\Documents\Courses\fastapi\app\models.py': 915f485d116cbdbba21f73e5527481.tmp'. Reloading...
INFO: Started server process [11820]
INFO: Waiting for application startup.
INFO: Application startup complete.
```

Alembic not only updates your schema automatically but also integrates smoothly with version control systems like Git, giving teams the flexibility to roll back to previous schema versions if needed.

***

## Summary

In this article, we discussed how SQLAlchemy creates database tables using model definitions but does not support automatic schema changes in an existing database. This limitation can force developers into undesirable practices like dropping tables—a risky approach in production environments.

Alembic addresses these challenges by automating database migrations. It reads your SQLAlchemy models, generates migration scripts, and applies incremental changes to keep your database schema synchronized with your codebase, all while offering robust versioning and rollback capabilities.

In upcoming lessons, we will delve deeper into Alembic—covering installation, configuration, and advanced usage for managing database migrations effectively.

***

## Related Resources

* [Alembic Documentation](https://alembic.sqlalchemy.org/)
* [SQLAlchemy Documentation](https://www.sqlalchemy.org/)
* [FastAPI Official Site](https://fastapi.tiangolo.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/a6a7b30d-5ca7-4d69-a323-c508340e9931/lesson/0ebc75ed-6e41-4876-a453-feeb958d1a78" />
</CardGroup>
