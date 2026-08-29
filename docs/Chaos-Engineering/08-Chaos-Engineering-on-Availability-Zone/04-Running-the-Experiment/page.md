# Running the Experiment

Source: https://notes.kodekloud.com/docs/Chaos-Engineering/Chaos-Engineering-on-Availability-Zone/Running-the-Experiment/page

Guide to running an AWS Fault Injection Service experiment triggering RDS failover while monitoring CloudWatch and X‑Ray to validate multi‑AZ resilience and recovery

Before injecting faults, we first establish the steady state so we can compare behavior during and after the experiment.

Start a browser-based load test that issues requests to the pet site and let it run for about 10 minutes. The test writes logs to the console; a representative excerpt looks like this:

```text theme={null}
time="2024-08-18T08:24:56Z" level=error msg="Uncaught (in promise) navigating frame to \"http:///\": Cannot navigate to invalid URL (-3)" executor=constant-vus scenario=browser
running (00m13.0s), 4/4 VUs, 93 complete and 0 interrupted iterations
browser [ 1 ] 4 VUs 00m13.0s/16m39s
time="2024-08-18T08:24:58Z" level=error msg="Uncaught (in promise) navigating frame to \"http:///\": Cannot navigate to invalid URL (-3)" executor=constant-vus scenario=browser
...
```

After roughly 10 minutes the run summary shows the test in steady progress:

```text theme={null}
time="2024-08-18T08:35:36Z" level=error msg="Uncaught (in promise) navigating frame to \"http:///\": Cannot navigate to invalid URL (-3 2000)" executor=constant-vus scenario=browser
running (10m52.0s), 4/4 VUs, 4643 complete and 0 interrupted iterations
browser    [ 65% ] 4 VUs  10m52.0s/16m39s
...
running (10m53.0s), 4/4 VUs, 4651 complete and 0 interrupted iterations
```

With the load running and steady, inspect application telemetry and capture steady-state values for the key observability signals:

* X-Ray trace map (PGSQL query): latency under 1 ms and \~139 requests/min (10-minute window).
* Custom CloudWatch dashboard (easy impairment dashboard): 15-minute view shows zero UnHealthyHostCount and all DB connections pointing to the writer node.

We’ve captured steady-state metrics; next we run the easy power-interruption experiment using AWS Fault Injection Service (FIS).

From the FIS experiment template, generate a preview of targets. The preview lists the actual resources the experiment may affect — use it to validate scope and plan mitigation.

<Callout icon="lightbulb">
  Use the preview to confirm which resources will be targeted and to ensure you’re prepared for the potential impact before starting the experiment.
</Callout>

The preview includes target details such as the custom role, auto scaling groups, EC2 instances, RDS cluster, and subnets:

<Frame>
  <img alt="A screenshot of the AWS Resilience Hub web console on the Fault Injection Service &#x22;Experiment templates&#x22; page, showing a Resources list with items like EC2 instances, autoscaling groups, RDS cluster, subnets, and an IAM role. The browser window also shows AWS navigation and multiple tabs at the top." />
</Frame>

Representative ARNs from the preview:

```text theme={null}
arn:aws:iam::877559718675:role/FisServerless-FISDummyRoleForASG3A1FA08C-lacm68B8H06B
arn:aws:autoscaling:ap-southeast-1:877559718675:autoScalingGroup:d593bb05-61b2-4f6a-b466-5b9779906d3d:autoScalingGroupName/Services-ecsEc2PetSearchA
arn:aws:autoscaling:ap-southeast-1:877559718675:autoScalingGroup:d4739adc-ed50-4b60-aecc-23fbe5a70131:autoScalingGroupName/eks-eksPetsiteASGClusterNod
arn:aws:ec2:ap-southeast-1:877559718675:instance/i-0352a49b56f8b4f45
arn:aws:ec2:ap-southeast-1:877559718675:instance/i-0b9f3d7ed567e7bb9
arn:aws:rds:ap-southeast-1:877559718675:cluster:services-databaseb269d8bb-jq76x92swjq0
arn:aws:ec2:ap-southeast-1:877559718675:instance/i-0352a49b56f8b4f45
arn:aws:ec2:ap-southeast-1:877559718675:instance/i-0b9f3d7ed567e7bb9
arn:aws:ec2:ap-southeast-1:877559718675:subnet/subnet-06cd6eb4ea4c59f21
arn:aws:ec2:ap-southeast-1:877559718675:subnet/subnet-08028330e6e68f408
```

Start the experiment. The FIS action summary lists each planned step and its status (for example: Failover-RDS, Pause-ASG-Scaling, Pause-ElastiCache, etc.):

<Frame>
  <img alt="A screenshot of the AWS Resilience Hub Fault Injection Service console showing an &#x22;Actions summary&#x22; table listing experiment actions (Failover-RDS, Pause-ASG-Scaling, Pause-ElastiCache, etc.) with their statuses and start times. The left sidebar shows navigation for Resilience management and Resilience testing (Experiments)." />
</Frame>

<Callout icon="warning">
  Some templates include an ElastiCache pause step. If your environment does not use ElastiCache, FIS skips that action and continues. Verify the preview to confirm resource availability before execution.
</Callout>

As the experiment runs, RDS failover is triggered: writer and reader roles begin to swap. Re-check the same metrics you used for steady state during the disruption window:

* X-Ray trace map (10-minute window): you should observe a drop in requests during the failover window.
* CloudWatch easy impairment dashboard (10-minute view): you will likely see RDS connection shifts and a transient increase in UnHealthyHostCount.

Monitor CloudWatch widgets while the experiment runs:

<Frame>
  <img alt="A screenshot of an AWS CloudWatch dashboard (AZImpairmentDashboard) showing multiple metric widgets—ALB HTTP 5XX/4XX codes, Active Connections, ProcessedBytes, UnHealthyHostCount and RDS Database Connections—displayed as small line charts. The console header shows the ap‑southeast‑1 region and a custom 10‑minute time range." />
</Frame>

Despite telemetry changes, the website can remain functional for end users (for example, completing UI flows like adopting pets) because of a resilient multi-AZ architecture and proper failover behavior. Controlled fault-injection tests are a repeatable alternative to an ad-hoc disaster recovery drill and can reveal configuration issues such as AZ-specific dependencies.

After the experiment finishes, verify recovery across observability tools:

* X-Ray trace map returns to normal request volume and latency.
* RDS cluster shows that roles have been swapped and the cluster is healthy.
* CloudWatch metrics return to steady-state levels.

Check trace-level details to confirm request patterns recovered:

<Frame>
  <img alt="A screenshot of the AWS CloudWatch console showing the X‑Ray Trace Map and a selected &#x22;PGSQL Query&#x22; details panel with graphs for latency, request count, and fault rate. The left sidebar shows CloudWatch navigation items (Alarms, Logs, Metrics, X‑Ray traces)." />
</Frame>

RDS console confirms instance roles and health:

<Frame>
  <img alt="A screenshot of the AWS Management Console on the Amazon RDS Databases page, showing a list of three Aurora PostgreSQL instances (regional cluster, writer, and reader) with their statuses, regions, and sizes. The left sidebar displays RDS navigation options and a banner at the top advertises Aurora I/O‑Optimized." />
</Frame>

The Database Connections chart clearly shows the role swap: the writer node's connections drop while the reader node's connections increase briefly, then both normalize:

<Frame>
  <img alt="A CloudWatch dashboard line chart titled &#x22;RDS Database Connections&#x22; showing two series: a blue line falling from about 27 connections to 0 and an orange line rising from 0 to roughly 28 over a short time window. The legend at the bottom shows instance identifiers and a timestamp (2024-08-18 08:35 UTC)." />
</Frame>

Key metrics and checks to capture (before, during, after)

| Metric / Signal              | Why it matters                                 | Where to check                            |
| ---------------------------- | ---------------------------------------------- | ----------------------------------------- |
| Request rate & error rate    | Detect user impact and recovery                | Load test logs, CloudWatch ALB metrics    |
| DB request latency & counts  | Detect DB performance and role changes         | X-Ray trace map, CloudWatch RDS metrics   |
| RDS connections per instance | Confirm failover and connection redistribution | CloudWatch RDS Database Connections chart |
| UnHealthyHostCount & ALB 5XX | Identify transient backend failures            | CloudWatch easy impairment dashboard      |
| Resource targets             | Ensure correct scope and mitigate impact       | FIS preview ARNs and resource list        |

Summary

* Captured a steady-state baseline (low latency, stable request rates).
* Previewed and validated FIS experiment targets before running the fault-injection template.
* The experiment caused a short RDS failover and temporary telemetry perturbations (reduced requests, brief UnHealthyHostCount spike), but the site remained functional thanks to multi-AZ resilience.
* All metrics returned to normal after the experiment, confirming automatic failover and recovery.

References and further reading

* [AWS Fault Injection Service (FIS)](https://docs.aws.amazon.com/fis/latest/userguide/what-is-fis.html)
* [AWS X-Ray Developer Guide](https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html)
* [Amazon RDS Documentation](https://docs.aws.amazon.com/rds/index.html)
* [Amazon ElastiCache Overview](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/WhatIs.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/chaos-engineering/module/e28ed74d-a0c9-4dbd-9950-2b6f83cd8511/lesson/4cf41e07-586a-4337-8295-1e86dc080365" />
</CardGroup>
