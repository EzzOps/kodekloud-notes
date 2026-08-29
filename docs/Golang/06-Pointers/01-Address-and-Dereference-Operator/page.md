# Address and Dereference Operator

Source: https://notes.kodekloud.com/docs/Golang/Pointers/Address-and-Dereference-Operator/page

This article explores the Address and Dereference Operators in Go for working with pointers and managing memory.

In this article, we explore two essential operators for working with pointers in Go: the Address Operator and the Dereference Operator.

A pointer in Go holds the memory address of a variable. To obtain this memory address, you use the Address Operator, represented by the ampersand (&). Conversely, the Dereference Operator, denoted by an asterisk (\*), accesses the value stored at that memory address.

Consider the following example. Suppose we have a variable x assigned the value 77. The variable x is stored at a specific memory location. When you apply the Address Operator (i.e., \&x), it returns the memory address of x (for example, 0x0301). Placing the Dereference Operator in front of the memory address (\*0x0301) retrieves the value stored at that location, which is 77.

```plaintext theme={null}
x := 77
&x = 0x0301
*0x0301 = 77
```

<Callout icon="lightbulb">
  In this example, the memory address (e.g., 0x0301) is illustrative. Actual memory addresses will vary when you run the program.
</Callout>

## A Practical Example in a Go Program

Let's see how these operators are used in a simple Go program. In this example, we define the main function, create a variable i with the value 10, and then print both the type and value of its address. We further demonstrate dereferencing the address of i to print its original value.

```go theme={null}
package main
import "fmt"

func main() {
    i := 10
    // Print the type and value of the address of i.
    fmt.Printf("%T %v\n", &i, &i)
    // Dereference the address to obtain and print the value stored at that address.
    fmt.Printf("%T %v\n", *(&i), *(&i))
}
```

When you run this program, the output is as follows:

```plaintext theme={null}
>>> go run main.go
*int 0xc00018c008
int 10
```

The first output line shows the type of \&i as \*int (a pointer to an integer) along with its memory address. The second output line demonstrates that dereferencing this address using \*(\&i) retrieves the integer value 10.

<Callout icon="lightbulb">
  Notice the distinction between the asterisk used in the Dereference Operator and the asterisk seen in the type output (\*int). They serve different purposes in the code and the output.
</Callout>

## Conclusion

This article demonstrated how pointers work in Go with the Address and Dereference Operators. Understanding these concepts is crucial for effectively managing memory and performing low-level operations in Go.

Happy coding, and check out more [Go tutorials](https://golang.org/doc/) for further learning!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/golang/module/ee351938-02d0-4200-ac8f-78b0da517e29/lesson/70cddb52-ab71-441b-9889-f44be4844ad9" />
</CardGroup>
