# revision identifiers, used by Alembic.
revision = 'cfcc4fd02d18'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    pass

def downgrade():
    pass
```

<Callout icon="lightbulb">
  The `upgrade()` function is used to apply changes, while the `downgrade()` function allows you to roll back those changes. Always add the necessary logic to these functions based on your migration requirements.
</Callout>

To explore more options for the `alembic revision` command, run:

```bash theme={null}
alembic revision --help
```

Some key options include:

| Option         | Description                                     |
| -------------- | ----------------------------------------------- |
| `-m`           | Specify the migration message                   |
| `--rev-id`     | Provide a hardcoded revision identifier         |
| `--depends-on` | Define dependencies between different revisions |

## Creating the Posts Table

After creating the revision file, add the logic to create the posts table in the `upgrade()` function. We'll define two essential columns:

* An `id` column of type `Integer`, which is non-nullable and serves as the primary key.
* A `title` column of type `String`, also non-nullable.

Below is the updated migration script:

```python theme={null}
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'cfcc4fd02d18'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False)
    )

def downgrade():
    op.drop_table('posts')
```

After saving the migration file, apply the latest revision by running:

```bash theme={null}
alembic upgrade <revision_id>
```

Replace `<revision_id>` with your revision identifier (e.g., `cfcc4fd02d18`). Alternatively, you can upgrade to the latest revision using:

```bash theme={null}
alembic upgrade head
```

This command applies the migration, creating the posts table. Verify the changes by refreshing your PostgreSQL interface with:

```sql theme={null}
SELECT * FROM public.posts
ORDER BY id ASC
```

You should now see that the posts table includes two columns: `id` (the primary key, non-nullable) and `title` (non-nullable).

<Frame>
  ![The image shows a Visual Studio Code interface with Python code for a database migration script using Alembic. The code editor displays a function definition, and a tooltip provides information about the Operations class.](https://kodekloud.com/kk-media/image/upload/v1752883379/notes-assets/images/Python-API-Development-with-FastAPI-First-Revision/vscode-python-database-migration-alembic.jpg)
</Frame>

Additionally, when you inspect the table in pgAdmin, the defined columns and associated constraints are clearly visible:

<Frame>
  ![The image shows a pgAdmin interface with a table named "posts" being edited. It displays columns for "id" and "title" with their data types and constraints.](https://kodekloud.com/kk-media/image/upload/v1752883380/notes-assets/images/Python-API-Development-with-FastAPI-First-Revision/pgadmin-posts-table-edit-interface.jpg)
</Frame>

## Tracking Migrations with Alembic

Alembic maintains a version table in your database that keeps track of all applied revisions. To inspect this version table, execute:

```sql theme={null}
SELECT * FROM public.alembic_version
ORDER BY version_num ASC
```

<Callout icon="triangle-alert">
  Do not delete the Alembic versioning table. It is crucial for tracking schema changes and ensuring the consistency of your database migrations.
</Callout>

## Conclusion

This guide demonstrated how to create a simple "posts" table using Alembic, including both the upgrade and downgrade migration paths. For additional operations—such as altering columns, adding constraints, or working with computed defaults—refer to the [Alembic API documentation](https://alembic.sqlalchemy.org/en/latest/).

By managing database migrations with Alembic, you ensure a controlled and consistent way to apply schema changes, making your database evolution both predictable and reversible.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/a6a7b30d-5ca7-4d69-a323-c508340e9931/lesson/6eb4e2de-24b7-4f45-a269-1cd0eecac8fb" />
</CardGroup>


# Rollback Alembic

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Database-Migration/Rollback-Alembic/page

This article explains how to create, modify, and roll back database tables using Alembic migrations for effective schema management.

In this article, we will walk through the process of creating and modifying database tables using Alembic migrations and how to roll back those changes when needed. This guide is ideal for developers looking to manage database schema changes in a seamless manner.

## Creating the Initial Table

Initially, we created our first table using an Alembic revision. The following migration script creates a "posts" table:

```python theme={null}
def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False)
    )
    pass

def downgrade():
    op.drop_table('posts')
```

When you run this migration, you may see output similar to the following:

```plaintext theme={null}
alembic: error: unrecognized arguments: ccfc4f0d2d18
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade -> ccfc4f0d2d18, create posts table
```

<Callout icon="lightbulb">
  Ensure your Alembic configuration is set correctly to avoid unrecognized argument errors.
</Callout>

## Modifying the Table: Adding a New Column

After reviewing our application models, we decided to add a new column called "content" to the "posts" table. First, update your SQLAlchemy model as shown below:

```python theme={null}
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, ondelete="CASCADE")
```

Next, generate a new Alembic revision with an informative message:

```bash theme={null}
(venv) C:\Users\sanje\Documents\Courses\fastapi>alembic revision -m "add content column to posts table"
```

This command creates a new migration file. You then need to define the upgrade and downgrade logic to add this column. Below is an example revision file for this change:

```python theme={null}
