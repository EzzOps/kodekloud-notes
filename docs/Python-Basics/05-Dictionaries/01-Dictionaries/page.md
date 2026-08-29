# Dictionaries

Source: https://notes.kodekloud.com/docs/Python-Basics/Dictionaries/Dictionaries/page

This article explains Python dictionaries, their structure, access methods, and how to modify their content for efficient data management.

Dictionaries are a powerful data type in Python that allow you to store and manage data in key-value pairs. They are especially useful when you need fast lookups for values based on unique keys. For example, if you want to associate user names with their corresponding account handles, a dictionary offers an ideal solution.

A dictionary is defined by enclosing key-value pairs in curly braces (), where each key is separated from its value by a colon.

```python theme={null}
usernames = {
    "lydia": "lydiahallie",
    "sarah": "sarah123",
    "max": "max_",
    "joe": "joejoe",
}
```

The code above creates a dictionary where each key (e.g., "lydia") is mapped to a value ("lydiahallie"). Unlike lists that use numeric indices, dictionaries use unique keys to access their corresponding values.

## Accessing Dictionary Elements

To retrieve a specific value in a dictionary, use its key inside square brackets. For instance, to obtain Sarah's username:

```python theme={null}
print(usernames["sarah"])  # Output: "sarah123"
```

> **triangle-alert** Attempting to access a key that does not exist in the dictionary will raise a KeyError.

## Common Dictionary Methods

Python dictionaries come with several built-in methods that simplify data handling. The key methods include:

* **keys()**: Returns an iterable view of all the keys.
* **values()**: Returns an iterable view of all the values.
* **items()**: Returns an iterable view of key-value pairs as tuples.

### Iterating Over Dictionaries

You can iterate over all key-value pairs using a loop. For example, to print each key alongside its corresponding value, you can use the following approaches:

Using the `keys()` method:

```python theme={null}
for key in usernames.keys():
    print(key + " - " + usernames[key])
```

Or, iterate directly over key-value pairs with the `items()` method:

```python theme={null}
for key, value in usernames.items():
    print(key + " - " + value)
```

To display only the values, use the `values()` method:

```python theme={null}
print(usernames.values())  # Output: dict_values(['lydiahallie', 'sarah123', 'max_', 'joejoe'])
```

## Modifying a Dictionary

You can easily update, add, or remove elements from a dictionary. Below are some common operations:

### Updating Values

To update an existing value, reference the key and assign a new value. For example, to update Max's username:

```python theme={null}
usernames["max"] = "max123"
print(usernames["max"])  # Output: "max123"
```

### Adding a New Key-Value Pair

To add a new entry, such as adding a user named Chloe with the username "chloe123", you can use the `update()` method:

```python theme={null}
usernames.update({"chloe": "chloe123"})
print(usernames)
```

### Deleting an Entry

If you need to remove an entry (for example, deleting Max's account), use the `del` statement:

```python theme={null}
del usernames["max"]
print(usernames)
```

Additionally, if you wish to remove all items, use the `clear()` method. For removing and returning the last inserted item, the `popitem()` method is available.

### Copying a Dictionary

To create a shallow copy of a dictionary, you can use the `copy()` method:

```python theme={null}
usernames_copy = usernames.copy()
```

## Summary

In this lesson, we explored Python dictionaries, discussing their structure, how to access elements, and the various methods available to modify dictionary content. Mastering dictionaries is essential for efficient data management in Python. Happy coding!

- [Watch Video](https://learn.kodekloud.com/user/courses/python-basics/module/999967d9-7cca-48f8-893c-5e61014671f8/lesson/79d5e64c-a3cb-4953-a956-0fbb17bc2266)
