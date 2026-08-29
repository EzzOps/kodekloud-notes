# Understanding Caching and Caching Strategies

Source: https://notes.kodekloud.com/docs/AWS-Certified-CloudOps-Engineer-Associate/Domain-2-Reliability-and-BCP/Understanding-Caching-and-Caching-Strategies/page

This article explains caching techniques and strategies to enhance application performance, reduce latency, and manage data retrieval efficiently.

Welcome to this comprehensive lesson on caching—a key technique that significantly enhances application performance and scalability by reducing latency and offloading repeated, expensive database queries.

Caching works by storing frequently accessed data in an in-memory database instead of continuously querying the primary database. This approach speeds up data retrieval, reduces resource consumption, and minimizes the load on your main database.

<Frame>
  ![The image illustrates the purpose of caching, showing a flow from a user device to servers, then to a cache, and finally to a database. It highlights the role of caching in optimizing data retrieval processes.](../../../../images/kodekloud.com/kk-media/image/upload/v1752860189/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Understanding-Caching-and-Caching-Strategies/caching-data-retrieval-flow-diagram.jpg)
</Frame>

In the diagram above, the cache resides between your application servers and your database, storing static or infrequently changed data such as historical data or daily averages (e.g., average stock prices from previous days). This in-memory retrieval mechanism effectively reduces latency and improves overall performance. Thanks to its superior speed, an in-memory database can perform better than a read replica of a traditional database.

<Frame>
  ![The image illustrates the importance of caching, highlighting four benefits: reduced latency, improved performance, reduced load, and cost efficiency.](../../../../images/kodekloud.com/kk-media/image/upload/v1752860190/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Understanding-Caching-and-Caching-Strategies/caching-benefits-latency-performance.jpg)
</Frame>

## Types of Caching

There are several types of caching used in modern applications:

1. **Database Caching:** Stores frequent database queries.
2. **Content Caching:** Saves web pages, images, videos, and PDF files.
3. **Application Caching:** Caches application-level data, such as session information or API responses.

<Frame>
  ![The image illustrates three types of caching: Database Caching, Content Caching, and Application Caching, each represented by a numbered icon.](../../../../images/kodekloud.com/kk-media/image/upload/v1752860191/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Understanding-Caching-and-Caching-Strategies/caching-types-database-content-application.jpg)
</Frame>

Even when underlying data might change, caching remains beneficial when accessed by many users. Services supporting database caching include:

* **ElastiCache:** Available with Redis or Memcached flavors.
* **Amazon DynamoDB Accelerator (DAX):** Provides microsecond response times for DynamoDB.
* **RDS Read Replicas:** Though not in-memory, they offer a form of caching. However, Redis typically delivers faster performance.

<Frame>
  ![The image lists AWS services for database caching, including ElastiCache for Redis, ElastiCache for Memcached, Amazon DynamoDB Accelerator (DAX), and Amazon RDS Read Replicas.](../../../../images/kodekloud.com/kk-media/image/upload/v1752860192/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Understanding-Caching-and-Caching-Strategies/aws-database-caching-services.jpg)
</Frame>

For networking, services such as CloudFront cache web pages and files closer to end users, while Route 53 caches DNS query responses. Additionally, Amazon's ElastiCache can be used to create an in-memory file cache for S3 or NFS (e.g., EFS), accelerating file retrieval.

Application caching is equally essential. For example, session data can be stored in DynamoDB, AWS Lambda leverages in-memory caching for warm instances, and API Gateway offers an attached cache for API responses—especially read responses.

## Caching Strategies

When implementing caching for databases, consider the following commonly used strategies:

### 1. Lazy Loading (Cache Aside)

Lazy loading, also known as cache aside, involves loading data into the cache only after a cache miss occurs. In practice, the application first queries the cache. If the data is absent, it then fetches from the database, returns the data to the user, and saves a copy in the cache for future requests.

<Frame>
  ![The image is a flowchart illustrating the "Lazy Loading (Cache Aside)" pattern, showing the process of checking if data is in the cache, retrieving it from the database if not, and storing it in the cache for future use.](../../../../images/kodekloud.com/kk-media/image/upload/v1752860193/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Understanding-Caching-and-Caching-Strategies/lazy-loading-cache-aside-flowchart.jpg)
</Frame>

<Callout icon="lightbulb">
  Cache systems like Redis or Memcached do not automatically synchronize with the database; your application must explicitly manage this process.
</Callout>

### 2. Read-Through Caching

In read-through caching, the application requests data through the cache interface. If the cache does not contain the data, the cache itself retrieves the data from the database before returning it. Although this model simplifies the application logic by centralizing data access, it is less commonly enabled by default in many in-memory databases without extra configuration.

<Frame>
  ![The image illustrates a read-through caching process, showing data flow between an application, cache, and database. If data exists in the cache, it's read from there; otherwise, it's fetched from the database.](../../../../images/kodekloud.com/kk-media/image/upload/v1752860194/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Understanding-Caching-and-Caching-Strategies/read-through-caching-process-diagram.jpg)
</Frame>

### 3. Write-Through Caching

Write-through caching updates both the cache and the database simultaneously whenever the application writes data. This method ensures data consistency and minimizes the risk of serving outdated information.

<Frame>
  ![The image illustrates a write-through caching process, showing data flow from an application to a cache and then to a database.](../../../../images/kodekloud.com/kk-media/image/upload/v1752860195/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Understanding-Caching-and-Caching-Strategies/write-through-caching-process-diagram.jpg)
</Frame>

## Cache Invalidation

Keeping the cached data fresh is critical for application accuracy and performance. Cache invalidation involves updating or removing stale cache entries. When outdated data is detected, the application may either compare it with the database or trigger a specific business logic to refresh the cache.

<Frame>
  ![The image is a diagram illustrating the process of cache invalidation, showing interactions between a client, database, and cache with actions like read, write, fill, and invalidate.](../../../../images/kodekloud.com/kk-media/image/upload/v1752860196/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Understanding-Caching-and-Caching-Strategies/cache-invalidation-diagram-client-database.jpg)
</Frame>

There are two common strategies for cache invalidation:

* **Event-Based Invalidation:** Directly invalidates cache entries immediately after a database update.
* **Time-Based Invalidation:** Uses a predetermined Time-To-Live (TTL) for cached data, after which the data is removed and refreshed on subsequent requests.

<Frame>
  ![The image illustrates types of cache invalidation, including event-based invalidation (invalidate when writing and reading) and time-based invalidation (TTL). It shows the interactions between applications, storage, and cache.](../../../../images/kodekloud.com/kk-media/image/upload/v1752860197/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Understanding-Caching-and-Caching-Strategies/cache-invalidation-types-diagram.jpg)
</Frame>

## Cache Eviction

Cache eviction is the process of determining which data should be removed when the cache reaches its capacity. For example, if your cache has a capacity of 4GB, eviction policies help decide which cached items to discard to make space for new data. Popular eviction strategies include:

* **Least Recently Used (LRU):** Evicts items that have not been accessed for the longest time.
* **Least Frequently Used (LFU):** Removes items that have the fewest accesses.
* **First In, First Out (FIFO):** Discards the oldest items in the cache to free up space.

<Frame>
  ![The image illustrates a "Cache Eviction Strategy – Least Recently Used" with an application accessing a cache containing items A, B, C, and D, arranged along a timeline.](../../../../images/kodekloud.com/kk-media/image/upload/v1752860198/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Understanding-Caching-and-Caching-Strategies/cache-eviction-strategy-lru-timeline.jpg)
</Frame>

For instance, if an application frequently accesses item B while item C is the least recently used, then item C might be evicted first.

<Frame>
  ![The image illustrates a "Least Frequently Used" cache eviction strategy, showing an application accessing a cache with items A, B, C, and D, each with different access frequencies.](../../../../images/kodekloud.com/kk-media/image/upload/v1752860200/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Understanding-Caching-and-Caching-Strategies/least-frequently-used-cache-eviction.jpg)
</Frame>

In a FIFO approach, once the cache is full, the item that was stored first is the one that gets removed when a new item is inserted.

<Frame>
  ![The image illustrates a "First In First Out" (FIFO) cache eviction strategy, showing the process of adding and removing items in a cache with three slots.](../../../../images/kodekloud.com/kk-media/image/upload/v1752860201/notes-assets/images/AWS-Certified-SysOps-Administrator-Associate-Understanding-Caching-and-Caching-Strategies/fifo-cache-eviction-strategy.jpg)
</Frame>

<Callout icon="lightbulb">
  When designing a caching strategy for your application, consider your data access patterns. Tools such as ElastiCache and Redis offer configurable eviction policies which can be adjusted based on your specific workload and performance needs.
</Callout>

## Conclusion

Caching and its associated strategies—lazy loading, read-through, write-through, cache invalidation, and cache eviction—are essential for building responsive and scalable applications. By understanding and applying the proper caching mechanisms, you can improve performance, reduce latency, and ensure your application scales efficiently under load.

Thank you for reading this lesson on caching and caching strategies. For further insights on caching and related cloud services, consider exploring the [AWS documentation](https://aws.amazon.com/documentation/) and [caching best practices](https://aws.amazon.com/caching/).

Happy caching!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-certified-sysops-administrator-associate/module/1b592900-bdef-468a-9a2b-de667b7e9cae/lesson/aff88416-6dd5-4643-9989-98b4e0b38453" />
</CardGroup>
