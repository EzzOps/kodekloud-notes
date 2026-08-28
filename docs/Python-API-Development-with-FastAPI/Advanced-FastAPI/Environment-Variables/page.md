# Environment Variables

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Advanced-FastAPI/Environment-Variables/page

This guide covers best practices for managing environment variables to enhance application security and adaptability.

In modern application development, it’s crucial to avoid hardcoding sensitive information—such as database credentials and secret keys—directly in your code. Hardcoding makes your application vulnerable to security risks, especially when code is shared or pushed to public repositories like GitHub. Moreover, it complicates deployment across multiple environments (development, staging, production). This guide covers best practices for managing environment variables, ensuring your application remains secure and adaptable.

***

## The Risks of Hardcoding

Embedding sensitive data directly in your source code exposes it to unnecessary risk and limits flexibility. Consider the following Python code snippet:

```python theme={null}
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost/fastapi'

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

Hardcoding the database URL leads to two significant problems:

1. If the code is pushed to a public repository, your credentials are exposed to...

<Callout icon="triangle-alert">
  If the code is pushed to a public repository, your credentials are exposed to everyone.
</Callout>

2. The static configuration ties the code to a single environment, forcing manua...

<Callout icon="triangle-alert">
  The static configuration ties the code to a single environment, forcing manual updates for production deployments.
</Callout>

Similarly, hardcoding OAuth secret keys can lead to security vulnerabilities. For example:

```python theme={null}
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
