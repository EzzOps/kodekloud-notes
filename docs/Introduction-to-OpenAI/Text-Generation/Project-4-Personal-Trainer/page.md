# Project 4 Personal Trainer

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Text-Generation/Project-4-Personal-Trainer/page

Create a command-line personal trainer application using Python and the OpenAI API to provide custom fitness recommendations based on user goals and data.

In this tutorial, you’ll create a command-line personal trainer application leveraging the OpenAI API and Python. You will:

* Load real-world fitness data
* Collect user health goals
* Generate custom, actionable recommendations

## Prerequisites

| Package    | Purpose                   | Installation Command                          |
| ---------- | ------------------------- | --------------------------------------------- |
| Python 3.x | Core programming language | [Download](https://www.python.org/downloads/) |
| openai     | OpenAI Python SDK         | `pip3 install openai`                         |
| pandas     | Data manipulation and I/O | `pip3 install pandas`                         |

```bash theme={null}
pip3 install openai pandas
```

<Callout icon="triangle-alert">
  Storing your API key in plaintext is insecure. Use environment variables or a secrets manager instead of hardcoding it in your script.
</Callout>

## 1. Setup and Imports

Create a file named `personal_trainer.py` and add:

```python theme={null}
import os
import pandas as pd
from openai import OpenAI
