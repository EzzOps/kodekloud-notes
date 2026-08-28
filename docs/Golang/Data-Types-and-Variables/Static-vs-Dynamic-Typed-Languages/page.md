# Static vs Dynamic Typed Languages

Source: https://notes.kodekloud.com/docs/Golang/Data-Types-and-Variables/Static-vs-Dynamic-Typed-Languages/page

This article explores static and dynamic typed programming languages and discusses Gos unique position within this landscape.

This article explores the key characteristics of static and dynamic typed programming languages and explains where Go stands in this landscape. By understanding these concepts, you can make informed decisions when choosing the right language for your project.

## Statically Typed Languages

Statically typed languages enforce data type rules at compile time. If the data types are used incorrectly, the compiler throws an error. Common examples include C, C++, and Java. Consider the following simple C++ example:

We define a function named add that takes two integers as inputs and prints their sum. When two numbers are provided, the function works as expected. If a number and a string are passed as arguments, the compiler responds with an error.

```cpp theme={null}
void add(int a, int b) {
    cout << a + b;
}

add(1, 2) => 3
add(1, "two") => ERROR
```

<Callout icon="lightbulb">
  The compile-time error in C++ occurs because a mismatched data type is used, ensuring better data integrity and optimized performance.
</Callout>

## Dynamically Typed Languages

Dynamically typed languages determine data types at runtime, so type checking occurs while the program is running rather than during compilation. Python and JavaScript are popular examples in this category. Below is the same add function implemented in JavaScript:

```javascript theme={null}
function add(a, b) {
    return a + b;
}
```

When called with two numbers, the function returns their sum:

```javascript theme={null}
add(1, 2) => 3
```

However, if a number and a string are passed, JavaScript implicitly converts them:

```javascript theme={null}
add(1, "two") => "1two"
```

<Callout icon="triangle-alert">
  While dynamic typing offers flexibility, it can also lead to unintended behavior if the data types are not properly managed.
</Callout>

## Advantages of Each Typing System

Each typing system has its own benefits. Here is a summary of the key advantages:

* **Static Typing:**
  * Enhanced performance through compile-time optimizations.
  * Early bug detection with compile-time error checks.
  * Improved data integrity.

<Frame>
  ![The image lists advantages of static typing: better performance, bug detection by a compiler, and improved data integrity.](https://kodekloud.com/kk-media/image/upload/v1752877719/notes-assets/images/Golang-Static-vs-Dynamic-Typed-Languages/frame_150.jpg)
</Frame>

* **Dynamic Typing:**
  * Faster and more flexible code development.
  * A less rigid structure that can simplify development.
  * Generally, an easier learning curve for new developers.

<Frame>
  ![The image lists advantages of dynamic typing: faster code writing and generally less rigidity.](https://kodekloud.com/kk-media/image/upload/v1752877720/notes-assets/images/Golang-Static-vs-Dynamic-Typed-Languages/frame_160.jpg)
</Frame>

## Where Does Go Stand?

Go introduces a hybrid approach that combines the benefits of static typing with the ease of type inference. It is a statically typed, compiled language that allows the compiler to infer types when they are not explicitly declared by the programmer. This feature makes Go feel intuitive while maintaining the performance and safety of a statically typed language.

<Frame>
  ![The image describes Golang as a fast, statically typed, compiled language with type inference, featuring a cartoon gopher mascot.](https://kodekloud.com/kk-media/image/upload/v1752877722/notes-assets/images/Golang-Static-vs-Dynamic-Typed-Languages/frame_190.jpg)
</Frame>

Consider the following example of a simple Go program:

```go theme={null}
package main
import (
	"fmt"
)

func main() {
	name := "Lisa"
	fmt.Println(name)
}
```

When you run the program, it produces the following output:

```console theme={null}
>>> go run main.go
Lisa
```

In this example, the variable declaration uses Go's short variable declaration syntax, allowing the compiler to automatically infer the data type. This blend of explicit type checking and type inference gives developers the benefits of static typing along with a simplified syntax.

## Conclusion

In summary, this article compared statically and dynamically typed languages, highlighting the advantages of each approach. We then discussed how Go offers a unique combination of static typing and type inference, providing both robust compile-time error checking and a streamlined coding experience.

Try practicing what you've learned by exploring our available lab exercises and deepen your understanding of these concepts.

## Further Reading

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/golang/module/eeafa284-50db-4de2-a58a-759d3926fced/lesson/55ba8e39-f990-4c40-8bed-affc58a2289a" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/golang/module/eeafa284-50db-4de2-a58a-759d3926fced/lesson/36d73038-dc85-4e2f-b847-d15dbee4f7c9" />
</CardGroup>
