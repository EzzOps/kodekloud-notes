# Update Post Test

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Testing/Update-Post-Test/page

This article on testing post update operations helps ensure that your application manages posts securely and reliably.

In this article, we explore how to test post update functionality, including scenarios such as unauthorized access, updating non-existent posts, and deleted posts. The test suite leverages an authorized client, multiple test users, and preconfigured test posts to verify the API's behavior. The detailed explanations below cover each test case along with the corresponding code samples.

***

## Deleting Posts

The deletion tests ensure that the API responds correctly in the following scenarios:

1. Deleting a non-existent post should return a 404 status code.
2. Attempting to delete a post created by another user should return a 403 status code.

```python theme={null}
import pytest

def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/800000")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403
```

***

## Updating Posts

### Successful Update by the Owner

For a successful update, the test builds a dictionary that includes a new title, updated content, and the specific post ID. The authorized client submits a PUT request to update the post, and upon receiving a successful response, the updated post details are validated against the provided data.

```python theme={null}
import pytest
from app import schemas

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]
```

<Callout icon="lightbulb">
  Ensuring correct ownership before updating a post is crucial, as it prevents unauthorized modifications.
</Callout>

### Attempt to Update Another User's Post

A user should not have the ability to update a post that belongs to someone else. The test below verifies this by attempting to update a post associated with `test_posts[3]` and expecting a 403 forbidden response.

```python theme={null}
def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    # Expecting a forbidden response because the post does not belong to the current user.
    assert res.status_code == 403
```

### Unauthorized Update Attempt

When an unauthenticated user attempts to update a post, the API must respond with a 401 status code. This test ensures that unauthorized access is prevented.

```python theme={null}
def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
```

<Callout icon="triangle-alert">
  Do not expose sensitive update endpoints to unauthenticated users, as this can lead to security breaches.
</Callout>

### Updating a Non-Existent Post

In cases where a user attempts to update a post that does not exist, the API should return a 404 error. This test provides valid JSON data to avoid schema validation errors while confirming the correct error response.

```python theme={null}
def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/8000000", json=data)
    assert res.status_code == 404
```

***

## Retrieving All Posts

This test validates the "get all posts" endpoint by retrieving all posts and ensuring each post adheres to the expected schema. The test confirms that the total number of retrieved posts matches the number of test posts created.

```python theme={null}
import pytest
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    
    def validate(post):
        return schemas.PostOut(**post)
    
    posts_list = list(map(validate, res.json()))
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
```

***

## Test Execution Summary

Below is an example of the test run output, highlighting that the tests have passed and listing any warnings that may have been issued.

```plaintext theme={null}
platform win32 -- Python 3.9.5, pytest-6.2.5, py-1.10.0, pluggy-1.0.0 -- c:\users\sanje\documents\courses\fastapi\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\sanje\Documents\Courses\fastapi
plugins: cov-2.12.1
collected 1 item

tests/test_posts.py::test_update_post PASSED

================================= warnings summary =================================
venv\lib\site-packages\aiofiles\os.py:10
  DeprecationWarning: "@coroutine" decorator is deprecated since Python 3.8, use "async def" instead

-- Docs: https://docs.pytest.org/en/stable/warnings.html
4 passed, 5 warnings in 2.17s
```

***

## Voting Tests and Other Post Cases

The remaining tests, such as those for voting functionality and other post-related scenarios, follow a similar structure. These tests are designed to be efficient and comprehensive, covering successful operations as well as unauthorized or invalid requests.

This article on testing post update operations helps ensure that your application manages posts securely and reliably. Continuous testing is key to maintaining robust and error-free API endpoints.

***

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/eed445e5-68aa-46b3-9922-0fdf2a57b8f1/lesson/ee388e20-5d42-4766-a78b-4d9ceed2b20c" />
</CardGroup>
