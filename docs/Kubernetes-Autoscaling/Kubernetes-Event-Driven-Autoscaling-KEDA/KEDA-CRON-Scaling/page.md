# KEDA CRON Scaling

Source: https://notes.kodekloud.com/docs/Kubernetes-Autoscaling/Kubernetes-Event-Driven-Autoscaling-KEDA/KEDA-CRON-Scaling/page

Explains KEDA Cron scaler for time-based Kubernetes pod scaling, using cron expressions and timezones to enforce desired replica counts during scheduled windows and revert afterward.

Welcome — this lesson explains how to use KEDA's Cron scaler to schedule Kubernetes pod replicas based on time. Cron-based scaling is ideal for predictable traffic patterns (for example, a coffee shop that opens at 6:00 AM daily, or scheduled promotions). With KEDA's Cron trigger you can:

* Select a timezone from the IANA Time Zone Database.
* Define cron expressions for when scaling should start and when it should end.
* Set the exact replica count (`desiredReplicas`) for the scheduled window.

Start and end times must be distinct: KEDA applies the scheduled replica count between the `start` and `end` boundaries and removes that constraint afterwards so the workload can resume its normal scaling behavior.

<Frame>
  <img alt="An infographic titled &#x22;KEDA Cron&#x22; showing a stylized framed list of scheduled items. A blue circle labeled &#x22;Cron&#x22; sits to the left and a callout to the right reads &#x22;Start and end time should be distinct.&#x22;" />
</Frame>

## Why use Cron scaling?

If you can predict times of higher load, pre-warming or pre-scaling your workloads reduces cold-start latency and improves user experience. KEDA Cron scaling provides a deterministic window to guarantee capacity during those events and to return to lower capacity afterward.

## How the Cron trigger works

A KEDA Cron trigger accepts the following key metadata fields:

* `timezone` — an IANA time zone string (for example, `Asia/Kolkata`). Use values from the IANA Time Zone Database.
* `start` and `end` — cron expressions that define when the scheduled replica count should be applied and when it should stop being enforced.
* `desiredReplicas` — the number of replicas to maintain during the scheduled period (KEDA expects this as a string).

Cron expressions in KEDA follow the standard 5-field format:

minute hour day-of-month month day-of-week

Use 24-hour format for the `hour` field.

### Cron field reference

| Field        | Range | Description                      |
| ------------ | ----- | -------------------------------- |
| minute       | 0-59  | Minute of the hour               |
| hour         | 0-23  | Hour of the day (24-hour format) |
| day-of-month | 1-31  | Day of the month                 |
| month        | 1-12  | Month number                     |
| day-of-week  | 0-7   | Day of week (0 or 7 = Sunday)    |

Example: `0 6 * * *` → run at 06:00 every day.

### Example trigger metadata

```yaml theme={null}
triggers:
- type: cron
  metadata:
    # Required
    timezone: Asia/Kolkata        # Value from the IANA Time Zone Database
    start: "0 6 * * *"           # At 06:00 (6:00 AM)
    end: "0 20 * * *"            # At 20:00 (8:00 PM)
    desiredReplicas: "10"        # Note: value must be a string
```

<Callout icon="lightbulb">
  Always use a valid IANA timezone string for `timezone` and provide cron expressions in 24-hour format. Quote cron expressions and `desiredReplicas` to avoid parsing issues.
</Callout>

## Example ScaledObject

Below is a complete example `ScaledObject` that applies the cron schedule above. This manifest includes:

* `minReplicaCount: 0` to allow scaling down to zero outside scheduled windows.
* `cooldownPeriod` (seconds) — the time KEDA waits after the last active trigger before scaling down. This helps prevent rapid down-scaling after brief spikes.

```yaml theme={null}
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: example-cron-scaledobject
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app-deployment
  minReplicaCount: 0
  cooldownPeriod: 300          # 300 seconds (5 minutes) before scaling down after inactivity
  triggers:
  - type: cron
    metadata:
      timezone: Asia/Kolkata
      start: "0 6 * * *"
      end: "0 20 * * *"
      desiredReplicas: "10"
```

## Notes on cooldown and behavior

* `cooldownPeriod` is the number of seconds KEDA waits after the last active trigger observation before attempting to scale down. For long scheduled windows (e.g., 06:00–20:00) this setting usually does not impact the scheduled period, but it can help avoid oscillation when other scalers are active.
* When the `end` cron expression matches, KEDA removes the scheduled desired replica count and other scalers (or the default behavior) determine the replica count. That may trigger a gradual scale-down according to your configuration.

## When to use KEDA Cron scaler

* Predictable, time-based traffic (daily business hours, scheduled promotions, batch processing windows).
* Need to guarantee minimum capacity for a known window (pre-warming).
* Desire to scale to zero outside scheduled windows to save resources.

## References

* KEDA Cron scaler: [https://keda.sh/docs/latest/scalers/cron/](https://keda.sh/docs/latest/scalers/cron/)
* IANA Time Zone Database: [https://www.iana.org/time-zones](https://www.iana.org/time-zones)
* Kubernetes Deployments: [https://kubernetes.io/docs/concepts/workloads/controllers/deployment/](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-autoscaling/module/c218f836-7d7e-425b-a8b7-0148914eb040/lesson/9e740c2e-e6fe-4358-9ad6-710868c57124" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kubernetes-autoscaling/module/c218f836-7d7e-425b-a8b7-0148914eb040/lesson/0dfeafae-cad9-4b5f-9afe-16ade758ed6d" />
</CardGroup>
