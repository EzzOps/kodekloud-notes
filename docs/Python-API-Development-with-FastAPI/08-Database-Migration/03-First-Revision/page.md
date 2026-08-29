# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from myapp import mymodel
target_metadata = mymodel.Base.metadata

target_metadata = None
```

To work with SQLAlchemy models, update the file to import your base object from your database module. For example:

```python theme={null}
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Then, modify your `env.py` file to import `Base` from your application’s database file. Replace the original metadata configuration with:

```python theme={null}
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.database import Base
from app.config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option(
    "sqlalchemy.url",
    f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata
```

If your models are defined or imported from a different file (e.g., `app.models`), ensure the import reflects that. For instance, to detect changes in a `Post` model:

```python theme={null}
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    # Define additional columns for the User model here.
```

Then, update your `env.py` accordingly:

```python theme={null}
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.models import Base
from app.config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option(
    "sqlalchemy.url",
    f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata
```

This configuration ensures that Alembic can access your SQLAlchemy models and automatically track schema changes.

## Configuring alembic.ini

Within the `alembic.ini` file, specify your SQLAlchemy database URL. Initially, it might appear as follows:

```ini theme={null}
[alembic]
# path to migration scripts
script_location = alembic

# template used to generate migration files
# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
prepend_sys_path = .

# timezone to use when rendering the date
# within the migration file as well as the filename.
# string value is passed to dateutil.tz.gettz()
# leave blank for localtime
# max length of characters to apply to the
sqlalchemy.url = driver://user:pass@localhost/dbname

[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts. See the documentation for further
# detail and examples.
```

Replace the placeholder connection string with your actual database credentials. For example, if you are using PostgreSQL:

```ini theme={null}
sqlalchemy.url = postgresql+psycopg2://postgres:password123@localhost:5432/fastapi
```

> **lightbulb** While the above example hardcodes credentials for demonstration purposes, it is advisable to manage sensitive information using environment variables in production.

## Overriding the Database URL in env.py

To avoid hardcoding credentials within `alembic.ini`, you can override the SQLAlchemy URL directly in `env.py` using values from your configuration file. For example:

```python theme={null}
from alembic import context
from app.database import Base
from app.config import settings
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool

# this is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config
config.set_main_option(
    "sqlalchemy.url",
    f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata
```

This method allows you to securely manage database credentials using environment variables. A typical Pydantic settings class defined in `config.py` might resemble:

```python theme={null}
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"
```

You can then use these settings in your main application as follows:

```python theme={null}
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

print(settings.database_username)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
```

## Final Remarks

After completing these configurations, Alembic will be connected to your PostgreSQL database and ready to detect changes in your SQLAlchemy models. This setup streamlines the process of generating migration scripts and applying database updates.

To create and run migrations, use the following commands:

```bash theme={null}
alembic revision --autogenerate -m "Your migration message"
alembic upgrade head
```

Happy migrating!

- [Watch Video](https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/a6a7b30d-5ca7-4d69-a323-c508340e9931/lesson/3ad8ae82-a1b2-4e6c-b89a-b2bae924f121)


# First Revision

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Database-Migration/First-Revision/page

This article demonstrates managing PostgreSQL database changes using Alembic, including creating tables and handling migrations step-by-step.

In this article, we demonstrate how to manage PostgreSQL database changes using Alembic. Initially, our database was empty, with no defined tables:

```sql theme={null}
SELECT * FROM public.posts
ORDER BY id ASC
```

We started building our application by creating tables directly in the PostgreSQL database as required. For instance, during the early stages, we created a "posts" table without handling user creation, password hashing, or establishing user relationships. Later, with the implementation of CRUD operations for posts and the introduction of user registration, we added a "users" table and modified the "posts" table to include a foreign key. Eventually, a "votes" table was added, complete with its own set of foreign keys.

Now, with Alembic integrated into our workflow, we will walk through a controlled, step-by-step process to manage these database migrations.

## Exploring Alembic Commands

Begin by reviewing the available Alembic commands. Running the help command:

```bash theme={null}
alembic --help
```

displays multiple options. One of the most frequently used options is the `revision` command, which is similar to a git commit message. It allows you to attach a human-readable message to each schema change.

For example, to create a revision for the posts table, run:

```bash theme={null}
alembic revision -m "create posts table"
```

This command generates a new file in the Alembic versions folder. The output will resemble:

```plaintext theme={null}
Generating C:\Users\sanje\Documents\Courses\fastapi\alembic\versions\cfcc4fd02d18_create_posts_table.py .
```

Inside this generated file, you will see a structure similar to the following:

```python theme={null}
from alembic import op
import sqlalchemy as sa
