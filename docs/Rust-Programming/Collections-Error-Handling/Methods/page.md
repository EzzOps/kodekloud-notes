# Methods

Source: https://notes.kodekloud.com/docs/Rust-Programming/Collections-Error-Handling/Methods/page

This lesson explores methods in Rust, focusing on their definition, usage, and enhancement for organized and maintainable code.

In this lesson, we explore methods in Rust, which are functions associated with structs, enums, or traits. Methods allow you to define behavior specific to custom data types, helping to keep your code organized and encapsulated. By the end of this guide, you'll know how to define, use, and enhance methods in Rust for more maintainable and idiomatic code.

## What Are Methods?

Methods in Rust are functions linked to a specific data type. They offer a natural, organized way to operate on instances of that type. To define a method, use the `impl` keyword followed by the name of the struct and enclose the method definitions within curly braces. Below is an example of a basic method definition:

```rust theme={null}
impl StructName {
    fn method_name(&self) {
        // Method body
    }
}
```

The parameter `&self` is shorthand for `self: &Self`, representing a reference to the instance on which the method is called.

## Example: Defining Methods for a Book Struct

Consider a `Book` struct with fields for a title and a number of pages. We will define various methods to calculate reading time (assuming one page per minute), compare the page count between books, and create a default book instance.

```rust theme={null}
struct Book {
    title: String,
    pages: u32,
}

impl Book {
    // Method to calculate reading time assuming 1 page per minute
    fn reading_time(&self) -> u32 {
        self.pages
    }

    // Method to check if one book has more pages than another
    fn has_more_pages_than(&self, other: &Book) -> bool {
        self.pages > other.pages
    }

    // Associated function (not a method) to create a book with a default title and given pages
    fn default_book(pages: u32) -> Book {
        Book {
            title: String::from("Untitled"),
            pages,
        }
    }
}
```

In the code above, the first two functions require `&self` because they act on an instance of `Book`. The function `default_book` does not take `self` as a parameter, which is why it's called an associated function and is invoked using the `::` syntax.

### Using the Book Methods in main()

Here is an example showing how to create `Book` instances and call the defined methods:

```rust theme={null}
fn main() {
    let book1 = Book {
        title: String::from("The Rust Programming Language"),
        pages: 500,
    };

    let book2 = Book {
        title: String::from("Learning Rust"),
        pages: 300,
    };

    let book3 = Book {
        title: String::from("Rust in Action"),
        pages: 600,
    };

    println!(
        "The reading time for '{}' is {} minutes.",
        book1.title,
        book1.reading_time()
    );
    
    println!(
        "Does '{}' have more pages than '{}'? {}",
        book1.title,
        book2.title,
        book1.has_more_pages_than(&book2)
    );

    println!(
        "Does '{}' have more pages than '{}'? {}",
        book1.title,
        book3.title,
        book1.has_more_pages_than(&book3)
    );

    let default_book = Book::default_book(150);
    println!(
        "Default Book: '{}' with {} pages",
        default_book.title,
        default_book.pages
    );
}
```

<Callout icon="lightbulb">
  This example demonstrates how methods encapsulate behavior within a struct, enhancing code readability and reusability.
</Callout>

## Calling Methods with Dot Notation

Rust allows you to call methods on struct instances using dot notation. For instance, to calculate the reading time for a book, you simply call the method on the instance:

```rust theme={null}
fn main() {
    let book1 = Book {
        title: String::from("The Rust Programming Language"),
        pages: 500,
    };

    println!(
        "The reading time for '{}' is {} minutes.",
        book1.title,
        book1.reading_time()
    );
}
```

This snippet clearly showcases how to use the `reading_time` method to determine the reading duration based on the page count.

## Mutable Methods

When a method needs to modify the instance it is called on, it takes `&mut self` as a parameter. Consider the following example where the `set_title` method updates the book's title:

```rust theme={null}
struct Book {
    title: String,
    pages: u32,
}

impl Book {
    fn set_title(&mut self, new_title: String) {
        self.title = new_title;
    }
}

fn main() {
    let mut book1 = Book {
        title: String::from("Old Title"),
        pages: 250,
    };

    book1.set_title(String::from("New Title"));
    println!("The new title of the book is '{}'.", book1.title);
}
```

Here, the `set_title` method uses a mutable reference (`&mut self`) to modify the `title` field. In the `main` function, note that `book1` must be declared as mutable (`mut`) to allow this modification.

## Implementing the Display Trait

Implementing the `Display` trait for a custom struct enables formatted output using the `{}` placeholder. The following is an example using a `Point` struct:

```rust theme={null}
use std::fmt;

struct Point {
    x: i32,
    y: i32,
}

impl fmt::Display for Point {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
    }
}

fn main() {
    let p = Point { x: 5, y: 10 };
    println!("{}", p);
}
```

In this example, the `fmt` method defines custom formatting for `Point`. The `println!` macro then uses this implementation to display the point in the desired format.

<Callout icon="lightbulb">
  Implementing traits like `Display` not only improves output readability but also enhances the overall flexibility of your custom types.
</Callout>

## Summary

* Methods in Rust are defined within an `impl` block linked to a specific type.
* Functions that require access to an instance use `&self`, while functions without `self` are associated functions called with the `::` syntax.
* Mutable methods require the use of `&mut self` to indicate that the instance can be modified.
* The `Display` trait can be implemented for custom formatting, making your types more versatile in formatted output.

These practices help in writing organized, reusable, and idiomatic Rust code. Happy coding!

## Further Reading

* [The Rust Programming Language Book](https://doc.rust-lang.org/book/)
* [Rust Documentation](https://doc.rust-lang.org/)
* [Rust by Example](https://doc.rust-lang.org/rust-by-example/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/rust/module/29fbe393-bae3-4a16-8fc5-a854a2400daa/lesson/7a387db0-6123-4eb5-adc4-e4445d308fd3" />
</CardGroup>
