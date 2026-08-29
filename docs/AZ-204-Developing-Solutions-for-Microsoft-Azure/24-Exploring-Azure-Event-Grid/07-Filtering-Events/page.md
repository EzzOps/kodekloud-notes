# Filtering Events

Source: https://notes.kodekloud.com/docs/AZ-204-Developing-Solutions-for-Microsoft-Azure/Exploring-Azure-Event-Grid/Filtering-Events/page

This article explains how to filter events in Azure Event Grid to deliver only relevant events to your endpoint.

In this lesson, we explore how Azure Event Grid filters incoming events so that only relevant events are delivered to your endpoint. By default, all event types from the event source are sent to the subscribed endpoint. However, you can customize this behavior by configuring Event Grid to deliver only selected event types, reducing unnecessary noise and ensuring that your application processes only the events it needs.

<Frame>
  <img alt="The image shows a comparison between &#x22;Default&#x22; and &#x22;Option&#x22; event type filtering, with &#x22;Default&#x22; sending all event types to the endpoint and &#x22;Option&#x22; allowing specific event types to be sent." />
</Frame>

For example, if you prefer to receive only deletion events from a storage account rather than every possible event, you can set up targeted filtering rules.

## Subject Filtering

Subject filtering allows for refining events based on a resource path or subject. This is accomplished by specifying a starting or ending value for the event subject. If you work with Azure Blob Storage and need to receive events solely from specific containers (such as default or test containers), subject filtering enables you to restrict events to just those containers while ignoring all others.

<Frame>
  <img alt="The image is about &#x22;Subject Filtering&#x22; and includes two colored boxes. The first box explains specifying starting or ending values for a subject, and the second provides an example of filtering subjects for specific events." />
</Frame>

## Advanced Filtering

Advanced filtering offers the capability to inspect values within an event's data field for more granular filtering. This method allows you to filter based on metadata, payload content, or other specific event properties. Supported comparison operators include:

* string contains
* string ends with
* string does not begin with
* string does not end with
* is null
* number is in
* boolean equals

Using these operators, you can construct filters for complex JSON arrays within event data. This is especially useful when targeting properties like access tier, blob type, or content length exceeding a specified threshold.

<Frame>
  <img alt="The image is a slide titled &#x22;Advanced Filtering&#x22; with two colored boxes. The left box says &#x22;Filter by values in data fields,&#x22; and the right box says &#x22;Specify comparison operators for precise filtering." />
</Frame>

> **lightbulb** Advanced filtering is ideal for scenarios requiring precise control over event processing. By leveraging various comparison operators, you can effectively handle complex events tailored to your application needs.

## Configuring Filters in the Azure Portal

To configure these filters, navigate to your event subscription in the Azure Event Grid setup within the Azure Portal. Under the **Filters** section, you can view and manage the available event types – a critical step in limiting the events that reach your endpoint.

If you enable subject filtering, you can specify a particular container name to further fine-tune which events are delivered. For instance, you might restrict events to those where the subject ends with a specific extension, and you even have the option for case-sensitive matching when needed.

<Frame>
  <img alt="The image shows a Microsoft Azure portal page for configuring an event subscription with filters for event types and subject filters. It includes options for enabling subject filtering and advanced filters." />
</Frame>

### Using Advanced Filtering in Practice

Advanced filtering is also available for a detailed inspection of event data. For example, when reviewing a captured event within a Logic App, you might observe a property in the event’s data, such as API. To filter for events where data.API equals "put blob," you would create an advanced filter with that condition. This approach empowers you to process complex JSON arrays effectively, like filtering based on blob properties.

<Frame>
  <img alt="The image shows a Microsoft Azure portal interface displaying the run history of a logic app named &#x22;webhook-ide-oauth.&#x22; It includes details of HTTP requests received, with parameters and outputs visible on the right side." />
</Frame>

> **triangle-alert** Ensure that your filter conditions are meticulously tested to avoid inadvertently excluding important events from your workflow.

By configuring these filters, Azure Event Grid ensures that your application processes only the events relevant to your business logic, improving performance and reducing unnecessary load.

As we conclude our discussion on Event Grid filtering, proceed to the next section where we cover Event Hubs for further insights into event-driven architectures.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-204-developing-solutions-for-microsoft-azure/module/12346ae4-1f5e-4115-bb36-f10f47c8026e/lesson/586ed7a2-f02e-412c-8879-dc0d33212762)
