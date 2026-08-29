# JSON PATH 2 Wild Cards

Source: https://notes.kodekloud.com/docs/JSON-Path-Test-Free-Course/Lesson/JSON-PATH-2-Wild-Cards/page

This article provides a comprehensive guide on using the JSONPath wildcard operator for querying JSON objects and arrays effectively.

Welcome to this comprehensive guide on using the JSONPath wildcard (`*`) operator. In this lesson, you’ll discover how to apply wildcards to both JSON objects and arrays, and how to combine them for powerful queries.

<Callout icon="lightbulb">
  JSONPath implementations can differ in syntax and features. Always test your expressions with your chosen library or tool.
</Callout>

***

## Wildcards in JSON Objects

Imagine you have a JSON document with two top-level entries, `car` and `bus`, each containing `color` and `price` properties:

```json theme={null}
{
  "car": {
    "color": "blue",
    "price": "$20,000"
  },
  "bus": {
    "color": "white",
    "price": "$120,000"
  }
}
```

| Task                | JSONPath Expression | Output                   |
| ------------------- | ------------------- | ------------------------ |
| Get the car’s color | `$.car.color`       | `["blue"]`               |
| Get the bus’s color | `$.bus.color`       | `["white"]`              |
| Get **all** colors  | `$.*.color`         | `["blue","white"]`       |
| Get **all** prices  | `$.*.price`         | `["$20,000","$120,000"]` |

* **Expression**: `$.*.color`\
  **Result**: `["blue","white"]`

* **Expression**: `$.*.price`\
  **Result**: `["$20,000","$120,000"]`

***

## Wildcards in JSON Arrays

Next, consider a simple list of wheel objects:

```json theme={null}
[
  { "model": "X345ERT", "location": "front-right" },
  { "model": "X346ERT", "location": "front-left"  },
  { "model": "X347ERT", "location": "rear-right"  },
  { "model": "X348ERT", "location": "rear-left"   }
]
```

| Task                 | JSONPath Expression | Output                                      |
| -------------------- | ------------------- | ------------------------------------------- |
| First wheel’s model  | `$[0].model`        | `["X345ERT"]`                               |
| Fourth wheel’s model | `$[3].model`        | `["X348ERT"]`                               |
| All wheels’ models   | `$[*].model`        | `["X345ERT","X346ERT","X347ERT","X348ERT"]` |

* **Expression**: `$[*].model`\
  **Result**: `["X345ERT","X346ERT","X347ERT","X348ERT"]`

***

## Combining Wildcards with Property Access

You can mix object wildcards and array wildcards for nested structures. Here’s a JSON object where each vehicle has a `wheels` array:

```json theme={null}
{
  "car": {
    "color": "blue",
    "price": 20000,
    "wheels": [
      { "model": "X345ERT" },
      { "model": "X346ERT" }
    ]
  },
  "bus": {
    "color": "white",
    "price": 120000,
    "wheels": [
      { "model": "Z227KLJ" },
      { "model": "Z226KLJ" }
    ]
  }
}
```

| Task                       | JSONPath Expression     | Output                                      |
| -------------------------- | ----------------------- | ------------------------------------------- |
| Car’s 1st wheel model      | `$.car.wheels[0].model` | `["X345ERT"]`                               |
| Car’s all wheel models     | `$.car.wheels[*].model` | `["X345ERT","X346ERT"]`                     |
| Bus’s wheel models         | `$.bus.wheels[*].model` | `["Z227KLJ","Z226KLJ"]`                     |
| All vehicles’ wheel models | `$.*.wheels[*].model`   | `["X345ERT","X346ERT","Z227KLJ","Z226KLJ"]` |

* **Expression**: `$.*.wheels[*].model`\
  **Result**: `["X345ERT","X346ERT","Z227KLJ","Z226KLJ"]`

***

## Tips for Building Complex JSONPath Queries

1. Break your expression into smaller parts:
   * Test one branch (e.g., `$.car.wheels[*].model`).
   * Then test another (e.g., `$.bus.wheels[*].model`).
2. Once each part works, combine them with wildcards:
   * Final: `$.*.wheels[*].model`
3. Use online [JSONPath evaluators](https://jsonpath.com/) to verify results interactively.

<Callout icon="triangle-alert">
  Overusing deep wildcards (`$..*`) can be inefficient on large JSON documents. Optimize your path when performance matters.
</Callout>

***

## Further Reading and Tools

* JSONPath Specification: [https://goessner.net/articles/JsonPath/](https://goessner.net/articles/JsonPath/)
* JSONPath Evaluator: [https://jsonpath.com/](https://jsonpath.com/)
* [Kubernetes JSONPath Guide](https://kubernetes.io/docs/reference/kubectl/jsonpath/) for real-world examples

***

Practice creating your own JSONPath expressions with wildcards to master complex data extraction scenarios!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/json-path-test-free-course/module/114e6dee-a9f2-49f3-a0c6-cdfb92f74310/lesson/4ee22714-9402-46bf-aca6-e96b9b3428ba" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/json-path-test-free-course/module/114e6dee-a9f2-49f3-a0c6-cdfb92f74310/lesson/6554e5ac-4380-4798-8b2b-01bf77f61fd3" />
</CardGroup>
