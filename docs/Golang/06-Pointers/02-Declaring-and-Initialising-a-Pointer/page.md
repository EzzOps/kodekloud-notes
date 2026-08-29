# Declaring and Initialising a Pointer

Source: https://notes.kodekloud.com/docs/Golang/Pointers/Declaring-and-Initialising-a-Pointer/page

This article explores how to declare and initialize pointers in Go for efficient memory management.

In this article, we explore how to declare and initialize pointers in Go. Understanding pointers is essential for managing memory addresses directly, which can lead to more efficient code.

## Declaring a Pointer

A pointer holds the memory address of a variable. In Go, you can declare a pointer using the following syntax:

```plaintext theme={null}
var <pointer_name> *<data_type>
```

For example, to declare an integer pointer, you would write:

```plaintext theme={null}
var ptr_i *int
```

Similarly, you can declare a string pointer alongside an integer pointer:

```plaintext theme={null}
var ptr_i *int
var ptr_s *string
```

## Complete Example: Declaring Pointers

Below is a complete example illustrating the declaration of an integer pointer and a string pointer within the `main` function. When executed, the pointers will display their zero value, which is `nil`.

```go theme={null}
package main

import "fmt"

func main() {
    var i *int
    var s *string
    fmt.Println(i)
    fmt.Println(s)
}
```

<Callout icon="lightbulb">
  The output confirms that uninitialized pointers in Go have the `nil` value.
</Callout>

## Initialising a Pointer

Once a pointer is declared, you must initialize it by assigning the memory address of an existing variable. There are several methods to do this.

### Method 1: Using the Address Operator (&)

The first method uses the address operator (`&`) to assign the pointer the address of a variable:

```plaintext theme={null}
var <pointer_name> *<data_type> = &<variable_name>
```

For instance, to initialize a pointer to an integer:

```plaintext theme={null}
i := 10
var ptr_i *int = &i
```

Here, the variable `i` has a value of 10, and its memory address is stored in `ptr_i`.

### Method 2: Type Inference

Go supports type inference, which allows you to omit the explicit data type. The compiler automatically determines the correct type:

```plaintext theme={null}
var <pointer_name> = &<variable_name>
```

For example, to initialize a pointer to a string variable:

```go theme={null}
s := "hello"
var ptr_s = &s
```

### Method 3: Shorthand Declaration Operator

You can also use the shorthand declaration operator to initialize a pointer. This approach eliminates the need for the `var` keyword:

```plaintext theme={null}
<pointer_name> := &<variable_name>
```

For example:

```go theme={null}
s := "hello"
ptr_s := &s
```

## Complete Example: Initialising Pointers

Below is an example that demonstrates all three methods together. In this program, we declare a string variable `s` and initialize three pointers (`a`, `b`, and `c`) to store its address. All three pointers will reference the same memory location.

```go theme={null}
package main

import "fmt"

func main() {
    s := "hello"
    var b *string = &s
    fmt.Println(b)
    var a = &s
    fmt.Println(a)
    c := &s
    fmt.Println(c)
}
```

When you run this program, you should see three identical memory addresses as output:

```plaintext theme={null}
>>> go run main.go
0xc000010230
0xc000010230
0xc000010230
```

<Callout icon="lightbulb">
  Pointers store the memory address of another variable, allowing you to manipulate data directly.
</Callout>

That concludes our guide on declaring and initializing pointers in Go. Keep exploring to further enhance your Go programming skills!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/golang/module/ee351938-02d0-4200-ac8f-78b0da517e29/lesson/6a07bc95-8f34-42c2-892d-c511bec14bf7" />
</CardGroup>
