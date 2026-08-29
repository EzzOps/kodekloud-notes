# Then return flattened with a response_model that matches this structure
return flattened
```

This approach lets you keep an existing `schemas.PostWithVotes` (or similar) with `votes` as a top-level field.

## Quick reference table — strategies and use cases

|                               Strategy | When to use                                                                                        | Resulting response shape                                                                 |
| -------------------------------------: | -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Create a new response schema (PostOut) | You want to return joined entities exactly as the ORM provides (possibly nested under model names) | Each item is a structured object matching the join (e.g., `{"Post": {...}, "votes": 3}`) |
|               Flatten results to dicts | You prefer a single-level object containing post fields + aggregated columns                       | Each item is a dict with post fields and top-level `votes` integer                       |
|         LEFT OUTER JOIN (isouter=True) | Include posts with zero votes                                                                      | Zero-count rows are included                                                             |
|                   INNER JOIN (default) | Only include posts that have at least one matching vote row                                        | Rows without votes excluded                                                              |

## Best practices and tips

* Always inspect generated SQL when debugging: `str(query)` or `query.statement`.
* Use `isouter=True` for left outer joins to include items without matches.
* Set `orm_mode = True` on Pydantic models that accept ORM objects.
* Ensure your response\_model exactly matches the keys, nesting, and capitalization of the returned data.
* If returning ORM instances directly, prefer response models designed for ORM dataclasses; when returning dicts, use plain Pydantic models.

## Links and references

* [SQLAlchemy ORM Query API](https://docs.sqlalchemy.org/en/14/orm/query.html)
* [SQLAlchemy func and aggregates](https://docs.sqlalchemy.org/en/14/core/functions.html)
* [FastAPI response models and Pydantic](https://fastapi.tiangolo.com/tutorial/response-model/)
* [Pydantic orm\_mode documentation](https://pydantic-docs.helpmanual.io/usage/models/#orm-mode)

Summary

* Build the SQLAlchemy query step-by-step: select entities, join (use `isouter=True` for LEFT JOIN), aggregate with `func`, `group_by`, then apply filters, limit, and offset.
* When returning results from joined queries, choose between updating/creating response models or flattening the result to match an existing schema.
* Always ensure Pydantic models match the exact structure returned by your endpoints to avoid validation errors.

- [Watch Video](https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi/module/ed782f8c-495c-4ff8-8703-c9ab0ab04a4d/lesson/ca189cde-8d5b-42d8-9e7b-88da83aea2c2)


# Jwt Token Basics

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Advanced-FastAPI/Jwt-Token-Basics/page

This article explains JWT token-based authentication, its structure, and how it enhances security and scalability in API development.

In this lesson, we explore one of the most critical aspects of API and application development: authentication. There are two primary methods to handle user authentication:

1. Session-based authentication – A session is stored on the backend server (or API) to track whether a user is logged in. This session data is typically saved in memory or in a database and remains active until the user logs out.
2. JWT token-based authentication – This stateless approach involves no backend storage for login sessions. Instead, the client stores a token containing all the necessary authentication details, and the API verifies this token to authenticate the user.

> **lightbulb** JWT token-based authentication simplifies horizontal scaling and reduces backend storage needs since the client is responsible for holding the token.

When a user logs in successfully via JWT, the API generates a token that the client retains. Every time the client needs to access a protected resource (for example, hitting the `/posts` endpoint), it sends the token in the request header. The API then validates the token to ensure the user is authenticated. The typical flow is as follows:

1. The client sends credentials (usually an email and password) to a login endpoint (e.g., `/login`).
2. The API validates the credentials and, if they are correct, generates a JWT token.
3. The client stores this token and includes it in the header for all subsequent requests to protected resources.
4. The API extracts and verifies the token. If the token is valid, the API responds with the requested data.

![The image illustrates the process of JWT token authentication, showing the interaction between a client and an API, including login, token issuance, and data access.](https://kodekloud.com/kk-media/image/upload/v1752883327/notes-assets/images/Python-API-Development-with-FastAPI-Jwt-Token-Basics/jwt-token-authentication-process.jpg)

The API does not maintain any session state; token validation alone confirms that the user is authenticated.

## JWT Token Structure

A JWT token is comprised of three parts separated by dots: the header, the payload, and the signature. Although the token is just a string, it carries structured data essential for authentication.

### 1. Header

The header contains metadata about the token, such as the token type and the algorithm used for signing. A typical header looks like this:

```python theme={null}
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### 2. Payload

The payload includes the actual data (claims) of the token. This can include non-sensitive information such as the user’s ID, name, or role. It is important to note that the payload is not encrypted, so sensitive data (like passwords) should never be stored here.

```python theme={null}
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022
}
```

You might also include additional metadata like user roles, but always keep the payload lightweight to reduce the overall token size.

### 3. Signature

The signature ensures the integrity of the token—it detects any tampering. To generate the signature, the API encodes the header and payload with a secret key (known only to the API) using a hashing algorithm (commonly HS256). In pseudocode, the process is as follows:

```python theme={null}
