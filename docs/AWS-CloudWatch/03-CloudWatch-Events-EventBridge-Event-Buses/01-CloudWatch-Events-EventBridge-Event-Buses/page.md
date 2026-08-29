# CloudWatch Events EventBridge Event Buses

Source: https://notes.kodekloud.com/docs/AWS-CloudWatch/CloudWatch-Events-EventBridge-Event-Buses/CloudWatch-Events-EventBridge-Event-Buses/page

This article explains Amazon EventBridges features and provides a use case for event-driven architectures in e-commerce order processing.

Amazon EventBridge (formerly CloudWatch Events) provides a fully managed event bus for building scalable, event-driven architectures. In this guide, you’ll learn how EventBridge ingests, routes, and processes events—then see it in action with an e-commerce order processing use case.

<Callout icon="lightbulb">
  EventBridge offers both a default event bus and the ability to create custom buses. You can also subscribe to partner SaaS event sources directly.
</Callout>

## Key Features of EventBridge

| Feature                           | Description                                                                                           |
| --------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Advanced Routing and Patterns     | Use content-based filters and transforms to route specific events to the right targets.               |
| Reliable Ingestion and Delivery   | Benefit from high throughput, built-in retries, and durable delivery guarantees.                      |
| Flexible Event Sources            | Connect AWS services, custom applications, and third-party SaaS partners on the same event bus.       |
| Schema Registry and Code Bindings | Define, discover, and enforce JSON schemas—then auto-generate client libraries in multiple languages. |

<Callout icon="triangle-alert">
  Be sure to clean up unused rules, buses, and schemas to avoid incurring unexpected charges. See [EventBridge pricing](https://aws.amazon.com/eventbridge/pricing/).
</Callout>

## Real-World Use Case: Order Processing Notifications

Imagine an e-commerce site where, after a successful payment, warehouse staff automatically receive shipping instructions:

1. A customer places an order via your website, running on an Auto Scaling group of EC2 instances.
2. The application publishes a `PaymentSucceeded` event to a custom EventBridge bus.
3. An EventBridge rule matches on `"detail-type": ["PaymentSucceeded"]` and forwards the event to a Lambda function.
4. The Lambda function formats order details and sends an email to the warehouse team.
5. Warehouse staff receive the notification, pack the items, and dispatch the shipment.

<Frame>
  ![The image illustrates a real-world use case of AWS EventBridge, showing a flow from user interaction through an auto-scaling group, successful payment, event triggering, and rule processing with a Lambda function, leading to email notifications and warehouse updates.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862422/notes-assets/images/AWS-CloudWatch-CloudWatch-Events-EventBridge-Event-Buses/aws-eventbridge-use-case-flow-diagram.jpg)
</Frame>

### Sample EventBridge Rule (AWS CLI)

```bash theme={null}
