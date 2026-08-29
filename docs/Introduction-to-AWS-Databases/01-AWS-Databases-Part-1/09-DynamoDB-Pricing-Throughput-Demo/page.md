# DynamoDB Pricing Throughput Demo

Source: https://notes.kodekloud.com/docs/Introduction-to-AWS-Databases/AWS-Databases-Part-1/DynamoDB-Pricing-Throughput-Demo/page

Demonstrates modifying DynamoDB table capacity, estimating RCUs and WCUs, choosing on demand or provisioned modes, configuring autoscaling, and validating settings with historical metrics and cost estimates

In this lesson we demonstrate how to modify pricing and throughput settings for an existing Amazon DynamoDB table. When creating a table you set capacity options up front, but you can also edit them later in the console — for example, open a `Products` table, go to "Additional settings", and click **Edit** to change capacity mode, provisioned throughput, and autoscaling.

This guide covers:

* DynamoDB capacity modes and use cases
* How to estimate read and write capacity (RCUs/WCUs)
* Provisioned throughput and autoscaling settings in the console
* Using historical metrics to validate your configuration

For reference, see the official DynamoDB documentation and pricing:

* [Amazon DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
* [DynamoDB Pricing](https://aws.amazon.com/dynamodb/pricing/)

## Capacity modes: On-demand vs Provisioned

DynamoDB supports two capacity modes. Use the table below to quickly compare them and pick the one that matches your workload.

| Capacity mode | Best for                                                        | Billing model               | Notes                                                                                                              |
| ------------- | --------------------------------------------------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| On-demand     | Unpredictable, spiky traffic or new apps with unknown demand    | Pay per request             | Simple to use — you pay for actual reads/writes. Typically more expensive per operation than provisioned capacity. |
| Provisioned   | Predictable, steady workloads where you can estimate throughput | Pay for allocated RCUs/WCUs | Cheaper per operation for steady loads, but requires setting read and write capacity and optionally autoscaling.   |

<Frame>
  <img alt="A screenshot of the AWS DynamoDB console on the &#x22;Edit read/write capacity&#x22; page showing capacity mode options, with &#x22;On-demand&#x22; selected. The page includes &#x22;Provisioned&#x22; vs &#x22;On-demand&#x22; choices and a &#x22;Save changes&#x22; button." />
</Frame>

## Estimating RCUs and WCUs (capacity calculator)

If you choose provisioned mode, you must set Read Capacity Units (RCUs) and Write Capacity Units (WCUs). Use the capacity calculator or the formulas below to estimate requirements based on item size and request pattern.

Inputs for the example:

* Average item size: 8 KB
* Expected reads per second: 20 (strongly consistent)
* Expected writes per second: 30

Calculation rules:

* Strongly consistent read = `ceil(item_size / 4 KB)` RCUs per read
* Eventually consistent read = half the RCUs of a strongly consistent read
* Write = `ceil(item_size / 1 KB)` WCUs per write

Example calculation (8 KB items):

```text theme={null}
RCUs:
  Strongly consistent read of 8 KB = ceil(8 KB / 4 KB) = 2 RCUs per read
  Total RCUs needed = 20 reads/sec × 2 = 40 RCUs

WCUs:
  Write of 8 KB = ceil(8 KB / 1 KB) = 8 WCUs per write
  Total WCUs needed = 30 writes/sec × 8 = 240 WCUs
```

Use the calculator to get estimated monthly costs for those units to avoid surprises on your bill.

> **lightbulb** Use the capacity calculator to estimate RCUs and WCUs based on item sizes and read/write patterns. Note: eventual consistency reduces RCU consumption by half compared to strongly consistent reads.

Under the Table capacity section in the console, enter the provisioned values from the example: Read capacity = `40`, Write capacity = `240`.

## Autoscaling for provisioned mode

Autoscaling lets DynamoDB adjust provisioned throughput automatically in response to traffic, keeping utilization near your target while respecting configured minimum and maximum bounds.

Key autoscaling settings:

| Setting            | Purpose                                               | Typical values                    |
| ------------------ | ----------------------------------------------------- | --------------------------------- |
| Minimum capacity   | Lower bound for scaling down                          | e.g., `1`                         |
| Maximum capacity   | Upper bound for scaling up                            | Set based on expected peak demand |
| Target utilization | Desired % of provisioned capacity that should be used | Commonly `70%`                    |

<Frame>
  <img alt="A screenshot of the AWS console showing DynamoDB table capacity settings. It displays read/write capacity units, autoscaling toggles, and fields for minimum/maximum capacity and target utilization." />
</Frame>

Autoscaling adjusts capacity when observed usage consistently deviates from the target utilization:

* If utilization > target, autoscaling increases provisioned units up to the maximum.
* If utilization \< target, it may scale down, but not below the minimum.

<Frame>
  <img alt="A screenshot of the AWS console showing DynamoDB write capacity auto-scaling settings (Auto scaling set to &#x22;On&#x22;) with fields for minimum (1), maximum (10) capacity units and target utilization (70%). Below are panels for historical read and write usage vs current unit selection." />
</Frame>

Use the console’s historical usage graphs alongside the capacity calculator to choose sensible minimums, maximums, and target utilization. If your table has no historical traffic, graphs will be empty until requests are observed.

> **warning** Changing capacity mode or scaling limits can affect costs and throttling behavior. Review historical metrics and cost estimates before switching modes or setting large max capacity values.

## Practical recommendations

* Choose On-demand for unpredictable or early-stage workloads to avoid under-provisioning.
* Choose Provisioned with autoscaling for predictable workloads where cost optimization is important.
* Always validate with historical usage graphs and the capacity calculator to set realistic RCUs/WCUs and autoscaling bounds.
* Monitor CloudWatch metrics (ConsumedCapacityUnits, ThrottledRequests) to ensure your configuration meets application needs.

Further reading:

* [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
* [DynamoDB Autoscaling](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/AutoScaling.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/introduction-to-aws-databases/module/001734a9-f7c2-4943-83a3-d64621fedfd2/lesson/070e7e70-c262-4d28-83c4-030734f3f27e)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/introduction-to-aws-databases/module/001734a9-f7c2-4943-83a3-d64621fedfd2/lesson/0424181a-e703-4930-824d-8ba879eecdc5)
