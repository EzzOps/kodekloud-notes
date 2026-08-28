# Database configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=express_login_demo
DB_USER=your_db_user
DB_PASSWORD=your_db_password
```

Create directories for configuration and routes:

```bash theme={null}
mkdir -p config routes
```

config/database.js (Postgres connection using pg)

```javascript theme={null}
const { Pool } = require('pg');

const pool = new Pool({
  host: process.env.DB_HOST,
  port: Number(process.env.DB_PORT || 5432),
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
});

pool.on('connect', () => {
  console.log('Connected to PostgreSQL database');
});

pool.on('error', (err) => {
  console.error('Unexpected error on idle client', err);
  process.exit(-1);
});

module.exports = pool;
```

schema.sql (table for users)

```sql theme={null}
-- Connect to database: \c express_login_demo
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

routes/auth.js (POST /api/auth/login)

```javascript theme={null}
const express = require('express');
const { body, validationResult } = require('express-validator');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const pool = require('../config/database');

const router = express.Router();

router.post(
  '/login',
  [
    body('email').isEmail().withMessage('Valid email is required'),
    body('password').isLength({ min: 8 }).withMessage('Password must be at least 8 characters'),
  ],
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { email, password } = req.body;

    try {
      const { rows } = await pool.query('SELECT id, email, name, password_hash FROM users WHERE email = $1', [email]);

      if (rows.length === 0) {
        return res.status(401).json({ message: 'Invalid credentials' });
      }

      const user = rows[0];

      const passwordMatch = await bcrypt.compare(password, user.password_hash);
      if (!passwordMatch) {
        return res.status(401).json({ message: 'Invalid credentials' });
      }

      const token = jwt.sign(
        { id: user.id, email: user.email },
        process.env.JWT_SECRET,
        { expiresIn: process.env.JWT_EXPIRES_IN || '24h' }
      );

      return res.json({
        token,
        user: { id: user.id, email: user.email, name: user.name },
      });
    } catch (err) {
      console.error('Database error:', err);
      return res.status(503).json({ message: 'Database unavailable' });
    }
  }
);

module.exports = router;
```

server.js (main app wiring)

```javascript theme={null}
const express = require('express');
const dotenv = require('dotenv');
const authRoutes = require('./routes/auth');

dotenv.config();

const app = express();
app.use(express.json());

app.use('/api/auth', authRoutes);

// Generic error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ message: 'Internal server error' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
```

Status-code guidance (common HTTP status codes used here)

| Status Code | Use Case                                   |
| ----------- | ------------------------------------------ |
| 400         | Validation errors (bad input)              |
| 401         | Invalid credentials / unauthorized         |
| 503         | Database connection or service unavailable |
| 500         | Generic server error                       |

To use the endpoint: set up your PostgreSQL database, configure credentials in `.env`, run `schema.sql` to create the `users` table, install dependencies (`npm install`), and start the server (`npm start` or `npm run dev`).

## Prompt-writing formula: Context → Action → Details → Examples

Use a concise formula to craft prompts that minimize follow-up:

* Context: Describe the environment or codebase (stack, existing endpoints, naming conventions, constraints).
* Action: Exactly what you want done (for example, "Create POST /api/auth/login endpoint").
* Details: Validation rules, libraries to use, security requirements, response shapes, and error handling.
* Examples: Provide sample request/response payloads or short output examples to set expectations.

<Callout icon="lightbulb">
  Tip: Put the most important constraints (stack, required libraries, validation rules, and response format) at the start of the prompt. Spending a minute to write a clear, complete prompt often saves 10+ minutes of revision.
</Callout>

## The three C's of good prompts

* Clear: Avoid ambiguity and name the exact behavior you expect.
* Complete: Include all requirements and constraints up front.
* Contextual: Provide relevant background—existing patterns, environment, or architecture decisions.

When your prompt is clear, complete, and contextual and includes a short example of expected output, the assistant will produce focused, usable code with minimal rework.

## Summary

* Vague prompts invite incorrect assumptions—be explicit about stack, validation, security, and response formats.
* Use the Context → Action → Details → Examples structure to make prompts actionable and reproducible.
* Follow the three C's: Clear, Complete, Contextual.
* Small time invested in writing a good prompt yields faster, more secure, and more maintainable results.

## Links and references

* Express.js: [https://expressjs.com/](https://expressjs.com/)
* express-validator: [https://express-validator.github.io/](https://express-validator.github.io/)
* bcrypt: [https://www.npmjs.com/package/bcrypt](https://www.npmjs.com/package/bcrypt)
* jsonwebtoken (JWT): [https://www.npmjs.com/package/jsonwebtoken](https://www.npmjs.com/package/jsonwebtoken)
* node-postgres (pg): [https://node-postgres.com/](https://node-postgres.com/)
* PostgreSQL documentation: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)

You can also consult these guides for deeper prompt-engineering and best practices:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) (for learning deployment patterns)
* Docker Hub: [https://hub.docker.com/](https://hub.docker.com/)
* Terraform Registry: [https://registry.terraform.io/](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/3e896e50-3c07-4fdc-8603-bf125255d0a9/lesson/315966b6-3aff-4359-8d16-256590ea9599" />
</CardGroup>


# Demo Context Management Techniques

Source: https://notes.kodekloud.com/docs/Cline/Core-Workflows-Prompt-Engineering/Demo-Context-Management-Techniques/page

Demonstrates using focused context management to safely refactor a FastAPI casting lookup API, removing write endpoints and guiding an AI assistant to make minimal, reliable changes.

In this lesson we demonstrate context management techniques for safely refactoring APIs and guiding an AI assistant to make focused, minimal changes to a codebase. Using a small FastAPI example (a casting number lookup API), you'll see why starting with a narrow context—one file or a few adjacent files—usually produces more reliable results than feeding the tool the entire repository.

We’ll cover:

* The dataset the API serves (CSV excerpt)
* The existing endpoints in the route file
* How to instruct the AI to remove write endpoints (POST/PUT/DELETE)
* A minimal, cleaned `casting.py` after the change
* Verifying the result in Swagger/OpenAPI and with curl
* Notes on related dependencies (SQLAlchemy, Pydantic)

Resources

* FastAPI: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
* Swagger / OpenAPI UI: [https://swagger.io/tools/swagger-ui/](https://swagger.io/tools/swagger-ui/)
* SQLAlchemy: [https://www.sqlalchemy.org/](https://www.sqlalchemy.org/)
* Pydantic v2: [https://docs.pydantic.dev/latest/](https://docs.pydantic.dev/latest/)

CSV sample (excerpt)

```csv theme={null}
Years,Casting,CID,Low Power,High Power,Main Caps,Comments,
1956-67,3849839,283,-,-,2,,
1956-67,3849935,283,-,-,2,,
1964-67,3858174,327,-,-,2,"car, truck",
1968-76,3855961,350,-,-,2,car,
1964-67,3858174,327,275,350,2,"Full, A & Y",
1964-67,3858180,327,250,300,2,,
1962-67,3858190,327,-,-,2,,
1965-67,3862194,283,195,220,2,Chevy II,
1962-66,3864812,283,230,-,2,"car, truck",
1964-67,3868657,327,300,-,2,,
1962-67,3876132,327,-,-,2,,
1963,3889935,283,-,-,2,truck,
1967,3892657,302,290,290,2,"Z-28, small journal",
1967,3892657,327,210,350,2,car & truck,
1967,3892657,350,295,295,2,Camaro,
1968-69,3892659,327,210,-,2,,
1967,3896944,283,195,195,2,replaced by 307 in 68,
1967,3896948,283,195,195,2,identical to 3834810,
1967,3903352,327,210,350,2,cars only,
1969-80,3911460,350,-,-,2,A,
1968-73,3914635,307,-,-,2,car,
1968,3914636,307,200,200,2,car & truck,
1968-69,3914638,327,-,-,2,,
1968-73,3914653,307,-,-,2,A,
```

Goal: Make the API read-only for production or third-party consumption (expose only GET endpoints: list, get-by-casting-number, and search). Rather than hand-editing many files, we’ll show how to limit the AI’s context to the relevant endpoint file and any directly related files.

Existing route file (example)

* File: `app/api/endpoints/casting.py`
* This is the starting point for the AI assistant; it includes GET, POST, PUT, DELETE, and SEARCH routes.

```python theme={null}
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.casting import Casting as CastingModel
from app.schemas.casting import Casting, CastingCreate, CastingUpdate

router = APIRouter()

@router.get("/", response_model=List[Casting])
def get_castings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of castings with pagination.
    """
    castings = db.query(CastingModel).offset(skip).limit(limit).all()
    return castings


@router.get("/{casting_id}", response_model=Casting)
def get_casting_by_id(
    casting_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific casting by its casting number.
    """
    casting = db.query(CastingModel).filter(
        CastingModel.casting == casting_id
    ).first()
    if casting is None:
        raise HTTPException(
            status_code=404,
            detail=f"Casting with number {casting_id} not found"
        )
    return casting


@router.post("/", response_model=Casting)
def create_casting(
    casting: CastingCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new casting.
    """
    db_casting = db.query(CastingModel).filter(
        CastingModel.casting == casting.casting
    ).first()

    if db_casting:
        raise HTTPException(
            status_code=400,
            detail=f"Casting with number {casting.casting} already exists"
        )

    db_casting = CastingModel(**casting.dict())
    db.add(db_casting)
    db.commit()
    db.refresh(db_casting)
    return db_casting


@router.put("/{casting_id}", response_model=Casting)
def update_casting(
    casting_id: str,
    casting: CastingUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing casting.
    """
    db_casting = db.query(CastingModel).filter(
        CastingModel.casting == casting_id
    ).first()
    if db_casting is None:
        raise HTTPException(status_code=404, detail="Not found")

    for key, value in casting.dict(exclude_unset=True).items():
        setattr(db_casting, key, value)
    db.add(db_casting)
    db.commit()
    db.refresh(db_casting)
    return db_casting


@router.delete("/{casting_id}", response_model=Casting)
def delete_casting(
    casting_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a casting.
    """
    db_casting = db.query(CastingModel).filter(
        CastingModel.casting == casting_id
    ).first()

    if db_casting is None:
        raise HTTPException(
            status_code=404,
            detail=f"Casting with number {casting_id} not found"
        )

    db.delete(db_casting)
    db.commit()
    return db_casting


@router.get("/search/", response_model=List[Casting])
def search_castings(
    years: Optional[str] = None,
    cid: Optional[int] = None,
    main_caps: Optional[str] = None,
    comments: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Search for castings based on various criteria.
    """
    query = db.query(CastingModel)

    if years:
        query = query.filter(CastingModel.years.ilike(f"%{years}%"))
    if cid:
        query = query.filter(CastingModel.cid == cid)
    if main_caps:
        query = query.filter(CastingModel.main_caps.ilike(f"%{main_caps}%"))
    if comments:
        query = query.filter(CastingModel.comments.ilike(f"%{comments}%"))

    results = query.offset(skip).limit(limit).all()
    return results
```

Which endpoints do we want to remove?

* POST /api/castings/ — create\_casting
* PUT /api/castings/ — update\_casting
* DELETE /api/castings/ — delete\_casting

Summary: endpoints before vs. after

| Endpoint                            |   Before | After     |
| ----------------------------------- | -------: | :-------- |
| `GET /api/castings/`                |   ✅ list | ✅ list    |
| `GET /api/castings/{casting_id}`    |    ✅ get | ✅ get     |
| `GET /api/castings/search/`         | ✅ search | ✅ search  |
| `POST /api/castings/`               | ✅ create | ❌ removed |
| `PUT /api/castings/{casting_id}`    | ✅ update | ❌ removed |
| `DELETE /api/castings/{casting_id}` | ✅ delete | ❌ removed |

Minimal, cleaned `casting.py`

* Remove the write route handlers and the now-unused schema imports (`CastingCreate`, `CastingUpdate`).
* Leaving only read/search routes keeps the OpenAPI surface minimal and easier to audit.

```python theme={null}
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.casting import Casting as CastingModel
from app.schemas.casting import Casting

router = APIRouter()

@router.get("/", response_model=List[Casting])
def get_castings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of castings with pagination.
    """
    castings = db.query(CastingModel).offset(skip).limit(limit).all()
    return castings


@router.get("/{casting_id}", response_model=Casting)
def get_casting_by_id(
    casting_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific casting by its casting number.
    """
    casting = db.query(CastingModel).filter(
        CastingModel.casting == casting_id
    ).first()

    if casting is None:
        raise HTTPException(
            status_code=404,
            detail=f"Casting with number {casting_id} not found"
        )

    return casting


@router.get("/search/", response_model=List[Casting])
def search_castings(
    years: Optional[str] = None,
    cid: Optional[int] = None,
    main_caps: Optional[str] = None,
    comments: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Search for castings based on various criteria.
    """
    query = db.query(CastingModel)

    if years:
        query = query.filter(CastingModel.years.ilike(f"%{years}%"))
    if cid:
        query = query.filter(CastingModel.cid == cid)
    if main_caps:
        query = query.filter(CastingModel.main_caps.ilike(f"%{main_caps}%"))
    if comments:
        query = query.filter(CastingModel.comments.ilike(f"%{comments}%"))

    results = query.offset(skip).limit(limit).all()
    return results
```

API docs (Swagger/OpenAPI)
Below is the same screenshot used in the original workflow showing GET/POST/PUT/DELETE entries. After removing the write routes and unused imports, the Swagger UI should show only the GET endpoints (list, get-by-id, search, and the root).

<Frame>
  <img alt="A screenshot of a web-based API documentation page (Swagger/OpenAPI) titled &#x22;Casting Number Lookup API,&#x22; showing colored endpoint entries (GET, POST, PUT, DELETE) for /api/castings/ and related routes. The page also shows a default root GET and a Schemas section listing casting-related objects." />
</Frame>

Run the server and verify the OpenAPI document
Example server logs after starting the FastAPI app (condensed):

```text theme={null}
INFO:     Started server process [18745]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:54624 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:54624 - "GET /openapi.json HTTP/1.1" 200 OK
```

Try the read endpoints with curl

Get a casting by number:

```bash theme={null}
curl -X 'GET' \
  'http://0.0.0.0:8000/api/castings/3896944' \
  -H 'accept: application/json'
```

Example JSON response:

```json theme={null}
{
  "casting": "3896944",
  "years": "1967",
  "cid": 283,
  "low_power": "195",
  "high_power": "195",
  "main_caps": "2",
  "comments": "replaced by 307 in 68",
  "id": 58
}
```

Another lookup:

```bash theme={null}
curl -X 'GET' \
  'http://0.0.0.0:8000/api/castings/3862194' \
  -H 'accept: application/json'
```

Response:

```json theme={null}
{
  "casting": "3862194",
  "years": "1965-67",
  "cid": 283,
  "low_power": "195",
  "high_power": "220",
  "main_caps": "2",
  "comments": "Chevy II",
  "id": 51
}
```

Database session dependency (reference)
Typical SQLAlchemy setup used in this example:

```python theme={null}
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
