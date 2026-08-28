# Cardinality

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Metrics-Data-Model/Cardinality/page

Explains metric cardinality in observability, its impact on series count, cost, and performance, and offers guidance for choosing low, medium, or high cardinality labels and strategies.

Cardinality (in metrics and observability) refers to the number of unique combinations of metric attributes, often called labels or dimensions. In practice, it describes how many distinct values those dimensions can produce — and directly affects the number of metric series your backend must store and query.

<Frame>
  <img alt="The image defines cardinality as the number of unique combinations of metric attributes (dimensions). It includes a quote design and has a copyright notice by KodeKloud." />
</Frame>

## Cardinality levels (quick summary)

| Cardinality level |                         Description | Common examples                                            | When to use                                                   |
| ----------------- | ----------------------------------: | ---------------------------------------------------------- | ------------------------------------------------------------- |
| Low               |    Few distinct values, bounded set | `HTTP status` (200, 404, 500), `region` (us-east, eu-west) | Broad monitoring and alerting; low cost                       |
| Medium            |  Moderate number of distinct values | `service name`, `instance type`, `model`                   | Segment analysis and trend detection                          |
| High              | Many unique values, often unbounded | `user_id`, `request_id`, `registration_number`             | Root-cause analysis, per-entity investigation (use sparingly) |

<Frame>
  <img alt="The image explains cardinality, distinguishing between low cardinality (small set of known values, e.g., status codes) and high cardinality (many unique values, e.g., IDs)." />
</Frame>

## Why cardinality matters

Cardinality affects cost, memory, query time, and dashboard responsiveness. Each unique combination of labels typically becomes a separate metric series:

* Low-cardinality metrics are cheap to store and fast to query.
* High-cardinality metrics can explode the number of series and increase ingestion and query costs.
* High-cardinality data is invaluable for targeted troubleshooting and identifying outliers, but requires careful design so your observability backend is not overwhelmed.

<Frame>
  <img alt="The image explains the importance of cardinality, highlighting its impact on cost, memory, performance, and its role in diagnosing anomalies and outliers. Additionally, it includes a graphic of a dashboard with charts and graphs." />
</Frame>

High-cardinality data is powerful for investigations — but must be used judiciously to balance operational cost and backend performance.

## Example: vehicle telemetry (low → high)

The following JavaScript snippet shows vehicle records where attributes vary in cardinality. This illustrates how different groupings produce different analytical granularity.

```javascript theme={null}
// Example vehicle records illustrating cardinality levels for attributes
const cars = [
  {
    "wheels": 4,                  // Low cardinality (few possible values)
    "color": "blue",              // Medium cardinality (limited palette)
    "fuel_type": "gasoline",      // Low cardinality (e.g., gas, diesel, electric)
    "make": "Toyota",             // Medium cardinality (many manufacturers)
    "model": "Camry",             // Medium cardinality (many models)
    "registration": "ABC-123-XYZ" // Very high cardinality (unique per vehicle)
  },
  {
    "wheels": 4,
    "color": "red",
    "fuel_type": "gasoline",
    "make": "Honda",
    "model": "Civic",
    "registration": "DEF-456-QRS"
  },
  {
    "wheels": 4,
    "color": "blue",
    "fuel_type": "electric",
    "make": "Tesla",
    "model": "Model 3",
    "registration": "GHI-789-TUV"
  }
];
```

* Group by `fuel_type` (low cardinality) — good for broad, cost-effective insights.
* Group by `model` (medium cardinality) — reveals more granular trends by model.
* Group by `registration` (high cardinality) — inspects specific vehicles (one point per entity).

<Frame>
  <img alt="The image shows a table titled &#x22;Analyzing Car Data by Attributes,&#x22; listing various cars with details such as registration number, make, model, color, fuel type, and kilometers run." />
</Frame>

Using different groupings yields different business questions and costs. For example:

<Frame>
  <img alt="The image shows a bar graph comparing the average kilometers run by vehicles with different fuel types: Diesel, Electric, Hybrid, and Petrol. Petrol and Diesel vehicles have the highest average kilometers, while Hybrid vehicles have the lowest." />
</Frame>

Grouping by model provides more detail than fuel type:

<Frame>
  <img alt="The image is a bar chart showing the average kilometers run by various car models, with the highest being the CR-V and X3 models exceeding 120,000 kilometers. The chart is titled &#x22;Medium Cardinality – Average Kilometers Run by Car Model.&#x22;" />
</Frame>

Grouping by `registration` (per-vehicle) is high cardinality and useful when you must pinpoint an exact entity.

## Real-world example: e-commerce

In e-commerce, datasets might include `user_id`, `loyalty_tier`, `country`, `city`, `product_category`, `purchase_channel`, and `total_spend`. Choose grouping keys based on the analysis you need:

<Frame>
  <img alt="The image displays an eCommerce dataset for cardinality analysis, featuring columns such as user ID, user type, loyalty level, location details, product category, purchase channel, and total purchase amount." />
</Frame>

* Group by `loyalty_tier` (low cardinality) to view overall trends quickly:

<Frame>
  <img alt="The image shows a bar chart titled &#x22;Low Cardinality – Total Purchases by Loyalty Status,&#x22; comparing total purchases across Gold, Platinum, and Silver loyalty statuses, with Platinum having the highest purchases." />
</Frame>

* Group by `city` (medium cardinality) for regional insights.
* Group by `user_id` (high cardinality) to surface top individual spenders or investigate an individual user issue.

High cardinality enables user-level troubleshooting and business analytics (e.g., identifying the top spender), but it increases the number of metric series.

<Frame>
  <img alt="The image presents a table describing attributes, types, cardinality, and example values, focusing on &#x22;userID&#x22; with high cardinality and &#x22;state&#x22; with low cardinality in a real-world context." />
</Frame>

<Frame>
  <img alt="The image is a table showcasing high cardinality key aspects using userID and state attributes, with userID having high cardinality and state having low cardinality. It also includes use cases related to backend load and error spikes." />
</Frame>

<Callout icon="lightbulb">
  High-cardinality metrics provide detailed, actionable insight but increase the number of metric series. Design labels to balance operational needs with backend cost and performance.
</Callout>

<Callout icon="warning">
  Warning: storing and querying high-cardinality data increases backend load. Confirm your observability backend can handle the ingestion and query volume before adding many high-cardinality labels.
</Callout>

## Practical guidance and patterns

* Use low-cardinality attributes for broad monitoring and alerting: cheaper and faster.
* Use medium cardinality for deeper trend analysis and segmentation.
* Use high-cardinality attributes sparingly for root-cause analysis or specific investigations.
* If you need per-entity visibility but want to limit metric cost:
  * Apply sampling for high-frequency entities.
  * Aggregate or bucket values (e.g., percentile or range buckets).
  * Store high-cardinality details in traces or logs and link them to aggregated metrics when necessary.
  * Use labeling strategies that avoid combinatorial explosion (e.g., avoid mixing many high-cardinality labels on a single metric).

## Summary

Cardinality is a key design decision in observability. Thoughtful selection of labels and aggregation levels ensures useful insights while keeping costs and backend load manageable. Balance granularity with practicality: instrument enough detail to troubleshoot and analyze, but avoid unnecessary high-cardinality series.

## Links and references

* OpenTelemetry metrics concepts: [https://opentelemetry.io/docs/](https://opentelemetry.io/docs/)
* Prometheus documentation (time series & labels): [https://prometheus.io/docs/introduction/overview/](https://prometheus.io/docs/introduction/overview/)
* Observability best practices: [https://landing.google.com/sre/sre-book/](https://landing.google.com/sre/sre-book/) (relevant SRE guidance)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/fffcb239-a53d-4a2c-beab-cc23c3514158/lesson/8d54f805-508c-44c2-b695-504e599ab07a" />
</CardGroup>
