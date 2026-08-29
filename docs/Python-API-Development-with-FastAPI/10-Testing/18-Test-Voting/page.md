# Test Voting

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Testing/Test-Voting/page

This article provides a guide to setting up and running tests for voting functionality in applications, covering various scenarios and edge cases.

In this article, we set up and run tests for the voting functionality in your application. Our tests cover various scenarios including successful voting, duplicate vote attempts, vote deletions, and edge cases such as voting on non-existent posts or by unauthorized users. Before running these tests, ensure you have an authorized client and properly configured test posts in your test environment.

***

## Retrieving and Validating Posts

The initial test function retrieves all posts and validates them using the defined schema. This ensures that the posts returned by the API match the expected structure.

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

Console Output:

```plaintext theme={null}
venv\lib\site-packages\aiofiles\os.py:10
venv\lib\site-packages\aiofiles\os.py:10
venv\lib\site-packages\aiofiles\os.py:10
venv\lib\site-packages\aiofiles\os.py:10
C:\Users\sanje\Documents\courses\fastapi\venv\lib\site-packages\aiofiles\os.py:10: DeprecationWarning: "@coroutine" decorator is deprecated since Python 3.8, use "async def" instead
=========== 4 passed, 5 warnings in 2.17s ===========
```

Save this file as `test_votes.py`.

***

## Testing a Successful Vote

For the successful vote test, we simulate voting on a post. Initially, the function prototype is set as follows:

```python theme={null}
def test_vote_on_post(authorized_client, test_post)
```

After setting up the endpoint URL and required data (post ID and vote direction), we update the test to include the correct post ID:

```python theme={null}
def test_vote_on_post(authorized_client, test_posts):
    # Vote on the first post by sending the post's id
    authorized_client.post("/vote/", json={"post_id": test_posts[0].id})
```

Since a vote direction is needed (with 1 representing a like/upvote), the function is modified accordingly:

```python theme={null}
def test_vote_on_post(authorized_client, test_posts):
    # Vote on the first post with direction set to 1 (like/upvote)
    authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
```

In our final version, we simulate voting on a post owned by another user by selecting the fourth post from the list:

```python theme={null}
def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 201
```

Console Output after running:

```plaintext theme={null}
C:\users\sanje\documents\courses\fastapi\venv\lib\site-packages\aiofiles\os.py:10: DeprecationWarning: "@coroutine" decorator is deprecated since Python 3.8, use "async def" instead
```

Running the command:

```bash theme={null}
pytest tests/test_posts.py -v -s
```

yields:

```plaintext theme={null}
=================================== test session starts ====================================
...
4 passed, 5 warnings in 2.17s
```

***

## Testing Duplicate Voting

Duplicate voting is an important scenario where a user attempts to vote on a post twice. First, a fixture is used to set up the initial vote:

```python theme={null}
import pytest
from app import models

@pytest.fixture()
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()
```

The test case for duplicate voting validates that the second vote attempt returns a 409 status code:

```python theme={null}
def test_vote_twice_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409
```

***

## Testing Vote Deletion

Vote deletion is triggered by setting the vote direction to 0. This function sends the deletion request and asserts a successful deletion:

```python theme={null}
def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201
```

To ensure proper error handling, the following test verifies that deleting a non-existent vote returns a 404 status code. Here, the `test_vote` fixture is not used so no vote exists for the given post:

```python theme={null}
def test_delete_vote_non_exist(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 404
```

***

## Testing Voting on a Non-Existent Post

When a user attempts to vote on a post that does not exist (using an ID that isn’t in the database), the API should return a 404 status code. The following test case ensures this behavior:

```python theme={null}
def test_vote_post_non_exist(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": 80000, "dir": 1})
    assert res.status_code == 404
```

***

## Testing Unauthorized Voting

To verify security measures, the final voting test checks that an unauthorized user (i.e., using an unauthenticated client) cannot vote. This test should return a 401 status code:

```python theme={null}
def test_vote_unauthorized_user(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 401
```

Console output when running these tests might display warnings such as:

```plaintext theme={null}
venv\lib\site-packages\aiofiles\os.py:10: DeprecationWarning: "@coroutine" decorator is deprecated since Python 3.8, use "async def" instead
```

***

## Additional Tests for Bank Account Operations

Although not directly related to voting tests, the repository also includes tests for bank account operations. An example from the bank account test file is given below:

```python theme={null}
def test_bank_default_amount(zero_bank_account):
    print("Testing my bank account")
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30
```

The output confirms that the tests pass:

```plaintext theme={null}
6 passed, 5 warnings in 3.25s
```

***

## Final Notes

<Callout icon="lightbulb">
  Before deleting the `database.py` file, ensure that all tests pass by running your complete test suite. The majority of functionality has now been moved to `conftest.py`.
</Callout>

An example of the `test_posts` fixture used throughout the tests is shown below:

```python theme={null}
@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user['id']
        },
        {
            "title": "2nd title",
            "content": "2nd content",
            "owner_id": test_user['id']
        },
        {
            "title": "3rd title",
            "content": "3rd content",
        },
    ]
```

<Callout icon="triangle-alert">
  When writing tests, consider additional scenarios that could potentially break the application by creating individual test cases for each situation. Comprehensive testing is essential for ensuring the stability and reliability of your application.
</Callout>

***

By following this guide, you have now set up a robust test suite covering various edge cases and scenarios for voting and other functionality. This comprehensive approach not only helps in maintaining functionality but also enhances the resilience of your application.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/eed445e5-68aa-46b3-9922-0fdf2a57b8f1/lesson/e293189f-da1c-48b2-993d-3b51153ede70" />
</CardGroup>
