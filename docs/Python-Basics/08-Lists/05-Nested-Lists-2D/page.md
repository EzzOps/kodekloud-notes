# Nested Lists 2D

Source: https://notes.kodekloud.com/docs/Python-Basics/Lists/Nested-Lists-2D/page

This article explains two-dimensional lists in Python, focusing on their structure, access methods, and practical applications like representing classroom layouts.

So far, we've explored simple lists that hold single values. Now, let's dive into two-dimensional (2D) lists—lists whose elements are themselves lists. This structure is especially useful for representing more complex data, such as a classroom layout where students are organized in rows.

<Callout icon="lightbulb">
  A 2D list (or matrix) in Python represents a grid-like structure where each element of an outer list is itself a list. This is ideal for modeling arrangements like classroom rows or grids.
</Callout>

## Representing a Classroom with a 2D List

Imagine a classroom arranged in rows with four students per row. In Python, you can represent this structure with a 2D list where each sublist corresponds to a row of students:

```python theme={null}
classroom = [
    ["Sam", "Max", "Joe", "Anne"],
    ["Sofie", "Lisa", "Tim", "Sasha"],
    ["Claire", "Sara", "Leo", "Kim"],
    ["Zoe", "Guy", "Anna", "Eva"],
]
```

## Accessing Elements in a 2D List

To retrieve a specific student's name from the classroom, you need to determine their row and then the position within that row. For example, to access the student "Sara":

1. "Sara" is in the third row. Since Python indexing starts at 0, the third row is at index 2.
2. Within that row, "Sara" is the second element (index 1).

Here's how you can access "Sara" from the 2D list:

```python theme={null}
