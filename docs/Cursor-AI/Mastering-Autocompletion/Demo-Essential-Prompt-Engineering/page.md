# Demo Essential Prompt Engineering

Source: https://notes.kodekloud.com/docs/Cursor-AI/Mastering-Autocompletion/Demo-Essential-Prompt-Engineering/page

Learn to craft effective prompts for large language models to achieve consistent, high-quality outputs in AI workflows.

In this guide, you’ll learn how to craft effective prompts that steer large language models (LLMs) and tools like Cursor toward consistent, high-quality outputs. From precise requirements to creative exploration, we cover zero-shot, one-shot, few-shot, chain-of-thought, and self-consistency techniques to elevate your AI workflows.

***

## Initial Context: Flask Task Manager Scaffold

Use this simple Flask application as a reference throughout our examples:

```python theme={null}
import csv
import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from datetime import datetime
import hashlib
import logging
