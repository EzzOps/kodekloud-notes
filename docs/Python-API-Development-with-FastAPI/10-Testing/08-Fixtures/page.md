# new_user = schemas.UserOut(**res.json())
# assert new_user.email == "hello123@gmail.com"
assert res.status_code == 201
```

If there’s an issue with the assertions, for example:

```plaintext theme={null}
tests/test_users.py:19: AssertionError
```

feel free to add additional assertions as needed for more robust testing.

***

## Transitioning to Login

Next, we address the login functionality with the `test_login_user` test case. This test depends on the client fixture to send requests to the login endpoint. Note that the login route is defined as `/login` (without a trailing slash), so our test request must reflect that configuration.

Initially, the code snippet for login testing might have been incomplete (missing the client parameter):

```python theme={null}
def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "password123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

def test_login_user()
```

After including the client injection and adapting the route, the updated test code becomes:

```python theme={null}
def test_create_user(client):
    res = client.post(
        "/users", 
        json={"email": "hello123@gmail.com", "password": "password123"}
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

def test_login_user(client):
    res = client.post(
        "/login", 
        json={"email": "hello123@gmail.com", "password": "password123"}
    )
    # assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201  # Note: Originally expecting a 307 redirect, but we want a 201
```

<Callout icon="lightbulb">
  For authentication, the login endpoint does not accept JSON. Instead, form data should be sent. Additionally, the field name should be "username" (not "email").
</Callout>

To simulate a proper login, update the test to send form data as follows:

```python theme={null}
def test_login_user(client):
    res = client.post(
        "/login", 
        data={"username": "hello123@gmail.com", "password": "password123"}
    )
    print(res.json())
    assert res.status_code == 200
```

If you run this test and encounter a 422 error, review the error message to ensure that the correct field ("username") is being used. Adjusting the payload accordingly should resolve the issue.

***

## Debugging Login Issues

If the login test returns a 403 error with the detail "Invalid Credentials," it may indicate one of the following:

* The user does not exist in the database.
* The provided password does not match the record in the database.

Review the login route in your authentication module (auth.py) for clarity:

```python theme={null}
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    # create and return token here
```

Ensure the test payload uses the field name "username" to match this implementation.

***

## Understanding Fixture Scopes

Our tests make use of a client fixture, which in turn relies on a session fixture to interact with the database. Consider the following session fixture:

```python theme={null}
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
```

And the corresponding client fixture:

```python theme={null}
@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
```

By default, these fixtures use the **function** scope, meaning they are recreated for each test. This behavior explains why a user created in `test_create_user` does not exist when `test_login_user` is run independently—each test starts with a fresh database.

### Fixture Scopes Explained

| Fixture Scope      | Behavior                                                                                      | Pros and Cons                                                              |
| ------------------ | --------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Function (default) | Runs for each test function, ensuring isolation by recreating the database before every test. | Ensures tests are independent.                                             |
| Module             | Runs once per module; all tests in the module share the same database state.                  | Can allow dependent tests to share state but risks interdependent tests.   |
| Session            | Runs once for the entire testing session, maintaining state across all tests.                 | Useful for state persistence but may lead to flaky tests if order changes. |

Changing to module or session scope can cause tests to pass or fail based on their order. Reliable tests should always set up their own data independently without relying on state changes from other tests.

***

## Final Test Code Example

Below is the final test code with proper scopes and correct data handling:

```python theme={null}
def test_create_user(client):
    res = client.post(
        "/users/", 
        json={"email": "hello123@gmail.com", "password": "password123"}
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

def test_login_user(client):
    res = client.post(
        "/login", 
        data={"username": "hello123@gmail.com", "password": "password123"}
    )
    print(res.json())
    assert res.status_code == 200
```

<Callout icon="lightbulb">
  While it might be tempting to tweak fixture scopes (e.g., set them to module or session scopes) to share state between tests, isolating each test is best practice. This prevents cascading failures and ensures that each test validates only its own functionality.
</Callout>

***

## Final Thoughts

This lesson demonstrated how to create independent and reliable tests for user creation and login in a FastAPI application by correctly handling fixture scopes. In the next part of the lesson, we will explore strategies for generating independent test data for login without relying on previously created users.

Happy Testing!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/eed445e5-68aa-46b3-9922-0fdf2a57b8f1/lesson/fc57a9bb-8e59-4b57-a225-e4ec1542d062" />
</CardGroup>


# Fixtures

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Testing/Fixtures/page

Learn to reduce repetitive code in bank account tests using pytest fixtures for efficient test setup and management.

In this article, you'll learn how to reduce repetitive code in your bank account tests using pytest fixtures. When testing your bank account functionality, you might notice that each test requires initializing a bank account instance multiple times. For example:

```python theme={null}
assert bank_account.balance == 80

def test_collect_interest():
    bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55
```

When running your tests, you might see output similar to this:

```pytest theme={null}
plugins: cov-2.12.1
collected 11 items

tests/test_calculations.py::test_add[3-2-5] PASSED
tests/test_calculations.py::test_add[7-1-8] PASSED
tests/test_calculations.py::test_add[2-4-16] PASSED
tests/test_calculations.py::test_subtract PASSED
tests/test_calculations.py::test_multiply PASSED
tests/test_calculations.py::test_divide PASSED
tests/test_calculations.py::test_bank_set_initial_amount PASSED
tests/test_calculations.py::test_bank_default_amount PASSED
tests/test_calculations.py::test_withdraw PASSED
tests/test_calculations.py::test_deposit PASSED
tests/test_calculations.py::test_collect_interest PASSED

============================= 11 passed in 0.09s =============================
```

Notice that every test involving the bank account starts by creating an instance:

```python theme={null}
def test_divide():
    assert divide(20, 5) == 4

def test_bank_set_initial_amount():
    bank_account = BankAccount(50)
    assert bank_account.balance == 50

def test_bank_default_amount():
    bank_account = BankAccount()
    assert bank_account.balance == 0

def test_withdraw():
    bank_account = BankAccount(50)
    bank_account.withdraw(20)
    assert bank_account.balance == 30
```

And similarly for deposit and interest collection:

```python theme={null}
def test_deposit():
    bank_account = BankAccount(50)
    bank_account.deposit(30)
    assert bank_account.balance == 80

def test_collect_interest():
    bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55
```

This repetitive code can become tedious when you have many tests (for example, 50 tests in a single class). Pytest fixtures help minimize this redundancy.

<Callout icon="lightbulb">
  A fixture is simply a function that runs before your tests and sets up the necessary environment, such as creating an instance of a bank account.
</Callout>

## Creating Fixtures

We'll start by creating two fixtures. One fixture initializes a bank account with a zero balance and the other initializes it with a preset balance (e.g., 50). Although you can place fixtures anywhere, the best practice is to define them at the top of your test file. For example:

```python theme={null}
import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount

@pytest.fixture
def zero_bank_account():
    print("Creating an empty bank account")
    return BankAccount()

@pytest.fixture
def bank_account():
    # Returns a bank account with an initial value of 50.
    return BankAccount(50)
```

You can use these fixtures by adding them as parameters to your test functions. Below is an example of refactored tests using these fixtures:

```python theme={null}
def test_divide():
    assert divide(20, 5) == 4

def test_bank_set_initial_amount(bank_account):
    # Using the bank_account fixture that initializes with 50.
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    # Using the zero_bank_account fixture that initializes with 0.
    print("Testing my bank account")
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30
```

When running the tests with the `-s` flag (which shows print statements), you'll see that the fixture runs before your test function. For instance, the output for `test_bank_default_amount` will display:

```text theme={null}
Creating an empty bank account
Testing my bank account
PASSED
```

This confirms that the fixture is executed prior to the test itself.

## Parameterizing Fixtures and Test Scenarios

Fixtures can also be combined with pytest’s parameterization feature to test multiple scenarios. For example, you can parameterize addition test cases as shown below:

```python theme={null}
@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    print("Testing add function")
    assert add(num1, num2) == expected

def test_subtract():
    assert subtract(9, 4) == 5
```

Consider a more complex test case that involves both depositing and withdrawing money. Initially, you might write:

```python theme={null}
def test_bank_transaction(zero_bank_account):
    zero_bank_account.deposit(200)
    zero_bank_account.withdraw(100)
    assert zero_bank_account.balance == 100
```

You can further combine fixtures with parameterized data in this way:

```python theme={null}
@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000),
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected
```

When you run the tests, the output may look like this:

```text theme={null}
tests/test_calculations.py::test_withdraw PASSED
tests/test_calculations.py::test_deposit PASSED
tests/test_calculations.py::test_collect_interest PASSED
tests/test_calculations.py::test_bank_transaction[200-100-100] Creating an empty bank account
tests/test_calculations.py::test_bank_transaction[50-10-40] Creating an empty bank account
tests/test_calculations.py::test_bank_transaction[1200-200-1000] Creating an empty bank account
============================== 14 passed in 0.09s ==============================
```

Each parameterized scenario uses the fixture to set up the test environment correctly.

## Conclusion

Using pytest fixtures helps eliminate repetitive setup code across multiple tests. They not only simplify your test code for scenarios like deposit and withdrawal operations but also make it easier to manage more complex cases, such as setting up databases or external services.

<Callout icon="lightbulb">
  By combining fixtures with parameterized test cases, you can efficiently cover a wide range of scenarios while keeping your test code concise, maintainable, and SEO-friendly.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/eed445e5-68aa-46b3-9922-0fdf2a57b8f1/lesson/b77bff5f-f83c-401c-a32b-7692f7ccd2ab" />
</CardGroup>
