# Updating Data

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Working-with-Databases/Updating-Data/page

This article explains how to update existing rows in a PostgreSQL database using the UPDATE command.

In this article, we explain how to update existing rows in a PostgreSQL database using the UPDATE command. Previously, we discussed how to insert new data and delete entries. Now, we will focus on updating records within the "products" table.

<Callout icon="lightbulb">
  Always include the WHERE clause in your UPDATE statement to ensure that only the intended records are modified.
</Callout>

## Retrieving Existing Data

Before performing an update, it's a good idea to view the current data. For example, to retrieve all records from the "products" table, you can run:

```sql theme={null}
SELECT * FROM products;
```

## Updating a Single Record

The basic structure for updating a row involves three steps:

1. Specify the table name (e.g., "products").
2. Use the SET keyword to assign new values to the desired columns.
3. Use the WHERE clause to target the specific row(s) for the update.

For instance, if you need to update the product with an ID of 25—changing its name to "flour tortilla" and its price to 40—the SQL command would be:

```sql theme={null}
UPDATE products
SET name = 'flour tortilla', price = 40
WHERE id = 25;
```

After executing this statement, you can verify the changes by running:

```sql theme={null}
SELECT * FROM products;
```

You should see that the record with ID 25 now shows the updated name and price, while the other fields remain unchanged.

## Returning Updated Records

To immediately confirm the changes after an update, you can use the RETURNING keyword. For example, if you want to update the "is\_sale" status of the product with an ID of 30 from false to true and then retrieve the updated record, use the following command:

```sql theme={null}
UPDATE products
SET is_sale = true
WHERE id = 30
RETURNING *;
```

This command updates the record with ID 30 and returns the complete updated row.

## Updating Multiple Records

If you need to update multiple rows at once—such as setting the "is\_sale" field to true for every product with an ID greater than 15—you can modify the WHERE clause accordingly:

```sql theme={null}
UPDATE products
SET is_sale = true
WHERE id > 15
RETURNING *;
```

This command applies the update to all records meeting the specified condition and returns all the updated rows.

By following these steps, you can efficiently modify entries in a PostgreSQL database while ensuring data integrity and precision in your updates.

For more insights on PostgreSQL and SQL commands, explore the [PostgreSQL documentation](https://www.postgresql.org/docs/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/0304b044-64ce-4fd6-a384-156867f36547/lesson/a1763cfe-a9ce-4f43-8e5d-660e5cf329f8" />
</CardGroup>
