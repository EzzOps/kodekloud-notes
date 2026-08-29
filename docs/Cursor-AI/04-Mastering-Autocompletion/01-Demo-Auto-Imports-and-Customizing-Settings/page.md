# Demo Auto Imports and Customizing Settings

Source: https://notes.kodekloud.com/docs/Cursor-AI/Mastering-Autocompletion/Demo-Auto-Imports-and-Customizing-Settings/page

This lesson explores Cursor IDE’s AI-powered autocompletion, Python auto-imports, and customizable settings to enhance Flask development workflows.

In this lesson we explore Cursor IDE’s AI-powered autocompletion, Python auto-imports, and customizable settings. We’ll demonstrate how to streamline your Flask development workflow and tailor Cursor to your preferences.

## Table of Contents

* Automatic Imports
* Quick Fix Menu
* Python Auto Import (Beta)
* Global & Project Settings
  * Importing VS Code Configuration
  * Defining .cursor-rules
  * Feature Toggles
* AI Models & API Keys
* Enabling Beta Features
* Next Steps

## Automatic Imports

Cursor leverages machine learning to detect missing Python modules and insert the corresponding imports. Consider this Flask example:

```python theme={null}
import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from datetime import datetime
import hashlib
import logging
