# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./castings.db"

# Create SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Pydantic v2 note
Pydantic v2 changed model configuration keys. If you see warnings about `orm_mode`, update your schema models to use `from_attributes=True` in Pydantic v2 model configs. See the Pydantic migration guide for details: [https://docs.pydantic.dev/latest/](https://docs.pydantic.dev/latest/)

Best practices when using an AI assistant to refactor

* Start with a narrow context: provide the single target file (e.g., `app/api/endpoints/casting.py`) first.
* Be explicit about the desired change (e.g., “remove POST/PUT/DELETE endpoints and unused schema imports”).
* If the AI needs more context, iteratively provide only the adjacent files it imports (schemas, models, and the DB dependency), not the entire repo.
* Re-run your tests and check the Swagger/OpenAPI UI after edits to confirm only the intended endpoints are exposed.

Key takeaways

* Start small: give the AI one or a few files that are directly relevant to the change you want.
* Be explicit about what you want removed or changed (e.g., remove POST/PUT/DELETE).
* Verify that unused imports are removed (e.g., schema types you no longer use).
* Check Swagger/OpenAPI after the edit to confirm the intended surface is exposed.
* If needed, gradually add more context (related modules, terminal output, or recent git commits) until the AI has enough information.

> **lightbulb** Start with a single, focused file as context (e.g., `casting.py`). If the AI's edits are incomplete, iteratively add only the adjacent files it imports (schemas, models, or database) rather than the entire repository. Smaller, relevant context often produces more reliable edits.

- [Watch Video](https://learn.kodekloud.com/user/courses/cline/module/23f587ab-5d25-46ca-98cd-26fe001682a0/lesson/19eb502a-748d-4c1b-83b8-f30c6df0e91a)


# Demo Prompt Anatomy and Best Practices

Source: https://notes.kodekloud.com/docs/Cline/Core-Workflows-Prompt-Engineering/Demo-Prompt-Anatomy-and-Best-Practices/page

Guide to refactoring a casting number lookup app to ingest Chevrolet small‑block CSVs, update models, handle messy CSVs, migrations, and import utilities

This walkthrough takes a deeper look at the Casting Number Lookup project and focuses on prompt engineering techniques, context injection, and using an assistant (Cline) to refactor an application to a new data model. Goal: convert casting numbers (stamped on automotive parts) into structured metadata so you can decide whether to buy a part from a junkyard.

Keywords: casting number lookup, Chevrolet small-block, SQLAlchemy refactor, CSV import, data model migration, FastAPI, Pydantic v2.

We’ll cover:

* The original project and its initial data model
* A real Chevrolet small‑block casting CSV (target dataset)
* Crafting prompts to refactor the app to the new schema
* Running the migration and handling errors
* Validating the refactored API

## Project background and original model

The original SQLAlchemy model used generic fields (material, weight, manufacturer, etc.). That general shape doesn’t match the Chevrolet small‑block casting CSV we want to ingest, which uses fields like Years, Casting, CID, factory power ratings, and notes about main caps or comments.

Original SQLAlchemy model:

```python theme={null}
