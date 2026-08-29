# JSON PATH Lists

Source: https://notes.kodekloud.com/docs/JSON-Path-Test-Free-Course/Lesson/JSON-PATH-Lists/page

Learn to use JSONPath expressions for querying, filtering, and slicing JSON arrays effectively.

In this guide, you'll learn how to leverage JSONPath expressions to query, filter, and slice JSON arrays effectively. JSONPath is a powerful query language for JSON, enabling developers to pinpoint data within nested structures, perform conditional selections, and iterate through collections.

## 1. Defining an Array in JSON

Consider a JSON document representing a set of users:

```json theme={null}
{
  "users": [
    { "id": 1, "name": "Alice",   "age": 30 },
    { "id": 2, "name": "Bob",     "age": 24 },
    { "id": 3, "name": "Charlie", "age": 29 },
    { "id": 4, "name": "Diana",   "age": 22 }
  ]
}
```

Here, `users` is an array of objects. Each object has `id`, `name`, and `age` properties.

## 2. Accessing Array Elements

### 2.1 By Index

Pick a single element by its zero-based index:

```bash theme={null}
$ jp query '$.users[0]'
```

Returns:

```json theme={null}
{ "id": 1, "name": "Alice", "age": 30 }
```

```bash theme={null}
$ jp query '$.users[2]'
```

Returns:

```json theme={null}
{ "id": 3, "name": "Charlie", "age": 29 }
```

### 2.2 Using Wildcard

Retrieve **all** users with the wildcard `*`:

```bash theme={null}
$ jp query '$.users[*]'
```

Returns:

```json theme={null}
[
  { "id": 1, "name": "Alice",   "age": 30 },
  { "id": 2, "name": "Bob",     "age": 24 },
  { "id": 3, "name": "Charlie", "age": 29 },
  { "id": 4, "name": "Diana",   "age": 22 }
]
```

### 2.3 Slicing the Array

Extract a range of elements with slice notation `[start:end]`:

```bash theme={null}
$ jp query '$.users[1:3]'
```

Returns:

```json theme={null}
[
  { "id": 2, "name": "Bob",   "age": 24 },
  { "id": 3, "name": "Charlie", "age": 29 }
]
```

You can omit `start` or `end`:

* `[:2]` → first two elements
* `[2:]` → from the third element onward

> **lightbulb** JSONPath uses zero-based indices. Negative indices or step values (e.g., `[::2]`) are not supported in all implementations.

## 3. Filtering Array Elements

Apply a filter expression to select items matching a condition:

```bash theme={null}
$ jp query '$.users[?(@.age >= 25)]'
```

Returns users aged 25 or older:

```json theme={null}
[
  { "id": 1, "name": "Alice",   "age": 30 },
  { "id": 3, "name": "Charlie", "age": 29 }
]
```

### 3.1 Accessing Properties of Filtered Results

Chain selectors to extract specific fields:

```bash theme={null}
$ jp query '$.users[?(@.age >= 25)].name'
```

Returns:

```json theme={null}
["Alice", "Charlie"]
```

## 4. Nested Arrays

Given nested arrays, you can flatten or traverse them:

```json theme={null}
{
  "groups": [
    {
      "groupName": "Admins",
      "members": ["Alice", "Bob"]
    },
    {
      "groupName": "Developers",
      "members": ["Charlie", "Diana"]
    }
  ]
}
```

List all members across every group:

```bash theme={null}
$ jp query '$.groups[*].members[*]'
```

Returns:

```json theme={null}
["Alice", "Bob", "Charlie", "Diana"]
```

## 5. Summary of JSONPath List Operators

| Operator       | Description                                       | Example                  |
| -------------- | ------------------------------------------------- | ------------------------ |
| `[index]`      | Selects a single element by position              | `$.users[0]`             |
| `[*]`          | Wildcard to select all elements                   | `$.users[*]`             |
| `[start:end]`  | Slice array between `start` (inclusive) and `end` | `$.users[1:3]`           |
| `[?()]`        | Filter by expression                              | `$.users[?(@.age>25)]`   |
| Chaining (`.`) | Traverse nested arrays or access properties       | `$.groups[*].members[*]` |

By mastering these operators, you can query, transform, and navigate JSON arrays with precision.

## Links and References

* [JSONPath Specification](https://goessner.net/articles/JsonPath/)
* [Online JSONPath Tester](https://jsonpath.com/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Terraform Registry](https://registry.terraform.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/json-path-test-free-course/module/114e6dee-a9f2-49f3-a0c6-cdfb92f74310/lesson/c94d843c-16dd-45e5-bda6-c318f29d16d5)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/json-path-test-free-course/module/114e6dee-a9f2-49f3-a0c6-cdfb92f74310/lesson/0b357686-dc66-41ba-9c59-845dadec6773)
