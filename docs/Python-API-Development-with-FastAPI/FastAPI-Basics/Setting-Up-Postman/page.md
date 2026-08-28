# Setting Up Postman

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/FastAPI-Basics/Setting-Up-Postman/page

This article explores using Postman to test APIs, focusing on advanced HTTP methods like PUT and PATCH for efficient endpoint testing.

In this article, we explore how to use Postman to test APIs, especially when working with advanced HTTP methods like PUT and PATCH. While simple GET requests can be handled directly in a web browser, testing more complex routes requires a dedicated tool. Postman fills this gap by allowing you to create and send custom HTTP requests effortlessly.

Postman is a lightweight application designed for building and sending HTTP requests. You can download it from its official website at [postman.com/downloads](https://www.postman.com/downloads). The installer automatically detects your operating system, ensuring a smooth installation process.

Once you launch Postman, you'll be greeted by an interface that lets you configure various components of an HTTP request, including the HTTP method, URL, headers, body, and authorization details—all through a user-friendly GUI.

<Frame>
  ![The image shows a webpage for downloading the Postman app, with a section displaying the Postman interface for API testing.](https://kodekloud.com/kk-media/image/upload/v1752883448/notes-assets/images/Python-API-Development-with-FastAPI-Setting-Up-Postman/postman-app-download-api-testing.jpg)
</Frame>

When you first start Postman, the interface appears mostly blank. To create a new HTTP request, simply click the plus button. Before building your request, you might want to switch to the dark theme and adjust the zoom level for improved visibility.

After clicking the plus button, Postman reveals all necessary fields for crafting an HTTP request. The first step is to select the HTTP method. For our current API testing, we primarily use GET requests. To test operations like data retrieval, ensure the method remains set to GET.

<Frame>
  ![The image shows the Postman application interface with an untitled request setup, displaying options for GET requests and parameters. The left sidebar includes options for collections, environments, and other features.](https://kodekloud.com/kk-media/image/upload/v1752883449/notes-assets/images/Python-API-Development-with-FastAPI-Setting-Up-Postman/postman-untitled-request-interface.jpg)
</Frame>

Next, enter the URL for the API endpoint just as you would in your web browser. If your server provides a URL upon startup, copy that URL—including the HTTP or HTTPS prefix—into Postman. Whether or not you include a trailing slash should not affect the outcome.

After configuring the URL, click the "Send" button. You should see a response similar to this:

```json theme={null}
{"message": "Hello World"}
```

This response confirms that the GET request to the root path is working correctly. Postman streamlines the process of testing API endpoints compared to using a browser alone.

<Callout icon="lightbulb">
  For more complex operations like POST, PUT, or PATCH, Postman's interface provides options to easily modify request headers and payloads, making it an indispensable tool for API development.
</Callout>

To further illustrate the testing process, consider the following sample Python code snippet:

```python theme={null}
@ app.get("/")
def root():
    return {"message": "Hello World"}

@ app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}
```

Restart your server with the following command:

```bash theme={null}
uvicorn main:app --reload
```

The console output will resemble this:

```plaintext theme={null}
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [22656] using watchgod
INFO:     Started server process [17808]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:51249 - "GET / HTTP/1.1" 200 OK
```

Now, use Postman to send a GET request to the `/posts` path. You should receive a response similar to:

```json theme={null}
{"data": "This is your posts"}
```

This confirms that both the root and `/posts` endpoints are functioning correctly when tested with Postman. As you continue learning and developing APIs, Postman will become an essential tool for efficient and effective endpoint testing.

For additional resources on API testing, check out the following links:

* [Postman Documentation](https://learning.postman.com/docs/getting-started/introduction/)
* [API Testing Best Practices](https://www.softwaretestinghelp.com/api-testing-tools/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/b1fa1425-07bf-49c6-b19d-ccded17d940d/lesson/b45b9bde-571a-4982-9bbe-e741db74c008" />
</CardGroup>
