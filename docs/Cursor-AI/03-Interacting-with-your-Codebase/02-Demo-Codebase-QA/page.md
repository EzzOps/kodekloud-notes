# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'  # Change in production
app.config['DATABASE'] = os.path.join(app.instance_path, 'task_manager.sqlite')

def read_csv(file_path):
    with open(file_path, 'r') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            print(row)

# Ensure the instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

# Database connection functions
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
```

> **triangle-alert** Never use a hardcoded `SECRET_KEY` in production. Store secrets securely using environment variables or a secrets manager.

***

## Querying Best Practices at a Glance

| Practice                    | Description                                                  |
| --------------------------- | ------------------------------------------------------------ |
| Be Specific & Clear         | Define the framework, library, and goal in your query        |
| Provide Just Enough Context | Share only the code or data snippets relevant to your issue  |
| Use Structured Formats      | Present examples in JSON, YAML, tables, or bullet lists      |
| Specify Output Formats      | Ask for code snippets, pseudocode, or documentation excerpts |

***

## 1. Follow Your Querying Guidelines

Maintain a concise set of rules when interacting with LLMs:

* **Be specific and clear:** “How do I implement JWT authentication in Flask?”
* **Provide context:** Mention Flask extensions or database libraries you’re using.
* **Use structured formats:** Wrap code in markdown, share JSON schemas, etc.
* **Specify output formats:** Request a complete function, YAML config, or a step-by-step tutorial.

![The image shows a code editor with a file named "rules.txt" open, displaying a list of guidelines such as "Be specific and clear" and "Provide Context." The interface includes a sidebar with project files and a chat or command input area on the right.](https://kodekloud.com/kk-media/image/upload/v1752872694/notes-assets/images/Cursor-AI-Demo-Best-Practices-for-Querying/code-editor-rules-txt-guidelines.jpg)

Example:

* Instead of “How do I do authentication?”, ask “What is the best way to implement JWT authentication in Flask using PyJWT?”

***

## 2. Provide Only the Context You Need

Adopt the **principle of least privilege** for your context:

* Share only the snippet that’s directly related to your question.
* Exclude unrelated files (e.g., CSS or frontend templates).
* Start minimal, then iterate if you need more detail.

> **lightbulb** Begin with the smallest code snippet that reproduces the issue, then expand only as necessary.

Workflow:

1. Submit a targeted snippet.
2. Evaluate the response.
3. Add relevant code if the answer is incomplete.
4. Refine your question to remove any noise.

***

## 3. Treat Web Searches Like LLM Queries

Search engines and Q\&A sites respond best to precise, action-oriented queries:

* Include the framework, library, and desired outcome.
* Example: “React hook for fetching API data with loading and error handling.”
* Iterate: refine keywords, add sample code, or specify browser support.

Resources:

* [Stack Overflow](https://stackoverflow.com)
* [Official Flask Docs](https://flask.palletsprojects.com/)
* [SQLite Documentation](https://sqlite.org/docs.html)

***

## 4. Iterate and Refine

Think of each query as a draft:

1. Review the LLM’s response.
2. Add or remove context based on accuracy.
3. Clarify output requirements (e.g., “Return JSON only”).
4. Leverage external references and official docs for edge cases.

By combining clear rules, minimal context, structured queries, and iterative refinement, you’ll get more accurate, actionable answers from both LLMs and search engines.

***

Thank you for following this demo. In our next lesson, we’ll dive into editing and debugging techniques for AI-generated code.

## Links and References

* [Flask Documentation](https://flask.palletsprojects.com/)
* [SQLite Official Site](https://sqlite.org/)
* [JWT.io Introduction](https://jwt.io/)
* [Stack Overflow](https://stackoverflow.com)

- [Watch Video](https://learn.kodekloud.com/user/courses/cursor-ai/module/68862e8d-747f-43b7-9411-80812e93a277/lesson/800d627b-2104-4e2b-ab51-961ab4e14a30)


# Demo Codebase QA

Source: https://notes.kodekloud.com/docs/Cursor-AI/Interacting-with-your-Codebase/Demo-Codebase-QA/page

Discover how the codebase feature transforms your repository into a searchable, context-aware knowledge base to boost developer productivity and ease onboarding.

Discover how the **codebase feature** transforms your repository into a searchable, context-aware knowledge base. By querying your entire project structure, you can quickly locate configuration blocks, data-processing routines, and CLI commands—boosting developer productivity and easing onboarding.

## Complete Application Example

Below is a sample [Flask](https://flask.palletsprojects.com/) application (`app.py`) that we’ll use to demonstrate codebase queries:

```python theme={null}
