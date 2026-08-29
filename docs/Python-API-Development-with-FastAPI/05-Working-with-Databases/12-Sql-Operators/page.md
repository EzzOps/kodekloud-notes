# Sql Operators

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Working-with-Databases/Sql-Operators/page

Explains SQL comparison and logical operators, covering =, <>, !=, >, <, >=, <=, AND/OR with examples, precedence, common mistakes and best practices for WHERE clauses

In this lesson we cover common SQL comparison and logical operators. Up to now we've mainly used equality in WHERE clauses; here we'll expand to greater-than, less-than, not-equal, and boolean combinations (AND / OR) with clear examples and best practices.

To follow the examples, assume the products table contains rows like the following:

| name             | price | id | is\_sale | inventory | created\_at                   |
| ---------------- | ----: | -: | :------: | --------: | ----------------------------- |
| TV               |   200 |  1 |   false  |         0 | 2021-08-20 00:49:58.021274-04 |
| DVD Players      |    80 |  2 |   false  |         0 | 2021-08-20 00:49:58.021274-04 |
| remote           |    10 |  3 |   false  |         0 | 2021-08-20 00:49:58.021274-04 |
| microphone       |    30 |  5 |   false  |         0 | 2021-08-20 00:49:58.021274-04 |
| Car              |    40 |  7 |   false  |         0 | 2021-08-20 00:49:58.021274-04 |
| pencil           |     2 |  8 |   false  |         0 | 2021-08-20 00:49:58.021274-04 |
| pencil sharpener |     4 |  9 |   true   |         0 | 2021-08-20 00:49:58.021274-04 |
| keyboard         |    28 | 10 |   false  |        50 | 2021-08-20 00:50:48.457985-04 |
| soda             |     2 | 11 |   true   |        10 | 2021-08-20 23:01:37.283024-04 |
| pizza            |    13 | 12 |   true   |        22 | 2021-08-20 23:01:37.283024-04 |
| toothbrush       |     2 | 13 |   true   |         8 | 2021-08-20 23:01:37.283024-04 |
| toilet paper     |     4 | 14 |   false  |       100 | 2021-08-20 23:02:37.786025-04 |
| xbox             |   380 | 15 |   true   |        45 | 2021-08-20 23:04:23.608326-04 |

Operator quick reference

| Operator | Meaning                            | Example                              |
| -------- | ---------------------------------- | ------------------------------------ |
| =        | Equal to                           | `WHERE price = 200`                  |
| \<>      | Not equal (SQL standard)           | `WHERE inventory <> 0`               |
| !=       | Not equal (also supported)         | `WHERE inventory != 0`               |
| >        | Greater than                       | `WHERE price > 50`                   |
| >=       | Greater than or equal to           | `WHERE price >= 80`                  |
| \<       | Less than                          | `WHERE price < 80`                   |
| \<=      | Less than or equal to              | `WHERE price <= 80`                  |
| AND      | Logical AND (both conditions true) | `WHERE inventory > 0 AND price > 20` |
| OR       | Logical OR (either condition true) | `WHERE price > 100 OR price < 20`    |

Equality (=)

* Use = to match exact values.

```sql theme={null}
-- Find products priced at 200
SELECT * FROM products WHERE price = 200;
```

Possible result:

```text theme={null}
name | price | id | is_sale | inventory | created_at
TV   | 200   | 1  | false   | 0         | 2021-08-20 00:49:58.021274-04
```

Greater than / Less than (> / \< / >= / \<=)

* Use >, \<, >=, \<= just like in most programming languages to compare numeric or date values.

```sql theme={null}
-- Prices strictly greater than 50
SELECT * FROM products WHERE price > 50;
```

Example result:

```text theme={null}
name        | price | id | is_sale | inventory | created_at
TV          | 200   | 1  | false   | 0         | ...
DVD Players | 80    | 2  | false   | 0         | ...
xbox        | 380   | 15 | true    | 45        | ...
```

Additional examples:

```sql theme={null}
-- Prices greater than or equal to 80 (includes 80)
SELECT * FROM products WHERE price >= 80;

-- Prices less than 80 (strictly less than 80)
SELECT * FROM products WHERE price < 80;

-- Prices less than or equal to 80 (includes 80)
SELECT * FROM products WHERE price <= 80;
```

Not equal (\<> and !=)

* SQL supports two common not-equal syntaxes: \<> (SQL standard) and != (supported by many engines such as PostgreSQL).

```sql theme={null}
-- Using !=
SELECT * FROM products WHERE inventory != 0;

-- Using <> (SQL standard)
SELECT * FROM products WHERE inventory <> 0;
```

Either query returns rows where inventory is not zero (i.e., items in stock).

> **lightbulb** Use \<> when you want to follow SQL standard syntax. Many databases accept both `<>` and `!=`; pick one consistent with your team's style guide or your DBMS documentation.

Combining conditions: AND / OR

* Use AND to require multiple conditions and OR to return rows that satisfy at least one condition.
* Use parentheses to control precedence when mixing AND and OR.

Example (AND):

```sql theme={null}
-- Items with inventory greater than 0 AND price greater than 20
SELECT * FROM products WHERE inventory > 0 AND price > 20;
```

Example (OR):

```sql theme={null}
-- Items with price greater than 100 OR less than 20
SELECT * FROM products WHERE price > 100 OR price < 20;
```

Precedence and grouping:

```sql theme={null}
-- Without parentheses AND has higher precedence than OR in SQL,
-- but it's clearer to group conditions explicitly if logic is complex:
SELECT * FROM products WHERE (price > 100 AND inventory > 0) OR is_sale = true;
```

Common mistake: missing WHERE

* Forgetting the WHERE keyword is a frequent source of syntax errors.

```sql theme={null}
-- Incorrect: missing WHERE
SELECT * FROM products inventory > 0 AND price > 20;
```

Typical error (psql example):

```text theme={null}
ERROR:  syntax error at or near "inventory"
LINE 1: SELECT * FROM products inventory > 0 AND price > 20;
                               ^
SQL state: 42601
```

> **warning** Always include WHERE after FROM (and after any JOIN clauses) when filtering rows. When queries become complex, format and indent conditions to make missing keywords obvious.

Summary and best practices

* Use =, >, \<, >=, \<= for comparisons.
* Prefer \<> for not-equal to follow SQL standard; `!=` is often supported but be consistent.
* Combine conditions with AND and OR; use parentheses to group logic explicitly.
* Place WHERE after FROM (and after JOINs) — omitting it causes syntax errors.
* For readability and maintainability, format multi-condition WHERE clauses on multiple lines and consider adding comments for complex boolean logic.

Links and references

* [PostgreSQL WHERE documentation](https://www.postgresql.org/docs/current/queries-table-expressions.html)
* [SQL Comparison Operators (general reference)](https://www.w3schools.com/sql/sql_operators.asp)

- [Watch Video](https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/0304b044-64ce-4fd6-a384-156867f36547/lesson/18e29f1f-09d5-4a3d-886f-65f9f1dceb87)
