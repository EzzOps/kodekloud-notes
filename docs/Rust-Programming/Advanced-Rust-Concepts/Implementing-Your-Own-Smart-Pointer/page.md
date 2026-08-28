# Non-generic functions to print specific types
def print_integer(num: int):
    print(num)

def print_string(text: str):
    print(text)

# Generic function to print any type of data
def print_item(item):
    print(item)

# Usage
print_integer(5)
print_string("Hello")
print_item(5)
print_item("Hello")
```

Using a generic function like `print_item` prevents code redundancy and maintains consistency. Now, let's take a look at a Rust implementation that returns the first element of a slice regardless of its type:

```rust theme={null}
fn first_element<T>(list: &[T]) -> Option<&T> {
    if list.is_empty() {
        None
    } else {
        Some(&list[0])
    }
}

fn main() {
    let numbers: Vec<i32> = vec![1, 2, 3];
    let words: Vec<&str> = vec!["apple", "banana", "cherry"];

    if let Some(first) = first_element(&numbers) {
        println!("First number: {}", first);
    }
    
    if let Some(first) = first_element(&words) {
        println!("First word: {}", first);
    }
}
```

In this Rust example, the generic type parameter `T` allows the function to handle slices containing any type. The return type is `Option<&T>`, which gracefully deals with the possibility of an empty slice.

<Frame>
  ![The image explains the benefits of using generics, highlighting two points: avoiding code duplication and improving flexibility and robustness.](https://kodekloud.com/kk-media/image/upload/v1752883763/notes-assets/images/Rust-Programming-Generic-Types/generics-benefits-code-duplication-flexibility.jpg)
</Frame>

## Generic Structs

Rust structs also support generics, letting you define data structures that work with any type. Consider a struct that represents a pair of values:

```rust theme={null}
// Using generics in structs
struct Pair<T> {
    first: T,
    second: T,
}

fn main() {
    let int_pair = Pair { first: 1, second: 2 };
    let float_pair = Pair { first: 1.0, second: 2.0 };
    let string_pair = Pair { 
        first: String::from("Hello"), 
        second: String::from("World") 
    };

    println!("Integer Pair: {}, {}", int_pair.first, int_pair.second);
    println!("Float Pair: {}, {}", float_pair.first, float_pair.second);
    println!("String Pair: {}, {}", string_pair.first, string_pair.second);
}
```

<Frame>
  ![The image is a slide titled "Using Generics in Structs," with a note stating that Rust structs can be generic to store any type of value.](https://kodekloud.com/kk-media/image/upload/v1752883764/notes-assets/images/Rust-Programming-Generic-Types/using-generics-in-structs-rust.jpg)
</Frame>

The type parameter `T` in the `Pair` struct allows you to store any type, and Rust infers the specific type based on the provided values.

### Mixing Generic and Concrete Fields

You may sometimes need to mix generic fields with fields that have fixed types. For example, if you want to add a mandatory `i32` field to your struct, you can do so while still using generics:

```rust theme={null}
struct Pair<T> {
    first: T,
    second: T,
    third: i32,
}

fn main() {
    let int_pair = Pair { first: 1, second: 2, third: 3 };
    println!("Integer Pair: ({}, {}, {})", int_pair.first, int_pair.second, int_pair.third);
}
```

In this example, while `first` and `second` remain generic, `third` is explicitly defined as an `i32`.

## Generic Enums

Enums in Rust can also leverage generics to represent multiple types. For instance, consider a custom `Result` type that encapsulates either a success result or an error message:

```rust theme={null}
enum MyResult<T, E> {
    Ok(T),
    Err(E),
}

fn main() {
    let success: MyResult<i32, &str> = MyResult::Ok(200);
    let error: MyResult<i32, &str> = MyResult::Err("Something went wrong");

    match success {
        MyResult::Ok(value) => println!("Success with value: {}", value),
        MyResult::Err(err) => println!("Error: {}", err),
    }

    match error {
        MyResult::Ok(value) => println!("Success with value: {}", value),
        MyResult::Err(err) => println!("Error: {}", err),
    }
}
```

Here, `T` represents the type for a successful result and `E` represents the error type, providing a robust way to handle different outcomes.

## Generic Methods

Generic methods on structs allow you to implement functionality that works across various types. For example, consider a method to swap the two values in a `Pair` struct. This method consumes the original struct and returns a new one with swapped values:

```rust theme={null}
struct Pair<T> {
    first: T,
    second: T,
}

impl<T> Pair<T> {
    fn swap(self) -> Pair<T> {
        Pair {
            first: self.second,
            second: self.first,
        }
    }
}

fn main() {
    let int_pair = Pair { first: 10, second: 20 };
    let swapped_pair = int_pair.swap();
    println!("Swapped Pair: ({}, {})", swapped_pair.first, swapped_pair.second);
}
```

Each method call works for any instantiation of `Pair<T>`, making your code more versatile.

## Performance Considerations

<Callout icon="lightbulb">
  Rust uses a process called monomorphization during compilation to generate type-specific versions of your generic code. This ensures that there is no runtime overhead, and your generic code performs as efficiently as if it were written specifically for each type.
</Callout>

## Conclusion

Generics in Rust enable you to create versatile, clean, and high-performance code. By leveraging generics in functions, structs, enums, and methods, you can reduce duplication and build robust libraries that work seamlessly with various data types.

For further reading, check out these resources:

* [Rust Programming Language](https://www.rust-lang.org/)
* [Rust Documentation](https://doc.rust-lang.org/)
* [Learning Rust](https://www.rust-lang.org/learn)

Embrace generics to write code that adapts to your needs without compromising on performance.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/rust/module/37d4032f-c90d-43ee-a0cd-981b95ab22b0/lesson/5806e4de-49f2-4b17-be72-c528e394e2c0" />
</CardGroup>


# Implementing Your Own Smart Pointer

Source: https://notes.kodekloud.com/docs/Rust-Programming/Advanced-Rust-Concepts/Implementing-Your-Own-Smart-Pointer/page

Learn to create a custom smart pointer in Rust by implementing the Deref and Drop traits for enhanced resource management.

In this lesson, you’ll learn how to create a custom smart pointer in Rust. Smart pointers are specialized data structures that not only store memory addresses but also manage the underlying resources. They offer advanced features such as reference counting and interior mutability, which enhance resource management. Although Rust provides robust smart pointers like Box\<T>, Rc\<T>, and RefCell\<T> in its standard library, there are scenarios where a customized solution is necessary.

We will walk you through the process of building a custom smart pointer by implementing two critical traits: Deref and Drop. The Deref trait allows your smart pointer to behave like a regular reference, while the Drop trait ensures automatic resource cleanup when the pointer goes out of scope.

***

## The Deref Trait

The Deref trait enables your smart pointer to be used like any other reference. By implementing Deref, you can use the dereference operator (`*`) to access the data inside the smart pointer, making it compatible in contexts where a regular reference is needed.

<Frame>
  ![The image is a diagram explaining the implementation of the Deref trait, showing a "MySmartPointer" containing "Data" that points to "Underlying Data" and interacts with the "Deref Trait."](https://kodekloud.com/kk-media/image/upload/v1752883764/notes-assets/images/Rust-Programming-Implementing-Your-Own-Smart-Pointer/deref-trait-mysmartpointer-diagram.jpg)
</Frame>

Consider the following example where we define a generic tuple struct, `MySmartPointer\<T>`, that wraps around a value of any type `T`. The implementation block includes a constructor method that initializes the smart pointer:

```rust theme={null}
struct MySmartPointer<T>(T);

impl<T> MySmartPointer<T> {
    fn new(x: T) -> MySmartPointer<T> {
        MySmartPointer(x)
    }
}
```

Without implementing the Deref trait, using the dereference operator (`*`) on an instance of `MySmartPointer` would not be possible. Below, we implement the Deref trait so that our custom smart pointer behaves like a standard reference:

```rust theme={null}
use std::ops::Deref; // Import the Deref trait

struct MySmartPointer<T>(T);

impl<T> Deref for MySmartPointer<T> {
    type Target = T; // Specify the type returned on dereferencing

    fn deref(&self) -> &T {
        &self.0 // Return a reference to the inner value
    }
}

impl<T> MySmartPointer<T> {
    fn new(x: T) -> MySmartPointer<T> {
        MySmartPointer(x)
    }
}

fn main() {
    // Create a smart pointer holding an integer
    let int_pointer: MySmartPointer<i32> = MySmartPointer::new(42);

    // Create a smart pointer holding a string
    let string_pointer: MySmartPointer<String> = MySmartPointer::new(String::from("Hello, Rust!"));

    // Using the dereference operator to access the inner value
    println!("Integer pointer created with value: {:?}", *int_pointer);
    // Alternatively, direct field access for tuple structs
    println!("String pointer created with value: {:?}", string_pointer.0);
}
```

By implementing Deref, our custom smart pointer can be seamlessly passed to functions and contexts that expect a regular reference, enhancing code reusability and maintainability.

***

## The Drop Trait

The Drop trait is essential for defining custom behavior when a smart pointer goes out of scope. It allows you to implement cleanup logic for resources such as memory, file handles, or network connections.

<Frame>
  ![The image is titled "The Drop Trait – Managing Cleanup" and features a diagram of a smart pointer managing memory, file handles, and network connections.](https://kodekloud.com/kk-media/image/upload/v1752883765/notes-assets/images/Rust-Programming-Implementing-Your-Own-Smart-Pointer/drop-trait-managing-cleanup-diagram.jpg)
</Frame>

In the following example, we extend our previous implementation by adding a custom Drop implementation. When an instance of `MySmartPointer` is dropped, the `drop` method is triggered, which in this example prints a message to indicate that the pointer is being cleaned up.

```rust theme={null}
use std::ops::{Deref, Drop};

struct MySmartPointer<T>(T);

impl<T> Deref for MySmartPointer<T> {
    type Target = T;

    fn deref(&self) -> &T {
        &self.0
    }
}

impl<T> Drop for MySmartPointer<T> {
    fn drop(&mut self) {
        println!("Dropping MySmartPointer!");
    }
}

impl<T> MySmartPointer<T> {
    fn new(x: T) -> MySmartPointer<T> {
        MySmartPointer(x)
    }
}

fn main() {
    let x: i32 = 5;
    // Create an instance of MySmartPointer. When 'y' goes out of scope, the drop method is called.
    let y: MySmartPointer<i32> = MySmartPointer::new(x);
    println!("Value of y: {}", *y);
}
```

When the variable `y` falls out of scope at the end of `main`, Rust automatically calls the `drop` method, ensuring that any associated resources are properly released.

<Callout icon="lightbulb">
  The sample console output for this code is:

  Value of y: 5\
  Dropping MySmartPointer!
</Callout>

***

## Summary

By implementing the Deref trait, your custom smart pointer works seamlessly as a regular reference, simplifying its integration with functions that expect references. Meanwhile, the Drop trait guarantees automatic cleanup of resources when the smart pointer goes out of scope, ensuring efficient resource management.

<Frame>
  ![The image is a conclusion slide with three key points about smart pointers, emphasizing flexibility, resource management, and control over memory. It features a gradient background and is copyrighted by KodeKloud.](https://kodekloud.com/kk-media/image/upload/v1752883767/notes-assets/images/Rust-Programming-Implementing-Your-Own-Smart-Pointer/smart-pointers-conclusion-slide.jpg)
</Frame>

Together, these traits offer you fine-grained control over memory and resource management in Rust, paving the way for more advanced and safe programming paradigms.

***

## Additional Resources

* [Rust Official Documentation](https://www.rust-lang.org/learn)
* [Understanding Ownership in Rust](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html)

For further reading on implementing custom smart pointers and advanced memory management techniques, explore additional tutorials available in the [Rust Programming Language Book](https://doc.rust-lang.org/book/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/rust/module/37d4032f-c90d-43ee-a0cd-981b95ab22b0/lesson/8b5a96f3-ce71-459b-8bff-e068e4bbb6a8" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/rust/module/37d4032f-c90d-43ee-a0cd-981b95ab22b0/lesson/0d9e02ac-0cc6-4e47-9a30-5443c6706575" />
</CardGroup>
