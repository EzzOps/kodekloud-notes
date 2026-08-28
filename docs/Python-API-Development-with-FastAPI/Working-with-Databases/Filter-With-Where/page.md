# Filter With Where

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Working-with-Databases/Filter-With-Where/page

Learn to filter SQL query results using the WHERE clause for specific data retrieval based on conditions.

In this lesson, learn how to filter SQL query results using the WHERE clause. Initially, we retrieved all rows from the table by selecting every column with an asterisk (\*). For example:

```sql theme={null}
SELECT * FROM products;
```

Since no filter criteria are provided, this query returns every entry in the table.

Now, let’s filter the data by returning only specific rows based on a condition. A common use case is retrieving a product by its unique identifier. Given that the ID field serves as a primary key (ensuring each entry is distinct), filtering by this field will return exactly one row. For example, to retrieve the product with an ID of 10, use:

```sql theme={null}
SELECT * FROM products WHERE id = 10;
```

This query returns only the product with an ID of 10. Below is an example of the output:

```text theme={null}
name       | character varying
price      | integer
id         | [PK] integer
is_sale    | boolean
inventory  | integer
created_at | timestamp with time zone
-------------------------------
keyboard   | 28
10         | false
50         | 2021-08-20 00:50:48.457985-04
```

```SQL theme={null}
Successfully run. Total query runtime: 132 msec. 1 rows affected.
```

You can also apply filters on other columns. For example, if you want to identify products that need to be reordered by checking for products with an inventory of zero, specify a condition on the inventory column:

```sql theme={null}
SELECT * FROM products WHERE inventory = 0;
```

When filtering by numeric columns like inventory, simply using the number is sufficient. However, when filtering by text-based (string) columns, such as the product name, you need to enclose the value in single quotes. For instance, to retrieve a product with the name "TV", use:

```sql theme={null}
SELECT * FROM products WHERE name = 'TV';
```

This query returns the product(s) named TV. An example output might look similar to this:

```SQL theme={null}
name               | price  | id  | is_sale | inventory | created_at
-------------------|--------|-----|---------|-----------|------------------------------------------
TV                 | 200    | 1   | false   | 0         | 2021-08-20 00:49:58.021274-04
```

<Callout icon="lightbulb">
  Always enclose text values in single quotes when using them in WHERE clauses. Omitting the quotes will result in an error.
</Callout>

By utilizing the WHERE clause, you can efficiently filter your query results to match specific criteria, be they numeric or text-based. This technique is essential for data retrieval and management in SQL, ensuring that you get exactly the information you need.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/0304b044-64ce-4fd6-a384-156867f36547/lesson/b9dd4edd-4b7a-4395-b42b-9d090b2fb87c" />
</CardGroup>
