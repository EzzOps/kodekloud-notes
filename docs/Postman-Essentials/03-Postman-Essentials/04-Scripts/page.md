# Scripts

Source: https://notes.kodekloud.com/docs/Postman-Essentials/Postman-Essentials/Scripts/page

Learn to use Postman scripts for dynamic token management in your development environment, capturing tokens from login responses and saving them as environment variables.

In this article, you'll learn how to use Postman scripts to dynamically manage tokens within your development environment. By capturing the token from a login response and saving it as an environment variable, you can reference this variable in subsequent API requests without the need for manual updates.

## Setting Up Your Environment

First, navigate to your development environment and create a new variable called "token". Instead of embedding the token directly in your collection’s configuration, dynamically referencing the token variable ensures that its value is always pulled from your environment. Be sure to save your environment after making any changes.

> **lightbulb** After a successful login, the token is automatically captured from the response body and set as the value of the token environment variable.

## Example Login Response

Below is an example of a token returned from a login response:

```json theme={null}
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjEyOGM3ZjQ0MzU0NjBiM2E2MTdiMWE2IiwiaWF0IjoxNjg3NjQ5NzY0LCJleHBfc2VyaWVzIjoxNjg3NjUzNTY0fQ.E0DENTIZORD9RAdfHqboxTroapWYBqcW9zAcU99YomB_3u_lP8Rs"
}
```

## Implementing the Token Extraction Script

To extract and store the token dynamically, add the following script to the Tests tab of your login request. This script parses the response JSON and sets the token environment variable:

![The image shows a Postman interface with a POST request to a login endpoint. The response body displays a JSON object containing a token.](https://kodekloud.com/kk-media/image/upload/v1752882936/notes-assets/images/Postman-Essentials-Scripts/postman-post-request-login-json.jpg)

```javascript theme={null}
var res = pm.response.json();
pm.environment.set("token", res.token);
```

When you execute your login request, Postman processes the script and updates the token variable automatically. This eliminates the need for manual token management.

## Verifying Dynamic Token Updates

After running the login request, inspect your environment settings to confirm that the token has been updated. This dynamic update is particularly useful when making authenticated requests, such as creating a new product, where the token is required for access.

### Example Request Body for Adding a Product

```json theme={null}
{
  "name": "TV123",
  "price": 100,
  "category": "electronics"
}
```

### Example JSON Response After Creating a Product

```json theme={null}
{
  "product": {
    "id": 2,
    "name": "TV1",
    "price": 100,
    "category": "electronics",
    "updatedAt": "2023-04-14T05:05:41.104Z",
    "createdAt": "2023-04-14T05:05:41.104Z"
  }
}
```

The authentication is managed automatically by the script shown earlier, ensuring that every time you log in, the token is captured and stored in your environment variable. This streamlined setup helps maintain up-to-date configurations with the latest authentication token.

> **lightbulb** For more detailed documentation on automating token management and optimizing your API testing workflow, check out the [Postman Documentation](https://learning.postman.com/docs/).

- [Watch Video](https://learn.kodekloud.com/user/courses/postman-essentials/module/0a8a02c7-cab8-4bd9-886e-c7570885146f/lesson/fbb1567f-6e06-4b28-b709-328054f0ce77)
