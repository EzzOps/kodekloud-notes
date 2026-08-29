# Print the version of Pandas
import pandas as pd
print(pd.__version__)

# Load the Iris dataset from URL
url = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv'
df = pd.read_csv(url)

# Display first 5 rows
print(df.head())

# Display last 5 rows
print(df.tail())

# Save to iris.csv without the index
df.to_csv('iris.csv', index=False)
"""
prompt = f"""
You are a Python data science developer. Return only the code:
```{context}```
"""

raw = get_code_completion(prompt, "python")
python_code = cleanup_code(raw, "python")
print(python_code)
```text

<Callout icon="lightbulb" color="#1CB2FE">
Customize the URL or file path as needed for your environment.
</Callout>

## 3. Auto-Commenting with Docstrings

Enhance an existing helper function by adding detailed docstring comments and explain its output:

```python
context = '''
def to_dictionary(keys, values):
    return dict(zip(keys, values))

keys = ["a", "b", "c"]
values = [2, 3, 4]
print(to_dictionary(keys, values))
'''
prompt = f"""
Regenerate this code with a proper docstring and explain its behavior:
```{context}```
"""

raw = get_code_completion(prompt, "python")
commented_code = cleanup_code(raw, "python")
print(commented_code)
````

Expected result:

```python theme={null}
def to_dictionary(keys, values):
    """
    Convert two lists into a dictionary.

    Parameters:
        keys (list): List of keys.
        values (list): List of values.

    Returns:
        dict: Mapping of keys to values.
    """
    return dict(zip(keys, values))

keys = ["a", "b", "c"]
values = [2, 3, 4]
print(to_dictionary(keys, values))
# Possible outcome: {'a': 2, 'b': 3, 'c': 4}
```

## 4. SQL DDL & Query Generation

Generate SQL statements to create a table, insert CSV rows, and query customers from Chile:

````python theme={null}
context = '''
Index,Customer Id,First Name,Last Name,Company,City,Country,Phone 1,Phone 2,Email,Subscription Date,Website
1,D37CF93EacA6D0,Sheryl,Baxter,Rasmussen Group,East Leonard,Chile,229.077.5154,397.884.0519x718,zunigavanessa@smith.in,2020-08-24,http://www.stephenson.com/
2,1EF7b824ACAD10,Preston,Lozano,Vega-Gentry,East Jimmychester,Djibouti,5153435776,686-620-1820x944,vmata@colon.com,2021-04-23,http://www.hobbs.com/
3,6F94879bdAfE5a6,Roy,Berry,Murillo-Perry,Isabelborough,Antigua and Barbuda,+1-539-402-0259,(496)978-3969x58947,beckycarr@hogan.com,2020-03-25,http://www.lawrence.com/
4,5CFE8FAB1E56e3c,Linda,Olsen,"Dominguez, Mcmillan and Donovan",Bensonview,Dominican Republic,001-808-617-6467x12895,+1-813-324-8756,stanleyblackwell@benson.org,2020-06-02,http://www.good-lyons.com/
5,053d5B5Ab61359,Joanna,Bender,"Martin, Lang and Andrade",West Priscilla,Slovakia (Slovak Republic),001-234-203-0635x76146,001-199-4460-3860x3486,colinalvarado@miles.net,2021-04-17,https://goodwin-ingram.com/
6,2d08F817E2E73F4,Aimee,Downs,Steele Group,Chavezborough,Bosnia and Herzegovina,(283)437-3886x88321,999-728-1637,louis27@gilbert.com,2020-02-25,http://www.berger.net/
'''
prompt = f"""
Using the CSV data below, write SQL to:
1. Create a table `customers`.
2. Insert all rows.
3. Select customers where country = 'Chile'.
Also, show the expected query result.
```{context}```
"""

raw = get_code_completion(prompt, "sql")
sql_code = cleanup_code(raw, "sql")
print(sql_code)
```text

Sample output:

```sql
CREATE TABLE customers (
    id INT PRIMARY KEY,
    customer_id VARCHAR(50),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    company VARCHAR(100),
    city VARCHAR(50),
    country VARCHAR(50),
    phone_1 VARCHAR(30),
    phone_2 VARCHAR(30),
    email VARCHAR(100),
    subscription_date DATE,
    website VARCHAR(200)
);

INSERT INTO customers (id, customer_id, first_name, last_name, company, city, country, phone_1, phone_2, email, subscription_date, website) VALUES
  (1, 'D37CF93EacA6D0', 'Sheryl', 'Baxter', 'Rasmussen Group', 'East Leonard', 'Chile', '229.077.5154', '397.884.0519x718', 'zunigavanessa@smith.in', '2020-08-24', 'http://www.stephenson.com/'),
  -- (remaining rows omitted for brevity)
;

SELECT * FROM customers WHERE country = 'Chile';

-- Possible outcome:
-- 1 | D37CF93EacA6D0 | Sheryl | Baxter | Rasmussen Group | East Leonard | Chile | 229.077.5154 | 397.884.0519x718 | zunigavanessa@smith.in | 2020-08-24 | http://www.stephenson.com/
````

## Resources & References

* [OpenAI Python Library](https://pypi.org/project/openai/)
* [OpenAI API Reference](https://platform.openai.com/docs/api-reference/)
* [Pandas Documentation](https://pandas.pydata.org/docs/)
* [IPython Display Utilities](https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/573b1c18-d6a4-4faa-b3c0-1aa306ea6d25/lesson/f51af4b8-7291-40ea-bc66-41050d44a86a" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/573b1c18-d6a4-4faa-b3c0-1aa306ea6d25/lesson/6e2105ed-19af-4cad-bb9b-5e3b0db7a311" />
</CardGroup>


# Implementing Code Completion

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Implementing-Code-Completion/Implementing-Code-Completion/page

This article provides a guide on using GPT-3.5 Turbo for automated code completion across HTML, Python, and SQL.

Welcome to our comprehensive guide on leveraging GPT-3.5 Turbo for automated code completion. In this tutorial, you’ll learn how to:

* Build interactive HTML examples
* Generate well-documented Python scripts
* Produce ANSI-compliant SQL commands for table creation and queries

By following these steps, you can streamline development workflows and improve code quality across multiple languages.

## 1. Interactive HTML Example

To create a more dynamic HTML demo, we’ll inject JavaScript powered by GPT-3.5 Turbo responses. Here’s an example HTML file that requests code snippets and displays them in a live editor:

```html theme={null}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>GPT-3.5 Turbo Code Preview</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2rem; }
    #editor { width: 100%; height: 300px; border: 1px solid #ccc; padding: 1rem; }
  </style>
</head>
<body>
  <h1>Auto-Generated Code Snippet</h1>
  <div id="editor">Loading...</div>
  <script>
    async function fetchSnippet() {
      const response = await fetch('/api/generate-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: 'Write a JavaScript function to reverse a string.' })
      });
      const data = await response.json();
      document.getElementById('editor').textContent = data.choices[0].text;
    }

    fetchSnippet();
  </script>
</body>
</html>
```

## 2. Generating Python Code with Explanations

Below is a Python script that uses GPT-3.5 Turbo to generate functions with inline comments. This approach ensures your code is both functional and self-documented.

```python theme={null}
import openai

openai.api_key = 'YOUR_API_KEY'

def generate_python_function(prompt: str) -> str:
    """
    Generate a Python function based on the provided prompt.
    Returns the generated code as a string.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=250
    )
    return response.choices[0].message.content

if __name__ == '__main__':
    prompt_text = "Create a Python function that checks if a number is prime, with comments."
    code = generate_python_function(prompt_text)
    print("Generated Python Code:\n", code)
```

<Callout icon="lightbulb">
  Be sure to install the OpenAI Python client with `pip install openai`. Keep your API key secure and never commit it to a public repository.
</Callout>

## 3. Producing ANSI SQL Commands

For dataset management, GPT-3.5 Turbo can auto-generate ANSI-compliant SQL to create tables, insert data, and run queries. Below is an example prompt and the expected output:

```sql theme={null}
-- Prompt: "Generate SQL to create a users table with id, name, email; insert three records; select all users."

CREATE TABLE users (
  id INT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100) UNIQUE
);

INSERT INTO users (id, name, email) VALUES
 (1, 'Alice Smith', 'alice@example.com'),
 (2, 'Bob Johnson', 'bob@example.com'),
 (3, 'Carol White', 'carol@example.com');

SELECT * FROM users;
```

<Callout icon="triangle-alert">
  Always review generated SQL before executing it against production databases to avoid unintended data loss.
</Callout>

## References

* [OpenAI API Documentation](https://platform.openai.com/docs/)
* [HTML5 Specification](https://html.spec.whatwg.org/multipage/)
* [ANSI SQL Standard](https://www.iso.org/standard/63555.html)
* [Python Official Documentation](https://docs.python.org/3/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/573b1c18-d6a4-4faa-b3c0-1aa306ea6d25/lesson/b69c2c0c-9cc8-41b6-a989-84a557da6d47" />
</CardGroup>
