# Building out our tool Creating the API

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-in-Action/Using-Copilot-Efficiently/Building-out-our-tool-Creating-the-API/page

Guide to building a FastAPI service that serves and generates fake CSV-derived data using SQLite and simple local generators.

In this project we generated a large set of fake CSV data with help from a local LLM, imported it into a SQLite database, and built a small REST API in Python (FastAPI) that can either query the DB or generate fake data on demand. This guide shows the core files, minimal DB helper, simple generators (no external Faker dependency), and how to run and test the service.

## CSV sample

A short excerpt of the CSV we imported into SQLite (the full file is in the project):

```csv theme={null}
474 Kara,Jordan,kara.jordan@example.com,28,Dallas,Lawyer
475 Leo,Nguyen,leo.nguyen@example.com,33,Athens,Teacher
476 Mia,Thomas,mia.thomas@example.com,30,Syracuse,Journalist
477 Nina,Harris,nina.harris@example.com,40,Buffalo,Psychologist
478 Oliver,Garcia,oliver.garcia@example.com,36,Raleigh,Electrician
479 Paula,Kim,paula.kim@example.com,32,Charlotte,Web Developer
480 Quinn,Walker,quinn.walker@example.com,29,Denver,Social Worker
481 Rachel,Perez,rachel.perez@example.com,27,Tucson,Research Scientist
482 Samuel,Gonzalez,samuel.gonzalez@example.com,44,Minneapolis,Business Consultant
483 Tina,Martinez,tina.martinez@example.com,30,Kansas City,Physician Assistant
484 Uma,Lopez,uma.lopez@example.com,31,Oklahoma City,Real Estate Agent
485 Victor,Rivera,victor.rivera@example.com,37,Cleveland,Dentist
486 Wendy,Patel,wendy.patel@example.com,28,Salt Lake City,Hospitality Manager
487 Xavier,Wong,xavier.wong@example.com,39,Fort Worth,Insurance Broker
488 Yara,Lee,yara.lee@example.com,25,Milwaukee,Automotive Engineer
489 Alice,Johnson,alice.johnson@example.com,28,San Francisco,Software Developer
490 Bob,Smith,bob.smith@example.com,34,Austin,Systems Analyst
491 Charlie,Brown,charlie.brown@example.com,45,New York,Graphic Designer
492 Diana,Garcia,diana.garcia@example.com,29,Dallas,Marketing Manager
493 Ethan,Lee,ethan.lee@example.com,31,Miami,Sales Representative
494 Fiona,Taylor,fiona.taylor@example.com,27,Houston,Business Analyst
495 George,Jones,george.jones@example.com,40,Seattle,Project Manager
496 Hannah,Williams,hannah.williams@example.com,22,Boston,Data Scientist
```

We imported this CSV into a table named `fake_data` inside a SQLite file named `fakeData.db`. After creating the DB and importing the CSV, the database UI looked like this:

<Frame>
  <img alt="A dark-mode screenshot of DB Browser for SQLite displaying a table named &#x22;fake_data&#x22; with columns like first_name, last_name, email_address, age, city, and occupation populated with sample rows. The right pane shows an editor for the selected cell (an email address)." />
</Frame>

With `fakeData.db` saved and verified, the next step is building a small API that can either query the `fake_data` table or generate additional fake records on demand.

## Quick DB helper (SQLAlchemy)

We use SQLAlchemy to obtain DB sessions inside FastAPI routes. Create a simple DB helper that exposes a `get_db` dependency for route injection:

```python theme={null}
