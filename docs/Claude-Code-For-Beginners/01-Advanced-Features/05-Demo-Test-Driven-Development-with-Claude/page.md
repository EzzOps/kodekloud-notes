# --- Configuration (replace or adapt to parse CLI args) ---
MYSQL_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "jeremy",
    "password": "password123",
    "database": "contactsdb",
}
SQLITE_PATH = "contacts.db"
TABLE_NAME = "contacts"
def create_sqlite_table(conn):
    # Approximate schema mapping for the known contacts table
    conn.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        job_title TEXT,
        email TEXT NOT NULL UNIQUE
    );
    """)
    conn.commit()

def migrate():
    # Connect to MariaDB
    mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
    mysql_cursor = mysql_conn.cursor(dictionary=True)

    # Connect to SQLite
    sqlite_conn = sqlite3.connect(SQLITE_PATH)
    create_sqlite_table(sqlite_conn)
    sqlite_cur = sqlite_conn.cursor()

    # Read rows from MariaDB and insert into SQLite using parameterized queries
    mysql_cursor.execute(f"SELECT id, first_name, last_name, job_title, email FROM {TABLE_NAME}")
    rows = mysql_cursor.fetchall()
    insert_sql = "INSERT OR REPLACE INTO contacts (id, first_name, last_name, job_title, email) VALUES (?, ?, ?, ?, ?)"

    count = 0
    for r in rows:
        sqlite_cur.execute(insert_sql, (r['id'], r['first_name'], r['last_name'], r.get('job_title'), r['email']))
        count += 1

    sqlite_conn.commit()
    mysql_cursor.close()
    mysql_conn.close()
    sqlite_conn.close()
    print(f"Successfully migrated {count} records from MariaDB to SQLite")

if __name__ == "__main__":
    try:
        migrate()
    except Exception as e:
        print("Migration failed:", e, file=sys.stderr)
        sys.exit(1)
```

Tips:

* Expand the script to discover schema programmatically (INFORMATION\_SCHEMA) if migrating multiple or unknown tables.
* Add CLI parsing (click/argparse) and optional logging for production use.
* Optionally write INSERT statements to .sql files for auditing or replay.

## Environment setup

Create and activate a virtual environment, then install the connector:

```bash theme={null}
python3 -m venv migration_env
source migration_env/bin/activate
pip install mysql-connector-python
```

Run the migration:

```bash theme={null}
source migration_env/bin/activate
python migrate.py
```

## Verification

Verify row counts and sample rows after migration.

Row count comparison:

```bash theme={null}
sqlite3 contacts.db "SELECT COUNT(*) as total_records FROM contacts;"
mysql -h localhost -u jeremy -ppassword123 contactsdb -e "SELECT COUNT(*) as total_records FROM contacts;"
# => total_records
#    1000
```

Sample rows from SQLite:

```bash theme={null}
sqlite3 contacts.db "SELECT * FROM contacts LIMIT 5;"
# Example output:
# 1|Britt|Hyne|Senior Editor|bhyne@lulu.com
# 2|Merrel|Cornew|VP Product Management|mcornew1@indiegogo.com
# 3|Emmit|Glasard|Senior Editor|eglasard2@behance.net
```

## Artifacts and repeatability

For repeatability and auditing, keep:

* The migration script (migrate.py),
* The mysqldump (contacts\_data.sql) or generated .sql insert files,
* The detailed prompt or runbook describing how the migration was performed.

These artifacts make the process auditable and allow re-running the migration or adapting it to other tables.

<Frame>
  <img alt="A screenshot of a dark-themed code editor (VS Code) showing a markdown file titled &#x22;detailed-prompt.md&#x22; with step-by-step instructions to generate Python and SQL code to migrate a MariaDB database to SQLite. The left sidebar lists project files (contacts, contacts_data.sql, migrate.py) and a terminal panel is visible along the bottom." />
</Frame>

## Inspect the resulting SQLite database

Open contacts.db in a GUI such as DB Browser for SQLite to inspect schema, indexes, and rows.

<Frame>
  <img alt="A screenshot of a database GUI (DB Browser for SQLite) showing a &#x22;contacts&#x22; table with columns like id, first_name, last_name, job_title, and email. The left pane lists many contact rows while the right pane shows an editor/SQL and database connection controls." />
</Frame>

## Summary and practical notes

* For simple tables, a compact Python script using mysql-connector-python + sqlite3 is reliable and avoids quoting pitfalls.
* For complex schemas (foreign keys, triggers, stored routines), plan for manual mapping or schema redesign; SQLite lacks some MariaDB features.
* Always test migrations in a sandbox and verify row counts and spot-check data.
* Prefer parameterized queries to avoid quoting and injection issues.
* Keep a dump (.sql) or TSV export for auditing and replay.

This migration converted 1,000 contacts from MariaDB (contactsdb.contacts) into a single-file SQLite database (contacts.db) and produced a reproducible migration script suitable for reruns or adaptation.

## Links and references

* [MariaDB Documentation](https://mariadb.org/)
* [SQLite Documentation](https://www.sqlite.org/docs.html)
* [DB Browser for SQLite](https://sqlitebrowser.org/)
* [Kubernetes Documentation — for related infra topics](https://kubernetes.io/docs/)
* [Python mysql-connector-python on PyPI](https://pypi.org/project/mysql-connector-python/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/a295c914-f61e-47bb-8adc-7a3145745aa6/lesson/2189df42-68f7-4b25-9ad9-da5941c626a6" />
</CardGroup>


# Demo Test Driven Development with Claude

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Advanced-Features/Demo-Test-Driven-Development-with-Claude/page

A demo of test-driven development using Claude Code to generate pytest tests and implement a Python unit converter for distance, volume, mass, and temperature

This lesson walks through a practical test-driven development (TDD) example using Claude Code to generate tests and iterate on an implementation. The sample project is a compact unit-converter supporting distance, volume, mass, and temperature conversions.

TDD workflow recap:

* Write tests first.
* Run tests and watch them fail (red).
* Implement the smallest amount of code to make the tests pass (green).
* Refactor while keeping tests green.

When a team consistently applies TDD it reduces regressions and improves long-term velocity. Claude Code can accelerate the mechanical, repetitive parts of TDD such as generating comprehensive test cases.

## Requirements and test expectations

* Every conversion function accepts a single numeric argument (int or float) and returns a float.
* Note: in Python, bool is a subclass of int and will satisfy isinstance(value, (int, float)). If you need to reject booleans (True/False), adjust the input validation accordingly.
* If a non-numeric value is passed, the functions must raise TypeError.
* Tests should cover: integers, floats, zero, negative values, and invalid inputs.
* Use pytest.approx() in tests where floating-point precision matters.

## Conversion formulas and constants

Below is a concise table of the functions, formulas, and precise conversion factors used by the tests and implementation.

| Function                      | Formula / Factor                   | Description                         |
| ----------------------------- | ---------------------------------- | ----------------------------------- |
| miles\_to\_kilometers(miles)  | km = miles \* 1.60934              | 1 mile = 1.60934 kilometers         |
| kilometers\_to\_miles(km)     | miles = km \* 0.621371             | 1 km ≈ 0.621371 miles               |
| gallons\_to\_liters(gallons)  | L = gallons \* 3.785411784         | 1 US gallon = 3.785411784 liters    |
| liters\_to\_gallons(liters)   | gal = liters \* 0.2641720523581484 | 1 L ≈ 0.2641720523581484 US gallons |
| pounds\_to\_kilograms(pounds) | kg = pounds \* 0.45359237          | 1 lb = 0.45359237 kg                |
| kilograms\_to\_pounds(kg)     | lb = kg \* 2.2046226218487757      | 1 kg ≈ 2.2046226218487757 lb        |
| fahrenheit\_to\_celsius(F)    | C = (F - 32) \* 5/9                | Fahrenheit → Celsius                |
| celsius\_to\_fahrenheit(C)    | F = C \* 9/5 + 32                  | Celsius → Fahrenheit                |

## Using Claude Code to generate tests

Workflow used:

1. Craft a clear prompt describing required test coverage for converter.py.
2. Ask Claude Code to generate a comprehensive pytest suite (test\_converter.py).
3. Run pytest to see failing tests (expected first red).
4. Implement converter.py to satisfy tests, iterate until green.

The generated test suite covers:

* Correctness for integers and floats.
* Zero input scenarios.
* Negative value tests.
* TypeError tests for non-numeric inputs.
* Use of pytest.approx() for floating-point comparisons.

Example test file header and organization (representative):

```python theme={null}
