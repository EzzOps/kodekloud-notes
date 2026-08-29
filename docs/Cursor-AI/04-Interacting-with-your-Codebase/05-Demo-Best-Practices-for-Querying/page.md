# Demo Best Practices for Querying

Source: https://notes.kodekloud.com/docs/Cursor-AI/Interacting-with-your-Codebase/Demo-Best-Practices-for-Querying/page

Learn effective querying techniques for large language models in code, documentation, and web searches using a simple Flask application.

Discover how to craft effective queries for large language models (LLMs) when working with code, documentation, and web searches. We’ll demonstrate each principle using a simple Flask application.

## Prerequisites

* Python 3.x
* Flask ([https://flask.palletsprojects.com/](https://flask.palletsprojects.com/))
* SQLite ([https://www.sqlite.org/](https://www.sqlite.org/))
* Basic HTML/CSS (for templates)

## Sample Flask Application

```python theme={null}
import csv
import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from datetime import datetime
import hashlib
import logging
