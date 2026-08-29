# Building out our tool Creating the API

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-Certification/Using-Copilot-Efficiently/Building-out-our-tool-Creating-the-API/page

This tutorial covers importing fake data into SQLite and creating a RESTful API using FastAPI.

In this tutorial, we’ll import fake data from a CSV into SQLite and then wrap it in a RESTful API using FastAPI—with help from GitHub Copilot. By the end, you'll have a working API that generates and persists fake data.

## Importing Fake Data into SQLite

First, open **DB Browser for SQLite** and create a database called `fake_data_generator.db`. Then import `fake-data.csv` into a table named `fake_data`:

![The image shows a code editor with a CSV file open, displaying a list of fake data entries including names, emails, ages, cities, and occupations. The file is part of a project named "FakeDataGenerator" in a directory structure.](https://kodekloud.com/kk-media/image/upload/v1752876954/notes-assets/images/GitHub-Copilot-Certification-Building-out-our-tool-Creating-the-API/fake-data-generator-csv-editor.jpg)

1. In DB Browser, choose **File > Import > Table from CSV file**.
2. Select `fake-data.csv`.
3. Set the table name to `fake_data`, enable **Column names in the first line**, and click **OK**.

![The image shows a screenshot of a database management application, specifically DB Browser for SQLite, with a CSV import dialog open. It displays options for importing data into a table named "fake\_data" and shows a preview of the data with columns like first name, last name, age, and occupation.](https://kodekloud.com/kk-media/image/upload/v1752876955/notes-assets/images/GitHub-Copilot-Certification-Building-out-our-tool-Creating-the-API/db-browser-sqlite-csv-import-dialog.jpg)

> **lightbulb** Ensure your CSV headers match the column names you want in SQLite. This makes querying and persistence more straightforward.

Once imported, confirm that `fake_data` is populated and ready for queries.

## Scaffolding the Python Project

Open your project root in **VS Code**:

![The image shows a Visual Studio Code interface with a file explorer open on the left, displaying various files. A warning message indicates that a file is not displayed because it is either binary or uses an unsupported text encoding.](https://kodekloud.com/kk-media/image/upload/v1752876956/notes-assets/images/GitHub-Copilot-Certification-Building-out-our-tool-Creating-the-API/vscode-file-explorer-warning-message.jpg)

Create `main.py` to invoke the CLI generator:

```python theme={null}
