# Cloud Functions Best Practices and Optimization

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Orchestration-Options/Cloud-Functions-Best-Practices-and-Optimization/page

Best practices for optimizing Cloud Functions performance, reliability, security including cold-start reduction, resource reuse, retries, observability, secrets and least privilege

Hello and welcome back.

This lesson explains practical best practices for optimizing Cloud Functions: improving performance, increasing reliability, and enforcing security. These recommendations are intended for teams operating multiple serverless functions in production and build on real-world integration patterns.

Goals:

* Reduce latency and cost.
* Improve resilience and observability.
* Limit blast radius with secure defaults.

## Performance: make functions fast and efficient

Focus on minimizing cold starts, reusing resources across invocations, and right-sizing compute.

Key strategies:

* Minimize cold starts
  * Keep dependencies small and trim package sizes.
  * Move expensive initialization outside of the hot path. Prefer lightweight, fast startup code.
  * Lazy-load heavy modules only when used.
* Reuse resources across invocations
  * Initialize database clients, HTTP clients, or connection pools in the global scope (outside the request handler) so warm instances can reuse them.
  * If your runtime supports instance concurrency (e.g., Cloud Functions Gen 2), ensure any shared/global resources are safe for concurrent access.
* Right-size memory and CPU
  * Increasing memory often increases CPU allocation; for CPU-bound workloads this can reduce execution time.
  * Benchmark different settings to find the best cost/performance trade-off.
* Reduce outbound connections
  * Use connection pooling and shared clients to lower the number of new connections and reduce latency.

Caching and reducing connections via global variables avoids expensive reconnects. This is particularly important for databases and third-party APIs.

<Frame>
  <img alt="A presentation slide titled &#x22;Best Practices and Optimization.&#x22; It shows three colored columns—Performance, Error Handling, and Security—each with short recommendations like minimize cold starts, implement retry logic, and use service accounts." />
</Frame>

Practical examples

* Node.js (initialize client once in global scope)

```javascript theme={null}
// global scope - executed once per instance
const {Pool} = require('pg');
const pool = new Pool({ connectionString: process.env.DB_CONN });

// handler uses the shared pool
exports.handler = async (req, res) => {
  const client = await pool.connect();
  try {
    const result = await client.query('SELECT NOW()');
    res.send(result.rows);
  } finally {
    client.release();
  }
};
```

* Python (reuse client across invocations)

```python theme={null}
