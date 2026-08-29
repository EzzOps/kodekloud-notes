# Logical Operators

Source: https://notes.kodekloud.com/docs/Golang/Operators-and-Control-Flow/Logical-Operators/page

This article provides an in-depth look at common logical operators and demonstrates their usage with practical Go code examples.

Logical operators, alongside comparison and arithmetic operators, play a crucial role in controlling the flow of your programs by evaluating Boolean expressions and combining multiple conditions. This article provides an in-depth look at common logical operators and demonstrates their usage with practical Go code examples.

Below is an image illustrating the three basic logical operators:

<Frame>
  ![The image illustrates three logical operators: AND (&&), OR (||), and NOT (!), used in programming for conditional logic.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877743/notes-assets/images/Golang-Logical-Operators/frame_50.jpg)
</Frame>

<Callout icon="lightbulb">
  Logical operators are fundamental in programming as they allow developers to construct complex logical statements by combining simpler Boolean expressions.
</Callout>

## AND Operator (&&)

The AND operator, represented by two ampersand symbols (&&), returns true only when both operands are true. If either condition is false, the overall expression evaluates to false.

### Example

```go theme={null}
package main

import "fmt"

func main() {
    var x int = 10
    fmt.Println((x < 100) && (x < 200)) // Both conditions are true, so the result is true.
    fmt.Println((x < 300) && (x < 0))     // One condition is false, so the result is false.
}
```

In the first print statement, both conditions (x \< 100 and x \< 200) are true. In the second print statement, though x \< 300 is true, x \< 0 is false, leading to a false outcome.

## OR Operator (||)

The OR operator is denoted by two vertical bars (||) and returns true if at least one of the expressions is true. It only yields false when both expressions are false.

### Example

```go theme={null}
package main

import "fmt"

func main() {
    var x int = 10
    fmt.Println((x < 0) || (x < 200))  // One condition is true, so the result is true.
    fmt.Println((x < 0) || (x > 200))  // Both conditions are false, so the result is false.
}
```

**Expected Output:**

```Go theme={null}
>>> go run main.go
true
false
```

In the first print statement, even though x is not less than 0, `x < 200` is true, resulting in a true expression. In the second print statement, both conditions evaluate to false, so the overall result is false.

## NOT Operator (!)

The NOT operator is a unary operator represented by the exclamation mark (!) that inverts the Boolean value of an expression. In other words, if an expression evaluates to true, applying the NOT operator will change it to false, and vice versa.

### Example

```go theme={null}
package main

import "fmt"

func main() {
    var x, y int = 10, 20
    fmt.Println(!(x > y)) // x > y is false; applying NOT converts it to true.
    fmt.Println(!true)    // Inverts true to false.
    fmt.Println(!false)   // Inverts false to true.
}
```

In this example, `x > y` is false because 10 is not greater than 20. The NOT operator inverts the false value to true. Similarly, using the NOT operator on true results in false and on false results in true.

<Callout icon="lightbulb">
  Understand how logical operators can be combined to form more complex conditions in your programs, making your code more dynamic and efficient.
</Callout>

This article has covered the fundamental logical operators in programming. For a deeper understanding, consider exploring additional practical exercises and more advanced topics.

For further reference, check out:

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/golang/module/036484d6-1e16-46e2-908d-77e545bde2bf/lesson/f28365ff-df82-4492-a0af-67963501ba18" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/golang/module/036484d6-1e16-46e2-908d-77e545bde2bf/lesson/1b1eb331-0c2e-4aa9-9bc4-b995ecb7130d" />
</CardGroup>
