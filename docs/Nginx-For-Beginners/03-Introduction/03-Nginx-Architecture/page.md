# Nginx Architecture

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Introduction/Nginx-Architecture/page

Explains NGINX’s event-driven asynchronous architecture and how master and worker processes use non-blocking I/O and readiness notifications to handle many concurrent connections efficiently.

This lesson explains NGINX’s event-driven architecture and how it achieves high concurrency with low resource usage.

Use this simple restaurant metaphor to visualize the flow:

* Customers place orders = incoming client requests
* Waiters take orders to the kitchen = the event loop registers and dispatches events
* Chefs prepare meals = workers process requests (I/O, proxying, upstreams)
* Waiters deliver meals = worker sends the response back to the client

This asynchronous, non-blocking approach prevents any single worker from idly waiting for I/O (for example, a slow upstream or disk read). Instead of processing requests one at a time, NGINX registers interest in events and uses readiness notifications to multiplex many connections efficiently.

How NGINX handles a request (step-by-step)

1. Incoming request
   * A client sends an HTTP(S) request to the server; the connection arrives at NGINX.

2. Event loop (the waiter)
   * The worker’s event loop observes the new connection and registers events (readable, writable, timers).
   * NGINX relies on scalable OS mechanisms: on Linux it typically uses `epoll`, on BSD systems it uses `kqueue`, and on older platforms it falls back to `poll`/`select`. These mechanisms notify the event loop when I/O is ready, avoiding blocking calls.

3. Processing the event (the chef)
   * A worker process handles the work associated with that event: parse headers, proxy to upstreams, run filters, or read files from disk.
   * If an operation requires waiting (e.g., upstream response, disk I/O), the worker uses non-blocking calls and returns to the event loop so other connections can be handled in the meantime.

4. Sending the response (the waiter returns)
   * Once the required data is available, the worker writes the response to the client (using the event loop to know when the socket is writable) and continues handling other events.

Scalability comes from combining non-blocking I/O, readiness notification (epoll/kqueue), and multiple worker processes. Each worker runs its own event loop and can multiplex thousands of connections.

Multiple workers and the master process

* The master process handles configuration, privilege tasks, and worker lifecycle management (start/reload/stop).
* Each worker process runs independently and uses an event loop to manage many concurrent connections.

<Frame>
  <img alt="A diagram titled &#x22;Request Handling in Nginx&#x22; showing a Master Process at the top distributing to multiple Worker Processes, each containing an Event Loop, with incoming request/response arrows feeding the workers." />
</Frame>

Process roles at a glance

|        Process | Primary responsibilities                                                                                                | Examples / notes                                                                       |
| -------------: | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Master process | Load and validate configuration, bind privileged ports, start/stop/reload workers, handle signals for graceful restarts | Typically runs as root to bind low ports, then drops privileges for workers            |
| Worker process | Run event loop, accept connections, handle request parsing and processing, proxying to upstreams, send responses        | Each worker uses `epoll`/`kqueue` and can handle thousands of simultaneous connections |

Practical tuning tips

* For many deployments set `worker_processes` to `auto` to let NGINX use all available CPU cores:
  `worker_processes auto;`
* Use `worker_connections` to control how many concurrent connections a single worker can manage. Total concurrent connections ≈ `worker_processes * worker_connections`.
* Choose the appropriate event method (`epoll`, `kqueue`) automatically by default; explicit configuration is rarely necessary.

Why the event-driven model scales

* Non-blocking I/O prevents idle waiting on slow operations.
* Readiness notifications (epoll/kqueue) allow the event loop to efficiently discover ready sockets.
* Multiple workers let NGINX utilize multiple CPU cores without shared-state contention between event loops.

Further reading and references

* Official NGINX documentation: [https://nginx.org/en/docs/](https://nginx.org/en/docs/)
* Linux `epoll` overview: [https://man7.org/linux/man-pages/man7/epoll.7.html](https://man7.org/linux/man-pages/man7/epoll.7.html)
* BSD `kqueue` overview: [https://man.openbsd.org/kqueue](https://man.openbsd.org/kqueue)

In short:

* The master process manages configuration and the worker lifecycle.
* Worker processes run the event loop and perform non-blocking request processing.
* The event-driven model (epoll/kqueue) lets each worker handle many connections concurrently, giving NGINX its high performance and scalability.

<Callout icon="lightbulb">
  Nginx is non-blocking and asynchronous: workers don’t block waiting for I/O — they register interest in events and continue processing other connections until notified. This is the core reason NGINX can handle large numbers of concurrent clients with low resource usage.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/9e6f72d7-933d-42dd-a948-ae48d66aecb6/lesson/56033553-c70c-4935-b94a-c1c369193c0a" />
</CardGroup>
