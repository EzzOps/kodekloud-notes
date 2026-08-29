# Alembic Finish Rest Of Schema

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Database-Migration/Alembic-Finish-Rest-Of-Schema/page

This guide explains how to finalize a database schema using Alembic, including creating tables, adding columns, and managing migrations.

In this guide, we will walk through how to complete your database schema using Alembic. We add user functionality by creating a users table, link posts to users using a foreign key, and then add additional columns along with a votes table via Alembic’s auto-generation feature.

***

## Creating the Users Table

After successfully creating the posts table, the next step is implementing user functionality by creating a users table. This table will allow users to register and log in.

> **lightbulb** Before proceeding, ensure that your existing posts table is functioning correctly.

First, we add a new column to the posts table by executing the following migration:

```python theme={null}
