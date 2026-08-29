# Deleting Data

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Working-with-Databases/Deleting-Data/page

This guide explains how to delete entries from a database table using SQL and verify successful deletions.

In this guide, you'll learn how to remove entries from a database table using SQL. Previously, we discussed how to insert new entries. Now, we will focus on the deletion process and how to verify that the intended rows have been removed.

## Basic SQL Delete Syntax

Recall that the basic syntax for deleting a row in SQL is:

```sql theme={null}
DELETE FROM table_name WHERE condition;
```

For example, if you want to delete a row from the "products" table, you must specify the correct row(s) using a unique identifier (typically the product ID).

## Example: Deleting a Single Product

Suppose you want to delete the product with an ID of 10. You can execute the following statements:

```sql theme={null}
DELETE FROM products WHERE id = 10;
SELECT * FROM products;
```

The first statement deletes the row with the specified ID, and the second statement retrieves the remaining products so you can verify that the deletion was successful.

<Callout icon="lightbulb">
  Always use a unique identifier when deleting records to avoid accidentally removing multiple rows.
</Callout>

## Handling Non-Existent Rows

There might be cases where the desired product has already been deleted. For instance, if product ID 10 does not exist and you need to delete product ID 11 instead, you would run:

```sql theme={null}
DELETE FROM products WHERE id = 11;
```

## Using PostgreSQL's RETURNING Clause

PostgreSQL provides a helpful `RETURNING` clause that retrieves data from the row before it is deleted. This feature is useful when confirming exactly which data was removed. For example:

```sql theme={null}
DELETE FROM products WHERE id = 11 RETURNING *;
```

Executing this command will remove the product with an ID of 11 and return all columns from the deleted row. If you omit the `RETURNING` clause, PostgreSQL returns the number of rows that were deleted:

```sql theme={null}
DELETE FROM products WHERE id = 12;
```

A typical console output might look like:

```text theme={null}
DELETE 
Query returned successfully in 99 msec.
```

## Deleting Multiple Products

You might need to delete multiple rows based on a specific criterion. For example, to remove all products with an inventory of zero, use the following command:

```sql theme={null}
DELETE FROM products WHERE inventory = 0;
```

After running the delete command, verify the changes with:

```sql theme={null}
SELECT * FROM products;
```

The console output may confirm that multiple rows were deleted, as shown below:

```SQL theme={null}
DELETE 8
Query returned successfully in 103 msec.
```

This output confirms that no products with an inventory of zero remain in the table.

<Callout icon="lightbulb">
  Always verify deletions by running a SELECT query after your DELETE operations to ensure that only the intended rows were removed.
</Callout>

By following these examples and explanations, you can efficiently manage data deletions in your SQL database while ensuring that you receive appropriate confirmation for each operation.

## Additional Resources

* [SQL Documentation](https://www.w3schools.com/sql/)
* [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)

This comprehensive approach not only secures your database operations but also aligns with best practices in SQL data management.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/0304b044-64ce-4fd6-a384-156867f36547/lesson/3e06bef3-5868-4d18-960f-ad8f836e2400" />
</CardGroup>
