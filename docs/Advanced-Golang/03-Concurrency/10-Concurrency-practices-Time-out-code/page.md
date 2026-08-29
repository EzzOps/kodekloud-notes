# Concurrency practices Time out code

Source: https://notes.kodekloud.com/docs/Advanced-Golang/Concurrency/Concurrency-practices-Time-out-code/page

This tutorial explores implementing timeouts in Golang using the time.After function for responsive applications.

In this tutorial, we explore a popular concurrency practice in Golang: implementing timeouts using the `time.After` function. Many interactive applications need to respond within a specific time frame, and Golang's concurrency model provides a neat approach to control how long a request or process runs.

The `time.After` function waits for a specified duration and then sends the current time on its returned channel. Its signature is as follows:

```go theme={null}
func After(d Duration) <-chan Time
```

This function is extremely useful when incorporated into a select statement to implement blocking timeouts.

## Using time.After in a Select Statement

The following steps will guide you through creating a channel, launching a goroutine to send a value, and then using a select statement to either receive the value or trigger a timeout if the operation takes too long.

### Step 1: Creating a Channel and Launching a Goroutine

First, you create a channel and start a goroutine called `sendValue`, which sends a value over the channel:

```go theme={null}
package main

func main() {
    ch1 := make(chan int)
    go sendValue(ch1)
}
```

### Step 2: Defining the sendValue Function

Next, implement the `sendValue` function that sends a value (for instance, `10`) into the channel:

```go theme={null}
package main

func main() {
    ch1 := make(chan int)
    go sendValue(ch1)
}

func sendValue(ch1 chan int) {
    ch1 <- 10
}
```

### Step 3: Incorporating a Timeout Case Using time.After

Modify the `main` function to utilize a select statement. In this statement, the first case listens for a message from the channel, while the second case uses `time.After` to enforce a timeout. This approach is ideal for scenarios where a RESTful API call, for example, should not wait more than one second:

```go theme={null}
package main

import (
    "fmt"
    "time"
)

func main() {
    ch1 := make(chan int)
    go sendValue(ch1)

    select {
    case msg := <-ch1:
        fmt.Println(msg)
    case <-time.After(1 * time.Second):
        fmt.Println("select timeout")
    }
}

func sendValue(ch1 chan int) {
    ch1 <- 10
}
```

When you run this program, the output will display `10` because the channel operation completes immediately.

### Step 4: Simulating a Delayed Response

To observe the timeout behavior, adjust the `sendValue` function to delay sending the value for more than one second (for instance, three seconds). This adjustment ensures that the select statement triggers the timeout case:

```go theme={null}
package main

import (
    "fmt"
    "time"
)

func main() {
    ch1 := make(chan int)
    go sendValue(ch1)

    select {
    case msg := <-ch1:
        fmt.Println(msg)
    case <-time.After(1 * time.Second):
        fmt.Println("select timeout")
    }
}

func sendValue(ch1 chan int) {
    time.Sleep(3 * time.Second)
    ch1 <- 10
}
```

To run the program, execute the following command in your terminal:

```bash theme={null}
go run main.go
```

The resulting output will be:

```bash theme={null}
select timeout
```

In this scenario, the timeout case is executed after one second because the goroutine’s delay surpasses the specified duration.

<Callout icon="lightbulb">
  The `time.After` function is an elegant tool for implementing timeouts in concurrent operations. It is especially useful in non-blocking scenarios where you want to avoid indefinite waiting during lengthy API or IO calls.
</Callout>

## Summary

The `time.After` function is a powerful mechanism for handling timeouts in Golang. By integrating it within a select statement, you can ensure that your code does not stall during prolonged API or IO operations, thus making your applications more responsive and fault-tolerant.

Happy coding, and see you in the next lesson!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-golang/module/5a3833bd-1030-4e53-a886-007bd0b9fbf3/lesson/41dcb30b-9f84-4943-b3f5-5a55e644e72a" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/advanced-golang/module/5a3833bd-1030-4e53-a886-007bd0b9fbf3/lesson/4ddce47a-d61a-42ec-a9fd-67c7c8a4c40b" />
</CardGroup>
