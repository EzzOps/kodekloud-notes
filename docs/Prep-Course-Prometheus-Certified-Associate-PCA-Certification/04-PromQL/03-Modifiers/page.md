# Modifiers

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/PromQL/Modifiers/page

Explains PromQL modifiers offset and @ to query and anchor historical metric values and ranges for debugging, incident analysis, and retrospective inspection.

This lesson explains how to query historic metric values with PromQL modifiers. So far we've been returning the most recent value for a metric. PromQL provides two modifiers — `offset` and `@` — to look back in time or anchor queries to a specific timestamp. Use these when you need to inspect values from minutes, hours, or days in the past, or when debugging incidents that happened at a particular time.

## offset — shift relative to “now” or an anchored time

Use the `offset` modifier to retrieve a metric value from some time ago. The modifier accepts a time duration (for example, `5m` for five minutes):

```promql theme={null}
node_memory_Active_bytes{instance="node1"} offset 5m
```

<Frame>
  <img alt="The image is a table showing time unit suffixes with their meanings, including milliseconds, seconds, minutes, hours, days, weeks, and years." />
</Frame>

Supported time suffixes:

| Suffix | Meaning      |
| ------ | ------------ |
| `ms`   | milliseconds |
| `s`    | seconds      |
| `m`    | minutes      |
| `h`    | hours        |
| `d`    | days         |
| `w`    | weeks        |
| `y`    | years        |

Examples:

```promql theme={null}
