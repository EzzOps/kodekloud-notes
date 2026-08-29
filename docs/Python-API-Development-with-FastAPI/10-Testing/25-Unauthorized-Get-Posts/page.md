# new_user = schemas.UserOut(**res.json())
assert res.status_code == 201
assert 307 == 201
# where 307 => Response[307].status_code
```

This results in a test failure, as the initial 307 status code from the redirect does not match the expected 201.

> **lightbulb** Always include the trailing slash in your request URL when your route is defined with one (e.g., `/users/`). This practice prevents unnecessary redirects and ensures your API responds as expected during tests.

## Conclusion

By consistently using the correct endpoint path with the required trailing slash, you eliminate the risk of unwanted 307 redirects. This ensures that your endpoints are accurately reached and that your API behaves reliably both in production and during testing.

For further details on FastAPI behavior and endpoint configuration, you can also review the [FastAPI Documentation](https://fastapi.tiangolo.com/).

Happy coding!

- [Watch Video](https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/eed445e5-68aa-46b3-9922-0fdf2a57b8f1/lesson/e3ad7f36-073b-4dbe-ba59-52c732e3fbdf)


# Unauthorized Get Posts

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Testing/Unauthorized-Get-Posts/page

This article explores errors from unauthorized GET requests to an API when retrieving posts due to missing or incorrect authentication credentials.

In this article, we explore scenarios where making an unauthorized GET request to retrieve posts from an API results in errors. Such issues typically arise when authentication credentials are missing, incorrect, or when the required permissions are not granted.

When the system cannot verify the client's identity, it may display an error message such as:

"Unable to fetch caption"

This error indicates that the caption for a post could not be retrieved due to authorization issues. To fix this problem, verify the following:

* Ensure that the correct API credentials (e.g., API key or token) are provided.
* Confirm that the proper authorization headers are included in your request.
* Check that your user account has the necessary permissions to access the resource.

> **lightbulb** Double-check your API gateway configuration to ensure that it correctly routes and validates authentication tokens.

By addressing these points, you can prevent unauthorized errors and guarantee smooth access to post details.

- [Watch Video](https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/eed445e5-68aa-46b3-9922-0fdf2a57b8f1/lesson/20dc6fae-7a0b-41fe-8951-f7a41c75eee1)
