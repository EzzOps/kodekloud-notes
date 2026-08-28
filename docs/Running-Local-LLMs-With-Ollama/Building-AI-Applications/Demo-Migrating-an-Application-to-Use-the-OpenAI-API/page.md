# server.py
import os
from flask import Flask, request, render_template_string
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("LLM_ENDPOINT")
)

# Simple HTML template for the app UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>AI Poem Generator</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 2rem; background: #f9f9f9; }
        .container { max-width: 800px; margin: 0 auto; background: #fff; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
        textarea { width: 100%; height: 120px; padding: 0.5rem; margin-bottom: 0.75rem; }
        button { padding: 0.5rem 1rem; }
        pre { background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Poem Generator</h1>
        <form method="POST">
            <textarea name="input" placeholder="Enter your prompt here..."></textarea>
            <br />
            <button type="submit">Generate Poem</button>
        </form>
        {% if poem %}
        <h2>Your AI-Generated Poem</h2>
        <pre>{{ poem }}</pre>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    poem = None
    if request.method == "POST":
        try:
            input_message = request.form["input"]

            response = client.chat.completions.create(
                model=os.environ.get("MODEL"),
                messages=[
                    {"role": "system", "content": "You are an AI assistant specialized in writing poems."},
                    {"role": "user", "content": input_message}
                ],
            )

            # Extract the generated text from the response
            # Structure: response.choices[0].message.content
            poem = response.choices[0].message.content
        except Exception as e:
            # log the exception, and show a friendly error to the user
            print("Error:", str(e))
            poem = "An error occurred when trying to fetch your poem."

    return render_template_string(HTML_TEMPLATE, poem=poem)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    # Development server — do not use this directly in production
    app.run(host="0.0.0.0", port=port)
```

## Configuration — environment variables

Store runtime configuration in a `.env` file at the project root. This keeps credentials and endpoints out of your code and makes switching between local Ollama and OpenAI hosted APIs straightforward.

| Variable         | Purpose                                                                                                                                   | Example                                                |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| OPENAI\_API\_KEY | API key used by the OpenAI client. For local Ollama testing this can be any value. Replace with a real key when using OpenAI hosted APIs. | kodekloud                                              |
| LLM\_ENDPOINT    | Base URL for the LLM endpoint. For Ollama local server use [http://localhost:11434/v1](http://localhost:11434/v1)                         | [http://localhost:11434/v1](http://localhost:11434/v1) |
| MODEL            | Model identifier to call (configurable without code changes).                                                                             | llama3.2                                               |

Example `.env` contents:

```bash theme={null}
OPENAI_API_KEY=kodekloud
LLM_ENDPOINT=http://localhost:11434/v1
MODEL=llama3.2
```

## How the app works (high-level)

* The HTML form posts the user's prompt to "/".
* The Flask route builds a `messages` array: a system message to define role plus the user's message.
* The OpenAI Python client sends that to the chat completions endpoint (`client.chat.completions.create(...)`) and returns a response object.
* We extract the model output at `response.choices[0].message.content` and render it inside the page.

## Start Ollama's REST API (local)

Ensure the Ollama local service is running so the OpenAI client can reach it. Typical local start command:

```bash theme={null}
ollama serve
```

By default Ollama exposes endpoints such as POST /v1/chat/completions and listens on `localhost:11434`.

Representative Ollama server log when started:

```log output theme={null}
time=2025-01-24T13:05:44.483+05:30 level=INFO msg="Listening on 127.0.0.1:11434 (version 0.5.7)"
time=2025-01-24T13:05:44.530+05:30 level=INFO msg="inference compute" id=0 library=metal total="10.7 GiB" available="10.7 GiB"
```

## Run the Flask app

With your virtualenv active and `.env` in place:

```bash theme={null}
python server.py
```

You should see the Flask development server start:

```text theme={null}
* Serving Flask app 'server'
* Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:3000
Press CTRL+C to quit
```

Open [http://127.0.0.1:3000](http://127.0.0.1:3000), enter a prompt such as "Write a short poem about cats" and click "Generate Poem." The app will POST the prompt to the model and display the returned poem.

<Frame>
  <img alt="A browser screenshot of a web app titled &#x22;AI Poem Generator&#x22; with a prompt input box, a &#x22;Generate Poem&#x22; button, and a panel labeled &#x22;Your AI-Generated Poem.&#x22; The displayed poem is a block of text about felines." />
</Frame>

## Logs you will see

* Flask logs GET and POST requests to `/`.
* Ollama logs incoming requests to `/v1/chat/completions`.

Example Flask access log:

```text theme={null}
127.0.0.1 - - [24/Jan/2025 13:07:03] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2025 13:07:43] "POST / HTTP/1.1" 200 -
```

## Next steps and production considerations

* This demo illustrates a minimal integration pattern. To prepare for production:
  * Use a production WSGI server (gunicorn/uvicorn) instead of Flask’s dev server.
  * Store secrets securely (e.g., a secret manager or environment variable service).
  * Add robust error handling, rate limiting, and input validation/sanitization.
  * Cache or paginate long-running requests and handle model timeouts gracefully.
  * When switching to OpenAI hosted APIs, change the `LLM_ENDPOINT` and set a valid `OPENAI_API_KEY`.

<Callout icon="lightbulb">
  This is a simple demo intended for local development. For production, use a production WSGI server (gunicorn/uvicorn), secure environment secrets properly, and follow best practices for rate-limiting, error handling, and user input sanitization.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/running-local-llms-with-ollama/module/8df2f2d5-d3c5-433d-b5f5-f553b040b2e7/lesson/a1ed1316-1893-4329-ae9e-f93f7202d62b" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/running-local-llms-with-ollama/module/8df2f2d5-d3c5-433d-b5f5-f553b040b2e7/lesson/ef20f910-b01d-45e1-8509-ce81507dfe77" />
</CardGroup>


# Demo Migrating an Application to Use the OpenAI API

Source: https://notes.kodekloud.com/docs/Running-Local-LLMs-With-Ollama/Building-AI-Applications/Demo-Migrating-an-Application-to-Use-the-OpenAI-API/page

This guide explains how to migrate a Flask-based AI app to use the OpenAI API while developing locally with Ollama.

This guide shows you how to update a Flask-based AI app to use the OpenAI API in production while still developing locally with Ollama. By changing only a few environment variables, you can switch between free local development and cost-effective cloud inference.

<Frame>
  ![The image shows the OpenAI developer platform webpage, featuring options to sign up or log in, and information about different AI models like GPT-4o and o1-mini. The sidebar includes links to various capabilities and resources.](https://kodekloud.com/kk-media/image/upload/v1752883645/notes-assets/images/Running-Local-LLMs-With-Ollama-Demo-Migrating-an-Application-to-Use-the-OpenAI-API/openai-developer-platform-webpage.jpg)
</Frame>

***

## 1. Create an OpenAI API Key

1. Sign in or sign up at [platform.openai.com](https://platform.openai.com/).

<Frame>
  ![The image shows a login page for OpenAI, offering options to sign in with an email address, phone, Google, Microsoft, or Apple accounts.](https://kodekloud.com/kk-media/image/upload/v1752883646/notes-assets/images/Running-Local-LLMs-With-Ollama-Demo-Migrating-an-Application-to-Use-the-OpenAI-API/openai-login-page-options.jpg)
</Frame>

2. Navigate to **Settings → API keys**, then click **Create new secret key**.
3. Provide a name (e.g., “Ollama app”), assign it to your default project, set permissions, and copy the secret key.

<Frame>
  ![The image shows a webpage for creating a new secret API key on the OpenAI platform, with a form to input details like name, project, and permissions.](https://kodekloud.com/kk-media/image/upload/v1752883647/notes-assets/images/Running-Local-LLMs-With-Ollama-Demo-Migrating-an-Application-to-Use-the-OpenAI-API/openai-new-api-key-form.jpg)
</Frame>

4. Confirm that your new key appears under **API keys**.

<Frame>
  ![The image shows a webpage from the OpenAI platform displaying API key management, with details of an API key named "ollama-app" including its secret key, creation date, and permissions.](https://kodekloud.com/kk-media/image/upload/v1752883648/notes-assets/images/Running-Local-LLMs-With-Ollama-Demo-Migrating-an-Application-to-Use-the-OpenAI-API/openai-api-key-management-ollama-app.jpg)
</Frame>

::: note
Keep your secret key safe. Do not commit it to version control.
:::

***

## 2. Choose a Model

Open the [Quickstart Guide](https://platform.openai.com/docs/quickstart) or the [Models Reference](https://platform.openai.com/docs/models) to compare models. In this demo, we’ll use **gpt-4o-mini**.

| Environment         | Endpoint                                               | Model       | Authentication |
| ------------------- | ------------------------------------------------------ | ----------- | -------------- |
| Local (Ollama)      | [http://localhost:11434](http://localhost:11434)       | o1-mini     | none           |
| Production (OpenAI) | [https://api.openai.com/v1](https://api.openai.com/v1) | gpt-4o-mini | Bearer API Key |

<Frame>
  ![The image shows a webpage from the OpenAI API documentation, detailing flagship models like GPT-4o and their capabilities, along with a sidebar menu for navigation.](https://kodekloud.com/kk-media/image/upload/v1752883650/notes-assets/images/Running-Local-LLMs-With-Ollama-Demo-Migrating-an-Application-to-Use-the-OpenAI-API/openai-api-documentation-gpt4o.jpg)
</Frame>

***

## 3. Update Your Environment Variables

In your project’s `.env` file, replace the Ollama endpoint with OpenAI’s and add your secret key:

```dotenv theme={null}
OPENAI_API_KEY=your_openai_api_key_here
LLM_ENDPOINT="https://api.openai.com/v1"
MODEL=gpt-4o-mini
```

***

## 4. Update the Flask Server

Install the OpenAI Python client and `python-dotenv` if you haven’t already:

```bash theme={null}
pip install openai python-dotenv Flask
```

```python theme={null}
import os
from flask import Flask, request, render_template_string
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("LLM_ENDPOINT")
)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI-Generated Poem</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; background-color: #f8f9fa; }
    .container { max-width: 600px; margin: auto; }
  </style>
</head>
<body>
  <div class="container">
    <h1>AI Poem Generator</h1>
    <form method="post">
      <label for="prompt">Enter a prompt:</label><br>
      <input id="prompt" name="prompt" type="text" required style="width: 100%;"><br><br>
      <button type="submit">Generate Poem</button>
    </form>
    
      <h2>Generated Poem:</h2>
      <pre>{{ poem }}</pre>
    
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    poem = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user",   "content": prompt}
            ],
            store=True
        )
        poem = response.choices[0].message.content
    return render_template_string(HTML_TEMPLATE, poem=poem)

if __name__ == '__main__':
    app.run(port=3000)
```

::: warning
Always use `https://api.openai.com/v1`. Requests over HTTP will be rejected with a 403 error.
:::

***

## 5. Run and Test

1. Activate your virtual environment:
   ```bash theme={null}
   source ollama-app/bin/activate
   ```
2. Start the Flask server:
   ```bash theme={null}
   python server.py
   ```
3. In your browser, go to [http://127.0.0.1:3000](http://127.0.0.1:3000), enter a prompt (e.g., “a poem on birds”) and click **Generate Poem**.

If you accidentally point to `http://api.openai.com`, you’ll see:

```json theme={null}
Error code: 403 - {
  "error": {
    "code": "http_unsupported",
    "message": "The OpenAI API is only accessible over HTTPS. Ensure the URL starts with 'https://'."
  }
}
```

Switching to the `https://` endpoint resolves this.

<Frame>
  ![The image shows an AI Poem Generator interface with a text box for input and a button labeled "Generate Poem." Below, there's a section displaying an AI-generated poem.](https://kodekloud.com/kk-media/image/upload/v1752883651/notes-assets/images/Running-Local-LLMs-With-Ollama-Demo-Migrating-an-Application-to-Use-the-OpenAI-API/ai-poem-generator-interface.jpg)
</Frame>

***

With just an environment-variable tweak, your app seamlessly transitions from local Ollama LLMs to production-ready OpenAI models.

## References

* [OpenAI Quickstart Guide](https://platform.openai.com/docs/quickstart)
* [OpenAI Models Reference](https://platform.openai.com/docs/models)
* [Python OpenAI Library](https://pypi.org/project/openai/)
* [python-dotenv Documentation](https://pypi.org/project/python-dotenv/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/running-local-llms-with-ollama/module/8df2f2d5-d3c5-433d-b5f5-f553b040b2e7/lesson/ca26ae89-22ef-4a76-bb68-78feb12b6f3b" />
</CardGroup>
